---
type: robot
name: PAL Robotics TALOS
summary: PAL Robotics' 1.75 m, 32-DoF research humanoid with joint torque sensing and 2 kHz EtherCAT control, used in European labs for whole-body and multi-contact control; official Apache-2.0 ROS 2 packages and a MuJoCo Menagerie model; price on request, reported near €1 million in 2017.
tags: [humanoid, torque-control, ethercat, ros2, ros2-control, gazebo, mujoco, pal-robotics, research]
category: humanoid
tier: B
openness: software-only
maker: PAL Robotics
year: 2017
license: {hardware: , software: Apache-2.0, docs: }
links: {repo: "https://github.com/pal-robotics/talos_robot", docs: , cad: , paper: "https://doi.org/10.1109/HUMANOIDS.2017.8246947", site: "https://pal-robotics.com/robots/talos/"}
specs: {dof: 32, payload_kg: 6, reach_mm: , mass_kg: 95, size_mm: , speed_mps: 0.83, runtime_h: 1.5}
stack: {actuators: "32 motorised joints, torque-controllable; joint torque sensors in all but the head, wrists and grippers", mcu: , compute: "onboard computers running Ubuntu LTS with a real-time OS", sensors: ["joint torque sensors", "force/torque sensors in wrists and ankles", "IMU", "high-resolution motor and joint encoders"], sim_models: ["URDF/Xacro and ros2_control (pal-robotics/talos_robot, ROS 2 Humble)", "Gazebo Classic (pal-robotics/talos_simulation, ROS 2 Humble)", "URDF and SRDF (stack-of-tasks/talos-data)", "MJCF (MuJoCo Menagerie pal_talos)"], ros2: official}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-02-19, stars: 26, active: false}
use_cases: [research, locomotion, manipulation, hri]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://pal-robotics.com/robots/talos/", title: "PAL Robotics: TALOS product page", accessed: 2026-11-18}
  - {url: "https://spectrum.ieee.org/talos-humanoid-now-available-from-pal-robotics", title: "IEEE Spectrum: TALOS humanoid now available from PAL Robotics (2017-03-07)", accessed: 2026-11-18}
  - {url: "https://doi.org/10.1109/HUMANOIDS.2017.8246947", title: "Stasse et al.: TALOS, a new humanoid research platform targeted for industrial applications (Humanoids 2017)", accessed: 2026-11-18}
  - {url: "https://github.com/pal-robotics/talos_robot", title: "pal-robotics talos_robot (humble-devel)", accessed: 2026-11-18}
  - {url: "https://github.com/pal-robotics/talos_simulation", title: "pal-robotics talos_simulation (humble-devel)", accessed: 2026-11-18}
  - {url: "https://github.com/stack-of-tasks/talos-data", title: stack-of-tasks talos-data README, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/pal_talos", title: "MuJoCo Menagerie: pal_talos", accessed: 2026-11-18}
  - {url: "https://www.tu-darmstadt.de/universitaet/aktuelles_meldungen/news_archive/news_details_en_496896.en.jsp", title: "TU Darmstadt: Extraordinary employee, humanoid robot TALOS (2025-02-28)", accessed: 2026-11-18}
---

# PAL Robotics TALOS

A full-size research humanoid from PAL Robotics, on sale since 2017; LAAS-CNRS in Toulouse had the
first unit [2]. Joint torque sensors and EtherCAT control loops at 2 kHz make it a platform for
whole-body and multi-contact control [1]. Few labs own one, but PAL's official ROS 2 packages and a
MuJoCo Menagerie model are open, so anyone can simulate it [4][7][8].

## Specs

| Item | Value | Source |
|---|---|---|
| Degrees of freedom | 32: 6 per leg, 7 per arm, 1 per gripper, 2 in the neck, 2 in the waist; the Menagerie model has 32 actuators | [2][7] |
| Height, mass | 175 cm, 95 kg (maker's claims); IEEE Spectrum gave 100 kg in 2017 | [1][2] |
| Arm payload | 6 kg per arm at full extension (maker's claim) | [1][3] |
| Walking speed | 3 km/h, about 0.83 m/s | [2] |
| Battery | 1.5 h walking, 3 h standby (maker's claim) | [1] |
| Torque sensing | joint torque sensors in all joints except head, wrists and grippers; force/torque sensors in wrists and ankles | [1] |
| Control | EtherCAT bus; control loops at 2 kHz, up to 5 kHz | [1] |
| Software | Ubuntu LTS with a real-time OS; ROS with ros_control, ROS 2 Humble packages | [1][4] |

## How it works

PAL designed TALOS with feedback from the DARPA Robotics Challenge. Its arm kinematics suit screwing
and drilling, and torque sensors plus high-resolution motor and joint encoders allow safe physical
interaction [3]. Head and grippers can be customised, and PAL sells whole-body control, navigation,
HRI skills and teleoperation as premium software [1].

`talos_robot` is PAL's official description, controller configuration and bringup; its default
branch, `humble-devel`, targets ROS 2 Humble with ros2_control under Apache-2.0 [4].
`talos_simulation` starts the robot in Gazebo Classic with gazebo_ros2_control and MoveIt
configuration [5]. LAAS's `talos-data` stores plain URDF and SRDF for the Stack of Tasks, without
xacro and with dummy rotor inertias, under LGPL-3.0 [6].

The Menagerie MJCF is converted from PAL's URDF and comes in torque- and position-controlled
versions, Apache-2.0 [7].

## What it is used for

- Humanoid locomotion and whole-body control at LAAS-CNRS, whose TALOS is called Pyrène [2].
- Research on motor skills, perception and HRI at TU Darmstadt, which bought Germany's only TALOS in
  2025; it counted five other research centres with one [8].
- Industrial tasks such as screwing and drilling, which shaped its arm design [3].

## Cost and BOM

Price on request: PAL's page offers only a quote form [1], so the frontmatter `cost` stays empty. In
2017 IEEE Spectrum reported "something around €1 million" [2]. In 2025 TU Darmstadt spent about €1.8
million on TALOS, future upgrades and lab equipment, half funded by the DFG [8]. No source gives a
USD price or an exchange rate.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Hardware, firmware, premium software | — | Not published | Proprietary |
| Description, controllers, bringup | ROS 2 Humble, URDF/Xacro | [talos_robot](https://github.com/pal-robotics/talos_robot) [4] | Apache-2.0 |
| Gazebo simulation | ROS 2 launch files | [talos_simulation](https://github.com/pal-robotics/talos_simulation) [5] | Apache-2.0 |
| Stack of Tasks model | URDF, SRDF | [talos-data](https://github.com/stack-of-tasks/talos-data) [6] | LGPL-3.0 |
| MuJoCo model | MJCF | [Menagerie pal_talos](https://github.com/google-deepmind/mujoco_menagerie/tree/main/pal_talos) [7] | Apache-2.0 |

## Strengths and limits

- **Strengths:** joint torque sensing and 2 to 5 kHz EtherCAT loops in a full-size humanoid [1];
  official, current ROS 2 packages [4][5]; models for Gazebo, the Stack of Tasks and MuJoCo [5][6][7].
- **Limits:** price on request, reported near €1 million [2]; 95 kg with 1.5 h of walking [1];
  whole-body control is a paid add-on [1]; rare, at six research centres by a 2025 count [8];
  simulation is Gazebo Classic only [5].

## Related robots

- [Boston Dynamics Atlas](boston-dynamics-atlas.md): the DRC humanoid whose lessons fed TALOS [3].
- [iCub](icub.md): another European research humanoid.
- [Unitree H1](unitree-h1.md) and [Fourier GR-1](fourier-gr-1.md): newer full-size humanoids.

## Sources

1. [PAL Robotics: TALOS product page](https://pal-robotics.com/robots/talos/), accessed 2026-11-18
2. [IEEE Spectrum: TALOS humanoid now available from PAL Robotics (2017-03-07)](https://spectrum.ieee.org/talos-humanoid-now-available-from-pal-robotics), accessed 2026-11-18
3. [Stasse et al.: TALOS, a new humanoid research platform targeted for industrial applications (Humanoids 2017)](https://doi.org/10.1109/HUMANOIDS.2017.8246947), accessed 2026-11-18
4. [pal-robotics talos_robot (humble-devel)](https://github.com/pal-robotics/talos_robot), accessed 2026-11-18
5. [pal-robotics talos_simulation (humble-devel)](https://github.com/pal-robotics/talos_simulation), accessed 2026-11-18
6. [stack-of-tasks talos-data README](https://github.com/stack-of-tasks/talos-data), accessed 2026-11-18
7. [MuJoCo Menagerie: pal_talos](https://github.com/google-deepmind/mujoco_menagerie/tree/main/pal_talos), accessed 2026-11-18
8. [TU Darmstadt: Extraordinary employee, humanoid robot TALOS (2025-02-28)](https://www.tu-darmstadt.de/universitaet/aktuelles_meldungen/news_archive/news_details_en_496896.en.jsp), accessed 2026-11-18
