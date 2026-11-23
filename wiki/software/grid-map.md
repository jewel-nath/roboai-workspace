---
type: tool
name: grid_map
summary: BSD-licensed C++ library from ETH Zurich and ANYbotics for multi-layer 2.5D grid maps (elevation, variance, traversability) with ROS 2 conversions, filters and an RViz plugin; binaries for Humble, Jazzy and Kilted, Lyrical pending, and maintenance now rests on community volunteers.
tags: [grid-map, elevation-map, traversability, 2.5d, rough-terrain, costmap, eigen, filters, rviz, anybotics, ros2]
kind: library
area: nav
support:
license: BSD-3-Clause
links: {repo: "https://github.com/ANYbotics/grid_map", docs: "https://github.com/ANYbotics/grid_map/blob/jazzy/README.md", site: }
version: {tested: , latest: 2.5.0, as_of: 2026-11-24}
platforms: [linux]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-24
sources:
  - {url: "https://github.com/ANYbotics/grid_map/tree/jazzy", title: "grid_map jazzy branch: README, LICENSE, package.xml files, grid_map_ros and grid_map_costmap_2d headers and sources", accessed: 2026-11-24}
  - {url: "https://github.com/ANYbotics/grid_map", title: "grid_map repository: branches, tags, rolling CHANGELOG, master history, issue tracker", accessed: 2026-11-24}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-24}
  - {url: "https://github.com/ANYbotics/grid_map/issues/544", title: "grid_map issue 544: Release grid_map for ROS 2 Lyrical", accessed: 2026-11-24}
  - {url: "https://github.com/ANYbotics/elevation_mapping", title: "ANYbotics elevation_mapping repository (archived)", accessed: 2026-11-24}
  - {url: "https://github.com/ros-navigation/navigation2/tree/jazzy/nav2_costmap_2d", title: "nav2_costmap_2d, jazzy branch: StaticLayer and Costmap2DROS parameters", accessed: 2026-11-24}
---

# grid_map

grid_map stores a 2.5D map as any number of float layers (elevation, variance, traversability)
on one grid, in Eigen matrices inside a circular buffer, so the map can follow the robot without
copying [1]. Legged and outdoor robots use it for height and traversability maps that Nav2's 2D
cost grid cannot hold. BSD-3-Clause, from ETH Zurich and ANYbotics; the README calls it research
code [1]. Releases: Humble 2.0.1, **Jazzy 2.2.2**, Kilted 2.4.0, **none yet for Lyrical or
Rolling** [3]. Not archived; newest tag 2.5.0 (2026-11-15), but see the maintenance trap [2].

## When to use it

- **Use it** for elevation or traversability maps from depth cameras or lidar, for rough-terrain
  and legged navigation, or for any per-cell float data to filter, view and convert [1].
- **Use something else** for 3D occupancy ([OctoMap](octomap.md); `grid_map_octomap` flattens it
  into a layer) [1], or [Nav2](nav2.md)'s own layers on a flat floor.

## Setup

```bash
sudo apt install ros-jazzy-grid-map          # the metapackage pulls in all the others
ros2 launch grid_map_demos simple_demo_launch.py
```

Packages: `grid_map_core` (Eigen only, no ROS), `grid_map_ros`, `grid_map_msgs`,
`grid_map_filters` (filter chains, math expressions, normals), `grid_map_rviz_plugin` (height
surfaces), `grid_map_visualization`, and converters for OpenCV, PCL, OctoMap and Nav2 [1][3].
Linux binaries only [3]; nothing needs CUDA [1]. Branches follow the distro; `master` is ROS 1 [2].

## How an agent works with it

In a C++ node, create `grid_map::GridMap map({"elevation"})`, then `setFrameId("odom")` and
`setGeometry(grid_map::Length(10.0, 10.0), 0.05)`; fill cells with the map, circle, polygon or
line iterators; publish `GridMapRosConverter::toMessage(map)` as `grid_map_msgs/GridMap` [1].
To reach Nav2, `toOccupancyGrid(map, layer, min, max, msg)` scales a layer to 0 to 100 (NaN
becomes -1) for a costmap `StaticLayer`'s `map_topic`; `grid_map_costmap_2d` copies between a
`nav2_costmap_2d::Costmap2D` and a layer, also cropped at the robot pose [1][6]. Check it in
RViz with the GridMap display, or republish layers with `grid_map_visualization` [1].

## Traps

- **No Lyrical binary.** The rosdistro release (PR 55503) was open on 2026-11-17; build the
  `lyrical` branch until it merges [4]. On Ubuntu 26.04, PCL plus `grid_map_ros` can fail at CMake
  on VTK's `JsonCpp::JsonCpp`: call `find_package(jsoncpp QUIET)` before `find_package(PCL)` [4].
- **Graded costs collapse to free.** Costmaps default to `trinary_costmap: true` and
  `lethal_cost_threshold: 100`, so every value below 100 reaches Nav2 as free space. Set
  `trinary_costmap: false` on that costmap [6]. No Nav2 layer plugin ships; an issue asks [2].
- **Thin maintenance.** ANYbotics archived elevation_mapping on 2026-11-16 [5], and on 2026-11-13
  replaced the named maintainers on ROS 1 `master` with a support address [2]. ROS 2 releases come
  from volunteers; an Autoware maintainer offered to take them on, with no reply yet [2]. Pin a
  version and expect to patch.
- **Stale README.** It says it was tested on Foxy, strikes out the apt install and links Kinetic
  API docs [1]; binaries do exist for Humble to Kilted [3]. Read the headers instead.

## Alternatives

[OctoMap](octomap.md) for 3D occupancy; [Nav2](nav2.md)'s own costmap layers for flat floors.

## Sources

1. [grid_map jazzy branch: README, LICENSE, package.xml files, grid_map_ros and grid_map_costmap_2d headers and sources](https://github.com/ANYbotics/grid_map/tree/jazzy), accessed 2026-11-24
2. [grid_map repository: branches, tags, rolling CHANGELOG, master history, issue tracker](https://github.com/ANYbotics/grid_map), accessed 2026-11-24
3. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-24
4. [grid_map issue 544: Release grid_map for ROS 2 Lyrical](https://github.com/ANYbotics/grid_map/issues/544), accessed 2026-11-24
5. [ANYbotics elevation_mapping repository (archived)](https://github.com/ANYbotics/elevation_mapping), accessed 2026-11-24
6. [nav2_costmap_2d, jazzy branch: StaticLayer and Costmap2DROS parameters](https://github.com/ros-navigation/navigation2/tree/jazzy/nav2_costmap_2d), accessed 2026-11-24
