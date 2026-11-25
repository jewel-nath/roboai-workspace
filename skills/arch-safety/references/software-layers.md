# Software layers: timeouts and limits

Where each ROS 2 Jazzy package stops a robot whose commands go silent, and where it clamps commands.
None of this is safety-rated. These layers make faults rarer and gentler; the stop chain
([stop-chain.md](stop-chain.md)) is what protects people. Defaults below are from the `jazzy` branches
of ros2_controllers (4.43.1), ros2_control (4.50), navigation2 (1.3.14), moveit2 (2.12.4) and
twist_mux (4.5.0) on 2026-11-25. They are the packages' defaults, not recommendations.

## The command chain

```text
teleop ─┐
web UI ─┼─> twist_mux ─> stop gate ─> velocity_smoother ─> collision_monitor ─> diff_drive_controller ─> hardware ─> drive / firmware
Nav2  ──┘   (timeouts,   (heartbeats,  (velocity_timeout)   (source_timeout)     (cmd_vel_timeout,       (its own command timeout)
             locks)       latch)                                                   limits)
```

Nav2's own wiring is controller → `velocity_smoother` → `collision_monitor` → `/cmd_vel`
([nav-nav2](../../nav-nav2/SKILL.md)). If teleop and the web UI should also pass the collision monitor,
put the mux in front of the smoother by remapping, as drawn. Whatever the order, the last hop before
the controller should be the one that can only stop or slow, never add motion.

## Timeouts

| Where | Parameter | Jazzy default | When it fires |
|---|---|---|---|
| `diff_drive_controller` | `cmd_vel_timeout` | 0.5 s; 0.0 disables | Wheel references set to zero; logs `Velocity command timed out. Braking.` |
| `joint_trajectory_controller` | `cmd_timeout` | 0.0 (off); ignored with a warning unless greater than `constraints.goal_time` | The trajectory is aborted and the arm holds once its last point is older than this (`Aborted due to command timeout`) |
| `velocity_smoother` | `velocity_timeout` | 1.0 s | Publishes zero commands, decelerating within its limits, then stops publishing |
| `collision_monitor` | `source_timeout` | 1.0 s in `nav2_params.yaml`; 0.0 disables | A silent or stale scan source stops the robot (`invalid source`) |
| `twist_mux` | `topics.<name>.timeout` | per entry (0.5 s in the package's example) | That input is ignored; the mux forwards nothing and never sends zero |
| `twist_mux` | `locks.<name>.timeout` | 0.0 (no timeout) | Above 0.0, a lock whose publisher goes silent engages |
| MoveIt Servo | `incoming_command_timeout` | 0.1 s | Older commands are discarded and Servo halts |
| MoveIt execution | `trajectory_execution.execution_duration_monitoring` | `true` | A trajectory running longer than expected (scaled by `allowed_execution_duration_scaling`, plus `allowed_goal_duration_margin`) is cancelled |
| Drive or firmware | your board's parameter | — | The only timeout here that works with Linux dead |

Pick each timeout from the stopping budget, not from habit: at 1.0 m/s a 0.5 s timeout means 0.5 m of
travel before braking even starts. The values in the snippets below are examples to tune.

**Stamps decide the age.** `diff_drive_controller` measures a command's age from its
`header.stamp`. A zero stamp is replaced by the controller's time; a command already older than the
timeout is dropped with a warning. A sender whose clock runs ahead of the robot's makes every command
look young, and the timeout fires late by the clock difference. The collision monitor ages its sources
the same way. Synchronise clocks (chrony) on every machine that publishes commands or sensor data.

## Configuration examples

Controller manager and base controller (`my_robot_bringup/config/controllers.yaml`):

```yaml
controller_manager:
  ros__parameters:
    update_rate: 100
    enforce_command_limits: true     # read-only; Jazzy default false
    diff_drive_controller:
      type: diff_drive_controller/DiffDriveController

diff_drive_controller:
  ros__parameters:
    left_wheel_names: ["left_wheel_joint"]
    right_wheel_names: ["right_wheel_joint"]
    wheel_separation: 0.30           # measured
    wheel_radius: 0.05               # measured
    cmd_vel_timeout: 0.25            # example: fits a 0.5 m/s top speed and a 0.15 m budget
    linear.x.max_velocity: 0.5       # unset (NaN) means no limit
    linear.x.min_velocity: -0.3
    linear.x.max_acceleration: 0.8
    linear.x.max_deceleration: -1.5
    angular.z.max_velocity: 1.5
    angular.z.min_velocity: -1.5
    angular.z.max_acceleration: 3.0
    angular.z.max_deceleration: -3.0
```

The `has_velocity_limits` style flags are deprecated on Jazzy; leave a limit unset to disable it.

Arm controller:

```yaml
arm_controller:
  ros__parameters:
    joints: [joint1, joint2, joint3, joint4, joint5, joint6]
    command_interfaces: [position]
    state_interfaces: [position, velocity]
    cmd_timeout: 0.5                  # example; must exceed constraints.goal_time
    constraints:
      stopped_velocity_tolerance: 0.01
      goal_time: 0.2                  # 0.0 waits forever for the goal
      joint1:
        trajectory: 0.2               # 0.0 disables the path tolerance check
        goal: 0.05
```

URDF limits that `enforce_command_limits` applies. With a `<safety_controller>` tag the controller
manager uses the soft-limit limiter, which pulls commands back inside the soft range without exceeding
the velocity limit; without it, it saturates to `<limit>`:

```xml
<joint name="joint2" type="revolute">
  <limit lower="-1.57" upper="1.57" velocity="1.0" effort="40.0"/>
  <safety_controller soft_lower_limit="-1.50" soft_upper_limit="1.50"
                     k_position="10.0" k_velocity="5.0"/>
</joint>
```

`twist_mux` with a lock that the stop gate holds open
([watchdog-node.md](watchdog-node.md)). A lock is engaged while its last `std_msgs/Bool` is `true`, or
when it has a timeout and its publisher goes silent; it masks every input with a lower priority:

```yaml
twist_mux:
  ros__parameters:
    use_stamped: true                 # Jazzy 4.5 default; false for plain Twist inputs
    topics:
      navigation:
        topic: nav_vel
        timeout: 0.5
        priority: 10
      joystick:
        topic: joy_vel
        timeout: 0.5
        priority: 100
    locks:
      stop_gate:
        topic: stop_gate/lock         # the gate publishes false at 10 Hz while all is well
        timeout: 0.3
        priority: 255
```

Velocity smoother and collision monitor parameters, polygons and the stamped-command switch are in
[nav-nav2's params.md](../../nav-nav2/references/params.md). Set the smoother's `max_velocity`,
`max_accel` and `max_decel` at or below the base controller's limits, so the smoother, not the
controller's clamp, shapes normal motion.

## Limits

| Where | Parameters | Note |
|---|---|---|
| URDF | `<limit>`; optional `<safety_controller>` soft limits | Read by ros2_control and MoveIt; keep them true to the hardware |
| Controller manager | `enforce_command_limits` | Read-only: set it in the YAML before start. Lyrical defaults it to `true` |
| `diff_drive_controller` | `linear.x.*`, `angular.z.*` velocity, acceleration, deceleration, jerk | Unset is unlimited |
| `velocity_smoother` | `max_velocity`, `min_velocity`, `max_accel`, `max_decel` per axis `[x, y, theta]` | Jazzy file: 0.5 m/s, 2.0 rad/s |
| Nav2 controller plugin | its own speed limits | At or below the smoother; [nav-planning](../../nav-planning/SKILL.md) |
| MoveIt | `joint_limits.yaml` velocity and acceleration; `default_velocity_scaling_factor`, `default_acceleration_scaling_factor` | [manip-moveit2](../../manip-moveit2/SKILL.md) |
| MoveIt Servo | `joint_limit_margins` (0.1), `check_collisions` (true), `self_collision_proximity_threshold` (0.01 m), `scene_collision_proximity_threshold` (0.02 m), `halt_all_joints_in_joint_mode` and `..._cartesian_mode` (true) | Servo slows and halts near limits and objects in its planning scene, not near people it cannot see |
| `joint_trajectory_controller` | `constraints` tolerances, `allow_nonzero_velocity_at_trajectory_end` (false) | A blocked arm aborts its goal instead of pushing on |

Software limits reduce speed and energy in normal use. A rated speed or zone limit that people rely on
belongs to a safety drive, safety controller or scanner, chosen by the assessment.

## Checks for this layer

```bash
ros2 param get /diff_drive_controller cmd_vel_timeout
ros2 param get /controller_manager enforce_command_limits
ros2 param get /velocity_smoother velocity_timeout
ros2 param get /collision_monitor source_timeout
ros2 topic echo /diagnostics --once        # twist_mux reports its topics and locks here
```

Then, with the robot on blocks or at crawl speed: stop each command source mid-motion and time the
stop; publish a command above each limit and confirm the joint states or odometry stay inside it.
