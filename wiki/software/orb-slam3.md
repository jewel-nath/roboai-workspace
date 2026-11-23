---
type: tool
name: ORB-SLAM3
summary: The reference feature-based visual and visual-inertial SLAM library (mono, stereo, RGB-D; pinhole and fisheye) from the University of Zaragoza; GPL-3.0-or-later, untouched since 2022, with no ROS 2 release and only community wrappers.
tags: [orb-slam3, orb-slam2, visual-slam, visual-inertial, monocular, stereo, rgb-d, loop-closure, atlas, baseline, gpl]
kind: library
area: perception
support:
license: GPL-3.0-or-later
links: {repo: "https://github.com/UZ-SLAMLab/ORB_SLAM3", docs: , site: }
version: {tested: , latest: v1.0-release, as_of: 2026-11-23}
platforms: [linux]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/UZ-SLAMLab/ORB_SLAM3", title: "ORB_SLAM3 repository: README, LICENSE, Dependencies.md, Changelog, CMakeLists.txt, build.sh, master and c++14_comp branches", accessed: 2026-11-23}
  - {url: "https://github.com/stevenlovegrove/Pangolin/blob/master/CMakeLists.txt", title: "Pangolin CMakeLists.txt (C++17)", accessed: 2026-11-23}
  - {url: "https://github.com/Mechazo11/ros2_orb_slam3/tree/jazzy", title: "Mechazo11/ros2_orb_slam3, jazzy branch: README and history", accessed: 2026-11-23}
  - {url: "https://github.com/suchetanrs/ORB-SLAM3-ROS2-Docker", title: "suchetanrs/ORB-SLAM3-ROS2-Docker: README, package.xml, params and history", accessed: 2026-11-23}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-23}
  - {url: "https://packages.ubuntu.com/noble/libopencv-dev", title: "Ubuntu 24.04 package: libopencv-dev", accessed: 2026-11-23}
---

# ORB-SLAM3

A C++ SLAM library that tracks ORB features, closes loops by place recognition (DBoW2) and keeps
several maps in an Atlas, on monocular, stereo or RGB-D cameras, with or without an IMU [1].
Builders use it as the visual SLAM baseline papers compare against. **Unmaintained**: v1.0 is from
December 2021, the last `master` commit from 2022-02-10, and no ROS 2 distro has a release [1][5].
Use [RTAB-Map](rtab-map.md) for maintained visual SLAM, [OpenVINS](openvins.md) for VIO.

## When to use it

For research, a baseline on EuRoC, TUM-VI or [TUM RGB-D](../learning/datasets/tum-rgbd.md) [1].
In a product, only if GPL-3.0-or-later suits you; the authors offer a closed-source version [1].

## Setup

Upstream tested Ubuntu 16.04 and 18.04 with OpenCV 3.2.0 and 4.4.0; it needs Pangolin, Eigen 3.1+
and OpenCV, and bundles DBoW2, g2o (BSD) and Sophus (MIT) [1]. No apt package exists [5].

```bash
sudo apt install build-essential cmake libeigen3-dev libopencv-dev python3-numpy
# build and install Pangolin from source first (the viewer), then:
git clone --depth 1 https://github.com/UZ-SLAMLab/ORB_SLAM3.git && cd ORB_SLAM3
./build.sh   # third-party libs, unpacks Vocabulary/ORBvoc.txt, builds lib/libORB_SLAM3.so
```

Run `Examples/Stereo-Inertial/stereo_inertial_euroc` with the vocabulary, `EuRoC.yaml`, a sequence
folder and its timestamps file [1]. CPU only; the README asks for an i7-class CPU [1].

## How an agent works with it

A run needs the vocabulary and a settings YAML (`File.version: "1.0"`) with camera intrinsics,
`IMU.T_b_c1` and IMU noise [1]; get them with [Kalibr](kalibr.md). Upstream's ROS nodes are ROS 1
Melodic [1]. Community ROS 2 wrappers:

- **Mechazo11/ros2_orb_slam3**, `jazzy` branch: tested on Jazzy, last commit 2025-11-21;
  monocular only, and the workspace must be named `ros2_ws` (a hard-coded path) [3].
- **suchetanrs/ORB-SLAM3-ROS2-Docker**: Humble on Ubuntu 22.04 in Docker; mono, stereo, RGB-D,
  each with or without IMU; `publish_tf` and `odometry_mode` parameters; last commit 2026-07-24 [4].

## Traps

- **C++ standard clash.** `master` forces `-std=c++11` [1]; Pangolin's CMake sets C++17 [2]. The
  upstream `c++14_comp` branch moves to C++14 [1]; raise the standard or pin an older Pangolin.
- **OpenCV drift.** CMake asks for 4.4 [1]; Ubuntu 24.04 ships 4.6.0 [6], never tested upstream.
  Link one OpenCV only, the one `cv_bridge` uses.
- **Build flags.** Release builds use `-march=native`, and `build.sh` runs `make -j` with no job
  limit [1]; build on the robot's CPU, and on a small board run its steps with `-j2`.
- **Missing helpers.** The README's `euroc_examples` scripts are not in the repo, and
  `evaluation/evaluate_ate_scale.py` is Python 2 [1]. v1.0 changed the settings format [1].
- **Two TF authorities.** With `publish_tf` on, the suchetanrs wrapper publishes `map` and `odom`
  frames [4]; keep one source, not also [robot_localization](robot-localization.md).

## Alternatives

[RTAB-Map](rtab-map.md), [OpenVINS](openvins.md), [VINS-Fusion](vins-fusion.md), NVIDIA Isaac ROS
Visual SLAM; see the [SLAM guide](../guides/choose-a-slam-system.md).

## Sources

1. [ORB_SLAM3 repository: README, LICENSE, Dependencies.md, Changelog, CMakeLists.txt, build.sh, master and c++14_comp branches](https://github.com/UZ-SLAMLab/ORB_SLAM3), accessed 2026-11-23
2. [Pangolin CMakeLists.txt (C++17)](https://github.com/stevenlovegrove/Pangolin/blob/master/CMakeLists.txt), accessed 2026-11-23
3. [Mechazo11/ros2_orb_slam3, jazzy branch: README and history](https://github.com/Mechazo11/ros2_orb_slam3/tree/jazzy), accessed 2026-11-23
4. [suchetanrs/ORB-SLAM3-ROS2-Docker: README, package.xml, params and history](https://github.com/suchetanrs/ORB-SLAM3-ROS2-Docker), accessed 2026-11-23
5. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-23
6. [Ubuntu 24.04 package: libopencv-dev](https://packages.ubuntu.com/noble/libopencv-dev), accessed 2026-11-23
