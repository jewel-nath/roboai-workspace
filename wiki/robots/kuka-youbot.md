---
type: robot
name: KUKA youBot
summary: KUKA's omnidirectional teaching mobile manipulator from 2010, a mecanum-wheel base with a five-axis arm and two-finger gripper on EtherCAT; discontinued, but still a stock robot in Webots and in the Modern Robotics course's CoppeliaSim scenes.
tags: [mobile-manipulator, mecanum, omnidirectional, 5-dof, ethercat, ros1, webots, coppeliasim, robocup, discontinued, kuka]
category: mobile-manipulator
tier: B
openness: software-only
maker: KUKA
year: 2010
license: {hardware: , software: LGPL-2.1-only OR BSD-3-Clause, docs: }
links: {repo: "https://github.com/youbot/youbot_driver", docs: , cad: , paper: , site: }
specs: {dof: 10, payload_kg: 0.5, reach_mm: , mass_kg: 26, size_mm: , speed_mps: 0.8, runtime_h: }
stack: {actuators: "four wheel motors (mecanum), five arm joint motors and a gripper, all on EtherCAT", mcu: , compute: , sensors: [], sim_models: ["Webots PROTO (Youbot.proto, Webots-only licence)", "CoppeliaSim youBot scene (Modern Robotics capstone)", "URDF/xacro with Gazebo plugins (youbot_description, ROS 1)"], ros2: none}
cost: {type: retail, usd: 24200, as_of: 2010-06-11, source: "https://spectrum.ieee.org/scoop-kukas-youbot"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2013-10-10, stars: 66, active: false}
use_cases: [education, research, manipulation, navigation, competition]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://spectrum.ieee.org/scoop-kukas-youbot", title: "IEEE Spectrum: Scoop: KUKA's youBot (2010-06-11)", accessed: 2026-11-18}
  - {url: "https://github.com/youbot/youbot_driver", title: "youbot_driver repository (youBot API)", accessed: 2026-11-18}
  - {url: "https://github.com/youbot/youbot_description", title: "youbot_description repository (hydro-devel)", accessed: 2026-11-18}
  - {url: "https://github.com/cyberbotics/webots/blob/master/projects/robots/kuka/youbot/protos/Youbot.proto", title: "Webots: Youbot PROTO", accessed: 2026-11-18}
  - {url: "http://hades.mech.northwestern.edu/index.php/Mobile_Manipulation_Capstone", title: "Modern Robotics: Mobile Manipulation Capstone (Northwestern)", accessed: 2026-11-18}
  - {url: "https://lists.robocup.org/archives/list/rc-work@lists.robocup.org/thread/YDRGSB3A3XD5MIGZOBLNLLZSSQ2ZYCFB/", title: "RoboCup@Work mailing list: alternatives to the youBot (2019)", accessed: 2026-11-18}
---

# KUKA youBot

The youBot is a small mobile manipulator that KUKA introduced at Automatica in Munich in June 2010 for
research and teaching: an omnidirectional base carrying a five-axis arm with a two-finger gripper [1].
It is **discontinued**; no source we found gives the date, and by March 2019 RoboCup@Work teams were
asking for replacements [6]. A builder meets it today mostly in simulation: Webots ships a youBot model,
and the Modern Robotics course drives one in CoppeliaSim [4][5].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | youBot with one arm: base, 5-DoF arm and gripper | 1 |
| Degrees of freedom | 4 wheels + 5 arm joints + gripper counted as one; `dof: 10` | 1, 5 |
| Base | Omnidirectional; 20 kg; 20 kg payload; 0.8 m/s (maker's claims) | 1 |
| Wheels | Four mecanum wheels; 0.47 m x 0.30 m wheel spacing, 47.5 mm radius in the course model | 5 |
| Arm | 5 DoF; 6 kg; 0.5 kg payload; 0.1 mm repeatability (maker's claims) | 1 |
| Arm size | 655 mm tall; 0.513 m³ work envelope; no reach figure given | 1 |
| Total mass | 26 kg (base 20 kg plus arm 6 kg, our sum) | 1 |
| Bus | EtherCAT from a Linux PC, through the bundled SOEM master | 2 |
| Gripper | Two fingers; the driver models it as a one-DoF gripper | 1, 2 |

## How it works

Four mecanum wheels let the base move in any direction; the driver's base kinematics class is named for
four "Swedish" (mecanum) wheels [2][5]. IEEE Spectrum calls them KUKA omniWheels [1]. The arm sits on
top of the base with five revolute joints [5]. A dual-arm version exists as a model in
`youbot_description` [3].

The youBot API, from Hochschule Bonn-Rhein-Sieg, treats the arm and base as sets of joints, each a
motor plus gearbox, and drives them over EtherCAT; it needs Linux and root access to the Ethernet
port [2]. The ROS wrapper and descriptions are ROS 1 only: the driver's last commit is from 2013 and
`youbot_description` (catkin, Gazebo plugins) from 2015 [2][3]. We found no ROS 2 driver.

Models: Webots ships a `Youbot` PROTO whose header says it is licensed for use only with Webots [4];
the Modern Robotics capstone drives a youBot scene in CoppeliaSim [5]; `youbot_description` has URDF
for the full robot, arm only, base only and dual arm [3]. Neither MuJoCo Menagerie nor
robot_descriptions has a youBot.

| Variant | Parts | Launch price (2010) | Source |
|---|---|---|---|
| youBot | Base, one arm, gripper | EUR 19,990 (USD 24,200) | 1 |
| youBot arm | Arm and gripper | EUR 12,990 (USD 15,700) | 1 |
| youBot base | Omnidirectional base | EUR 8,990 (USD 10,900) | 1 |
| Dual-arm youBot | Base and two arms | model only in our sources | 3 |

## What it is used for

- **Teaching mobile manipulation:** in the Coursera Modern Robotics capstone, students write trajectory
  generation, odometry and feedback control so a simulated youBot moves a cube in CoppeliaSim [5].
- **RoboCup@Work:** teams competed with youBots and still used them in 2019 despite the arm's limited
  range [6].
- **Simulation:** Webots keeps a youBot in its robot library [4].

## Cost and BOM

No longer sold new [6]. At launch the full robot listed at EUR 19,990, which IEEE Spectrum gave as
USD 24,200, with 20–25% off for early buyers and universities [1]. That launch price is the
frontmatter `cost` (type `retail`, dated 2010-06-11).

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| youBot API driver | C++ | [youbot_driver](https://github.com/youbot/youbot_driver) [2] | Dual: LGPL-2.1 or BSD-3-Clause |
| ROS 1 description | URDF/xacro, Gazebo | [youbot_description](https://github.com/youbot/youbot_description) [3] | GPL-3.0 (package.xml) |
| Webots model | Webots PROTO | Webots repository [4] | For use only with Webots |
| Hardware, motor controller firmware | | | Closed |

## Strengths and limits

- **Strengths:** a compact omnidirectional mobile manipulator with an open C++ EtherCAT driver [1][2];
  ready models in Webots, CoppeliaSim and URDF make it a free simulation target [3][4][5].
- **Limits:** discontinued [6]; a small arm with 0.5 kg payload and limited range [1][6]; drivers
  stuck on ROS 1 since 2013–2015 [2][3]; the Webots model is not open [4].

## Related robots

- [Fetch](fetch.md) and [TIAGo](tiago.md): mobile manipulators suggested as youBot replacements [6].
- [Clearpath research bases](clearpath-robots.md): the Ridgeback is a larger mecanum base sold with arms.
- [Hello Robot Stretch](hello-robot-stretch.md): a current single-arm mobile manipulator.

## Sources

1. [IEEE Spectrum: Scoop: KUKA's youBot (2010-06-11)](https://spectrum.ieee.org/scoop-kukas-youbot), accessed 2026-11-18
2. [youbot_driver repository (youBot API)](https://github.com/youbot/youbot_driver), accessed 2026-11-18
3. [youbot_description repository (hydro-devel)](https://github.com/youbot/youbot_description), accessed 2026-11-18
4. [Webots: Youbot PROTO](https://github.com/cyberbotics/webots/blob/master/projects/robots/kuka/youbot/protos/Youbot.proto), accessed 2026-11-18
5. [Modern Robotics: Mobile Manipulation Capstone (Northwestern)](http://hades.mech.northwestern.edu/index.php/Mobile_Manipulation_Capstone), accessed 2026-11-18
6. [RoboCup@Work mailing list: alternatives to the youBot (2019)](https://lists.robocup.org/archives/list/rc-work@lists.robocup.org/thread/YDRGSB3A3XD5MIGZOBLNLLZSSQ2ZYCFB/), accessed 2026-11-18
