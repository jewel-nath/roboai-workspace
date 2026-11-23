---
type: tool
name: PCL (Point Cloud Library)
summary: The BSD-licensed C++ library for point-cloud filtering, segmentation, features and registration; ROS 2 reaches it through pcl_conversions and pcl_ros, released from Humble to Lyrical, though pcl_ros ports only its filter nodes.
tags: [pcl, point-cloud-library, point-cloud, lidar, depth-camera, pointcloud2, voxel-grid, outlier-removal, ransac, segmentation, icp, ndt, perception-pcl, pcl-ros, pcl-conversions]
kind: library
area: perception
support:
license: BSD-3-Clause
links: {repo: "https://github.com/PointCloudLibrary/pcl", docs: "https://pcl.readthedocs.io/projects/tutorials/en/master/", site: "https://pointclouds.org"}
version: {tested: , latest: 1.15.1, as_of: 2026-11-23}
platforms: [linux, windows, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/PointCloudLibrary/pcl", title: "PCL repository: README, LICENSE.txt, CHANGES.md, CMake options, common/memory.h, conversions.h (master)", accessed: 2026-11-23}
  - {url: "https://pointclouds.org/downloads/", title: "PCL downloads", accessed: 2026-11-23}
  - {url: "https://pcl.readthedocs.io/projects/tutorials/en/master/", title: "PCL tutorials", accessed: 2026-11-23}
  - {url: "https://pcl.readthedocs.io/projects/tutorials/en/master/adding_custom_ptype.html", title: "PCL tutorial: Adding your own custom PointT type", accessed: 2026-11-23}
  - {url: "https://github.com/PointCloudLibrary/pcl/pulls?q=is%3Apr+is%3Amerged", title: "PCL merged pull requests", accessed: 2026-11-23}
  - {url: "https://github.com/ros-perception/perception_pcl", title: "perception_pcl repository: README, package.xml, CMakeLists and changelogs (jazzy and ros2 branches)", accessed: 2026-11-23}
  - {url: "https://github.com/ros-perception/perception_pcl/blob/jazzy/pcl_ros/src/pcl_ros/filters/filter.cpp", title: "pcl_ros filter base class source, jazzy branch", accessed: 2026-11-23}
  - {url: "https://github.com/ros-perception/perception_pcl/blob/jazzy/pcl_ros/src/pcl_ros/filters/voxel_grid.cpp", title: "pcl_ros VoxelGrid source, jazzy branch", accessed: 2026-11-23}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro: distribution files (humble, jazzy, kilted, lyrical, rolling) and rosdep/base.yaml", accessed: 2026-11-23}
  - {url: "https://packages.ubuntu.com/search?keywords=libpcl-dev&searchon=names&suite=all&section=all", title: "Ubuntu packages: libpcl-dev and pcl-tools", accessed: 2026-11-23}
  - {url: "https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html", title: "ROS 2 docs (Jazzy): Quality of Service settings", accessed: 2026-11-23}
  - {url: "https://bugs.launchpad.net/ubuntu/+source/pcl/+bug/1771124", title: "Launchpad bug 1771124: libpcl cflags -march=native make user programs crash", accessed: 2026-11-23}
  - {url: "https://github.com/strawlab/python-pcl", title: "python-pcl repository (archived)", accessed: 2026-11-23}
---

# PCL (Point Cloud Library)

PCL is a large C++ library for 2D and 3D point clouds: filters, segmentation, features,
keypoints, registration, surface reconstruction, k-d tree and octree search, and a VTK viewer,
under BSD-3-Clause [1]. Builders use it inside C++ ROS 2 nodes to crop, downsample and clean lidar
or depth-camera clouds, find the floor or a table plane, cluster objects and align scans. ROS 2
reaches it through `perception_pcl`: `pcl_conversions` converts messages and `pcl_ros` ships
ready filter nodes [6].

## When to use it

- **C++ perception nodes on ROS 2.** Binaries exist from Humble to Lyrical [9], and rosdistro
  lists many packages built on PCL, such as `grid_map_pcl` [9].
- **Standard cleanup without code:** `pcl_ros` runs VoxelGrid, PassThrough, CropBox,
  StatisticalOutlierRemoval, RadiusOutlierRemoval, ExtractIndices and ProjectInliers as
  components [6].
- **Use [Open3D](open3d.md) instead** for Python, notebooks, RGB-D reconstruction or GPU ICP from
  a pip wheel. PCL has no maintained Python binding: python-pcl was archived in December 2023 [13].
- **Use a finished system** rather than PCL building blocks for lidar odometry
  ([KISS-ICP](kiss-icp.md), [LIO-SAM](lio-sam.md)), 3D occupancy ([OctoMap](octomap.md)) or
  inspecting a map by hand ([CloudCompare](../tools/cloudcompare.md)).

## Versions and maintenance

Releases came about twice a year: 1.13.0 (December 2022) to 1.14.1 (May 2024), 1.15.0 (February
2025, C++17 by default) and **1.15.1** (26 August 2025, nanoflann search, CUDA 13) [1]. None since,
but `master` is active: last commit 14 November 2026, pull requests merged most weeks [1][5].

**What ROS 2 uses.** Binary ROS packages depend on the rosdep key `libpcl-all-dev`, which maps to
Ubuntu's `libpcl-dev` [9]: 1.12.1 on 22.04, **1.14.0 on 24.04** (Jazzy, Kilted), 1.15.1 on
26.04 (Lyrical) [10]. `perception_pcl` is the official ROS package, from the ros-perception
organisation; both active branches got commits in November 2026 [6]:

| Distro | Branch | Release [9] | apt |
|---|---|---|---|
| Humble | `humble` | 2.4.5 | `ros-humble-pcl-ros` |
| **Jazzy** | `jazzy` | **2.6.5** (July 2026) [6] | `ros-jazzy-pcl-ros`, `ros-jazzy-pcl-conversions` |
| Kilted, Lyrical, Rolling | `ros2` | 2.10.0 (July 2026) [6] | `ros-lyrical-pcl-ros` |

## Setup

Ubuntu 24.04 with Jazzy:

```bash
sudo apt install ros-jazzy-pcl-ros ros-jazzy-pcl-conversions  # brings libpcl-dev 1.14.0
sudo apt install pcl-tools          # pcl_viewer and the pcl_* command-line converters
```

Without ROS: `sudo apt install libpcl-dev`, `brew install pcl` on macOS, `vcpkg install pcl` on
Windows [2]. A source build needs C++17 and CMake 3.16.3 or newer, with Eigen, Boost, FLANN and
VTK (for the viewer); CUDA and GPU modules are optional (`WITH_CUDA`) [1]. In an ament package,
declare `<depend>libpcl-all-dev</depend>` and `<depend>pcl_conversions</depend>`, then:

```cmake
find_package(PCL REQUIRED COMPONENTS common filters segmentation)
find_package(pcl_conversions REQUIRED)
target_include_directories(my_node PRIVATE ${PCL_INCLUDE_DIRS})
target_link_libraries(my_node ${PCL_LIBRARIES})
ament_target_dependencies(my_node rclcpp sensor_msgs pcl_conversions)
```

## How an agent works with it

The lidar procedures are in [perception-lidar](../../skills/perception-lidar/SKILL.md).

**pcl_ros filter nodes.** Each filter is a component with an executable `filter_<name>_node`
[6]. It subscribes to `input` (`sensor_msgs/msg/PointCloud2`, sensor-data QoS) and publishes
`output`; `input_frame` and `output_frame` transform through tf2, and `max_queue_size` (3),
`use_indices` and `approximate_sync` are read-only [7]. Key parameters: VoxelGrid `leaf_size`
(0.01 m, at most 1.0) and `min_points_per_voxel` (2) [8]; StatisticalOutlierRemoval `mean_k`
and `stddev`; CropBox `min_x` to `max_z`, `negative`, `keep_organized` [6].

```yaml
/**:            # voxel.yaml
  ros__parameters:
    leaf_size: 0.05
    filter_field_name: ""   # process the whole cloud (see Traps)
```

```bash
ros2 run pcl_ros filter_voxel_grid_node --ros-args --params-file voxel.yaml \
  -r input:=/lidar/points -r output:=/lidar/points_ds
ros2 topic hz /lidar/points_ds                      # also wakes the lazy subscriber
ros2 run pcl_ros pointcloud_to_pcd --ros-args -r input:=/lidar/points_ds -p prefix:=scan_
ros2 run pcl_ros pcd_to_pointcloud --ros-args -p file_name:=map.pcd -p tf_frame:=map
```

`pointcloud_to_pcd` also takes `fixed_frame` and `binary`; `pcd_to_pointcloud` publishes the file
on `cloud_pcd` every `publishing_period_ms` (3000) [6]. View saved files with `pcl_viewer`.

**Writing a node.** Convert with `pcl::fromROSMsg(*msg, cloud)` and `pcl::toROSMsg(cloud, out)`
from `pcl_conversions/pcl_conversions.h`, then copy the input header so `frame_id` and the stamp
survive [6]. The usual chain, each step a PCL tutorial [3]: PassThrough or CropBox to the region
of interest, VoxelGrid, StatisticalOutlierRemoval, `SACSegmentation` with `SACMODEL_PLANE` and
RANSAC plus `ExtractIndices` to drop the floor, then `EuclideanClusterExtraction` on a k-d tree
for objects. Registration offers ICP, GICP and NDT [3]; check `hasConverged()` and
`getFitnessScore()` before trusting a transform.

**Checks.** The output topic runs near the input rate (`ros2 topic hz`); point counts drop as
expected after each filter; a saved PCD opens in `pcl_viewer` or CloudCompare in the right frame.

## Traps

- **VoxelGrid and PassThrough keep only z from 0 to 1 m by default.** pcl_ros declares
  `filter_field_name: z` with limits 0.0 and 1.0 and applies them at start [7][8], so most of a
  lidar cloud vanishes. Set `filter_field_name` to an empty string to keep everything; PCL skips
  the limit test when the name is empty [1]. CropBox defaults to a box of ±1 m [6].
- **Filter nodes sleep until someone listens.** pcl_ros subscribes to `input` only while
  `output` has a subscriber [7]; with no consumer it does nothing, and `ros2 topic hz` wakes it.
- **QoS mismatch on sensor topics.** Drivers often publish best effort; a reliable subscription
  never connects [11]. Use `rclcpp::SensorDataQoS()`, as pcl_ros does [7]; check `topic info -v`.
- **Only the filters were ported.** pcl_ros features, segmentation (SAC, Euclidean clusters) and
  surface nodes are still commented out of the ROS 2 build [6]; write a node with the PCL classes.
- **Eigen alignment crashes.** A source build of PCL defaults to `-march=native` and SSE/AVX on
  x86 Linux [1]; code built with other flags against it, or beside the apt PCL, can crash in
  Eigen's aligned free. PCL 1.15 warns "Potential runtime error due to aligned malloc mismatch"
  [1]; Ubuntu once shipped the bug itself [12]. With ROS binaries use apt `libpcl-dev`; otherwise
  build PCL and all its users with the same flags (`PCL_ENABLE_MARCHNATIVE=OFF`) [1].
- **Custom lidar point types build slowly.** Fields such as `ring` and `time` need a registered
  struct with `EIGEN_ALIGN16`, `PCL_MAKE_ALIGNED_OPERATOR_NEW` and `#define PCL_NO_PRECOMPILE`
  before any PCL include [4], so every algorithm compiles in your node. For a source build of
  PCL, `PCL_ONLY_CORE_POINT_TYPES` cuts compile time [1].
- **"Failed to find exact match for field".** `fromROSMsg` into a point type with fields the
  message lacks warns and leaves them unset [1]; use `PointXYZI` when the driver sends intensity.
- **NaN points.** Organized clouds from depth cameras keep invalid points as NaN and set
  `is_dense` false [3]; remove them (`pcl::removeNaNFromPointCloud`) before k-d tree steps.

## Alternatives

[Open3D](open3d.md) (Python, MIT, GPU tensor API); [CloudCompare](../tools/cloudcompare.md) (GUI);
[OctoMap](octomap.md), [RTAB-Map](rtab-map.md) and [GTSAM](gtsam.md) for maps and pose graphs.
NVIDIA's cuda-pcl and Isaac ROS accelerate some of this on Jetson (not reviewed here).

## Sources

1. [PCL repository: README, LICENSE.txt, CHANGES.md, CMake options, common/memory.h, conversions.h (master)](https://github.com/PointCloudLibrary/pcl), accessed 2026-11-23
2. [PCL downloads](https://pointclouds.org/downloads/), accessed 2026-11-23
3. [PCL tutorials](https://pcl.readthedocs.io/projects/tutorials/en/master/), accessed 2026-11-23
4. [PCL tutorial: Adding your own custom PointT type](https://pcl.readthedocs.io/projects/tutorials/en/master/adding_custom_ptype.html), accessed 2026-11-23
5. [PCL merged pull requests](https://github.com/PointCloudLibrary/pcl/pulls?q=is%3Apr+is%3Amerged), accessed 2026-11-23
6. [perception_pcl repository: README, package.xml, CMakeLists and changelogs (jazzy and ros2 branches)](https://github.com/ros-perception/perception_pcl), accessed 2026-11-23
7. [pcl_ros filter base class source, jazzy branch](https://github.com/ros-perception/perception_pcl/blob/jazzy/pcl_ros/src/pcl_ros/filters/filter.cpp), accessed 2026-11-23
8. [pcl_ros VoxelGrid source, jazzy branch](https://github.com/ros-perception/perception_pcl/blob/jazzy/pcl_ros/src/pcl_ros/filters/voxel_grid.cpp), accessed 2026-11-23
9. [rosdistro: distribution files (humble, jazzy, kilted, lyrical, rolling) and rosdep/base.yaml](https://github.com/ros/rosdistro), accessed 2026-11-23
10. [Ubuntu packages: libpcl-dev and pcl-tools](https://packages.ubuntu.com/search?keywords=libpcl-dev&searchon=names&suite=all&section=all), accessed 2026-11-23
11. [ROS 2 docs (Jazzy): Quality of Service settings](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html), accessed 2026-11-23
12. [Launchpad bug 1771124: libpcl cflags -march=native make user programs crash](https://bugs.launchpad.net/ubuntu/+source/pcl/+bug/1771124), accessed 2026-11-23
13. [python-pcl repository (archived)](https://github.com/strawlab/python-pcl), accessed 2026-11-23
