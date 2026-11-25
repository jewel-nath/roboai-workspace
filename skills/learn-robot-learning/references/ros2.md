# Learning with a ROS 2 robot

Part of [learn-robot-learning](../SKILL.md). For ROS 2 Jazzy. Checked against LeRobot 0.7.0 sources and docs,
`rosidl_python` (`jazzy`) and `vision_opencv` sources, `ros/rosdistro` (2026-11-25) and `mcap-ros2-support` 0.6.0.
The scripts were not run.

LeRobot, openpi, Isaac-GR00T, Isaac Lab and ManiSkill are not ROS packages and have no rosdistro release. A ROS 2
robot reaches them in one of four ways:

| Way | When |
|---|---|
| LeRobot drives the hardware directly | The arm has a LeRobot driver (SO-101, Koch, OpenArm...); ROS runs only for deployment |
| A LeRobot robot plugin that speaks ROS 2 | Third-party plugins listed in LeRobot's docs: `leros2`, `lerobot_robot_ros2_zenoh`, `lerobot-robot-rosetta`; not reviewed here |
| Record rosbag2, convert to a LeRobotDataset | Your ROS 2 stack already teleoperates the robot ([below](#record-with-rosbag2-and-convert)) |
| Policy in its own process, bridged to a ROS 2 node | Evaluating a trained policy on a ROS 2 robot from a workstation ([below](#run-a-policy-on-a-ros-2-robot)) |

Fast on-robot inference (TensorRT, ONNX Runtime, a policy node on a Jetson): [learn-edge-deployment](../../learn-edge-deployment/SKILL.md).

## Why separate processes

- Jazzy's Python message modules are compiled against Ubuntu 24.04's numpy 1.26 (the `rosidl_generator_py`
  type support uses numpy's C API, as does `cv_bridge`). LeRobot 0.7 requires numpy 2.0 or newer. Modules
  built for numpy 1.x fail to import under numpy 2 (`A module that was compiled using NumPy 1.x cannot be run in
  NumPy 2`), so a virtual environment with `--system-site-packages` mixing both is fragile.
- Lyrical runs Python 3.14; LeRobot supports 3.12-3.13 and Isaac-GR00T 3.12 only.
- Send plain JSON and JPEG bytes between the two sides, not pickles: pickled numpy objects tie the receiver to
  the sender's numpy version.

So: ROS nodes in the system Python, learning code in its own environment or container, joined by rosbag2 files
or a socket.

## Record with rosbag2 and convert

Record one bag per episode while your ROS 2 teleoperation runs (follower state, the command or leader state,
compressed camera images):

```bash
ros2 bag record -s mcap -o bags/ep_017 --topics /joint_states /leader/joint_states \
  /camera/top/image_raw/compressed /camera/wrist/image_raw/compressed
```

Then convert in the LeRobot environment, which needs no `rclpy` (`pip install mcap-ros2-support`):

```python
"""bag_to_lerobot.py - rosbag2 MCAP episodes (one bag folder each) to a LeRobotDataset v3.0.
python bag_to_lerobot.py --bags bags/ep_* --repo-id local/pick_cube --task "Pick the cube and put it in the bin"
"""
import argparse
from pathlib import Path

import cv2
import numpy as np
from lerobot.datasets import LeRobotDataset
from mcap_ros2.reader import read_ros2_messages

FPS = 30
JOINTS = ["joint1", "joint2", "joint3", "joint4", "joint5", "gripper"]  # training order, from the URDF
STATE_TOPIC = "/joint_states"            # follower, measured
ACTION_TOPIC = "/leader/joint_states"    # what the operator commanded
CAMERAS = {"top": "/camera/top/image_raw/compressed", "wrist": "/camera/wrist/image_raw/compressed"}
HEIGHT, WIDTH = 480, 640


def joints(msg) -> np.ndarray:
    index = {name: i for i, name in enumerate(msg.name)}
    return np.array([msg.position[index[j]] for j in JOINTS], dtype=np.float32)


def rgb(msg) -> np.ndarray:
    bgr = cv2.imdecode(np.frombuffer(bytes(msg.data), np.uint8), cv2.IMREAD_COLOR)
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)


def read_bag(bag: Path) -> dict[str, list]:
    topics = [STATE_TOPIC, ACTION_TOPIC, *CAMERAS.values()]
    streams = {t: [] for t in topics}
    for path in sorted(bag.glob("*.mcap")):
        for m in read_ros2_messages(str(path), topics=topics):
            stamp = m.ros_msg.header.stamp  # sensor time; use m.log_time_ns for header-less topics
            streams[m.channel.topic].append((stamp.sec * 1_000_000_000 + stamp.nanosec, m.ros_msg))
    for samples in streams.values():
        samples.sort(key=lambda s: s[0])
    return streams


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bags", nargs="+", type=Path, required=True)
    parser.add_argument("--repo-id", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--root", default=None)
    args = parser.parse_args()

    vector = {"dtype": "float32", "shape": (len(JOINTS),), "names": JOINTS}
    image = {"dtype": "video", "shape": (HEIGHT, WIDTH, 3), "names": ["height", "width", "channels"]}
    features = {"observation.state": vector, "action": vector,
                **{f"observation.images.{c}": image for c in CAMERAS}}
    dataset = LeRobotDataset.create(repo_id=args.repo_id, fps=FPS, features=features, root=args.root,
                                    robot_type="my_robot", use_videos=True)

    period = 1_000_000_000 // FPS
    for bag in args.bags:
        streams = read_bag(bag)
        start = max(s[0][0] for s in streams.values())   # every stream has data
        end = min(s[-1][0] for s in streams.values())
        cursor = dict.fromkeys(streams, 0)
        stale = 0
        for tick in range(start, end, period):
            latest = {}
            for topic, samples in streams.items():   # newest sample at or before the tick
                while cursor[topic] + 1 < len(samples) and samples[cursor[topic] + 1][0] <= tick:
                    cursor[topic] += 1
                stamp, latest[topic] = samples[cursor[topic]]
                stale += tick - stamp > 2 * period
            frame = {"observation.state": joints(latest[STATE_TOPIC]),
                     "action": joints(latest[ACTION_TOPIC]), "task": args.task}
            for name, topic in CAMERAS.items():
                frame[f"observation.images.{name}"] = rgb(latest[topic])
            dataset.add_frame(frame)
        dataset.save_episode()
        print(f"{bag}: {(end - start) / 1e9:.1f} s, {stale} stale samples")
    dataset.finalize()


if __name__ == "__main__":
    main()
```

- Timestamps in a LeRobotDataset come from the frame index, so the converter resamples to a fixed rate. Many
  stale samples mean a topic ran slower than `FPS` or stopped: fix the source rather than the converter.
- Units stay as in ROS (radians, metres). Deployment must feed the policy the same units and joint order.
- A mobile base: add `geometry_msgs/Twist` commands as action dimensions (header-less: use `log_time_ns`). Then
  check the dataset as usual ([dataset-checks.md](dataset-checks.md)).

## Run a policy on a ROS 2 robot

A policy server in the LeRobot environment and a small `rclpy` node exchange JSON and JPEG bytes over ZMQ on
localhost. The node clamps every command. Nothing here was run: it relies on the joint limits and step limit in
the node, the controller's own limits ([ros2-control](../../ros2-control/SKILL.md)) and a hardware e-stop
([arch-safety](../../arch-safety/SKILL.md)).

```python
"""policy_server.py - LeRobot environment, no ROS. Serves one robot on localhost."""
import json

import cv2
import numpy as np
import torch
import zmq
from lerobot.configs.policies import PreTrainedConfig
from lerobot.datasets import LeRobotDatasetMetadata
from lerobot.policies import get_policy_class, make_pre_post_processors
from lerobot.policies.utils import build_inference_frame, make_robot_action

CKPT = "outputs/train/act_pick_cube/checkpoints/last/pretrained_model"
CAMERAS = ["top", "wrist"]
device = torch.device("cuda")
cfg = PreTrainedConfig.from_pretrained(CKPT)
policy = get_policy_class(cfg.type).from_pretrained(CKPT).to(device).eval()
pre, post = make_pre_post_processors(cfg, pretrained_path=CKPT)
features = LeRobotDatasetMetadata("local/pick_cube").features   # the training dataset

sock = zmq.Context().socket(zmq.REP)
sock.bind("tcp://127.0.0.1:5556")
while True:
    header, *jpegs = sock.recv_multipart()
    msg = json.loads(header)
    if msg.get("reset"):
        policy.reset()                       # clears queued action chunks
        sock.send(b"{}")
        continue
    obs = dict(msg["state"])                 # joint name -> position
    for name, data in zip(CAMERAS, jpegs):
        obs[name] = cv2.cvtColor(cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    with torch.inference_mode():
        batch = pre(build_inference_frame(obs, device, features, task=msg["task"]))
        action = make_robot_action(post(policy.select_action(batch)), features)
    sock.send(json.dumps({k: float(v) for k, v in action.items()}).encode())
```

```python
"""policy_bridge.py - ROS 2 Jazzy node in the system Python (apt python3-zmq); no LeRobot import."""
import json

import rclpy
import zmq
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage, JointState
from std_msgs.msg import Float64MultiArray

JOINTS = ["joint1", "joint2", "joint3", "joint4", "joint5", "gripper"]
LOWER = [-1.9, -1.7, -1.6, -1.6, -2.8, 0.0]   # rad, placeholders: copy from your URDF, with margin
UPPER = [1.9, 1.7, 1.6, 1.6, 2.8, 1.0]
MAX_STEP = 0.03                                # rad per command at 30 Hz; start small
CAMERAS = {"top": "/camera/top/image_raw/compressed", "wrist": "/camera/wrist/image_raw/compressed"}
TASK = "Pick the cube and put it in the bin"


class PolicyBridge(Node):
    def __init__(self):
        super().__init__("policy_bridge")
        self.position, self.images = None, {}
        self.create_subscription(JointState, "/joint_states", self.on_joints, 10)
        for name, topic in CAMERAS.items():
            self.create_subscription(CompressedImage, topic,
                                     lambda m, n=name: self.images.__setitem__(n, bytes(m.data)), 2)
        self.pub = self.create_publisher(Float64MultiArray, "/forward_position_controller/commands", 10)
        self.sock = zmq.Context().socket(zmq.REQ)
        for option, value in ((zmq.RCVTIMEO, 300), (zmq.REQ_RELAXED, 1), (zmq.REQ_CORRELATE, 1)):
            self.sock.setsockopt(option, value)
        self.sock.connect("tcp://127.0.0.1:5556")
        self.sock.send(json.dumps({"reset": True}).encode())
        self.sock.recv()
        self.create_timer(1.0 / 30.0, self.tick)

    def on_joints(self, msg: JointState) -> None:
        index = {n: i for i, n in enumerate(msg.name)}
        self.position = [msg.position[index[j]] for j in JOINTS]

    def tick(self) -> None:
        if self.position is None or len(self.images) < len(CAMERAS):
            return
        header = json.dumps({"state": dict(zip(JOINTS, self.position)), "task": TASK}).encode()
        self.sock.send_multipart([header, *(self.images[c] for c in CAMERAS)])
        try:
            action = json.loads(self.sock.recv())
        except zmq.Again:
            self.get_logger().warning("policy timeout: no command sent, controller holds its last target")
            return
        target = []
        for j, lo, hi, now in zip(JOINTS, LOWER, UPPER, self.position):
            step = min(max(action[j], now - MAX_STEP), now + MAX_STEP)
            target.append(min(max(step, lo), hi))
        self.pub.publish(Float64MultiArray(data=target))


def main() -> None:
    rclpy.init()
    rclpy.spin(PolicyBridge())


if __name__ == "__main__":
    main()
```

- Commands go to a `position_controllers/JointGroupPositionController` named `forward_position_controller`
  (ros2_controllers, released for Jazzy). Keep the server on `127.0.0.1`: this ZMQ link has no authentication.
- The request blocks the timer for the inference time, so a slow policy lowers the rate: measure it. For slow
  models use chunked execution on a GPU host (LeRobot remote inference, openpi or GR00T servers).
- Lyrical: `ros2 bag record` needs `--topics` (positional topics were removed); the bridge node is unchanged.
