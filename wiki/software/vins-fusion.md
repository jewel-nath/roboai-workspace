---
type: tool
name: VINS-Fusion
summary: HKUST's optimisation-based visual-inertial estimator (mono plus IMU, stereo, stereo plus IMU, loose GPS fusion) and a common VIO baseline; GPL-3.0, ROS 1 only upstream and unmaintained since 2021, with an unofficial ROS 2 port.
tags: [vins-fusion, vins-mono, visual-inertial-odometry, vio, stereo, imu, ceres, loop-closure, hkust, baseline, gpl]
kind: library
area: perception
support:
license: GPL-3.0-only
links: {repo: "https://github.com/HKUST-Aerial-Robotics/VINS-Fusion", docs: , site: }
version: {tested: , latest: , as_of: 2026-11-23}
platforms: [linux]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/HKUST-Aerial-Robotics/VINS-Fusion", title: "VINS-Fusion repository: README, LICENCE, package.xml, source headers and history", accessed: 2026-11-23}
  - {url: "https://github.com/zinuok/VINS-Fusion-ROS2", title: "zinuok/VINS-Fusion-ROS2: README, CMakeLists, launch, config, source and history", accessed: 2026-11-23}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-23}
  - {url: "http://ceres-solver.org/version_history.html", title: "Ceres Solver version history (2.1.0 and 2.2.0)", accessed: 2026-11-23}
  - {url: "https://packages.ubuntu.com/noble/libceres-dev", title: "Ubuntu 24.04 package: libceres-dev", accessed: 2026-11-23}
  - {url: "https://github.com/ros2-gbp/vision_opencv-release/tree/release/jazzy/cv_bridge/4.1.0-1", title: "cv_bridge 4.1.0, Jazzy release: include/cv_bridge", accessed: 2026-11-23}
---

# VINS-Fusion

VINS-Fusion estimates a camera's motion by sliding-window optimisation (Ceres) over visual feature
tracks and preintegrated IMU data. It runs mono plus IMU, stereo plus IMU or stereo alone,
calibrates the camera-IMU transform and time offset online, closes loops and can fuse GPS [1]. A
common VIO baseline for drones, cars and AR/VR. **Unmaintained**: the last commit is from
2021-07-26, upstream targets ROS 1 Kinetic and Melodic on Ubuntu 16.04 and 18.04, has no tags, and
no ROS 2 distro has a release [1][3]; about 200 issues are open [1]. For VIO on ROS 2 use
[OpenVINS](openvins.md). GPL-3.0; the source headers name v3.0 only [1].

## When to use it

To reproduce a baseline on EuRoC or [KITTI](../learning/datasets/kitti.md), whose examples ship in
the repo [1], or to keep a stack built on it. Otherwise prefer [OpenVINS](openvins.md) (maintained,
ROS 2 build) or [ORB-SLAM3](orb-slam3.md) (visual-inertial SLAM with saved maps), both GPL too.

## Setup

Upstream builds with `catkin_make` on ROS 1 and needs Ceres [1]. On ROS 2, the unofficial zinuok
port is the live one: GPL-3.0, commits in February, March and April 2026 [2].

```bash
sudo apt install libceres-dev libeigen3-dev ros-jazzy-cv-bridge
cd ~/ros2_ws/src && git clone https://github.com/zinuok/VINS-Fusion-ROS2.git
cd .. && colcon build --symlink-install && source install/setup.bash
ros2 launch vins euroc.launch.py      # stereo plus IMU EuRoC config; config_path:=<yaml> for yours
```

Its README still says Ubuntu 20.04, Foxy and OpenCV 3.4.1 with CUDA; the code builds the CPU path
unless you enable `GPU_MODE` in `feature_tracker.h`. ROS 1 bags convert with `rosbags` [2].

## How an agent works with it

`vins_node` takes one YAML: `imu_topic`, `image0_topic`, `image1_topic`, camera calibration files,
`body_T_cam0` and IMU noise; images and IMU use sensor-data QoS [2]. It publishes `odometry`,
`imu_propagate` (IMU rate), `path`, point clouds and a TF `world → body` (the IMU), renamed by
`world_frame_id` and `body_frame_id` since April 2026 [2]. `loop_fusion_node` closes loops [1][2].

## Traps

- **Ceres 2.2 breaks upstream.** It uses `ceres::LocalParameterization` [1], removed in Ceres 2.2.0
  [4], which Ubuntu 24.04 ships [5]; the port moved to `ceres::Manifold` in March 2026 [2].
- **cv_bridge header flip-flop.** Jazzy's cv_bridge ships only `cv_bridge.hpp` [6]. The port's
  February 2026 Jazzy fix switched seven includes to it; the March Humble commit switched them
  back to `cv_bridge.h` [2]. On Jazzy, reapply the February change.
- **Frames outside REP 105.** `world` and `body` match no robot frame; feed `odometry` into
  [robot_localization](robot-localization.md) or rename the frames, but never let two nodes
  publish the same TF [2].
- **Calibration taken as given.** With `estimate_extrinsic: 0` it trusts `body_T_cam0`, and with
  `estimate_td: 0` the time offset `td` [2]. Calibrate with [Kalibr](kalibr.md), or set them to 1
  to refine a rough guess online.

## Alternatives

[OpenVINS](openvins.md), [ORB-SLAM3](orb-slam3.md), [RTAB-Map](rtab-map.md) with a stereo or RGB-D
camera; see the [SLAM guide](../guides/choose-a-slam-system.md).

## Sources

1. [VINS-Fusion repository: README, LICENCE, package.xml, source headers and history](https://github.com/HKUST-Aerial-Robotics/VINS-Fusion), accessed 2026-11-23
2. [zinuok/VINS-Fusion-ROS2: README, CMakeLists, launch, config, source and history](https://github.com/zinuok/VINS-Fusion-ROS2), accessed 2026-11-23
3. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-23
4. [Ceres Solver version history (2.1.0 and 2.2.0)](http://ceres-solver.org/version_history.html), accessed 2026-11-23
5. [Ubuntu 24.04 package: libceres-dev](https://packages.ubuntu.com/noble/libceres-dev), accessed 2026-11-23
6. [cv_bridge 4.1.0, Jazzy release: include/cv_bridge](https://github.com/ros2-gbp/vision_opencv-release/tree/release/jazzy/cv_bridge/4.1.0-1), accessed 2026-11-23
