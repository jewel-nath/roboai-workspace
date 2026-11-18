---
type: robot
name: TurtleBot (1, 2 and 4)
summary: The ROS reference robot line other than TurtleBot3; TurtleBot 1 (iRobot Create, 2010), TurtleBot 2 (Kobuki base, 2012) and the current TurtleBot 4 (iRobot Create 3 base, Clearpath, 2022), the stock ROS 2 robot for learning SLAM and Nav2.
tags: [ros2, differential-drive, create3, kobuki, raspberry-pi, lidar, oak-d, nav2, slam, clearpath, education]
category: mobile-base
tier: B
openness: partial
maker: Willow Garage (TurtleBot 1); Kobuki base by Yujin Robot (TurtleBot 2); Clearpath Robotics with Open Robotics (TurtleBot 4)
year: 2010
license: {hardware: , software: Apache-2.0, docs: }
links: {repo: "https://github.com/turtlebot/turtlebot4", docs: "https://turtlebot.github.io/turtlebot4-user-manual/", cad: "https://github.com/turtlebot/turtlebot4-hardware", paper: , site: "https://www.turtlebot.com/"}
specs: {dof: 2, payload_kg: 9, reach_mm: , mass_kg: 3.945, size_mm: "342 x 339 x 351", speed_mps: 0.46, runtime_h: 2.5}
stack: {actuators: "iRobot Create 3 two-wheel differential drive", mcu: "iRobot Create 3 base", compute: "Raspberry Pi 4B 4GB", sensors: ["RPLIDAR A1M8 2D lidar", "OAK-D-Pro stereo depth camera (OAK-D-Lite on the Lite)", "Create 3 base sensors"], sim_models: ["URDF/xacro (turtlebot4_description)", "Gazebo Harmonic on Jazzy, Ignition Fortress on Humble (turtlebot4_simulator)"], ros2: official}
cost: {type: retail, usd: 2708.00, as_of: 2026-11-18, source: "https://www.robotshop.com/products/clearpath-robotics-turtlebot-4-mobile-robot"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2025-09-09, stars: 168, active: false}
use_cases: [education, research, navigation, teleop]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://www.turtlebot.com/about/", title: "TurtleBot website: about and history", accessed: 2026-11-18}
  - {url: "https://turtlebot.github.io/turtlebot4-user-manual/overview/features.html", title: "TurtleBot 4 User Manual: features", accessed: 2026-11-18}
  - {url: "https://github.com/turtlebot/turtlebot4", title: "turtlebot4 repository (jazzy branch)", accessed: 2026-11-18}
  - {url: "https://turtlebot.github.io/turtlebot4-user-manual/software/turtlebot4_simulator.html", title: "TurtleBot 4 User Manual: turtlebot4_simulator", accessed: 2026-11-18}
  - {url: "https://github.com/turtlebot/turtlebot4-hardware", title: "turtlebot4-hardware repository", accessed: 2026-11-18}
  - {url: "https://store.clearpathrobotics.com/blogs/blog/clearpath-robotics-launches-turtlebot-4", title: "Clearpath Robotics: Clearpath Robotics launches TurtleBot 4 (2022)", accessed: 2026-11-18}
  - {url: "https://www.robotshop.com/products/clearpath-robotics-turtlebot-4-mobile-robot", title: "RobotShop US: Clearpath Robotics TurtleBot 4", accessed: 2026-11-18}
  - {url: "https://www.robotshop.com/products/clearpath-robotics-turtlebot-4-lite-mobile-robot", title: "RobotShop US: Clearpath Robotics TurtleBot 4 Lite", accessed: 2026-11-18}
  - {url: "https://github.com/kobuki-base/kobuki_ros", title: "kobuki_ros repository (Kobuki ROS 2 driver)", accessed: 2026-11-18}
  - {url: "https://iroboteducation.github.io/create3_docs/", title: "iRobot Create 3 documentation", accessed: 2026-11-18}
---

# TurtleBot (1, 2 and 4)

TurtleBot is the line of low-cost ROS reference robots begun at Willow Garage in November 2010 [1].
This card covers TurtleBot 1, 2 and 4; TurtleBot 4 was launched by Clearpath Robotics and Open Robotics
in May 2022 on the iRobot Create 3 base [1][6]. [TurtleBot3](turtlebot3.md) has its own page. TurtleBot 4
is the stock ROS 2 robot for learning SLAM and Nav2: sold assembled, with a Gazebo twin [3][4][7].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | TurtleBot 4 (Standard) | 2 |
| Drive | Create 3 base, differential drive (the Nav2 config uses a diff-drive model); `dof: 2` | 2, 3 |
| Size, mass | 342 x 339 x 351 mm, 3.945 kg; Lite 342 x 339 x 192 mm, 3.27 kg | 2 |
| Speed, payload | 0.31 m/s in safe mode, 0.46 m/s without it, 1.90 rad/s; 9 kg payload (maker's claims) | 2 |
| Battery, runtime | 26 Wh Li-ion at 14.4 V; 2.5 to 4 h by load; 2.5 h to charge (maker's claims) | 2 |
| Compute, sensors | Raspberry Pi 4B 4 GB; RPLIDAR A1M8 (12 m); OAK-D-Pro camera (Lite: OAK-D-Lite) | 2 |

## How it works

TurtleBot 4 puts a Raspberry Pi 4B, a 2D lidar and an OAK-D camera on an iRobot Create 3 education
base [2]. The Create 3 runs the motors and its own sensors, and its software is built on ROS 2, so it
publishes sensor data and takes commands over ROS 2 interfaces [10]. The `turtlebot4` repository adds
the description, messages, Nav2, SLAM and localization configs, and a node that drives the Standard's
buttons, LEDs and display; it has Galactic, Humble and Jazzy branches [3].

`turtlebot4_simulator` runs the robot in Ignition Fortress on Humble or Gazebo Harmonic on Jazzy, with
depot, maze and warehouse worlds [4]. TurtleBot 2 (October 2012) replaced TurtleBot 1's iRobot Create
with Yujin's Kobuki base and a charging dock [1]; the Kobuki driver has a ROS 2 port, `kobuki_ros` [9].

| Variant | Year | Base | Sensors | Computer | Source |
|---|---|---|---|---|---|
| TurtleBot 1 | 2010 | iRobot Create | Kinect | Asus 1215N laptop | 1 |
| TurtleBot 2 | 2012 | Yujin Kobuki | Kinect | Asus 1215N laptop | 1 |
| TurtleBot 4 Lite | 2022 | iRobot Create 3 | RPLIDAR A1M8, OAK-D-Lite | Raspberry Pi 4B | 2, 6 |
| TurtleBot 4 | 2022 | iRobot Create 3 | RPLIDAR A1M8, OAK-D-Pro | Raspberry Pi 4B | 2, 6 |

## What it is used for

- **Learning ROS 2 navigation:** Nav2, SLAM and localization launch files ship with the robot [3].
- **Simulation-first courses:** the Gazebo twin and its worlds run without the hardware [4].
- **Older labs:** Kobuki was built to the TurtleBot spec, ROS REP 119, and has a ROS 2 driver [9].

## Cost and BOM

| Item | Price (USD) | Type | Date | Source |
|---|---|---|---|---|
| TurtleBot 4 (Standard), RobotShop US | 2,708.00 | retail | 2026-11-18 | 7 |
| TurtleBot 4 Lite, RobotShop US | 1,647.00 | retail | 2026-11-18 | 8 |
| TurtleBot 4 Standard, launch price | from 1,850 | retail | 2022-05-04 | 6 |
| TurtleBot 4 Lite, launch price | 1,195 | retail | 2022-05-04 | 6 |

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| ROS 2 packages | ROS 2, URDF/xacro | [turtlebot4](https://github.com/turtlebot/turtlebot4) [3] | Apache-2.0 |
| Simulator | ROS 2, Gazebo | [turtlebot4_simulator](https://github.com/turtlebot/turtlebot4_simulator) [4] | Apache-2.0 |
| Mechanical parts, UI board | STEP, DXF, PDF drawings, PCB manufacturing zip | [turtlebot4-hardware](https://github.com/turtlebot/turtlebot4-hardware) [5] | None stated |
| Kobuki ROS 2 driver | ROS 2 | [kobuki_ros](https://github.com/kobuki-base/kobuki_ros) [9] | BSD (package.xml) |
| Create 3 base and firmware | | iRobot [10] | Closed |

## Strengths and limits

- **Strengths:** sold assembled with a lidar and a depth camera [2][7]; official ROS 2 packages and a
  Gazebo twin share one interface [3][4]; STEP and DXF drawings of plates and brackets help you add mounts [5].
- **Limits:** indoor and slow, 0.31 m/s by default [2]; the closed Create 3 base means no rebuild from
  open files, and the hardware files carry no licence [5][10]; the price rose from $1,850 to $2,708 [6][7].

## Related robots

- [TurtleBot3](turtlebot3.md): the ROBOTIS generation, with open chassis CAD and DYNAMIXEL wheels.
- [Clearpath robots](clearpath-robots.md): Clearpath's larger outdoor and indoor research bases.
- [F1TENTH](f1tenth.md): a faster ROS 2 learning platform built on an RC car.

## Sources

1. [TurtleBot website: about and history](https://www.turtlebot.com/about/), accessed 2026-11-18
2. [TurtleBot 4 User Manual: features](https://turtlebot.github.io/turtlebot4-user-manual/overview/features.html), accessed 2026-11-18
3. [turtlebot4 repository (jazzy branch)](https://github.com/turtlebot/turtlebot4), accessed 2026-11-18
4. [TurtleBot 4 User Manual: turtlebot4_simulator](https://turtlebot.github.io/turtlebot4-user-manual/software/turtlebot4_simulator.html), accessed 2026-11-18
5. [turtlebot4-hardware repository](https://github.com/turtlebot/turtlebot4-hardware), accessed 2026-11-18
6. [Clearpath Robotics: Clearpath Robotics launches TurtleBot 4 (2022)](https://store.clearpathrobotics.com/blogs/blog/clearpath-robotics-launches-turtlebot-4), accessed 2026-11-18
7. [RobotShop US: Clearpath Robotics TurtleBot 4](https://www.robotshop.com/products/clearpath-robotics-turtlebot-4-mobile-robot), accessed 2026-11-18
8. [RobotShop US: Clearpath Robotics TurtleBot 4 Lite](https://www.robotshop.com/products/clearpath-robotics-turtlebot-4-lite-mobile-robot), accessed 2026-11-18
9. [kobuki_ros repository (Kobuki ROS 2 driver)](https://github.com/kobuki-base/kobuki_ros), accessed 2026-11-18
10. [iRobot Create 3 documentation](https://iroboteducation.github.io/create3_docs/), accessed 2026-11-18
