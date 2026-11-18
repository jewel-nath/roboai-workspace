---
type: robot
name: Boston Dynamics Atlas
summary: Boston Dynamics' humanoid line, covering the 28-DoF hydraulic DRC Atlas (2013) that DARPA Robotics Challenge teams shared, its 2016 redesign known for parkour (retired in 2024), and the electric Atlas factory product (2026); never sold to the public, with DRC-era Gazebo and URDF models open.
tags: [humanoid, hydraulic, darpa-robotics-challenge, drc, boston-dynamics, gazebo, drake, electric-atlas, commercial]
category: humanoid
tier: B
openness: closed-reference
maker: Boston Dynamics
year: 2013
license: {hardware: , software: Apache-2.0, docs: }
links: {repo: "https://github.com/osrf/drcsim", docs: , cad: , paper: , site: "https://bostondynamics.com/atlas"}
specs: {dof: 28, payload_kg: , reach_mm: , mass_kg: 155, size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "28 hydraulic actuators fed by an onboard electric pump", mcu: , compute: "onboard real-time computer running Boston Dynamics' proprietary software; team computers off-board over a 10 Gbit/s fibre link", sensors: ["Carnegie Robotics sensor head: lidar and stereo cameras", "LVDT joint position sensors", "actuator pressure sensors for joint force"], sim_models: ["URDF/Xacro and Gazebo (osrf/drcsim atlas_description, Atlas v1 to v5, ROS 1)", "URDF (RobotLocomotion/models atlas, Drake)", "URDF (openai/roboschool atlas_description, Atlas v4)"], ros2: none}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2016-07-13, stars: 21, active: false}
use_cases: [research, competition, locomotion, manipulation, teleop]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://www.darpa.mil/news/2013/atlas-robot-unveiled", title: "DARPA: Atlas robot unveiled (2013-07-11)", accessed: 2026-11-18}
  - {url: "https://www.darpa.mil/news/2015/atlas-robot-wireless", title: "DARPA: upgraded Atlas robot goes wireless (2015-01-20)", accessed: 2026-11-18}
  - {url: "https://spectrum.ieee.org/next-generation-of-boston-dynamics-atlas-robot", title: "IEEE Spectrum: Next generation of Boston Dynamics' Atlas robot (2016-02-23)", accessed: 2026-11-18}
  - {url: "https://spectrum.ieee.org/boston-dynamics-atlas-retires", title: "IEEE Spectrum: Boston Dynamics retires its legendary humanoid robot (2024-04-16)", accessed: 2026-11-18}
  - {url: "https://bostondynamics.com/wp-content/uploads/2026/01/atlas-spec-sheet.pdf", title: "Boston Dynamics: Atlas spec sheet (January 2026)", accessed: 2026-11-18}
  - {url: "https://robotsguide.com/robots/atlas", title: "IEEE Robots guide: Atlas", accessed: 2026-11-18}
  - {url: "https://dair.seas.upenn.edu/assets/pdf/Fallon2015.pdf", title: "Fallon et al.: An Architecture for Online Affordance-based Perception and Whole-body Planning (MIT, DRC Trials)", accessed: 2026-11-18}
  - {url: "https://github.com/osrf/drcsim", title: OSRF DRC Simulator (drcsim) repository, accessed: 2026-11-18}
  - {url: "https://github.com/robot-descriptions/robot_descriptions.py", title: robot_descriptions model list, accessed: 2026-11-18}
---

# Boston Dynamics Atlas

Boston Dynamics' humanoid line. The hydraulic Atlas was built for the DARPA Robotics Challenge
(DRC): DARPA gave it to the seven teams that won the 2013 simulation round [1]. Its 2016 redesign
became known for running, dancing and parkour videos [3][4]. Boston Dynamics retired the hydraulic
Atlas on 16 April 2024 [4] and unveiled an electric Atlas that month, now a factory product [5][6].
No Atlas was sold to the public; builders meet it through DRC papers and models.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | DRC Atlas (2013–2015), the hydraulic version with public models | [1][8] |
| Degrees of freedom | 28 hydraulic joints: 6 per leg and per arm, 3 in the back, 1 in the neck; hands not counted | [1][7] |
| Height | 1.88 m (6 ft 2 in) | [2][7] |
| Mass | about 155 kg without hands (frontmatter value) [7]; DARPA gave 330 lb in 2013 [1] | [1][7] |
| Power, 2013 | tether carrying three-phase power for the onboard electric hydraulic pump, cooling water and a 10 Gbit/s fibre link | [7] |
| Sensing | Carnegie Robotics head with lidar and stereo; LVDT joint positions; joint forces from actuator pressure; joint data at 1 kHz on the robot | [1][7] |
| Hands | none built in; DARPA supplied iRobot and Sandia hands, and teams also fitted Robotiq hands and hooks | [1][7] |
| Electric Atlas (maker's claims) | 50 kg instant and 30 kg sustained lift, 20 kg one-handed; 2.3 m reach | [5] |

## How it works

Hydraulic actuators give the DRC Atlas large forces at high bandwidth, up to several hundred N·m in
the leg joints [7]. Boston Dynamics' software ran on the robot and stayed closed; teams got a minimal
interface for behaviour-level commands (balance, step, walk) or low-level control of all 28 actuators
from their own computers [7]. MIT, for example, built its planner on its open Drake and LCM tools [7].

Models: OSRF's DRC simulator holds Gazebo models of Atlas v1 to v5 with iRobot, Sandia and Robotiq
hands, Apache-2.0; it is ROS 1 and last changed in 2016 [8]. robot_descriptions loads MIT's Drake
URDF (BSD-3-Clause) and the roboschool Atlas v4 URDF (MIT) [9]; neither it nor MuJoCo Menagerie
lists the 2016 or electric Atlas (checked 2026-11-18). There is no ROS 2 driver.

| Version | Years | Actuation and power | Height | Mass | DoF | Source |
|---|---|---|---|---|---|---|
| Atlas (DRC Trials) | 2013 | hydraulic, tethered | 1.88 m | 330 lb | 28 | [1][7] |
| Atlas Unplugged (DRC Finals) | 2015 | hydraulic, 3.7 kWh battery, about 1 h; electric lower arms | 1.88 m | 156.5 kg | 28 plus an extra wrist joint | [2] |
| Next-generation Atlas | 2016–2024 | hydraulic, battery powered | 1.75 m | 82 kg | — | [3][4] |
| Electric Atlas | unveiled 2024; product 2026 | electric; 4 h battery (2 h heavy lifting), 3 min self battery swap | 1.9 m | 90 kg | 56 | [5][6] |

## What it is used for

- The DRC: seven teams received Atlas in 2013 and the rebuilt Atlas Unplugged in 2015 [1][2]; at
  the 2013 Trials, IHMC placed second and MIT fourth with Atlas [7].
- Whole-body planning and control research on the DRC models in Gazebo and Drake [7][8][9].
- Electric Atlas: factory and warehouse work such as part sequencing and machine tending [5].

## Cost and BOM

Not sold to the public, and no price was published for any version, so the frontmatter `cost`
stays empty. DRC teams received their robots from DARPA [1]; the 2026 spec sheet gives no price [5].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Hardware, robot software | — | Not published | Proprietary |
| DRC simulator with Atlas models | Gazebo, URDF/Xacro, ROS 1 | [osrf/drcsim](https://github.com/osrf/drcsim) [8] | Apache-2.0 |
| Drake Atlas model | URDF, glTF meshes | [RobotLocomotion/models](https://github.com/RobotLocomotion/models) [9] | BSD-3-Clause |
| Atlas v4 model | URDF | [openai/roboschool](https://github.com/openai/roboschool) [9] | MIT |

## Strengths and limits

- **Strengths:** a full-size hydraulic humanoid with strong, high-bandwidth joints [7]; open
  DRC-era models in Gazebo and Drake [8][9]; a large body of DRC papers, such as MIT's [7].
- **Limits:** never sold, and the hydraulic line is retired [4]; open models stop at 2015 hardware,
  on ROS 1 [8][9]; the electric Atlas is a closed industrial product with no public price [5].

## Related robots

- [PAL TALOS](pal-talos.md): a torque-controlled research humanoid that came after the DRC.
- [Agility Digit](agility-digit.md) and [Unitree H1](unitree-h1.md): electric full-size humanoids.
- [Boston Dynamics Spot](boston-dynamics-spot.md): Boston Dynamics' quadruped.

## Sources

1. [DARPA: Atlas robot unveiled (2013-07-11)](https://www.darpa.mil/news/2013/atlas-robot-unveiled), accessed 2026-11-18
2. [DARPA: upgraded Atlas robot goes wireless (2015-01-20)](https://www.darpa.mil/news/2015/atlas-robot-wireless), accessed 2026-11-18
3. [IEEE Spectrum: Next generation of Boston Dynamics' Atlas robot (2016-02-23)](https://spectrum.ieee.org/next-generation-of-boston-dynamics-atlas-robot), accessed 2026-11-18
4. [IEEE Spectrum: Boston Dynamics retires its legendary humanoid robot (2024-04-16)](https://spectrum.ieee.org/boston-dynamics-atlas-retires), accessed 2026-11-18
5. [Boston Dynamics: Atlas spec sheet (January 2026)](https://bostondynamics.com/wp-content/uploads/2026/01/atlas-spec-sheet.pdf), accessed 2026-11-18
6. [IEEE Robots guide: Atlas](https://robotsguide.com/robots/atlas), accessed 2026-11-18
7. [Fallon et al.: An Architecture for Online Affordance-based Perception and Whole-body Planning (MIT, DRC Trials)](https://dair.seas.upenn.edu/assets/pdf/Fallon2015.pdf), accessed 2026-11-18
8. [OSRF DRC Simulator (drcsim) repository](https://github.com/osrf/drcsim), accessed 2026-11-18
9. [robot_descriptions model list](https://github.com/robot-descriptions/robot_descriptions.py), accessed 2026-11-18
