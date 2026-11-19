---
type: tool
name: MAVROS
summary: MAVLink-to-ROS 2 bridge that turns a PX4, ArduPilot or other MAVLink flight controller into ROS 2 topics, services and parameters, converting NED to ENU and proxying a ground station.
tags: [mavros, mavlink, px4, ardupilot, drone, uav, offboard, geographiclib, companion-computer]
kind: library
area: ros2
support:
license: "BSD-3-Clause OR GPL-3.0-only OR LGPL-3.0-only"
links: {repo: "https://github.com/mavlink/mavros", docs: "https://mavros.readthedocs.io/en/latest/", site: }
version: {tested: , latest: "2.17.0", as_of: 2026-11-18}
platforms: [linux]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://index.ros.org/p/mavros/", title: "ROS Index: mavros versions per distro", accessed: 2026-11-18}
  - {url: "https://github.com/mavlink/mavros/blob/ros2/README.md", title: MAVROS README (ros2 branch), accessed: 2026-11-18}
  - {url: "https://github.com/mavlink/mavros/blob/ros2/docs/connection_urls.md", title: MAVROS connection URLs, accessed: 2026-11-18}
  - {url: "https://github.com/mavlink/mavros/blob/ros2/docs/frames.md", title: MAVROS coordinate frames, accessed: 2026-11-18}
  - {url: "https://github.com/mavlink/mavros/blob/ros2/docs/plugins/std/sys_status.md", title: MAVROS sys_status plugin reference, accessed: 2026-11-18}
  - {url: "https://docs.px4.io/main/en/ros2/user_guide.html", title: PX4 ROS 2 user guide, accessed: 2026-11-18}
  - {url: "https://docs.px4.io/main/en/flight_modes/offboard.html", title: PX4 Offboard mode, accessed: 2026-11-18}
  - {url: "https://github.com/ArduPilot/ardupilot/blob/master/Tools/ros2/README.md", title: ArduPilot ROS 2 packages README, accessed: 2026-11-18}
---

# MAVROS

MAVROS turns a MAVLink autopilot such as PX4 or ArduPilot into ROS 2 topics, services and
parameters, and can relay a ground station over the same link [2]. Builders run it on a companion
computer to give a drone, rover or boat ROS 2 autonomy without writing MAVLink code.

## When to use it

- **MAVROS** for ArduPilot or mixed autopilots, an existing MAVLink radio or ground station, or
  missions, parameters and modes as ROS services, with frames converted for you [2][4].
- **PX4's uXRCE-DDS bridge** (PX4 v1.14 on) when the autopilot is PX4: ROS 2 nodes reach PX4's
  uORB topics directly, but `px4_msgs` must match the firmware's messages (or run the Message
  Translation Node, v1.16 on), frames stay NED/FRD and subscribers need sensor-data QoS [6].
- **ArduPilot's AP_DDS** client with micro_ros_agent, built from source, for Humble or Jazzy [8].

## Setup

MAVROS 2.17.0 (2026-11-11) is released for Humble, Jazzy, Kilted, **Lyrical** and Rolling, all from
the `ros2` branch [1]. PX4 documents Jazzy (recommended) and Humble, ArduPilot Humble and Jazzy [6][8].

```bash
sudo apt install ros-jazzy-mavros
sudo /opt/ros/jazzy/lib/mavros/install_geographiclib_datasets.sh
ros2 launch mavros px4.launch fcu_url:=/dev/ttyACM0:57600                   # autopilot on USB
ros2 launch mavros apm.launch fcu_url:=udp://0.0.0.0:14555@127.0.0.1:14550  # local SITL over UDP
```

A URL reads `scheme://bind@remote`: the bind host defaults to all interfaces, the UDP remote is
updated from each incoming packet, and TCP defaults to port 5760 [3]. An agent checks the link with
`ros2 topic echo --once /mavros/state` (`connected`, `armed`, `mode`) and switches modes with
`ros2 service call /mavros/set_mode mavros_msgs/srv/SetMode "{custom_mode: 'GUIDED'}"` [5].

## Traps

- **GeographicLib datasets** are mandatory [2]; MAVROS uses the geoid for AMSL to WGS-84 altitude [4].
  `sudo ros2 run` often fails because sudo drops your sourced setup; call the script by path as above.
- **Frames.** MAVROS converts NED/FRD to ENU/FLU [4]; PX4's DDS topics stay NED/FRD and PX4 does
  not convert them [6]. Convert in one place only, or headings and altitudes flip.
- **Offboard needs a setpoint stream.** PX4 enters or stays in Offboard only with a continuous 2 Hz
  stream; over MAVLink the setpoints are that signal, and a gap past `COM_OF_LOSS_T` fails safe [7].
  Publish setpoints well above 2 Hz before calling `set_mode`, and keep publishing while in Offboard.
- **Silent or slow topics.** The FCU may not stream that message fast enough: raise it with
  `set_message_interval` or `set_stream_rate` [5], within the radio's bandwidth. `battery` and other
  sensor topics use the best-effort SensorDataQoS, so a reliable subscriber hears nothing [5].
- **`connected: false`.** Check the bind and remote ports [3] and that a ground station does not hold
  the same UDP port; let MAVROS relay to it with `gcs_url` instead [2].

## Alternatives

PX4: build Micro-XRCE-DDS-Agent (v2.4.3 for Jazzy) and run `MicroXRCEAgent udp4 -p 8888` [6].
ArduPilot: `ros2 run micro_ros_agent micro_ros_agent` with the AP_DDS client [8]. Web access to
MAVROS topics: [rosbridge_suite](rosbridge-suite.md).

## Sources

1. [ROS Index: mavros versions per distro](https://index.ros.org/p/mavros/), accessed 2026-11-18
2. [MAVROS README (ros2 branch)](https://github.com/mavlink/mavros/blob/ros2/README.md), accessed 2026-11-18
3. [MAVROS connection URLs](https://github.com/mavlink/mavros/blob/ros2/docs/connection_urls.md), accessed 2026-11-18
4. [MAVROS coordinate frames](https://github.com/mavlink/mavros/blob/ros2/docs/frames.md), accessed 2026-11-18
5. [MAVROS sys_status plugin reference](https://github.com/mavlink/mavros/blob/ros2/docs/plugins/std/sys_status.md), accessed 2026-11-18
6. [PX4 ROS 2 user guide](https://docs.px4.io/main/en/ros2/user_guide.html), accessed 2026-11-18
7. [PX4 Offboard mode](https://docs.px4.io/main/en/flight_modes/offboard.html), accessed 2026-11-18
8. [ArduPilot ROS 2 packages README](https://github.com/ArduPilot/ardupilot/blob/master/Tools/ros2/README.md), accessed 2026-11-18
