---
type: tool
name: OctoMap
summary: BSD-licensed probabilistic 3D occupancy map in an octree, the map MoveIt 2 uses for 3D obstacles; octomap_server turns PointCloud2 into maps on ROS 2, released for Humble to Lyrical from the ros2 branch.
tags: [octomap, octree, occupancy-map, 3d-mapping, octomap-server, octomap-msgs, octomap-rviz-plugins, octovis, moveit, collision, pointcloud2]
kind: library
area: perception
support:
license: BSD-3-Clause
links: {repo: "https://github.com/OctoMap/octomap", docs: "https://octomap.github.io/octomap/doc/", site: "https://octomap.github.io"}
version: {tested: , latest: 2.0.0, as_of: 2026-11-23}
platforms: [linux, windows]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/OctoMap/octomap", title: "OctoMap repository: README, LICENSE files, CHANGELOG, CMake config, OcTreeBaseImpl (devel, v1.10.1 and v2.0.0 tags)", accessed: 2026-11-23}
  - {url: "https://octomap.github.io", title: "OctoMap project site and paper reference", accessed: 2026-11-23}
  - {url: "https://github.com/OctoMap/octomap_mapping", title: "octomap_mapping repository: README, octomap_server source, launch file, changelog (ros2 branch)", accessed: 2026-11-23}
  - {url: "https://github.com/OctoMap/octomap_rviz_plugins", title: "octomap_rviz_plugins repository (ros2 branch)", accessed: 2026-11-23}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-23}
  - {url: "https://packages.ubuntu.com/search?keywords=liboctomap-dev&searchon=names&suite=all&section=all", title: "Ubuntu packages: liboctomap-dev", accessed: 2026-11-23}
  - {url: "https://moveit.picknik.ai/main/doc/examples/perception_pipeline/perception_pipeline_tutorial.html", title: "MoveIt 2 docs: Perception pipeline tutorial", accessed: 2026-11-23}
---

# OctoMap

OctoMap keeps a 3D occupancy map in an octree: each cell holds an occupancy probability updated
along sensor rays, so free, occupied and unknown space stay distinct [2]. Builders use it as the 3D
obstacle map for arms and drones (MoveIt 2 builds its occupancy map with it [7]) and to save 3D
maps. Library BSD-3-Clause, octovis viewer GPL-2.0 [1]; paper: Hornung et al., 2013 [2].

## When to use it

For 3D collision maps from depth cameras or 3D lidar once poses are in TF. It does not estimate
poses: feed it from [RTAB-Map](rtab-map.md), [Cartographer](cartographer.md) or
[LIO-SAM](lio-sam.md). 2D floor maps: [SLAM Toolbox](slam-toolbox.md); meshes: [Open3D](open3d.md).

## Setup

`sudo apt install ros-jazzy-octomap-server ros-jazzy-octomap-rviz-plugins`. Releases [5]: the
`octomap` library 1.9.8 (Humble) and 1.10.0 (Jazzy); Kilted and Lyrical use Ubuntu's
`liboctomap-dev` (1.9.7 on 24.04, 1.10.0 on 26.04 [6]). `octomap_server` 2.3.1 and `octomap_msgs`
2.0.1 cover Humble to Lyrical; `octomap_rviz_plugins` is 2.1.0 on Jazzy, 2.2.0 on Lyrical. The ROS
2 code is on each repo's `ros2` branch [3]. Maintained: library 2.0.0 tagged 22 November 2026 [1],
server commits in November 2026 [3], RViz plugins 2.2.0 in February 2026 [4].

## How an agent works with it

```bash
ros2 run octomap_server octomap_server_node --ros-args -p resolution:=0.05 \
  -p frame_id:=map -p sensor_model.max_range:=5.0 -r cloud_in:=/camera/depth/points
ros2 run octomap_server octomap_saver_node --ros-args -p octomap_path:=room.bt  # .ot: -p full:=true
```

The server reads `cloud_in` (sensor-data QoS) into `frame_id` (default `map`) through tf2 and
publishes, latched: `octomap_binary`, `octomap_full`, `occupied_cells_vis_array` and a 2D
`projected_map`; services `~/clear_bbox` and `~/reset`. Defaults: hit 0.7, miss 0.4, clamping
0.12 to 0.97, unlimited range [3]. View with the RViz display `octomap_rviz_plugins/OccupancyGrid`
[4]; MoveIt 2 reads clouds through `occupancy_map_monitor/PointCloudOctomapUpdater` [7]. Check:
cells appear where the sensor looks, and a saved `.bt` reloads through `-p octomap_path:=` [3].

## Traps

- **Clouds dropped silently:** each waits 5 s in a tf2 filter for its frame to `frame_id` [3].
  Check `tf2_echo`; the shipped launch file uses `odom_combined` and a PR2 topic, so edit it [3].
- **Slow inserts, bounded size:** every point casts a ray; downsample ([PCL](pcl.md)) and set
  `max_range` [3]. Keys are 16 bits, ±32768 cells from the origin: ±1.6 km at 5 cm [1].
- **Two OctoMaps on Jazzy:** `ros-jazzy-octomap` is 1.10.0, but since 2.3.0 the server links
  Ubuntu's 1.9.7 [3][5][6]; know which one `find_package(octomap)` finds in your own code.
- **2.0.0 breaks CMake users:** `OCTOMAP_INCLUDE_DIRS` is gone; link `octomap::octomap` [1]. No
  ROS distro or Ubuntu release ships 2.0 yet [5][6].
- **GPL viewer:** `octovis` (`ros-jazzy-octovis`) is GPL-2.0 and links libQGLViewer [1]; keep it
  out of closed products. The library itself is BSD.

## Alternatives

Voxblox, UFOMap, Bonxai and NVIDIA's nvblox fill the same role (not reviewed here); SLAM choices:
[Choose a SLAM system](../guides/choose-a-slam-system.md).

## Sources

1. [OctoMap repository: README, LICENSE files, CHANGELOG, CMake config, OcTreeBaseImpl (devel, v1.10.1 and v2.0.0 tags)](https://github.com/OctoMap/octomap), accessed 2026-11-23
2. [OctoMap project site and paper reference](https://octomap.github.io), accessed 2026-11-23
3. [octomap_mapping repository: README, octomap_server source, launch file, changelog (ros2 branch)](https://github.com/OctoMap/octomap_mapping), accessed 2026-11-23
4. [octomap_rviz_plugins repository (ros2 branch)](https://github.com/OctoMap/octomap_rviz_plugins), accessed 2026-11-23
5. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-23
6. [Ubuntu packages: liboctomap-dev](https://packages.ubuntu.com/search?keywords=liboctomap-dev&searchon=names&suite=all&section=all), accessed 2026-11-23
7. [MoveIt 2 docs: Perception pipeline tutorial](https://moveit.picknik.ai/main/doc/examples/perception_pipeline/perception_pipeline_tutorial.html), accessed 2026-11-23
