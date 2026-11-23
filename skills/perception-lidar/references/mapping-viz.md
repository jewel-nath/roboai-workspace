# Maps from clouds, PCD files, and looking at the data

Part of [perception-lidar](../SKILL.md): build an OctoMap and a 2D occupancy grid from clouds when a
pose source already exists, move clouds in and out of PCD files, and inspect them in RViz,
Foxglove and CloudCompare. Checked against octomap_server 2.3.1 (`ros2`), pcl_ros 2.6.5 tools
(`jazzy`) and the rviz `jazzy` sources.

## OctoMap from clouds: octomap_server

`octomap_server` integrates each cloud into a probabilistic 3D occupancy octree. It does **not**
estimate the pose: it looks up `frame_id` → cloud frame in TF at each cloud's stamp, so odometry or
SLAM must already publish that chain ([perception-slam](../../perception-slam/SKILL.md)). Install
`ros-jazzy-octomap-server` and, for RViz, `ros-jazzy-octomap-rviz-plugins`.

```python
Node(package='octomap_server', executable='octomap_server_node', name='octomap_server',
     remappings=[('cloud_in', '/lidar/points_filtered')],
     parameters=[{
         'frame_id': 'map',                 # fixed frame the map is built in (default map)
         'base_frame_id': 'base_footprint', # used by filter_ground_plane
         'resolution': 0.05,                # leaf size in m (default 0.05)
         'sensor_model.max_range': 15.0,    # -1 (default) inserts every point
         'sensor_model.hit': 0.7, 'sensor_model.miss': 0.4,
         'sensor_model.min': 0.12, 'sensor_model.max': 0.97,
         'point_cloud_min_z': -0.5,         # points kept for insertion, in frame_id
         'point_cloud_max_z': 2.0,
         'occupancy_min_z': 0.1,            # height band projected into projected_map
         'occupancy_max_z': 1.5,
         'filter_ground_plane': False,
         'latch': True,                     # transient-local outputs, published once ready
     }])
```

Outputs (transient local when `latch` is true): `octomap_binary` and `octomap_full`
(`octomap_msgs/Octomap`), `occupied_cells_vis_array` (MarkerArray), `octomap_point_cloud_centers`
(PointCloud2) and `projected_map` (`nav_msgs/OccupancyGrid`, the occupied cells between
`occupancy_min_z` and `occupancy_max_z` flattened to 2D). Services: `octomap_binary`,
`octomap_full`, `~/clear_bbox`, `~/reset`. The input subscription uses sensor-data QoS.

- Set `sensor_model.max_range`: every inserted point also ray-casts free space from the sensor to
  the point, and long rays dominate the cost.
- Feed it a cropped, voxelised cloud ([filters.md](filters.md)); the robot's own body and the floor
  otherwise end up as occupied cells. `occupancy_min_z` above the floor keeps the floor out of
  `projected_map`.
- With `frame_id: odom` the map drifts with odometry; use `map` when SLAM or localisation runs.
- Other executables: `octomap_server_static_node` (serves a saved map), `color_octomap_server_node`,
  `tracking_octomap_server_node`, `octomap_server_multilayer_node`.

Save and reload:

```bash
ros2 run octomap_server octomap_saver_node --ros-args -p octomap_path:=my_map.bt   # binary
ros2 run octomap_server octomap_saver_node --ros-args -p octomap_path:=my_map.ot -p full:=true
ros2 run octomap_server octomap_server_node --ros-args -p octomap_path:=my_map.bt -p frame_id:=map
```

`.bt` stores occupied and free only; `.ot` stores the full probabilities. A colour octree saves only
with `full:=true`. The 2D `projected_map` saves like any occupancy grid, with Nav2's map saver
(`nav-nav2`).

For navigation, a 2D or 3D lidar usually feeds a costmap's obstacle or voxel layer directly rather
than a stored OctoMap; that is the `nav-nav2` skill's job. For 2.5D elevation maps from PCD files,
`grid_map_pcl` has a Jazzy binary (no Lyrical release yet); its README still shows ROS 1 launch
commands, so start from the files in its `launch/` folder.

## PCD files

The Jazzy `pcl_ros` has three tools (all take `input` with sensor-data QoS):

```bash
# One file per message: <prefix><sec>.<nsec>.pcd
ros2 run pcl_ros pointcloud_to_pcd --ros-args -r input:=/lidar/points \
  -p prefix:=/tmp/scan_ -p binary:=true -p fixed_frame:=base_link

# Accumulate many clouds into one file, transformed into fixed_frame, written on Ctrl-C
ros2 run pcl_ros combined_pointcloud_to_pcd --ros-args -r input:=/lidar/points_filtered \
  -p prefix:=/tmp/ -p fixed_frame:=odom -p binary:=true -p save_on_shutdown:=true

# Publish a PCD on cloud_pcd every publishing_period_ms (default 3000)
ros2 run pcl_ros pcd_to_pointcloud --ros-args -p file_name:=/tmp/scan.pcd -p tf_frame:=map
```

- `pointcloud_to_pcd` keeps all fields; `fixed_frame` transforms each cloud first (empty: keep the
  cloud's frame). `compressed:=true` writes binary-compressed files.
- `combined_pointcloud_to_pcd` names its file `<prefix>combined_<time>.pcd`; `save_timer_sec`
  writes periodically. With `fixed_frame: odom` the result is only as good as odometry: a quick map
  of a small area, not a SLAM map.
- `pcd_to_pointcloud` defaults `tf_frame` to `/base_link`, with a leading slash that TF2 rejects as
  a frame name; always set it.
- There is no `bag_to_pcd` on Jazzy (it is commented out of the build; Lyrical has it). Play the
  bag and run `pointcloud_to_pcd` instead: `ros2 bag play run/ & ros2 run pcl_ros pointcloud_to_pcd ...`.
- Open3D reads and writes PCD and PLY too: `o3d.io.read_point_cloud`, `o3d.io.write_point_cloud`.

## RViz

- **Fixed Frame**: a frame that exists and suits the check (`base_link` for mounting, `odom` or
  `map` for accumulation). A wrong fixed frame shows "No transform" in red under the display.
- **PointCloud2 display**: Topic; **Reliability Policy `Best Effort`** for best-effort drivers
  (RViz subscribes reliable, depth 5, by default); Style (`Flat Squares` by default, `Points` is
  cheapest); Size (m) (0.01 default; raise for sparse clouds); Color Transformer `Intensity`,
  `AxisColor` (height) or `RGB8`; Decay Time > 0 accumulates clouds in the fixed frame, which makes
  calibration and odometry errors visible as smearing.
- **LaserScan display** for 2D scans, with the same QoS and colour settings.
- **TF display** with names on, to see where each sensor frame sits.
- **MarkerArray** for boxes such as `obstacle_boxes` from [python-node.md](python-node.md);
  the **Map** display for `projected_map`; from `octomap_rviz_plugins`, **OccupancyGrid** (the octree
  as 3D cells; **ColorOccupancyGrid** for colour trees) and **OccupancyMap** (its 2D projection),
  on `octomap_binary` or `octomap_full`.

## Foxglove

Run `foxglove_bridge` on the robot (see [Foxglove](../../../wiki/tools/foxglove.md)) and use a 3D
panel: clouds, scans, TF and markers in one view, from a remote machine through one WebSocket, or
from an MCAP bag without ROS installed. Over Wi-Fi a 3D lidar can outrun the link; view a cropped,
voxelised topic or compress it ([filters.md](filters.md)).

## CloudCompare

[CloudCompare](../../../wiki/tools/cloudcompare.md) (GPL, a desktop app; Ubuntu 24.04 ships
`cloudcompare` 2.11.3 through apt) opens PCD and PLY files from the tools above. Use it to:

- measure distances between picked points, to check a lidar's range against a tape measure;
- fit a plane to the floor and read its normal, to check the mount's pitch and roll;
- compute cloud-to-cloud distances between two scans of the same static scene, to check a
  lidar-to-lidar calibration or a map's repeatability;
- crop and clean a map by hand before using it as a reference.

Save clouds in `fixed_frame: base_link` for mount checks, and in `map` for map checks, so the
coordinates in CloudCompare mean what you think.
