---
name: arch-safety
description: Plan and check the safety and security layers of a ROS 2 Jazzy robot - hardware E-stop chain and IEC 60204-1 stop categories,
  ISO 12100 risk assessment, ISO 10218 / 13849-1 / 13482 / 3691-4 by robot type, safety scanners, command timeouts, heartbeats, watchdogs,
  ros2_control and MoveIt limits, twist_mux locks, Nav2 collision monitor, SROS2 keystore, enclaves and permissions.
license: Apache-2.0
metadata:
  sources: [robotics-agent-skills]
  evidence: researched
  last_verified: 2026-11-25
---

# Robot safety and security layers

Lets an agent lay out what stops a ROS 2 robot and who may command it: the rated stop chain, the
standards and risk assessment that size it, the software layers that help, and SROS2. Checked against
Jazzy binaries on 2026-11-25 (ros2_control 4.50, ros2_controllers 4.43.1, Nav2 1.3.14, MoveIt 2.12.4,
twist_mux 4.5.0, sros2 0.13.6) and the official catalogues for standards; the recipes were not run.

> **Read first.** ROS 2, Linux and every recipe in this skill are **not safety-rated**. The safety
> function is carried by a hardware E-stop chain and certified safety components (safety relay or
> safety controller, drives with Safe Torque Off, safety laser scanners), and they must stop the
> robot with every computer switched off. Software layers make faults rarer and stops gentler; they
> never replace the chain. This skill is **not a substitute for a risk assessment by a qualified
> person**: it prepares the facts for one and builds the software around its result.

## When to use

- Planning or reviewing a robot's stop chain, E-stops, safety scanners and safety controller.
- Finding which standards apply (industrial arm, collaborative application, AMR, service robot) and
  preparing for a risk assessment.
- Adding command timeouts, heartbeats, a stop gate, limits, `twist_mux` locks or the Nav2 collision
  monitor, and proving that each one stops the robot.
- Securing ROS 2 traffic with SROS2: keystore, enclaves, policies, `Enforce`.
- Reviewing code or a design that claims to "make the robot safe" in software.

Elsewhere: arm force guard and grasp limits in [manip-grasping](../manip-grasping/SKILL.md); first
powered runs of a learned policy in [sim-to-real](../sim-to-real/SKILL.md); web bridge exposure in
[ros2-web-bridge](../ros2-web-bridge/references/secure-access.md); systemd units and boot order in
[ops-bringup](../ops-bringup/SKILL.md); networks and fleets in [ops-fleet](../ops-fleet/SKILL.md); the
overall node layout in [arch-robot-architecture](../arch-robot-architecture/SKILL.md); drive firmware,
motor control and firmware watchdogs in the later `fw-` skills (Phase 5).

## The layers

| Layer | Example | Rated? | Stops the robot if ROS is dead? |
|---|---|---|---|
| 1. Stop chain | E-stops → safety relay or controller → STO in each drive, or a contactor | Yes, when parts and design meet the PLr | Yes |
| 2. Protective devices | Safety scanner fields, light curtains, door switches → safety controller | Yes | Yes |
| 3. Drive and firmware | Drive current and speed limits, a command timeout in the motor board | Only if the drive function is rated | Yes, when it times out |
| 4. ros2_control | `cmd_vel_timeout`, `cmd_timeout`, `enforce_command_limits` | No | No |
| 5. Command chain | `twist_mux`, stop gate, velocity smoother, collision monitor, MoveIt Servo | No | No |
| 6. Supervision | Heartbeats, systemd `WatchdogSec=`, diagnostics | No | No |
| 7. Security | SROS2, closed bridge ports, network isolation | No | Keeps others out of layers 4 to 6 |

## Quick start

An audit of an existing robot, safest first:

```bash
# 1. Robot computer off: press each E-stop. Drives must lose torque. Release and reset: no motion.
# 2. Timeouts and limits that are on:
ros2 param get /diff_drive_controller cmd_vel_timeout       # Jazzy default 0.5 s; 0.0 disables
ros2 param get /controller_manager enforce_command_limits    # Jazzy default false
ros2 param get /collision_monitor source_timeout
# 3. Driving slowly, kill the command source (teleop, bridge, Nav2): the base stops within the timeout.
# 4. Who can command the robot?
ros2 topic info -v /cmd_vel                                  # every publisher should be expected
printenv | grep ROS_SECURITY      # run where the nodes run; unset means anyone on the domain can publish
```

Any "no" in steps 1 to 3 is a finding to fix before anyone works near the robot.

## Workflow

1. **Classify the robot and list the standards.** Industrial arm, arm application or cell,
   collaborative application, driverless truck or AMR, personal care or service robot: the type picks
   the product standard, which names the safety functions. ISO 10218-1/-2 moved to 2025 editions and
   absorbed the collaborative content of ISO/TS 15066; ISO 13482 has a second edition in publication.
   Editions, catalogue links and status: [references/standards.md](references/standards.md).
   *Check:* the project's safety file lists each standard with edition and the date its iso.org or
   iec.ch page was checked; nothing quotes a standard's text.

2. **Get the risk assessment done.** A qualified person leads it to ISO 12100; the builder brings
   masses, speeds, forces, modes, people, every life phase and measured stopping data. Each safety
   function comes back with its stop category and required performance level (PLr, ISO 13849-1) or
   SIL (IEC 62061). Inputs and outputs: [references/standards.md](references/standards.md).
   *Check:* every hazard has a measure and an owner, and no safety function is assigned to ROS,
   Linux or an unrated board.

3. **Build the stop chain in rated hardware.** E-stops and protective devices into a safety relay or
   controller, out to STO or a contactor, category 0 or 1 as assessed; brakes on axes that fall; a
   manual reset that never restarts motion. ROS reads the chain's status and may ask for a stop; it
   never resets or bypasses it. Shape, rules and tests: [references/stop-chain.md](references/stop-chain.md).
   *Check:* each E-stop removes torque with the computer off and again while ROS commands full speed;
   release and reset cause no motion.

4. **Let rated sensors guard people.** Safety scanner fields stop the robot through the safety
   controller. ROS drivers (`sick_safetyscanners2` 1.0.5, `sick_safevisionary_ros2`, `sicks300_ros2`
   on Jazzy) give the scan for navigation and logging only.
   *Check:* a body entering each protective field stops the robot with the ROS stack killed.

5. **Tell ROS about stops.** Publish the chain status latched on `/safety/chain_ok`; let the hardware
   interface return `DEACTIVATE` from `write()` when the drives report STO, so the controller manager
   deactivates the controllers. After a manual reset, reactivate with `ros2 control
   set_hardware_component_state` and `switch_controllers`; commands start at the measured state.
   [references/stop-chain.md](references/stop-chain.md).
   *Check:* `/safety/chain_ok` and `ros2 control list_controllers` follow each E-stop; after reset the
   robot stays still until a new command.

6. **Put a timeout on every command hop.** `diff_drive_controller` `cmd_vel_timeout`, JTC
   `cmd_timeout`, velocity smoother `velocity_timeout`, collision monitor `source_timeout`, `twist_mux`
   per-input `timeout`, Servo `incoming_command_timeout`, and a firmware timeout under all of them.
   Size each from the stopping budget. Table and YAML:
   [references/software-layers.md](references/software-layers.md).
   *Check:* killing each source mid-motion stops the robot within its timeout; times and distances are
   logged.

7. **Clamp commands where they are enforced.** URDF `<limit>` and `<safety_controller>` soft limits
   with `enforce_command_limits: true`; base controller and smoother limits; MoveIt joint limits and
   scaling; Servo margins. [references/software-layers.md](references/software-layers.md).
   *Check:* a command beyond each limit comes out clamped in `/joint_states` or odometry.

8. **Supervise with a stop gate.** One node forwards commands only while the chain is OK and every
   required heartbeat is fresh; otherwise it sends zero, holds a `twist_mux` lock and latches until
   `~/reset`. Heartbeats come from each critical node's main loop. Node, QoS deadline caveats and
   systemd watchdog: [references/watchdog-node.md](references/watchdog-node.md).
   *Check:* killing each monitored node stops the robot within the heartbeat timeout, and it stays
   stopped after the node respawns until reset.

9. **Keep the collision monitor as a convenience layer.** It stops or slows on scan points in
   polygons and on silent sources; its README says it gives no real-time safety certification. Configure it
   from [nav-nav2](../nav-nav2/references/params.md); restrict its `~/toggle` service with SROS2.
   *Check:* a box in the stop polygon halts the robot; a stopped scan driver halts it within
   `source_timeout`.

10. **Secure the graph with SROS2.** Keystore made offline with the runtime `ROS_DOMAIN_ID`, one
    enclave per process, a policy per enclave, `ROS_SECURITY_STRATEGY=Enforce`, and only `public/` and
    the robot's enclaves on the robot. Restrict who publishes the base command, calls reset, toggles
    the collision monitor, switches controllers and sets parameters.
    [references/sros2.md](references/sros2.md).
    *Check:* a process without keys fails to start under `Enforce`; one with security off sees
    nothing; `private/` is not on the robot.

11. **Test, record, repeat.** A fault-injection log: each E-stop, each protective field, each killed
    node and command source, each unplugged sensor, the network dropped, a rogue `/cmd_vel`, power
    cut to the computer. Run it before first motion, after every change to the chain or stack, and at
    the interval the assessment sets.
    *Check:* the log is committed with date, versions, parameter values and results; each failure has
    an issue.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| The "E-stop" is a topic or a button in a web page | A software stop dies with its process or link | Hardware chain; the topic only reports it |
| Robot moves when the E-stop is released or reset | Last command still active, or the code auto-resets | Latch in the stop gate; reset never restarts; commands resume from zero |
| Timeout never fires | `cmd_vel_timeout: 0.0`; JTC `cmd_timeout` 0 or not above `goal_time`; `twist_mux` `timeout: 0.0` | Set each, then test it |
| Timeout fires seconds late | Command stamps come from a clock ahead of the robot's | chrony on every machine; restamp at the robot (stop gate) |
| `twist_mux` lock engaged but the robot coasts | The mux stops forwarding; it never sends zero | Keep the controller timeout; the gate sends zero |
| Heartbeat subscriber receives nothing | Requested QoS deadline that the publisher does not offer; deadline unimplemented on `rmw_zenoh` | Age check in a timer, as in the stop gate |
| Linux watchdog reboots, the motors keep going | A reboot does not stop drives | Firmware or drive command timeout |
| `enforce_command_limits` cannot be set at run time | Read-only parameter | Put it in the controller manager YAML |
| Collision monitor does nothing | Toggled off, a source misnamed, or it sits before another publisher on `/cmd_vel` | `ros2 topic info -v /cmd_vel`; SROS2 on `~/toggle` |
| One process can still reach everything | `create_enclave` alone grants every topic | Generate permissions from a trimmed policy |
| Old snippets fail | `create_key`, `list_keys` (deprecated on Jazzy, removed from Kilted); launch has no `security` or `enclave` attribute | `create_enclave`, `list_enclaves`; `--enclave` via `ros_arguments` (XML: `ros_args`) |
| A table maps E-stop to PL e and SIL 3 | Invented: ISO 13849-1 leaves the PLr to the application | PLr from the risk assessment or the product standard |

## Checks

Before reporting a robot's safety and security layers done:

- Every E-stop and protective field stops the robot with the computer off and with ROS commanding
  motion; release and reset cause no motion; stopping times and distances are recorded.
- The risk assessment exists, names its assessor, and assigns no safety function to software.
- `ros2 param get` values for every timeout and limit match the safety file and the test log.
- Killing each command source and each monitored node stops the robot; the gate stays latched until
  reset.
- `ros2 topic info -v` shows only the expected publishers on each command topic.
- SROS2 runs with `Enforce`; an unkeyed process is refused; `private/` is off the robot.
- The safety file, parameters, policy and fault-injection log are committed in the project's repo.

## Distro differences

- **Lyrical** (ros2_control 6.x, Nav2 1.5, sros2 0.16): `enforce_command_limits` defaults to `true`;
  Nav2 sends `TwistStamped` by default (`enable_stamped_cmd_vel: true`); `create_key` and `list_keys`
  are gone (removed in Kilted). `twist_mux` 4.5.1 behaves the same.
- **Humble**: no `enforce_command_limits` in the controller manager (added for Jazzy);
  `diff_drive_controller` accepts plain `Twist` with `use_stamped_vel: false`; no `DEACTIVATE` return from
  hardware `write()`; rclpy event callbacks import from `rclpy.qos_event`.

## Related

- References: [standards.md](references/standards.md), [stop-chain.md](references/stop-chain.md),
  [software-layers.md](references/software-layers.md), [watchdog-node.md](references/watchdog-node.md),
  [sros2.md](references/sros2.md).
- Wiki: [SROS2](../../wiki/software/sros2.md), [ROS 2](../../wiki/tools/ros2.md),
  [ros2_control](../../wiki/software/ros2-control.md), [Nav2](../../wiki/software/nav2.md),
  [MoveIt 2](../../wiki/software/moveit2.md), [Fast DDS](../../wiki/software/fast-dds.md),
  [Cyclone DDS](../../wiki/software/cyclone-dds.md), [rmw_zenoh](../../wiki/software/rmw-zenoh.md),
  [rosbridge suite](../../wiki/software/rosbridge-suite.md), [Foxglove](../../wiki/tools/foxglove.md),
  [choose a ROS 2 middleware](../../wiki/guides/choose-a-ros2-middleware.md).
- Skills: [ros2-control](../ros2-control/SKILL.md), [nav-nav2](../nav-nav2/SKILL.md),
  [manip-moveit2](../manip-moveit2/SKILL.md), [manip-grasping](../manip-grasping/SKILL.md),
  [ros2-core](../ros2-core/SKILL.md), [ros2-web-bridge](../ros2-web-bridge/SKILL.md),
  [sim-to-real](../sim-to-real/SKILL.md), [ops-bringup](../ops-bringup/SKILL.md),
  [ops-fleet](../ops-fleet/SKILL.md), [ops-docker-ci](../ops-docker-ci/SKILL.md),
  [arch-robot-architecture](../arch-robot-architecture/SKILL.md); lifecycle stages in
  [playbooks](../../playbooks/README.md).
- Upstream: iso.org and webstore.iec.ch catalogue pages; A3's ISO 10218 FAQ; the `jazzy` branches of
  ros2_controllers, ros2_control, navigation2 (`nav2_collision_monitor/README.md`), moveit2
  (`moveit_servo/config/servo_parameters.yaml`), sros2, rmw_zenoh (`docs/design.md`,
  `zenoh_security_tools`); the ROS 2 Jazzy security tutorials and QoS concepts page.
