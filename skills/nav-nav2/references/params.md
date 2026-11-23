# Nav2 parameters a builder sets (Jazzy)

Part of [nav-nav2](../SKILL.md). Start from the Jazzy file and change only what this page lists. "Jazzy file" is the
value in `nav2_bringup/params/nav2_params.yaml` (navigation2 1.3.14); "node default" is what the node uses when the
key is missing. Planner, controller and smoother plugin parameters belong to [nav-planning](../../nav-planning/SKILL.md).

```bash
cp $(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/params/nav2_params.yaml \
  src/my_robot_navigation/config/nav2_params.yaml
```

## Layout rules

- One top-level key per node. Costmaps are nodes inside the planner and controller servers, so their keys nest twice:
  `global_costmap: global_costmap: ros__parameters:`. A single level loads nothing and the node runs on defaults.
- Keep every section of the copied file. Jazzy's `navigation_launch.py` starts `route_server` and `docking_server`
  too; `docking_server` fails to configure without `dock_plugins`, which aborts the whole bringup.
- Values may use substitutions such as `$(find-pkg-share my_robot_navigation)`; `nav2_bringup` loads the file with
  substitutions enabled.
- Verify what a node really uses: `ros2 param get /local_costmap/local_costmap footprint`, `ros2 param dump /amcl`.

## Frames and topics

| Node: keys | Jazzy file | Set to |
|---|---|---|
| `bt_navigator`: `global_frame`, `robot_base_frame`, `odom_topic` | `map`, `base_link`, `/odom` | map frame, base frame, odometry topic |
| both costmaps: `robot_base_frame` | `base_link` | base frame |
| `global_costmap` / `local_costmap`: `global_frame` | `map` / `odom` | keep |
| `amcl`: `base_frame_id`, `odom_frame_id`, `global_frame_id`, `scan_topic` | `base_footprint`, `odom`, `map`, `scan` | frames in your URDF; scan topic |
| `behavior_server`: `robot_base_frame`, `local_frame`, `global_frame` | `base_link`, `odom`, `map` | same frames |
| `collision_monitor`: `base_frame_id`, `odom_frame_id` | `base_footprint`, `odom` | frames in your URDF |
| `docking_server`: `base_frame`, `fixed_frame` | `base_link`, `odom` | keep `fixed_frame` on the smooth `odom` frame |
| `controller_server`: `odom_topic` | unset (node default `odom`) | your odometry topic |
| `velocity_smoother`: `odom_topic` | `odom` | read only with `feedback: CLOSED_LOOP` |
| each costmap and collision monitor source: `topic` | `/scan` or `scan` | your scan or cloud topic |

With robot_localization the odometry topic is usually `/odometry/filtered`.

## Robot shape

- `footprint` is a string of points in `robot_base_frame`, closed automatically; it wins over `robot_radius`
  (node default 0.1 m) when both are set. `footprint_padding` (node default 0.01 m) is added around it.
- Non-circular robots should give the local costmap the polygon. The global costmap may keep `robot_radius` when the
  planner is NavFn, Theta* or Smac 2D, which ignore heading; kinematically feasible planners use the polygon
  (Nav2 tuning guide; choice in nav-planning).
- Measure the real outline with bumpers and anything that sticks out. A shape that changes (a lifted load) can be
  published on the costmap's `footprint` topic.

## Global costmap

```yaml
global_costmap:
  global_costmap:
    ros__parameters:
      global_frame: map
      robot_base_frame: base_link
      robot_radius: 0.30            # or footprint: "[[...], ...]"
      resolution: 0.05              # match the map; node default 0.1
      track_unknown_space: true     # node default false treats unknown space as free
      update_frequency: 1.0
      publish_frequency: 1.0
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
      static_layer:
        plugin: "nav2_costmap_2d::StaticLayer"
        map_subscribe_transient_local: true
      obstacle_layer:
        plugin: "nav2_costmap_2d::ObstacleLayer"
        observation_sources: scan
        scan:
          topic: /scan
          data_type: "LaserScan"
          marking: true
          clearing: true              # node default false
          max_obstacle_height: 2.0    # node default 0.0 drops every point above the floor
          obstacle_max_range: 2.5
          raytrace_max_range: 3.0
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        inflation_radius: 0.7         # node default 0.55
        cost_scaling_factor: 3.0      # node default 10.0; lower = wider, gentler gradient
      always_send_full_costmap: true
```

## Local costmap with a lidar and a depth camera

```yaml
local_costmap:
  local_costmap:
    ros__parameters:
      global_frame: odom
      robot_base_frame: base_link
      rolling_window: true
      width: 3                      # m; widen for faster robots
      height: 3
      resolution: 0.05
      footprint: "[[0.25, 0.20], [0.25, -0.20], [-0.25, -0.20], [-0.25, 0.20]]"
      update_frequency: 5.0
      publish_frequency: 2.0
      plugins: ["voxel_layer", "inflation_layer"]
      voxel_layer:
        plugin: "nav2_costmap_2d::VoxelLayer"
        z_resolution: 0.05
        z_voxels: 16                # at most 16; covers z_voxels * z_resolution metres
        max_obstacle_height: 2.0
        observation_sources: scan depth
        scan:
          topic: /scan
          data_type: "LaserScan"
          marking: true
          clearing: true
          max_obstacle_height: 2.0
          obstacle_max_range: 2.5
          raytrace_max_range: 3.0
        depth:
          topic: /camera/depth/points
          data_type: "PointCloud2"
          marking: true
          clearing: true
          min_obstacle_height: 0.05   # above floor noise
          max_obstacle_height: 1.5    # robot height plus margin
          obstacle_max_range: 2.0
          raytrace_max_range: 2.5
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        inflation_radius: 0.7
        cost_scaling_factor: 3.0
      always_send_full_costmap: true
```

- One planar lidar and little CPU: `nav2_costmap_2d::ObstacleLayer` instead of the voxel layer, same source keys.
- Per-source keys and node defaults: `topic` (source name), `data_type` (`LaserScan`), `marking` (true),
  `clearing` (false), `min_obstacle_height` / `max_obstacle_height` (0.0 / 0.0), `obstacle_max_range` (2.5),
  `obstacle_min_range` (0.0), `raytrace_max_range` (3.0), `raytrace_min_range` (0.0), `inf_is_valid` (false; set
  true for lidars that report no return as `inf`), `expected_update_rate` (0.0, off), `observation_persistence`
  (0.0), `sensor_frame` (empty: the message's frame).
- Heights are checked in the costmap's `global_frame`, so `odom` z = 0 must be the floor.
- Other layers in Jazzy: `RangeSensorLayer` (sonar, IR; `topics`), `DenoiseLayer`, `PluginContainerLayer`.
  For 3D lidars or many depth cameras the docs suggest `spatio_temporal_voxel_layer`
  (`ros-jazzy-spatio-temporal-voxel-layer`, LGPL-2.1). Clean noisy clouds before they reach the costmap:
  [perception-lidar](../../perception-lidar/SKILL.md).
- Cell values: 0 free, 253 inscribed (the footprint would touch an obstacle), 254 lethal, 255 unknown.

## AMCL

| Key | Jazzy file | Change when |
|---|---|---|
| `robot_model_type` | `nav2_amcl::DifferentialMotionModel` | holonomic base: `nav2_amcl::OmniMotionModel` |
| `set_initial_pose`, `initial_pose.{x,y,z,yaw}` | unset (node default false, zeros) | the robot always starts at a known spot |
| `laser_max_range`, `laser_min_range` | 100.0, -1.0 | positive values clamp the scan's own limits |
| `max_beams` | 60 | more for accuracy, fewer for CPU |
| `min_particles`, `max_particles` | 500, 2000 | large maps, global localization |
| `update_min_d`, `update_min_a` | 0.25 m, 0.2 rad | how far the robot moves between filter updates |
| `alpha1` ... `alpha5` | 0.2 each | odometry noise; raise only if wheels slip a lot |
| `tf_broadcast` | true | false when another node owns `map` → `odom` |
| `transform_tolerance` | 1.0 | keep |

Services: `/reinitialize_global_localization` (`std_srvs/srv/Empty`, spreads particles over the map),
`/request_nomotion_update`, `/set_initial_pose` (`nav2_msgs/srv/SetInitialPose`). Topics: `/amcl_pose`,
`/particle_cloud`.

## Map server and map saver

- `map_server` takes `yaml_filename` (set by the launch file's `map:=`), `topic_name` (`map`), `frame_id` (`map`).
  Change the map at run time:
  `ros2 service call /map_server/load_map nav2_msgs/srv/LoadMap "{map_url: /home/<user>/maps/other.yaml}"`.
- Save a map: `ros2 run nav2_map_server map_saver_cli -f /home/<user>/maps/my_map` (options `--occ`, `--free`,
  `--mode trinary|scale|raw`, `--fmt`). With slam_toolbox, save as in [perception-slam](../../perception-slam/references/slam-toolbox.md).

## Controller server (server level only)

| Key | Jazzy file | Note |
|---|---|---|
| `controller_frequency` | 20.0 | what the CPU can hold; the plugin choice is in nav-planning |
| `general_goal_checker.xy_goal_tolerance`, `yaw_goal_tolerance` | 0.25, 0.25 | tighter than the localization error makes the robot hunt |
| `progress_checker.required_movement_radius`, `movement_time_allowance` | 0.5 m, 10.0 s | slow robots need more time |
| `failure_tolerance` | 0.3 s | how long a controller may fail before the action aborts |
| `speed_limit_topic` | node default `speed_limit` | the speed filter publishes here |

## Velocity smoother

| Key | Jazzy file | Set to |
|---|---|---|
| `max_velocity`, `min_velocity` | `[0.5, 0.0, 2.0]`, `[-0.5, 0.0, -2.0]` | real base limits `[vx, vy, wz]`; vy 0 for diff drive |
| `max_accel`, `max_decel` | `[2.5, 0.0, 3.2]`, `[-2.5, 0.0, -3.2]` | measured limits; decel values negative |
| `smoothing_frequency` | 20.0 | about the controller rate; much higher interpolates between commands |
| `feedback` | `OPEN_LOOP` | `CLOSED_LOOP` uses odometry (needs fast, low-latency odometry) |
| `velocity_timeout` | 1.0 s | sends zero and stops publishing after this long without input |
| `deadband_velocity` | `[0.0, 0.0, 0.0]` | speeds below which the motors stall; smaller commands become zero |

## Collision monitor

Sits last on `/cmd_vel`. It is a software check, not a safety-rated stop (`arch-safety`).

```yaml
collision_monitor:
  ros__parameters:
    base_frame_id: "base_link"
    odom_frame_id: "odom"
    cmd_vel_in_topic: "cmd_vel_smoothed"
    cmd_vel_out_topic: "cmd_vel"
    state_topic: "collision_monitor_state"
    transform_tolerance: 0.2
    source_timeout: 1.0             # no data for this long stops the robot; 0.0 disables the watchdog
    stop_pub_timeout: 2.0
    polygons: ["PolygonStop", "PolygonSlow"]
    PolygonStop:
      type: "polygon"
      points: "[[0.35, 0.25], [0.35, -0.25], [0.0, -0.25], [0.0, 0.25]]"   # string form since Jazzy
      action_type: "stop"
      min_points: 4
      visualize: true
      polygon_pub_topic: "polygon_stop"
    PolygonSlow:
      type: "polygon"
      points: "[[0.6, 0.35], [0.6, -0.35], [-0.3, -0.35], [-0.3, 0.35]]"
      action_type: "slowdown"
      slowdown_ratio: 0.3
      min_points: 4
      visualize: true
      polygon_pub_topic: "polygon_slowdown"
    observation_sources: ["scan"]
    scan:
      type: "scan"
      topic: "scan"
```

- `type`: `polygon`, `circle` (`radius`) or `velocity_polygon` (shapes chosen by current speed). `action_type`:
  `stop`, `slowdown`, `limit` (`linear_limit`, `angular_limit`), `approach` (uses the footprint and
  `time_before_collision`), or `none`. Sources: `scan`, `pointcloud` (`min_height`, `max_height`), `range`, `polygon`.
- The Jazzy file ships only `FootprintApproach`; add a stop polygon. The docking server publishes straight to
  `cmd_vel`, so docking motion bypasses this node and relies on its own collision check.

## Behavior server and waypoint follower

- `behavior_server.behavior_plugins`: `spin`, `backup`, `drive_on_heading`, `assisted_teleop`, `wait` as
  `nav2_behaviors::Spin` and so on. A robot with no rear sensing should drop `BackUp` from its behavior tree
  ([behavior-trees.md](behavior-trees.md)); `max_rotational_vel` (1.0) and `rotational_acc_lim` (3.2) bound the spin.
- `waypoint_follower`: `stop_on_failure` (Jazzy file false, node default true), `waypoint_task_executor_plugin`
  (`wait_at_waypoint` with `waypoint_pause_duration` in milliseconds; also `PhotoAtWaypoint`, `InputAtWaypoint`).

## TwistStamped for a ros2_control base

Jazzy publishes `Twist` unless told otherwise. For `diff_drive_controller` add to each of `controller_server`,
`behavior_server`, `velocity_smoother`, `collision_monitor` and `docking_server`:

```yaml
    enable_stamped_cmd_vel: true
```

Mixed settings leave two message types on one topic, and the subscriber with the other type gets nothing.
