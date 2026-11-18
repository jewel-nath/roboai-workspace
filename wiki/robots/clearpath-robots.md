---
type: robot
name: Clearpath research bases (Husky, Jackal, Dingo, Ridgeback, Boxer)
summary: Rugged research mobile bases from Clearpath Robotics, part of Rockwell Automation since 2023; the outdoor Husky (now the A300) and Jackal, the indoor Dingo and the mecanum Ridgeback, with an official BSD-3 ROS 2 stack and Gazebo models.
tags: [ros2, ugv, skid-steer, mecanum, husky, jackal, dingo, ridgeback, boxer, warthog, gazebo, mobile-manipulation, commercial]
category: mobile-base
tier: B
openness: software-only
maker: Clearpath Robotics (Rockwell Automation since 2023)
year:
license: {hardware: , software: BSD-3-Clause, docs: }
links: {repo: "https://github.com/clearpathrobotics/clearpath_common", docs: "https://docs.clearpathrobotics.com/docs/ros/", cad: , paper: , site: "https://clearpathrobotics.com/"}
specs: {dof: 4, payload_kg: 100, reach_mm: , mass_kg: 80, size_mm: "990 x 698 x 372", speed_mps: 2.0, runtime_h: 4}
stack: {actuators: "four brushless motors, skid steer (Husky A300)", mcu: , compute: "Intel Core i3-13100TE (standard) or i7-13700TE (performance) PC, GPU optional", sensors: ["wheel odometry", "motor current and battery monitoring", "e-stop status"], sim_models: ["URDF/xacro for A200, A300, J100, Dingo-D and -O, R100, W200 (clearpath_common)", "Gazebo (clearpath_simulator)"], ros2: official}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-11-09, stars: 64, active: true}
use_cases: [research, navigation, manipulation, teleop, data-collection]
evidence: vendor-claim
last_verified: 2026-11-18
sources:
  - {url: "https://clearpathrobotics.com/husky-spec-comparison/", title: "Clearpath: Husky A300 vs A200 spec comparison", accessed: 2026-11-18}
  - {url: "https://clearpathrobotics.com/husky-a300-unmanned-ground-vehicle-robot/", title: "Clearpath: Husky A300 product page", accessed: 2026-11-18}
  - {url: "https://clearpathrobotics.com/", title: "Clearpath Robotics home page (product line-up)", accessed: 2026-11-18}
  - {url: "https://logisticsbusiness.com/materials-handling-warehousing/agv-amr-robots/rockwell-completes-acquisition-of-clearpath-robotics/", title: "Logistics Business: Rockwell completes acquisition of Clearpath Robotics (2023-10-03)", accessed: 2026-11-18}
  - {url: "https://github.com/clearpathrobotics/clearpath_common", title: "clearpath_common repository (jazzy branch)", accessed: 2026-11-18}
  - {url: "https://clearpathrobotics.com/jackal-small-unmanned-ground-vehicle/", title: "Clearpath: Jackal product page", accessed: 2026-11-18}
  - {url: "https://clearpathrobotics.com/dingo-indoor-mobile-robot/", title: "Clearpath: Dingo product page", accessed: 2026-11-18}
  - {url: "https://clearpathrobotics.com/ridgeback-indoor-robot-platform/", title: "Clearpath: Ridgeback product page", accessed: 2026-11-18}
  - {url: "https://docs.clearpathrobotics.com/docs_robots/indoor_robots/boxer/user_manual_boxer", title: "Clearpath docs: Boxer user manual", accessed: 2026-11-18}
  - {url: "https://clearpathrobotics.com/assets/guides/indigo/husky/HuskyDualManip.html", title: "Clearpath: Husky dual UR5 mobile manipulation demo (ROS Indigo tutorial)", accessed: 2026-11-18}
---

# Clearpath research bases (Husky, Jackal, Dingo, Ridgeback, Boxer)

Clearpath Robotics of Ontario, Canada, makes rugged mobile bases for outdoor and indoor research [3][4].
Rockwell Automation completed its purchase of Clearpath and its OTTO Motors division in October 2023;
the site now reads "Clearpath Robotics, by Rockwell Automation" [3][4]. For a builder these are bases to
buy or simulate: the hardware is closed, but the ROS 2 stack and Gazebo setup are BSD-3 on GitHub [5].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Husky A300, the current Husky; the A200 is the previous version | 1, 3 |
| Drive, protection | Four brushless motors, skid steer, `dof: 4`; IP54, -20 to +40 °C | 1 |
| Size, mass | 990 x 698 x 372 mm, 80 kg (maker's claims) | 1 |
| Payload, speed | 100 kg max, 50 kg on all terrain, 30° climb; 2.0 m/s (maker's claims) | 1 |
| Battery, runtime | LiFePO4 at 25.6 V: 40, 80 or 120 Ah for about 4, 8 or 12 h (maker's claims) | 1 |
| Computer, software | Intel Core i3-13100TE or i7-13700TE, GPU optional; ships with ROS 2 Jazzy | 1, 2 |

## How it works

The Husky A300 has four motors, a LiFePO4 battery and an onboard PC; the A200 had two motors, a lead-acid
battery, an RS232 link and no computer [1]. Jackal is a small 4x4 outdoor base (IP62), Ridgeback runs on
mecanum wheels, Dingo comes in differential and omnidirectional forms, and Boxer is adapted from the OTTO
100 industrial AMR [5][6][7][8][9]. Warthog is a further outdoor UGV on the product page [3].

All current bases share one ROS 2 stack. A `robot.yaml` file lists the platform, attachments, sensors
and arms; generators turn it into launch files, parameters and a URDF for the real robot
(`clearpath_robot`) or for Gazebo (`clearpath_simulator`) [5]. `clearpath_common` holds descriptions for
a200, a300, j100, dd100/dd150 (Dingo-D), do100/do150 (Dingo-O), r100 (Ridgeback) and w200 (Warthog), plus
Franka, Kinova Gen3 and Universal Robots arms [5]. The A200 runs ROS 1 Noetic or ROS 2 Humble, the A300
ROS 2 Jazzy [1]. We found no MuJoCo Menagerie model of a Clearpath base.

| Variant | Use | Size (mm) | Mass | Payload | Max speed | Source |
|---|---|---|---|---|---|---|
| Husky A300 | outdoor | 990 x 698 x 372 | 80 kg | 100 kg | 2.0 m/s | 1 |
| Husky A200 | outdoor | 990 x 670 x 390 | 50 kg | 75 kg | 1.0 m/s | 1 |
| Jackal | outdoor | 508 x 430 x 250 | 17 kg | 20 kg | 2.0 m/s | 6 |
| Dingo | indoor | 686 x 517 x 114 | 13 kg | 20 kg | 1.3 m/s | 7 |
| Ridgeback | indoor, mecanum | 960 x 793 x 311 | 135 kg | 100 kg | 1.1 m/s | 8 |
| Boxer | indoor, OTTO 100 base | 740 x 550 x 320 | 114 kg | not stated | 2.0 m/s | 9 |

## What it is used for

- **Field robotics and navigation:** Husky and Jackal are Clearpath's outdoor research UGVs [1][6].
- **Mobile manipulation:** a Husky package with a Franka Research 3 arm and MoveIt 2 [2], a Ridgeback
  UR5e package [8], and the older dual-UR5 Husky, whose ROS Indigo tutorial runs in Gazebo [10].
- **Inspection:** the Husky A200 Observer is sold as a robotic inspection system [3].

## Cost and BOM

Price on request: the Husky A300, Jackal, Dingo and Ridgeback pages offer only a quote form [2][6][7][8].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Descriptions, control, config generators | ROS 2, URDF/xacro | [clearpath_common](https://github.com/clearpathrobotics/clearpath_common) [5] | BSD-3-Clause |
| On-robot drivers and services | ROS 2 | [clearpath_robot](https://github.com/clearpathrobotics/clearpath_robot) | BSD-3-Clause |
| Simulator | ROS 2, Gazebo | [clearpath_simulator](https://github.com/clearpathrobotics/clearpath_simulator) | BSD-3-Clause |
| Hardware, motor controllers, Boxer's OTTO software | | | Closed |

## Strengths and limits

- **Strengths:** one BSD-3 ROS 2 stack and one config file serve every current base, real or simulated,
  so sensors and arms are added by config [5]; IP54 and IP62 outdoor bases [1][6].
- **Limits:** price on request [2]; closed hardware [5]; the A200 and A300 need different ROS
  versions [1]; Boxer depends on OTTO software and is not on the current product page [3][9].

## Related robots

- [TurtleBot](turtlebot.md): Clearpath also builds TurtleBot 4, a small ROS 2 teaching base.
- [Universal Robots](universal-robots.md), [Franka Panda](franka-panda.md) and
  [Kinova Gen3](kinova-gen3.md): arms with descriptions in `clearpath_common` [5].
- [KUKA youBot](kuka-youbot.md): an older omnidirectional base with a small arm.

## Sources

1. [Clearpath: Husky A300 vs A200 spec comparison](https://clearpathrobotics.com/husky-spec-comparison/), accessed 2026-11-18
2. [Clearpath: Husky A300 product page](https://clearpathrobotics.com/husky-a300-unmanned-ground-vehicle-robot/), accessed 2026-11-18
3. [Clearpath Robotics home page (product line-up)](https://clearpathrobotics.com/), accessed 2026-11-18
4. [Logistics Business: Rockwell completes acquisition of Clearpath Robotics (2023-10-03)](https://logisticsbusiness.com/materials-handling-warehousing/agv-amr-robots/rockwell-completes-acquisition-of-clearpath-robotics/), accessed 2026-11-18
5. [clearpath_common repository (jazzy branch)](https://github.com/clearpathrobotics/clearpath_common), accessed 2026-11-18
6. [Clearpath: Jackal product page](https://clearpathrobotics.com/jackal-small-unmanned-ground-vehicle/), accessed 2026-11-18
7. [Clearpath: Dingo product page](https://clearpathrobotics.com/dingo-indoor-mobile-robot/), accessed 2026-11-18
8. [Clearpath: Ridgeback product page](https://clearpathrobotics.com/ridgeback-indoor-robot-platform/), accessed 2026-11-18
9. [Clearpath docs: Boxer user manual](https://docs.clearpathrobotics.com/docs_robots/indoor_robots/boxer/user_manual_boxer), accessed 2026-11-18
10. [Clearpath: Husky dual UR5 mobile manipulation demo (ROS Indigo tutorial)](https://clearpathrobotics.com/assets/guides/indigo/husky/HuskyDualManip.html), accessed 2026-11-18
