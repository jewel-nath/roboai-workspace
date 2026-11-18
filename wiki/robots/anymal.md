---
type: robot
name: ANYmal B, C, D and X
summary: Industrial quadruped from ANYbotics, the anchor of legged research at ETH Zurich and a standard legged-RL baseline in legged_gym and Isaac Lab; later sold as the ANYmal D inspection robot and the explosion-proof ANYmal X.
tags: [quadruped, anymal-b, anymal-c, anymal-d, anymal-x, anydrive, legged-gym, isaac-lab, mujoco, eth-zurich, inspection, commercial]
category: legged
tier: B
openness: software-only
maker: ANYbotics
year: 2019
license: {hardware: , software: BSD-3-Clause, docs: }
links: {repo: "https://github.com/ANYbotics/anymal_c_simple_description", docs: , cad: , paper: , site: "https://www.anybotics.com/"}
specs: {dof: 12, payload_kg: 10, reach_mm: , mass_kg: 50, size_mm: , speed_mps: 1, runtime_h: 2}
stack: {actuators: "12 ANYdrive joint actuators (ANYdrive 3.0 on ANYmal C)", mcu: , compute: "two six-core Intel Core i7 computers; optional NVIDIA Jetson Xavier", sensors: ["lidar", "depth cameras", "cameras", "optional thermal camera"], sim_models: ["URDF (ANYbotics anymal_b, anymal_c and anymal_d simple descriptions)", "MJCF (MuJoCo Menagerie: anybotics_anymal_b, anybotics_anymal_c)", "Isaac Gym (legged_gym: anymal_b, anymal_c)", "USD (Isaac Lab: ANYmal B, C and D)"], ros2: none}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2023-05-12, stars: 75, active: false}
use_cases: [research, reinforcement-learning, locomotion, navigation]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://spectrum.ieee.org/anybotics-introduces-sleek-new-anymal-c-quadruped", title: "IEEE Spectrum: ANYbotics introduces sleek new ANYmal C quadruped (2019-08-22)", accessed: 2026-11-18}
  - {url: "https://newatlas.com/robotics/anybotics-anymal-d-walking-robot-inspection/", title: "New Atlas: ANYmal D inspection robot (2021-04-21)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/anybotics-begins-delivering-anymal-x-legged-robot-explosive-atmospheres/", title: "The Robot Report: ANYbotics begins delivering ANYmal X (2026-10-27)", accessed: 2026-11-18}
  - {url: "https://en.wikipedia.org/wiki/ANYbotics", title: "Wikipedia: ANYbotics", accessed: 2026-11-18}
  - {url: "https://www.anymal-research.org/", title: ANYmal Research community, accessed: 2026-11-18}
  - {url: "https://github.com/ANYbotics/anymal_c_simple_description", title: anymal_c_simple_description README and LICENSE, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie", title: "MuJoCo Menagerie: anybotics_anymal_b and anybotics_anymal_c", accessed: 2026-11-18}
  - {url: "https://github.com/leggedrobotics/legged_gym", title: legged_gym README and task registry, accessed: 2026-11-18}
  - {url: "https://github.com/isaac-sim/IsaacLab", title: "Isaac Lab: ANYmal asset configs and velocity tasks", accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2201.08117", title: Learning robust perceptive locomotion for quadrupedal robots in the wild, accessed: 2026-11-18}
---

# ANYmal B, C, D and X

A 12-joint quadruped from ANYbotics, a 2016 spin-off of ETH Zurich's legged robotics research [4].
The ANYmal C (2019) is the version open models and RL code target most [1][7][8]; later products
are the ANYmal D inspection robot (2021) and the explosion-proof ANYmal X, delivered from October
2026 [2][3]. Most builders meet it in RL simulation, where it is a standard legged baseline [8][9].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | ANYmal C, launched in August 2019 | [1] |
| Degrees of freedom | 12: hip abduction, hip flexion and knee on each leg (URDF joints HAA, HFE, KFE); no gripper | [6] |
| Mass, payload | 50 kg; 10 kg payload (maker's claims) | [1] |
| Speed, runtime | 1 m/s; over 2 h, then it docks itself to recharge (maker's claims) | [1] |
| Terrain, protection | 20° slopes, 45° stairs, 25 cm gaps, 60 cm passages; IP67, survives 1 m submersion for an hour (maker's claims) | [1] |
| Compute | two six-core Intel i7 computers; optional NVIDIA Jetson Xavier for learning | [1] |
| Sensors | lidar for mapping and SLAM, depth cameras, cameras; optional thermal camera | [1] |

## How it works

Each leg has three joints driven by ANYbotics' ANYdrive actuators [6][9]. Isaac Lab models the
ANYdrive 3.0 of the ANYmal C with a learned LSTM actuator network, capped at 80 N·m and 7.5 rad/s
in its config (simulation settings, not datasheet values) [9]; legged_gym ships an actuator network
too, plus friction and mass randomisation, observation noise and random pushes for sim-to-real [8].

ANYbotics publishes simplified URDFs of the B, C and D as BSD-3 ROS 1 (catkin) packages; the full
description, Gazebo simulation and control software go only to ANYmal Research members, under a
research agreement [5][6]. No public ROS 2 driver was found. Menagerie converts the B and C URDFs
to MJCF [7]; legged_gym (Isaac Gym, now in limited maintenance) has B and C tasks; Isaac Lab has
B, C and D velocity tasks and reuses the C actuator network for the D, as none is public [8][9].

| Variant | Year | What is different | Open models | Source |
|---|---|---|---|---|
| ANYmal B | — | The research version before C | URDF, MJCF, legged_gym, Isaac Lab | [1][7][8][9] |
| ANYmal C | 2019 | Industrial redesign: new drives and computers, IP67, docking | URDF, MJCF, legged_gym, Isaac Lab | [1][6][7][9] |
| ANYmal D | 2021 | Inspection product: 90 min runtime, pan-tilt head with zoom and thermal cameras and a microphone, IP67 | URDF, Isaac Lab | [2][9] |
| ANYmal X | deliveries from Oct 2026 | ATEX and IECEx version for explosive atmospheres; leg actuators and battery in flameproof casings | none found | [3] |

## What it is used for

- Legged RL baseline: legged_gym's example task trains ANYmal C; Isaac Lab has B, C and D [8][9].
- Perceptive locomotion: Miki et al. (Science Robotics, 2022) took ANYmal on an hour-long Alpine
  hike in about the time suggested for human hikers [10].
- Industrial inspection with the ANYmal D and X [2][3].
- The ANYmal Research community, whose members include ETH Zurich, NVIDIA and Intel [5].

## Cost and BOM

Price on request: no source read gives a price for any ANYmal version, so `cost` stays empty.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Simplified descriptions of B, C and D | URDF, DAE meshes, ROS 1 catkin | [anymal_b](https://github.com/ANYbotics/anymal_b_simple_description), [anymal_c](https://github.com/ANYbotics/anymal_c_simple_description) [6], [anymal_d](https://github.com/ANYbotics/anymal_d_simple_description) | BSD-3-Clause |
| MuJoCo models of B and C | MJCF | Menagerie [7] | BSD-3-Clause |
| RL environments and actuator networks | Python | legged_gym [8], Isaac Lab [9] | BSD-3-Clause; Isaac Lab USD assets download from NVIDIA's server |
| Full description, simulation, control software | — | ANYmal Research members only [5] | Research agreement |
| Hardware, actuator firmware | — | Not published | Closed |

## Strengths and limits

- **Strengths:** IP67, self-docking and on-board lidar mapping in an industrial product [1][2]; well
  supported in open RL code, with maker URDFs and learned actuator networks [6][8][9].
- **Limits:** no public price, control software or ROS 2 driver [5]; 50 kg and 1 m/s for the C [1];
  the public URDFs are simplified ROS 1 packages, and the C repo has not changed since 2023 [6].

## Related robots

- [Boston Dynamics Spot](boston-dynamics-spot.md): the other industrial inspection quadruped.
- [Unitree A1](unitree-a1.md), [Unitree Go2](unitree-go2.md): cheaper quadrupeds, same RL tools.
- [MIT Mini Cheetah](mini-cheetah.md) and [ODRI Solo](odri-solo.md): small research quadrupeds.

## Sources

1. [IEEE Spectrum: ANYbotics introduces sleek new ANYmal C quadruped (2019-08-22)](https://spectrum.ieee.org/anybotics-introduces-sleek-new-anymal-c-quadruped), accessed 2026-11-18
2. [New Atlas: ANYmal D inspection robot (2021-04-21)](https://newatlas.com/robotics/anybotics-anymal-d-walking-robot-inspection/), accessed 2026-11-18
3. [The Robot Report: ANYbotics begins delivering ANYmal X (2026-10-27)](https://www.therobotreport.com/anybotics-begins-delivering-anymal-x-legged-robot-explosive-atmospheres/), accessed 2026-11-18
4. [Wikipedia: ANYbotics](https://en.wikipedia.org/wiki/ANYbotics), accessed 2026-11-18
5. [ANYmal Research community](https://www.anymal-research.org/), accessed 2026-11-18
6. [anymal_c_simple_description README and LICENSE](https://github.com/ANYbotics/anymal_c_simple_description), accessed 2026-11-18
7. [MuJoCo Menagerie: anybotics_anymal_b and anybotics_anymal_c](https://github.com/google-deepmind/mujoco_menagerie), accessed 2026-11-18
8. [legged_gym README and task registry](https://github.com/leggedrobotics/legged_gym), accessed 2026-11-18
9. [Isaac Lab: ANYmal asset configs and velocity tasks](https://github.com/isaac-sim/IsaacLab), accessed 2026-11-18
10. [Learning robust perceptive locomotion for quadrupedal robots in the wild](https://arxiv.org/abs/2201.08117), accessed 2026-11-18
