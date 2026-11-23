---
type: tool
name: YOLO
summary: The YOLO family of real-time object detectors; Ultralytics' package (YOLO26 and older lines) is the usual choice, but its code and weights are AGPL-3.0 with a paid Enterprise Licence, so closed products turn to Apache-2.0 detectors such as YOLOX, RT-DETR, D-FINE or RF-DETR; yolo_ros (MIT) runs the exported models on ROS 2, built from source.
tags: [yolo, ultralytics, yolo26, yolo11, yolov8, object-detection, segmentation, onnx, tensorrt, jetson, yolo-ros, agpl, yolox, rt-detr, rf-detr, d-fine]
kind: model
area: perception
support:
license: AGPL-3.0-or-later
links: {repo: "https://github.com/ultralytics/ultralytics", docs: "https://docs.ultralytics.com", site: "https://www.ultralytics.com"}
version: {tested: , latest: 8.4.216, as_of: 2026-11-23}
platforms: [linux, windows, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/ultralytics/ultralytics", title: "Ultralytics repository: README, LICENSE, pyproject.toml, tags and docs (YOLO26, export, TensorRT, Jetson, ROS)", accessed: 2026-11-23}
  - {url: "https://www.ultralytics.com/license", title: "Ultralytics Licensing: AGPL-3.0 and Enterprise License", accessed: 2026-11-23}
  - {url: "https://github.com/mgonzs13/yolo_ros", title: "yolo_ros repository: README, LICENSE, package.xml files, config/yolo.yaml, tags", accessed: 2026-11-23}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro: humble, jazzy, kilted, lyrical and rolling distribution.yaml (no yolo_ros entry)", accessed: 2026-11-23}
  - {url: "https://github.com/Megvii-BaseDetection/YOLOX", title: "YOLOX repository: README, LICENSE, deployment demos", accessed: 2026-11-23}
  - {url: "https://github.com/lyuwenyu/RT-DETR", title: "RT-DETR repository: README and LICENSE", accessed: 2026-11-23}
  - {url: "https://github.com/roboflow/rf-detr", title: "RF-DETR repository: README licence notes and benchmark table, LICENSE", accessed: 2026-11-23}
  - {url: "https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_object_detection", title: "Isaac ROS Object Detection repository: package list", accessed: 2026-11-23}
---

# YOLO

YOLO ("you only look once") detectors find objects in one pass over an image, fast enough for live
cameras. Most builders use Ultralytics' package (newest models YOLO26; YOLOv3 loads as `yolov3u`)
[1][3]. **Licence first:** its code is AGPL-3.0; Ultralytics says its weights and models trained
with it are too, and that closed products or embedded robots need a paid licence [1][2].

## When to use it

- Classes you can label: Ultralytics trains, tracks and exports detection, segmentation, pose
  and oriented-box models in one tool [1]. Objects you can only name:
  [Grounding DINO](grounding-dino.md); masks of anything: [Segment Anything](segment-anything.md).
- A closed-source robot: Apache-2.0 YOLOX [5], RT-DETR [6], D-FINE, or RF-DETR's Nano to Large
  sizes (its other sizes use Roboflow's PML licence) [7].

## Setup

```bash
python3 -m venv ~/venvs/yolo && . ~/venvs/yolo/bin/activate    # Python 3.8+, PyTorch 1.8+
pip install ultralytics                                        # 8.4.216
yolo predict model=yolo26n.pt source='https://ultralytics.com/images/bus.jpg'
yolo export model=yolo26n.pt format=onnx      # format=engine builds TensorRT on NVIDIA
```

Linux, Windows, macOS, and Jetson Docker images per JetPack; TensorRT export takes `quantize=16`
or `quantize=8` (INT8, with calibration images) [1]. Ultralytics' YOLO26n: 2.4 M parameters, 40.9
COCO mAP, 1.7 ms on a T4 (TensorRT), 38.9 ms on CPU (ONNX); no GPU memory figures [1].

## How an agent works with it

- Python: `YOLO("yolo26n.pt")(frame)` returns boxes, masks or keypoints; tracking adds IDs [1].
- ROS 2: **yolo_ros** (MIT) is a C++ ONNX Runtime node, no Python at run time, for exports from
  YOLOv3u to YOLO26 [3]. No distro has a binary release [4]: clone it, `rosdep install`,
  `colcon build` (`-DONNX_GPU=ON` for CUDA), `ros2 launch yolo_bringup yolo.launch.py`. CI
  builds `main` for Humble to Lyrical; newest tag 4.7.1, `main` (2026-11-19) holds 5.0.0 [3].
- `config/yolo.yaml` sets each camera's RGB topic, plus depth and `camera_info` for 3D boxes;
  check that `ros2 topic hz /yolo/cam0/detections` matches the camera rate [3].

## Traps

- **An MIT wrapper does not free the weights.** The Ultralytics models yolo_ros downloads stay
  AGPL-3.0 [3]; so does RT-DETR run through Ultralytics, unlike the Apache-2.0 original [6].
- **No detections, no error.** The shipped `yolo.yaml` subscribes Reliable (`reliability: 1`),
  so a best-effort camera delivers nothing; set `2` [3].
- **3D boxes need TF** from each camera frame to `target_frame` ([tf2](../../software/tf2.md)) [3].
- **Engines do not travel.** Build TensorRT engines on the robot's own GPU and TensorRT [1];
  yolo_ros's TensorRT provider needs TensorRT 10 and falls back to CUDA with 11 [3].
- **Jazzy YAML:** an empty list such as `cameras: []` stops yolo_ros; leave the key out [3].

## Alternatives

YOLOX (idle since 2025-06) [5], RT-DETR [6], D-FINE, RF-DETR [7], Isaac ROS `isaac_ros_yolov8` [8].

## Sources

1. [Ultralytics repository: README, LICENSE, pyproject.toml, tags and docs (YOLO26, export, TensorRT, Jetson, ROS)](https://github.com/ultralytics/ultralytics), accessed 2026-11-23
2. [Ultralytics Licensing: AGPL-3.0 and Enterprise License](https://www.ultralytics.com/license), accessed 2026-11-23
3. [yolo_ros repository: README, LICENSE, package.xml files, config/yolo.yaml, tags](https://github.com/mgonzs13/yolo_ros), accessed 2026-11-23
4. [rosdistro: humble, jazzy, kilted, lyrical and rolling distribution.yaml (no yolo_ros entry)](https://github.com/ros/rosdistro), accessed 2026-11-23
5. [YOLOX repository: README, LICENSE, deployment demos](https://github.com/Megvii-BaseDetection/YOLOX), accessed 2026-11-23
6. [RT-DETR repository: README and LICENSE](https://github.com/lyuwenyu/RT-DETR), accessed 2026-11-23
7. [RF-DETR repository: README licence notes and benchmark table, LICENSE](https://github.com/roboflow/rf-detr), accessed 2026-11-23
8. [Isaac ROS Object Detection repository: package list](https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_object_detection), accessed 2026-11-23
