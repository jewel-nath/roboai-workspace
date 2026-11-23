---
type: tool
name: KISS-ICP
summary: MIT-licensed 3D lidar odometry from the University of Bonn that works with few parameters; a pip package plus a ROS 2 node built from source (no rosdistro release). Odometry only, so pair it with a mapping back end.
tags: [lidar-odometry, 3d-lidar, icp, point-cloud, deskewing, odometry, python, pip, ros2, prbonn, baseline]
kind: library
area: perception
support:
license: MIT
links: {repo: "https://github.com/PRBonn/kiss-icp", docs: "https://github.com/PRBonn/kiss-icp/tree/main/ros", site: }
version: {tested: , latest: 1.3.0, as_of: 2026-11-23}
platforms: [linux, macos, windows]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/PRBonn/kiss-icp", title: "KISS-ICP repository: README, LICENSE, CI workflows, tags and history", accessed: 2026-11-23}
  - {url: "https://github.com/PRBonn/kiss-icp/tree/main/ros", title: "KISS-ICP ROS 2 wrapper: README, odometry.launch.py, config.yaml, OdometryServer and Utils sources", accessed: 2026-11-23}
  - {url: "https://github.com/PRBonn/kiss-icp/tree/main/python", title: "KISS-ICP Python package: README, pyproject.toml, pipeline and dataloaders", accessed: 2026-11-23}
  - {url: "https://pypi.org/project/kiss-icp/", title: "kiss-icp on PyPI: releases and wheels", accessed: 2026-11-23}
  - {url: "https://github.com/PRBonn/kiss-slam", title: "KISS-SLAM repository: README, LICENSE, pyproject.toml", accessed: 2026-11-23}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-23}
---

# KISS-ICP

KISS-ICP estimates motion from a 3D lidar alone: point-to-point ICP against a local voxel map,
with an adaptive threshold and optional deskewing [1][2]. From the PRBonn lab at the University
of Bonn and MIT-licensed, it claims to work in most cases without tuning [1]. **No ROS 2 binary
release** exists in any distro: build the node from source [2][6]. It is odometry only, with no
loop closure and no global map. Last commit 2026-05-04; newest release 1.3.0 (2026-04-26) [1][4].

## When to use it

- **Use it** for robust odometry from a spinning 3D lidar, or as a dataset baseline: the Python
  pipeline reads bags, MCAP, Ouster pcap and [KITTI](../learning/datasets/kitti.md) [3].
- **Pair it with a back end:** [RTAB-Map](rtab-map.md) takes any odometry on `odom`;
  [robot_localization](robot-localization.md) fuses it with wheels and IMU. The lab's KISS-SLAM
  adds loop closure (MIT, `pip install kiss-slam` 0.0.2, offline, no ROS node) [5].
- **Use something else** with an IMU ([LIO-SAM](lio-sam.md), FAST-LIO2) or a 2D lidar
  ([SLAM Toolbox](slam-toolbox.md)).

## Setup

```bash
python3 -m venv ~/kiss && ~/kiss/bin/pip install "kiss-icp[all]"   # [all] adds the viewer
cd ~/ros2_ws/src && git clone https://github.com/PRBonn/kiss-icp      # ROS 2 node, from source
cd ~/ros2_ws && colcon build --packages-select kiss_icp
```

Wheels: Linux x86-64 and aarch64, macOS arm64, Windows x86-64, CPython 3.8 to 3.13 [4]. CI
builds the ROS 2 node on Humble, Jazzy, Kilted and Rolling [1]. CPU only; nothing needs a GPU [3].

## How an agent works with it

- **ROS 2:** `ros2 launch kiss_icp odometry.launch.py topic:=/points base_frame:=base_link
  use_sim_time:=false visualize:=false` subscribes to `PointCloud2` (sensor-data QoS) and
  publishes `/kiss/odometry`, TF and, with `publish_debug_clouds`, `/kiss/local_map` [2].
- **Frames:** by default (`invert_odom_tf` true) it publishes `base_frame → odom_lidar` (the
  lidar frame when `base_frame` is empty), so it never fights wheel odometry for `base_link` [2].
  To be the `odom` source: `invert_odom_tf:=false lidar_odom_frame:=odom`, other odometry TF off.
- **Offline:** `kiss_icp_pipeline --dataloader kitti --sequence 07 <kitti root>` (or a bag or
  MCAP path) saves poses in KITTI and TUM formats for scoring against ground truth [3].

## Traps

- **Frozen clock on hardware.** `odometry.launch.py` defaults `use_sim_time` to true, for bags;
  pass `use_sim_time:=false` [2].
- **No deskewing.** Without a per-point time field (`t`, `timestamp`, `time` or `time_stamp`)
  it warns once and skips deskewing [2].
- **Coarse map indoors.** `voxel_size` defaults to `max_range / 100` with `max_range` at 100 m,
  so 1 m voxels. Set `data.max_range` to the lidar's real range [2].
- **Config beats command line.** ROS parameters in the YAML override the same launch arguments [2].
- **Drift is never corrected.** Error grows with distance, and nothing closes the loop without a
  back end [1].

## Alternatives

[LIO-SAM](lio-sam.md), FAST-LIO2, [RTAB-Map](rtab-map.md) (`icp_odometry`), [PCL](pcl.md),
[Open3D](open3d.md); see [Choose a SLAM system](../guides/choose-a-slam-system.md).

## Sources

1. [KISS-ICP repository: README, LICENSE, CI workflows, tags and history](https://github.com/PRBonn/kiss-icp), accessed 2026-11-23
2. [KISS-ICP ROS 2 wrapper: README, odometry.launch.py, config.yaml, OdometryServer and Utils sources](https://github.com/PRBonn/kiss-icp/tree/main/ros), accessed 2026-11-23
3. [KISS-ICP Python package: README, pyproject.toml, pipeline and dataloaders](https://github.com/PRBonn/kiss-icp/tree/main/python), accessed 2026-11-23
4. [kiss-icp on PyPI: releases and wheels](https://pypi.org/project/kiss-icp/), accessed 2026-11-23
5. [KISS-SLAM repository: README, LICENSE, pyproject.toml](https://github.com/PRBonn/kiss-slam), accessed 2026-11-23
6. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-23
