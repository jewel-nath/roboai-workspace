---
type: tool
name: GTSAM
summary: Georgia Tech's BSD-licensed C++ and Python library for factor graphs and smoothing (iSAM2, IMU preintegration), the optimiser inside LIO-SAM and many SLAM and VIO systems; 4.3.0 is current, while Jazzy still ships 4.2.0.
tags: [gtsam, factor-graph, isam2, smoothing, slam, pose-graph, imu-preintegration, nonlinear-least-squares, python, cpp, borglab]
kind: library
area: perception
support:
license: BSD-3-Clause
links: {repo: "https://github.com/borglab/gtsam", docs: "https://borglab.github.io/gtsam/", site: "https://gtsam.org"}
version: {tested: , latest: 4.3.0, as_of: 2026-11-23}
platforms: [linux, macos, windows]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/borglab/gtsam", title: "GTSAM repository, develop: README, LICENSE, LICENSE.BSD, package.xml, CMakeLists.txt and cmake/", accessed: 2026-11-23}
  - {url: "https://github.com/borglab/gtsam/blob/develop/INSTALL.md", title: "GTSAM installation guide", accessed: 2026-11-23}
  - {url: "https://github.com/borglab/gtsam/blob/develop/python/README.md", title: "GTSAM Python wrapper README", accessed: 2026-11-23}
  - {url: "https://github.com/borglab/gtsam/tree/develop/python/gtsam/examples", title: "GTSAM Python examples: Pose2ISAM2Example, ImuFactorISAM2Example, CombinedImuFactorExample", accessed: 2026-11-23}
  - {url: "https://github.com/borglab/gtsam/blob/develop/gtsam/navigation/PreintegrationParams.h", title: "GTSAM PreintegrationParams.h", accessed: 2026-11-23}
  - {url: "https://github.com/borglab/gtsam/releases/tag/4.3.0", title: "GTSAM 4.3.0 release notes", accessed: 2026-11-23}
  - {url: "https://github.com/borglab/gtsam/tree/4.2.0/cmake", title: "GTSAM 4.2.0 tag: HandleEigen.cmake and GtsamBuildTypes.cmake", accessed: 2026-11-23}
  - {url: "https://pypi.org/project/gtsam/", title: "gtsam on PyPI (4.3.0 wheels)", accessed: 2026-11-23}
  - {url: "https://borglab.github.io/gtsam/", title: "GTSAM documentation site", accessed: 2026-11-23}
  - {url: "https://launchpad.net/~borglab/+archive/ubuntu/gtsam-release-4.2/+packages", title: "BorgLab PPA gtsam-release-4.2: published packages", accessed: 2026-11-23}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling (gtsam)", accessed: 2026-11-23}
  - {url: "https://github.com/TixiaoShan/LIO-SAM/blob/ros2/README.md", title: "LIO-SAM README, ros2 branch", accessed: 2026-11-23}
  - {url: "https://github.com/HKUST-Aerial-Robotics/VINS-Fusion", title: "VINS-Fusion README (Ceres Solver)", accessed: 2026-11-23}
  - {url: "https://github.com/UZ-SLAMLab/ORB_SLAM3/blob/master/Dependencies.md", title: "ORB-SLAM3 Dependencies.md (g2o)", accessed: 2026-11-23}
---

# GTSAM

GTSAM (Georgia Tech Smoothing and Mapping) treats estimation as a factor graph: the unknowns
(poses, landmarks, velocities, IMU biases) are variables, each measurement is a factor, and
nonlinear least squares finds the most likely values [1][9]. iSAM2 updates that solution as new
measurements arrive instead of solving from scratch. Builders meet it inside SLAM systems such as
[LIO-SAM](lio-sam.md) [12], and use it directly to write their own estimator. The licence is
BSD-3-Clause (three clauses, though the LICENSE file and PyPI call it "simplified BSD"); bundled
Eigen is MPL-2.0 and METIS Apache-2.0 [1][8]. Active: the newest commit is from 2026-11-21 [1].

| Version | Date | Where |
|---|---|---|
| 4.2.0 | 2023-09-03 | `ros-jazzy-gtsam`, `ros-humble-gtsam`; BorgLab PPA |
| **4.3.0** | 2026-09-18 | Lyrical binary; `pip install gtsam` |
| 4.3.1 | — | Kilted and Rolling binaries; no upstream tag for it |
| 4.3.2 | — | `develop` branch, not released |

Tags and versions from the repo [1], ROS binaries from rosdistro, where its status is
`developed` [11], PyPI [8]. 4.3.0 needs C++17, makes Boost optional, removes code deprecated in
4.2, and adds hybrid discrete-continuous inference, GNSS factors and experimental CUDA solvers [6].

## When to use it

- **Your own estimator from parts**: wheel odometry, IMU preintegration and GPS in a smoother;
  pose-graph optimisation of a mapping run with loop closures; structure from motion [4].
- **Use a packaged system when one fits**: [LIO-SAM](lio-sam.md) for lidar-inertial (GTSAM inside),
  [robot_localization](robot-localization.md) for a plain EKF over odometry and IMU, and
  [OpenVINS](openvins.md) or [ORB-SLAM3](orb-slam3.md) for cameras.
- **Python to prototype, C++ on the robot.** The Python wrapper mirrors the C++ classes [3].

## Setup

Python, Ubuntu 24.04 (the system Python refuses a bare `pip install`, PEP 668) [3]:

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install gtsam
python -c "import gtsam; print(gtsam.Pose2(1, 2, 0.5))"
```

4.3.0 wheels cover CPython 3.11–3.14 on Linux x86-64 and aarch64 and macOS universal2; there is
no Windows wheel [8]. `gtsam-develop` holds nightly wheels of `develop` [1][8].
**ROS 2 Jazzy**: `sudo apt install ros-jazzy-gtsam` gives 4.2.0 [11]. Link it from your package
with `find_package(GTSAM REQUIRED)` and `target_link_libraries(<target> gtsam)` [2].

**From source** (CMake 3.16+, GCC 11–15, Clang, Xcode 16 or MSVC 14.40) [2]:

```bash
sudo apt install cmake libeigen3-dev libtbb-dev libboost-all-dev
git clone --depth 1 --branch 4.3.0 https://github.com/borglab/gtsam.git
cmake -S gtsam -B build -DCMAKE_BUILD_TYPE=Release -DGTSAM_BUILD_WITH_MARCH_NATIVE=OFF
cmake --build build -j4 && sudo cmake --install build
```

Boost is needed only while `GTSAM_USE_BOOST_FEATURES` or `GTSAM_ENABLE_BOOST_SERIALIZATION` is
on; both default on in plain CMake builds and off in colcon or `/opt/ros` builds [2]. Add
`-DGTSAM_BUILD_PYTHON=ON` for the wrapper. The BorgLab PPA publishes 4.2.0 for Ubuntu 18.04, 20.04
and 22.04, not 24.04 [10]. Windows builds use CMake with Ninja or Visual Studio [2]. The CPU does
the work; CUDA solvers are optional and need compute capability 6.0+ [2].

## How an agent works with it

GTSAM is a library, not a ROS node: an agent writes a script or a node that builds the graph. A
2D pose graph with iSAM2, after `Pose2ISAM2Example` and `ImuFactorISAM2Example` [4]:

```python
import numpy as np
import gtsam
from gtsam.symbol_shorthand import X

graph, guess = gtsam.NonlinearFactorGraph(), gtsam.Values()
prior = gtsam.noiseModel.Diagonal.Sigmas(np.array([0.1, 0.1, 0.05]))
odom = gtsam.noiseModel.Diagonal.Sigmas(np.array([0.2, 0.2, 0.1]))
graph.push_back(gtsam.PriorFactorPose2(X(0), gtsam.Pose2(0, 0, 0), prior))
graph.push_back(gtsam.BetweenFactorPose2(X(0), X(1), gtsam.Pose2(1.0, 0, 0), odom))
guess.insert(X(0), gtsam.Pose2(0, 0, 0))
guess.insert(X(1), gtsam.Pose2(0.9, 0.1, 0.0))

isam = gtsam.ISAM2(gtsam.ISAM2Params())
isam.update(graph, guess)
graph, guess = gtsam.NonlinearFactorGraph(), gtsam.Values()   # next update: new items only
print(isam.calculateEstimate().atPose2(X(1)))
```

The parts an agent combines [1][4][5]:

- **Variables** are keyed by symbols (`X(i)` poses, `V(i)` velocities, `B(i)` biases, `L(j)`
  landmarks). **Factors**: priors, between factors (odometry, loop closures), projection factors,
  `ImuFactor` or `CombinedImuFactor` over `PreintegratedImuMeasurements`, GPS factors.
- **Noise models**: `noiseModel.Diagonal.Sigmas`, wrapped in `noiseModel.Robust` with an
  M-estimator such as Huber to tame outliers.
- **Solvers**: `LevenbergMarquardtOptimizer` for a batch problem, `ISAM2` for incremental use,
  fixed-lag smoothers to bound memory; `Marginals` gives covariances.

**Check the result**: `graph.error(values)` should fall sharply after optimising, as the IMU
examples print [4]. Compare the trajectory with ground truth, for example on
[KITTI](../learning/datasets/kitti.md) or [TUM RGB-D](../learning/datasets/tum-rgbd.md). The skill
[skills/perception-slam/SKILL.md](../../skills/perception-slam/SKILL.md) covers SLAM workflows.

## Traps

- **Two GTSAMs on one machine.** LIO-SAM's ROS 2 README installs the 4.1 PPA and blames
  mapOptimization crashes on a wrong GTSAM [12]; Jazzy's apt package is 4.2.0 [11]. Build every
  consumer against one copy, and check which `GTSAMConfig.cmake` CMake found (`/opt/ros/jazzy` or
  `/usr/local`).
- **`-march=native` by default.** 4.3.0 turns `GTSAM_BUILD_WITH_MARCH_NATIVE` on for non-MSVC
  builds; 4.2.0 left it off [1][7]. Every project that links GTSAM must use the same flag, or it
  may segfault, and the binary may not run on another CPU [2]. Turn it off for anything you ship.
- **Eigen mismatch.** Plain CMake builds use GTSAM's bundled Eigen; since 4.3, ROS builds use the
  system Eigen so GTSAM and other ROS packages agree [1]. 4.2.0 always defaulted to the bundled
  copy [7]. When your code links system Eigen, set `-DGTSAM_USE_SYSTEM_EIGEN=ON`.
- **TBB is on when found.** It can slow small problems and grow memory; benchmark, set
  `-DGTSAM_TBB_BOUNDED_MEMORY_GROWTH=ON`, or `-DGTSAM_WITH_TBB=OFF` when TBB is missing [2][3].
- **Debug builds are slow.** Debug enables heavy assertions; time and run in Release [2].
- **Porting 4.2 code to 4.3.** Code deprecated in 4.2 is gone [6];
  `GTSAM_ALLOW_DEPRECATED_SINCE_V43` (on by default) keeps 4.3's own deprecations for now.
  `Point2` and `Point3` are Eigen vectors whose default constructor leaves them uninitialised [1].
- **Gravity direction.** `PreintegrationParams.MakeSharedU` is for z-up frames such as ENU (ROS,
  REP 103), `MakeSharedD` for z-down frames such as NED [5]; match the frame of your IMU data.
- **Re-adding the whole graph to iSAM2.** Pass only new factors and values to `update()`;
  `ImuFactorISAM2Example` starts a new graph and clears the values after each call [4].

## Alternatives

Ceres Solver (used by [VINS-Fusion](vins-fusion.md)) and g2o (inside [ORB-SLAM3](orb-slam3.md))
are the other common optimisers [13][14]. For filters rather than smoothers, see
[robot_localization](robot-localization.md) and [OpenVINS](openvins.md). The
[SLAM guide](../guides/choose-a-slam-system.md) compares complete systems.

## Sources

1. [GTSAM repository, develop: README, LICENSE, LICENSE.BSD, package.xml, CMakeLists.txt and cmake/](https://github.com/borglab/gtsam), accessed 2026-11-23
2. [GTSAM installation guide](https://github.com/borglab/gtsam/blob/develop/INSTALL.md), accessed 2026-11-23
3. [GTSAM Python wrapper README](https://github.com/borglab/gtsam/blob/develop/python/README.md), accessed 2026-11-23
4. [GTSAM Python examples: Pose2ISAM2Example, ImuFactorISAM2Example, CombinedImuFactorExample](https://github.com/borglab/gtsam/tree/develop/python/gtsam/examples), accessed 2026-11-23
5. [GTSAM PreintegrationParams.h](https://github.com/borglab/gtsam/blob/develop/gtsam/navigation/PreintegrationParams.h), accessed 2026-11-23
6. [GTSAM 4.3.0 release notes](https://github.com/borglab/gtsam/releases/tag/4.3.0), accessed 2026-11-23
7. [GTSAM 4.2.0 tag: HandleEigen.cmake and GtsamBuildTypes.cmake](https://github.com/borglab/gtsam/tree/4.2.0/cmake), accessed 2026-11-23
8. [gtsam on PyPI (4.3.0 wheels)](https://pypi.org/project/gtsam/), accessed 2026-11-23
9. [GTSAM documentation site](https://borglab.github.io/gtsam/), accessed 2026-11-23
10. [BorgLab PPA gtsam-release-4.2: published packages](https://launchpad.net/~borglab/+archive/ubuntu/gtsam-release-4.2/+packages), accessed 2026-11-23
11. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling (gtsam)](https://github.com/ros/rosdistro), accessed 2026-11-23
12. [LIO-SAM README, ros2 branch](https://github.com/TixiaoShan/LIO-SAM/blob/ros2/README.md), accessed 2026-11-23
13. [VINS-Fusion README (Ceres Solver)](https://github.com/HKUST-Aerial-Robotics/VINS-Fusion), accessed 2026-11-23
14. [ORB-SLAM3 Dependencies.md (g2o)](https://github.com/UZ-SLAMLab/ORB_SLAM3/blob/master/Dependencies.md), accessed 2026-11-23
