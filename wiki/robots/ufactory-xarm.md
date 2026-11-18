---
type: robot
name: UFACTORY xArm and Lite 6
summary: Low-cost cobot line from UFACTORY (2018) with 5-, 6- and 7-axis xArms, the 850 and the small Lite 6, sold with public shop prices; BSD-3 Python SDK and ROS 2 driver, and MuJoCo models of the xArm7 and Lite 6.
tags: [cobot, xarm, lite-6, low-cost, ros2, moveit, mujoco, python-sdk, commercial]
category: arm
tier: B
openness: software-only
maker: UFACTORY
year: 2018
license: {hardware: , software: BSD-3-Clause, docs: }
links: {repo: "https://github.com/xArm-Developer/xarm_ros2", docs: "https://docs.xarm.ufactory.cc", cad: , paper: , site: "https://www.ufactory.cc"}
specs: {dof: 6, payload_kg: 5, reach_mm: 700, mass_kg: 12.5, size_mm: , speed_mps: 1, runtime_h: }
stack: {actuators: "6 joint drives; motor and reducer types not published", mcu: , compute: "AC or DC control box; host PC over Ethernet", sensors: ["joint position sensing", "optional 6-axis force/torque sensor at the wrist"], sim_models: ["URDF/Xacro and Gazebo (xarm_ros2 xarm_description: xArm5, xArm6, xArm7, Lite 6, 850)", "MJCF (MuJoCo Menagerie: ufactory_xarm7, ufactory_lite6)", "URDF and MJCF (robot_descriptions: xarm6, xarm7)"], ros2: official}
cost: {type: retail, usd: 9175.86, as_of: 2026-11-18, source: "https://www.robotshop.com/products/xarm-6-dof-robotic-arm"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-10-20, stars: 284, active: true}
use_cases: [research, manipulation, teleop, imitation-learning, education, data-collection]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://www.ufactory.cc/xarm-collaborative-robot/", title: UFACTORY xArm series page, accessed: 2026-11-18}
  - {url: "https://docs.xarm.ufactory.cc/8.technical_specifications.html", title: xArm user manual, technical specifications, accessed: 2026-11-18}
  - {url: "https://www.ufactory.cc/lite-6-collaborative-robot/", title: UFACTORY Lite 6 page, accessed: 2026-11-18}
  - {url: "https://www.ufactory.cc/", title: UFACTORY home page with product prices, accessed: 2026-11-18}
  - {url: "https://www.ufactory.cc/about-us/", title: UFACTORY about page, accessed: 2026-11-18}
  - {url: "https://github.com/xArm-Developer/xarm_ros2", title: xarm_ros2 README, accessed: 2026-11-18}
  - {url: "https://github.com/xArm-Developer/xArm-Python-SDK", title: xArm-Python-SDK repository, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/ufactory_xarm7", title: "MuJoCo Menagerie: ufactory_xarm7", accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/ufactory_lite6", title: "MuJoCo Menagerie: ufactory_lite6", accessed: 2026-11-18}
  - {url: "https://github.com/robot-descriptions/robot_descriptions.py", title: robot_descriptions model list, accessed: 2026-11-18}
  - {url: "https://wuphilipp.github.io/gello_site/", title: GELLO project page, accessed: 2026-11-18}
  - {url: "https://www.robotshop.com/products/xarm-6-dof-robotic-arm", title: "RobotShop: UFACTORY xArm 6 with AC control box and 1.5 m cables", accessed: 2026-11-18}
---

# UFACTORY xArm and Lite 6

A family of low-cost collaborative arms from UFACTORY of Shenzhen, China: the 5-, 6- and 7-axis
xArm (2018), the higher-precision UFACTORY 850 and the small Lite 6 (2021) [1][5]. UFACTORY
publishes its prices, from US$2,999 for the Lite 6 [4]. For a builder it is an affordable step up
to an industrial-style arm with an official ROS 2 driver, a Python SDK and MuJoCo models.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | xArm6 | [1][2] |
| Degrees of freedom | 6; gripper optional, so `dof: 6` | [2] |
| Payload | 5 kg (maker's claim) | [1][2] |
| Reach | 700 mm (maker's claim) | [1] |
| Mass | 12.5 kg, arm only (maker's claim) | [1][2] |
| Repeatability | ±0.1 mm (maker's claim) | [1][2] |
| Joint ranges | J1 ±360°; J2 −117° to 116°; J3 −219° to 10°; J4 ±360°; J5 −97° to 180°; J6 ±360° | [2] |
| Maximum joint speed | 180°/s | [2] |
| Maximum TCP speed | 1 m/s (maker's claim) | [1][2] |
| Power | 24 V DC, 20.8 A input; 200 W typical, 500 W supply recommended | [2] |
| Control box | AC: 100–240 VAC in, 3.9 kg; DC: 24–72 V DC in, 2.6 kg. I/O: 8 configurable in and out, 8 digital in and out, 2 analog in and out, RS-485 | [2] |
| Communication | UFACTORY's own TCP protocol to the arm; Modbus TCP to the end effector | [2] |
| Body, footprint, flange | aluminium and carbon fibre; Ø126 mm; DIN ISO 9409-1-A50/63 | [2] |
| Force sensing | no built-in torque sensing; optional 6-axis wrist force/torque sensor | [1] |
| Ambient, cleanroom | 0 to 50 °C; ISO class 5 | [2] |

## How it works

The xArm5, 6 and 7 share their controller, common specifications and software; they differ in
joint count, payload and mass [1][2]. The host talks to the controller over Ethernet with
UFACTORY's own TCP protocol [2]. UFACTORY Studio is the maker's programming app [2]; the BSD-3
Python SDK (`pip install xarm-python-sdk`) adds joint and Cartesian velocity control, servo-mode
streaming and online trajectory planning, and supports every model including the Lite 6 and
850 [7]. UFACTORY does not publish motor, reducer or encoder details in
the pages read.

xarm_ros2 is UFACTORY's ROS 2 package set, with one branch per distro from Foxy to Jazzy and
Rolling [6]. It holds the URDF models, controller and MoveIt configs, Gazebo simulation, dual-arm
setups, optional RealSense D435i and gripper models, and a demo of an arm on a mobile chassis; it
covers the Lite 6 and, since June 2023, the 850 [6]. Its C++ SDK is a git submodule, so it must be cloned with `--recursive` [6].

MuJoCo Menagerie carries the xArm7 with its gripper and the Lite 6 with two gripper set-ups, both
BSD-3 and derived from UFACTORY's URDFs [8][9]; there is no Menagerie xArm6. robot_descriptions
loads xArm6 and xArm7 URDFs and the xArm7 MJCF [10].

| Model | DoF | Payload | Reach | Mass | Repeatability | Max TCP speed | Price (UFACTORY) | Source |
|---|---|---|---|---|---|---|---|---|
| Lite 6 | 6 | 0.6 kg | 440 mm | 8 kg | ±0.5 mm | 0.5 m/s | US$2,999 | [3][4] |
| xArm5 | 5 | 3 kg | 700 mm | 11.3 kg | ±0.1 mm | 1 m/s | xArm series from US$5,299 | [1][2][4] |
| xArm6 | 6 | 5 kg | 700 mm | 12.5 kg | ±0.1 mm | 1 m/s | xArm series from US$5,299 | [1][2][4] |
| xArm7 | 7 | 3.5 kg | 700 mm | 14.3 kg | ±0.1 mm | 1 m/s | xArm series from US$5,299 | [1][2][4] |
| UFACTORY 850 | 6 | 5 kg | 850 mm | 20 kg | ±0.02 mm | 1 m/s | US$8,999 | [1][4] |

## What it is used for

- Learning and teleoperation research: GELLO's low-cost leader arm was built for the xArm as well
  as the Franka and UR5, and its demos use an xArm7 [11].
- Simulation-first work with the Menagerie xArm7 and Lite 6 models [8][9].
- Light industrial cells: UFACTORY's xArm page shows a bin-picking case built on an xArm6 [1].

## Cost and BOM

| Item | Price (USD) | Type | Date | Source |
|---|---|---|---|---|
| xArm6 with AC control box and 1.5 m cables, RobotShop (US) | 9,175.86 | retail | 2026-11-18 | [12] |
| xArm series, UFACTORY's lowest listed price (model not named) | from 5,299 | retail | 2026-11-18 | [1][4] |
| Lite 6, UFACTORY | 2,999 | retail | 2026-11-18 | [3][4] |
| UFACTORY 850, UFACTORY | 8,999 | retail | 2026-11-18 | [4] |

UFACTORY's own shop page for the xArm6 could not be read for this card (it refused or failed every
request), so the frontmatter uses RobotShop's xArm6 price. The wrist force/torque sensor is an
option [1].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| ROS 2 driver, descriptions, MoveIt, Gazebo | ROS 2 packages, URDF/Xacro | [xarm_ros2](https://github.com/xArm-Developer/xarm_ros2) [6] | BSD-3-Clause |
| Python SDK | Python | [xArm-Python-SDK](https://github.com/xArm-Developer/xArm-Python-SDK) [7] | BSD-3-Clause |
| C++ SDK | C++ | [xArm-CPLUS-SDK](https://github.com/xArm-Developer/xArm-CPLUS-SDK), submodule of xarm_ros2 [6] | Licence not checked |
| MuJoCo models | MJCF | Menagerie `ufactory_xarm7`, `ufactory_lite6` [8][9] | BSD-3-Clause |
| Arm hardware, controller firmware, UFACTORY Studio | — | Not published | Closed |

## Strengths and limits

- **Strengths:** public prices, from US$2,999 for the Lite 6 and US$5,299 for an xArm [4]; 5-, 6-
  and 7-axis arms on one SDK and one ROS 2 package set [6][7]; BSD-3 software across the stack;
  light at 12.5 kg for the xArm6 [2]; a DC control box that takes 24–72 V [2] and a mobile-chassis
  demo in xarm_ros2 [6]; Menagerie models for two arms [8][9].
- **Limits:** no joint torque sensing, only an optional wrist force/torque sensor [1]; 700 mm
  reach and ±0.1 mm repeatability on the xArms, ±0.5 mm on the Lite 6 [1][3]; a private arm
  protocol, so you depend on UFACTORY's SDKs [2]; no IP rating in the specification table read [2];
  no Menagerie xArm6 or xArm5 [8]; UFACTORY's list price for the xArm6 alone was not confirmed.

## Related robots

- [AgileX PiPER](agilex-piper.md): a cheaper six-axis arm on a CAN bus, also with MuJoCo models.
- [Universal Robots](universal-robots.md): the industrial cobots the xArm undercuts on price.
- [Kinova Gen3](kinova-gen3.md) and [Franka Panda](franka-panda.md): research arms with joint
  torque sensing, sold on quote.
- [SO-101](so-101.md): the printed low-cost contrast for imitation learning.

## Sources

1. [UFACTORY xArm series page](https://www.ufactory.cc/xarm-collaborative-robot/), accessed 2026-11-18
2. [xArm user manual, technical specifications](https://docs.xarm.ufactory.cc/8.technical_specifications.html), accessed 2026-11-18
3. [UFACTORY Lite 6 page](https://www.ufactory.cc/lite-6-collaborative-robot/), accessed 2026-11-18
4. [UFACTORY home page with product prices](https://www.ufactory.cc/), accessed 2026-11-18
5. [UFACTORY about page](https://www.ufactory.cc/about-us/), accessed 2026-11-18
6. [xarm_ros2 README](https://github.com/xArm-Developer/xarm_ros2), accessed 2026-11-18
7. [xArm-Python-SDK repository](https://github.com/xArm-Developer/xArm-Python-SDK), accessed 2026-11-18
8. [MuJoCo Menagerie: ufactory_xarm7](https://github.com/google-deepmind/mujoco_menagerie/tree/main/ufactory_xarm7), accessed 2026-11-18
9. [MuJoCo Menagerie: ufactory_lite6](https://github.com/google-deepmind/mujoco_menagerie/tree/main/ufactory_lite6), accessed 2026-11-18
10. [robot_descriptions model list](https://github.com/robot-descriptions/robot_descriptions.py), accessed 2026-11-18
11. [GELLO project page](https://wuphilipp.github.io/gello_site/), accessed 2026-11-18
12. [RobotShop: UFACTORY xArm 6 with AC control box and 1.5 m cables](https://www.robotshop.com/products/xarm-6-dof-robotic-arm), accessed 2026-11-18
