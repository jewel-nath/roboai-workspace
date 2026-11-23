# Docking with `opennav_docking` (Jazzy)

Part of [nav-nav2](../SKILL.md). Checked against `nav2_docking` in navigation2 1.3.14 (`jazzy` branch: its README,
`opennav_docking` sources and `nav2_params.yaml`) and the docs.nav2.org docking tutorial. Licence Apache-2.0.
Jazzy binaries: `ros-jazzy-opennav-docking`, `-opennav-docking-bt`, `-opennav-docking-core` (pulled in by
`navigation2`).

## What the server does

`docking_server` (already in Jazzy's `navigation_launch.py` and its lifecycle list) runs one `dock_robot` action:

1. Look up the dock (by id in the database, or a pose and type in the request).
2. If the robot is farther than `dock_prestaging_tolerance` from the dock's staging pose, send it there through
   `navigate_to_pose`.
3. Ask the dock plugin for the dock pose (from detection or the database), then close in with its own
   pose-following controller, refining the target as detections arrive.
4. Stop when the plugin reports docked (pose within `docking_threshold`, or a motor stall), then wait for charging
   (charging docks) and succeed. Failures retry up to `max_retries` by backing out to the staging pose.

`undock_robot` drives back to the staging pose. The server publishes on `/cmd_vel` directly, so the velocity
smoother and collision monitor do not see docking motion; its controller has its own `use_collision_detection`.

## Configuration

```yaml
docking_server:
  ros__parameters:
    base_frame: "base_link"
    fixed_frame: "odom"               # smooth frame for the final approach, not map
    dock_backwards: false             # true if the robot reverses into the dock
    dock_prestaging_tolerance: 0.5
    max_retries: 3
    enable_stamped_cmd_vel: true      # if the base takes TwistStamped
    dock_plugins: ["charger"]
    charger:
      plugin: "opennav_docking::SimpleChargingDock"   # or SimpleNonChargingDock (conveyor, pallet)
      staging_x_offset: -0.7          # staging pose 0.7 m in front of the dock pose
      docking_threshold: 0.05         # m; docked when this close (without stall detection)
      use_external_detection_pose: true
      external_detection_timeout: 1.0
      external_detection_translation_x: -0.18   # docked base pose relative to the detected marker
      external_detection_translation_y: 0.0
      external_detection_rotation_roll: -1.57   # values from Jazzy's nav2_params.yaml (node default
      external_detection_rotation_pitch: -1.57  # pitch is +1.57); check them against your detector
      external_detection_rotation_yaw: 0.0
      use_battery_status: true        # node default true; charging when current > charging_threshold
      charging_threshold: 0.5
      use_stall_detection: false      # true: docked when stall_joint_names stall (joint_states)
    docks: ["home_dock"]
    home_dock:
      type: "charger"
      frame: map
      pose: [1.20, -0.40, 3.14]       # x, y, yaw of the dock in frame
    controller:
      v_linear_min: 0.1
      v_linear_max: 0.15
      use_collision_detection: true
```

- `dock_plugins` must name at least one plugin or the server fails to configure, which aborts Nav2's bringup.
- Many docks: put them in a file and set `dock_database: $(find-pkg-share my_robot_navigation)/config/docks.yaml`
  (top key `docks:`, one entry per dock with `type`, `frame`, `pose`, optional `id`). Reload at run time with
  `/docking_server/reload_database` (`nav2_msgs/srv/ReloadDockDatabase`).
- `type` may be empty when only one plugin is loaded.
- Without detection (`use_external_detection_pose: false`) the plugin trusts the database pose: fine for testing,
  weak in production. Without battery data set `use_battery_status: false`, or the robot docks and then fails with
  `FAILED_TO_CHARGE` after `wait_charge_timeout`.

## Inputs the simple plugins read

| Topic | Type | Needed when |
|---|---|---|
| `detected_dock_pose` | `geometry_msgs/msg/PoseStamped` | `use_external_detection_pose: true` |
| `battery_state` | `sensor_msgs/msg/BatteryState` | `use_battery_status: true` (charging dock) |
| `joint_states` | `sensor_msgs/msg/JointState` | `use_stall_detection: true` |

Detection: a fiducial on the dock seen by a camera. `image_proc`'s `track_marker_node` (BSD, `ros-jazzy-image-proc`)
publishes `tracked_pose` (`PoseStamped`) for one OpenCV ArUco marker; remap it to `detected_dock_pose`:

```bash
ros2 run image_proc track_marker_node --ros-args \
  -r image:=/camera/image_rect -r camera_info:=/camera/camera_info -r tracked_pose:=/detected_dock_pose \
  -p marker_id:=0 -p marker_size:=0.10 -p dictionary:=10      # 10 = DICT_6X6_250, the default
```

`apriltag_ros` publishes detections and TF instead, so it needs a small node that turns the tag frame into a
`PoseStamped` ([AprilTag](../../../wiki/software/apriltag.md); camera setup in
[perception-camera](../../perception-camera/SKILL.md)). The simple plugins publish `dock_pose` and
`filtered_dock_pose` for checking in RViz.

## Sending dock requests

```bash
ros2 action send_goal /dock_robot nav2_msgs/action/DockRobot "{dock_id: home_dock}" --feedback
ros2 action send_goal /dock_robot nav2_msgs/action/DockRobot \
  "{use_dock_id: false, dock_type: charger, dock_pose: {header: {frame_id: map}, pose: {position: {x: 1.2, y: -0.4}, orientation: {z: 1.0, w: 0.0}}}}"
ros2 action send_goal /undock_robot nav2_msgs/action/UndockRobot "{dock_type: charger}"
```

- `navigate_to_staging_pose: false` skips step 2 (the robot must already be within tolerance); `max_staging_time`
  bounds it (1000 s default).
- Python: `BasicNavigator.dockRobotByID('home_dock')`, `dockRobotByPose(pose, 'charger')`, `undockRobot('charger')`.
- In a behavior tree: `DockRobot` (`dock_id`, `use_dock_id`, `dock_pose`, `dock_type`, `navigate_to_staging_pose`)
  and `UndockRobot` (`dock_type`). They are not built into `bt_navigator`; add
  `plugin_lib_names: ["opennav_dock_action_bt_node", "opennav_undock_action_bt_node"]`. The installed
  `opennav_docking_bt/behavior_trees/application_example.xml` sketches undock, work, dock; it lacks
  `BTCPP_format="4"` and uses a lowercase `inverter`, so fix both before loading it.
- Result `error_code`: 901 dock not in database, 902 dock not valid, 903 failed to stage, 904 failed to detect,
  905 failed to control, 906 failed to charge.
- RViz: the `nav2_rviz_plugins/Docking` panel sends dock and undock requests.

## Checks

- `ros2 lifecycle get /docking_server` is `active`; the log lists the dock plugins and docks it loaded.
- With the robot at the staging pose, `ros2 topic echo /detected_dock_pose` updates while the marker is in view,
  and `filtered_dock_pose` in RViz sits on the physical dock.
- `dock_robot` succeeds ten times in a row from the staging pose and from across the room; `undock_robot` returns
  the robot to the staging pose.
- On a charging dock, `battery_state` current rises above `charging_threshold` within `wait_charge_timeout`.
