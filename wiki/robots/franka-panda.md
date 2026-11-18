---
type: robot
name: Franka Emika Panda and Franka Research 3
summary: Seven-axis research arm with torque sensors in every joint and a 1 kHz control interface; the 2017 Panda is end of life and the Franka Research 3 replaces it, with Apache-2.0 libfranka, franka_ros2 and MuJoCo models.
tags: [cobot, panda, fr3, torque-sensing, 7-dof, fci, libfranka, ros2, mujoco, commercial]
category: arm
tier: B
openness: software-only
maker: Franka Emika, now Franka Robotics (Agile Robots)
year: 2017
license: {hardware: , software: Apache-2.0, docs: }
links: {repo: "https://github.com/frankarobotics/franka_ros2", docs: "https://frankarobotics.github.io/docs", cad: , paper: "https://doi.org/10.1109/MRA.2021.3138382", site: "https://franka.de"}
specs: {dof: 7, payload_kg: 3, reach_mm: 855, mass_kg: 17.8, size_mm: , speed_mps: 2, runtime_h: }
stack: {actuators: "7 joint drives with link-side torque sensors", mcu: , compute: "Franka Control unit (19-inch rack box); external Linux PC over Ethernet for the 1 kHz FCI", sensors: ["joint position sensing", "link-side joint torque sensors in all 7 axes"], sim_models: ["URDF/Xacro (franka_description: fer, fr3, fr3v2, fr3v2_1, fp3, fr3_duo)", "MJCF and MJX (MuJoCo Menagerie: franka_emika_panda, franka_fr3, franka_fr3_v2, franka_fr3_duo)", "Gazebo (franka_ros2 franka_gazebo)", "URDF and MJCF (robot_descriptions)"], ros2: community}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-10-27, stars: 396, active: true}
use_cases: [research, manipulation, imitation-learning, reinforcement-learning, data-collection, teleop, hri]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://download.franka.de/documents/100010_Product%20Manual%20Franka%20Emika%20Robot_10.21_EN.pdf", title: "Product Manual Franka Emika Robot (Panda), v10.21, October 2021", accessed: 2026-11-18}
  - {url: "https://franka.de/hubfs/Datasheet%20Franka%20Research%203_R02212_2.6_EN_July%202026.pdf", title: "Datasheet Franka Research 3, Arm v2.1 and v2.2 (R02212 2.6, July 2026)", accessed: 2026-11-18}
  - {url: "https://franka.de/hubfs/Datasheet%20Franka%20Research%203_R02212_1.4_EN_June%202026.pdf", title: "Datasheet Franka Research 3, Arm v1 (R02212 1.4, June 2026)", accessed: 2026-11-18}
  - {url: "https://franka.de/documents", title: Franka Robotics product documentation page, accessed: 2026-11-18}
  - {url: "https://franka.de/franka-research-3", title: Franka Research 3 product page, accessed: 2026-11-18}
  - {url: "https://ramagazine.ieee.org/2024/12/12/the-franka-emika-robot-a-standard-platform-in-robotics-research-survey/", title: "IEEE RAM: The Franka Emika Robot, a standard platform in robotics research (survey, 2024)", accessed: 2026-11-18}
  - {url: "https://doi.org/10.1109/MRA.2021.3138382", title: "The Franka Emika Robot: A Reference Platform for Robotics Research and Education (IEEE RAM, 2022)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/agile-robots-acquires-franka-emika/", title: "The Robot Report: Agile Robots acquires Franka Emika", accessed: 2026-11-18}
  - {url: "https://github.com/frankarobotics/libfranka", title: libfranka README and changelog, accessed: 2026-11-18}
  - {url: "https://github.com/frankarobotics/franka_ros2", title: franka_ros2 README and changelog, accessed: 2026-11-18}
  - {url: "https://github.com/frankarobotics/franka_description", title: franka_description README, accessed: 2026-11-18}
  - {url: "https://github.com/srl-ethz/multipanda_ros2", title: multipanda_ros2 repository README, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie", title: "MuJoCo Menagerie model list (franka_emika_panda, franka_fr3, franka_fr3_v2, franka_fr3_duo)", accessed: 2026-11-18}
  - {url: "https://github.com/robot-descriptions/robot_descriptions.py", title: robot_descriptions model list, accessed: 2026-11-18}
  - {url: "https://droid-dataset.github.io/", title: DROID dataset project page, accessed: 2026-11-18}
  - {url: "https://github.com/real-stanford/universal_manipulation_interface", title: Universal Manipulation Interface repository README, accessed: 2026-11-18}
  - {url: "https://wuphilipp.github.io/gello_site/", title: GELLO project page, accessed: 2026-11-18}
  - {url: "https://spectrum.ieee.org/franka-a-robot-arm-thats-safe-low-cost-and-can-replicate-itself", title: "IEEE Spectrum: Franka, a robot arm that's safe, low cost, and can replicate itself (29 December 2016)", accessed: 2026-11-18}
---

# Franka Emika Panda and Franka Research 3

A seven-axis arm with a torque sensor in every joint and a 1 kHz low-level control interface, made
by the Munich start-up Franka Emika and introduced in 2017 [6][18]. It became one of the standard
arms of manipulation and robot-learning research [6]. **The Panda is end of life**: Franka Robotics
(formerly Franka Emika, bought by Agile Robots in 2023) lists it only as a legacy product and sells
the Franka Research 3 (FR3) instead [4][8][13].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Panda (Franka Emika Robot, `fer`); FR3 values in the variant table | [1] |
| Degrees of freedom | 7 revolute joints; the two-finger hand is an add-on, so `dof: 7` | [1] |
| Payload | 3 kg (maker's claim) | [1] |
| Reach | 855 mm (maker's claim) | [1] |
| Mass | ~17.8 kg arm; ~7 kg control unit (maker's claims) | [1] |
| Pose repeatability | below ±0.1 mm, ISO 9283 (maker's claim) | [1] |
| Joint limits | A1, A3, A5, A7 ±166°; A2 ±101°; A4 −176° to −4°; A6 −1° to 215° | [1] |
| Joint speed limits | A1–A4 150°/s; A5–A7 180°/s | [1] |
| Cartesian speed | up to 2 m/s at the end effector (maker's claim) | [1] |
| Joint torque limits | A1–A4 87 Nm; A5–A7 12 Nm | [1] |
| Torque sensing | link-side sensors in all 7 joints; 0.02 Nm resolution; collision detection under 2 ms (maker's claims) | [1] |
| Control interface | Franka Control Interface (FCI) at 1 kHz | [1][7] |
| Protection, power | arm IP30; up to ~350 W, ~60 W typical | [1] |

## How it works

Each of the seven joints carries a link-side torque sensor, so the arm can sense contact along the
whole arm, not only at a wrist sensor; the manual gives torque resolution, force accuracy and
collision reaction times for it [1]. The arm runs from a 19-inch control unit. Users program it
at three levels: Desk, an app-based interface for task programming; RIDE, a command-based
environment for custom skills; and FCI, which streams joint torque, position or velocity and
Cartesian pose or velocity commands at 1 kHz from an external PC [1][5][7].

FCI is driven by libfranka, a C++ library with Python bindings (pylibfranka), and franka_ros2 wraps
it in ros2_control [9][10]. libfranka 0.9.x was the last release for Panda system software;
0.10.0 (September 2022) switched to FR3 system software, and franka_ros2 has required 0.10.0 or
later since its first release, so it does not drive a real Panda [9][10]. franka_description still
ships the Panda model but says issues against it will not be fixed [11]. For a Panda on ROS 2 there
is community work such as multipanda_ros2, tested with Panda system 4.2.1 and 4.2.2 and libfranka
0.9.2 [12]; that is why `stack.ros2` says `community` for the Panda.

For simulation, franka_description generates URDFs for every arm type, franka_ros2 has a Gazebo
bringup, and MuJoCo Menagerie carries the Panda (with MJX variants), FR3, FR3 v2 and the dual-arm
FR3 Duo, all Apache-2.0 [10][11][13]. robot_descriptions loads URDF and MJCF versions [14].

| Arm | Model id | Mass | Joint limits that differ from Panda | Status | Source |
|---|---|---|---|---|---|
| Panda (Franka Emika Robot) | `fer` | ~17.8 kg | — | End of life | [1][4][11] |
| FR3, Arm v1 | `fr3` (Desk: Arm3R) | ~17.8 kg | A2 ±105°; A4 −176° to −7°; A5 ±165°; A6 25° to 265°; A7 ±175° | Earlier FR3 arm | [3][11] |
| FR3, Arm v2.1 / v2.2 | `fr3v2`, `fr3v2_1` (Desk: Arm3Rv2, Arm3Rv2.1) | ~18.3 kg | Same as FR3 Arm v1 | Current datasheet, July 2026 | [2][11] |

Both FR3 datasheets read keep the 3 kg payload, 855 mm reach and ±0.1 mm repeatability, and rate
the arm IP40 [2][3]. The current FR3 datasheet gives joint speeds of 150°/s for A1–A4 and 301°/s for A5–A7
(239°/s for A6 under FCI) [2]. An Arm v2.0 has its own datasheet, not read for this card [4].
franka_description also models an `fp3` arm, the dual-arm FR3 Duo and a mobile base (`tmrv0_2`)
[11].

## What it is used for

- Manipulation, control, HRI and robot learning: Sami Haddadin's 2024 survey describes it as a
  reference platform across AI and machine learning, manipulation, control, HRI and motion
  planning [6].
- Large datasets: DROID collected 76k demonstrations, about 350 hours across 564 scenes, on Franka
  Panda arms [15].
- Data-collection and teleoperation tools target it: the Universal Manipulation Interface deploys
  policies on Franka arms, and GELLO's leader arm was built for the Franka, UR5 and xArm [16][17].

## Cost and BOM

Price on request: the FR3 page has only a quote form [5], so the frontmatter `cost` stays empty. At
launch, IEEE Spectrum reported a not-yet-confirmed Panda preorder price of €9,900, "or about
$10,500" (December 2016) [18]. The Panda is end of life [4], so a Panda now means a used arm;
check its system version, since that decides which libfranka release can drive it [9].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| FCI client library | C++, Python bindings | [libfranka](https://github.com/frankarobotics/libfranka) [9] | Apache-2.0 |
| ROS 2 driver, controllers, MoveIt, Gazebo | ROS 2 packages | [franka_ros2](https://github.com/frankarobotics/franka_ros2) [10] | Apache-2.0 |
| Robot descriptions and meshes | URDF/Xacro, DAE/STL | [franka_description](https://github.com/frankarobotics/franka_description) [11] | Apache-2.0 |
| Community Panda ROS 2 stack | ROS 2 packages, MuJoCo | [multipanda_ros2](https://github.com/srl-ethz/multipanda_ros2) [12] | Apache-2.0 |
| MuJoCo models | MJCF, MJX | Menagerie `franka_emika_panda`, `franka_fr3`, `franka_fr3_v2`, `franka_fr3_duo` [13] | Apache-2.0 |
| Arm hardware, robot firmware, Desk | — | Not published; FCI must be enabled on the robot [9] | Closed |

## Strengths and limits

- **Strengths:** torque sensing in every joint and real 1 kHz torque control from your own code
  [1][7]; seven joints for redundancy; a permissive, maker-maintained software stack [9][10];
  models in Menagerie, Gazebo and robot_descriptions [10][13][14]; a large body of published work
  and datasets to compare against [6][15].
- **Limits:** only 3 kg payload [1]; the Panda is end of life and the official ROS 2 driver does not
  support it [4][10]; FCI wants a Linux PC, ideally with a PREEMPT_RT kernel, and a libfranka
  release that matches the robot's system version [9]; the Panda arm is only IP30 [1]; franka_ros2
  warns of breaking changes during rapid development [10]; price on request.

## Related robots

- [KUKA LBR iiwa](kuka-lbr-iiwa.md): the other seven-axis torque-sensing research arm, heavier and
  with more payload.
- [Kinova Gen3](kinova-gen3.md): a lighter seven-axis arm with joint torque sensors.
- [Universal Robots](universal-robots.md): six-axis industrial cobots, also used with UMI and GELLO.
- [UMI gripper](umi-gripper.md): its policies run on Franka arms [16].
- [Sawyer](sawyer.md): Rethink Robotics' seven-axis arm, another common research platform.
- [SO-101](so-101.md): a printed hobby-servo arm for imitation learning, the low-cost contrast.

## Sources

1. [Product Manual Franka Emika Robot (Panda), v10.21, October 2021](https://download.franka.de/documents/100010_Product%20Manual%20Franka%20Emika%20Robot_10.21_EN.pdf), accessed 2026-11-18
2. [Datasheet Franka Research 3, Arm v2.1 and v2.2 (R02212 2.6, July 2026)](https://franka.de/hubfs/Datasheet%20Franka%20Research%203_R02212_2.6_EN_July%202026.pdf), accessed 2026-11-18
3. [Datasheet Franka Research 3, Arm v1 (R02212 1.4, June 2026)](https://franka.de/hubfs/Datasheet%20Franka%20Research%203_R02212_1.4_EN_June%202026.pdf), accessed 2026-11-18
4. [Franka Robotics product documentation page](https://franka.de/documents), accessed 2026-11-18
5. [Franka Research 3 product page](https://franka.de/franka-research-3), accessed 2026-11-18
6. [IEEE RAM: The Franka Emika Robot, a standard platform in robotics research (survey, 2024)](https://ramagazine.ieee.org/2024/12/12/the-franka-emika-robot-a-standard-platform-in-robotics-research-survey/), accessed 2026-11-18
7. [The Franka Emika Robot: A Reference Platform for Robotics Research and Education (IEEE RAM, 2022)](https://doi.org/10.1109/MRA.2021.3138382), accessed 2026-11-18
8. [The Robot Report: Agile Robots acquires Franka Emika](https://www.therobotreport.com/agile-robots-acquires-franka-emika/), accessed 2026-11-18
9. [libfranka README and changelog](https://github.com/frankarobotics/libfranka), accessed 2026-11-18
10. [franka_ros2 README and changelog](https://github.com/frankarobotics/franka_ros2), accessed 2026-11-18
11. [franka_description README](https://github.com/frankarobotics/franka_description), accessed 2026-11-18
12. [multipanda_ros2 repository README](https://github.com/srl-ethz/multipanda_ros2), accessed 2026-11-18
13. [MuJoCo Menagerie model list (franka_emika_panda, franka_fr3, franka_fr3_v2, franka_fr3_duo)](https://github.com/google-deepmind/mujoco_menagerie), accessed 2026-11-18
14. [robot_descriptions model list](https://github.com/robot-descriptions/robot_descriptions.py), accessed 2026-11-18
15. [DROID dataset project page](https://droid-dataset.github.io/), accessed 2026-11-18
16. [Universal Manipulation Interface repository README](https://github.com/real-stanford/universal_manipulation_interface), accessed 2026-11-18
17. [GELLO project page](https://wuphilipp.github.io/gello_site/), accessed 2026-11-18
18. [IEEE Spectrum: Franka, a robot arm that's safe, low cost, and can replicate itself (29 December 2016)](https://spectrum.ieee.org/franka-a-robot-arm-thats-safe-low-cost-and-can-replicate-itself), accessed 2026-11-18
