# The MoveIt config package (Jazzy)

Part of [manip-moveit2](../SKILL.md). Checked against MoveIt 2.12.4 (`jazzy` branch: `moveit_setup_assistant`,
`moveit_configs_utils`, `moveit_kinematics`) and the moveit2_tutorials source. Launching it: [launch.md](launch.md).

## What the Setup Assistant writes

`ros2 launch moveit_setup_assistant setup_assistant.launch.py`, load `my_robot_description`'s xacro, then generate:

```text
my_robot_moveit_config/
  .setup_assistant                 # URDF package, xacro args, SRDF path; MoveItConfigsBuilder reads it
  package.xml, CMakeLists.txt
  config/
    my_robot.urdf.xacro            # includes your xacro and adds the ros2_control macro
    my_robot.ros2_control.xacro    # mock_components/GenericSystem, values from initial_positions.yaml
    initial_positions.yaml
    my_robot.srdf                  # groups, end effector, poses, virtual joint, disabled collisions
    kinematics.yaml                # IK plugin per group
    joint_limits.yaml              # velocity/acceleration limits, default scaling
    pilz_cartesian_limits.yaml
    moveit_controllers.yaml        # the action servers MoveIt sends trajectories to
    ros2_controllers.yaml          # controller_manager config for the demo
    sensors_3d.yaml                # only if a 3D sensor was configured
    moveit.rviz
  launch/                          # demo, move_group, moveit_rviz, rsp, spawn_controllers,
                                   # static_virtual_joint_tfs, warehouse_db, setup_assistant (.launch.py)
```

There is no `ompl_planning.yaml`: `MoveItConfigsBuilder` falls back to the defaults shipped in
`moveit_configs_utils/default_configs` (OMPL, Pilz, CHOMP, STOMP). Each generated launch file is two lines that
call a `generate_*_launch()` function from `moveit_configs_utils.launches`.

Fix the generated `package.xml` before `rosdep install`:

- The "Warehouse DB Launch" bundle adds `<exec_depend>warehouse_ros_mongo</exec_depend>`, which has no Jazzy
  release, so rosdep cannot resolve it. Untick that bundle in the Launch Files pane, or delete the line and the
  `warehouse_db.launch.py` file.
- It does not depend on the controllers the demo spawns (`controller_manager` comes with the spawn bundle). Add
  `joint_state_broadcaster`, `joint_trajectory_controller`, `parallel_gripper_controller` and
  `hardware_interface` (which provides `mock_components`).

Re-open an existing package with `ros2 launch my_robot_moveit_config setup_assistant.launch.py`. Files edited by
hand are detected by timestamp and left unticked by default; files changed both by hand and in the assistant
are marked red. Keep hand edits in git and read the file list before pressing Generate.

## SRDF essentials

```xml
<robot name="my_robot">
  <!-- Arm as a chain: the IK solver solves from base_link to tool0 -->
  <group name="arm">
    <chain base_link="base_link" tip_link="tool0"/>
  </group>
  <!-- Gripper as links plus its actuated joint; no IK solver -->
  <group name="gripper">
    <link name="gripper_base_link"/>
    <link name="left_finger_link"/>
    <link name="right_finger_link"/>
    <joint name="left_finger_joint"/>
  </group>
  <group_state name="home" group="arm">
    <joint name="joint1" value="0"/>
    <!-- one line per arm joint -->
  </group_state>
  <group_state name="open" group="gripper"><joint name="left_finger_joint" value="0.04"/></group_state>
  <group_state name="close" group="gripper"><joint name="left_finger_joint" value="0.0"/></group_state>
  <end_effector name="gripper" parent_link="tool0" group="gripper" parent_group="arm"/>
  <virtual_joint name="virtual_joint" type="fixed" parent_frame="world" child_link="base_link"/>
  <disable_collisions link1="base_link" link2="link1" reason="Adjacent"/>
  <!-- the Self-Collisions pane writes the rest -->
</robot>
```

- **Chain groups** (`<chain>`) work with every IK plugin; KDL and TRAC-IK need a serial chain. Keep gripper
  joints out of `arm`, or MoveIt looks for one controller that drives both.
- **Virtual joint:** only when `base_link` must hang under a frame the URDF does not have; the generated
  `static_virtual_joint_tfs.launch.py` then publishes `world` → `base_link`. If the URDF already has `world`, skip
  it, or two nodes publish the same edge.
- **Self-collision matrix:** generate it with high sampling density. Every disabled pair is a pair MoveIt never
  checks, so review "Never in collision" pairs on arms that can fold back onto themselves.
- **Mimic and passive joints:** mimic joints follow their parent (list only the parent in poses); passive joints
  are never planned for but must still appear on `/joint_states`.

## kinematics.yaml

```yaml
arm:
  kinematics_solver: kdl_kinematics_plugin/KDLKinematicsPlugin
  kinematics_solver_timeout: 0.05            # s; Jazzy default 0.05
  kinematics_solver_search_resolution: 0.005 # Jazzy default 0.1; used for redundant joints
  # KDL only: position_only_ik (false), orientation_vs_position (1.0), max_solver_iterations (500), epsilon (1e-5)
```

`kinematics_solver_attempts`, still in many old configs, is not read by MoveIt 2. The gripper group gets no
entry. Other solvers: [ik-solvers.md](ik-solvers.md).

## joint_limits.yaml

```yaml
default_velocity_scaling_factor: 0.1      # generated value; MoveGroupInterface and RViz start from these
default_acceleration_scaling_factor: 0.1
joint_limits:
  joint1:
    has_velocity_limits: true
    max_velocity: 2.0          # placeholder: rad/s from the actuator datasheet, not above the URDF limit
    has_acceleration_limits: true
    max_acceleration: 3.0      # placeholder: rad/s^2 from the datasheet or a measured step response
    has_jerk_limits: false     # set true with max_jerk if you add the Ruckig smoothing adapter
  # one block per joint, gripper joints included
```

The Setup Assistant copies velocity limits from the URDF, but URDF cannot hold accelerations, so it writes
`has_acceleration_limits: false` and `max_acceleration: 0`. The default time parameterization (TOTG) then fails
every plan with `No acceleration limit was defined for joint ...`. Set an acceleration limit for every joint.
Position limits can be narrowed here with `has_position_limits`, `min_position`, `max_position`. Pilz also
accepts `has_deceleration_limits` / `max_deceleration` (negative); by default it uses `-max_acceleration`.

## moveit_controllers.yaml

```yaml
moveit_controller_manager: moveit_simple_controller_manager/MoveItSimpleControllerManager
moveit_simple_controller_manager:
  controller_names: [arm_controller, gripper_controller]
  arm_controller:
    type: FollowJointTrajectory
    action_ns: follow_joint_trajectory     # served as /arm_controller/follow_joint_trajectory
    default: true
    joints: [joint1, joint2, joint3, joint4, joint5, joint6]
  gripper_controller:                      # parallel_gripper_action_controller/GripperActionController
    type: ParallelGripperCommand           # MoveIt 2.12.2+; GripperCommand only for the deprecated gripper_controllers
    action_ns: gripper_cmd
    default: true
    joints: [left_finger_joint]
trajectory_execution:                       # optional; Jazzy code defaults shown
  allowed_execution_duration_scaling: 1.1   # cancel when execution exceeds expected time x this ...
  allowed_goal_duration_margin: 0.5         # ... plus this, in s
  allowed_start_tolerance: 0.01             # rad; first point vs current state; 0 disables the check
  execution_duration_monitoring: true
```

Controller names and joints must match `ros2_controllers.yaml` exactly. The gripper's `type` must match its
controller's action: `ParallelGripperCommand` for `parallel_gripper_action_controller` (the default; the older
`gripper_controllers` GripperActionController logs a deprecation warning on Jazzy and is not released on
Lyrical). On Jazzy the Setup Assistant's ROS 2 Controllers pane offers `parallel_gripper_action_controller`, but
its MoveIt Controllers pane offers only `FollowJointTrajectory` and `GripperCommand`: after generating, change the
gripper entry to `ParallelGripperCommand` by hand. The gripper controller's setup and limits are in
[manip-grasping](../../manip-grasping/references/gripper.md). To let MoveIt switch
ros2_control controllers itself, use `moveit_ros_control_interface/Ros2ControlManager` as the manager instead.

## ros2_controllers.yaml: what MoveIt relies on

The full controller file and the hardware tag are in [ros2-control](../../ros2-control/references/urdf-yaml-launch.md).
For MoveIt the arm's `joint_trajectory_controller` needs:

- `command_interfaces: [position]` (or velocity/effort with `gains`), `state_interfaces: [position, velocity]`.
- `constraints`: per-joint `trajectory` and `goal` tolerances (0.0, the default, disables the check),
  `stopped_velocity_tolerance` (0.01) and `goal_time` (0.0 waits forever; MoveIt's duration monitor still cancels).
- `allow_nonzero_velocity_at_trajectory_end: false` (Jazzy default). MoveIt plans end at rest; streaming
  sources such as Servo do not use the action, so leave it false unless a goal is rejected for that reason.

## ompl_planning.yaml (only to choose OMPL planners)

Without this file every request runs RRTConnect, whatever `planner_id` it names. Add it to `config/` to pick
planners per group; the builder then loads it instead of the default and still merges the global
`planner_configs` from `ompl_defaults.yaml` if you leave that key out.

```yaml
planning_plugins: [ompl_interface/OMPLPlanner]
request_adapters:
  - default_planning_request_adapters/ResolveConstraintFrames
  - default_planning_request_adapters/ValidateWorkspaceBounds
  - default_planning_request_adapters/CheckStartStateBounds
  - default_planning_request_adapters/CheckStartStateCollision
response_adapters:
  - default_planning_response_adapters/AddTimeOptimalParameterization
  - default_planning_response_adapters/ValidateSolution
  - default_planning_response_adapters/DisplayMotionPath
arm:
  default_planner_config: RRTConnect
  planner_configs: [RRTConnect, RRTstar, PRMstar, BiTRRT]   # ids from ompl_defaults.yaml, no "kConfigDefault"
  # projection_evaluator: joints(joint1,joint2)             # for constrained planning (planners.md)
  # enforce_constrained_state_space: true
```

## pilz_cartesian_limits.yaml

```yaml
cartesian_limits:
  max_trans_vel: 1.0     # m/s    generated values are generic; set them for your arm
  max_trans_acc: 2.25    # m/s^2
  max_trans_dec: -5.0    # m/s^2, negative
  max_rot_vel: 1.57      # rad/s
```

Used only by Pilz LIN and CIRC. An old `cartesian_limits.yaml` is not loaded (the builder only warns), so rename
it to `pilz_cartesian_limits.yaml`.

## Other files

- `sensors_3d.yaml` and octomap parameters: [perception.md](perception.md).
- `moveit_cpp.yaml` (MoveItPy only; the Setup Assistant does not write it): [moveit-py.md](moveit-py.md).
- `servo.yaml`: [servo.md](servo.md).
