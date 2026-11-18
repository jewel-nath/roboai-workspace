---
type: robot
name: Unitree G1
summary: 1.32 m, 35 kg research humanoid from Unitree with 23 to 43 DoF; the EDU editions open the SDK, and Unitree publishes BSD-3 SDK headers, ROS 2 messages, URDF/MJCF models, RL and teleop code.
tags: [humanoid, unitree, g1, g1-edu, unitree-sdk2, ros2, dds, mujoco, isaac-gym, reinforcement-learning, teleoperation, commercial]
category: humanoid
tier: B
openness: software-only
maker: Unitree Robotics
year: 2024
license: {hardware: , software: BSD-3-Clause, docs: }
links: {repo: "https://github.com/unitreerobotics/unitree_ros2", docs: "https://support.unitree.com/home/en/G1_developer", cad: , paper: , site: "https://www.unitree.com/g1"}
specs: {dof: 29, payload_kg: 3, reach_mm: , mass_kg: 35, size_mm: , speed_mps: , runtime_h: 2}
stack: {actuators: "Unitree joint motors in five sizes (5010-16, 5019-16, 6010-32, 7519-14.3, 7519-22.5), two encoders per joint", mcu: , compute: "NVIDIA Jetson Orin NX, 100 TOPS (EDU)", sensors: ["Livox MID-360 3D lidar", "Intel RealSense D435i depth camera"], sim_models: ["URDF and MJCF (unitree_ros g1_description: 23 and 29 DoF, hand variants)", "MJCF and MJX (MuJoCo Menagerie unitree_g1)", "URDF and MJCF (unitree_rl_gym: 12, 23 and 29 DoF)"], ros2: official}
cost: {type: retail, usd: 53900, as_of: 2026-11-18, source: "https://www.robotshop.com/products/unitree-g1-edu-advanced-u2-humanoid-robot-us"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-07-02, stars: 899, active: true}
use_cases: [research, reinforcement-learning, locomotion, teleop, imitation-learning, data-collection]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://www.robotshop.com/products/unitree-g1-edu-advanced-u2-humanoid-robot-us", title: "RobotShop: Unitree G1 EDU Advanced (U2)", accessed: 2026-11-18}
  - {url: "https://heise.de/-9720187", title: "heise online: Humanoid robot Unitree G1 costs 16,000 dollars (2024-05-16)", accessed: 2026-11-18}
  - {url: "https://github.com/unitreerobotics/unitree_sdk2", title: unitree_sdk2 repository, accessed: 2026-11-18}
  - {url: "https://github.com/unitreerobotics/unitree_ros2", title: unitree_ros2 README, accessed: 2026-11-18}
  - {url: "https://github.com/unitreerobotics/unitree_ros/tree/master/robots/g1_description", title: "unitree_ros: g1_description", accessed: 2026-11-18}
  - {url: "https://github.com/unitreerobotics/unitree_rl_gym", title: unitree_rl_gym README, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/unitree_g1", title: "MuJoCo Menagerie: unitree_g1", accessed: 2026-11-18}
  - {url: "https://github.com/unitreerobotics/xr_teleoperate", title: xr_teleoperate README, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2502.01143", title: "He et al., ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills (2025)", accessed: 2026-11-18}
  - {url: "https://www.robotshop.com/products/unitree-g1-edu-standard-u1-humanoid-robot-us", title: "RobotShop: Unitree G1 EDU Standard (U1)", accessed: 2026-11-18}
---

# Unitree G1

A compact humanoid from Unitree Robotics of Hangzhou, China, shown at ICRA 2024 at $16,000 for the
base model [2]. Only the EDU editions add SDK access [10]; they are the G1s in most humanoid-learning
papers. The hardware is closed; the SDK headers, ROS 2 messages, models and training code are open.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | G1 EDU Advanced (U2), 29 DoF, no hands | [1] |
| Degrees of freedom | 6 per leg, 3 at the waist, 7 per arm; `dof: 29` counts these joints | [1] |
| Height, mass | 1320 mm standing, 690 mm folded; 35 kg or more with battery (maker's claims) | [1][2] |
| Torque, payload | up to 120 N·m at the knee; about 3 kg per arm (maker's claims) | [1] |
| Battery, runtime | 9000 mAh, swappable; about 2 h | [2][1] |
| Compute | NVIDIA Jetson Orin NX, 100 TOPS | [1] |
| Sensors | Livox MID-360 3D lidar; Intel RealSense D435i depth camera | [1] |

## How it works

The joints use Unitree motors in five sizes, rated 13.4 to 121 N·m in the model repo's motor table,
the largest at hip and knee [5]. Each joint has two encoders [1].

Control goes through unitree_sdk2, a C++ SDK on CycloneDDS: the headers and examples are
BSD-3-Clause, but the core ships as prebuilt static libraries for x86-64 and aarch64 [3]. Its G1
examples cover locomotion and arm commands, low-level joint control and the Dex3 hand [3].
unitree_ros2 lets ROS 2 nodes (Foxy, or Humble as recommended) use the robot's DDS topics
directly, with the humanoid messages in the `unitree_hg` package [4].

unitree_ros holds URDF and MJCF files for 23- and 29-DoF G1s, with and without hands [5]. Menagerie's
`unitree_g1` comes from the 29-DoF file, with an MJX version MuJoCo Playground ran on hardware [7].

| Variant | DoF | Notes | Price, USD | Source |
|---|---|---|---|---|
| G1 (base) | 23 | no SDK access for own code | 16,000 launch list price, May 2024 | [2][10] |
| G1 EDU Standard (U1) | 23 | 5-DoF arms; adds SDK access | 43,900 retail, 2026-11-18 | [10] |
| G1 EDU Advanced (U2) | 29 | 3-DoF waist, 7-DoF arms | 53,900 retail, 2026-11-18 | [1] |
| With dexterous hands | up to 43 | Unitree's Dex3 hand has SDK examples | — | [2][3] |

## What it is used for

- Learned locomotion: unitree_rl_gym trains in Isaac Gym, checks in MuJoCo and deploys to the G1 [6].
- Agile whole-body skills: ASAP (2025) moved policies from Isaac Gym to a real G1 [9].
- Teleoperation and data collection: xr_teleoperate drives the arms and hands from Apple Vision
  Pro, PICO 4 Ultra Enterprise or Meta Quest 3 and records episodes [8].

## Cost and BOM

Retail at RobotShop, which calls itself an authorized distributor, on 2026-11-18: U2 $53,900 and
U1 $43,900, both special order [1][10]. The base G1 launched at $16,000 [2].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| SDK | C++ headers and examples; prebuilt static library | [unitree_sdk2](https://github.com/unitreerobotics/unitree_sdk2) [3] | BSD-3-Clause; core library binary only |
| ROS 2 messages, examples | ROS 2 packages | [unitree_ros2](https://github.com/unitreerobotics/unitree_ros2) [4] | BSD-3-Clause |
| Models | URDF, MJCF | unitree_ros [5], Menagerie `unitree_g1` [7] | BSD-3-Clause |
| RL and teleop code | Python | unitree_rl_gym [6], xr_teleoperate [8] | BSD-3-Clause; Apache-2.0 |
| Hardware, motor firmware | — | Not published | Closed |

## Strengths and limits

- **Strengths:** a small humanoid with an official SDK and ROS 2 messages [3][4], maker-kept models
  in many configurations [5], a Menagerie model with MJX [7], and open RL and teleop pipelines
  [6][8] that papers build on [9].
- **Limits:** hardware and firmware are closed and the SDK core is a binary [3]; the base edition
  has no SDK access [10]; 120 N·m knee torque, about 3 kg per arm [1] and about 2 h per battery [2].

## Related robots

- [Unitree H1](unitree-h1.md): Unitree's full-size humanoid on the same SDK [3].
- [Booster T1](booster-t1.md), [AgiBot X1](agibot-x1.md) and [Fourier GR-1](fourier-gr-1.md):
  other research humanoids. [Berkeley Humanoid Lite](berkeley-humanoid-lite.md): one you can build.

## Sources

1. [RobotShop: Unitree G1 EDU Advanced (U2)](https://www.robotshop.com/products/unitree-g1-edu-advanced-u2-humanoid-robot-us), accessed 2026-11-18
2. [heise online: Humanoid robot Unitree G1 costs 16,000 dollars (2024-05-16)](https://heise.de/-9720187), accessed 2026-11-18
3. [unitree_sdk2 repository](https://github.com/unitreerobotics/unitree_sdk2), accessed 2026-11-18
4. [unitree_ros2 README](https://github.com/unitreerobotics/unitree_ros2), accessed 2026-11-18
5. [unitree_ros: g1_description](https://github.com/unitreerobotics/unitree_ros/tree/master/robots/g1_description), accessed 2026-11-18
6. [unitree_rl_gym README](https://github.com/unitreerobotics/unitree_rl_gym), accessed 2026-11-18
7. [MuJoCo Menagerie: unitree_g1](https://github.com/google-deepmind/mujoco_menagerie/tree/main/unitree_g1), accessed 2026-11-18
8. [xr_teleoperate README](https://github.com/unitreerobotics/xr_teleoperate), accessed 2026-11-18
9. [He et al., ASAP: Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills (2025)](https://arxiv.org/abs/2502.01143), accessed 2026-11-18
10. [RobotShop: Unitree G1 EDU Standard (U1)](https://www.robotshop.com/products/unitree-g1-edu-standard-u1-humanoid-robot-us), accessed 2026-11-18
