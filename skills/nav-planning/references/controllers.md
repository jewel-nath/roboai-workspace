# Controllers

Part of [nav-planning](../SKILL.md). Defaults are the values the plugin code declares in Nav2 1.3.14
(`jazzy` branch, the Jazzy binary); "bringup" means `nav2_bringup/params/nav2_params.yaml`, which ships
MPPI. Velocity and acceleration limits must not exceed what the drive controller accepts
([ros2-control](../../ros2-control/SKILL.md)).

## controller_server

```yaml
controller_server:
  ros__parameters:
    controller_frequency: 20.0            # Hz
    min_x_velocity_threshold: 0.001       # odometry below this reads as 0 (code default 0.0001)
    min_y_velocity_threshold: 0.5         # bringup value; set 0.001 on omni robots
    min_theta_velocity_threshold: 0.001
    failure_tolerance: 0.3                # s a controller may fail before the action aborts (code 0.0)
    progress_checker_plugins: ["progress_checker"]
    goal_checker_plugins: ["general_goal_checker"]
    controller_plugins: ["FollowPath"]    # keep this ID: the default BTs use controller_id "FollowPath"
    progress_checker:
      plugin: "nav2_controller::SimpleProgressChecker"
      required_movement_radius: 0.5
      movement_time_allowance: 10.0
    general_goal_checker:
      plugin: "nav2_controller::SimpleGoalChecker"
      xy_goal_tolerance: 0.25
      yaw_goal_tolerance: 0.25
      stateful: true
    FollowPath:
      plugin: "nav2_mppi_controller::MPPIController"
```

Other server keys: `costmap_update_timeout` 0.30 s, `use_realtime_priority` `false`,
`publish_zero_velocity` `true`, `speed_limit_topic` `speed_limit`. The odometry thresholds zero the
measured twist the controller sees, so the bringup `min_y_velocity_threshold: 0.5` hides all sideways
motion below 0.5 m/s from an omni robot's controller.

## MPPI: `nav2_mppi_controller::MPPIController`

Samples `batch_size` noisy control sequences around the last solution, rolls them through a motion model
for `time_steps` x `model_dt` seconds, scores them with critic plugins and blends them. CPU only (its README;
vectorised with xtensor/xsimd), no GPU. Works for diff, omni and Ackermann.

| Key | Code default (bringup) | Notes |
|---|---|---|
| `motion_model` | `"DiffDrive"` | `"Omni"` or `"Ackermann"` |
| `time_steps`, `model_dt` | 56, 0.05 | horizon 2.8 s; `model_dt` no larger than 1/`controller_frequency` (README) |
| `batch_size` | 1000 (2000) | lower first if the loop misses its rate |
| `iteration_count` | 1 | |
| `vx_max`, `vx_min` | 0.5, -0.35 | m/s; `vx_min: 0.0` forbids reversing |
| `vy_max` | 0.5 | omni only |
| `wz_max` | 1.9 | rad/s |
| `ax_max`, `ax_min`, `ay_max`, `ay_min`, `az_max` | 3.0, -3.0, 3.0, -3.0, 3.5 | acceleration bounds |
| `vx_std`, `vy_std`, `wz_std` | 0.2, 0.2, 0.4 | sampling noise |
| `temperature`, `gamma` | 0.3, 0.015 | leave unless you know MPPI |
| `prune_distance` | 1.5 (1.7) | m of path ahead considered; at least max speed x horizon |
| `transform_tolerance` | 0.1 | s |
| `enforce_path_inversion` | `false` | `true` to stop at Reeds-Shepp cusps before reversing |
| `AckermannConstraints.min_turning_r` | 0.2 | m, with `motion_model: "Ackermann"` |
| `visualize` | `false` (`true`) | publishes `/trajectories`; costly, turn off when deployed |
| `regenerate_noises` | `false` (`true`) | |

Critics in the bringup file: `ConstraintCritic`, `CostCritic`, `GoalCritic`, `GoalAngleCritic`,
`PathAlignCritic`, `PathFollowCritic`, `PathAngleCritic`, `PreferForwardCritic`, each with `enabled`,
`cost_weight`, `cost_power` and its own keys. Start from those values. Per drive:

```yaml
    FollowPath:                          # omnidirectional (mecanum, omni wheels)
      plugin: "nav2_mppi_controller::MPPIController"
      motion_model: "Omni"
      vy_max: 0.5
      vy_std: 0.2
      critics: ["ConstraintCritic", "CostCritic", "GoalCritic", "GoalAngleCritic",
                "PathAlignCritic", "PathFollowCritic", "PathAngleCritic", "TwirlingCritic"]
      TwirlingCritic:                    # stops needless spinning on omni models
        enabled: true
        cost_power: 1
        cost_weight: 10.0                # code default
```

```yaml
    FollowPath:                          # Ackermann
      plugin: "nav2_mppi_controller::MPPIController"
      motion_model: "Ackermann"
      AckermannConstraints:
        min_turning_r: 0.80              # same radius the Smac planner uses
      vx_min: -0.35                      # 0.0 if the car must not reverse
      enforce_path_inversion: true       # with a REEDS_SHEPP planner
      PathAngleCritic:
        mode: 2                          # follow the path's own direction, reversing included
```

Keep the other critics and their keys from the bringup file in both cases (omitted above).
`PathAngleCritic.mode` is 0 (prefer driving forward, the default), 1 (no preferred direction) or 2 (follow
the orientations in a feasible Smac path); `PreferForwardCritic` penalises reversing. Tuning order from the MPPI
README: set the speed limits and the motion model; make sure the local costmap half-width covers
`vx_max x time_steps x model_dt` (2.8 s at 0.5 m/s needs at least 1.4 m each side); tune `CostCritic`
weight together with the inflation radius and scale (too strong and the robot wobbles in corridors or will
not leave zero-cost space); then balance `PathFollowCritic` and `PathAlignCritic` for how closely it tracks
the path.

## Regulated Pure Pursuit: `nav2_regulated_pure_pursuit_controller::RegulatedPurePursuitController`

Geometric path tracker: drives toward a lookahead point, slows in tight turns and near obstacles. Follows
the path closely and does not swerve around new obstacles (it stops). Pair it with a feasible planner for
Ackermann; diff-drive robots can follow any path.

| Key | Default | Notes |
|---|---|---|
| `desired_linear_vel` | 0.5 | m/s cruise speed |
| `lookahead_dist`, `min_lookahead_dist`, `max_lookahead_dist` | 0.6, 0.3, 0.9 | m |
| `use_velocity_scaled_lookahead_dist`, `lookahead_time` | `false`, 1.5 | lookahead = speed x time, clamped |
| `use_regulated_linear_velocity_scaling` | `true` | slow in curves below `regulated_linear_scaling_min_radius` 0.9 m |
| `regulated_linear_scaling_min_speed` | 0.25 | |
| `use_cost_regulated_linear_velocity_scaling` | `true` | slow near obstacles: `cost_scaling_dist` 0.6, `cost_scaling_gain` 1.0, `inflation_cost_scaling_factor` 3.0 (match the costmap's) |
| `use_rotate_to_heading` | `true` | rotate in place to the path and the goal; **`false` for Ackermann** |
| `rotate_to_heading_angular_vel`, `rotate_to_heading_min_angle`, `max_angular_accel` | 1.8, 0.785, 3.2 | |
| `allow_reversing` | `false` | `true` follows reversing segments; needs `use_rotate_to_heading: false` |
| `use_collision_detection`, `max_allowed_time_to_collision_up_to_carrot` | `true`, 1.0 | s |
| `approach_velocity_scaling_dist`, `min_approach_linear_velocity` | 0.6, 0.05 | slow-down near the goal |
| `use_fixed_curvature_lookahead`, `curvature_lookahead_dist` | `false`, 0.6 | |
| `stateful` | `true` | keeps rotating once the xy goal is reached |
| `transform_tolerance`, `max_robot_pose_search_dist` | 0.1, half the local costmap size | |

Car-like robot:

```yaml
    FollowPath:
      plugin: "nav2_regulated_pure_pursuit_controller::RegulatedPurePursuitController"
      desired_linear_vel: 0.8
      use_velocity_scaled_lookahead_dist: true
      lookahead_time: 1.5
      min_lookahead_dist: 0.5
      max_lookahead_dist: 1.5
      use_rotate_to_heading: false
      allow_reversing: true              # only with a REEDS_SHEPP or reversing lattice planner
      regulated_linear_scaling_min_radius: 0.9
```

## DWB: `dwb_core::DWBLocalPlanner`

Samples velocity pairs (or triples for omni), simulates each for `sim_time`, scores them with critics.
Every kinematic limit defaults to **0.0**, so a DWB block without them never moves the robot.

```yaml
    FollowPath:
      plugin: "dwb_core::DWBLocalPlanner"
      min_vel_x: 0.0
      max_vel_x: 0.5
      max_vel_y: 0.0                     # > 0 and vy_samples > 1 on omni robots
      max_vel_theta: 1.5
      min_speed_xy: 0.0
      max_speed_xy: 0.5
      min_speed_theta: 0.0
      acc_lim_x: 2.5
      acc_lim_y: 0.0
      acc_lim_theta: 3.2
      decel_lim_x: -2.5
      decel_lim_y: 0.0
      decel_lim_theta: -3.2
      vx_samples: 20                     # defaults 20, 5, 20
      vy_samples: 5
      vtheta_samples: 20
      sim_time: 1.7                      # default
      critics: ["RotateToGoal", "Oscillation", "BaseObstacle", "GoalAlign", "PathAlign", "PathDist", "GoalDist"]
      BaseObstacle.scale: 0.02
      PathAlign.scale: 32.0
      PathAlign.forward_point_distance: 0.1
      GoalAlign.scale: 24.0
      GoalAlign.forward_point_distance: 0.1
      PathDist.scale: 32.0
      GoalDist.scale: 24.0
      RotateToGoal.scale: 32.0
      RotateToGoal.slowing_factor: 5.0
      RotateToGoal.lookahead_time: -1.0
```

The critic weights are the ones in the DWB page of docs.nav2.org, not code defaults. `BaseObstacle` checks
only the robot centre; use `ObstacleFootprint` for non-round robots. Other keys: `prune_distance` 2.0,
`transform_tolerance` 0.1, `debug_trajectory_details` `false`, `trajectory_generator_name`
`dwb_plugins::StandardTrajectoryGenerator` (or `dwb_plugins::LimitedAccelGenerator`).

## Graceful: `nav2_graceful_controller::GracefulController`

Jong Jin Park's smooth pose-following control law, steering toward a motion target on the path: smooth,
comfortable curves. The Nav2 plugin list gives differential, omni and legged robots.

| Key | Default | Notes |
|---|---|---|
| `v_linear_min`, `v_linear_max`, `v_angular_max` | 0.1, 0.5, 1.0 | |
| `v_angular_min_in_place` | 0.25 | |
| `min_lookahead`, `max_lookahead` | 0.25, 1.0 | m, motion target search |
| `k_phi`, `k_delta`, `beta`, `lambda` | 2.0, 1.0, 0.4, 2.0 | control law gains; `lambda` >= 1, `beta` > 0 |
| `slowdown_radius` | 1.5 | m |
| `initial_rotation`, `initial_rotation_tolerance` | `true`, 0.75 | rotate first when the path heading differs |
| `prefer_final_rotation` | `true` | follow the path heading, rotate at the goal |
| `rotation_scaling_factor` | 0.5 | |
| `allow_backward` | `false` | |
| `in_place_collision_resolution` | 0.1 | rad |

The package README still lists `motion_target_dist`, `initial_rotation_min_angle` and `final_rotation`;
the Jazzy code reads the names above.

## Rotation Shim: `nav2_rotation_shim_controller::RotationShimController`

Rotates in place toward the path's heading, then hands over to a primary controller. Use it in front of
RPP, DWB or MPPI on robots that can turn in place, when paths come from NavFn, Theta* or Smac 2D. Not for
Ackermann, and not needed with Hybrid-A* or Lattice paths.

```yaml
    FollowPath:
      plugin: "nav2_rotation_shim_controller::RotationShimController"
      primary_controller: "nav2_regulated_pure_pursuit_controller::RegulatedPurePursuitController"
      angular_dist_threshold: 0.785        # rad; rotate first above this
      angular_disengage_threshold: 0.3925  # rad; default is half the threshold
      forward_sampling_distance: 0.5
      rotate_to_heading_angular_vel: 1.8
      max_angular_accel: 3.2
      simulate_ahead_time: 1.0
      rotate_to_goal_heading: false
      # the primary controller's own keys go in this same block in Jazzy
      desired_linear_vel: 0.5
      lookahead_dist: 0.6
```

Other keys: `max_cost_threshold` 254, `rotate_to_heading_once` `false`, `closed_loop` `true`,
`use_path_orientations` `false`.

## Vector Pursuit

`vector_pursuit_controller::VectorPursuitController` from Black Coffee Robotics (Apache-2.0,
`ros-jazzy-vector-pursuit-controller`, outside the Nav2 repo) is a geometric tracker that also uses the
path heading; Nav2's tuning guide suggests it, like RPP, for feasible paths at higher speed. Read its
README for parameters.
