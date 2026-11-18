---
type: robot
name: Universal Robots UR3, UR5, UR10 and e-Series
summary: The most widely deployed collaborative arms, from the 2008 UR5 to the e-Series and UR Series; closed hardware with an official BSD-3 ROS 2 driver that covers every model, plus URSim and MuJoCo models.
tags: [cobot, ur5e, e-series, cb3, industrial, ros2, moveit, ursim, commercial]
category: arm
tier: B
openness: software-only
maker: Universal Robots (Teradyne Robotics)
year: 2008
license: {hardware: , software: BSD-3-Clause, docs: }
links: {repo: "https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver", docs: "https://docs.universal-robots.com/Universal_Robots_ROS2_Documentation/", cad: , paper: , site: "https://www.universal-robots.com"}
specs: {dof: 6, payload_kg: 5, reach_mm: 850, mass_kg: 20.7, size_mm: , speed_mps: 4, runtime_h: }
stack: {actuators: "6 revolute joints, ±360° each", mcu: , compute: "UR control box (CB3, CB5 or Gen 7 controller); external Linux PC over Ethernet for ROS 2", sensors: ["joint encoders", "6-axis force/torque sensor at the tool flange (e-Series)"], sim_models: ["URDF/Xacro (Universal_Robots_ROS2_Description, all UR models)", "MJCF (MuJoCo Menagerie, universal_robots_ur5e and universal_robots_ur10e)", "URSim offline controller simulator (Docker images from UR)", "URDF and MJCF (robot_descriptions)"], ros2: official}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-11-13, stars: 847, active: true}
use_cases: [research, manipulation, teleop, imitation-learning, data-collection]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://www.universal-robots.com/manuals/latest/en/datasheets/ur5e/", title: "UR5e technical specification (updated October 2026)", accessed: 2026-11-18}
  - {url: "https://www.universal-robots.com/media/1828033/ur5_tech_spec_web_en.pdf", title: UR5 (CB3) technical details, accessed: 2026-11-18}
  - {url: "https://www.universal-robots.com/products/e-series/", title: Universal Robots e-Series product page, accessed: 2026-11-18}
  - {url: "https://www.universal-robots.com/products/ur-series/", title: Universal Robots UR Series product page, accessed: 2026-11-18}
  - {url: "https://www.universal-robots.com/products/g-series/", title: Universal Robots g-Series product page, accessed: 2026-11-18}
  - {url: "https://www.universal-robots.com/products/faq", title: Universal Robots product FAQ, accessed: 2026-11-18}
  - {url: "https://www.universal-robots.com/articles/ur/documentation/product-notice-cb3-end-of-sale-announcement/", title: CB3 end-of-sale announcement, accessed: 2026-11-18}
  - {url: "https://en.wikipedia.org/wiki/Universal_Robots", title: "Wikipedia: Universal Robots", accessed: 2026-11-18}
  - {url: "https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver", title: Universal_Robots_ROS2_Driver README, accessed: 2026-11-18}
  - {url: "https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver/blob/main/ur_robot_driver/doc/features.rst", title: UR ROS 2 driver feature list, accessed: 2026-11-18}
  - {url: "https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver/blob/main/ur_robot_driver/doc/usage/force_torque_control.rst", title: UR ROS 2 driver force and torque control guide, accessed: 2026-11-18}
  - {url: "https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver/blob/main/ur_robot_driver/doc/usage/simulation.rst", title: UR ROS 2 driver simulation guide (URSim and mock hardware), accessed: 2026-11-18}
  - {url: "https://docs.universal-robots.com/tutorials/communication-protocol-tutorials/rtde-guide.html", title: UR RTDE guide, accessed: 2026-11-18}
  - {url: "https://github.com/UniversalRobots/Universal_Robots_ROS2_Description", title: Universal_Robots_ROS2_Description README, accessed: 2026-11-18}
  - {url: "https://github.com/UniversalRobots/Universal_Robots_Client_Library", title: Universal_Robots_Client_Library repository, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/universal_robots_ur5e", title: "MuJoCo Menagerie: universal_robots_ur5e", accessed: 2026-11-18}
  - {url: "https://github.com/robot-descriptions/robot_descriptions.py", title: robot_descriptions model list, accessed: 2026-11-18}
  - {url: "https://github.com/real-stanford/universal_manipulation_interface", title: Universal Manipulation Interface repository README, accessed: 2026-11-18}
  - {url: "https://wuphilipp.github.io/gello_site/", title: GELLO project page, accessed: 2026-11-18}
---

# Universal Robots UR3, UR5, UR10 and e-Series

Six-axis collaborative arms from Universal Robots of Odense, Denmark, now part of Teradyne. The UR5
went on sale in 2008, and UR says more than 100,000 of its cobots have been delivered [1][8]. A
builder meets them in factories and manipulation papers, and their maker-maintained ROS 2 driver
was one of the first for any arm [9]. The CB3 arms (UR3, UR5, UR10) ended sale in 2024; the
e-Series and the heavier UR Series are current [3][4][7].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | UR5e (e-Series); UR has since renamed it UR7e | [1][6] |
| Degrees of freedom | 6 revolute joints, ±360° each; no gripper included, so `dof: 6` | [1] |
| Payload | 5 kg (UR5e datasheet); 7.5 kg under the UR7e name, same arm (maker's claims) | [1][6] |
| Reach | 850 mm; UR quotes 920 mm for the UR7e-920 after changing how it measures reach | [1][6] |
| Mass | 20.7 kg including cable (maker's claim) | [1] |
| Pose repeatability | ±0.03 mm, ISO 9283 (maker's claim) | [1] |
| Joint speed | ±180°/s on every joint (maker's claim) | [1] |
| Maximum TCP speed | 4 m/s (maker's claim) | [1] |
| Tool force/torque sensor | Range ±50 N, ±10 Nm; accuracy ±4.0 N, ±0.3 Nm (maker's claim) | [1] |
| Footprint, tool flange | Ø151 mm; ISO 9409-1-50-4-M6 flange; M8 8-pin tool connector with 2 digital in, 2 digital out, 2 analog in or RS-485, 12/24 V | [1] |
| Protection, noise, power | IP54; below 67 dB(A); 570 W maximum (maker's claims) | [1] |
| Control box | 460 x 449 x 254 mm, 12 kg, 100–240 VAC; Modbus TCP, EtherNet/IP, PROFINET | [1] |
| Safety | 23 configurable safety functions; EN ISO 13849-1 PLd Cat 3 and EN ISO 10218-1 | [1] |
| Real-time data | RTDE interface up to 500 Hz on e-Series and UR Series, TCP port 30004 | [13] |

## How it works

Every model is a chain of six revolute joints that each turn ±360°, with a separate control box
and teach pendant [1]. The e-Series has a six-axis force/torque sensor at the tool flange; the CB3
UR5 datasheet lists none, and gives ±0.1 mm repeatability against ±0.03 mm for the UR5e [1][2].
The datasheets do not name the joint motors or gearboxes.

Programs run on the controller in PolyScope (PolyScope 5 or the newer PolyScope X) or as URScript
[1][6][11]. The official ROS 2 driver sits on UR's C++ client library and reads the robot over RTDE
[9][13][15]. A small URCap program on the pendant hands motion control to ROS; a headless mode
skips the pendant [9]. The driver offers scaled joint trajectories that slow down with the
pendant's speed slider, joint position and velocity streaming, force mode, freedrive, tool contact
and passthrough trajectories; its feature list marks Cartesian position and twist control as not
supported [10]. Direct joint torque control needs PolyScope 5.25.1 or 10.12.1 or later [11]. The
driver runs only on Linux and covers every model from CB3 to the 2026 g-Series [6][9].

For simulation, UR's own URSim runs the real controller software in Docker, so the driver connects
to it exactly as to an arm; torque commands have no effect there [12]. The description package
holds URDF models of every arm [14]. MuJoCo Menagerie carries the UR5e and UR10e, converted from
the ROS-Industrial URDF [16], and robot_descriptions loads URDFs for most models [17].

| Model | Family, year | Payload | Reach | Mass | Status | Source |
|---|---|---|---|---|---|---|
| UR3 | CB3, 2015 | 3 kg | 500 mm | 11 kg | End of sale 2024 | [7][8] |
| UR5 | CB3; first sold 2008 | 5 kg | 850 mm | 18.4 kg | End of sale 2024 | [2][7][8] |
| UR10 | CB3, 2012 | 10 kg | 1300 mm | 28.9 kg | End of sale 2024 | [7][8] |
| UR3e | e-Series, 2018 | 3 kg | 500 mm (540 mm as UR3e-540) | 11.2 kg | Current | [3][8] |
| UR5e / UR7e | e-Series, 2018 | 5 kg; 7.5 kg as UR7e | 850 mm; 920 mm as UR7e-920 | 20.7 kg | Current as UR7e | [1][3][6] |
| UR10e / UR12e | e-Series, 2018 | 12.5 kg | 1300 mm | 33.5 kg | Current as UR12e | [3][6][8] |
| UR16e | e-Series, 2019 | 16 kg | 900 mm | 33.1 kg | Listed | [3][8] |
| UR20 | UR Series, 2022 | 20 kg (25 kg extended) | 1750 mm | 64 kg | Current | [4][8] |
| UR30 | UR Series, 2024 | 30 kg (35 kg extended) | 1300 mm | 63.5 kg | Current | [4][8] |

The UR Series also lists the UR8 Long, UR15 and UR18, and the 2026 g-Series (UR10g-1750, UR17g-1300,
UR18g-950) brings power, data and safety lines to the tool flange [4][5][6]. CB3 service and spare
parts continue until December 2032 [7].

## What it is used for

- Industrial automation: UR calls the e-Series the most deployed industrial cobot family [3].
- Manipulation research and learning: the Universal Manipulation Interface deploys its policies on
  UR5 and UR5e arms as well as Franka arms [18]; GELLO's low-cost teleoperation controller was built
  for the UR5, Franka and xArm [19].
- Testing ROS 2 controllers and MoveIt setups without hardware, through URSim or mock hardware [12].

## Cost and BOM

Price on request. UR's product pages list no prices [3][4], and its FAQ sends buyers to
distributors [6], so the frontmatter `cost` stays empty. UR no longer sells CB3 arms new [7].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| ROS 2 driver, controllers, MoveIt config | ROS 2 packages | [Universal_Robots_ROS2_Driver](https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver) [9] | BSD-3-Clause |
| Client library | C++ | [Universal_Robots_Client_Library](https://github.com/UniversalRobots/Universal_Robots_Client_Library) [15] | Apache-2.0 |
| Robot descriptions | URDF/Xacro, meshes | [Universal_Robots_ROS2_Description](https://github.com/UniversalRobots/Universal_Robots_ROS2_Description) [14] | BSD-3-Clause; meshes of the UR8 Long, UR15, UR18, UR20, UR30 and g-Series under UR's Graphical Documentation terms, which UR says are not OSI open source |
| MuJoCo models | MJCF | Menagerie `universal_robots_ur5e`, `universal_robots_ur10e` [16] | BSD-3-Clause |
| URSim | Docker images | Docker Hub, `universalrobots/ursim_*` [12] | Licence not checked |
| Arm hardware, controller firmware, PolyScope | — | Not published | Closed |

## Strengths and limits

- **Strengths:** a maker-maintained ROS 2 driver released for Humble through Rolling that covers
  every UR model [9]; URSim for testing without an arm [12]; built-in tool force/torque sensing on
  the e-Series [1]; direct torque control from ROS 2 [11]; a large installed base, with CB3 spares
  and service promised until 2032 [1][7].
- **Limits:** closed hardware and price on request; six joints only, so no redundant elbow and no
  joint torque sensors like the seven-axis research arms; no Cartesian control modes in the driver
  [10]; torque control has no effect in URSim [12]; the rename and new reach measurement make spec
  comparisons across years confusing [6]; Menagerie has only two models [16].

## What to reuse

- A small program on the robot controller that hands control to an external computer and takes it
  back, so the arm runs pendant programs and ROS commands in one session [9].
- Speed scaling that slows trajectories with the pendant's speed slider and safety limits instead of
  aborting them [9].
- Per-arm kinematic calibration stored on the robot and read out by the driver, so the TCP pose in
  ROS matches the real arm [9].

## Related robots

- [Franka Panda](franka-panda.md), [KUKA LBR iiwa](kuka-lbr-iiwa.md) and
  [Kinova Gen3](kinova-gen3.md): seven-axis research arms with joint torque sensing, which UR arms
  lack.
- [UFACTORY xArm](ufactory-xarm.md): a cheaper cobot with published shop prices.
- [UMI gripper](umi-gripper.md): the hand-held data-collection gripper whose policies run on UR5
  and UR5e arms [18].
- [SO-101](so-101.md): the low-cost contrast, a printed hobby-servo arm for imitation learning.

## Sources

1. [UR5e technical specification (updated October 2026)](https://www.universal-robots.com/manuals/latest/en/datasheets/ur5e/), accessed 2026-11-18
2. [UR5 (CB3) technical details](https://www.universal-robots.com/media/1828033/ur5_tech_spec_web_en.pdf), accessed 2026-11-18
3. [Universal Robots e-Series product page](https://www.universal-robots.com/products/e-series/), accessed 2026-11-18
4. [Universal Robots UR Series product page](https://www.universal-robots.com/products/ur-series/), accessed 2026-11-18
5. [Universal Robots g-Series product page](https://www.universal-robots.com/products/g-series/), accessed 2026-11-18
6. [Universal Robots product FAQ](https://www.universal-robots.com/products/faq), accessed 2026-11-18
7. [CB3 end-of-sale announcement](https://www.universal-robots.com/articles/ur/documentation/product-notice-cb3-end-of-sale-announcement/), accessed 2026-11-18
8. [Wikipedia: Universal Robots](https://en.wikipedia.org/wiki/Universal_Robots), accessed 2026-11-18
9. [Universal_Robots_ROS2_Driver README](https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver), accessed 2026-11-18
10. [UR ROS 2 driver feature list](https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver/blob/main/ur_robot_driver/doc/features.rst), accessed 2026-11-18
11. [UR ROS 2 driver force and torque control guide](https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver/blob/main/ur_robot_driver/doc/usage/force_torque_control.rst), accessed 2026-11-18
12. [UR ROS 2 driver simulation guide (URSim and mock hardware)](https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver/blob/main/ur_robot_driver/doc/usage/simulation.rst), accessed 2026-11-18
13. [UR RTDE guide](https://docs.universal-robots.com/tutorials/communication-protocol-tutorials/rtde-guide.html), accessed 2026-11-18
14. [Universal_Robots_ROS2_Description README](https://github.com/UniversalRobots/Universal_Robots_ROS2_Description), accessed 2026-11-18
15. [Universal_Robots_Client_Library repository](https://github.com/UniversalRobots/Universal_Robots_Client_Library), accessed 2026-11-18
16. [MuJoCo Menagerie: universal_robots_ur5e](https://github.com/google-deepmind/mujoco_menagerie/tree/main/universal_robots_ur5e), accessed 2026-11-18
17. [robot_descriptions model list](https://github.com/robot-descriptions/robot_descriptions.py), accessed 2026-11-18
18. [Universal Manipulation Interface repository README](https://github.com/real-stanford/universal_manipulation_interface), accessed 2026-11-18
19. [GELLO project page](https://wuphilipp.github.io/gello_site/), accessed 2026-11-18
