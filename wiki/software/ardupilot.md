---
type: tool
name: ArduPilot
summary: GPL-3.0 autopilot firmware with stable Copter, Plane, Rover (ground vehicles and boats) and Sub builds; it talks MAVLink to ground stations and MAVROS, reaches ROS 2 through its AP_DDS client, and runs Lua scripts on the flight controller.
tags: [ardupilot, autopilot, flight-controller, arducopter, arduplane, rover, ardusub, boat, mavlink, ap-dds, micro-ros-agent, lua, sitl, mission-planner, mavproxy]
kind: framework
area: firmware
support:
license: GPL-3.0-or-later
links: {repo: "https://github.com/ArduPilot/ardupilot", docs: "https://ardupilot.org/dev/", site: "https://ardupilot.org"}
version: {tested: , latest: 4.7.3, as_of: 2026-11-27}
platforms: [linux, windows, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://github.com/ArduPilot/ardupilot", title: "ArduPilot repository: README, COPYING.txt, release tags and issues", accessed: 2026-11-27}
  - {url: "https://ardupilot.org/dev/docs/ros2-interfaces.html", title: "ArduPilot dev docs: ROS 2 interfaces", accessed: 2026-11-27}
  - {url: "https://github.com/ArduPilot/ardupilot/tree/master/Tools/ros2", title: "ArduPilot Tools/ros2: README, repos files and DDS default parameters", accessed: 2026-11-27}
  - {url: "https://ardupilot.org/dev/docs/ros2-pi.html", title: "ArduPilot dev docs: ROS 2 on Raspberry Pi", accessed: 2026-11-27}
  - {url: "https://github.com/ArduPilot/ardupilot/blob/Rover-4.7.3/Rover/ReleaseNotes.txt", title: "ArduPilot Rover release notes up to 4.7.3", accessed: 2026-11-27}
  - {url: "https://ardupilot.org/dev/docs/license-gplv3.html", title: "ArduPilot dev docs: GPLv3 licence overview", accessed: 2026-11-27}
  - {url: "https://ardupilot.org/copter/docs/common-lua-scripts.html", title: "ArduPilot docs: Lua scripts", accessed: 2026-11-27}
  - {url: "https://ardupilot.org/copter/docs/common-prearm-safety-checks.html", title: "ArduPilot docs: Pre-arm safety checks", accessed: 2026-11-27}
---

# ArduPilot

ArduPilot is flight-controller firmware built per vehicle: Copter (multirotors, helicopters), Plane
(quadplanes too), Rover (also boats), Sub and Antenna Tracker [1][5]. Licence: GPL-3.0-or-later [1].
Ship a modified build and you owe customers its source or a link and the credits, and consumer
products must let users load their own build; closed code may run on a companion computer [6].

## When to use it

- Ground and water robots on outdoor GNSS missions with RC override, failsafes and a ground
  station; ROS 2 joins through AP_DDS [2] or [MAVROS](mavros.md). Drones: it or [PX4](px4.md).
- Not indoor bases, arms or legged robots: write your own firmware ([micro-ROS](micro-ros.md),
  [ros2_control](ros2-control.md)); see [MCU guide](../guides/choose-an-mcu-and-firmware-stack.md).

**Maintenance.** The ArduPilot project, with per-area maintainers in its README and partner funding
[1]. 4.6.0 2025-05-21; 4.7.0 2026-07-21 after betas from March; 4.7.3 (2026-11-14) is stable for
Copter, Plane, Rover, Sub and Tracker [1][5]; `master` active on 2026-11-27, 1.7k issues open [1].

## Setup

ROS 2 and SITL on Ubuntu 24.04 with Jazzy, using the files in `Tools/ros2` [3]:

```bash
cd ~/ros2_ws/src && vcs import --recursive < ros2.jazzy.repos   # ArduPilot + micro-ROS-Agent
cd .. && rosdep install --from-paths src --ignore-src --skip-keys microxrcedds_agent
colcon build && source install/setup.bash      # needs microxrceddsgen on PATH
ros2 launch ardupilot_sitl sitl.launch.py command:=ardurover model:=rover
ros2 run micro_ros_agent micro_ros_agent serial -b 115200 -D /dev/ttyS0   # real board [4]
```

`sitl_dds_udp.launch.py` runs the agent, a DDS SITL copter and MAVProxy [3]. A real board needs a
custom DDS build on an H7 [4], `DDS_ENABLE 1`, `SERIALn_PROTOCOL 45` and the agent's baud [3][4].
Node `/ap` publishes `/ap/pose/filtered` and `/ap/twist/filtered` (ENU), takes `/ap/cmd_vel`, and
serves `/ap/arm_motors`, `/ap/mode_switch`, `/ap/prearm_check` and `ros2 param` [2]. Lua scripts
in `APM/scripts` (`SCR_ENABLE 1`) add drivers [7]; Mission Planner and MAVProxy are GCSs [6].

## Traps

- **ROS 2 distro.** The docs name Humble [2], as does the Pi guide [4]; the `Tools/ros2` README also
  names Jazzy and ships its repos file [3]. The docs lag the repo: test Jazzy before relying on it.
- **Board choice.** DDS needs an H7; F4 and F7 boards lack the CPU [4]. Lua needs 2 MB flash and
  about 80 kB RAM, and F4 boards have no scripting [7].
- **Parameter files across 4.7.** `ARMING_CHECK` became `ARMING_SKIPCHK`, `ANGLE_MAX` (centidegrees)
  `ATC_ANGLE_MAX` (degrees), `EK3_MAX_FLOW` `EK3_FLOW_MAX`; Copter distances moved to metres [5].
- **Arming refused.** The GCS shows each failure (calibration, compass near metal, GPS sky view,
  `AHRS: waiting for home`, battery failsafe levels) [8]. Skip checks only on the bench [8].
- **EKF and memory.** Without GPS the EKF needs an origin; 4.7 can reuse the last known one
  (`AHRS_ORIGIN_LAT/LON/ALT`) [5]. A script heap set too large can stop the EKF starting [7].

## Alternatives

[PX4](px4.md), [MAVROS](mavros.md), [micro-ROS](micro-ros.md); Betaflight, INAV (FPV craft).

## Sources

1. [ArduPilot repository: README, COPYING.txt, release tags and issues](https://github.com/ArduPilot/ardupilot), accessed 2026-11-27
2. [ArduPilot dev docs: ROS 2 interfaces](https://ardupilot.org/dev/docs/ros2-interfaces.html), accessed 2026-11-27
3. [ArduPilot Tools/ros2: README, repos files and DDS default parameters](https://github.com/ArduPilot/ardupilot/tree/master/Tools/ros2), accessed 2026-11-27
4. [ArduPilot dev docs: ROS 2 on Raspberry Pi](https://ardupilot.org/dev/docs/ros2-pi.html), accessed 2026-11-27
5. [ArduPilot Rover release notes up to 4.7.3](https://github.com/ArduPilot/ardupilot/blob/Rover-4.7.3/Rover/ReleaseNotes.txt), accessed 2026-11-27
6. [ArduPilot dev docs: GPLv3 licence overview](https://ardupilot.org/dev/docs/license-gplv3.html), accessed 2026-11-27
7. [ArduPilot docs: Lua scripts](https://ardupilot.org/copter/docs/common-lua-scripts.html), accessed 2026-11-27
8. [ArduPilot docs: Pre-arm safety checks](https://ardupilot.org/copter/docs/common-prearm-safety-checks.html), accessed 2026-11-27
