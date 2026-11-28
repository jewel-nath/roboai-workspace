---
type: tool
name: PX4
summary: BSD-3-Clause autopilot firmware for multicopters, fixed-wing and VTOL (rovers experimental) on Pixhawk-standard flight controllers, hosted by the Dronecode Foundation, with a uXRCE-DDS bridge that puts its uORB topics on ROS 2.
tags: [px4, autopilot, flight-controller, pixhawk, drone, uav, vtol, rover, uxrce-dds, px4-msgs, mavlink, qgroundcontrol, nuttx, sitl, dronecode]
kind: framework
area: firmware
support:
license: BSD-3-Clause
links: {repo: "https://github.com/PX4/PX4-Autopilot", docs: "https://docs.px4.io/main/en/", site: "https://px4.io"}
version: {tested: , latest: 1.18.0, as_of: 2026-11-27}
platforms: [linux, windows, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://github.com/PX4/PX4-Autopilot", title: "PX4-Autopilot repository: README, LICENSE, release tags and issues", accessed: 2026-11-27}
  - {url: "https://docs.px4.io/main/en/dev_setup/building_px4.html", title: "PX4 docs: Building PX4 software", accessed: 2026-11-27}
  - {url: "https://docs.px4.io/main/en/flight_controller/autopilot_pixhawk_standard.html", title: "PX4 docs: Pixhawk Standard autopilots", accessed: 2026-11-27}
  - {url: "https://docs.px4.io/main/en/ros2/user_guide.html", title: "PX4 docs: ROS 2 user guide", accessed: 2026-11-27}
  - {url: "https://docs.px4.io/main/en/middleware/uxrce_dds.html", title: "PX4 docs: uXRCE-DDS (PX4-ROS 2/DDS bridge)", accessed: 2026-11-27}
  - {url: "https://docs.px4.io/main/en/frames_rover/", title: "PX4 docs: Rovers", accessed: 2026-11-27}
  - {url: "https://docs.px4.io/main/en/flying/pre_flight_checks.html", title: "PX4 docs: Pre-flight checks", accessed: 2026-11-27}
  - {url: "https://docs.px4.io/main/en/releases/1.18.html", title: "PX4 docs: v1.18 release notes and upgrade guide", accessed: 2026-11-27}
---

# PX4

PX4 is flight-controller firmware for multicopters, fixed-wing and VTOL; rovers are experimental,
and boats and subs get basic support [1][6]. It runs on NuttX (Pixhawk boards) or Linux. Its code
is BSD-3-Clause, so a modified build may ship closed if it carries the copyright notice; NuttX and
other submodules keep their own licences [1], and each v1.18 build writes an SPDX SBOM [8].

## When to use it

- Drones and VTOL that need tested estimation, modes, missions and failsafes. ROS 2 reaches it over
  uXRCE-DDS [4] or MAVLink ([MAVROS](mavros.md)).
- Ground or water robots only for outdoor GNSS missions: the rover modules are experimental and not
  in the default firmware [6]; [ArduPilot](ardupilot.md) ships Rover as a stable vehicle. Indoor
  bases, arms and legged robots want their own firmware ([micro-ROS](micro-ros.md),
  [ros2_control](ros2-control.md)); see [MCU guide](../guides/choose-an-mcu-and-firmware-stack.md).

**Maintenance.** Hosted by the Dronecode Foundation [1]. v1.16.0 2025-08-06, v1.17.0 2026-05-13,
v1.18.0 2026-11-23; `main` had commits on 2026-11-27; 145 issues open, many awaiting triage [1].

## Setup

Jazzy on Ubuntu 24.04 is recommended, Humble on 22.04 the fallback [4]:

```bash
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
bash ./PX4-Autopilot/Tools/setup/ubuntu.sh
cd PX4-Autopilot && make px4_sitl gz_x500        # SITL quadcopter in Gazebo
make px4_fmu-v6x_default upload                  # build and flash a Pixhawk 6X over USB
```

ROS 2: build `px4_msgs` and Micro-XRCE-DDS-Agent v2.4.3 (v2.4.2 on Humble) from source, run
`MicroXRCEAgent udp4 -p 8888`, and `ros2 topic list` shows `/fmu/out/...`; SITL starts the client
[4]. On hardware set `UXRCE_DDS_CFG` and the port's baud; `dds_topics.yaml` lists the bridged
topics [5]. WSL2 builds but cannot upload [2].

## Traps

- **Versions must pair.** `px4_msgs` must match the firmware (tag `v1.18.0`) or the translation node
  must run [4][8]. Agent 2.4.x serves Humble to Kilted; Lyrical needs agent 3.0.2 and a PX4 build
  with Kconfig `UXRCE_DDS_CLIENT_USE_DDS_V3` [5]. Use sensor-data QoS; frames are NED/FRD [4].
- **Old parameter files.** v1.18 renamed or dropped many (`COM_RC_OVERRIDE` is `MAN_OVERRIDE_SPD`,
  `COM_FLTT_LOW_ACT` folds into `COM_LOW_BAT_ACT`) and changed failsafe exceptions in auto modes;
  run `Tools/migrate_param_file.py`, then recheck the failsafes [8].
- **Arming refused.** QGroundControl's Arming Check Report names the cause: often accel or gyro
  bias, sensors that disagree, or EKF innovations from magnetic interference [7]. Recalibrate.
- **Board choice.** Pixhawk Standard boards (6X, 6C, 5X) are tested by the PX4 maintainers and the
  Dronecode test team [3]. 1 MB `fmu-v2` builds overflow flash [2].
- **The bridge is unauthenticated** and writes into uORB: use a direct serial or Ethernet link [5].

## Alternatives

[ArduPilot](ardupilot.md), [MAVROS](mavros.md), [micro-ROS](micro-ros.md); Betaflight, INAV (FPV).

## Sources

1. [PX4-Autopilot repository: README, LICENSE, release tags and issues](https://github.com/PX4/PX4-Autopilot), accessed 2026-11-27
2. [PX4 docs: Building PX4 software](https://docs.px4.io/main/en/dev_setup/building_px4.html), accessed 2026-11-27
3. [PX4 docs: Pixhawk Standard autopilots](https://docs.px4.io/main/en/flight_controller/autopilot_pixhawk_standard.html), accessed 2026-11-27
4. [PX4 docs: ROS 2 user guide](https://docs.px4.io/main/en/ros2/user_guide.html), accessed 2026-11-27
5. [PX4 docs: uXRCE-DDS (PX4-ROS 2/DDS bridge)](https://docs.px4.io/main/en/middleware/uxrce_dds.html), accessed 2026-11-27
6. [PX4 docs: Rovers](https://docs.px4.io/main/en/frames_rover/), accessed 2026-11-27
7. [PX4 docs: Pre-flight checks](https://docs.px4.io/main/en/flying/pre_flight_checks.html), accessed 2026-11-27
8. [PX4 docs: v1.18 release notes and upgrade guide](https://docs.px4.io/main/en/releases/1.18.html), accessed 2026-11-27
