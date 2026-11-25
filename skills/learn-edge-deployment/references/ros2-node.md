# Inference inside ROS 2 Jazzy

Part of [learn-edge-deployment](../SKILL.md). Written for `rclpy` on Jazzy, ONNX Runtime and TensorRT as in
[onnx-runtime.md](onnx-runtime.md) and [tensorrt.md](tensorrt.md), and Isaac ROS 4.6 (`isaac_ros_dnn_inference`
`release-4.6`, docs for 4.6); not run. The policy runner itself (observation assembly by joint name, soft
start, stale-state watchdog, tilt stop, limits) is in [sim-to-real](../../sim-to-real/references/deployment.md);
the detector node with `cv_bridge` and `vision_msgs` is in
[perception-camera](../../perception-camera/references/detection-node.md). This file adds what changes when the
model must be fast and steady.

> Code here commands robots through other nodes. It was not run. It relies on the limits, watchdog and stop
> path of the sim-to-real runner, on joint limits enforced in ros2_control, on drive torque and speed limits,
> and on a hardware E-stop within reach ([arch-safety](../../arch-safety/SKILL.md)).

## Where the model runs

| Model | Put it | Why |
|---|---|---|
| Policy whose output a controller follows | A policy node publishing targets to a ros2_control controller (`JointGroupPositionController`, `joint_trajectory_controller`) | The controller loop runs in `ros2_control_node`'s real-time thread; policy jitter delays targets, not the motor loop ([ros2-control](../../ros2-control/SKILL.md)) |
| Detector or segmenter on camera images | Its own process, subscribing best effort with depth 1 | A slow frame never blocks other nodes; the newest frame wins |
| Several models on one GPU | One process per model, or one process that runs them in turn | Measure: they share the GPU and, on Jetson, the RAM |
| Camera pipeline on a Jetson with many stages | C++ composable nodes in one container, or an Isaac ROS graph | Avoids serialisation and copies between stages (below) |

Python threads share one interpreter lock. A `MultiThreadedExecutor` with separate callback groups keeps
sensor callbacks from queuing behind inference, but it does not make a heavy model and a fast control loop
share one Python process well: split them into processes.

## One call for ONNX Runtime and TensorRT

```python
"""my_robot_inference/backend.py: load .onnx or .engine, warm up, return (call, description)."""
import numpy as np


def make_backend(model_path: str, warmup_feeds: dict, warmup_runs: int = 20, ort_providers=None):
    if model_path.endswith(".engine"):
        from my_robot_inference.trt_model import TrtModel      # the class in tensorrt.md
        call, used = TrtModel(model_path), "TensorRT"
    else:
        import onnxruntime as ort
        session = ort.InferenceSession(model_path, providers=ort_providers or ["CPUExecutionProvider"])
        names = [o.name for o in session.get_outputs()]
        call, used = (lambda feeds: dict(zip(names, session.run(names, feeds)))), session.get_providers()[0]
    for _ in range(warmup_runs):            # first runs allocate, compile kernels or build engines
        call(warmup_feeds)
    return call, used
```

Log `used` at start, and refuse to start if it is not the expected provider: a GPU model silently running on
the CPU is the most common deployment failure. Load and warm up in the constructor, never in a callback.

## Timing every step

```python
"""my_robot_inference/timing.py: period, input age and inference time per step, published and summarised."""
import time

import numpy as np
from rclpy.time import Time
from std_msgs.msg import Float32MultiArray


class StepTimer:
    def __init__(self, node, period_s: float, late_factor: float = 1.5, report_every: int = 1000):
        self._node, self._period_s, self._late = node, period_s, late_factor * period_s
        self._pub = node.create_publisher(Float32MultiArray, "~/timing", 10)
        self._last, self._rows, self._report_every, self.late = None, [], report_every, 0

    def record(self, input_stamp, infer_s: float) -> None:
        """Call once per step after publishing; input_stamp is the header.stamp of the newest input used."""
        now = time.monotonic()
        period = self._period_s if self._last is None else now - self._last
        self._last = now
        age = (self._node.get_clock().now() - Time.from_msg(input_stamp)).nanoseconds * 1e-9
        self.late += period > self._late
        self._rows.append((period, age, infer_s))
        self._pub.publish(Float32MultiArray(data=[1e3 * period, 1e3 * age, 1e3 * infer_s]))
        if len(self._rows) >= self._report_every:
            ms = 1e3 * np.asarray(self._rows)
            p50, p99, top = np.percentile(ms, 50, axis=0), np.percentile(ms, 99, axis=0), ms.max(axis=0)
            self._node.get_logger().info(
                "ms p50/p99/max: period %.1f/%.1f/%.1f, input age %.1f/%.1f/%.1f, inference %.1f/%.1f/%.1f; late %d"
                % (p50[0], p99[0], top[0], p50[1], p99[1], top[1], p50[2], p99[2], top[2], self.late))
            self._rows.clear()
```

`~/timing` goes into the bag with everything else, so the latency report comes from the same run as the
behaviour ([latency.md](latency.md)). Input age uses ROS time: across two computers their clocks must be
synchronised ([ops-bringup](../../ops-bringup/references/time-sync.md)).

## A policy node: what changes

Start from the sim-to-real `PolicyRunner` and change three things: the backend, the threading and the timing.

```python
import time

import numpy as np
import rclpy
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import JointState

from my_robot_inference.backend import make_backend
from my_robot_inference.timing import StepTimer


class PolicyNode(Node):
    def __init__(self):
        super().__init__("policy")
        rate_hz = self.declare_parameter("rate_hz", 50.0).value
        model = self.declare_parameter("model", "policy.engine").value
        obs_dim = self.declare_parameter("obs_dim", 48).value
        self.backend, used = make_backend(model, {"obs": np.zeros((1, obs_dim), np.float32)})
        self.get_logger().info(f"{model} on {used}")
        self.latest = None                                    # (stamp, obs) from the newest messages
        sensors, control = MutuallyExclusiveCallbackGroup(), MutuallyExclusiveCallbackGroup()
        self.create_subscription(JointState, "joint_states", self.on_joints,
                                 qos_profile_sensor_data, callback_group=sensors)
        self.timer = StepTimer(self, 1.0 / rate_hz)
        self.create_timer(1.0 / rate_hz, self.step, callback_group=control)

    def on_joints(self, msg):
        obs = self.build_observation(msg)                     # by joint name, as in the sim-to-real runner
        self.latest = (msg.header.stamp, obs)

    def step(self):
        if self.latest is None:
            return
        stamp, obs = self.latest
        t0 = time.monotonic()
        action = self.backend({"obs": obs[None]})["action"][0]
        infer_s = time.monotonic() - t0
        self.publish_command(action)                          # limits, clip and watchdog as in sim-to-real
        self.timer.record(stamp, infer_s)


def main():
    rclpy.init()
    node = PolicyNode()
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(node)
    try:
        executor.spin()
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
```

`build_observation` and `publish_command` are the sim-to-real runner's observation, limit and stop code.
`rclpy` timers jitter under load; if the period's p99 is too wide for the policy, move the loop out of
Python (a C++ node or a ros2_control controller that runs the engine) rather than tuning Python.

## A detector on camera images

- Use perception-camera's `DetectorNode`: best effort depth 1, newest frame only, input header on every output.
- **Ultralytics models** (AGPL-3.0 unless you hold their licence): build the engine on the target with
  `yolo export model=<weights>.pt format=engine quantize=16 device=0` (`half`/`int8` are the older,
  deprecated arguments; `quantize=8` needs `data=` for calibration) and pass the `.engine` as the adapter's
  `weights`; Ultralytics predicts directly on exported models.
- **Other models**: replace the adapter's call with your preprocessing (or the preprocessing inside the graph,
  [onnx-export.md](onnx-export.md#image-inputs)), `make_backend`, and the model's own decoding (box format,
  score threshold, NMS unless it is in the graph).

## Copies and zero-copy in Jazzy

- **rclpy** has no intra-process path: every image crosses the middleware and is converted to Python objects,
  a copy on each side. Fine for a detector at camera rate on small images; measure for large ones.
- **rclcpp composable nodes** in one container with `use_intra_process_comms: True` hand a published
  `std::unique_ptr` message to a single intra-process subscriber without copying (CPU memory).
- **Loaned messages** (shared-memory zero-copy) need fixed-size types and an RMW that supports loans;
  `sensor_msgs/Image` has an unbounded `data` array, so it does not qualify.
- **GPU memory between nodes** stays on the GPU only through type adaptation (REP 2007): Isaac ROS NITROS in
  4.x, between NITROS nodes in one container. Lyrical adds `rosidl::Buffer`, which Isaac ROS 5 uses instead.
- **On a Jetson** CPU and GPU share DRAM, so host-device copies are cheaper than over PCIe, but they still
  take time and bandwidth: they show up in the node's inference time, not in trtexec's default numbers.

## Isaac ROS 4.6 TensorRT node (Jazzy)

Isaac ROS 4.6 (2026-08-18) is the Jazzy line: JetPack 7.2 on Thor (T5000, T4000) and Orin, or x86_64 with an
Ampere or newer GPU, Ubuntu 24.04, CUDA 13.2+ and driver 595+. Packages come from NVIDIA's Isaac ROS apt
repository, not ros/rosdistro. Its repositories are Apache-2.0; CUDA and TensorRT underneath are under NVIDIA's
terms. Whether 4.6 runs on JetPack 7.2.2's TensorRT 11.4.1 was not checked.

```bash
sudo apt-get install isaac-ros-cli
sudo isaac-ros init docker              # or venv, or baremetal (advanced; can break the host)
isaac-ros activate
sudo apt-get update && sudo apt-get install -y ros-jazzy-isaac-ros-tensor-rt
```

The usual graph: camera image and `camera_info` → `DnnImageEncoderNode` (resize, normalise: `network_image_width`,
`network_image_height`, `image_mean`, `image_stddev`, `input_encoding`) → `TensorRTNode` → a model-specific
decoder from `isaac_ros_object_detection` (`isaac_ros_yolov8`, `isaac_ros_rtdetr`, `isaac_ros_detectnet`,
`isaac_ros_grounding_dino`) → detections.

```python
ComposableNode(
    package="isaac_ros_tensor_rt",
    plugin="nvidia::isaac_ros::dnn_inference::TensorRTNode",
    name="tensor_rt",
    parameters=[{
        "model_file_path": "/opt/my_robot/models/detector.onnx",
        "engine_file_path": "/var/cache/my_robot/detector.plan",
        "force_engine_update": False,       # default true: rebuilds the engine at every start
        "input_tensor_names": ["input_tensor"],
        "input_binding_names": ["images"],  # the ONNX input name
        "output_tensor_names": ["output_tensor"],
        "output_binding_names": ["output0"],
        "enable_fp16": True,                # default true
        "verbose": False,
    }])
```

Run it in a `component_container_mt` (package `rclcpp_components`) with the encoder and decoder. The node
subscribes to `tensor_pub` and publishes `tensor_sub` (`isaac_ros_tensor_list_interfaces/TensorList`), names
that read backwards; remap them explicitly. NITROS acceleration applies only between NITROS nodes; a plain ROS
node in the chain gets ordinary messages and copies.

## Checks

```bash
ros2 topic hz /policy/timing                 # the node's real step rate
ros2 topic echo --once /detections --field header.stamp   # equals the input image's stamp
ros2 topic delay /detections                 # now minus header.stamp: capture-to-result age
```

- The startup log names the expected provider or engine, and warm-up finished before the node reported ready.
- `~/timing` p99 period and input age fit the budget with every other node running.
- Stopping the input (unplug the camera, stop `joint_states`) makes the node stop commanding within its
  watchdog time.
