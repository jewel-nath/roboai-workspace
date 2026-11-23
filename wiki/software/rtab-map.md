---
type: tool
name: RTAB-Map
summary: Graph SLAM library and ROS 2 stack from IntRoLab for RGB-D, stereo and 2D or 3D lidar, with loop closure, multi-session SQLite map databases and occupancy grids for Nav2; BSD, with GPL and non-commercial build options.
tags: [slam, visual-slam, rgbd, stereo, lidar, loop-closure, graph-slam, occupancy-grid, octomap, localization, rtabmap-ros, ros2]
kind: library
area: perception
support:
license: BSD-3-Clause
links: {repo: "https://github.com/introlab/rtabmap", docs: "https://github.com/introlab/rtabmap_ros/tree/ros2", site: "https://introlab.github.io/rtabmap"}
version: {tested: , latest: 0.24.2, as_of: 2026-11-23}
platforms: [linux, windows, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/introlab/rtabmap", title: "RTAB-Map repository: README, LICENSE, CMakeLists.txt build options and licence summary", accessed: 2026-11-23}
  - {url: "https://github.com/introlab/rtabmap/releases", title: RTAB-Map releases, accessed: 2026-11-23}
  - {url: "https://github.com/introlab/rtabmap_ros/tree/ros2", title: "rtabmap_ros ros2 branch: README and LICENSE", accessed: 2026-11-23}
  - {url: "https://github.com/introlab/rtabmap_ros/blob/ros2/rtabmap_slam/README.md", title: "rtabmap_slam README: frames, database, update rate, odometry, mapping and localization", accessed: 2026-11-23}
  - {url: "https://github.com/introlab/rtabmap_ros/blob/ros2/rtabmap_slam/doc/rtabmap.md", title: "rtabmap node documentation: inputs, topics, services, parameters", accessed: 2026-11-23}
  - {url: "https://github.com/introlab/rtabmap_ros/blob/jazzy-devel/rtabmap_launch/launch/rtabmap.launch.py", title: "rtabmap.launch.py, jazzy-devel branch", accessed: 2026-11-23}
  - {url: "https://github.com/introlab/rtabmap_ros/blob/jazzy-devel/rtabmap_examples/launch/lidar3d.launch.py", title: "rtabmap_examples lidar3d.launch.py, jazzy-devel branch", accessed: 2026-11-23}
  - {url: "https://github.com/introlab/rtabmap/blob/jazzy-devel/corelib/include/rtabmap/core/Parameters.h", title: "RTAB-Map Parameters.h, jazzy-devel branch", accessed: 2026-11-23}
  - {url: "https://github.com/introlab/rtabmap/tree/jazzy-devel/tools", title: "RTAB-Map command-line tools (Export, DatabaseViewer, Recovery), jazzy-devel branch", accessed: 2026-11-23}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-23}
---

# RTAB-Map

RTAB-Map is a graph SLAM library with real-time constraints, from IntRoLab at the Université de
Sherbrooke [1]. It builds a map from RGB-D, stereo, 2D lidar or 3D lidar data plus odometry,
finds loop closures by image appearance or, without images, by proximity, and stores the whole
map in one SQLite database [4][5]. A builder gets a 2D occupancy grid for Nav2, a 3D point cloud
or OctoMap, and a database to localize in later [5]. Both repos are BSD-3-Clause, but some
optional built-in components are GPL or non-commercial (see Traps) [1][3].

## When to use it

- **Use it** for a robot with an RGB-D or stereo camera that needs a map with loop closure, for 3D
  lidar mapping, for camera plus lidar, and for multi-session mapping into one database [4][5].
- **2D lidar only, with Nav2:** RTAB-Map works (`Reg/Force3DoF`) [5], but
  [SLAM Toolbox](slam-toolbox.md) is the simpler, Nav2-recommended choice.
- **Odometry only:** its own `rtabmap_odom` nodes, or [KISS-ICP](kiss-icp.md) for 3D lidar and
  [VINS-Fusion](vins-fusion.md) or [OpenVINS](openvins.md) for visual-inertial. Any odometry can
  feed RTAB-Map [3].
- **Lidar plus IMU:** a tightly coupled lidar-inertial odometry such as [LIO-SAM](lio-sam.md) is
  built for that pairing; RTAB-Map can use LIO-SAM as its odometry, a build option that is off by
  default [1][8].
- See [Choose a SLAM system](../guides/choose-a-slam-system.md).

## Setup

The newest library release is 0.24.2 (tagged 2026-10-24), with app builds for Windows (CUDA 13.0
and 11.7 variants) and macOS, which also has `brew install rtabmap` [2]. The ROS binaries lag:
`rtabmap` 0.23.14 and `rtabmap_ros` 0.23.13 are released for Humble, Jazzy, Kilted, Lyrical and
Rolling [10]. Both repos had commits on 2026-11-21 or later [1][3]. On Ubuntu 24.04:

```bash
sudo apt install ros-jazzy-rtabmap-ros
```

From source, remove the binaries first (`sudo apt remove ros-jazzy-rtabmap*`), clone `rtabmap`
and the `ros2` branch of `rtabmap_ros` into a workspace, `rosdep install`, and build with
`export MAKEFLAGS="-j6"` on machines with 16 GB of RAM or less [3]. No GPU is needed. The GPU
features (SuperPoint through libtorch, CudaSift, cuVSLAM) are build options, off by default [1].

## How an agent works with it

**Packages** [3]: `rtabmap_slam` (the `rtabmap` node), `rtabmap_odom` (`rgbd_odometry`,
`stereo_odometry`, `icp_odometry`), `rtabmap_sync` (`rgbd_sync`, `stereo_sync`), `rtabmap_viz`
(the GUI), `rtabmap_launch` and `rtabmap_examples`.

**One launch for an RGB-D camera** (replace the topics with your driver's) [6]:

```bash
ros2 launch rtabmap_launch rtabmap.launch.py rtabmap_args:="--delete_db_on_start" \
  frame_id:=base_link rgb_topic:=<rgb image> depth_topic:=<depth registered to rgb> \
  camera_info_topic:=<rgb camera_info> approx_sync:=false qos:=1
```

**3D lidar** (starts `icp_odometry`, `rtabmap` and `rtabmap_viz`; `deskewing` is on by
default) [7]:

```bash
ros2 launch rtabmap_examples lidar3d.launch.py lidar_topic:=/points frame_id:=base_link
```

**Inputs** [5]:

- RGB-D: `rgb/image`, `depth/image` (registered to RGB), `rgb/camera_info`, or one `rgbd_image`
  from `rgbd_sync`, which is the recommended way. Stereo: rectified left and right images with
  both `camera_info`.
- `scan` (`LaserScan`) or `scan_cloud` (`PointCloud2`, already deskewed).
- `odom` (`nav_msgs/Odometry`), or odometry from TF with `odom_frame_id`. Its covariance weights
  each link.
- `imu`: only the orientation is used, for gravity; it must already be estimated.
- TF: odometry publishes `odom → base_link`, the URDF places the sensors on `base_link`, and
  `rtabmap` publishes `map → odom` [4].

**Outputs** (under the `rtabmap` namespace with the launch file) [5][6]: `map` (occupancy grid
for Nav2), `cloud_map`, `mapGraph`, `mapPath`, `localization_pose`, `info` (one per update, with
loop closure results), and OctoMap topics when built with OctoMap.

**Launch arguments and parameters builders change** [6][8]:

| Name | Default | What it does |
|---|---|---|
| `database_path` | `~/.ros/rtabmap.db` | Where the map is saved and loaded |
| `localization` | false | true sets `Mem/IncrementalMemory` false: localize, do not extend |
| `approx_sync` | false | Approximate time sync for sensors not stamped together |
| `qos` | 0 (system default) | 1 = reliable, 2 = best effort for sensor inputs |
| `visual_odometry`, `icp_odometry` | true, false | Which built-in odometry to start |
| `Rtabmap/DetectionRate` | 1 Hz | Map updates per second |
| `RGBD/LinearUpdate`, `RGBD/AngularUpdate` | 0.1 m, 0.1 rad | Motion needed before a new node |
| `Reg/Strategy` | 0 (visual) | 1 = ICP, 2 = visual then ICP |
| `Reg/Force3DoF` | false | true for ground robots drifting in z, roll or pitch |
| `Grid/Sensor`, `Grid/RangeMax` | 1 (depth), 5.0 m | Which sensor builds the grid, and how far |

Core parameters (`Rtabmap/*`, `Reg/*`, `Grid/*`) are string-valued ROS parameters on the node,
for example `'Reg/Force3DoF': 'true'` [5]; the parameter reference lists them all [3].

**Services** [5]: `set_mode_localization`, `set_mode_mapping`, `pause`, `resume`, `reset`
(erases the map), `trigger_new_map` (new session, same database) and `backup`.

**Checking it works:** `ros2 topic hz /rtabmap/info` should match the detection rate; the
`info` messages show loop closure ids; the map grows in `rtabmap_viz` or RViz. Offline, the tools
`rtabmap-databaseViewer` (inspect a database), `rtabmap-export` (`--cloud`, `--mesh`, `--las`)
and `rtabmap-recovery` work on the `.db` file [9]. The skill
[skills/perception-slam/SKILL.md](../../skills/perception-slam/SKILL.md) covers the workflow.

## Traps

- **Yesterday's map comes back.** A restart on an existing database continues it, and the
  database also restores the parameters it was built with. Pass `--delete_db_on_start` (`-d`) for
  a fresh map [4].
- **Killed nodes lose data.** The database is written on shutdown; a killed process loses what
  was not saved. Stop it cleanly, or try `rtabmap-recovery` on the file [4][9].
- **Frames dropped without warning.** With `qos` at 0, Fast DDS subscribes best effort and
  drops large images while a node is busy. Use `qos:=1` with Fast DDS, plus
  `FASTDDS_BUILTIN_TRANSPORTS=LARGE_DATA` on all computers or none, or switch to Cyclone DDS [3].
  See [Fast DDS](fast-dds.md) and [Cyclone DDS](cyclone-dds.md).
- **`Rtabmap/DetectionRate` at 0** with sensors above about 2 Hz makes every update a node, and
  loop closure and optimization soon become intractable [4].
- **The map splits into sessions.** An odometry reset, or odometry that returns exactly to the
  identity pose (simulators and tests driving back to the origin), starts a new map in the same
  database: the log says "Increment map id" [4].
- **Raw IMU data.** `rtabmap` uses only the IMU's orientation; feed it from an orientation filter
  such as `imu_filter_madgwick`, not raw gyro and accelerometer data [5][7].
- **Licence surprises.** A default build compiles in TORO (CC BY-NC-SA), Vertigo and ORB OcTree
  (GPLv3) and Madgwick (GPL); CMake prints each component's licence in its summary [1]. Options
  such as ORB-SLAM and SuperPoint (GPLv3) are off by default, and SURF or SIFT from an OpenCV
  built with non-free modules is marked non-commercial [1]. The default features are GFTT/ORB or
  GFTT/BRIEF, not SURF [8]. For a commercial product, assume the apt binaries match the default
  build until you check, or build with `-DWITH_TORO=OFF -DWITH_VERTIGO=OFF -DWITH_ORB_OCTREE=OFF
  -DWITH_MADGWICK=OFF` and read the summary.
- **ROS 1 tutorials.** Much of the wiki is ROS 1; parameters and topic names are the same, and
  `rtabmap.launch` became `rtabmap.launch.py` with the same arguments [3].

## Alternatives

- 2D lidar: [SLAM Toolbox](slam-toolbox.md), [Cartographer](cartographer.md).
- Visual and visual-inertial: [ORB-SLAM3](orb-slam3.md), [VINS-Fusion](vins-fusion.md),
  [OpenVINS](openvins.md), and NVIDIA's cuVSLAM in Isaac ROS.
- Lidar odometry: [KISS-ICP](kiss-icp.md), [LIO-SAM](lio-sam.md); 3D occupancy: [OctoMap](octomap.md).
- Fusing wheel odometry and IMU before SLAM: [robot_localization](robot-localization.md).

## Sources

1. [RTAB-Map repository: README, LICENSE, CMakeLists.txt build options and licence summary](https://github.com/introlab/rtabmap), accessed 2026-11-23
2. [RTAB-Map releases](https://github.com/introlab/rtabmap/releases), accessed 2026-11-23
3. [rtabmap_ros ros2 branch: README and LICENSE](https://github.com/introlab/rtabmap_ros/tree/ros2), accessed 2026-11-23
4. [rtabmap_slam README: frames, database, update rate, odometry, mapping and localization](https://github.com/introlab/rtabmap_ros/blob/ros2/rtabmap_slam/README.md), accessed 2026-11-23
5. [rtabmap node documentation: inputs, topics, services, parameters](https://github.com/introlab/rtabmap_ros/blob/ros2/rtabmap_slam/doc/rtabmap.md), accessed 2026-11-23
6. [rtabmap.launch.py, jazzy-devel branch](https://github.com/introlab/rtabmap_ros/blob/jazzy-devel/rtabmap_launch/launch/rtabmap.launch.py), accessed 2026-11-23
7. [rtabmap_examples lidar3d.launch.py, jazzy-devel branch](https://github.com/introlab/rtabmap_ros/blob/jazzy-devel/rtabmap_examples/launch/lidar3d.launch.py), accessed 2026-11-23
8. [RTAB-Map Parameters.h, jazzy-devel branch](https://github.com/introlab/rtabmap/blob/jazzy-devel/corelib/include/rtabmap/core/Parameters.h), accessed 2026-11-23
9. [RTAB-Map command-line tools (Export, DatabaseViewer, Recovery), jazzy-devel branch](https://github.com/introlab/rtabmap/tree/jazzy-devel/tools), accessed 2026-11-23
10. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-23
