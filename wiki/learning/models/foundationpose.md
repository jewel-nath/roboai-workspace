---
type: tool
name: FoundationPose
summary: NVIDIA's model for 6D pose estimation and tracking of objects it never saw in training, from RGB-D plus a mesh or a few reference images; the research code and weights may be used only for non-commercial research or evaluation, while Isaac ROS FoundationPose (Apache-2.0 code, NGC weights under an NVIDIA model EULA) is the ROS 2 path on NVIDIA GPUs.
tags: [foundationpose, 6d-pose, pose-estimation, object-tracking, novel-objects, rgbd, cad-model, grasping, nvidia, isaac-ros, tensorrt, non-commercial]
kind: model
area: perception
support:
license: LicenseRef-NVIDIA-Source-Code-License
links: {repo: "https://github.com/NVlabs/FoundationPose", docs: "https://nvidia-isaac-ros.github.io/v/release-4.6/repositories_and_packages/isaac_ros_pose_estimation/isaac_ros_foundationpose/index.html", site: "https://nvlabs.github.io/FoundationPose/"}
version: {tested: , latest: , as_of: 2026-11-23}
platforms: [linux]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/NVlabs/FoundationPose", title: "FoundationPose repository: README, LICENSE, run_demo.py, datareader.py, docker, history", accessed: 2026-11-23}
  - {url: "https://github.com/NVlabs/FoundationPose/issues/44", title: "FoundationPose issue 44: unreasonable results (mesh units, RGB-D alignment, intrinsics)", accessed: 2026-11-23}
  - {url: "https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_pose_estimation", title: "Isaac ROS Pose Estimation repository: README, LICENSE, tags v4.6-0 to v5.1-0, FoundationPose node and model script", accessed: 2026-11-23}
  - {url: "https://nvidia-isaac-ros.github.io/v/release-4.6/repositories_and_packages/isaac_ros_pose_estimation/isaac_ros_foundationpose/index.html", title: "Isaac ROS 4.6 docs: isaac_ros_foundationpose", accessed: 2026-11-23}
  - {url: "https://nvidia-isaac-ros.github.io/v/release-4.6/getting_started/index.html", title: "Isaac ROS 4.6 getting started: ROS 2 Jazzy and platform requirements", accessed: 2026-11-23}
  - {url: "https://nvidia-isaac-ros.github.io/releases/index.html", title: "Isaac ROS release notes (4.0 to 5.1)", accessed: 2026-11-23}
  - {url: "https://catalog.ngc.nvidia.com/orgs/nvidia/teams/isaac/models/foundationpose", title: "NVIDIA NGC: Isaac FoundationPose model card", accessed: 2026-11-23}
---

# FoundationPose

NVIDIA's model (CVPR 2024) for the 6D pose of an object it was never trained on. From RGB-D
frames, intrinsics, a first-frame mask and a textured mesh (or a few reference images) it finds
the pose, then tracks it frame to frame; it led the BOP leaderboard for unseen objects with a
model as of March 2024 [1]. Builders use it to grasp a part from its CAD model.

**Licence: research and evaluation only.** The NVIDIA Source Code License allows the code and
its derivatives only non-commercial use, defined as "for research or evaluation purposes only"
[1]. A lab or hobby demo is fine; a product, paid service or production robot is not. Isaac ROS
FoundationPose is Apache-2.0 code [3] fetching NGC weights under an NVIDIA model EULA; its card
says no further training is needed for commercial applications [7]; we did not review the EULA.

## When to use it

- One object with a mesh (or a scan) and an RGB-D camera, to grasp or track it. No mesh, known
  category: CenterPose; one object with your own trained model: DOPE; both in Isaac ROS [3].
  Only a box or mask: [YOLO](yolo.md) or [Segment Anything](segment-anything.md).

## Setup

**Isaac ROS on Jazzy:** release 4.6 targets Jazzy on Ubuntu 24.04, on x86-64 with an Ampere or
newer 8 GB GPU (CUDA 13.2+, driver 595+) or Jetson AGX Thor or Orin with JetPack 7.2 [5]. Add
NVIDIA's Isaac ROS apt repository, then `sudo apt-get install -y ros-jazzy-isaac-ros-foundationpose`
(4.6.0) [3][4]. Not in rosdistro; Isaac ROS 5.0 (2026-09-18) moved to Lyrical [6]. The FP32
pipeline peaks near 7 GB of GPU memory, so NVIDIA asks for 8 GB or more [4].

**Research code:** `docker pull wenbowen123/foundationpose`, `bash docker/run_container.sh`, then
`bash build_all.sh` inside once. The image is CUDA 11.3 on Ubuntu 20.04; for an RTX 4090 or newer
the README points to a community CUDA 12.1 image. Weights are on Google Drive; `run_demo.py`
tracks a mustard bottle. No releases or tags; last commit 2026-04-29 [1].

## How an agent works with it

- Python: `est.register(K=, rgb=, depth=, ob_mask=, iteration=5)`, then `est.track_one(...)`
  per frame [1]. A scene holds `rgb/`, `depth/` (16-bit PNG in mm), `masks/` and `cam_K.txt` [1].
- ROS 2: the node syncs `pose_estimation/image`, `depth_image`, `camera_info` and `segmentation`
  by approximate time and publishes `vision_msgs/Detection3DArray` on `pose_estimation/output`,
  with TF frame `fp_object` [3]. A tracking node, a selector and Detection2DToMask (best 2D box
  to mask) complete the graph [4]. Check that `fp_object` sits on the real object in RViz.

## Traps

- **Mesh in millimetres.** FoundationPose works in metres; a CAD file in millimetres gives absurd
  poses. Also align RGB with depth and check the intrinsics [2].
- **Mask size:** Detection2DToMask's default 640 x 480 mask must match the colour image [4].
- **Far objects vanish.** Depth outside `min_depth` to `max_depth` (0.1 to 2.0) is dropped [3].
- **A stale pose after the object moves.** In 4.6 the selector re-runs full estimation only every
  `reset_period` (600000 ms); tracking resets only below 50 supporting depth points [3]. Lower it.
- **Licence drift.** Code built on the research repo inherits its non-commercial limit [1].

## Alternatives

CenterPose, DOPE [3]; for the mask, [SAM](segment-anything.md), [Grounding DINO](grounding-dino.md).

## Sources

1. [FoundationPose repository: README, LICENSE, run_demo.py, datareader.py, docker, history](https://github.com/NVlabs/FoundationPose), accessed 2026-11-23
2. [FoundationPose issue 44: unreasonable results (mesh units, RGB-D alignment, intrinsics)](https://github.com/NVlabs/FoundationPose/issues/44), accessed 2026-11-23
3. [Isaac ROS Pose Estimation repository: README, LICENSE, tags v4.6-0 to v5.1-0, FoundationPose node and model script](https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_pose_estimation), accessed 2026-11-23
4. [Isaac ROS 4.6 docs: isaac_ros_foundationpose](https://nvidia-isaac-ros.github.io/v/release-4.6/repositories_and_packages/isaac_ros_pose_estimation/isaac_ros_foundationpose/index.html), accessed 2026-11-23
5. [Isaac ROS 4.6 getting started: ROS 2 Jazzy and platform requirements](https://nvidia-isaac-ros.github.io/v/release-4.6/getting_started/index.html), accessed 2026-11-23
6. [Isaac ROS release notes (4.0 to 5.1)](https://nvidia-isaac-ros.github.io/releases/index.html), accessed 2026-11-23
7. [NVIDIA NGC: Isaac FoundationPose model card](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/isaac/models/foundationpose), accessed 2026-11-23
