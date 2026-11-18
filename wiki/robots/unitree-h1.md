---
type: robot
name: Unitree H1 and H1-2
summary: Full-size 1.8 m, 47 kg electric humanoid from Unitree with knee joints of about 360 N·m, a common body in whole-body teleoperation and RL papers; the H1-2 adds ankle roll and 7-DoF arms. SDK headers, ROS 2 messages and models are BSD-3.
tags: [humanoid, unitree, h1, h1-2, unitree-sdk2, ros2, dds, mujoco, isaac-gym, reinforcement-learning, teleoperation, commercial]
category: humanoid
tier: B
openness: software-only
maker: Unitree Robotics
year: 2023
license: {hardware: , software: BSD-3-Clause, docs: }
links: {repo: "https://github.com/unitreerobotics/unitree_ros2", docs: "https://support.unitree.com/main/en", cad: , paper: , site: "https://www.unitree.com/h1"}
specs: {dof: 19, payload_kg: , reach_mm: , mass_kg: 47, size_mm: "1805 x 570 x 220", speed_mps: 1.5, runtime_h: }
stack: {actuators: "Unitree joint motors and gearing; about 360 N·m at the knee, 220 N·m hip, 59 N·m ankle, 75 N·m arm (maker's claims)", mcu: , compute: "Intel Core i5 for motion control and Intel Core i7 for user development; Core i7 or NVIDIA Jetson Orin NX as options", sensors: ["3D lidar", "depth camera"], sim_models: ["URDF and MJCF (unitree_ros h1_description, h1_2_description, with or without hands)", "MJCF (MuJoCo Menagerie unitree_h1)", "URDF and MJCF (unitree_rl_gym: h1, h1_2)"], ros2: official}
cost: {type: retail, usd: 90000, as_of: 2024-05-15, source: "https://www.therobotreport.com/unitree-robotics-unveils-g1-humanoid-for-16k/"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-07-02, stars: 899, active: true}
use_cases: [research, reinforcement-learning, locomotion, teleop, imitation-learning, data-collection]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://www.generationrobots.com/en/404154-h1-humanoid-robot.html", title: "Generation Robots: H1 humanoid robot", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/unitree-teases-new-h1-humanoid-robot/", title: "The Robot Report: Unitree teases new H1 humanoid robot (2023-08-15)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/unitree-robotics-unveils-g1-humanoid-for-16k/", title: "The Robot Report: Unitree Robotics unveils G1 humanoid for $16k (2024-05-15)", accessed: 2026-11-18}
  - {url: "https://github.com/unitreerobotics/unitree_ros/tree/master/robots", title: "unitree_ros: robot descriptions (h1_description, h1_2_description)", accessed: 2026-11-18}
  - {url: "https://github.com/unitreerobotics/unitree_sdk2", title: unitree_sdk2 repository, accessed: 2026-11-18}
  - {url: "https://github.com/unitreerobotics/unitree_ros2", title: unitree_ros2 README, accessed: 2026-11-18}
  - {url: "https://github.com/unitreerobotics/unitree_rl_gym", title: unitree_rl_gym README, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/unitree_h1", title: "MuJoCo Menagerie: unitree_h1", accessed: 2026-11-18}
  - {url: "https://github.com/unitreerobotics/xr_teleoperate", title: xr_teleoperate README, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2403.04436", title: "He et al., Learning Human-to-Humanoid Real-Time Whole-Body Teleoperation (H2O, 2024)", accessed: 2026-11-18}
---

# Unitree H1 and H1-2

Unitree's full-size electric humanoid, about 1.8 m and 47 kg, first shown in August 2023 [2] and
priced at $90,000 in 2024 [3]. Whole-body teleoperation papers such as H2O use it [10]; the H1-2
adds 6-DoF legs and 7-DoF arms [4]. Hardware is closed; SDK headers, ROS 2 messages and models are open.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | H1 (original), 19 DoF, no hands | [4] |
| Degrees of freedom | 5 per leg and 4 per arm [2], plus one torso joint in Unitree's URDF [4] | [2][4] |
| Size, mass | 1805 x 570 x 220 mm; about 47 kg (maker's claims) | [2] |
| Peak joint torque | knee about 360 N·m, hip 220, ankle 59, arm 75 N·m (maker's claims) | [1] |
| Battery | 15 Ah, 0.864 kWh, 67.2 V maximum; runtime not stated in the sources read | [1] |
| Speed | 1.5 m/s walking; Unitree also claims a 3.3 m/s running record | [2][1] |
| Compute | Intel Core i5 for motion control, Core i7 for user code; Core i7 or Jetson Orin NX options | [1] |
| Sensors | 3D lidar and depth camera | [2] |

## How it works

Each leg has three hip joints, a knee and a single pitch ankle [1][4], driven by motors and gears
Unitree makes in-house [2]. The H1-2 adds an ankle roll joint and 3-DoF wrists, for 27 joints in
its URDF; both versions have URDFs with dexterous hands [4].

Software is the same as Unitree's other robots: unitree_sdk2, a C++ SDK on CycloneDDS with
BSD-3-Clause headers and examples but a prebuilt core library, has H1 and H1-2 locomotion and arm
examples [5]. unitree_ros2 lists the H1 among its supported robots and lets ROS 2 Foxy or Humble
nodes use the DDS topics directly; the H1-2 uses the `unitree_hg` messages [6].

Unitree's unitree_ros repo has URDF and MJCF for both versions, and also for the newer H2 [4].
MuJoCo Menagerie's `unitree_h1` was converted from a URDF Unitree supplied [8], and unitree_rl_gym
trains, plays, checks in MuJoCo and deploys policies for `h1` and `h1_2` [7].

| Variant | DoF | Notes | Source |
|---|---|---|---|
| H1 | 19 | 5-DoF legs, 4-DoF arms, 1 torso joint | [2][4] |
| H1 with hands | 19 plus hands | Unitree URDF `h1_with_hand` | [4] |
| H1-2 | 27 | 6-DoF legs, 7-DoF arms; hand and handless models | [4] |

## What it is used for

- Whole-body teleoperation: H2O (CMU, 2024) drove a real H1 from a human's motion, using the
  robot's built-in sensors for proprioception [10].
- Learned locomotion: unitree_rl_gym takes H1 and H1-2 policies from Isaac Gym to the robot [7].
- XR teleoperation and data recording for the H1 and H1-2 arms with xr_teleoperate [9].

## Cost and BOM

The Robot Report gave the H1 a base price of $90,000 in May 2024 [3], after Unitree's 2023 hint
of below $90,000 [2]. A European distributor lists it in euros, with delivery on request [1].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| SDK | C++ headers and examples; prebuilt static library | [unitree_sdk2](https://github.com/unitreerobotics/unitree_sdk2) [5] | BSD-3-Clause; core library binary only |
| ROS 2 messages, examples | ROS 2 packages | [unitree_ros2](https://github.com/unitreerobotics/unitree_ros2) [6] | BSD-3-Clause |
| Models | URDF, MJCF | unitree_ros [4], Menagerie `unitree_h1` [8] | BSD-3-Clause |
| RL and teleop code | Python | unitree_rl_gym [7], xr_teleoperate [9] | BSD-3-Clause; Apache-2.0 |
| Hardware, motor firmware | — | Not published | Closed |

## Strengths and limits

- **Strengths:** adult size with strong knees [1][2]; the same SDK, ROS 2 messages and RL code as
  Unitree's other robots [5][6][7]; maker-supplied models [4][8]; published work such as H2O [10].
- **Limits:** the original H1 has 1-DoF ankles and 4-DoF arms [1][2]; it cost over five times a
  base G1 in 2024 [3]; hardware and firmware are closed and the SDK core is a binary [5].

## Related robots

- [Unitree G1](unitree-g1.md): the smaller, cheaper Unitree humanoid on the same SDK [3][5].
- [Fourier GR-1](fourier-gr-1.md): another full-size research humanoid.
- [Booster T1](booster-t1.md) and [AgiBot X1](agibot-x1.md): smaller research humanoids.

## Sources

1. [Generation Robots: H1 humanoid robot](https://www.generationrobots.com/en/404154-h1-humanoid-robot.html), accessed 2026-11-18
2. [The Robot Report: Unitree teases new H1 humanoid robot (2023-08-15)](https://www.therobotreport.com/unitree-teases-new-h1-humanoid-robot/), accessed 2026-11-18
3. [The Robot Report: Unitree Robotics unveils G1 humanoid for $16k (2024-05-15)](https://www.therobotreport.com/unitree-robotics-unveils-g1-humanoid-for-16k/), accessed 2026-11-18
4. [unitree_ros: robot descriptions (h1_description, h1_2_description)](https://github.com/unitreerobotics/unitree_ros/tree/master/robots), accessed 2026-11-18
5. [unitree_sdk2 repository](https://github.com/unitreerobotics/unitree_sdk2), accessed 2026-11-18
6. [unitree_ros2 README](https://github.com/unitreerobotics/unitree_ros2), accessed 2026-11-18
7. [unitree_rl_gym README](https://github.com/unitreerobotics/unitree_rl_gym), accessed 2026-11-18
8. [MuJoCo Menagerie: unitree_h1](https://github.com/google-deepmind/mujoco_menagerie/tree/main/unitree_h1), accessed 2026-11-18
9. [xr_teleoperate README](https://github.com/unitreerobotics/xr_teleoperate), accessed 2026-11-18
10. [He et al., Learning Human-to-Humanoid Real-Time Whole-Body Teleoperation (H2O, 2024)](https://arxiv.org/abs/2403.04436), accessed 2026-11-18
