---
type: robot
name: Boston Dynamics Spot
summary: The most deployed commercial quadruped, with over 1,500 in customer hands, a Python SDK under Boston Dynamics' own licence, an optional arm, a ROS 2 driver from the RAI Institute and MuJoCo and Isaac Lab models.
tags: [quadruped, spot, spot-arm, inspection, spot-sdk, ros2, mujoco, isaac-lab, commercial]
category: legged
tier: B
openness: closed-reference
maker: Boston Dynamics
year: 2020
license: {hardware: , software: MIT AND BSD-3-Clause, docs: }
links: {repo: "https://github.com/rai-opensource/spot_ros2", docs: "https://dev.bostondynamics.com", cad: , paper: , site: "https://bostondynamics.com/products/spot/"}
specs: {dof: 12, payload_kg: 20.43, reach_mm: , mass_kg: 33.8, size_mm: "1100 x 500 x 610", speed_mps: 1.6, runtime_h: 1.5}
stack: {actuators: "12 joint actuators: two in each hip, one in each knee", mcu: , compute: "on-board computer; optional Spot CORE payload computer", sensors: ["5 stereo camera pairs (projected stereo, 360°, 4 m range)", "joint position, velocity and load"], sim_models: ["URDF/Xacro (spot_description, used by spot_ros2)", "MJCF (MuJoCo Menagerie boston_dynamics_spot, with and without arm)", "USD (Isaac Lab Spot velocity task)"], ros2: community}
cost: {type: retail, usd: 74500, as_of: 2020-06-16, source: "https://spectrum.ieee.org/boston-dynamics-spot-robot-dog-now-available"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-10-14, stars: 297, active: true}
use_cases: [research, navigation, locomotion, reinforcement-learning, manipulation, teleop]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://bostondynamics.com/products/spot/", title: Boston Dynamics Spot product page and specifications, accessed: 2026-11-18}
  - {url: "https://github.com/boston-dynamics/spot-sdk", title: "Spot SDK repository (README, LICENSE, v5.2.0)", accessed: 2026-11-18}
  - {url: "https://github.com/boston-dynamics/spot-sdk/blob/master/docs/concepts/about_spot.md", title: "Spot SDK docs: About Spot", accessed: 2026-11-18}
  - {url: "https://github.com/boston-dynamics/spot-sdk/blob/master/docs/concepts/joint_control/README.md", title: "Spot SDK docs: Joint Control API", accessed: 2026-11-18}
  - {url: "https://spectrum.ieee.org/boston-dynamics-spot-robot-dog-now-available", title: "IEEE Spectrum: Spot is now available for $74,500 (2020-06-16)", accessed: 2026-11-18}
  - {url: "https://github.com/rai-opensource/spot_ros2", title: spot_ros2 README and LICENSE, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/boston_dynamics_spot", title: "MuJoCo Menagerie: boston_dynamics_spot", accessed: 2026-11-18}
  - {url: "https://github.com/isaac-sim/IsaacLab", title: "Isaac Lab: Spot asset config and velocity task", accessed: 2026-11-18}
  - {url: "https://github.com/rai-opensource/spot_description", title: spot_description repository, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2504.17857", title: "High-Performance Reinforcement Learning on Spot: Optimizing Simulation Parameters with Distributional Measures", accessed: 2026-11-18}
---

# Boston Dynamics Spot

A 12-joint quadruped from Boston Dynamics, on general sale since June 2020 and, by the maker's
count, with over 1,500 robots in customer hands [1][5]. It climbs stairs and keeps clear of
obstacles by itself; builders program it through the Spot SDK or a ROS 2 driver, and simulate it
from open URDF, MJCF and Isaac Lab models [2][6][7][8].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Spot base robot, without arm, as on the current product page | [1] |
| Degrees of freedom | 12, three per leg: hip X, hip Y, knee; the optional arm adds six joints and a gripper | [3][7] |
| Mass, payload | 33.8 kg with battery; 20.43 kg (45 lb) maximum payload; two DB25 payload ports, 150 W each (maker's claims) | [1] |
| Size | 1100 x 500 mm; walking height 610 mm, adjustable 520–700 mm (maker's claims) | [1] |
| Speed, terrain | 1.6 m/s; ±30° slopes; 300 mm steps (maker's claims) | [1] |
| Battery | 564 Wh; 90 min average runtime, 60 min recharge (maker's claims) | [1] |
| Environment | IP54; −20 to 55 °C (maker's claims) | [1] |
| Perception | five stereo camera pairs; 360° terrain sensing up to 4 m (maker's claims) | [1][3] |
| Older SDK spec table | "Spot Gamma": 32.5 kg, 14 kg payload, 605 Wh, 120 min charge, −20 to 45 °C | [3] |

## How it works

Each leg has two hip actuators and one knee actuator [3]. Boston Dynamics' controller handles
walking and stairs; applications talk to it through the Spot SDK: a Python client, a protobuf API
for other languages, payload interface docs and examples (v5.2.0 when read) [2]. The beta Joint
Control API streams per-joint position, velocity, torque and gains at a high rate, but needs a
special licence on the robot [4]; it is how outside groups run their own learned gaits [10].

spot_ros2 bridges the SDK to ROS 2 Humble on Ubuntu 22.04, for AMD64 and ARM64, with a ros2_control
interface for the joint-level API [6]. It is maintained by the RAI Institute and MASKOR, not
Boston Dynamics, and moved from the bdaiinstitute to the RAI-Opensource GitHub organisation on
2026-04-28; the Spot SDK docs do not mention it, so `stack.ros2` is `community` [2][6].

The URDF lives in spot_description [9]. MuJoCo Menagerie converts it to MJCF with and without the
arm, using heuristic gains that were not identified on hardware [7]. Isaac Lab has a Spot velocity
task whose actuator data was collected by the Boston Dynamics AI Institute [8].

## What it is used for

- Commercial work: the licence aims Spot at businesses, not homes or use near children [5].
- Legged RL on commercial hardware: Miller et al. (2025) trained a policy in Isaac Lab and ran it
  through the low-level API at more than triple the default controller's top speed [10].
- Mobile manipulation with the Spot Arm, which Menagerie also models [1][7].
- ROS 2 control, robot state and camera images through spot_ros2 [6].

## Cost and BOM

Retail: US$74,500 plus tax for the Spot Explorer kit (robot, two batteries, charger, tablet
controller, case) at general launch on 2020-06-16; an extra battery was $4,620 and the Enhanced
Autonomy Package $34,570 [5]. The current product page gives no price and points to sales [1].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Spot SDK: Python client, protobuf API, docs, examples | Python, protobuf | [spot-sdk](https://github.com/boston-dynamics/spot-sdk) [2] | Boston Dynamics SDK licence (20191101-BDSDK-SL): source may be modified and shared, but used only with Boston Dynamics robots or software simulators |
| ROS 2 driver | ROS 2 packages | [spot_ros2](https://github.com/rai-opensource/spot_ros2) [6] | MIT; BSD-3-Clause for parts from Clearpath's ROS 1 driver |
| Robot description | URDF/Xacro | [spot_description](https://github.com/rai-opensource/spot_description) [9] | MIT |
| MuJoCo model, with and without arm | MJCF | Menagerie `boston_dynamics_spot` [7] | BSD-3-Clause |
| Hardware, firmware, walking controller | — | Not published | Closed |

## Strengths and limits

- **Strengths:** a mature, widely deployed product with IP54, 1.6 m/s and 300 mm steps [1]; a
  documented SDK and payload interface [2]; open URDF, MJCF and Isaac Lab models [7][8][9].
- **Limits:** the SDK licence bars use with other hardware [2]; joint-level control needs an extra
  licence [4]; the ROS 2 driver is not Boston Dynamics' own and supports Humble only [6].

## Related robots

- [ANYmal](anymal.md): the other industrial inspection quadruped, IP67 and heavier.
- [Unitree Go2](unitree-go2.md): a far cheaper quadruped with an official ROS 2 interface.
- [Boston Dynamics Atlas](boston-dynamics-atlas.md): the maker's humanoid.

## Sources

1. [Boston Dynamics Spot product page and specifications](https://bostondynamics.com/products/spot/), accessed 2026-11-18
2. [Spot SDK repository (README, LICENSE, v5.2.0)](https://github.com/boston-dynamics/spot-sdk), accessed 2026-11-18
3. [Spot SDK docs: About Spot](https://github.com/boston-dynamics/spot-sdk/blob/master/docs/concepts/about_spot.md), accessed 2026-11-18
4. [Spot SDK docs: Joint Control API](https://github.com/boston-dynamics/spot-sdk/blob/master/docs/concepts/joint_control/README.md), accessed 2026-11-18
5. [IEEE Spectrum: Spot is now available for $74,500 (2020-06-16)](https://spectrum.ieee.org/boston-dynamics-spot-robot-dog-now-available), accessed 2026-11-18
6. [spot_ros2 README and LICENSE](https://github.com/rai-opensource/spot_ros2), accessed 2026-11-18
7. [MuJoCo Menagerie: boston_dynamics_spot](https://github.com/google-deepmind/mujoco_menagerie/tree/main/boston_dynamics_spot), accessed 2026-11-18
8. [Isaac Lab: Spot asset config and velocity task](https://github.com/isaac-sim/IsaacLab), accessed 2026-11-18
9. [spot_description repository](https://github.com/rai-opensource/spot_description), accessed 2026-11-18
10. [High-Performance Reinforcement Learning on Spot: Optimizing Simulation Parameters with Distributional Measures](https://arxiv.org/abs/2504.17857), accessed 2026-11-18
