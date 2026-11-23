---
type: tool
name: OpenVINS
summary: The University of Delaware RPNG lab's MSCKF visual-inertial estimator (mono, stereo, multi-camera) with online calibration and evaluation tools; GPL-3.0-or-later, builds for ROS 1 and ROS 2 from source, with no rosdistro release.
tags: [openvins, open-vins, msckf, ekf, visual-inertial-odometry, vio, stereo, imu, kalibr, ov-msckf, ov-eval, gpl]
kind: library
area: perception
support:
license: GPL-3.0-or-later
links: {repo: "https://github.com/rpng/open_vins", docs: "https://docs.openvins.com/", site: }
version: {tested: , latest: v2.7, as_of: 2026-11-23}
platforms: [linux]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/rpng/open_vins", title: "open_vins repository: ReadMe, LICENSE, package.xml, workflows, Dockerfiles, config, ROS2Visualizer and history", accessed: 2026-11-23}
  - {url: "https://docs.openvins.com/gs-installing.html", title: "OpenVINS docs: Installation guide (ROS 1 and ROS 2)", accessed: 2026-11-23}
  - {url: "https://docs.openvins.com/gs-calibration.html", title: "OpenVINS docs: Sensor calibration", accessed: 2026-11-23}
  - {url: "https://github.com/ethz-asl/kalibr/wiki/yaml-formats", title: "Kalibr wiki: YAML formats", accessed: 2026-11-23}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-23}
  - {url: "https://github.com/ros-perception/image_common/tree/jazzy/image_transport/include/image_transport", title: "image_common, jazzy branch: image_transport headers", accessed: 2026-11-23}
  - {url: "https://github.com/ros2/geometry2/tree/jazzy/tf2_geometry_msgs/include/tf2_geometry_msgs", title: "geometry2, jazzy branch: tf2_geometry_msgs headers", accessed: 2026-11-23}
  - {url: "https://github.com/ros2-gbp/vision_opencv-release/tree/release/jazzy/cv_bridge/4.1.0-1", title: "cv_bridge 4.1.0, Jazzy release: include/cv_bridge", accessed: 2026-11-23}
---

# OpenVINS

An extended Kalman filter that fuses IMU data with sparse visual feature tracks in the MSCKF
sliding-window form, for one or more cameras; it calibrates intrinsics, camera-IMU extrinsics and
time offset online, and ships a simulator and `ov_eval` (ATE, RPE, NEES) [1]. Builders use it for
camera-plus-IMU odometry and as a research baseline. GPL-3.0-or-later. Maintained slowly: v2.7
(June 2023) is the newest tag; Ceres 2.2 support merged 2025-11-29 [1].

## When to use it

For VIO with good docs and evaluation tools [1][2]. Unlike [VINS-Fusion](vins-fusion.md) it is a
filter, has no loop closure in the core (`ov_secondary` adds a loose one) and still merges fixes
[1]. For saved maps, use [ORB-SLAM3](orb-slam3.md) or [RTAB-Map](rtab-map.md).

## Setup

No ROS distro has a binary [5]; the docs list ROS 2 Dashing and Galactic [2], and CI builds up to
Humble in Docker [1]. CPU only; ArUco tags need opencv_contrib or `-DENABLE_ARUCO_TAGS=OFF` [2].

```bash
sudo apt install libeigen3-dev libboost-all-dev libceres-dev
cd ~/ros2_ws/src && git clone https://github.com/rpng/open_vins.git   # master, not tag v2.7
cd .. && colcon build --packages-up-to ov_msckf && source install/setup.bash
ros2 launch ov_msckf subscribe.launch.py config:=euroc_mav   # then: ros2 bag play V1_01_easy
```

## How an agent works with it

A config folder holds `estimator_config.yaml`, `kalibr_imu_chain.yaml` (IMU noise, rate, topic)
and `kalibr_imucam_chain.yaml` (intrinsics, `T_imu_cam`, time shift, image topics). The node
publishes `odomimu`, `poseimu`, `pathimu`, feature clouds and TF `global → imu → cam0` [1].

Calibrate as the docs say [3]: intrinsics with [Kalibr](kalibr.md) (under 0.5 px error), IMU noise
from allan_variance_ros inflated 10–20 times, extrinsics from 30–60 s of smooth motion.

## Traps

- **Jazzy headers.** `ROS2Visualizer.h` includes `tf2_geometry_msgs.h`, `image_transport.h` and
  `cv_bridge.h` [1]; Jazzy ships only the `.hpp` forms [6][7][8]. Rename the includes to build.
- **Build master, not v2.7.** Ceres 2.2, on Ubuntu 24.04 (see [VINS-Fusion](vins-fusion.md)),
  needs `ceres::Manifold`; that path merged in November 2025 [1].
- **Kalibr's extrinsic is inverted.** OpenVINS reads `T_imu_cam`, the camera pose in the IMU frame
  [1]; Kalibr writes `T_cam_imu`, IMU to camera [4]. Invert and rename it when you copy it over.
- **It waits for a jerk.** Static initialisation needs the rig still, then a motion above
  `init_imu_thresh`; set `init_dyn_use: true` for dynamic start [1].
- **Frames and stamps.** `global` and `imu` are not REP 105 names, and that TF is stamped with the
  node clock, not image time [1]; fuse `odomimu` in [robot_localization](robot-localization.md).

## Alternatives

[VINS-Fusion](vins-fusion.md), [ORB-SLAM3](orb-slam3.md), [RTAB-Map](rtab-map.md), Kimera-VIO; see
the [SLAM guide](../guides/choose-a-slam-system.md).

## Sources

1. [open_vins repository: ReadMe, LICENSE, package.xml, workflows, Dockerfiles, config, ROS2Visualizer and history](https://github.com/rpng/open_vins), accessed 2026-11-23
2. [OpenVINS docs: Installation guide (ROS 1 and ROS 2)](https://docs.openvins.com/gs-installing.html), accessed 2026-11-23
3. [OpenVINS docs: Sensor calibration](https://docs.openvins.com/gs-calibration.html), accessed 2026-11-23
4. [Kalibr wiki: YAML formats](https://github.com/ethz-asl/kalibr/wiki/yaml-formats), accessed 2026-11-23
5. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-23
6. [image_common, jazzy branch: image_transport headers](https://github.com/ros-perception/image_common/tree/jazzy/image_transport/include/image_transport), accessed 2026-11-23
7. [geometry2, jazzy branch: tf2_geometry_msgs headers](https://github.com/ros2/geometry2/tree/jazzy/tf2_geometry_msgs/include/tf2_geometry_msgs), accessed 2026-11-23
8. [cv_bridge 4.1.0, Jazzy release: include/cv_bridge](https://github.com/ros2-gbp/vision_opencv-release/tree/release/jazzy/cv_bridge/4.1.0-1), accessed 2026-11-23
