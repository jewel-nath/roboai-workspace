# rosbridge_suite with roslibjs and roslibpy (Jazzy)

rosbridge turns ROS 2 topics, services and actions into JSON messages over a WebSocket. A browser
talks to it with roslibjs, a Python program without ROS with roslibpy. Checked against
rosbridge_suite 2.7.1 (the `jazzy` branch), roslib 2.1.0 on npm and roslibpy 2.1.0.

## Install and launch, restricted

```bash
sudo apt install ros-jazzy-rosbridge-suite
```

Wrap the stock launch file in your bringup package so the limits travel with the robot:

```xml
<!-- my_robot_bringup/launch/rosbridge.launch.xml -->
<launch>
  <include file="$(find-pkg-share rosbridge_server)/launch/rosbridge_websocket_launch.xml">
    <!-- Default "" listens on every interface; keep it local and put a proxy in front -->
    <arg name="address" value="127.0.0.1"/>
    <arg name="port" value="9090"/>
    <!-- Glob lists are strings: the inner quotes stop launch from turning them into arrays -->
    <arg name="topics_sub_glob" value="'[/odom, /battery_state, /diagnostics, /camera/image_raw/compressed]'"/>
    <arg name="topics_pub_glob" value="'[/cmd_vel]'"/>
    <arg name="services_glob" value="'[/my_robot/reset_odometry]'"/>
    <arg name="params_glob" value="'[]'"/>
  </include>
</launch>
```

- An empty glob (`""`, the default) allows everything; `'[]'` allows nothing.
- Patterns are shell-style (`/my_robot/*`). When `services_glob` is set, rosbridge adds
  `/rosapi/*` so clients can still list topics.
- The launch file also starts `rosapi`, which answers `getTopics` and similar client calls.
- `topics_glob` still works and applies to both directions; the split `_pub_`/`_sub_` globs are
  clearer.
- `ssl:=true certfile:=... keyfile:=...` serves `wss://` directly, but a reverse proxy is the
  usual place for TLS (see [secure-access.md](secure-access.md)).

Check:

```bash
ros2 launch my_robot_bringup rosbridge.launch.xml
ss -ltnp | grep 9090          # 127.0.0.1:9090, not 0.0.0.0:9090
ros2 node list                # /rosbridge_websocket and /rosapi
```

## The wire protocol, for debugging

Every message is a JSON object with an `op` field. With any WebSocket client connected to
`ws://127.0.0.1:9090`:

```json
{"op": "subscribe", "topic": "/odom", "type": "nav_msgs/msg/Odometry", "throttle_rate": 200, "queue_length": 1}
{"op": "advertise", "topic": "/cmd_vel", "type": "geometry_msgs/msg/TwistStamped"}
{"op": "publish", "topic": "/cmd_vel", "msg": {"twist": {"linear": {"x": 0.1}}}}
{"op": "call_service", "service": "/my_robot/reset_odometry", "type": "std_srvs/srv/Trigger", "args": {}, "id": "r1"}
```

- `throttle_rate` is the minimum gap in milliseconds; `queue_length: 1` keeps only the newest.
- `compression` may be `none`, `png`, `cbor` or `cbor-raw`; CBOR sends binary frames and suits
  large arrays.
- Types work as `pkg/msg/Type` or `pkg/Type`; use the full form. `ros2 topic info /odom` gives it.
- Fields left out of `msg` get default values; a zero `header.stamp` is normal from a browser.
- A publish the globs refuse is dropped with only a warning in the `rosbridge_websocket` log; the
  client sees nothing. Check that log first when "nothing happens".

## roslibjs 2.x (browser)

roslib 2 is an ES module written in TypeScript: import the classes, publish plain objects (no
`ROSLIB.Message` wrapper needed), and prefer the promise-based calls.

```bash
npm install roslib@2
```

```js
// dashboard/src/robot.js
import { Ros, Topic, Service } from "roslib";

// Same origin as the page, through the authenticating proxy
const url = `wss://${location.host}/rosbridge`;
export const ros = new Ros({ url });
ros.on("connection", () => setStatus("connected"));
ros.on("error", () => setStatus("error"));
ros.on("close", () => {
  setStatus("disconnected");
  // roslib does not reconnect by itself; topics resubscribe once connect() succeeds
  setTimeout(() => ros.connect(url).catch(() => {}), 2000);
});

const odom = new Topic({
  ros,
  name: "/odom",
  messageType: "nav_msgs/msg/Odometry",
  throttle_rate: 100,  // at most 10 Hz to this browser
  queue_length: 1,
});
odom.subscribe((msg) => drawPose(msg.pose.pose.position));

const cmdVel = new Topic({ ros, name: "/cmd_vel", messageType: "geometry_msgs/msg/TwistStamped" });

// Dead-man teleop: send only while held, at a steady rate, and stop on every way out
let timer = null;
export function holdDrive(linear, angular) {
  clearInterval(timer);
  timer = setInterval(
    () => cmdVel.publish({ twist: { linear: { x: linear }, angular: { z: angular } } }),
    100,
  );
}
export function releaseDrive() {
  clearInterval(timer);
  timer = null;
  cmdVel.publish({ twist: {} });  // all zeros
}
window.addEventListener("pointerup", releaseDrive);
window.addEventListener("blur", releaseDrive);
document.addEventListener("visibilitychange", () => document.hidden && releaseDrive());

const resetOdom = new Service({
  ros,
  name: "/my_robot/reset_odometry",
  serviceType: "std_srvs/srv/Trigger",
});
export async function resetOdometry() {
  const response = await resetOdom.callServiceAsync({}, 5);  // timeout in seconds
  return response.success;
}
```

The browser cannot be trusted to stop the robot: the tab may freeze or the network may drop with
no event. The controller's own command timeout (`cmd_vel_timeout` in `diff_drive_controller`)
is the real stop; the browser side only makes it quicker.

## roslibpy (Python without ROS)

For a laptop script, a test rig or a Windows tool that should not install ROS 2.

```bash
python3 -m venv .venv && . .venv/bin/activate && pip install roslibpy
```

```python
import time

import roslibpy

# A full URL also works: roslibpy.Ros(host="wss://robot.local/rosbridge")
client = roslibpy.Ros(host="127.0.0.1", port=9090)
client.run()  # starts the network loop in the background and waits for the connection

odom = roslibpy.Topic(client, "/odom", "nav_msgs/msg/Odometry", throttle_rate=200, queue_length=1)
odom.subscribe(lambda msg: print(msg["pose"]["pose"]["position"]))

reset = roslibpy.Service(client, "/my_robot/reset_odometry", "std_srvs/srv/Trigger")
print(reset.call(roslibpy.ServiceRequest({}), timeout=5))  # blocks without a callback

cmd = roslibpy.Topic(client, "/cmd_vel", "geometry_msgs/msg/TwistStamped")
for _ in range(20):  # 2 s forward at 10 Hz
    cmd.publish(roslibpy.Message({"twist": {"linear": {"x": 0.1}}}))
    time.sleep(0.1)
cmd.publish(roslibpy.Message({"twist": {}}))

odom.unsubscribe()
client.terminate()  # once, at the end: the default Twisted loop cannot be restarted
```

- `roslibpy.Ros(..., headers={"Authorization": "Bearer ..."})` sends a header on the WebSocket
  handshake, which a token-checking proxy can verify. Browsers cannot do this.
- `transport="asyncio"` selects the asyncio backend instead of Twisted.

Sources: rosbridge_suite `jazzy` branch (`rosbridge_websocket_launch.xml`,
`rosbridge_websocket.py`, `ROSBRIDGE_PROTOCOL.md`, rosapi README); roslibjs `packages/roslib`
(2.1.0); roslibpy (2.1.0) source and docs.
