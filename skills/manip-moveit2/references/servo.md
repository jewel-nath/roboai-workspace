# MoveIt Servo (Jazzy)

Part of [manip-moveit2](../SKILL.md). Checked against `moveit_servo` 2.12.4 (`servo_parameters.yaml`,
`servo_node.cpp`, `servo.cpp`, `demo_ros_api.launch.py`), `moveit_msgs` (`ServoCommandType.srv`,
`ServoStatus.msg`) and the realtime-servo tutorial source. Nothing here was run on hardware.

Servo turns a stream of commands (joint jog, end-effector twist, or a target pose to track) into joint commands
for one planning group, at a fixed rate, while it slows down near collisions, singularities and joint limits.
Use it for joystick or keyboard teleoperation, visual servoing and small corrections; use planning for moves
between distant poses.

```bash
sudo apt install ros-jazzy-moveit-servo
ros2 launch moveit_servo demo_ros_api.launch.py   # Panda demo from moveit_resources
```

## What it commands

Servo publishes on `command_out_topic`, either:

- `trajectory_msgs/JointTrajectory` to the arm's `joint_trajectory_controller` topic
  (`/arm_controller/joint_trajectory`): the same controller MoveIt executes plans with, so no switching.
- `std_msgs/Float64MultiArray` to a forward command controller (for example
  `position_controllers/JointGroupPositionController`): fewer layers, but MoveIt's plans then need a controller
  switch.

A planned trajectory and Servo must not command the controller at the same time: pause Servo
(`~/pause_servo`) before executing a plan and resume afterwards.

## config/servo.yaml

Flat keys; the launch file wraps them under `moveit_servo`. Values marked default are Jazzy's code defaults.

```yaml
move_group_name: arm                       # required, no default
command_in_type: speed_units               # default unitless (joystick range -1..1)
scale:
  linear: 0.1        # m/s max in speed_units (default 0.4); placeholder: start slow
  rotational: 0.3    # rad/s max (default 0.8)
  joint: 0.3         # used for unitless joint jog only (default 0.5)
publish_period: 0.01                       # s, default (100 Hz loop)
incoming_command_timeout: 0.1              # s, default; uses each command's header.stamp
command_out_topic: /arm_controller/joint_trajectory   # default is a Panda topic: always set it
command_out_type: trajectory_msgs/JointTrajectory      # or std_msgs/Float64MultiArray
publish_joint_positions: true
publish_joint_velocities: true
joint_topic: /joint_states
check_collisions: true                     # default
self_collision_proximity_threshold: 0.01   # m, default: start slowing
scene_collision_proximity_threshold: 0.02  # m, default
lower_singularity_threshold: 17.0          # Jacobian condition number, default: start slowing
hard_stop_singularity_threshold: 30.0      # default: stop
joint_limit_margins: [0.1]                 # rad, default; one value or one per joint
use_smoothing: true
smoothing_filter_plugin_name: online_signal_smoothing::ButterworthFilterPlugin   # default
is_primary_planning_scene_monitor: false   # move_group owns the scene (default true)
monitored_planning_scene_topic: /monitored_planning_scene   # move_group's scene updates
```

- Without `move_group`, keep `is_primary_planning_scene_monitor: true` and the default `/planning_scene`.
- Other smoothing plugins: `online_signal_smoothing::AccelerationLimitedPlugin` and
  `online_signal_smoothing::RuckigFilterPlugin`; both use the limits in `joint_limits.yaml`, and the upstream
  demo gives the acceleration-limited one `update_period` and `planning_group_name` parameters too.
- If the group has an IK solver, twist and pose commands are solved with it (approximate solutions allowed);
  otherwise Servo uses the Jacobian pseudo-inverse.

## Launch

```python
# add to the bringup launch from launch.md
from launch_param_builder import ParameterBuilder

servo_params = {
    "moveit_servo": ParameterBuilder("my_robot_moveit_config").yaml("config/servo.yaml").to_dict()
}
servo_node = Node(
    package="moveit_servo",
    executable="servo_node",
    name="servo_node",
    parameters=[
        servo_params,
        moveit_config.robot_description,
        moveit_config.robot_description_semantic,
        moveit_config.robot_description_kinematics,
        moveit_config.joint_limits,
    ],
    output="screen",
)
```

`moveit_servo::ServoNode` can also run as a component in a `component_container_mt` for intra-process latency,
as the upstream demo does.

## Commanding it

```bash
# Select the input: 0 = JOINT_JOG, 1 = TWIST, 2 = POSE
ros2 service call /servo_node/switch_command_type moveit_msgs/srv/ServoCommandType "{command_type: 1}"

# 2 cm/s along base_link x; stamp: now is refreshed on each publish, 50 Hz beats the 0.1 s timeout
ros2 topic pub -r 50 /servo_node/delta_twist_cmds geometry_msgs/msg/TwistStamped \
  "{header: {stamp: now, frame_id: base_link}, twist: {linear: {x: 0.02}}}"

ros2 topic echo /servo_node/status          # moveit_msgs/ServoStatus
ros2 service call /servo_node/pause_servo std_srvs/srv/SetBool "{data: true}"
ros2 run moveit_servo servo_keyboard_input  # keyboard teleop for the Panda demo
```

| Input | Topic (default) | Message |
|---|---|---|
| Joint jog | `~/delta_joint_cmds` | `control_msgs/msg/JointJog` (joint names and velocities) |
| Twist | `~/delta_twist_cmds` | `geometry_msgs/msg/TwistStamped`, `frame_id` required |
| Pose | `~/pose_target_cmds` | `geometry_msgs/msg/PoseStamped`, `frame_id` required |

- Twists are converted from their `frame_id` into the IK base frame. With `apply_twist_commands_about_ee_frame:
  true` (default) the angular part rotates about the end effector instead of the frame origin.
- `ServoStatus.code`: 0 no warning, 1 and 3 decelerating near or leaving a singularity, 2 halted for
  singularity, 4 decelerating for collision, 5 halted for collision, 6 joint bound, -1 invalid.
- A command older than `incoming_command_timeout` (by its header stamp) is ignored and Servo brings the arm to a
  smooth halt. Stamp commands with the current time of the same clock (`use_sim_time` in Gazebo).

## Before a real arm moves

This drives real joints continuously. What limits motion: `scale` (the commanded speed), the velocity
(and, with the acceleration or Ruckig filters, acceleration) limits in `joint_limits.yaml`,
`joint_limit_margins`, the singularity thresholds, and collision checks against the objects in the planning
scene only. None of these is a safety function: keep a hardware emergency stop in reach, start with
`scale` at a few cm/s in simulation, then on the arm with nothing in reach. System-level safety belongs to
[arch-safety](../../arch-safety/SKILL.md).

## Checks

- With the arm still, `/servo_node/status` reports code 0 and no output is published once commands stop.
- A +x twist in `base_link` moves `tool0` along +x (`ros2 run tf2_ros tf2_echo base_link tool0`) at the set speed.
- Driving toward a scene object slows and then halts (status 4, then 5) before contact, in simulation first.
- Driving toward a singular pose (arm stretched out) slows and halts with status 1, then 2.
