---
type: robot
name: ROBOTIS OP3
summary: 51 cm, 20-DoF kid-size humanoid from ROBOTIS on Dynamixel XM430-W350-R servos, an Intel NUC and an OpenCR board, with Apache-2.0 ROS packages (ROS 1 on master, ROS 2 Jazzy for the 2025 re-release) and a MuJoCo Menagerie model; part STEP files are published without a licence.
tags: [kid-size, dynamixel, xm430, opencr, intel-nuc, robocup, ros, ros2, mujoco, commercial]
category: humanoid
tier: B
openness: partial
maker: ROBOTIS
year: 2017
license: {hardware: , software: Apache-2.0, docs: }
links: {repo: "https://github.com/ROBOTIS-GIT/ROBOTIS-OP3", docs: "https://emanual.robotis.com/docs/en/platform/op3/introduction/", cad: "https://github.com/ROBOTIS-GIT/ROBOTIS-OP-Series-Data/tree/master/ROBOTIS-OP3", paper: , site: }
specs: {dof: 20, payload_kg: , reach_mm: , mass_kg: 3.5, size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "Dynamixel XM430-W350-R servos", mcu: [robotis-opencr, "OpenCR sub-controller"], compute: "Intel NUC with Core i3, 8 GB DDR4, 250 GB SSD (2025 version)", sensors: ["Logitech C920 HD Pro webcam (1920 x 1080)", "3-axis gyroscope, accelerometer and magnetometer"], sim_models: ["URDF/Xacro (ROBOTIS-OP3-Common: op3_description)", "Gazebo Classic (ROBOTIS-OP3-Common: op3_gazebo, ROS 1 branch)", "MJCF (MuJoCo Menagerie: robotis_op3)"], ros2: official}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2024-12-13, stars: 165, active: false}
use_cases: [research, competition, reinforcement-learning, locomotion, education]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://emanual.robotis.com/docs/en/platform/op3/introduction/", title: ROBOTIS e-Manual, OP3 introduction and specifications, accessed: 2026-11-18}
  - {url: "https://emanual.robotis.com/docs/en/platform/op3/hardware/", title: ROBOTIS e-Manual, OP3 hardware data, accessed: 2026-11-18}
  - {url: "https://github.com/ROBOTIS-GIT/ROBOTIS-OP3", title: ROBOTIS-OP3 repository (master), accessed: 2026-11-18}
  - {url: "https://github.com/ROBOTIS-GIT/ROBOTIS-OP3/tree/jazzy-devel", title: ROBOTIS-OP3 jazzy-devel branch, accessed: 2026-11-18}
  - {url: "https://github.com/ROBOTIS-GIT/ROBOTIS-OP3-Common", title: ROBOTIS-OP3-Common repository (description and Gazebo), accessed: 2026-11-18}
  - {url: "https://github.com/ROBOTIS-GIT/ROBOTIS-OP-Series-Data", title: ROBOTIS-OP-Series-Data repository, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/robotis_op3", title: "MuJoCo Menagerie: robotis_op3", accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2304.13653", title: "Haarnoja et al.: Learning Agile Soccer Skills for a Bipedal Robot with Deep Reinforcement Learning", accessed: 2026-11-18}
  - {url: "https://hsl.robocup.org/wp-content/uploads/2026/03/small_Blenders_FC-specs-698052b2b0901.pdf", title: "RoboCup Humanoid League team spec: Hardware specification for Robotis OP3 (2026)", accessed: 2026-11-18}
---

# ROBOTIS OP3

A kid-size humanoid, about 51 cm tall, from ROBOTIS, the maker of Dynamixel servos, built on XM430
servos with an Intel NUC and open ROS packages [1][3]. It succeeds the OP2; ROBOTIS's packages were
first tagged in 2017, and a 2025 re-release was rebuilt for ROS 2 [1][3]. Learning research and
RoboCup teams use it [8][9].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | 2025 re-release | [1] |
| Degrees of freedom | 20: head 2, arms 3 each, legs 6 each | [1][5] |
| Actuators | Dynamixel XM430-W350-R | [1] |
| Height, mass | about 510 mm; about 3.5 kg without the skin cover (maker's claims) | [1] |
| Main computer | Intel NUC, Core i3, 8 GB DDR4, 250 GB M.2 SSD | [1] |
| Sub-controller | OpenCR | [1] |
| Sensors | Logitech C920 camera (1920 x 1080); 3-axis gyroscope, accelerometer and magnetometer | [1] |
| Battery | 3-cell LiPo, 11.1 V, 3300 mAh (earlier version: 1800 mAh) | [1] |
| Software | Linux, C++, ROS 2 and the Dynamixel SDK | [1] |
| Walking speed | 7.14 cm/s on one RoboCup team's OP3 with a Jetson Nano (team's claim) | [9] |

## How it works

Twenty XM430 servos (Dynamixel Protocol 2.0) form a body with a 2-DoF head, 3-DoF arms and 6-DoF
legs [1][5]. An Intel NUC runs the control software, with an OpenCR board as sub-controller [1][3].
ROBOTIS's framework loads motion modules in `op3_manager`: walking, online walking, balance control,
action playback, head control, direct control and tuning [3].

The default `master` branch holds ROS 1 catkin packages; the README lists Kinetic and Melodic, and
the last commit is from December 2024 [3]. `jazzy-devel` branches of ROBOTIS-OP3 and
ROBOTIS-OP3-Common hold ament (ROS 2) packages, last changed in February 2025, for the re-release
that ROBOTIS says was developed from the ground up for ROS 2 [1][4][5]. ROBOTIS-OP3-Common has the
URDF/Xacro description and, on `master`, a Gazebo package [5]. MuJoCo Menagerie has an Apache-2.0
MJCF model derived from that URDF with simplified convex meshes [7].

| Variant | Changes | Source |
|---|---|---|
| OP3 (2017) | ROS 1 packages; 1800 mAh battery; vs OP2: XM430 for MX-28 servos, OpenCR for CM-730, NUC for an Atom board | [1][3] |
| OP3 2025 re-release | rebuilt for ROS 2 (jazzy-devel branches); Core i3 NUC; 3300 mAh battery | [1][4] |

## What it is used for

- Reinforcement learning: a Google DeepMind team trained one-versus-one soccer in simulation and ran
  it zero-shot on OP3s, which walked 181% faster than with a scripted controller [8].
- RoboCup humanoid soccer: one 2026 team's spec sheet lists an OP3 with a Jetson Nano computer [9].
- Walking and balance work built on ROBOTIS's open motion modules [3].

## Cost and BOM

Not verified. ROBOTIS's US shop answered automated requests with HTTP 429 on 2026-11-18, and the
other listings found were resellers in GBP or EUR, so `cost` stays empty.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| ROS packages | C++; ROS 1 on `master`, ROS 2 on `jazzy-devel` | [ROBOTIS-OP3](https://github.com/ROBOTIS-GIT/ROBOTIS-OP3) [3][4] | Apache-2.0 |
| Description, Gazebo | URDF/Xacro | [ROBOTIS-OP3-Common](https://github.com/ROBOTIS-GIT/ROBOTIS-OP3-Common) [5] | Apache-2.0 |
| MuJoCo model | MJCF | [Menagerie robotis_op3](https://github.com/google-deepmind/mujoco_menagerie/tree/main/robotis_op3) [7] | Apache-2.0 |
| Mechanical CAD, skins, boards | STEP part assembly; 3 printable skin sets; board PDFs | [ROBOTIS-OP-Series-Data](https://github.com/ROBOTIS-GIT/ROBOTIS-OP-Series-Data/tree/master/ROBOTIS-OP3) [2][6] | none stated (all rights reserved by default) |

## Strengths and limits

- **Strengths:** a small, light humanoid on well-documented Dynamixel servos [1]; open motion
  modules and descriptions under Apache-2.0 [3][5]; a Menagerie model [7]; proven sim-to-real RL [8].
- **Limits:** the default branch is still ROS 1, with ROS 2 only on `jazzy-devel` branches [3][4];
  the CAD has no licence [6]; the scripted walk is slow, learned policies walked 181% faster [8];
  no USD price verified.

## Related robots

- [ToddlerBot](toddlerbot.md) and [Poppy Humanoid](poppy-humanoid.md): open Dynamixel humanoids.
- [NAO](nao.md): a commercial kid-size humanoid; [TurtleBot3](turtlebot3.md) and
  [OpenManipulator-X](openmanipulator-x.md): other ROBOTIS robots on Dynamixel servos.

## Sources

1. [ROBOTIS e-Manual, OP3 introduction and specifications](https://emanual.robotis.com/docs/en/platform/op3/introduction/), accessed 2026-11-18
2. [ROBOTIS e-Manual, OP3 hardware data](https://emanual.robotis.com/docs/en/platform/op3/hardware/), accessed 2026-11-18
3. [ROBOTIS-OP3 repository (master)](https://github.com/ROBOTIS-GIT/ROBOTIS-OP3), accessed 2026-11-18
4. [ROBOTIS-OP3 jazzy-devel branch](https://github.com/ROBOTIS-GIT/ROBOTIS-OP3/tree/jazzy-devel), accessed 2026-11-18
5. [ROBOTIS-OP3-Common repository (description and Gazebo)](https://github.com/ROBOTIS-GIT/ROBOTIS-OP3-Common), accessed 2026-11-18
6. [ROBOTIS-OP-Series-Data repository](https://github.com/ROBOTIS-GIT/ROBOTIS-OP-Series-Data), accessed 2026-11-18
7. [MuJoCo Menagerie: robotis_op3](https://github.com/google-deepmind/mujoco_menagerie/tree/main/robotis_op3), accessed 2026-11-18
8. [Haarnoja et al.: Learning Agile Soccer Skills for a Bipedal Robot with Deep Reinforcement Learning](https://arxiv.org/abs/2304.13653), accessed 2026-11-18
9. [RoboCup Humanoid League team spec: Hardware specification for Robotis OP3 (2026)](https://hsl.robocup.org/wp-content/uploads/2026/03/small_Blenders_FC-specs-698052b2b0901.pdf), accessed 2026-11-18
