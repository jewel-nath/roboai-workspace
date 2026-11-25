---
name: manip-moveit2
description: Set up and use MoveIt 2 on ROS 2 Jazzy for a robot arm - Setup Assistant, my_robot_moveit_config (SRDF, kinematics.yaml,
  joint_limits.yaml, moveit_controllers.yaml, MoveItConfigsBuilder launch), joint_trajectory_controller, IK (KDL, TRAC-IK, pick_ik, IKFast),
  OMPL/Pilz/STOMP/CHOMP pipelines, planning scene, octomap, MoveGroupInterface, MoveItPy, Servo, Task Constructor, planning failures.
license: Apache-2.0
metadata:
  sources: []
  evidence: researched
  last_verified: 2026-11-25
---

# MoveIt 2 for a robot arm

Lets an agent take an arm with a working URDF and ros2_control setup and make it plan and move with MoveIt 2:
generate and fix the config package, launch it on mock hardware, in Gazebo and on the real arm, pick IK solvers
and planners, script motions, teleoperate with Servo, chain a pick with Task Constructor, and debug failures.
Written for Jazzy against MoveIt 2.12.4, ros2_controllers 4.43.1 and MoveIt Task Constructor 0.1.8 (the Jazzy
binaries on 2026-11-25); the recipes were not run. Lyrical and Humble differences are at the end.

## When to use

- Making `my_robot_moveit_config` with the Setup Assistant or by hand, and launching `move_group` with it.
- Choosing and configuring the IK solver and the planning pipelines; setting joint and Cartesian limits.
- Writing motion code: C++ `MoveGroupInterface`, Python MoveItPy, collision objects, Cartesian moves, constraints.
- Jogging or teleoperating with MoveIt Servo; multi-step pick and place with MoveIt Task Constructor (MTC).
- Debugging: no plan, IK fails, execution aborts, MoveIt cannot find the controller.

Elsewhere: grippers, grasp poses, hand-eye calibration, force-torque sensing and the pick sequence's checks in
[manip-grasping](../manip-grasping/SKILL.md); URDF, frames and collision meshes in
[ros2-robot-description](../ros2-robot-description/SKILL.md); hardware interfaces and controller basics in
[ros2-control](../ros2-control/SKILL.md); the simulated arm in [sim-gazebo](../sim-gazebo/SKILL.md); cameras in
[perception-camera](../perception-camera/SKILL.md); GPU or optimization planners outside MoveIt on the
[cuRobo](../../wiki/software/curobo.md) and [Drake](../../wiki/software/drake.md) pages.

## What MoveIt needs first

| Input | Usually from | Read by |
|---|---|---|
| URDF on `/robot_description`: collision geometry on every link, position and velocity limits, a tool frame `tool0` | `robot_state_publisher` | `move_group`, RViz, your nodes |
| `/joint_states` for every non-fixed joint, gripper and passive joints included | `joint_state_broadcaster` | the current-state monitor |
| TF from the planning frame to every link (plus `world` → `base_link` if the SRDF has a virtual joint) | `robot_state_publisher`, a static TF | the planning scene monitor |
| One `FollowJointTrajectory` action per arm | `joint_trajectory_controller` | trajectory execution |

## Quick start

```bash
sudo apt install ros-jazzy-moveit ros-jazzy-moveit-resources-panda-moveit-config
source /opt/ros/jazzy/setup.bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py   # mock arm + move_group + RViz
# In RViz: drag the marker, Plan, Execute
```

For your arm (package details in [references/config-package.md](references/config-package.md)):

```bash
ros2 launch moveit_setup_assistant setup_assistant.launch.py     # load my_robot_description's xacro; generate into src/
colcon build --packages-select my_robot_moveit_config && source install/setup.bash
ros2 launch my_robot_moveit_config demo.launch.py                 # mock_components arm, plan and execute in RViz
```

## Workflow

1. **Prove the description.** Collision geometry that is simple (boxes, cylinders or decimated meshes), joint
   limits that match the arm, and a `tool0` frame at the flange or tool centre point
   ([ros2-robot-description](../ros2-robot-description/SKILL.md)).
   *Check:* `check_urdf` passes on the expanded xacro; RViz shows collision and visual geometry aligned.

2. **Run the Setup Assistant.** Self-collision matrix at high sampling density; a fixed virtual joint only if
   `base_link` needs a parent frame the URDF lacks; groups `arm` (chain `base_link` → `tool0`, KDL) and `gripper`
   (links plus the finger joint, no solver); poses `home`, `ready`, `open`, `close`; end effector `gripper` on
   `tool0`; passive joints; ros2_control with position command and position+velocity state; a
   `joint_trajectory_controller` for `arm` and the gripper controller from
   [manip-grasping](../manip-grasping/references/gripper.md); untick the Warehouse DB launch on Jazzy.
   *Check:* `colcon build` passes; `demo.launch.py` plans and executes `home` in RViz.

3. **Fix the generated config.** Acceleration limits for every joint in `joint_limits.yaml` (generated as
   `false`, which fails every plan), default scaling (0.1), `package.xml` dependencies, the gripper entry in
   `moveit_controllers.yaml` (`ParallelGripperCommand`), and `ompl_planning.yaml` if you want planners other
   than RRTConnect. All in [references/config-package.md](references/config-package.md).
   *Check:* a plan at scaling 1.0 succeeds without `No acceleration limit was defined for joint`;
   `ros2 param get /move_group robot_description_planning.joint_limits.joint1.max_acceleration` is your value.

4. **Choose the IK solver.** KDL first; TRAC-IK when KDL fails near joint limits; IKFast for an analytic 6-DOF
   solver; pick_ik only for its cost functions (deprecated upstream). [references/ik-solvers.md](references/ik-solvers.md).
   *Check:* `/compute_ik` succeeds on 50+ reachable poses sampled from forward kinematics; the RViz marker
   tracks without flips.

5. **Choose pipelines.** OMPL for general moves, Pilz `PTP`/`LIN`/`CIRC` for predictable and straight moves,
   STOMP or CHOMP for smooth paths. Load only those you use. [references/planners.md](references/planners.md).
   *Check:* `/query_planner_interface` lists them; RViz plans with each in the Context tab.

6. **Write the bringup launch** for `hardware:=mock|gz|real`: `robot_state_publisher`, `ros2_control_node` (not
   in Gazebo), one spawner with `--param-file`, `move_group`, RViz. [references/launch.md](references/launch.md).
   *Check:* `ros2 control list_controllers` all active; `/arm_controller/follow_joint_trajectory` listed;
   `move_group` logs `You can start planning now!`.

7. **Simulate before hardware.** Same launch with `hardware:=gz use_sim_time:=true` and the Gazebo pieces
   from [sim-gazebo](../sim-gazebo/SKILL.md).
   *Check:* ten plans to poses across the workspace execute in Gazebo; `/joint_states` follows each trajectory.

8. **Build the planning scene.** Table, walls and fixtures as collision objects; an octomap from a calibrated
   camera if the workspace changes. [references/perception.md](references/perception.md).
   *Check:* RViz shows the scene where it really is; plans route around a test box; `/check_state_validity`
   flags a state touching it.

9. **Script the task.** C++: [references/move-group-interface.md](references/move-group-interface.md). Python:
   [references/moveit-py.md](references/moveit-py.md) (needs its own `moveit_cpp.yaml`).
   *Check:* named, joint, pose and Cartesian moves succeed in simulation; Cartesian paths return fraction 1.0.

10. **Move the real arm.** Velocity scaling 0.1 at first, an emergency stop in reach, JTC goal tolerances set,
    `allowed_start_tolerance` and execution-duration monitoring left on.
    *Check:* ten moves at low speed end within the JTC goal tolerances; no
    `start point deviates` or `taking too long` errors.

11. **Teleoperate or servo** with MoveIt Servo on the JTC topic, paused while plans execute.
    [references/servo.md](references/servo.md).
    *Check:* a twist in `base_link` moves `tool0` along that axis; it halts near a scene object (status 5).

12. **Chain a pick and place** with MTC (binaries on Jazzy; `move_group` needs the ExecuteTaskSolution
    capability). [references/task-constructor.md](references/task-constructor.md).
    *Check:* the task plans, the Motion Planning Tasks display shows the solution, and it executes in simulation.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| Every plan fails: `No acceleration limit was defined for joint ...` | Setup Assistant wrote `has_acceleration_limits: false` | Set acceleration limits for every joint |
| Robot crawls | Default scaling 0.1 from `joint_limits.yaml` | Raise per request or the default, after testing |
| MoveItPy moves at full speed | `plan_request_params` scaling defaults to 1.0 | Set it in `moveit_cpp.yaml` |
| `rosdep` cannot resolve `warehouse_ros_mongo` | Warehouse DB bundle; no Jazzy release | Untick it, or delete the dependency |
| `Unable to identify any set of controllers ...` | Names or joints differ between `moveit_controllers.yaml` and `ros2_controllers.yaml`, controller inactive, gripper joints in `arm` | Match them; separate groups |
| Gripper command fails at once | `type: GripperCommand` (Setup Assistant) against `parallel_gripper_action_controller` | `type: ParallelGripperCommand` |
| `START_STATE_IN_COLLISION` | Missing ACM entry, object overlapping the robot, attached part without touch links | `/check_state_validity`; Jazzy no longer nudges the start free |
| `planner_id` ignored, always RRTConnect | No per-group `planner_configs`; ids are `RRTConnect`, not `RRTConnectkConfigDefault` | Add `ompl_planning.yaml` |
| Old config keys do nothing or fail | `planning_plugin`, `default_planner_request_adapters/Fix...`, `kinematics_solver_attempts`, `lma_kinematics_plugin` | `planning_plugins` list, `request_adapters`/`response_adapters` lists, KDL or TRAC-IK |
| `.h header is obsolete` warnings | Pre-Jazzy include names | `.hpp` headers |
| `No kinematics plugins defined` from your node | Node lacks `robot_description_kinematics` | Pass it in the launch file |
| `Invalid Trajectory: start point deviates ...` | Arm sagged or moved after planning; stale `/joint_states` | Plan just before executing; fix holding |
| Cartesian path fraction below 1.0 | IK branch change, collision, unreachable waypoint, wrong reference frame | Smaller `eef_step`, check frames, or Pilz `LIN` |
| Plans pass through an object you added | Wrong `frame_id`, object added to a different scene (MoveItPy vs `move_group`) | Check in RViz; add through shared topics |
| Pilz LIN fails near obstacles | Pilz does not avoid obstacles | OMPL to a pre-pose, Pilz for the last straight part |
| Edited config has no effect | Config read from `install/` at launch | Rebuild, or `--symlink-install` |
| Servo does nothing | Wrong `command_out_topic`, command type not switched, stale `header.stamp`, paused | [references/servo.md](references/servo.md) |
| MTC executes nothing | `move_group` lacks `ExecuteTaskSolutionCapability` | Add the capability |

Error codes and messages in detail: [references/debugging.md](references/debugging.md).

## Checks

Before reporting MoveIt working on an arm:

- `move_group` starts without errors; `ros2 control list_controllers` shows every controller active.
- `/joint_states` lists every joint; `tf2_echo base_link tool0` matches the real tool position.
- IK success rate over sampled reachable poses is recorded for the chosen solver.
- Twenty plans across the workspace succeed and execute in simulation with the scene loaded, then at low
  speed on the arm within the JTC tolerances.
- A Cartesian approach of 5-10 cm returns fraction 1.0.
- Config package, bringup launch and the test script are committed with the results.

## Distro differences

- **Lyrical** (MoveIt 2.15, ros2_controllers 6.10, MTC 0.2.0, OMPL 2.0): the controller manager no longer
  forwards its parameter file to controllers, so spawners need `--param-file` (the generated launch adds it from
  2.15.2). `gripper_controllers` is not released: `ParallelGripperCommand` only. Pilz adds `POLYLINE`. MoveIt
  packages export only namespaced CMake targets (`ament_target_dependencies` removed from MoveIt itself).
- **Humble** (MoveIt 2.5): `.h` headers; pipeline YAML uses `planning_plugin: <name>`, a space-separated
  `request_adapters` string and `default_planner_request_adapters/...`, with `FixStartStateCollision` nudging
  the start state; no STOMP; `computeCartesianPath` needs a `jump_threshold` argument; MoveItPy
  `execute(group_name, trajectory, blocking=True)`; Servo's old API (`~/start_servo`, separate pose tracking);
  no `ParallelGripperCommand` (use `GripperCommand`); JTC `allow_nonzero_velocity_at_trajectory_end` defaults
  to `true`; MTC from the `humble` branch (0.1.3 binary).

## Related

- References: [config-package.md](references/config-package.md), [launch.md](references/launch.md),
  [ik-solvers.md](references/ik-solvers.md), [planners.md](references/planners.md),
  [move-group-interface.md](references/move-group-interface.md), [moveit-py.md](references/moveit-py.md),
  [servo.md](references/servo.md), [task-constructor.md](references/task-constructor.md),
  [perception.md](references/perception.md), [debugging.md](references/debugging.md).
- Wiki: [MoveIt 2](../../wiki/software/moveit2.md), [OMPL](../../wiki/software/ompl.md),
  [cuRobo](../../wiki/software/curobo.md), [Drake](../../wiki/software/drake.md),
  [Pinocchio](../../wiki/software/pinocchio.md), [Robotics Toolbox for Python](../../wiki/software/robotics-toolbox-python.md),
  [ros2_control](../../wiki/software/ros2-control.md), [URDF](../../wiki/software/urdf.md),
  [tf2](../../wiki/software/tf2.md), [OctoMap](../../wiki/software/octomap.md), [Gazebo](../../wiki/tools/gazebo.md),
  [choose an arm motion planner](../../wiki/guides/choose-an-arm-motion-planner.md).
- Arms that ship their own MoveIt config (check before running the Setup Assistant):
  [Universal Robots](../../wiki/robots/universal-robots.md), [Franka](../../wiki/robots/franka-panda.md),
  [Kinova Gen3](../../wiki/robots/kinova-gen3.md), [xArm](../../wiki/robots/ufactory-xarm.md).
- Skills: [manip-grasping](../manip-grasping/SKILL.md), [ros2-control](../ros2-control/SKILL.md),
  [ros2-robot-description](../ros2-robot-description/SKILL.md), [ros2-core](../ros2-core/SKILL.md),
  [sim-gazebo](../sim-gazebo/SKILL.md), [perception-camera](../perception-camera/SKILL.md),
  [sim-to-real](../sim-to-real/SKILL.md), [ops-docker-ci](../ops-docker-ci/SKILL.md); later `arch-safety`,
  `ops-bringup`, `learn-robot-learning` (learned policies instead of planned motions).
- Upstream: moveit.picknik.ai (`main` docs track Rolling; there is no Jazzy edition), the `moveit2` `jazzy`
  branch (`MIGRATION.md`, `moveit_configs_utils`), moveit2_tutorials, moveit_task_constructor, control.ros.org.
