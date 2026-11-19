# A FastAPI service that wraps rclpy (Jazzy)

A narrow HTTP and WebSocket API for `my_robot`: status, a clamped drive command with a watchdog,
a service call and an MJPEG stream. One rclpy node spins in a background thread; uvicorn runs the
app in the main thread. For Ubuntu 24.04, Python 3.12, Jazzy, FastAPI 0.101 or newer.

## Install

```bash
sudo apt install python3-fastapi python3-uvicorn   # Ubuntu 24.04: FastAPI 0.101, uvicorn 0.27
```

`pip install` into the system Python is refused on 24.04 (PEP 668); for newer versions use
`python3 -m venv --system-site-packages .venv` after sourcing `/opt/ros/jazzy/setup.bash`, so
rclpy stays importable. In the `ament_python` package `my_robot_web`, add `<exec_depend>` on
`rclpy`, `geometry_msgs`, `nav_msgs`, `sensor_msgs`, `std_srvs`, `python3-fastapi` and
`python3-uvicorn` (all rosdep keys) and a console script `server = my_robot_web.server:main`.

## The threading model

- rclpy callbacks run in the executor thread, FastAPI `def` endpoints in a thread pool, `async def`
  endpoints and WebSockets on the event loop. Shared data crosses only through locked methods.
- Never `rclpy.spin_until_future_complete(node, ...)` a node another executor spins: it moves
  the node into a second executor and the background thread stops serving it. Await the
  service future on the event loop instead (`call_service` below).
- Never block the event loop: no `time.sleep` or `future.result()` waits in `async def`.
- `SignalHandlerOptions.NO` leaves Ctrl-C to uvicorn, which then runs the shutdown half of
  `lifespan`; rosbridge starts rclpy the same way.

## `my_robot_web/server.py`

```python
"""HTTP and WebSocket API for my_robot, backed by one rclpy node."""
import asyncio
import math
import threading
from contextlib import asynccontextmanager

import rclpy
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry
from pydantic import BaseModel, Field
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.signals import SignalHandlerOptions
from sensor_msgs.msg import CompressedImage
from std_srvs.srv import Trigger


class WebBridgeNode(Node):
    """Owns every ROS endpoint; web handlers call its thread-safe methods."""

    def __init__(self):
        super().__init__("my_robot_web")
        self.max_linear = self.declare_parameter("max_linear", 0.3).value  # m/s, example
        self.max_angular = self.declare_parameter("max_angular", 1.0).value  # rad/s, example
        self.command_timeout = self.declare_parameter("command_timeout", 0.5).value  # s
        self._lock = threading.Lock()
        self._odom = None
        self._jpeg = None
        self._last_motion = None  # time of the last non-zero command
        self._cmd_pub = self.create_publisher(TwistStamped, "/cmd_vel", 10)
        self.create_subscription(Odometry, "/odom", self._on_odom, 10)
        self.create_subscription(
            CompressedImage, "/camera/image_raw/compressed", self._on_image,
            qos_profile_sensor_data)
        self.reset_client = self.create_client(Trigger, "/my_robot/reset_odometry")
        self.create_timer(0.1, self._watchdog)

    def _on_odom(self, msg):
        p, t = msg.pose.pose.position, msg.twist.twist
        snapshot = {"x": p.x, "y": p.y, "linear": t.linear.x, "angular": t.angular.z}
        with self._lock:
            self._odom = snapshot

    def _on_image(self, msg):
        if "jpeg" in msg.format:
            with self._lock:
                self._jpeg = bytes(msg.data)

    def _watchdog(self):
        with self._lock:
            last = self._last_motion
        if last is not None and \
                (self.get_clock().now() - last).nanoseconds > self.command_timeout * 1e9:
            self.drive(0.0, 0.0)

    def latest_odom(self):
        with self._lock:
            return self._odom

    def latest_jpeg(self):
        with self._lock:
            return self._jpeg

    def drive(self, linear, angular):
        if not (math.isfinite(linear) and math.isfinite(angular)):
            linear = angular = 0.0  # min/max would turn NaN into full speed
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "base_link"
        msg.twist.linear.x = max(-self.max_linear, min(self.max_linear, linear))
        msg.twist.angular.z = max(-self.max_angular, min(self.max_angular, angular))
        moving = msg.twist.linear.x != 0.0 or msg.twist.angular.z != 0.0
        with self._lock:
            self._last_motion = self.get_clock().now() if moving else None
        self._cmd_pub.publish(msg)


async def call_service(client, request, timeout_s):
    """Await an rclpy service call from the event loop without blocking it."""
    loop = asyncio.get_running_loop()
    done = loop.create_future()

    def resolve(ros_future):
        if done.done():
            return
        if ros_future.exception() is not None:
            done.set_exception(ros_future.exception())
        else:
            done.set_result(ros_future.result())

    ros_future = client.call_async(request)
    # The done callback runs in the executor thread; hop to the event loop thread
    ros_future.add_done_callback(lambda f: loop.call_soon_threadsafe(resolve, f))
    try:
        return await asyncio.wait_for(done, timeout_s)
    except TimeoutError:
        client.remove_pending_request(ros_future)
        raise


@asynccontextmanager
async def lifespan(app):
    rclpy.init(signal_handler_options=SignalHandlerOptions.NO)
    node = WebBridgeNode()
    executor = SingleThreadedExecutor()
    executor.add_node(node)
    spin_thread = threading.Thread(target=executor.spin, daemon=True)
    spin_thread.start()
    app.state.node = node
    try:
        yield
    finally:
        node.drive(0.0, 0.0)
        executor.shutdown()
        spin_thread.join(timeout=2.0)
        node.destroy_node()
        rclpy.try_shutdown()


app = FastAPI(lifespan=lifespan)


class DriveCommand(BaseModel):
    linear: float = Field(0.0, ge=-1.0, le=1.0)  # m/s; the node clamps again
    angular: float = Field(0.0, ge=-3.0, le=3.0)  # rad/s


@app.get("/api/status")
def status():
    odom = app.state.node.latest_odom()
    if odom is None:
        raise HTTPException(503, "no odometry yet")
    return odom


@app.post("/api/drive")
def drive(command: DriveCommand):
    app.state.node.drive(command.linear, command.angular)
    return {"ok": True}


@app.post("/api/reset_odometry")
async def reset_odometry():
    client = app.state.node.reset_client
    if not client.service_is_ready():
        raise HTTPException(503, "reset service not available")
    try:
        response = await call_service(client, Trigger.Request(), timeout_s=3.0)
    except TimeoutError:
        raise HTTPException(504, "reset service timed out") from None
    return {"success": response.success, "message": response.message}


@app.websocket("/ws/teleop")
async def teleop(websocket: WebSocket):
    await websocket.accept()
    node = app.state.node
    try:
        while True:
            data = await websocket.receive_json()
            try:
                node.drive(float(data["linear"]), float(data["angular"]))
            except (KeyError, TypeError, ValueError):
                node.drive(0.0, 0.0)
    except WebSocketDisconnect:
        pass
    finally:
        node.drive(0.0, 0.0)  # every way out of this handler stops the robot


async def mjpeg(node, fps):
    while True:
        frame = node.latest_jpeg()
        if frame is not None:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        await asyncio.sleep(1.0 / fps)


@app.get("/video.mjpg")
def video():
    return StreamingResponse(mjpeg(app.state.node, fps=10.0),
                             media_type="multipart/x-mixed-replace; boundary=frame")


def main():
    import uvicorn
    # Local only (the proxy adds TLS and login); one process, as each worker would add a node
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

## Check it

```bash
ros2 run my_robot_web server
ros2 topic echo /cmd_vel                   # second terminal, before the next command
curl -s localhost:8000/api/status
curl -s -X POST localhost:8000/api/drive -H 'Content-Type: application/json' \
  -d '{"linear": 0.1, "angular": 0.0}'
# echo shows linear.x 0.1, then all zeros about 0.5 s later: the watchdog fired
curl -s -X POST localhost:8000/api/drive -H 'Content-Type: application/json' -d '{"linear": 99}'
# 422: validation rejects it
```

`/video.mjpg` works as an `<img src>`. Turn off the generated API docs at `/docs`
(`FastAPI(docs_url=None, redoc_url=None)`) unless only you can reach the service.

## Adapting it

- Add endpoints for what the dashboard needs; a generic "call any service" route rebuilds
  rosbridge without its globs.
- Actions such as Nav2 goals: `send_goal_async`, return a job id, report progress over a
  WebSocket; never hold an HTTP request open for minutes.

Sources: rclpy `jazzy` branch (`node.py`, `task.py`, `client.py`, `signals.py`); FastAPI docs
(`lifespan`, `StreamingResponse`, WebSockets); Ubuntu noble packages; rosdep `python.yaml`.
