---
type: tool
name: SLAM Toolbox
summary: 2D lidar SLAM and localization for ROS 2, the package Nav2's docs recommend; maps from a LaserScan plus odometry, saves lossless pose graphs, and can keep refining or localizing in them.
tags: [slam, 2d-lidar, mapping, localization, nav2, occupancy-grid, karto, pose-graph, ceres, lifelong-mapping, ros2]
kind: library
area: perception
support:
license: LGPL-2.1-only AND LGPL-3.0-or-later
links: {repo: "https://github.com/SteveMacenski/slam_toolbox", docs: "https://github.com/SteveMacenski/slam_toolbox/blob/jazzy/README.md", site: }
version: {tested: , latest: 2.10.0, as_of: 2026-11-23}
platforms: [linux]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/SteveMacenski/slam_toolbox/tree/jazzy", title: "slam_toolbox jazzy branch: README, LICENSE, package.xml, config, launch and source files", accessed: 2026-11-23}
  - {url: "https://github.com/SteveMacenski/slam_toolbox", title: "slam_toolbox repository: branches, release tags, ros2 branch package.xml", accessed: 2026-11-23}
  - {url: "https://docs.nav2.org/tutorials/docs/navigation2_with_slam.html", title: "Nav2 docs: (SLAM) Navigating While Mapping", accessed: 2026-11-23}
  - {url: "https://docs.nav2.org/setup_guides/sensors/mapping_localization.html", title: "Nav2 docs: Mapping and Localization", accessed: 2026-11-23}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-23}
  - {url: "https://www.ros.org/reps/rep-0105.html", title: "REP 105: Coordinate frames for mobile platforms", accessed: 2026-11-23}
  - {url: "https://github.com/SteveMacenski/slam_toolbox/issues", title: slam_toolbox issue tracker, accessed: 2026-11-23}
---

# SLAM Toolbox

SLAM Toolbox builds a 2D occupancy-grid map from a planar lidar (`sensor_msgs/LaserScan`) and the
robot's odometry, using Karto's scan matcher and a Ceres pose-graph solver [1]. It can save the
pose graph losslessly, continue mapping it later, or localize in it. Nav2 recommends it when a
robot needs SLAM and uses it in its tutorial [3][4]. Steve Macenski maintains it: both the `jazzy`
and `ros2` branches had commits on 2026-11-02, and 32 issues were open [1][2][7].

## When to use it

- **Use it** for an indoor wheeled robot with a 2D lidar and wheel odometry that will run Nav2.
  Async mode suits a live robot (it never falls behind); sync mode processes every scan, for bags
  or when no scan may be skipped [1].
- **Localization:** its pose-graph localization mode can replace AMCL, but the README warns it
  needs tuning and high-quality odometry, and suggests AMCL (`nav2_amcl`) for most beginners [1].
- **Use something else** for 3D maps, cameras or uneven ground: [RTAB-Map](rtab-map.md) for
  RGB-D, stereo and 3D lidar, [KISS-ICP](kiss-icp.md) or [LIO-SAM](lio-sam.md) for 3D lidar
  odometry. [Cartographer](cartographer.md) also does 2D but is barely maintained. See
  [Choose a SLAM system](../guides/choose-a-slam-system.md).

## Setup

Released for Humble (2.6.10), Jazzy (2.8.5), Kilted (2.9.0) and Lyrical (2.10.0); Rolling has no
release [5]. The newest tag is 2.10.0, the `ros2` branch's version [2]. On Ubuntu 24.04:

```bash
sudo apt install ros-jazzy-slam-toolbox ros-jazzy-nav2-map-server
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=false \
  slam_params_file:=$HOME/robot_ws/config/slam.yaml
```

Start the params file from a copy of `config/mapper_params_online_async.yaml` [1]. Source branches
are named after the distro (`jazzy`, `kilted`, `lyrical`, `humble`); `ros2` is development [2].
Binaries exist only for Linux [5]. It runs on the CPU; the author reports mapping about 30,000 sq
ft at over 5x real time, and benchmarked the solver on a low-power 7th-gen i7 [1].
The README recommends the `slam-toolbox` snap for production robots, claiming about 10x speed
from build tweaks; the RViz plugin needs the apt or source install [1].

## How an agent works with it

**Launch files and modes** (all in `slam_toolbox/launch`, each with a matching config) [1]:

| Launch file | Node | Use |
|---|---|---|
| `online_async_launch.py` | `async_slam_toolbox_node` | Live mapping; keeps only the newest scan |
| `online_sync_launch.py` | `sync_slam_toolbox_node` | Live mapping that queues and processes every scan |
| `offline_launch.py` | `sync_slam_toolbox_node` | Mapping from a recorded bag |
| `localization_launch.py` | `localization_slam_toolbox_node` | Localize in a serialized pose graph |
| `lifelong_launch.py` | `lifelong_slam_toolbox_node` | Continue a saved map and prune old scans |
| `merge_maps_kinematic_launch.py` | `merge_maps_kinematic` | Line up saved submaps in RViz and merge them |

The nodes are lifecycle nodes; the launch files configure and activate them (`autostart:=true`),
or hand that to Nav2's lifecycle manager with `use_lifecycle_manager:=true` [1].

**Inputs and outputs** [1][6]:

- In: `/scan` (`LaserScan`, subscribed with the sensor-data QoS, so best-effort drivers work), and
  TF from `odom_frame` to `base_frame` (odometry) and from `base_frame` to the laser (URDF).
- Out: TF `map → odom` every `transform_publish_period` (0.02 s); `/map` (`OccupancyGrid`,
  reliable and transient-local) every `map_update_interval` (5 s); `/pose` with covariance.
- This is the REP 105 chain: odometry owns `odom → base_link`, SLAM owns `map → odom` [6].

**Parameters builders change** (defaults from the shipped async config) [1]:

| Parameter | Default | Change it when |
|---|---|---|
| `base_frame`, `odom_frame`, `map_frame` | `base_footprint`, `odom`, `map` | Your URDF names differ |
| `scan_topic` | `/scan` | The lidar publishes elsewhere (absolute name) |
| `resolution` | 0.05 m | You want a coarser or finer grid |
| `max_laser_range` | 20.0 m | Your lidar's usable range is shorter |
| `minimum_travel_distance`, `minimum_travel_heading` | 0.5 m, 0.5 rad | Too few or too many scans enter the graph |
| `map_update_interval` | 5.0 s | You want `/map` refreshed faster |
| `do_loop_closing`, `loop_search_maximum_distance` | true, 3.0 m | Loops are missed or false loops snap the map |
| `ceres_loss_function` | `None` | Wheels slip: try `HuberLoss` |
| `mode`, `map_file_name`, `map_start_pose` | `mapping`, unset | Start from a saved graph |
| `enable_interactive_mode` | true | RAM is tight (it caches every scan) |

**Saving maps.** There are two kinds, and they are not interchangeable [1]:

```bash
# Lossless pose graph: writes office.posegraph and office.data, reloadable for more mapping
ros2 service call /slam_toolbox/serialize_map slam_toolbox/srv/SerializePoseGraph \
  "{filename: '/home/robot/maps/office'}"
# Image plus YAML for AMCL or display, through Nav2's map saver
ros2 run nav2_map_server map_saver_cli -f ~/maps/office
```

`/slam_toolbox/save_map` does the second through the same `map_saver_cli` [1]. To localize, set
`mode: localization`, `map_file_name` to the serialized path without extension, and
`map_start_pose`, or give a pose with RViz's 2D Pose Estimate (`/initialpose`) [1].

**Checking it works:** the log prints "Registering sensor" once scans and TF line up [4];
`ros2 run tf2_ros tf2_echo map odom` shows the correction; `ros2 topic echo /map --once` (or an
RViz Map display) shows the grid growing as the robot drives [3]. The [tf2](tf2.md) page covers
TF debugging; [skills/perception-slam/SKILL.md](../../skills/perception-slam/SKILL.md) covers the
mapping workflow. The [TurtleBot3](../robots/turtlebot3.md) is Nav2's test robot for this [3].

## Traps

- **`use_sim_time` defaults to true** in the online, localization and lifelong launch files [1].
  On a real robot there is no `/clock`, so the node's clock stays at zero; pass
  `use_sim_time:=false`.
- **No map, TF errors about `base_footprint`.** The shipped configs use `base_frame:
  base_footprint`; a URDF with only `base_link` needs the parameter changed [1].
- **Nav2's source-build line fails on Jazzy.** It clones `-b $ROS_DISTRO-devel` [3], but the
  branches are `jazzy`, `humble` and so on, with no `-devel` suffix [2].
- **`save_map` needs Nav2's map saver.** It shells out to `ros2 run nav2_map_server
  map_saver_cli`, which slam_toolbox does not declare as a dependency; install
  `ros-jazzy-nav2-map-server` [1].
- **Localization cannot load a `.pgm`.** It needs a serialized `.posegraph` and `.data` pair;
  save one with `serialize_map` while mapping [1].
- **Smeared or doubled walls.** Usually bad odometry or a wrong laser transform, not SLAM
  parameters. Check the laser frame in TF first, then try `HuberLoss` for wheel slip [1].
- **Memory grows on long runs.** Interactive mode keeps every scan for RViz editing; turn it off
  on small computers [1].
- **Lifelong mode is not for the robot yet.** Its node removal is "highly" experimental, and the
  README advises running lifelong mapping in the cloud for its compute cost. It suggests building
  the full map with continued mapping, then switching to localization [1].
- **Licence.** The repo's `LICENSE` is LGPL 2.1, the bundled Karto SDK is LGPL 3 or later, and the
  node sources carry a Creative Commons licence notice that names no specific licence [1]. LGPL
  requires sharing changes to the library itself; have someone check before shipping a modified
  copy in a closed product.

## Alternatives

- [RTAB-Map](rtab-map.md): 2D or 3D, cameras and lidar, multi-session databases.
- [Cartographer](cartographer.md): 2D and 3D, but no new development.
- AMCL (`nav2_amcl`, part of Nav2): localization only, in a saved image map.
- 3D lidar: [KISS-ICP](kiss-icp.md), [LIO-SAM](lio-sam.md); see
  [Choose a SLAM system](../guides/choose-a-slam-system.md).

## Sources

1. [slam_toolbox jazzy branch: README, LICENSE, package.xml, config, launch and source files](https://github.com/SteveMacenski/slam_toolbox/tree/jazzy), accessed 2026-11-23
2. [slam_toolbox repository: branches, release tags, ros2 branch package.xml](https://github.com/SteveMacenski/slam_toolbox), accessed 2026-11-23
3. [Nav2 docs: (SLAM) Navigating While Mapping](https://docs.nav2.org/tutorials/docs/navigation2_with_slam.html), accessed 2026-11-23
4. [Nav2 docs: Mapping and Localization](https://docs.nav2.org/setup_guides/sensors/mapping_localization.html), accessed 2026-11-23
5. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-23
6. [REP 105: Coordinate frames for mobile platforms](https://www.ros.org/reps/rep-0105.html), accessed 2026-11-23
7. [slam_toolbox issue tracker](https://github.com/SteveMacenski/slam_toolbox/issues), accessed 2026-11-23
