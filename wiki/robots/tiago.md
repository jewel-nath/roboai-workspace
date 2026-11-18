---
type: robot
name: PAL Robotics TIAGo, TIAGo++ and TIAGo Pro
summary: PAL Robotics' modular research mobile manipulator (2015) with a lifting torso, one or two 7-DoF arms and swappable grippers; common in European labs and RoboCup@Home, with official Apache-2.0 ROS 2 Humble packages, Gazebo and MuJoCo models; price on request today.
tags: [single-arm, dual-arm, ros2, ros2-control, gazebo, mujoco, moveit, nav2, pal-robotics, robocup]
category: mobile-manipulator
tier: B
openness: software-only
maker: PAL Robotics
year: 2015
license: {hardware: , software: Apache-2.0, docs: }
links: {repo: "https://github.com/pal-robotics/tiago_robot", docs: , cad: , paper: , site: "https://pal-robotics.com/robots/tiago/"}
specs: {dof: 11, payload_kg: 3, reach_mm: 870, mass_kg: 70, size_mm: , speed_mps: 1.5, runtime_h: 4}
stack: {actuators: "7-DoF arm, standard or series elastic (SEA); prismatic torso with 35 cm lift; pan-tilt head; differential or omnidirectional base; motors with current feedback", mcu: , compute: "Intel i5, 8 GB RAM, 250 GB SSD, or i7, 16 GB, 500 GB; Ubuntu LTS with RT Preempt", sensors: ["base laser, 5.6 m or optional 10 m or 25 m", "RGB-D camera in the head", "rear sonars", "6-DoF IMU in the base", "microphone array", "optional 6-axis wrist force/torque sensor"], sim_models: ["URDF/Xacro and ros2_control (pal-robotics/tiago_robot, ROS 2 Humble)", "Gazebo Classic and new Gazebo (pal-robotics/tiago_simulation, ROS 2 Humble)", "MJCF (MuJoCo Menagerie pal_tiago)", "MJCF of TIAGo++ on the omni base (MuJoCo Menagerie pal_tiago_dual)"], ros2: official}
cost: {type: retail, usd: 57000, as_of: 2015-02-04, source: "https://spectrum.ieee.org/pal-robotics-introduces-tiago-mobile-manipulator"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-04-24, stars: 74, active: false}
use_cases: [research, manipulation, navigation, hri, competition, education]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://pal-robotics.com/robots/tiago/", title: "PAL Robotics: TIAGo product page", accessed: 2026-11-18}
  - {url: "https://pal-robotics.com/datasheet/tiago/", title: "PAL Robotics: TIAGo technical specifications (datasheet)", accessed: 2026-11-18}
  - {url: "https://spectrum.ieee.org/pal-robotics-introduces-tiago-mobile-manipulator", title: "IEEE Spectrum: PAL Robotics introduces TIAGo mobile manipulator (2015-02-04)", accessed: 2026-11-18}
  - {url: "https://pal-robotics.com/robots/tiago-pro/", title: "PAL Robotics: TIAGo Pro product page", accessed: 2026-11-18}
  - {url: "https://github.com/pal-robotics/tiago_robot", title: "pal-robotics/tiago_robot (humble-devel)", accessed: 2026-11-18}
  - {url: "https://github.com/pal-robotics/tiago_simulation", title: "pal-robotics/tiago_simulation (humble-devel)", accessed: 2026-11-18}
  - {url: "https://github.com/pal-robotics/tiago_pro_robot", title: "pal-robotics/tiago_pro_robot (humble-devel)", accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/pal_tiago", title: "MuJoCo Menagerie: pal_tiago", accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/pal_tiago_dual", title: "MuJoCo Menagerie: pal_tiago_dual", accessed: 2026-11-18}
  - {url: "https://pal-robotics.com/blog/ready-steady-tiago-pal-robotics-at-robocup-2024", title: "PAL Robotics blog: Ready, steady, TIAGo! PAL Robotics at RoboCup 2024 (2024-07-23)", accessed: 2026-11-18}
---

# PAL Robotics TIAGo, TIAGo++ and TIAGo Pro

A modular research mobile manipulator from PAL Robotics of Barcelona, introduced in February 2015
[3]. A lifting torso carries one 7-DoF arm (two on TIAGo++ and TIAGo Pro), a pan-tilt RGB-D head and
a choice of grippers [1][4]. It is still sold, price on request [1]. PAL keeps official ROS 2
packages and simulations open [5][6], so a builder can simulate it or borrow its layout.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | TIAGo with one arm and the parallel gripper | [1][2] |
| Degrees of freedom | 11 counted: torso lift, 7-DoF arm, head pan and tilt, gripper; the base is not counted (PAL lists base 2, torso 1, arm 7, head 2) | [2] |
| Arm payload, reach | 3 kg at full extension; 87 cm; both without end-effector (maker's claims) | [2] |
| Size, mass, speed | 110 to 145 cm tall (35 cm torso lift); 54 cm diameter; 70 kg; 1.5 m/s (maker's claims) | [2] |
| Battery | 36 V, 20 Ah; 4 to 5 h on one battery, 8 to 10 h on two; the frontmatter uses 4 h | [2] |
| Computer, control | Intel i5, 8 GB RAM, 250 GB SSD, or i7, 16 GB, 500 GB; Ubuntu LTS with RT Preempt; arm in position, velocity or effort mode | [1][2] |
| Sensors | base laser 5.6 m (10 m or 25 m optional), rear sonars, base IMU, RGB-D head camera, microphones; wrist F/T sensor optional | [1][2] |

## How it works

The base drives differentially or omnidirectionally, and a prismatic torso lifts the arm and head
[1][2]. The arm is standard or series elastic (SEA); end-effectors include PAL's gripper, the Hey5
hand, Robotiq 2F-85, 2F-140 and EPick [1][2]. Whole-body control is a paid add-on [1][2].

`tiago_robot` is PAL's description, ros2_control configuration and bringup for every configuration,
picked by xacro arguments, under Apache-2.0 on `humble-devel` [5]. `tiago_simulation` runs it in
Gazebo Classic or, since January 2026, the new Gazebo, with Nav2 and MoveIt 2 [6]. TIAGo Pro has its
own ROS 2 packages [7]. MuJoCo Menagerie converts PAL's ROS 1 URDF into `pal_tiago` and has
`pal_tiago_dual` for TIAGo++ on the omni base; both are Apache-2.0 and drop the URDF's collision
elements [8][9].

| Variant | Arms and base | Price | Source |
|---|---|---|---|
| TIAGo | none or one 7-DoF arm; differential or omni base | 2015: no arm about €30,000 ($34,000); arm and gripper about €50,000 ($57,000); five-finger hand and F/T sensor about €60,000 ($68,000) | [1][3] |
| TIAGo++ | two 7-DoF arms; omni base in the Menagerie model | on request | [1][9] |
| TIAGo Pro | one or two 7-DoF arms with torque sensing in every actuator, 3 kg each; omni base with four mecanum wheels and two 10 m lidars | on request | [4][7] |

## What it is used for

- RoboCup@Home 2024: eight teams, nearly half the league, used PAL robots, placing first and third [10].
- Manipulation and HRI research with swappable grippers and force/torque sensing [1][2].
- Teaching and development without a robot, in PAL's free ROS 2 simulation [1][6].

## Cost and BOM

Price on request: PAL's page offers only a quote form [1]. The frontmatter uses the 2015 launch price
for TIAGo with arm and gripper, about €50,000, which IEEE Spectrum gave as $57,000 [3].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Description, controllers, bringup | ROS 2 Humble, URDF/Xacro | [tiago_robot](https://github.com/pal-robotics/tiago_robot) [5] | Apache-2.0 |
| Simulation | ROS 2 launch files, Gazebo Classic and new Gazebo | [tiago_simulation](https://github.com/pal-robotics/tiago_simulation) [6] | Apache-2.0; one package BSD |
| TIAGo Pro description, bringup | ROS 2 Humble, URDF/Xacro | [tiago_pro_robot](https://github.com/pal-robotics/tiago_pro_robot) [7] | Apache-2.0 |
| MuJoCo models | MJCF | Menagerie `pal_tiago`, `pal_tiago_dual` [8][9] | Apache-2.0 |
| Hardware, firmware, premium software | — | Not published | Proprietary |

## Strengths and limits

- **Strengths:** no, one or two arms, several end-effectors, two base types [1]; current official ROS 2
  packages with Gazebo, Nav2 and MoveIt 2 [5][6]; MuJoCo models [8][9]; 8 to 10 h on two batteries [2].
- **Limits:** 3 kg payload at full reach and 70 kg mass [2]; price on request [1]; ROS 2 packages
  target Humble [5]; whole-body control is paid [1]; Menagerie models lack collision geometry [8].

## What to reuse

- One parameterised xacro for every arm, gripper, sensor and laser option, with configs generated from templates [5].

## Related robots

- [PAL TALOS](pal-talos.md): PAL Robotics' torque-controlled humanoid.
- [Fetch](fetch.md), [PR2](pr2.md), [Hello Robot Stretch](hello-robot-stretch.md): other research mobile manipulators.

## Sources

1. [PAL Robotics: TIAGo product page](https://pal-robotics.com/robots/tiago/), accessed 2026-11-18
2. [PAL Robotics: TIAGo technical specifications (datasheet)](https://pal-robotics.com/datasheet/tiago/), accessed 2026-11-18
3. [IEEE Spectrum: PAL Robotics introduces TIAGo mobile manipulator (2015-02-04)](https://spectrum.ieee.org/pal-robotics-introduces-tiago-mobile-manipulator), accessed 2026-11-18
4. [PAL Robotics: TIAGo Pro product page](https://pal-robotics.com/robots/tiago-pro/), accessed 2026-11-18
5. [pal-robotics/tiago_robot (humble-devel)](https://github.com/pal-robotics/tiago_robot), accessed 2026-11-18
6. [pal-robotics/tiago_simulation (humble-devel)](https://github.com/pal-robotics/tiago_simulation), accessed 2026-11-18
7. [pal-robotics/tiago_pro_robot (humble-devel)](https://github.com/pal-robotics/tiago_pro_robot), accessed 2026-11-18
8. [MuJoCo Menagerie: pal_tiago](https://github.com/google-deepmind/mujoco_menagerie/tree/main/pal_tiago), accessed 2026-11-18
9. [MuJoCo Menagerie: pal_tiago_dual](https://github.com/google-deepmind/mujoco_menagerie/tree/main/pal_tiago_dual), accessed 2026-11-18
10. [PAL Robotics blog: Ready, steady, TIAGo! PAL Robotics at RoboCup 2024 (2024-07-23)](https://pal-robotics.com/blog/ready-steady-tiago-pal-robotics-at-robocup-2024), accessed 2026-11-18
