---
name: arch-robot-architecture
description: Structure a ROS 2 Jazzy robot's software - package layout (my_robot_description, _bringup, _interfaces, _hardware), layers from
  MCU firmware and ros2_control up to behavior and operator UI, components vs processes, lifecycle manager, topics/services/actions and QoS,
  behavior trees vs state machines (BehaviorTree.CPP, YASMIN, SMACC2, FlexBE), TF and estimation ownership, multi-robot namespaces.
license: Apache-2.0
metadata:
  sources: [robotics-agent-skills]
  evidence: researched
  last_verified: 2026-11-25
---

# Robot software architecture

Lets an agent lay out a robot's ROS 2 software, or review a layout: packages, layers, the microcontroller split,
processes and start-up, interfaces, and where mission logic lives. Written for ROS 2 Jazzy against rclcpp 28.1,
launch_ros 0.26.13, Nav2 1.3.14 and BehaviorTree.CPP 4.11.1 (the Jazzy binaries on 2026-11-25); the recipes were
not run. Lyrical and Humble differences are at the end.

## When to use

- Starting a robot's software: packages, layers, the computer and microcontroller split.
- Adding a capability (a sensor, an arm, docking, a mission): which package and layer, which interfaces.
- Choosing processes or components, lifecycle nodes and who starts them; topics, services, actions, QoS.
- Choosing the mission logic (behavior tree or state machine); TF ownership; namespaces for several robots.
- Reviewing a design: god nodes, two publishers of one transform, absolute names, a mission node on the motors.

Elsewhere: node, launch, QoS and lifecycle API detail in [ros2-core](../ros2-core/SKILL.md); hardware interfaces
and controllers in [ros2-control](../ros2-control/SKILL.md); URDF and frames in
[ros2-robot-description](../ros2-robot-description/SKILL.md); EKF setup in [perception-slam](../perception-slam/SKILL.md);
Nav2's own trees in [nav-nav2](../nav-nav2/SKILL.md); e-stops, watchdogs and safety layers in
[arch-safety](../arch-safety/SKILL.md); boot and systemd in [ops-bringup](../ops-bringup/SKILL.md); fleets in
[ops-fleet](../ops-fleet/SKILL.md).

## Quick start

The default package set; add only what the robot needs. Contents, dependency rules and the top-level launch
file: [references/packages-launch.md](references/packages-launch.md).

```text
src/
  my_robot_description/    URDF/xacro, meshes, RViz config            model
  my_robot_interfaces/     msg/ srv/ action/ only                     contracts between packages
  my_robot_hardware/       ros2_control hardware interface (C++)      drivers
  my_robot_bringup/        launch/ and config/, no nodes              start-up
  my_robot_localization/   EKF config and launch                      estimation
  my_robot_perception/     perception nodes                           perception
  my_robot_navigation/     Nav2 parameters, maps, BT XML              planning
  my_robot_behavior/       mission tree or state machine              behavior
```

```bash
colcon list --topological-order      # dependencies before the packages using them
colcon graph                         # no cycles; nothing depends on my_robot_bringup
ros2 launch my_robot_bringup robot.launch.py hardware:=mock map:=$HOME/maps/my_map.yaml
```

## Workflow

1. **Draw the system before the packages.** Sensors, actuators, computer, microcontrollers and their links (USB,
   UART, CAN, Ethernet); then the capabilities ("dock", "pick a box"), each an action that one layer serves.
   *Check:* every actuator has one command path, every sensor one driver, every capability one owning package.

2. **Split the computer and the microcontrollers.**

   | Runs on | Work | Why there |
   |---|---|---|
   | MCU or motor driver | PWM, commutation, current and velocity loops, encoder counting, a command timeout that stops the motors, the hardware e-stop chain | Hard timing that must hold when Linux stalls |
   | Computer, `ros2_control_node` | controllers (`diff_drive_controller`, `joint_trajectory_controller`), joint state, the hardware interface's read and write at `update_rate` | One control loop, with the standard controllers Nav2 and MoveIt expect |
   | Computer, other processes | camera and lidar drivers, estimation, perception, planning, behavior, operator UI | Throughput, not hard deadlines |

   Link them with a ros2_control hardware interface speaking a small serial, CAN or EtherCAT protocol to the MCU
   when standard controllers should drive the joints ([ros2-control](../ros2-control/SKILL.md)); or with
   micro-ROS (rclc on the MCU; the agent has no Jazzy apt package, build its `jazzy` branch) when the MCU should
   publish sensors or take `cmd_vel` itself, as [linorobot2](../../wiki/software/linorobot2.md) does. Firmware,
   micro-ROS and motor control are Phase 5 (`fw-mcu`, `fw-serial-can`, `fw-rtos-micro-ros`, `fw-motor-control`).
   *Check:* with the wheels off the ground, cutting the computer's link stops the motors on the MCU's timeout.

3. **Lay out the packages** (Quick start). Definitions alone in `my_robot_interfaces`; launch and config, no nodes,
   in `my_robot_bringup`; dependencies point down the layers, nothing depends on bringup. Drivers, controllers and
   high-rate pipelines in C++ (composable, fit for the control loop); behavior, tools and UI glue may be Python.
   Build files: [ros2-core](../ros2-core/references/packages.md).
   *Check:* `colcon graph` shows no cycles; a clean workspace builds after `rosdep install --from-paths src -i -y`.

4. **Give every node one layer.** A layer uses the one below only through its ROS interfaces; only drivers open
   devices; one node, one job.

   | Layer | Typical nodes | Serves the layer above with |
   |---|---|---|
   | Drivers | ros2_control hardware interface, camera and lidar drivers | `/joint_states`, sensor topics |
   | Control | `controller_manager` and its controllers | `odom`, `cmd_vel` (`TwistStamped`), `FollowJointTrajectory` |
   | Estimation | `robot_state_publisher`, robot_localization EKF, AMCL or slam_toolbox | TF, `odometry/filtered` |
   | Perception | filters, detectors, mapping | obstacles, detections, maps |
   | Planning | Nav2, MoveIt 2 | `NavigateToPose`, MoveIt's `MoveGroup` and other actions |
   | Behavior | a mission tree or state machine | a mission action, the robot's mode |
   | Operator interface | rosbridge or Foxglove bridge, RViz, diagnostics monitor | (people) |

   Safety cuts across all layers ([arch-safety](../arch-safety/SKILL.md)). Velocity sources (Nav2, teleop,
   behavior) meet in one arbiter before the base: `twist_mux` (Apache-2.0; Jazzy's 4.5.0 publishes `TwistStamped`
   on `cmd_vel_out` unless `use_stamped: false`). The operator UI ([ros2-web-bridge](../ros2-web-bridge/SKILL.md))
   calls the behavior layer, not Nav2.
   *Check:* `ros2 node info /<node>` shows each node's clients and publishers reaching only the layer below;
   the base controller's command topic has one publisher.

5. **Fix who owns each transform and estimate.** Each frame has one parent and each edge one publisher (REP 105).

   | Transform | Owner: exactly one of | Turn the others off with |
   |---|---|---|
   | `map` → `odom` | AMCL, slam_toolbox, or a global EKF | AMCL `tf_broadcast: false`; EKF `publish_tf: false` |
   | `odom` → `base_link` | `diff_drive_controller` (wheel odometry), or a local EKF fusing it with the IMU | controller `enable_odom_tf: false`; EKF `publish_tf: false` |
   | `base_link` → sensors and joints | `robot_state_publisher`, from the URDF and `/joint_states` | calibrated mounts go in the URDF, not in extra static publishers |

   Perception and planning read the pose from TF or `odometry/filtered`, never integrate their own. EKF files:
   [perception-slam](../perception-slam/SKILL.md); frames: [frames.md](../ros2-robot-description/references/frames.md).
   *Check:* `ros2 run tf2_tools view_frames` shows one tree, `map` → `odom` → `base_link` → sensors;
   `ros2 topic info -v /tf` lists only the owners in the table; `ros2 param get` confirms each off switch.

6. **Design the interfaces.** Topic for streams and state; service for a call that returns at once; action for
   anything that takes time, reports progress or must be cancellable; parameter for configuration. Standard types
   first, custom ones in `my_robot_interfaces`, typed (never `std_msgs/String` commands); relative names; QoS per
   kind of data; sensor data stamped at capture, `frame_id` in TF. Tables: [references/interfaces.md](references/interfaces.md).
   *Check:* `ros2 interface show` prints each custom type; `ros2 topic info -v` shows compatible QoS on both
   ends; no topic name in node code starts with `/`.

7. **Choose the process layout.** Components (C++ only) share a container and can pass messages without copying;
   processes isolate faults and restart alone. Own process (`respawn=True` where a restart is safe) for nodes on
   hardware that can hang, Python nodes and `ros2_control_node`; a container for C++ pipelines moving images or
   clouds and for groups of small nodes like Nav2's servers. A crash ends every component in its container.
   Launch files: [references/lifecycle-composition.md](references/lifecycle-composition.md).
   *Check:* `ros2 component list` shows each container's components; killing one driver leaves the rest running.

8. **Order start-up with lifecycle nodes.** Drivers, and anything that must start after something else, are
   lifecycle nodes: configure opens and checks, activate starts data. Drive them with `autostart=True` in launch
   (no order, no monitoring), `nav2_lifecycle_manager` with a `node_names` list (in order, reverse on shutdown;
   with bonds the group goes down when one node dies), or your own supervisor calling `change_state`. Details:
   [references/lifecycle-composition.md](references/lifecycle-composition.md); boot: [ops-bringup](../ops-bringup/SKILL.md).
   *Check:* `ros2 lifecycle get /<node>` is `active [3]` for every managed node; each lifecycle manager logs
   `Managed nodes are active`.

9. **Pick the behavior layer.** A behavior tree when the robot must keep checking conditions while it acts
   (battery, a new goal, a blocked path) and missions reuse steps; a state machine for a few explicit modes
   (manual, autonomous, docking, fault) that operators watch; often a mode machine on top, a tree inside, Nav2's
   tree below. It calls actions and services below, never a device or the velocity topic; halting a step cancels
   its goal. Jazzy apt: BehaviorTree.CPP (MIT; Groot2 editor closed-source, large-tree monitoring paid),
   py_trees_ros (BSD), YASMIN (Apache-2.0), SMACC2 (Apache-2.0), FlexBE (BSD-3-Clause), SMACH (BSD). Versions,
   choice table, examples: [references/behavior-layer.md](references/behavior-layer.md).
   *Check:* cancelling the mission stops the robot through the planning layer; a failed condition preempts
   the running step within one tick.

10. **Report health.** Each driver reports through `diagnostic_updater`; `diagnostic_aggregator` groups them on
    `/diagnostics_agg` for the operator (rqt_robot_monitor, Foxglove). Code: [references/interfaces.md](references/interfaces.md).
    *Check:* `ros2 topic echo /diagnostics_agg --once` lists every driver; unplugging a sensor turns its entry
    to ERROR or stale.

11. **Namespace for more than one robot.** Nodes under `/robot_01`, `/robot_02`; relative names; parameter files
    keyed `/**/node_name:`; one TF tree per robot (Nav2's way), frame prefixes on one shared tree, or a ROS domain
    per robot. Launch, ros2_control, Nav2, diagnostics: [references/multi-robot.md](references/multi-robot.md).
    *Check:* with two robots in simulation, `ros2 node list` shows each node once under its namespace and each
    robot's TF tree is complete on its own.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| A fault in logging or the web server stops the motors | God node: one process owns the port, SLAM, planning and HTTP | Split by layer; one node, one job |
| Mission ignores obstacle stops, or fails only on the real robot | Behavior node opens the motor port or publishes the base's velocity topic | Call planning actions; any direct motion goes through the arbiter |
| Robot jumps between two poses | Controller and EKF (or AMCL and SLAM) both publish one edge | One owner per edge (step 5) |
| A mistyped mode is silently ignored; a late node never learns the mode | `std_msgs/String` events | Typed message with constants, latched; commands as services or actions |
| Topics collide or vanish once a namespace is added | Absolute names (`/state`) in node code | Relative names; remap in launch |
| Parameters silently ignored after namespacing | YAML key `controller_server:` matches only `/controller_server` | `/**/controller_server:`, or rewrite under the namespace as Nav2 does |
| `robot_01/odom` → `robot_01/base_link` beside an unprefixed URDF tree | Jazzy `diff_drive_controller` prefixes frames with its namespace by default | `tf_frame_prefix_enable: false`, or prefix every frame the same way |
| `Server <node> was unable to be reached after 4.00s by bond` | `nav2_lifecycle_manager` waits for a bond your node never makes | Bond from the node (`nav2_util::LifecycleNode`), or `bond_timeout: 0.0` |
| A driver sometimes configures before what it needs is ready | `autostart=True` on several nodes: no order between them | One lifecycle manager with an ordered `node_names` |
| A camera driver crash also kills the detector | They share a container | Own process for the crash-prone driver |
| A Python node cannot be loaded into a container | rclpy has no components | Run it as its own process |
| Mission node freezes; Nav2 feedback stops arriving | `tickWhileRunning()` or a blocking call inside a callback | `tickOnce()` from a timer; asynchronous calls in a `StatefulActionNode` |
| State machine with dozens of states and hundreds of transitions | Every mode and task combination spelled out | Modes, then tasks inside them; or a behavior tree |
| Every robot's diagnostics mixed in one view | `diagnostic_updater` and the aggregator use absolute `/diagnostics` | Remap per robot, or `diagnostic_updater.use_fqn: true` |
| Nav2 nodes appear as `/robot_01/robot_01/...` | Nav2's bringup pushed into a namespace a second time | Include it outside your namespace group and pass `namespace` |

## Checks

Before reporting an architecture done:

- The block diagram and layer table exist; every node has one layer and one package; `colcon graph` is clean.
- `view_frames` shows one tree; `ros2 topic info -v /tf` shows only the planned owners.
- Custom types print with `ros2 interface show`; no `std_msgs/String` commands; no absolute names in node code.
- Every managed node is `active`; killing one driver leaves other processes running and its group reacts as designed.
- The mission can be cancelled and preempted; the base's command topic has one publisher; `/diagnostics_agg`
  covers every driver.
- With several robots, two run side by side in simulation and share only the topics chosen to share.

## Distro differences

- **Lyrical**: `component_container_mt` and `_isolated` are deprecated (removal in the next distro); use
  `component_container --executor-type multi-threaded` and `--isolated`. Nav2's lifecycle base class is
  `nav2::LifecycleNode` in `nav2_ros_common`, and its bringup drops `use_namespace`. `diff_drive_controller`
  deprecates `tf_frame_prefix_enable`; `tf_frame_prefix` takes `~` for the namespace. SMACC2 has no Lyrical
  release; FlexBE's Lyrical engine (4.1.4) works with the FlexBE WebUI.
- **Humble**: launch_ros has no `autostart` or `ComposableLifecycleNode` (Jazzy got both in 0.26.7) and spells it
  `PushRosNamespace` (Jazzy accepts both); `IncludeLaunchDescription` needs a `PythonLaunchDescriptionSource`.
  Nav2 uses BehaviorTree.CPP v3. FlexBE 2.3.5 pairs with the FlexBE App.

## Related

- References: [packages-launch.md](references/packages-launch.md), [interfaces.md](references/interfaces.md),
  [lifecycle-composition.md](references/lifecycle-composition.md), [behavior-layer.md](references/behavior-layer.md),
  [multi-robot.md](references/multi-robot.md).
- Wiki: [ROS 2](../../wiki/tools/ros2.md), [ros2_control](../../wiki/software/ros2-control.md),
  [Nav2](../../wiki/software/nav2.md), [BehaviorTree.CPP](../../wiki/software/behaviortree-cpp.md),
  [robot_localization](../../wiki/software/robot-localization.md), [tf2](../../wiki/software/tf2.md),
  [rosbridge_suite](../../wiki/software/rosbridge-suite.md), [Foxglove](../../wiki/tools/foxglove.md),
  [Open-RMF](../../wiki/software/open-rmf.md), [choose a middleware](../../wiki/guides/choose-a-ros2-middleware.md).
- Skills: those named above, plus [manip-moveit2](../manip-moveit2/SKILL.md), [sim-gazebo](../sim-gazebo/SKILL.md),
  [ops-docker-ci](../ops-docker-ci/SKILL.md); Phase 5 `fw-` skills. Stage 2 of the [playbooks](../../playbooks/README.md).
- Upstream: docs.ros.org/en/jazzy (composition, launch for large projects, node arguments), REP 105, REP 144,
  `navigation2`, `launch_ros`, `rclcpp`, `ros2_controllers` `jazzy` branches, behaviortree.dev, the YASMIN, SMACC2
  and FlexBE repositories, `ros/rosdistro`.
