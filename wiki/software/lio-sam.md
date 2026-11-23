---
type: tool
name: LIO-SAM
summary: Tightly coupled lidar-inertial odometry and mapping on GTSAM (IROS 2020), still a common baseline; BSD-3-Clause, no ROS 2 binaries, a source-only ros2 branch tested to Humble, and a strict 9-axis IMU requirement.
tags: [lidar-inertial-odometry, lio, 3d-lidar, imu, gtsam, factor-graph, loop-closure, gps, mapping, ros2, baseline]
kind: library
area: perception
support:
license: BSD-3-Clause
links: {repo: "https://github.com/TixiaoShan/LIO-SAM", docs: "https://github.com/TixiaoShan/LIO-SAM/tree/ros2", site: }
version: {tested: , latest: , as_of: 2026-11-23}
platforms: [linux]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/TixiaoShan/LIO-SAM", title: "LIO-SAM repository, master branch: README, LICENSE, history, tags", accessed: 2026-11-23}
  - {url: "https://github.com/TixiaoShan/LIO-SAM/tree/ros2", title: "LIO-SAM ros2 branch: README, LICENSE, package.xml, params.yaml, run.launch.py, Dockerfile, sources, history", accessed: 2026-11-23}
  - {url: "https://github.com/TixiaoShan/LIO-SAM/issues", title: LIO-SAM issue tracker, accessed: 2026-11-23}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling (lio_sam absent; gtsam)", accessed: 2026-11-23}
  - {url: "https://github.com/hku-mars/FAST_LIO", title: "FAST_LIO repository: LICENSE, package.xml and README, main and ROS2 branches", accessed: 2026-11-23}
---

# LIO-SAM

LIO-SAM fuses a 3D lidar and an IMU in GTSAM factor graphs: IMU preintegration gives odometry at
IMU rate, and a mapping graph adds lidar odometry, GPS and loop closure factors [2]. BSD-3-Clause
[1][2]. **No ROS 2 binary release in any distro, and no release tags** [1][4]: ROS 2 support is a
source-only `ros2` branch tested on Foxy, Galactic and Humble [2]. `master` has had no commit since
2023-04-17; `ros2` merges occasional fixes (2025-02-14, 2026-11-19); 178 issues are open [1][2][3].

## When to use it

- **Use it** with a spinning lidar and a good 9-axis IMU, optionally GPS, or as a baseline [2].
  **Not** with a 6-axis IMU (such as the Ouster's internal one) or a solid-state lidar: the README
  supports mechanical lidars only, and `ros2` was tested with Ouster lidars only [2].
- **Maintained successor:** FAST-LIO2 (`hku-mars/FAST_LIO`) supports spinning and solid-state
  lidars; GPL-2.0 per its LICENSE (its package.xml says BSD); its ROS2 branch has a community
  maintainer, last commit 2026-10-25 [5]. Lidar only: [KISS-ICP](kiss-icp.md).

## Setup

```bash
cd ~/ros2_ws/src && git clone -b ros2 https://github.com/TixiaoShan/LIO-SAM.git
cd ~/ros2_ws && rosdep install --from-paths src --ignore-src -y && colcon build
ros2 launch lio_sam run.launch.py    # then play a bag or start the drivers
```

The README uses GTSAM 4.1 from the borglab PPA on Ubuntu 22.04; since 2025 rosdep resolves it, on
Jazzy to `ros-jazzy-gtsam` 4.2.0, a pairing the README never tested [2][4]. CPU only.

## How an agent works with it

- **Config** (`config/params.yaml`) [2]: `pointCloudTopic` `/points`, `imuTopic` `/imu/data`,
  `gpsTopic`; frames `lidar_link`, `base_link`, `odom`, `map`; `sensor` (default `ouster`),
  `N_SCAN`, `Horizon_SCAN`; IMU extrinsics `extrinsicTrans`, `extrinsicRot`, `extrinsicRPY`.
- **Launch** starts `robot_state_publisher`, a static `map → odom`, the four `lio_sam_*` nodes
  and RViz; the nodes publish `odom → base_link` [2]. No ROS 2 sample data is provided [2].
- **Save the map:** `ros2 service call /lio_sam/save_map lio_sam/srv/SaveMap "{resolution: 0.2,
  destination: /Downloads/service_LOAM}"` [2].

## Traps

- **The IMU decides everything.** It must be 9-axis with an orientation estimate (roll and pitch
  start the system; yaw sets the GPS heading), at 200 Hz or more; the authors used 500 Hz [2].
- **Wrong extrinsics.** `extrinsicRot` rotates gyro and accelerometer data, `extrinsicRPY` the
  orientation, and they can differ. A pose jumping up and down at start means wrong extrinsics [2].
- **Missing point fields.** Deskewing needs a per-point relative `time` (0 to 0.1 s at 10 Hz) and
  a `ring`. Zigzag motion means lidar and IMU stamps are not synchronised [2].
- **Two odometry publishers.** Turn off wheel or EKF `odom → base_link` TF. Its launch file gives
  `static_transform_publisher` positional arguments: Jazzy warns, Lyrical rejects ([tf2](tf2.md)).
- **Crashes and lost folders.** `mapOptimization` crashes usually mean a GTSAM mismatch; with
  `savePCD` on, the code deletes and recreates `savePCDDirectory` [2].

## Alternatives

FAST-LIO2, [KISS-ICP](kiss-icp.md), [RTAB-Map](rtab-map.md) (which can use LIO-SAM as odometry),
[GTSAM](gtsam.md) (the library underneath). See
[Choose a SLAM system](../guides/choose-a-slam-system.md).

## Sources

1. [LIO-SAM repository, master branch: README, LICENSE, history, tags](https://github.com/TixiaoShan/LIO-SAM), accessed 2026-11-23
2. [LIO-SAM ros2 branch: README, LICENSE, package.xml, params.yaml, run.launch.py, Dockerfile, sources, history](https://github.com/TixiaoShan/LIO-SAM/tree/ros2), accessed 2026-11-23
3. [LIO-SAM issue tracker](https://github.com/TixiaoShan/LIO-SAM/issues), accessed 2026-11-23
4. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling (lio_sam absent; gtsam)](https://github.com/ros/rosdistro), accessed 2026-11-23
5. [FAST_LIO repository: LICENSE, package.xml and README, main and ROS2 branches](https://github.com/hku-mars/FAST_LIO), accessed 2026-11-23
