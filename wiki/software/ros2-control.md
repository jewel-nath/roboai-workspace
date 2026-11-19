---
type: tool
name: ros2_control
summary: The ROS 2 framework between controllers and robot hardware - a controller manager, hardware plugins and named command and state interfaces - so the same controllers drive mock, simulated and real joints.
tags: [ros2, control, controller-manager, hardware-interface, ros2-controllers, joint-trajectory-controller, diff-drive-controller, gz-ros2-control, mock-hardware, real-time]
kind: framework
area: control
support:
license: Apache-2.0
links: {repo: "https://github.com/ros-controls/ros2_control", docs: "https://control.ros.org/jazzy/index.html", site: "https://control.ros.org"}
version: {tested: , latest: 4.50.0, as_of: 2026-11-18}
platforms: [linux]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://control.ros.org/jazzy/doc/getting_started/getting_started.html", title: "ros2_control (Jazzy): Getting started", accessed: 2026-11-18}
  - {url: "https://github.com/ros-controls/ros2_control", title: ros2_control repository README and branch table, accessed: 2026-11-18}
  - {url: "https://control.ros.org/jazzy/doc/ros2_control/controller_manager/doc/userdoc.html", title: "Controller manager user documentation (Jazzy)", accessed: 2026-11-18}
  - {url: "https://control.ros.org/jazzy/doc/ros2_control/hardware_interface/doc/lifecycle_of_a_hardware_component.html", title: Lifecycle of a hardware component, accessed: 2026-11-18}
  - {url: "https://control.ros.org/jazzy/doc/ros2_control/hardware_interface/doc/mock_components_userdoc.html", title: Mock components, accessed: 2026-11-18}
  - {url: "https://control.ros.org/jazzy/doc/ros2_control/ros2controlcli/doc/userdoc.html", title: "ros2controlcli: the ros2 control command", accessed: 2026-11-18}
  - {url: "https://control.ros.org/jazzy/doc/ros2_controllers/doc/controllers_index.html", title: "ros2_controllers index (Jazzy)", accessed: 2026-11-18}
  - {url: "https://control.ros.org/jazzy/doc/ros2_control/doc/migration.html", title: "ros2_control migration guide: Humble to Jazzy", accessed: 2026-11-18}
  - {url: "https://control.ros.org/master/doc/ros2_control/doc/migration.html", title: "ros2_control migration guide and release notes: Kilted to Lyrical", accessed: 2026-11-18}
  - {url: "https://github.com/ros-controls/ros2_control/blob/jazzy/hardware_interface/CHANGELOG.rst", title: "hardware_interface changelog (jazzy branch)", accessed: 2026-11-18}
  - {url: "https://control.ros.org/jazzy/doc/ros2_controllers/doc/migration.html", title: "ros2_controllers migration guide: Humble to Jazzy", accessed: 2026-11-18}
  - {url: "https://control.ros.org/master/doc/ros2_controllers/doc/migration.html", title: "ros2_controllers migration guide: Kilted to Lyrical", accessed: 2026-11-18}
  - {url: "https://github.com/ros-controls/gz_ros2_control", title: gz_ros2_control README and documentation, accessed: 2026-11-18}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files (humble, jazzy, kilted, lyrical)", accessed: 2026-11-18}
---

# ros2_control

ros2_control sits between ROS 2 controllers and robot hardware. A controller manager runs one loop
that reads hardware state, updates the active controllers and writes commands; the hardware is
loaded as plugins described in the robot's URDF [1]. Builders use it to drive motors and read
sensors from ROS 2, and to swap real hardware for a mock or Gazebo without touching the controllers
[5][13]. Its companion repo, ros2_controllers, ships the common controllers [7].

## When to use it

- **Use it** for joint-level control from ROS 2: an arm under MoveIt 2, a wheeled base under Nav2
  (ros2_controllers is built for both [7]), a gripper; or to test the whole pipeline before the
  hardware exists, since the mock system mirrors commands to states [5].
- **Use something else** when an autopilot already closes the loop ([MAVROS](mavros.md)), or the
  stack never touches ROS (LeRobot drives the [SO-101](../robots/so-101.md)'s servos directly).
  Hardware components and controllers are C++ pluginlib plugins [1]: a cost for Python-only teams.

## Setup

Versions released per distro (Jazzy is this wiki's default) [14][13]:

| Distro | ros2_control | ros2_controllers | gz_ros2_control | Gazebo | Branch |
|---|---|---|---|---|---|
| Humble | 2.54.4 | 2.54.1 | 0.7.21 (`ign_ros2_control` repo entry) | Fortress | `humble` |
| **Jazzy** | **4.50.0** | **4.43.1** | **1.2.20** | **Harmonic** | `jazzy` |
| Kilted | 5.20.0 | 5.18.1 | 2.0.17 | Ionic | `kilted` |
| Lyrical | 6.13.0 | 6.10.1 | 3.0.9 | Jetty | `master` (shared with Rolling) |

Jazzy on Ubuntu 24.04 (RHEL uses `dnf` with the same names) [1][13]:

```bash
sudo apt install ros-jazzy-ros2-control ros-jazzy-ros2-controllers
sudo apt install ros-jazzy-gz-ros2-control   # only if you simulate in Gazebo Harmonic
```

- The docs list binaries for Ubuntu and RHEL only [1]; on Windows or macOS, build from source.
- From source: `vcs import` the repo's `ros2_control.jazzy.repos`, `rosdep install`, then
  `colcon build --symlink-install` [1][2]. The examples in ros2_control_demos are not released
  for Jazzy; build them from source too [14].
- **Real time:** the manager's main thread asks for `SCHED_FIFO` priority 50. Add your user to a
  `realtime` group with `rtprio 99` and `memlock unlimited` in `/etc/security/limits.conf`; in
  Docker pass `--cap-add=sys_nice --ulimit rtprio=99 --ulimit memlock=-1`. A real-time or
  low-latency kernel cuts jitter further [3].

## How an agent works with it

The skill [skills/ros2-control/SKILL.md](../../skills/ros2-control/SKILL.md) holds the recipes.
The pieces an agent writes are text files:

1. **The `<ros2_control>` tag** in the [URDF](urdf.md), usually a xacro macro. It names a hardware
   type (`system` for many joints on one bus, `actuator` for one joint, `sensor` for read-only
   devices), a `<plugin>`, its `<param>`s, and per joint the command and state interfaces [1]:

   ```xml
   <ros2_control name="arm" type="system">
     <hardware><plugin>mock_components/GenericSystem</plugin></hardware>
     <joint name="joint1">
       <command_interface name="position"/>
       <state_interface name="position"><param name="initial_value">0.0</param></state_interface>
       <state_interface name="velocity"/>
     </joint>
   </ros2_control>
   ```

   Make the plugin a xacro argument so one file serves the mock, `gz_ros2_control/GazeboSimSystem`
   and the real driver [5][13].
2. **A controllers YAML.** Under `controller_manager: ros__parameters:` set the loop's
   `update_rate` (Hz) and each controller's `type`, such as
   `joint_trajectory_controller/JointTrajectoryController`; each controller's parameters go under
   its own name. A controller without its own `update_rate` runs at the manager's rate [3][7].
3. **A launch file:** `robot_state_publisher` publishes `/robot_description`, which the controller
   manager (`ros2_control_node`) subscribes to; then one `spawner` per controller [3]:

   ```bash
   ros2 run controller_manager spawner joint_state_broadcaster arm_controller \
     --param-file config/controllers.yaml
   ```

**Check the result** with `ros2 control` [6]: `list_hardware_components` (with lifecycle states),
`list_hardware_interfaces` (claimed or available), `list_controllers`, `view_controller_chains`,
and `set_controller_state <name> active`; then echo `/joint_states`, filled by the broadcaster.

**Lifecycle.** Hardware and controllers move through unconfigured, inactive, active and finalized.
A hardware `on_configure` opens communication; `on_activate` powers the drives [4]. Commands are
still written while a component is inactive, so `write()` must ignore them itself [4].

**Controllers in Jazzy** [7]: wheeled bases (diff drive, mecanum, omni wheel, tricycle, and the
steering library for Ackermann, bicycle and tricycle); arms (joint trajectory, forward command,
admittance, PID, GPIO, parallel gripper, motion primitives); broadcasters (joint state, IMU, force
torque, range, pose, GPS, battery, magnetometer, any state interface); a chainable filter.

## Traps

- **Old tutorials, new distro.** Much online material targets Humble. Since Jazzy, the controller
  manager takes the URDF from the `/robot_description` topic (the `description` parameter is gone),
  and controller parameters loaded only into the controller manager node no longer reach the
  controllers: pass them with the spawner's `--param-file` [8].
- **"Not found in URDF".** Every joint in the `<ros2_control>` tag must exist in the URDF, and mimic
  joints are declared with the URDF `<mimic>` tag, not ros2_control parameters [8].
- **diff_drive_controller ignores your teleop.** Since Jazzy `~/cmd_vel` must be
  `geometry_msgs/TwistStamped` [11]. A plain `Twist` publisher is a different type and nothing
  moves; switch the publisher to stamped messages.
- **Hardware API drift.** Jazzy can already build a component's interfaces from the URDF tag [8],
  and `on_init(const HardwareComponentInterfaceParams &)` arrived in hardware_interface 4.34.0,
  deprecating `on_init(const HardwareInfo &)` [10]. Lyrical removes the old `on_init` and
  `export_state_interfaces()` / `export_command_interfaces()`; use `set_state()` and `get_command()`.
  Mark old methods `override` first, or they compile, are never called, and interfaces vanish [9].
- **Lyrical behaviour changes** [9][12]: `set_value(0)` on a double interface throws at run time
  (`0` is an int; write `0.0`); remaps given to the controller manager no longer reach controllers
  (use the spawner's `--controller-ros-args`); joint_trajectory_controller's
  `constraints.goal_time` defaults to 10 s and 0.0 now means "no grace period" (negative means
  "wait forever"); the `JointGroup*Controller`s give way to forward_command_controller.
- **No priority, silent jitter.** Users may not set real-time priorities by default, so without
  the `realtime` limits the loop cannot get its priority, and a stock kernel adds jitter. Keep
  `get_lifecycle_state()` out of the real-time loop [3].
- **Two controller managers in Gazebo.** The gz_ros2_control plugin starts its own controller
  manager inside Gazebo [13]; do not also launch `ros2_control_node`, and run every node with
  `use_sim_time: true`.
- **Mock is ideal.** `mock_components/GenericSystem` copies commands straight to states [5], so
  gains tuned against it mean nothing; use `disable_commands` or `position_state_following_offset`
  to test failure and lag paths [5].

## Alternatives

- A plain driver node that takes commands and publishes `/joint_states` and [tf2](tf2.md)
  frames: simpler for one actuator, but no controller reuse. micro-ROS when the loop closes on an
  MCU.
- [MAVROS](mavros.md) for PX4 and ArduPilot vehicles, whose autopilot runs the control loops.
- gazebo_ros2_control, the Gazebo Classic counterpart, is released for Humble but not for Jazzy,
  Kilted or Lyrical [14].

## Sources

1. [ros2_control (Jazzy): Getting started](https://control.ros.org/jazzy/doc/getting_started/getting_started.html), accessed 2026-11-18
2. [ros2_control repository README and branch table](https://github.com/ros-controls/ros2_control), accessed 2026-11-18
3. [Controller manager user documentation (Jazzy)](https://control.ros.org/jazzy/doc/ros2_control/controller_manager/doc/userdoc.html), accessed 2026-11-18
4. [Lifecycle of a hardware component](https://control.ros.org/jazzy/doc/ros2_control/hardware_interface/doc/lifecycle_of_a_hardware_component.html), accessed 2026-11-18
5. [Mock components](https://control.ros.org/jazzy/doc/ros2_control/hardware_interface/doc/mock_components_userdoc.html), accessed 2026-11-18
6. [ros2controlcli: the ros2 control command](https://control.ros.org/jazzy/doc/ros2_control/ros2controlcli/doc/userdoc.html), accessed 2026-11-18
7. [ros2_controllers index (Jazzy)](https://control.ros.org/jazzy/doc/ros2_controllers/doc/controllers_index.html), accessed 2026-11-18
8. [ros2_control migration guide: Humble to Jazzy](https://control.ros.org/jazzy/doc/ros2_control/doc/migration.html), accessed 2026-11-18
9. [ros2_control migration guide and release notes: Kilted to Lyrical](https://control.ros.org/master/doc/ros2_control/doc/migration.html), accessed 2026-11-18
10. [hardware_interface changelog (jazzy branch)](https://github.com/ros-controls/ros2_control/blob/jazzy/hardware_interface/CHANGELOG.rst), accessed 2026-11-18
11. [ros2_controllers migration guide: Humble to Jazzy](https://control.ros.org/jazzy/doc/ros2_controllers/doc/migration.html), accessed 2026-11-18
12. [ros2_controllers migration guide: Kilted to Lyrical](https://control.ros.org/master/doc/ros2_controllers/doc/migration.html), accessed 2026-11-18
13. [gz_ros2_control README and documentation](https://github.com/ros-controls/gz_ros2_control), accessed 2026-11-18
14. [rosdistro distribution files (humble, jazzy, kilted, lyrical)](https://github.com/ros/rosdistro), accessed 2026-11-18
