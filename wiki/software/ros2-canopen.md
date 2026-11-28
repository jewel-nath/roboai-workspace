---
type: tool
name: ros2_canopen
summary: ROS-Industrial's CANopen stack for ROS 2 on top of Lely CANopen; a master, proxy and CiA 402 drivers configured from a bus.yml with EDS/DCF files, and ros2_control system interfaces for CiA 402 motor drives; binaries for Humble, Jazzy, Kilted, Lyrical and Rolling.
tags: [ros2, canopen, cia402, ros2-control, lely, eds, dcf, motor-drive, socketcan, ros-industrial]
kind: library
area: firmware
support:
license: "Apache-2.0 AND LGPL-3.0-only"
links: {repo: "https://github.com/ros-industrial/ros2_canopen", docs: "https://ros-industrial.github.io/ros2_canopen/manual/rolling/", site: }
version: {tested: , latest: 0.3.4, as_of: 2026-11-27}
platforms: [linux]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://github.com/ros-industrial/ros2_canopen", title: "ros2_canopen README, LICENSE and package files, tests, changelog, branches and tags", accessed: 2026-11-27}
  - {url: "https://ros-industrial.github.io/ros2_canopen/manual/rolling/", title: "ros2_canopen manual (rolling): configuration, CiA 402 driver, CAN controller setup, robot system", accessed: 2026-11-27}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-27}
  - {url: "https://github.com/ros-industrial/ros2_canopen/issues", title: "ros2_canopen issue tracker (issues 448 and 463)", accessed: 2026-11-27}
  - {url: "https://gitlab.com/lely_industries/lely-core", title: lely-core repository, accessed: 2026-11-27}
---

# ros2_canopen

ros2_canopen runs a CANopen master in [ROS 2](../tools/ros2.md) on Lely's lely-core and SocketCAN
[1][5], with a proxy driver for CiA 301 devices, a CiA 402 drive driver and
[ros2_control](ros2-control.md) interfaces; its README says "not yet ready for production use" [1].
Apache-2.0, but `canopen_402_driver`'s LICENSE and package.xml say LGPL-3.0 while its headers say
GPL-3.0-or-later, and the ros2_control interfaces link it [1]: ask upstream before shipping it.

## When to use it

- CiA 402 drives (servo drives with an EDS file) as ros2_control joints; the manual covers a Pilz
  PRBT 6 arm and a Trinamic smart stepper [2]. Other CiA 301 devices go through the proxy driver.
- Node firmware: [CANopenNode](canopennode.md). Non-CANopen drives: [python-can](python-can.md).

## Setup

0.3.4 (2026-05-24) is released for Jazzy, Kilted, Lyrical and Rolling from `master`; Humble has
0.2.13 from `humble` [3][1]. Last commit 2026-11-27, by maintainers at Fraunhofer IPA and Stogl
Robotics; 93 issues are open, and most of the newest have no comments [1][4].

```bash
sudo apt install ros-jazzy-canopen ros-jazzy-canopen-ros2-control ros-jazzy-canopen-tests
sudo modprobe vcan && sudo ip link add dev vcan0 type vcan
sudo ip link set vcan0 txqueuelen 1000 && sudo ip link set up vcan0   # real bus: can-utils page
ros2 launch canopen_tests robot_control_setup.launch.py               # simulated CiA 402 slaves
```

A configuration package holds `config/<bus>/bus.yml` and EDS files; `cogen_dcf(<bus>)` in CMake
makes the DCFs with Lely's tools [2]. `canopen_core`'s `canopen.launch.py` and the ros2_control
plugins (`RobotSystem`, `Cia402System`, `CanopenSystem`) take `bus_config`, `master_config` and
`can_interface_name` [1][2]. A minimal `bus.yml`, after the upstream tests [1]:

```yaml
options: {dcf_path: "@BUS_CONFIG_PATH@"}
master: {node_id: 1, sync_period: 10000,              # sync in microseconds
         driver: "ros2_canopen::MasterDriver", package: "canopen_master_driver"}
nodes:                                                # URDF joints name these in device_name
  joint_1: {node_id: 2, dcf: "drive.eds", period: 10, # ms, near the sync period
            driver: "ros2_canopen::Cia402Driver", package: "canopen_402_driver"}
```

## Traps

- **Lyrical and ros2_control.** `canopen_ros2_control` fails to build against Lyrical's
  hardware_interface 6.13 (issue 463, open), and rosdistro's Lyrical entry no longer lists it
  [4][3]. Use Jazzy for CANopen joints in ros2_control.
- **Drive stays disabled or joints read zero.** Map status word 0x6041, mode display 0x6061,
  position and velocity to TPDOs; control word 0x6040, mode 0x6060 and targets to RPDOs [2].
- **Mixing drivers.** Lifecycle and simple drivers do not mix on one bus [2]; `RobotSystem` takes
  only nodes whose driver is exactly `ros2_canopen::Cia402Driver` (issue 448) [4][1].
- **Node IDs, bitrate, timeouts.** Give each node a unique `node_id`; set the master's `baudrate`
  (default 1000 kbit/s) to the `ip link` rate; raise `sdo_timeout_ms` (20 ms) for slow drives [2].
- **Source builds need gitlab.com:** `lely_core_libraries` fetches lely-core at a pinned commit
  while building [1][5]. Offline builders should use the binaries.

## Alternatives

[CANopenNode](canopennode.md)'s `canopend` master; Python `canopen` for tests; ROS 1 `ros_canopen`.

## Sources

1. [ros2_canopen README, LICENSE and package files, tests, changelog, branches and tags](https://github.com/ros-industrial/ros2_canopen), accessed 2026-11-27
2. [ros2_canopen manual (rolling): configuration, CiA 402 driver, CAN controller setup, robot system](https://ros-industrial.github.io/ros2_canopen/manual/rolling/), accessed 2026-11-27
3. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-27
4. [ros2_canopen issue tracker (issues 448 and 463)](https://github.com/ros-industrial/ros2_canopen/issues), accessed 2026-11-27
5. [lely-core repository](https://gitlab.com/lely_industries/lely-core), accessed 2026-11-27
