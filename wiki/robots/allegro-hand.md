---
type: robot
name: Allegro Hand
summary: Commercial four-finger research hand with 16 motor-driven joints from Wonik Robotics; the closed hand most open-hand papers benchmark against, with official ROS 2 drivers and models; price on request.
tags: [dexterous-hand, four-finger, direct-drive, can-bus, ros2-control, mujoco, isaac-gym, commercial]
category: gripper
tier: B
openness: software-only
maker: Wonik Robotics (older software and models carry the SimLab name)
year:
license: {hardware: , software: , docs: }
links: {repo: "https://github.com/Wonikrobotics-git/allegro_hand_ros2_v4", docs: "https://github.com/Wonikrobotics-git/allegro_hand_ros2_v4/blob/main/allegro_hand_bringup/getting_started_v4.md", cad: , paper: , site: "https://www.allegrohand.com/"}
specs: {dof: 16, payload_kg: 5, reach_mm: , mass_kg: 1.08, size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "16 geared DC motors (1:369), one per joint", mcu: , compute: "host PC over CAN (for example a PEAK PCAN-USB adapter)", sensors: ["joint potentiometers (16)"], sim_models: ["MJCF (MuJoCo Menagerie, wonik_allegro, Allegro V3)", "URDF (Wonikrobotics-git/allegro_hand_model_v4)", "URDF/Xacro with Gazebo Harmonic plugin (allegro_hand_ros2_v4)", "URDF (RobotLocomotion/models, allegro_hand_description)", "Isaac Gym task (IsaacGymEnvs, AllegroHand)", "USD for Isaac Sim (allegro_hand_ros2_v5, V5 only)"], ros2: official}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-10-29, stars: 0, active: true}
use_cases: [research, reinforcement-learning, manipulation, teleop]
evidence: vendor-claim
last_verified: 2026-11-18
sources:
  - {url: "https://www.allegrohand.com/sub/product/p.php?idx=1", title: Allegro Hand V4 product page, accessed: 2026-11-18}
  - {url: "https://www.allegrohand.com/", title: Allegro Hand website (product line), accessed: 2026-11-18}
  - {url: "https://github.com/Wonikrobotics-git/allegro_hand_ros2_v4", title: allegro_hand_ros2_v4 repository README, accessed: 2026-11-18}
  - {url: "https://github.com/Wonikrobotics-git/allegro_hand_ros2_v4/blob/main/allegro_hand_bringup/getting_started_v4.md", title: Allegro Hand V4 ROS 2 user guide, accessed: 2026-11-18}
  - {url: "https://github.com/Wonikrobotics-git/allegro_hand_ros2_v5", title: allegro_hand_ros2_v5 repository README, accessed: 2026-11-18}
  - {url: "https://github.com/Wonikrobotics-git/allegro_hand_ros2_v5/blob/master-4finger/AllegroHandV5%284F%29UserManual_v1.2.1.pdf", title: "Allegro Hand V5 (4F) user manual v1.2.1", accessed: 2026-11-18}
  - {url: "https://www.allegrohand.com/sub/product/p.php?idx=3", title: Allegro Hand V5 product page, accessed: 2026-11-18}
  - {url: "https://www.allegrohand.com/sub/product/p.php?idx=4", title: Allegro Hand V5 Plus product page, accessed: 2026-11-18}
  - {url: "https://www.allegrohand.com/sub/product/p.php?idx=22", title: Allegro Hand V5 Sense product page, accessed: 2026-11-18}
  - {url: "https://www.allegrohand.com/sub/product/p.php?idx=25", title: Allegro Hand V6 F product page, accessed: 2026-11-18}
  - {url: "https://www.venturesquare.net/en/1110501/", title: "Venture Square: Wonik Robotics launches 5-finger robot hand V6 F", accessed: 2026-11-18}
  - {url: "https://github.com/orgs/Wonikrobotics-git/repositories", title: Wonik Robotics GitHub repositories, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/wonik_allegro", title: "MuJoCo Menagerie: Allegro Hand V3 description", accessed: 2026-11-18}
  - {url: "https://github.com/Wonikrobotics-git/allegro_hand_model_v4", title: allegro_hand_model_v4 repository, accessed: 2026-11-18}
  - {url: "https://github.com/Wonikrobotics-git/allegro_hand_ros2_v4/blob/main/allegro_hand_hardwares/gazebo/plugin/readme.md", title: Allegro Hand Gazebo Harmonic plugin README, accessed: 2026-11-18}
  - {url: "https://github.com/isaac-sim/IsaacGymEnvs/blob/main/isaacgymenvs/tasks/allegro_hand.py", title: IsaacGymEnvs AllegroHand task, accessed: 2026-11-18}
  - {url: "https://github.com/Wonikrobotics-git/allegro_inhand_rotation", title: allegro_inhand_rotation repository README, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2210.04887", title: In-Hand Object Rotation via Rapid Motor Adaptation, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2309.06440", title: "LEAP Hand: Low-Cost, Efficient, and Anthropomorphic Hand for Robot Learning", accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2504.13165", title: "RUKA: Rethinking the Design of Humanoid Hands with Learning", accessed: 2026-11-18}
  - {url: "https://www.knoxlabs.com/products/wonik-robotics-allegro-hand-v4", title: Knox Labs Allegro Hand V4 listing, accessed: 2026-11-18}
  - {url: "https://github.com/RobotLocomotion/models/tree/master/allegro_hand_description", title: RobotLocomotion models, allegro_hand_description, accessed: 2026-11-18}
---

# Allegro Hand

A commercial robot hand with three fingers and a thumb, each with four joints, every joint driven by
its own geared DC motor [1]. Wonik Robotics of South Korea sells it; older software and models carry
the SimLab name [13][14]. It is the closed hand that open designs such as LEAP Hand and RUKA measure
themselves against [19][20], and Wonik publishes ROS 2 drivers and models for each version [12].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Allegro Hand V4, the four-finger version Wonik's reference learning code targets | [1][3][17] |
| Fingers and DoF | 3 fingers + thumb; 16 joints, all actuated, 4 per digit (maker's claim) | [1] |
| Actuators | DC motors, 1:369 gear ratio, max torque 0.70 N·m (maker's claim) | [1] |
| Joint speed | 0.11 s per 60° (maker's claim) | [1] |
| Joint sensing | potentiometers, 0.002° nominal resolution (maker's claim) | [1] |
| Mass | 1.08 kg: finger 0.17 kg, thumb 0.19 kg (maker's claim) | [1] |
| Payload | 5 kg (maker's claim) | [1] |
| Power | 24 V, 100 W | [1] |
| Host link | CAN at 1 Mbit/s; 333 Hz control rate | [1][4] |
| Independent tests | pull-out force 8.5 N per finger [19]; payload 3.6 kg and pinch 1.60 N [20] | [19][20] |

The maker's page gives no size. The LEAP Hand paper describes LEAP as about 30% larger than an
adult hand and similar in size to the Allegro [19].

## How it works

Each finger is a chain of four revolute joints with a motor at every joint, so there are no
tendons or coupled joints, and the host can command each joint's position or torque [1][4][20].
The hand talks to a host PC over CAN through an adapter such as the PEAK PCAN-USB, which Wonik does
not sell [4][6].

The official V4 driver, `allegro_hand_ros2_v4`, is a `ros2_control` hardware interface for ROS 2
Humble on Ubuntu 22.04 with position and effort command interfaces. It ships a position
controller, a posture controller and a grasp controller that sends torques from a grasp library
(power grasp, pinch and others), plus RViz and an RQT panel, for one or two hands [3][4]. Its
`humble` tag keeps the original `allegro_hand_ros2` release [3]. Each newer hand has its own
repository: V5 (4F) on Humble with MoveIt 2, a GUI and Isaac Sim real-to-sim and sim-to-real
tools; V6 F and V6 V on ROS 2 Jazzy [5][12]. The V5 grasp library ships as a prebuilt x86-64
binary, with a separate ARM build for boards such as Jetson [5][12].

For simulation, MuJoCo Menagerie has `wonik_allegro`, a model of the older V3 derived from SimLab's
URDF [13]. Wonik publishes V4 URDF and meshes, and the V4 ROS 2 stack adds Xacro files and a Gazebo
Harmonic plugin [14][15]. IsaacGymEnvs has an AllegroHand task, and Drake's model set has a
description [16][22].

| Variant | Digits, DoF | Mass | Payload | Bus | Notes | Source |
|---|---|---|---|---|---|---|
| V4 | 4, 16 | 1.08 kg | 5 kg | CAN, 333 Hz | potentiometers, no touch sensing | [1] |
| V5 (4F) | 4, 16 | 1.00 kg | 10 kg | CAN, 500 Hz | fingertip pressure sensors; torque-controlled | [5][6] |
| V5 Plus | 4, 16 | 1.024 kg | 15 kg | CAN, 500 Hz | geared second joint, 576.7:1, 1.84 N·m stall | [8] |
| V5 (3F) | 3, 9 | 1.05 kg | 12 kg | CAN, 500 Hz | three fingers of three joints | [7] |
| V5 Sense | 4, 16 | 1.24 kg | 15 kg | CAN, 333 Hz | 16-point fingertip and joint pressure sensing | [9] |
| V6 F | 5, 20 | 1.15 kg | 15 kg | RS-485 or Ethernet, Modbus | pressure sensing on tips, joints and palm; launched September 2026 | [10][11] |

All figures in the variant table are the maker's claims. The site also lists a V6 V with
vision-based tactile sensing, without a spec table read here [2].

## What it is used for

- **Learning in-hand manipulation:** the HORA in-hand rotation work trained in simulation and ran
  on an Allegro Hand, and Wonik now ships a reference port of it for V4 on ROS 2 Humble [17][18].
- **Baseline for open hands:** LEAP Hand and RUKA both report tests against it [19][20].
- **GPU reinforcement learning** through the IsaacGymEnvs task [16], and teleoperation through
  Wonik's teleoperation repository [12].

## Cost and BOM

Price on request: neither Wonik's site nor its product pages list a price [1][2]. On 2026-11-18 the
US distributor Knox Labs showed "pricing on request" for the V4 next to an original price of
$9,910 per hand, which included a provisional import allowance but not freight [21]. Papers quote
older figures: "over $16K" in 2023 and $15,000 in 2025 [19][20].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| V4 ROS 2 driver | ROS 2 Humble packages, URDF/Xacro | [allegro_hand_ros2_v4](https://github.com/Wonikrobotics-git/allegro_hand_ros2_v4) | "BSD" in package.xml (one package Apache 2); no licence file |
| V5 (4F) ROS 2 driver | ROS 2 Humble packages, URDF, USD | [allegro_hand_ros2_v5](https://github.com/Wonikrobotics-git/allegro_hand_ros2_v5) | BSD-2-Clause |
| V5 (4F) ROS 1 driver | ROS 1 packages | [allegro_hand_ros_v5](https://github.com/Wonikrobotics-git/allegro_hand_ros_v5) | MIT |
| V4 model | URDF, meshes | [allegro_hand_model_v4](https://github.com/Wonikrobotics-git/allegro_hand_model_v4) | MIT |
| V3 model | MJCF | MuJoCo Menagerie | BSD-2-Clause [13] |
| Grasp library | prebuilt binary | in the V5 driver repos | not stated |
| Manuals | PDF | V5 driver repo, allegrohand.com | all rights reserved [6] |
| CAD and electronics | not published | — | closed |

## Strengths and limits

- **Strengths:** every joint independently torque-controlled; an official ROS 2 driver for each
  version [12]; models for MuJoCo, Gazebo, Isaac Gym and Drake [13][15][16][22]; a large body of
  papers to compare against [19][20].
- **Limits:** price on request, and eight times LEAP Hand's cost by that paper's count [19];
  independent tests find weaker fingers than the maker's payload suggests [19][20]; no touch sensing
  on V4 [1]; four digits until V6 [10]; the Menagerie model is V3, not V4 [13]; the V4 driver has no
  licence file, and its README calls the repository private although it can be cloned publicly [3].

## Related robots

- [LEAP Hand](leap-hand.md) and [RUKA](ruka.md): open hands that benchmark against it.
- [Shadow Dexterous Hand](shadow-dexterous-hand.md): the other commercial reference hand.
- [Aero Hand Open](aero-hand-open.md) and [TriFinger](trifinger.md): open alternatives for
  dexterity research.

## Sources

1. [Allegro Hand V4 product page](https://www.allegrohand.com/sub/product/p.php?idx=1), accessed 2026-11-18
2. [Allegro Hand website (product line)](https://www.allegrohand.com/), accessed 2026-11-18
3. [allegro_hand_ros2_v4 repository README](https://github.com/Wonikrobotics-git/allegro_hand_ros2_v4), accessed 2026-11-18
4. [Allegro Hand V4 ROS 2 user guide](https://github.com/Wonikrobotics-git/allegro_hand_ros2_v4/blob/main/allegro_hand_bringup/getting_started_v4.md), accessed 2026-11-18
5. [allegro_hand_ros2_v5 repository README](https://github.com/Wonikrobotics-git/allegro_hand_ros2_v5), accessed 2026-11-18
6. [Allegro Hand V5 (4F) user manual v1.2.1](https://github.com/Wonikrobotics-git/allegro_hand_ros2_v5/blob/master-4finger/AllegroHandV5%284F%29UserManual_v1.2.1.pdf), accessed 2026-11-18
7. [Allegro Hand V5 product page](https://www.allegrohand.com/sub/product/p.php?idx=3), accessed 2026-11-18
8. [Allegro Hand V5 Plus product page](https://www.allegrohand.com/sub/product/p.php?idx=4), accessed 2026-11-18
9. [Allegro Hand V5 Sense product page](https://www.allegrohand.com/sub/product/p.php?idx=22), accessed 2026-11-18
10. [Allegro Hand V6 F product page](https://www.allegrohand.com/sub/product/p.php?idx=25), accessed 2026-11-18
11. [Venture Square: Wonik Robotics launches 5-finger robot hand V6 F](https://www.venturesquare.net/en/1110501/), accessed 2026-11-18
12. [Wonik Robotics GitHub repositories](https://github.com/orgs/Wonikrobotics-git/repositories), accessed 2026-11-18
13. [MuJoCo Menagerie: Allegro Hand V3 description](https://github.com/google-deepmind/mujoco_menagerie/tree/main/wonik_allegro), accessed 2026-11-18
14. [allegro_hand_model_v4 repository](https://github.com/Wonikrobotics-git/allegro_hand_model_v4), accessed 2026-11-18
15. [Allegro Hand Gazebo Harmonic plugin README](https://github.com/Wonikrobotics-git/allegro_hand_ros2_v4/blob/main/allegro_hand_hardwares/gazebo/plugin/readme.md), accessed 2026-11-18
16. [IsaacGymEnvs AllegroHand task](https://github.com/isaac-sim/IsaacGymEnvs/blob/main/isaacgymenvs/tasks/allegro_hand.py), accessed 2026-11-18
17. [allegro_inhand_rotation repository README](https://github.com/Wonikrobotics-git/allegro_inhand_rotation), accessed 2026-11-18
18. [In-Hand Object Rotation via Rapid Motor Adaptation](https://arxiv.org/abs/2210.04887), accessed 2026-11-18
19. [LEAP Hand: Low-Cost, Efficient, and Anthropomorphic Hand for Robot Learning](https://arxiv.org/abs/2309.06440), accessed 2026-11-18
20. [RUKA: Rethinking the Design of Humanoid Hands with Learning](https://arxiv.org/abs/2504.13165), accessed 2026-11-18
21. [Knox Labs Allegro Hand V4 listing](https://www.knoxlabs.com/products/wonik-robotics-allegro-hand-v4), accessed 2026-11-18
22. [RobotLocomotion models, allegro_hand_description](https://github.com/RobotLocomotion/models/tree/master/allegro_hand_description), accessed 2026-11-18
