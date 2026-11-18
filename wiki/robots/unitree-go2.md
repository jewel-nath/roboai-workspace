---
type: robot
name: Unitree Go1 and Go2
summary: Unitree's low-cost quadrupeds and the common entry-level research platform; the Go2 EDU adds foot force sensors, a depth camera and an optional Orin compute module, with Unitree's own ROS 2 and SDK2 interfaces and MuJoCo and Isaac Lab models.
tags: [quadruped, unitree, go1, go2, go2-edu, unitree-sdk2, ros2, lidar, mujoco, isaac-lab, commercial]
category: legged
tier: B
openness: software-only
maker: Unitree Robotics
year: 2023
license: {hardware: , software: BSD-3-Clause, docs: }
links: {repo: "https://github.com/unitreerobotics/unitree_ros2", docs: "https://github.com/unitreerobotics/unitree_sdk2", cad: , paper: , site: "https://www.unitree.com/go2/"}
specs: {dof: 12, payload_kg: , reach_mm: , mass_kg: 15, size_mm: "700 x 310 x 400", speed_mps: 3.7, runtime_h: 2}
stack: {actuators: "12 Unitree joint motors, about 45 N·m peak on the largest joint", mcu: , compute: "8-core CPU; EDU: optional compute module such as NVIDIA Jetson Orin (40–100 TOPS)", sensors: ["Unitree 4D LiDAR L1 (360° x 90°)", "EDU: depth camera", "EDU: foot-end force sensors"], sim_models: ["URDF (unitree_ros: go1_description, go2_description)", "MJCF (MuJoCo Menagerie: unitree_go1, unitree_go2)", "MJCF (unitree_mujoco: go2, with an SDK2 bridge)", "Isaac Gym (unitree_rl_gym: go2)", "USD (Isaac Lab: Go1 and Go2 velocity tasks)"], ros2: official}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-07-02, stars: 899, active: true}
use_cases: [research, reinforcement-learning, locomotion, navigation, education]
evidence: vendor-claim
last_verified: 2026-11-18
sources:
  - {url: "https://www.unitree.com/go2/", title: "Unitree Go2 product page and spec table", accessed: 2026-11-18}
  - {url: "https://shop.unitree.com/products/unitree-go2", title: "Unitree shop: Go2 product page", accessed: 2026-11-18}
  - {url: "https://prnewswire.co.uk/news-releases/future-explorer-unitree-go2---quadruped-robot-of-embodied-ai-301879707.html", title: "Unitree press release: Go2 launch (2023-07-18)", accessed: 2026-11-18}
  - {url: "https://spectrum.ieee.org/unitrees-go1-robot-dog-looks-pretty-great-costs-just-usd-2700", title: "IEEE Spectrum: Unitree's Go1 costs just US $2,700 (2021-06-09)", accessed: 2026-11-18}
  - {url: "https://github.com/unitreerobotics/unitree_sdk2", title: unitree_sdk2 README, accessed: 2026-11-18}
  - {url: "https://github.com/unitreerobotics/unitree_ros2", title: unitree_ros2 README, accessed: 2026-11-18}
  - {url: "https://github.com/unitreerobotics/unitree_mujoco", title: unitree_mujoco README, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie", title: "MuJoCo Menagerie: unitree_go1 and unitree_go2", accessed: 2026-11-18}
  - {url: "https://github.com/unitreerobotics/unitree_rl_gym", title: unitree_rl_gym README, accessed: 2026-11-18}
  - {url: "https://github.com/isaac-sim/IsaacLab", title: "Isaac Lab: Unitree asset configs and Go1 and Go2 velocity tasks", accessed: 2026-11-18}
---

# Unitree Go1 and Go2

Unitree's low-cost quadrupeds: the Go1 (2021) and the Go2 (unveiled 2023-07-12), sold from
US$1,600 [2][3][4]. The Go2 is the common entry-level research quadruped, with Unitree's own SDK2,
ROS 2 interface, MuJoCo simulator and RL code [5][6][7][9]. Foot force sensors, a depth camera and
the compute module come only on the EDU, which is priced on request [1][2].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Go2 EDU; the spec table also lists Air, Pro and X | [1] |
| Degrees of freedom | 12, three per leg; no gripper | [8] |
| Mass, size | about 15 kg with battery; about 700 x 310 x 400 mm standing (maker's claims) | [1] |
| Speed | EDU 0–3.7 m/s, about 5 m/s in the lab; Air 0–2.5 m/s; Pro 0–3.5 m/s (maker's claims) | [1] |
| Battery, runtime | 8,000 mAh (236.8 Wh), about 1–2 h; 15,000 mAh on the EDU, about 2–4 h (maker's claims) | [1] |
| Joint torque | about 45 N·m peak, on the largest joint motor (maker's claim) | [1][3] |
| Lidar | Unitree 4D LiDAR L1: 360° x 90° view, 0.05 m minimum range (maker's claims at launch) | [3] |
| EDU extras | foot-end force sensors, depth camera; optional compute module such as Orin, 40–100 TOPS | [1] |

## How it works

Twelve joint motors, three per leg, drive the robot [8]; a built-in motion control service walks it
and can be switched off for low-level control [7]. unitree_sdk2 talks to the Go2 over CycloneDDS;
its core is a prebuilt static library for aarch64 and x86_64, with BSD-3 headers and examples [5].
As ROS 2 also uses DDS, unitree_ros2 drives the Go2, B2 and H1 with plain ROS 2 messages on Foxy or
Humble, without wrapping the SDK [6].

unitree_mujoco runs SDK2 and ROS 2 programs against MuJoCo to check low-level controllers [7];
Menagerie converts the unitree_ros URDFs of the Go1 and Go2 to MJCF [8]; unitree_rl_gym trains Go2
policies in Isaac Gym, checks them in MuJoCo and deploys them [9]; Isaac Lab has Go2 and Go1
velocity tasks, the Go1 with a learned MLP actuator model [10].

| Variant | Year | Price | What is different | Source |
|---|---|---|---|---|
| Go1 Air | 2021 | US$2,700 at launch | base model | [4] |
| Go1 | 2021 | US$3,500 at launch | 12 kg, five stereo depth cameras, 16-core CPU and 1.5 TFLOP GPU, 3.5 m/s, about 1 h jogging | [4] |
| Go1 Edu | 2021 | US$8,500 at launch | higher-end compute, 5 kg payload, foot force sensors, lidar, API access | [4] |
| Go2 Air | 2023 | US$1,600; US$1,850 with controller | up to 2.5 m/s | [1][2] |
| Go2 Pro | 2023 | US$2,800 without controller | up to 3.5 m/s | [1][2] |
| Go2 EDU | 2023 | contact sales | foot force sensors, depth camera, optional Orin module, 15,000 mAh battery | [1][2] |

## What it is used for

- Entry-level legged RL: unitree_rl_gym's Go2 pipeline and Isaac Lab's Go2 task [9][10].
- ROS 2 navigation and mapping with the built-in 4D lidar [3][6].

## Cost and BOM

Price on request for the Go2 EDU, so `cost` stays empty. On 2026-11-18 Unitree's shop listed the
Air at US$1,600 (US$1,850 with controller) and the Pro at US$2,800, before tax and freight [2][3].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| SDK | C++ headers and examples; prebuilt static library | unitree_sdk2 [5] | BSD-3-Clause; the core library is prebuilt |
| ROS 2 interface | ROS 2 messages and examples | unitree_ros2 [6] | BSD-3-Clause |
| Robot models | URDF, MJCF | [unitree_ros](https://github.com/unitreerobotics/unitree_ros), Menagerie [8], unitree_mujoco [7] | BSD-3-Clause |
| RL training and deployment | Python | unitree_rl_gym [9], Isaac Lab [10] | BSD-3-Clause |
| Hardware, motor and controller firmware | — | Not published | Closed |

## Strengths and limits

- **Strengths:** a low entry price [2], with Unitree's own ROS 2, SDK, MuJoCo bridge and RL code
  [5][6][7][9]; built-in 360° lidar [3]; Menagerie and Isaac Lab models [8][10].
- **Limits:** research features come only on the EDU, whose price is not published [1][2]; the SDK
  core is prebuilt and firmware closed [5]; unitree_ros2 is tested on Foxy and Humble only [6].

## Related robots

- [Unitree A1](unitree-a1.md): the earlier Unitree quadruped of the legged_gym era.
- [ANYmal](anymal.md) and [Boston Dynamics Spot](boston-dynamics-spot.md): industrial quadrupeds.
- [Pupper v3](pupper-v3.md) and [Petoi Bittle](petoi-nybble-bittle.md): small open quadrupeds.

## Sources

1. [Unitree Go2 product page and spec table](https://www.unitree.com/go2/), accessed 2026-11-18
2. [Unitree shop: Go2 product page](https://shop.unitree.com/products/unitree-go2), accessed 2026-11-18
3. [Unitree press release: Go2 launch (2023-07-18)](https://prnewswire.co.uk/news-releases/future-explorer-unitree-go2---quadruped-robot-of-embodied-ai-301879707.html), accessed 2026-11-18
4. [IEEE Spectrum: Unitree's Go1 costs just US $2,700 (2021-06-09)](https://spectrum.ieee.org/unitrees-go1-robot-dog-looks-pretty-great-costs-just-usd-2700), accessed 2026-11-18
5. [unitree_sdk2 README](https://github.com/unitreerobotics/unitree_sdk2), accessed 2026-11-18
6. [unitree_ros2 README](https://github.com/unitreerobotics/unitree_ros2), accessed 2026-11-18
7. [unitree_mujoco README](https://github.com/unitreerobotics/unitree_mujoco), accessed 2026-11-18
8. [MuJoCo Menagerie: unitree_go1 and unitree_go2](https://github.com/google-deepmind/mujoco_menagerie), accessed 2026-11-18
9. [unitree_rl_gym README](https://github.com/unitreerobotics/unitree_rl_gym), accessed 2026-11-18
10. [Isaac Lab: Unitree asset configs and Go1 and Go2 velocity tasks](https://github.com/isaac-sim/IsaacLab), accessed 2026-11-18
