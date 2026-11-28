# A CiA 402 drive through ros2_canopen on Jazzy

Part of [fw-serial-can](../SKILL.md). Two CiA 402 servo drives (node IDs 2 and 3) under
ros2_control with `canopen_ros2_control/RobotSystem`, tried first against simulated drives on
`vcan0`. Checked against ros2_canopen 0.3.4 (the Jazzy binary; tag `0.3.4` of `master`): the manual
(configuration, CiA 402 driver, ros2_control interface), `canopen_ros2_control`, `canopen_402_driver`,
`lely_core_libraries` (cogen, CMake macros) and `canopen_tests`. Most packages and lely-core are
Apache-2.0, but `canopen_402_driver` is LGPL-3.0 by its LICENSE file while its sources carry
GPL-3.0-or-later headers: read [ros2_canopen](../../../wiki/software/ros2-canopen.md) before shipping.

## Install

```bash
sudo apt install ros-jazzy-canopen ros-jazzy-canopen-master-driver ros-jazzy-canopen-402-driver \
  ros-jazzy-canopen-ros2-control ros-jazzy-canopen-fake-slaves ros-jazzy-canopen-tests \
  ros-jazzy-ros2-control ros-jazzy-ros2-controllers ros-jazzy-xacro
```

The `canopen` metapackage does not pull in the master driver or the ros2_control plugin; name them.

## Configuration package

```text
my_robot_canopen/
  CMakeLists.txt
  package.xml                 # build_depend lely_core_libraries; exec_depend canopen_master_driver,
                              # canopen_402_driver, canopen_ros2_control, canopen_fake_slaves
  config/arm_sim/bus.yml      # simulated drives
  config/arm_sim/cia402_slave.eds   # copied from canopen_tests/config/robot_control (Apache-2.0)
  config/arm/bus.yml          # real drives
  config/arm/my_drive.eds     # the vendor's EDS file
```

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_canopen)
find_package(ament_cmake REQUIRED)
find_package(lely_core_libraries REQUIRED)
# Expands bus.yml (nodes + defaults), runs dcfgen, installs bus.yml, master.dcf and the .bin files
# to share/my_robot_canopen/config/<name>/
cogen_dcf(arm_sim)
cogen_dcf(arm)
ament_package()
```

## `bus.yml`

```yaml
# config/arm/bus.yml
options:
  dcf_path: "@BUS_CONFIG_PATH@"        # filled in by cogen_dcf

master:
  node_id: 1
  driver: "ros2_canopen::MasterDriver"
  package: "canopen_master_driver"
  baudrate: 500                        # kbit/s; must match can0 and every drive (default 1000)
  sync_period: 10000                   # us: SYNC at 100 Hz, the controller-manager rate
  heartbeat_producer: 100              # ms, example: the drives watch this

defaults:                              # copied into every node, REPLACING the node's own key
  dcf: "my_drive.eds"
  driver: "ros2_canopen::Cia402Driver"
  package: "canopen_402_driver"
  revision_number: 0                   # as in ros2_canopen's examples
  period: 10                           # ms, 402 state machine; like the SYNC period
  heartbeat_producer: 100              # ms: the master watches each drive
  heartbeat_consumer: true             # each drive watches the master's heartbeat
  position_mode: 1                     # 8 (cyclic synchronous) on drives whose 0x6502 lists it
  diagnostics: {enable: true, period: 1000}
  sdo:
    - {index: 0x6098, sub_index: 0, value: 0}     # homing method: none (if the drive accepts 0)
    - {index: 0x6081, sub_index: 0, value: 1000}  # profile velocity, device units: low for first runs
    - {index: 0x6083, sub_index: 0, value: 2000}  # profile acceleration, device units
  tpdo:
    1: {enabled: true, cob_id: "auto", transmission: 0x01,
        mapping: [{index: 0x6041, sub_index: 0}, {index: 0x6061, sub_index: 0}]}
    2: {enabled: true, cob_id: "auto", transmission: 0x01,
        mapping: [{index: 0x6064, sub_index: 0}, {index: 0x606C, sub_index: 0}]}
  rpdo:
    1: {enabled: true, cob_id: "auto",
        mapping: [{index: 0x6040, sub_index: 0}, {index: 0x6060, sub_index: 0}]}
    2: {enabled: true, cob_id: "auto", mapping: [{index: 0x607A, sub_index: 0}]}

nodes:
  joint_1:
    node_id: 2
    scale_pos_to_dev: 32594.9          # counts per rad: 4096 counts x 50:1 gear / (2 pi), example
    scale_pos_from_dev: 3.06796e-05    # rad per count, the inverse
    scale_vel_to_dev: 32594.9          # check the drive's velocity unit (counts/s, rpm ...)
    scale_vel_from_dev: 3.06796e-05
  joint_2:
    node_id: 3
    scale_pos_to_dev: 32594.9
    scale_pos_from_dev: 3.06796e-05
    scale_vel_to_dev: 32594.9
    scale_vel_from_dev: 3.06796e-05
```

`arm_sim/bus.yml` is the same with `dcf: "cia402_slave.eds"`, no scales and no
`heartbeat_consumer` (that test EDS has no 0x1016; a real drive's EDS must have it).
Rules from the source:

- With `cogen_dcf`, nodes sit under `nodes:` and every key in `defaults:` overwrites the same key
  in each node. Keep per-node values (scales, node IDs) out of `defaults`.
- Unset scales default to 1000 (to device) and 0.001 (from device): a 1 rad command becomes 1000
  counts. Set all of them for every drive.
- The RobotSystem plugin turns `position_mode`, `velocity_mode` and `effort_mode` into command
  interfaces (the manual's `torque_mode` is for the driver's own services).
- A drive's TPDOs must carry the statusword and the actual values, and its RPDOs the controlword,
  the mode and the target, or the 402 state machine waits forever.

## URDF

```xml
<!-- my_robot_description/urdf/my_robot.ros2_control.xacro (inside a macro with args bus, can) -->
<ros2_control name="my_robot_arm" type="system">
  <hardware>
    <plugin>canopen_ros2_control/RobotSystem</plugin>
    <param name="bus_config">$(find my_robot_canopen)/config/${bus}/bus.yml</param>
    <param name="master_config">$(find my_robot_canopen)/config/${bus}/master.dcf</param>
    <param name="can_interface_name">${can}</param>
  </hardware>
  <!-- device_name is the node's key in bus.yml; the plugin exports position, velocity and effort
       states and one command interface per *_mode key -->
  <joint name="joint_1">
    <param name="device_name">joint_1</param>
    <state_interface name="position"/>
  </joint>
  <joint name="joint_2">
    <param name="device_name">joint_2</param>
    <state_interface name="position"/>
  </joint>
</ros2_control>
```

The manual calls this plugin `Cia402RobotSystem` with a `node_id` per joint; the 0.3.4 code
registers `canopen_ros2_control/RobotSystem` and reads `device_name`. It works only with the
non-lifecycle `ros2_canopen::Cia402Driver`.

## Controllers and launch

```yaml
# my_robot_bringup/config/canopen_controllers.yaml
joint_state_broadcaster:
  ros__parameters:
    type: joint_state_broadcaster/JointStateBroadcaster
arm_position_controller:
  ros__parameters:
    type: forward_command_controller/ForwardCommandController
    joints: [joint_1, joint_2]
    interface_name: position
```

Launch as in [ros2-control urdf-yaml-launch.md](../../ros2-control/references/urdf-yaml-launch.md):
`robot_state_publisher`, `ros2_control_node` with `update_rate: 100`, one spawner with
`--param-file`. Two additions:

- Start the hardware inactive for the first real run, so states are read but drives stay off:
  `ros2_control_node` parameter `hardware_components_initial_state.inactive: [my_robot_arm]`. Spawn
  only the broadcaster then; the arm controller after activation, or with the spawner's `--inactive`.
- For `arm_sim`, include `canopen_fake_slaves`' `launch/cia402_slave.launch.py` once per drive
  with `node_id` (2, 3), `node_name`, `can_interface_name: vcan0` and `slave_config` pointing at
  `cia402_slave.eds` (`canopen_tests`' `robot_control_setup.launch.py` is the model).

## Bring-up order

1. **Simulated:** `vcan0` up ([can-linux.md](can-linux.md)), launch with `bus:=arm_sim can:=vcan0`.
   Check: `ros2 control list_hardware_components` shows `my_robot_arm` active, both controllers
   active; `ros2 topic pub --once /arm_position_controller/commands std_msgs/msg/Float64MultiArray
   "{data: [0.5, -0.5]}"` moves `/joint_states`.
2. **Real bus, no motion:** set each drive's node ID and bitrate with its vendor tool or LSS; check
   wiring ([wiring.md](wiring.md)); `python3 can_probe.py` shows nodes 2 and 3; read 0x1000 (profile
   402) and 0x6502 (supported modes) with `--sdo`.
3. **Real launch, inactive:** `bus:=arm can:=can0` with the initial state inactive. Turn each motor
   shaft by hand: one output revolution must move its joint by 2π rad with the URDF's sign.
4. **Enable:** axis clear, E-stop in reach, profile limits low:
   `ros2 control set_hardware_component_state my_robot_arm active`. Activation shuts down, switches
   on and enables each drive (torque on) and runs homing if 0x6098 is non-zero. Command small steps.
5. **Faults and link loss:** deactivating the component sends quick stop (0x605A decides what
   follows). `RobotSystem::read()` and `write()` return OK even when a drive is gone, so ros2_control
   does not notice: pull the CAN cable and confirm the drives react on their own (heartbeat consumer
   plus 0x6007), and watch the drivers' diagnostics on `/diagnostics`
   ([ops-bringup](../../ops-bringup/SKILL.md)).

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| Build fails in `cogen_dcf` | EDS not next to `bus.yml`, or a node key misspelt | Paths relative to `config/<name>/`; run `dcfgen` by hand to see the error |
| "Could not find driver for joint" | `device_name` differs from the node key, or the node never booted | Same names; `candump` for its boot-up heartbeat |
| Plugin or master class not found | Only `ros-jazzy-canopen` installed | Install the master driver and `canopen-ros2-control` packages |
| Drive stays in `Switch on disabled` | Missing PDO mapping, wrong mode, or a drive fault | Check TPDO/RPDO lists; read 0x6041 and the drive's error code by SDO |
| Hangs at activation | Homing running, or mode not in 0x6502 | Set 0x6098; pick a supported mode |
| Joint jumps on enable | Stale target in the drive | Profile modes with low 0x6081/0x6083; command the current position first |

Sources: ros2_canopen manual (installation, configuration, CiA 402 driver, ros2_control interface,
how to create a robot system); 0.3.4 sources: `canopen_ros2_control/src/robot_system.cpp` and
`include/canopen_ros2_control/cia402_data.hpp`, `canopen_402_driver/src/motor.cpp` and
`node_canopen_402_driver_impl.hpp` (scales, homing), `lely_core_libraries/cogen/cogen.py` and
`cmake/lely_core_libraries-extras.cmake`, `canopen_tests` configs and launch files; ros2_control
`jazzy` `controller_manager_parameters.yaml`; rosdistro `jazzy` (ros2_canopen 0.3.4-1).
