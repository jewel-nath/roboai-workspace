# The planning scene: known objects and sensed obstacles (Jazzy)

Part of [manip-moveit2](../SKILL.md). Checked against MoveIt 2.12.4 (`occupancy_map_monitor`,
`pointcloud_octomap_updater`, `move_group` default capabilities, the Setup Assistant's `sensors_3d.yaml`
template) and the perception-pipeline tutorial source.

MoveIt avoids only what is in its planning scene. Objects get there in two ways: as known geometry you add
(boxes, cylinders, meshes) or as an occupancy map (octomap) built from a depth camera or point cloud.

## Known geometry

- Add `moveit_msgs/CollisionObject`s from code ([move-group-interface.md](move-group-interface.md),
  [moveit-py.md](moveit-py.md)), from RViz (MotionPlanning, Scene Objects tab), or by publishing on
  `/collision_object`. Give each a `header.frame_id` that TF knows; MoveIt stores it in the planning frame.
- Save and reload a whole scene: `move_group` serves `/save_geometry_to_file` and `/load_geometry_from_file`
  by default (`moveit_msgs/srv/SaveGeometryToFile`, `LoadGeometryFromFile`), and the Scene Objects tab exports
  and imports `.scene` files.
- Model the table, walls, the mounting plate and any cable carrier as boxes even if a camera also sees them: the
  octomap is coarse and arrives late.
- Detected objects you will grasp are better as collision objects (a box or mesh at the detected pose) than as
  octomap cells: they can then be attached, and MTC can name them. Getting the pose is in
  [perception-camera](../../perception-camera/SKILL.md) and [manip-grasping](../../manip-grasping/references/grasp-poses.md).

## Sensed obstacles: sensors_3d.yaml

The octomap updaters live in `moveit_ros_perception`, which `ros-jazzy-moveit` does not pull in: install
`ros-jazzy-moveit-ros-perception` (or `ros-jazzy-moveit-runtime`, which includes it).

```yaml
# my_robot_moveit_config/config/sensors_3d.yaml
sensors: [wrist_camera]
wrist_camera:
  sensor_plugin: occupancy_map_monitor/PointCloudOctomapUpdater
  point_cloud_topic: /camera/depth/color/points   # your driver's PointCloud2 topic
  max_range: 1.5               # m; points further away are dropped
  point_subsample: 1           # use every n-th point
  padding_offset: 0.03         # m added around robot links when filtering the robot out of the cloud
  padding_scale: 1.0
  max_update_rate: 5.0         # Hz
  filtered_cloud_topic: /camera/filtered_points   # the cloud after self-filtering, for checking
```

The point-cloud updater needs every key above (`ns` is optional): one missing key and it does not load. For a
depth image use `occupancy_map_monitor/DepthImageOctomapUpdater` with `image_topic`, `queue_size`,
`near_clipping_plane_distance`, `far_clipping_plane_distance`, `shadow_threshold`, `padding_scale`,
`padding_offset`, `max_update_rate`, `skip_vertical_pixels`, `skip_horizontal_pixels`, `filtered_cloud_topic`;
it reads them in that order and stops at the first missing one, leaving the rest at their defaults.

Also give `move_group` these parameters (in the launch file or a YAML loaded with it):

| Parameter | Meaning | If missing |
|---|---|---|
| `octomap_frame` | Fixed frame the map is kept in (`base_link` or `world`; on a mobile base an odometry or map frame) | Error `No 'octomap_frame' parameter defined for octomap updates` |
| `octomap_resolution` | Voxel size, m | 0.1 m, with a warning |

`MoveItConfigsBuilder` loads `config/sensors_3d.yaml` by default when the file exists and its `sensors` list is
not empty.

- The camera's TF must be right: the self-filter and the map both depend on `camera_link` relative to the arm.
  Calibrate it with the hand-eye procedure in [manip-grasping](../../manip-grasping/references/hand-eye.md).
- The self-filter removes points inside the padded robot links and attached objects. Too little padding and the
  arm sees its own fingers as obstacles; check `filtered_cloud_topic` in RViz.
- An object you are about to grasp is also in the octomap; either remove it from the cloud, add it as a collision
  object and allow contact, or clear the map (`ros2 service call /clear_octomap std_srvs/srv/Empty`) before the
  final approach.
- Occupied cells stay until a sensor ray passes through them, so obstacles that moved away can leave ghosts in
  places the camera no longer sees. Clear the map before each pick if that happens.
- Finer voxels make collision checks slower: use the coarsest `octomap_resolution` that still separates the
  objects near the gripper, and measure planning time when you change it.

## Checks

- RViz MotionPlanning display, Scene Geometry: the table and fixtures appear where they are in reality
  (measure two corners with the tool tip).
- With a camera: the octomap appears in RViz, the arm itself is not in it, and a box placed in the workspace
  makes plans route around it.
- `ros2 service call /check_state_validity moveit_msgs/srv/GetStateValidity "{group_name: arm, robot_state: {is_diff: true}}"`
  checks the current state; with the arm touching a known object it reports `valid: false` and lists the contact.
