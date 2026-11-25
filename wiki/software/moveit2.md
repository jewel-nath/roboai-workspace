---
type: tool
name: MoveIt 2
summary: The standard ROS 2 motion-planning framework for arms; move_group with OMPL, Pilz, CHOMP and STOMP pipelines, IK plugins, collision checking, Servo jogging, a Python API and the Task Constructor. BSD-3-Clause, led by PickNik; binaries for Humble to Lyrical and Rolling.
tags: [moveit, moveit2, motion-planning, manipulation, arm, inverse-kinematics, collision-checking, ompl, pilz, chomp, stomp, servo, moveit-py, task-constructor, hybrid-planning, setup-assistant, ros2]
kind: framework
area: manip
support:
license: BSD-3-Clause
links: {repo: "https://github.com/moveit/moveit2", docs: "https://moveit.picknik.ai/main/", site: "https://moveit.ai"}
version: {tested: , latest: 2.15.3, as_of: 2026-11-25}
platforms: [linux, windows]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/moveit/moveit2/tree/jazzy", title: "moveit2 jazzy branch: LICENSE, package.xml files, moveit_configs_utils, ompl_interface, Servo, MoveItPy and Setup Assistant sources", accessed: 2026-11-25}
  - {url: "https://github.com/moveit/moveit2", title: "moveit2 repository: README branch policy, DISTRO_COMPAT_POLICY.md, MIGRATION.md, tags, issues and pull requests", accessed: 2026-11-25}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-25}
  - {url: "https://moveit.ai/install-moveit2/binary/", title: "MoveIt 2 Binary Install (Linux), with its linked Windows page", accessed: 2026-11-25}
  - {url: "https://moveit.ai/", title: "MoveIt home page: release versions, licence, PickNik", accessed: 2026-11-25}
  - {url: "https://github.com/moveit/moveit2_tutorials", title: "moveit2_tutorials repository: branches, AGENTS.md, Getting Started and tutorial sources", accessed: 2026-11-25}
  - {url: "https://moveit.picknik.ai/main/doc/examples/setup_assistant/setup_assistant_tutorial.html", title: "MoveIt docs: MoveIt Setup Assistant", accessed: 2026-11-25}
  - {url: "https://moveit.picknik.ai/main/doc/examples/motion_planning_python_api/motion_planning_python_api_tutorial.html", title: "MoveIt docs: Motion Planning Python API", accessed: 2026-11-25}
  - {url: "https://moveit.picknik.ai/main/doc/examples/realtime_servo/realtime_servo_tutorial.html", title: "MoveIt docs: Realtime Servo", accessed: 2026-11-25}
  - {url: "https://moveit.picknik.ai/main/doc/concepts/hybrid_planning/hybrid_planning.html", title: "MoveIt docs: Hybrid Planning", accessed: 2026-11-25}
  - {url: "https://github.com/moveit/moveit_resources/tree/ros2", title: "moveit_resources ros2 branch: panda_moveit_config", accessed: 2026-11-25}
  - {url: "https://github.com/moveit/moveit_task_constructor", title: "MoveIt Task Constructor repository: README, LICENSE, branches", accessed: 2026-11-25}
  - {url: "https://picknik.ai/pro", title: "PickNik: MoveIt Pro", accessed: 2026-11-25}
  - {url: "https://www.therobotreport.com/qualcomm-acquires-picknik-robotics-keep-moveit-open-source/", title: "The Robot Report: Qualcomm acquires PickNik Robotics, to keep MoveIt open source (2026-09-23)", accessed: 2026-11-25}
---

# MoveIt 2

MoveIt 2 plans collision-free motion for ROS 2 arms. It loads the robot from URDF and SRDF, solves
IK, checks collisions against a planning scene, plans with pluggable planners, adds timing, and
sends the trajectory to a controller [1][6]. Builders use it to reach poses or named states, plan
Cartesian paths, pick and place, and jog in real time. BSD-3-Clause [1]. PickNik leads it [2];
Qualcomm announced on 2026-09-23 that it is buying PickNik and will keep MoveIt open source [14];
moveit.ai now calls PickNik a Qualcomm company [5]. **Jazzy binary: 2.12.4** [3]. Active: eight
pull requests merged on 2026-11-23 and 24; 310 issues were open [2].

## When to use it

- **Use it** for any ROS 2 arm with a URDF, including dual arms and mobile manipulators [6]; the
  demo robot is the [Franka Panda](../robots/franka-panda.md) [11]. Pipelines [1]:
  [OMPL](ompl.md) (sampling planners, the default) for free space; Pilz for industrial PTP, LIN
  and CIRC moves; CHOMP or STOMP to optimise a smooth path. See
  [Choose an arm motion planner](../guides/choose-an-arm-motion-planner.md).
- **Add-ons:** Servo jogs the arm from velocity or pose commands [9]; the Task Constructor chains
  stages such as approach, grasp and lift [12]; hybrid planning pairs a global planner with a
  fast local planner that adapts the motion during execution [10].
- **Use something else** without ROS or for batch work in Python ([Drake](drake.md),
  [Robotics Toolbox for Python](robotics-toolbox-python.md)), for GPU planning in milliseconds
  ([cuRobo](curobo.md)), or for learned policies (ACT, Diffusion Policy).

## Setup

```bash
sudo apt install ros-jazzy-moveit ros-jazzy-moveit-py ros-jazzy-moveit-servo \
  ros-jazzy-moveit-resources-panda-moveit-config
ros2 launch moveit_resources_panda_moveit_config demo.launch.py   # Panda, mock hardware, RViz
```

| Distro (Ubuntu) | Release | Notes [2][3][4] |
|---|---|---|
| Humble (22.04) | 2.5.10 | Older pipeline parameters (see Traps) |
| **Jazzy (24.04)** | 2.12.4 (2025-12-05) | The `jazzy` branch has 25 unreleased commits since |
| Kilted (24.04) | 2.14.3 (2026-01-13) | Stable branch `kilted` |
| Lyrical (26.04) | 2.15.2 (2026-09-16) | Released from `main`; no `lyrical` branch yet |
| Rolling (26.04) | 2.15.3 (2026-11-18) | `main` |

`ros-jazzy-moveit` brings the core, the OMPL, Pilz, CHOMP and STOMP planners, the simple
controller manager and the Setup Assistant; `moveit_py`, `moveit_servo`,
`moveit_hybrid_planning` and `moveit_ros_perception` are separate [1]. The Task Constructor is
`ros-jazzy-moveit-task-constructor-core` 0.1.8 [3]. IK: KDL is the default [7]; pick_ik 1.1.2
and TRAC-IK 2.0.2 (`ros-jazzy-trac-ik-kinematics-plugin`) have Jazzy binaries [3]. The install
page recommends [Cyclone DDS](cyclone-dds.md) on every node [4]; Windows gets Humble through
RoboStack (`mamba install ros-humble-moveit`) [4]. A source build needs up to 16 GB of RAM for
some packages [6]. Nothing needs a GPU.

## How an agent works with it

The skill [skills/manip-moveit2/SKILL.md](../../skills/manip-moveit2/SKILL.md) covers bring-up.

**Config package.** The Setup Assistant (`ros2 launch moveit_setup_assistant
setup_assistant.launch.py`) is a GUI: it loads the URDF, samples a self-collision matrix (10,000
poses by default), and defines virtual joints, planning groups with an IK solver, named poses,
end effectors and controllers [7]. It writes `<robot>_moveit_config`: the SRDF, launch files and
`kinematics`, `joint_limits`, `*_planning`, `moveit_controllers` and `ros2_controllers` YAML
[1][7]. An agent can edit these directly; `panda_moveit_config` is a full reference [11].

**What MoveIt needs** [1][11]: the [URDF](urdf.md) on `robot_description`, the SRDF on
`robot_description_semantic`, `/joint_states` and [TF](tf2.md); and a `FollowJointTrajectory`
action server, usually [ros2_control](ros2-control.md)'s `joint_trajectory_controller`, named
in `moveit_controllers.yaml` with `action_ns: follow_joint_trajectory` and the same joints.

**Launch.** `MoveItConfigsBuilder("<robot>").to_moveit_configs().to_dict()` gives the
`move_group` node its parameters [1]. The default pipeline is `ompl` when present, and OMPL uses
RRTConnect unless a group sets `default_planner_config` [1]. `move_group` serves the
`move_action` and `execute_trajectory` actions and services such as `plan_kinematic_path`,
`compute_ik`, `compute_cartesian_path` and `get_planning_scene`; C++ nodes use
`MoveGroupInterface` [1][6].

**Python** with MoveItPy, which reads pipelines and `plan_request_params` from a MoveItCpp YAML [8]:

```python
from moveit.planning import MoveItPy
from moveit_configs_utils import MoveItConfigsBuilder
cfg = MoveItConfigsBuilder("moveit_resources_panda").moveit_cpp(
    file_path="config/moveit_py.yaml").to_moveit_configs()   # your pipelines file
robot = MoveItPy(node_name="moveit_py", config_dict=cfg.to_dict())
arm = robot.get_planning_component("panda_arm")
arm.set_start_state_to_current_state()
arm.set_goal_state(configuration_name="ready")
result = arm.plan()
if result:
    robot.execute(result.trajectory, controllers=[])
```

**Servo.** `servo_node` takes `JointJog` on `~/delta_joint_cmds`, `TwistStamped` on
`~/delta_twist_cmds` or `PoseStamped` on `~/pose_target_cmds`, and publishes a `JointTrajectory`
(default) or `Float64MultiArray` [1][9]. Choose the input with the `~/switch_command_type`
service (`moveit_msgs/srv/ServoCommandType`: 0 joint, 1 twist, 2 pose); `~/pause_servo` pauses
it and `~/status` reports singularity and collision slow-downs [9].

**Check:** in RViz's MotionPlanning panel, Plan then Execute moves the mock or
[Gazebo](../tools/gazebo.md) arm; `error_code.val` is 1 (SUCCESS); the controller is active.

## Traps

- **Very slow motion.** The Setup Assistant writes velocity and acceleration scaling of 0.1, and
  `MoveGroupInterface` and RViz fall back to 0.1 [1]. Raise them (up to 1.0) or set per request.
- **Planning fails after a path is found.** URDF has no acceleration limits, so time
  parameterisation stops with "No acceleration limit was defined for joint". Set
  `has_acceleration_limits: true` and `max_acceleration` per joint in `joint_limits.yaml` [1].
- **Plans but never moves.** Controller names and joints in `moveit_controllers.yaml` must match
  the running controller. Execution aborts if the start state is over `allowed_start_tolerance`
  (0.01) from the plan, or runs past 1.1 times the expected time plus 0.5 s [1][11]. Check
  `ros2 action list` for `.../follow_joint_trajectory`.
- **Always in collision.** A stale self-collision matrix after a URDF change, or a start state
  in collision, fails the `CheckStartStateCollision` adapter. Regenerate the matrix [1][7].
- **Humble configs on Jazzy.** `planning_plugin` became the list `planning_plugins`; request
  adapters split into `request_adapters` and `response_adapters` with new names; headers moved
  from `.h` to `.hpp` [2]. Start from the defaults in `moveit_configs_utils` [1].
- **Servo ignores input.** A command that does not match the selected type is dropped with
  "Command type has not been set"; twists need `header.frame_id`; commands older than
  `incoming_command_timeout` (0.1 s) are dropped [1][9].
- **Docs and binaries out of step.** The docs serve Rolling and Humble only [6]. Jazzy 2.12.4
  lacks fixes on the `jazzy` branch, such as MoveItPy releasing the GIL in `plan()` (other Python
  threads stall while it plans) [2]. Check APIs against that branch, and build it if needed.
- **No obstacles from the camera.** The point-cloud and depth octomap updaters live in
  `moveit_ros_perception`, which `ros-jazzy-moveit` leaves out; install it and add a
  `sensors_3d.yaml` [1]. See [OctoMap](octomap.md).
- **Open source versus Pro.** MoveIt Pro (formerly MoveIt Studio) is PickNik's separate,
  commercial platform with a behaviour-tree editor, extra planners and controllers, ML grasping
  and an MCP server [13][14]; none of it is in MoveIt 2.

## Alternatives

[OMPL](ompl.md) alone, [cuRobo](curobo.md) (GPU), [Drake](drake.md), [Pinocchio](pinocchio.md),
[Robotics Toolbox for Python](robotics-toolbox-python.md), MoveIt Pro (commercial).

## Sources

1. [moveit2 jazzy branch: LICENSE, package.xml files, moveit_configs_utils, ompl_interface, Servo, MoveItPy and Setup Assistant sources](https://github.com/moveit/moveit2/tree/jazzy), accessed 2026-11-25
2. [moveit2 repository: README branch policy, DISTRO_COMPAT_POLICY.md, MIGRATION.md, tags, issues and pull requests](https://github.com/moveit/moveit2), accessed 2026-11-25
3. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-25
4. [MoveIt 2 Binary Install (Linux), with its linked Windows page](https://moveit.ai/install-moveit2/binary/), accessed 2026-11-25
5. [MoveIt home page: release versions, licence, PickNik](https://moveit.ai/), accessed 2026-11-25
6. [moveit2_tutorials repository: branches, AGENTS.md, Getting Started and tutorial sources](https://github.com/moveit/moveit2_tutorials), accessed 2026-11-25
7. [MoveIt docs: MoveIt Setup Assistant](https://moveit.picknik.ai/main/doc/examples/setup_assistant/setup_assistant_tutorial.html), accessed 2026-11-25
8. [MoveIt docs: Motion Planning Python API](https://moveit.picknik.ai/main/doc/examples/motion_planning_python_api/motion_planning_python_api_tutorial.html), accessed 2026-11-25
9. [MoveIt docs: Realtime Servo](https://moveit.picknik.ai/main/doc/examples/realtime_servo/realtime_servo_tutorial.html), accessed 2026-11-25
10. [MoveIt docs: Hybrid Planning](https://moveit.picknik.ai/main/doc/concepts/hybrid_planning/hybrid_planning.html), accessed 2026-11-25
11. [moveit_resources ros2 branch: panda_moveit_config](https://github.com/moveit/moveit_resources/tree/ros2), accessed 2026-11-25
12. [MoveIt Task Constructor repository: README, LICENSE, branches](https://github.com/moveit/moveit_task_constructor), accessed 2026-11-25
13. [PickNik: MoveIt Pro](https://picknik.ai/pro), accessed 2026-11-25
14. [The Robot Report: Qualcomm acquires PickNik Robotics, to keep MoveIt open source (2026-09-23)](https://www.therobotreport.com/qualcomm-acquires-picknik-robotics-keep-moveit-open-source/), accessed 2026-11-25
