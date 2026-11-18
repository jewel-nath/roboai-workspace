---
type: robot
name: Interbotix X-Series arms (ViperX 300 S, WidowX 250 S)
summary: Trossen Robotics' Dynamixel research arms with BSD-licensed ROS drivers; the ViperX and WidowX are the follower and leader arms of ALOHA and the robot of BridgeData V2. Discontinued in 2025.
tags: [dynamixel, viperx, widowx, aloha, bridgedata, trossen, interbotix, ros2, moveit, discontinued]
category: arm
tier: B
openness: software-only
maker: Trossen Robotics
year:
license: {hardware: , software: BSD-3-Clause, docs: }
links: {repo: "https://github.com/Interbotix/interbotix_ros_manipulators", docs: "https://docs.trossenrobotics.com/interbotix_xsarms_docs", cad: , paper: , site: "https://trossenrobotics.com/viperx-300"}
specs: {dof: 7, payload_kg: 0.75, reach_mm: 750, mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "Dynamixel XM540-W270 (7) and XM430-W350 (2) smart servos", mcu: "none on the arm; ROBOTIS U2D2 USB-to-TTL adapter and a 12 V power hub", compute: "host PC over USB", sensors: ["servo encoders"], sim_models: ["URDF and Gazebo configs (interbotix_xsarm_descriptions, interbotix_xsarm_gazebo)", "MJCF (MuJoCo Menagerie, trossen_vx300s and trossen_wx250s)", "MJCF (MuJoCo Menagerie, aloha)"], ros2: official}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2024-07-10, stars: 184, active: false}
use_cases: [imitation-learning, teleop, data-collection, research, manipulation]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://docs.trossenrobotics.com/interbotix_xsarms_docs/specifications/vx300s.html", title: "Trossen docs: ViperX-300 6DOF specifications", accessed: 2026-11-18}
  - {url: "https://docs.trossenrobotics.com/interbotix_xsarms_docs/specifications/wx250s.html", title: "Trossen docs: WidowX-250 6DOF specifications", accessed: 2026-11-18}
  - {url: "https://trossenrobotics.com/_files/ugd/d3716d_9a5b59ecd8c74582926054578d3b9896.pdf", title: WidowX 250 S datasheet (PDF), accessed: 2026-11-18}
  - {url: "https://github.com/Interbotix/interbotix_ros_manipulators", title: interbotix_ros_manipulators repository and X-Series arms README, accessed: 2026-11-18}
  - {url: "https://docs.trossenrobotics.com/interbotix_xsarms_docs/ros_interface/ros2.html", title: "Trossen docs: X-Series arms ROS 2 interface", accessed: 2026-11-18}
  - {url: "https://trossenrobotics.com/viperx-300", title: Trossen ViperX 300 S product page, accessed: 2026-11-18}
  - {url: "https://www.trossenrobotics.com/widowx-250", title: Trossen WidowX 250 S product page, accessed: 2026-11-18}
  - {url: "https://www.trossenrobotics.com/post/honoring-the-past-building-the-future-trossen-legacy-hardware-reaches-end-of-life", title: "Trossen: legacy hardware reaches end of life", accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2304.13705", title: Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware (ALOHA), accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2308.12952", title: "BridgeData V2: A Dataset for Robot Learning at Scale", accessed: 2026-11-18}
  - {url: "https://rail-berkeley.github.io/bridgedata/", title: BridgeData V2 project page, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie", title: MuJoCo Menagerie model list, accessed: 2026-11-18}
  - {url: "https://github.com/huggingface/lerobot", title: LeRobot repository README, accessed: 2026-11-18}
---

# Interbotix X-Series arms (ViperX 300 S, WidowX 250 S)

Trossen Robotics' research arms, built from ROBOTIS Dynamixel X-Series servos and run by
BSD-licensed ROS packages [4]. They matter because of two landmark projects: ALOHA used WidowX arms
as leaders and ViperX arms as followers [9], and BridgeData V2 was collected on a WidowX 250 [11].
Both models are **discontinued**: Trossen ended its legacy and ALOHA hardware lines in July 2025
[8].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | ViperX 300 S (ViperX-300 6DOF) | [1] |
| Degrees of freedom | 6 arm joints plus a gripper; `dof: 7` counts the gripper as one | [1] |
| Servos | 9: XM540-W270 on waist, shoulder (2), elbow (2), forearm roll and wrist angle; XM430-W350 on wrist rotate and gripper | [1] |
| Reach / total span | 750 mm / 1500 mm (maker's claim) | [1] |
| Working payload | 750 g, at no more than 50% extension (maker's claim) | [1] |
| Repeatability / accuracy | 1 mm / 5 to 8 mm (maker's claim) | [1] |
| Joint limits | Waist and both rolls ±180°; shoulder ±101°; elbow −101 to 92°; wrist angle −107 to 130° | [1] |
| Gripper opening | 42 to 116 mm | [1] |
| Bus | Dynamixel TTL at 1 Mbit/s through a U2D2 | [1] |
| Mass | Not published for the ViperX; WidowX 250 S is 2.8 kg (maker's claim) | [3] |

## How it works

Every joint is a Dynamixel X-Series servo; the shoulder and elbow use two servos each, a main and a
"shadow" [1][2][4]. The servos daisy-chain to a power hub that feeds them 12 V and to a ROBOTIS U2D2
that links the bus to a PC over USB [4]. There is no other electronics.

The `interbotix_xs_sdk` node in `interbotix_ros_core` drives the servos;
`interbotix_ros_manipulators` adds per-arm motor configs (including ALOHA versions of both arms),
URDFs with inertias, MoveIt and Gazebo setups, and demos such as a leader-follower "puppet" mode
[4]. A Python module hides ROS for simple scripts [4]. The ROS 2 packages live on the `humble`,
`jazzy` and `rolling` branches (last commit 2025-01-02); Trossen's docs list ROS 2 Galactic and
Humble [5]. The default `main` branch holds the ROS 1 packages.

MuJoCo Menagerie carries `trossen_vx300s`, `trossen_wx250s` and the full bimanual `aloha` scene, all
BSD-3-Clause [12].

| Variant | Reach | Payload | Servos | Note | Source |
|---|---|---|---|---|---|
| ViperX 300 S | 750 mm | 750 g | 7 x XM540-W270, 2 x XM430-W350 | ALOHA follower | [1][9] |
| WidowX 250 S | 650 mm | 250 g | 7 x XM430-W350, 2 x XL430-W250 | ALOHA leader; BridgeData V2 robot; 2.8 kg | [2][3][11] |
| ViperX 300, WidowX 250 | — | — | — | 5-DoF versions without the forearm roll (`vx300`, `wx250` configs) | [4] |
| WidowX AI (Trossen AI line) | — | — | — | Trossen's successor line; Menagerie `trossen_wxai` | [8][12] |

## What it is used for

- **ALOHA:** a bimanual teleoperation rig of two WidowX leaders and two ViperX followers, built for
  under $20k, which introduced the ACT policy [9]. Menagerie's `aloha` model reproduces it [12].
- **BridgeData V2:** 60,096 trajectories over 24 environments and 13 skills on a WidowX 250 6DOF,
  released under CC BY 4.0 [10][11].
- **LeRobot:** WidowX is supported through a community plugin, not a native driver [13].

## Cost and BOM

No dated price could be confirmed. Both product pages say the arms are discontinued [6][7], and
Trossen's store pages for them no longer load (404 on 2026-11-18). Trossen promises support and
spare parts while components last [8]. Used arms and Trossen's newer WidowX AI line are the ways in
today. The WidowX 250 S datasheet lists a U2D2, a 12 V 5 A power supply and a parallel gripper
kit with the arm [3].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| ROS driver (`interbotix_xs_sdk`) | ROS 1 and ROS 2 packages | [interbotix_ros_core](https://github.com/Interbotix/interbotix_ros_core) | BSD-3-Clause |
| Arm packages: configs, MoveIt, Gazebo, demos | ROS 1 and ROS 2 packages | [interbotix_ros_manipulators](https://github.com/Interbotix/interbotix_ros_manipulators) [4] | BSD-3-Clause |
| Robot models | URDF (xacro), meshes | `interbotix_xsarm_descriptions` [4] | BSD-3-Clause |
| MuJoCo models | MJCF | MuJoCo Menagerie [12] | BSD-3-Clause |
| Gripper finger CAD | Downloadable for custom fingers | Trossen [3] | Not stated |
| Arm CAD, servo firmware | — | Not published; Dynamixel firmware is ROBOTIS's | Closed |

## Strengths and limits

- **Strengths:** the hardware behind ALOHA and BridgeData V2, so many datasets, policies and
  sim models match it [9][11][12]; mature ROS packages with MoveIt and Gazebo [4]; off-the-shelf
  servos that are easy to swap [3].
- **Limits:** discontinued, with no current price [6][7][8]; 5 to 8 mm accuracy and payload rated
  only at half extension (maker's claims) [1]; ROS 2 support stops at Humble in the docs [5];
  closed mechanical design.

## What to reuse

- Two servos on one joint (main and shadow) to double torque at the shoulder and elbow.
- A smaller arm with the same joint layout as the leader, as ALOHA did with WidowX and ViperX.
- Swappable gripper fingers, so tasks get custom printed fingers rather than a new gripper.

## Related robots

- [Koch v1.1](koch-v1-1.md) and [SO-101](so-101.md): printed leader-follower arms that bring the
  ALOHA idea down to a few hundred dollars.
- [AgileX PiPER](agilex-piper.md): a newer, closed six-axis arm used as a follower in recent papers.
- [OpenManipulator-X](openmanipulator-x.md): ROBOTIS's own Dynamixel arm.

## Sources

1. [Trossen docs: ViperX-300 6DOF specifications](https://docs.trossenrobotics.com/interbotix_xsarms_docs/specifications/vx300s.html), accessed 2026-11-18
2. [Trossen docs: WidowX-250 6DOF specifications](https://docs.trossenrobotics.com/interbotix_xsarms_docs/specifications/wx250s.html), accessed 2026-11-18
3. [WidowX 250 S datasheet (PDF)](https://trossenrobotics.com/_files/ugd/d3716d_9a5b59ecd8c74582926054578d3b9896.pdf), accessed 2026-11-18
4. [interbotix_ros_manipulators repository and X-Series arms README](https://github.com/Interbotix/interbotix_ros_manipulators), accessed 2026-11-18
5. [Trossen docs: X-Series arms ROS 2 interface](https://docs.trossenrobotics.com/interbotix_xsarms_docs/ros_interface/ros2.html), accessed 2026-11-18
6. [Trossen ViperX 300 S product page](https://trossenrobotics.com/viperx-300), accessed 2026-11-18
7. [Trossen WidowX 250 S product page](https://www.trossenrobotics.com/widowx-250), accessed 2026-11-18
8. [Trossen: legacy hardware reaches end of life](https://www.trossenrobotics.com/post/honoring-the-past-building-the-future-trossen-legacy-hardware-reaches-end-of-life), accessed 2026-11-18
9. [Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware (ALOHA)](https://arxiv.org/abs/2304.13705), accessed 2026-11-18
10. [BridgeData V2: A Dataset for Robot Learning at Scale](https://arxiv.org/abs/2308.12952), accessed 2026-11-18
11. [BridgeData V2 project page](https://rail-berkeley.github.io/bridgedata/), accessed 2026-11-18
12. [MuJoCo Menagerie model list](https://github.com/google-deepmind/mujoco_menagerie), accessed 2026-11-18
13. [LeRobot repository README](https://github.com/huggingface/lerobot), accessed 2026-11-18
