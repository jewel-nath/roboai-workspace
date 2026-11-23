# Filtering scans and clouds with stock packages

Part of [perception-lidar](../SKILL.md): `laser_filters` for LaserScan, `pcl_ros` filter components for
PointCloud2, `pointcloud_to_laserscan` in both directions, and `point_cloud_transport` for bandwidth.
Checked against laser_filters 2.0.10, perception_pcl 2.6.5 (`jazzy`), pointcloud_to_laserscan 2.0.2
(`jazzy`) and point_cloud_transport 4.0.10 (`jazzy`) sources.

## 2D: laser_filters

`scan_to_scan_filter_chain` subscribes to `scan` (sensor-data QoS) and publishes `scan_filtered`
(reliable, depth 1000). Filters run in the order `filter1`, `filter2`, ... The YAML's top-level key
must equal the node's name.

`my_robot_bringup/config/scan_filters.yaml`:

```yaml
scan_filter:
  ros__parameters:
    filter1:
      name: range
      type: laser_filters/LaserScanRangeFilter
      params:
        use_message_range_limits: false
        lower_threshold: 0.15          # below this: hits on the robot or the window
        upper_threshold: 12.0
        lower_replacement_value: -.inf # REP 117: -inf too close, +inf no return
        upper_replacement_value: .inf
    filter2:
      name: body
      type: laser_filters/LaserScanBoxFilter
      params:
        box_frame: base_link           # needs TF from the scan frame
        min_x: -0.30
        max_x: 0.30
        min_y: -0.25
        max_y: 0.25
        min_z: -0.10
        max_z: 0.50
        invert: false                  # true keeps only the box
    filter3:
      name: speckle
      type: laser_filters/LaserScanSpeckleFilter
      params:
        filter_type: 0                 # 0: distance between neighbours, 1: radius outlier
        max_range: 2.0
        max_range_difference: 0.1
        filter_window: 2
```

```python
# In a launch file: from launch.substitutions import PathJoinSubstitution;
# from launch_ros.actions import Node; from launch_ros.substitutions import FindPackageShare
Node(package='laser_filters', executable='scan_to_scan_filter_chain', name='scan_filter',
     parameters=[PathJoinSubstitution([FindPackageShare('my_robot_bringup'), 'config',
                                       'scan_filters.yaml'])],
     remappings=[('scan', '/scan'), ('scan_filtered', '/scan_filtered')])
```

Other filter types (all `laser_filters/...`): `LaserScanAngularBoundsFilter` (keeps
`lower_angle`..`upper_angle` and shortens the scan), `LaserScanAngularBoundsFilterInPlace` (blanks
that sector, `replace_with_nan` optional), `ScanShadowsFilter` (veiling points at object edges:
`min_angle`, `max_angle`, `neighbors`, `window`), `LaserScanIntensityFilter`,
`LaserScanFootprintFilter` (`inscribed_radius`), `LaserScanPolygonFilter`, `LaserScanMaskFilter`,
`LaserScanMedianSpatialFilter`, `LaserArrayFilter`, `LaserScanBinningFilter`. Each has an example
YAML in the package's `examples/` folder; the speckle example there is still in ROS 1 list format,
so copy the `ros__parameters` layout above instead. `scan_to_cloud_filter_chain` runs a scan chain
(`scan_filter_chain`), projects to a cloud in `target_frame` (default `base_link`) and runs a cloud
chain (`cloud_filter_chain`), publishing `cloud_filtered`.

## 3D: pcl_ros filter components

The Jazzy `pcl_ros` builds only the filters and the PCD tools; the segmentation, feature and surface
nodelets of ROS 1 were not ported. Each filter is a component and an executable:

| Plugin | Executable | Parameters (besides the common ones) |
|---|---|---|
| `pcl_ros::CropBox` | `filter_crop_box_node` | `min_x..max_z` (default ±1 m), `negative`, `keep_organized` |
| `pcl_ros::PassThrough` | `filter_passthrough_node` | `filter_field_name`, `filter_limit_min/max`, `filter_limit_negative`, `keep_organized` |
| `pcl_ros::VoxelGrid` | `filter_voxel_grid_node` | `leaf_size` (0..1 m, default 0.01), `min_points_per_voxel` (default 2), the `filter_*` fields |
| `pcl_ros::StatisticalOutlierRemoval` | `filter_statistical_outlier_removal_node` | `mean_k` (default 2), `stddev` (default 0.0), `negative`, `keep_organized` |
| `pcl_ros::RadiusOutlierRemoval` | `filter_radius_outlier_removal_node` | `radius_search` (0.1), `min_neighbors` (5), `keep_organized` |
| `pcl_ros::ExtractIndices`, `pcl_ros::ProjectInliers` | `filter_extract_indices_node`, `filter_project_inliers_node` | need an `indices` / `model` input |

Common to all: topics `input` (sensor-data QoS) and `output` (reliable, depth `max_queue_size`, 3),
`input_frame` and `output_frame` (TF), `use_indices`, `approximate_sync`. Since 2.6.4 a filter
subscribes to `input` only while `output` has a subscriber.

Defaults that bite:

- **VoxelGrid also crops**: `filter_field_name` defaults to `z` with limits 0.0 to 1.0, so only points
  with 0 ≤ z ≤ 1 m survive. Set `filter_field_name: ''` to turn that off, or set real limits.
- VoxelGrid's `min_points_per_voxel` is 2, which deletes lone points: sparse far returns vanish.
- StatisticalOutlierRemoval's defaults (`mean_k` 2, `stddev` 0) remove a large share of any cloud.
  Start from `mean_k: 20`, `stddev: 1.0`.
- With `input_frame` set and `output_frame` empty, the result is transformed back to the original
  frame. Set both to keep the cloud in `base_link`.

`my_robot_perception/launch/cloud_filters.launch.py`, a crop to the robot's surroundings in
`base_footprint`, then a voxel grid, in one container so clouds pass by pointer:

```python
from launch import LaunchDescription
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode


def generate_launch_description():
    ipc = [{'use_intra_process_comms': True}]
    crop = ComposableNode(
        package='pcl_ros', plugin='pcl_ros::CropBox', name='crop',
        remappings=[('input', '/lidar/points'), ('output', '/lidar/points_cropped')],
        parameters=[{'input_frame': 'base_footprint', 'output_frame': 'base_footprint',
                     'min_x': -10.0, 'max_x': 10.0, 'min_y': -10.0, 'max_y': 10.0,
                     'min_z': -0.5, 'max_z': 2.0}],
        extra_arguments=ipc)
    voxel = ComposableNode(
        package='pcl_ros', plugin='pcl_ros::VoxelGrid', name='voxel',
        remappings=[('input', '/lidar/points_cropped'), ('output', '/lidar/points_filtered')],
        parameters=[{'leaf_size': 0.05, 'min_points_per_voxel': 1, 'filter_field_name': ''}],
        extra_arguments=ipc)
    return LaunchDescription([ComposableNodeContainer(
        name='lidar_filters', namespace='', package='rclcpp_components',
        executable='component_container', composable_node_descriptions=[crop, voxel],
        output='screen')])
```

CropBox keeps what is inside the box; to cut the robot's own body out, add a second CropBox with
the body's extent and `negative: true`.

## 3D to 2D and back: pointcloud_to_laserscan

`pointcloud_to_laserscan_node` slices a height band of a cloud into a LaserScan, for 2D SLAM or a 2D
costmap fed by a 3D lidar or a depth camera. It subscribes to `cloud_in` and publishes `scan`, both
with sensor-data (best-effort) QoS, and only subscribes while `scan` has a subscriber.

```python
Node(package='pointcloud_to_laserscan', executable='pointcloud_to_laserscan_node',
     name='cloud_to_scan',
     remappings=[('cloud_in', '/lidar/points'), ('scan', '/lidar/scan')],
     parameters=[{
         'target_frame': 'base_footprint',  # a level frame; empty keeps the cloud's frame
         'transform_tolerance': 0.01,
         'min_height': 0.10,                # always set: the default is the smallest positive double
         'max_height': 1.50,
         'angle_min': -3.14159, 'angle_max': 3.14159, 'angle_increment': 0.0087,
         'scan_time': 0.1,                  # the lidar's period
         'range_min': 0.3, 'range_max': 30.0,
         'use_inf': True, 'inf_epsilon': 1.0,
     }])
```

- `min_height` defaults to `std::numeric_limits<double>::min()`, about 2e-308, not minus infinity:
  every point at or below z = 0 is dropped. Set it.
- Heights are measured in `target_frame`. With the lidar's own frame on a tilted mount the slice is
  tilted too; use a frame parallel to the floor.
- `queue_size` defaults to the CPU's thread count.

`laserscan_to_pointcloud_node` does the reverse (`scan_in` to `cloud`, `target_frame`,
`transform_tolerance`). Inside a Python node, project a scan with `laser_geometry`:

```python
from laser_geometry import LaserProjection

cloud = LaserProjection().projectLaser(scan_msg)   # PointCloud2 in the scan's frame
```

The C++ class `laser_geometry::LaserProjection` also has `transformLaserScanToPointCloud`, which
uses TF and corrects for motion during the sweep.

## Bandwidth: point_cloud_transport

A 3D lidar cloud over Wi-Fi or between machines can saturate the link. Compress it on the robot and
decompress where it is used:

```bash
sudo apt install ros-jazzy-point-cloud-transport ros-jazzy-point-cloud-transport-plugins
ros2 run point_cloud_transport republish --ros-args -p in_transport:=raw -p out_transport:=draco \
  --remap in:=/lidar/points --remap out:=/lidar/points_compressed
```

The plugins are `draco` (lossy, quantised), `zlib` and `zstd`. The plugin adds its name to the
output topic (the node logs the full name, here `/lidar/points_compressed/draco`). On the receiving
machine, republish with `-p in_transport:=draco -p out_transport:=raw`, remapping `in` to the base
name `/lidar/points_compressed`. Draco's quantisation moves points slightly; process the raw cloud
on the robot and compress only for viewing or logging.
