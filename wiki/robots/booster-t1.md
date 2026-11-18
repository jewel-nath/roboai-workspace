---
type: robot
name: Booster T1
summary: 1.18 m, 30 kg research humanoid from Booster Robotics with 23 DoF, Jetson AGX Orin compute and Apache-2.0 RL training code (booster_gym); Tsinghua won RoboCup 2025 AdultSize with it, and a reseller says the T2 has replaced it.
tags: [humanoid, booster, t1, robocup, booster-gym, isaac-gym, isaac-lab, mujoco, webots, reinforcement-learning, ros2, commercial]
category: humanoid
tier: B
openness: software-only
maker: Booster Robotics
year:
license: {hardware: , software: Apache-2.0, docs: }
links: {repo: "https://github.com/BoosterRobotics/booster_gym", docs: "https://docs.booster.tech/docs/product-manual/t1/getting-started/specifications", cad: , paper: "https://arxiv.org/abs/2506.15132", site: "https://www.booster.tech/"}
specs: {dof: 23, payload_kg: , reach_mm: , mass_kg: 30, size_mm: , speed_mps: 1, runtime_h: 2}
stack: {actuators: "Booster joint actuators, peak torque 130 N·m (maker's claim)", mcu: , compute: "Standard: Intel i7 motion-control board plus NVIDIA Jetson AGX Orin 32GB (200 TOPS); Basic: Jetson AGX Orin only", sensors: ["camera", "depth camera", "microphone array"], sim_models: ["URDF and MJCF (booster_gym resources/T1)", "URDF and MJCF (booster_assets: T1 23 and 29 DoF)", "MJCF (MuJoCo Menagerie booster_t1)"], ros2: official}
cost: {type: retail, usd: 41224, as_of: 2026-11-18, source: "https://www.robotshop.com/products/booster-t1-humanoid-robot-standard"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2025-12-23, stars: 308, active: false}
use_cases: [research, reinforcement-learning, locomotion, competition]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://docs.booster.tech/docs/product-manual/t1/getting-started/specifications", title: "Booster docs: T1 Specifications", accessed: 2026-11-18}
  - {url: "https://www.robotshop.com/products/booster-t1-humanoid-robot-standard", title: "RobotShop: Booster T1 Humanoid Robot (Standard)", accessed: 2026-11-18}
  - {url: "https://github.com/BoosterRobotics/booster_gym", title: booster_gym README, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2506.15132", title: "Wang et al., Booster Gym: An End-to-End Reinforcement Learning Framework for Humanoid Robot Locomotion (2025)", accessed: 2026-11-18}
  - {url: "https://github.com/BoosterRobotics/booster_robotics_sdk", title: booster_robotics_sdk README, accessed: 2026-11-18}
  - {url: "https://github.com/BoosterRobotics/booster_robotics_sdk_ros2", title: booster_robotics_sdk_ros2 README, accessed: 2026-11-18}
  - {url: "https://github.com/BoosterRobotics/booster_assets", title: booster_assets README, accessed: 2026-11-18}
  - {url: "https://github.com/BoosterRobotics/booster_train", title: booster_train README, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/booster_t1", title: "MuJoCo Menagerie: booster_t1", accessed: 2026-11-18}
  - {url: "https://news.cgtn.com/news/2025-07-23/Two-Chinese-teams-sweep-1-2-in-adult-size-at-Robo-Cup-Humanoid-League-1FeWW0KezmM/share_amp.html", title: "CGTN: Two Chinese teams sweep 1-2 in adult size at RoboCup Humanoid League (2025-07-23)", accessed: 2026-11-18}
---

# Booster T1

A compact humanoid from Booster Robotics of Beijing, 1.18 m and about 30 kg [1], with an open RL
pipeline from training to deployment and a paper behind it [3][4]. Tsinghua won RoboCup 2025
AdultSize with T1s [10]. A reseller says the T2 has replaced it [2]; the open code and models remain.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | T1 Standard, 23 DoF, no grippers or hands | [1][2] |
| Degrees of freedom | 6 per leg, 4 per arm, 1 waist, 2 head; `dof: 23` counts these joints | [1] |
| Height, mass | 1.18 m; about 30 kg (maker's claims) | [1] |
| Peak joint torque | 130 N·m (maker's claim, via reseller) | [2] |
| Speed | walking 1 m/s; turning 1.5 rad/s (maker's claims) | [1] |
| Battery | about 2 h; charging 2 h or less | [1] |
| Compute | Standard: Intel i7 motion board and Jetson AGX Orin 32GB (200 TOPS); Basic: Orin only | [1] |
| Sensors, links | camera, depth camera, microphone array, speaker; Wi-Fi 6, Bluetooth 5.2, 2 x gigabit Ethernet | [1] |

## How it works

The Standard T1 splits the work between two boards: an Intel i7 board runs motion control and a
Jetson AGX Orin runs perception [1]. Booster's model repo also has a 29-DoF T1 with 7-DoF arms [7].

Booster's C++ SDK, built on its own copy of Fast DDS, has Apache-2.0 headers and examples, but its
core ships as prebuilt static libraries for x86-64 and aarch64; the Python SDK comes from pip [5].
Booster's ROS 2 repo adds message and service packages (LowState, LowCmd, MotorState, ImuState,
Odometer and more) and examples, with no licence declared [6].

booster_gym trains T1 walking in Isaac Gym, tests the policy in MuJoCo, then runs it in Webots and
on the robot with the same deployment script [3]; the paper reports zero-shot sim-to-real transfer
on the T1 [4]. booster_train is the newer Isaac Lab pipeline, adapting BeyondMimic motion tracking
to the T2, T1 and K1 [8]. MuJoCo Menagerie's `booster_t1` is derived from booster_gym's URDF [9].

| Variant | DoF | Notes | Source |
|---|---|---|---|
| T1 Basic | 23 | Jetson AGX Orin only | [1] |
| T1 Standard | 23 | Intel i7 motion board plus Jetson AGX Orin | [1][2] |
| T1 with 7-DoF arms (model) | 29 | head 2, arms 7 x 2, waist 1, legs 6 x 2 | [7] |

## What it is used for

- Robot soccer: Tsinghua's Hephaestus beat China Agricultural University 5-3 in the RoboCup 2025
  AdultSize final with T1s; Booster was the event's official hardware supplier [10].
- Humanoid RL research: the Booster Gym paper (2025) walks the T1 with zero-shot sim-to-real [4].
- Motion tracking from human data with booster_train [8].

## Cost and BOM

Retail at RobotShop: $41,224 for the T1 Standard as a special order on 2026-11-18, on a page that
also says the T1 is discontinued for the T2 [2]. No price from Booster itself was found.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| RL training and deployment | Python | [booster_gym](https://github.com/BoosterRobotics/booster_gym) [3], booster_train [8] | Apache-2.0 |
| SDK | C++ headers and examples; prebuilt static library | booster_robotics_sdk [5] | Apache-2.0; core library binary only |
| ROS 2 interface | ROS 2 messages, services, examples | booster_robotics_sdk_ros2 [6] | None declared |
| Models | URDF, MJCF | booster_gym [3], booster_assets [7], Menagerie [9] | Apache-2.0; BSD-3-Clause; Apache-2.0 |
| Hardware, firmware | — | Not published | Closed |

## Strengths and limits

- **Strengths:** a light humanoid with a full open RL pipeline and paper [3][4], proven in RoboCup
  play [10], Jetson AGX Orin on board [1], and models in Menagerie and booster_assets [7][9].
- **Limits:** discontinued for the T2 [2]; 4-DoF arms on the Standard [1]; 2 h runtime [1]; the
  SDK core is a binary [5] and the ROS 2 interface has no licence [6]; no official price found.

## Related robots

- [Unitree G1](unitree-g1.md): the most common compact research humanoid.
- [ROBOTIS OP3](robotis-op3.md) and [Microban](microban.md): smaller RoboCup humanoids.
- [Berkeley Humanoid Lite](berkeley-humanoid-lite.md): an open humanoid you can build.

## Sources

1. [Booster docs: T1 Specifications](https://docs.booster.tech/docs/product-manual/t1/getting-started/specifications), accessed 2026-11-18
2. [RobotShop: Booster T1 Humanoid Robot (Standard)](https://www.robotshop.com/products/booster-t1-humanoid-robot-standard), accessed 2026-11-18
3. [booster_gym README](https://github.com/BoosterRobotics/booster_gym), accessed 2026-11-18
4. [Wang et al., Booster Gym: An End-to-End Reinforcement Learning Framework for Humanoid Robot Locomotion (2025)](https://arxiv.org/abs/2506.15132), accessed 2026-11-18
5. [booster_robotics_sdk README](https://github.com/BoosterRobotics/booster_robotics_sdk), accessed 2026-11-18
6. [booster_robotics_sdk_ros2 README](https://github.com/BoosterRobotics/booster_robotics_sdk_ros2), accessed 2026-11-18
7. [booster_assets README](https://github.com/BoosterRobotics/booster_assets), accessed 2026-11-18
8. [booster_train README](https://github.com/BoosterRobotics/booster_train), accessed 2026-11-18
9. [MuJoCo Menagerie: booster_t1](https://github.com/google-deepmind/mujoco_menagerie/tree/main/booster_t1), accessed 2026-11-18
10. [CGTN: Two Chinese teams sweep 1-2 in adult size at RoboCup Humanoid League (2025-07-23)](https://news.cgtn.com/news/2025-07-23/Two-Chinese-teams-sweep-1-2-in-adult-size-at-Robo-Cup-Humanoid-League-1FeWW0KezmM/share_amp.html), accessed 2026-11-18
