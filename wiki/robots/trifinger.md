---
type: robot
name: TriFinger
summary: Open three-finger dexterity platform from the Open Dynamic Robot Initiative, 9 torque-controlled brushless joints at 1 kHz for about $5,000; the closed TriFingerPro version ran the Real Robot Challenge.
tags: [dexterous-manipulation, three-finger, brushless, torque-control, odri, pybullet, real-robot-challenge, offline-rl]
category: other
tier: B
openness: full
maker: Max Planck Society and New York University (Open Dynamic Robot Initiative)
year: 2020
license: {hardware: BSD-3-Clause, software: BSD-3-Clause, docs: BSD-3-Clause}
links: {repo: "https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware", docs: "https://open-dynamic-robot-initiative.github.io/robot_fingers/", cad: "https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/tree/master/mechanics/tri_finger_edu_v1", paper: "https://arxiv.org/abs/2008.03596", site: "https://sites.google.com/view/trifinger"}
specs: {dof: 9, payload_kg: , reach_mm: , mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "9 brushless modules: T-Motor Antigravity 4004 300kV motors with a two-stage 9:1 timing-belt reduction", mcu: "TI LAUNCHXL-F28069M LaunchPads with BOOSTXL-DRV8305EVM motor drivers", compute: "real-time PC with a CAN interface, 1 kHz", sensors: ["optical motor encoders (Broadcom AEDT-9810)", "3 x Basler acA720-520uc cameras"], sim_models: ["PyBullet environment (trifinger_simulation)", "URDF/Xacro for FingerOne, FingerEdu, FingerPro and their tri versions (robot_properties_fingers)", "Isaac Gym task (IsaacGymEnvs, Trifinger)", "URDF (Gepetto example-robot-data, finger_edu_description)", "URDF (facebookresearch differentiable-robot-model, trifinger_edu_description)"], ros2: official}
cost: {type: bom, usd: 5000, as_of: 2020-08-08, source: "https://arxiv.org/abs/2008.03596"}
build: {difficulty: 4, hours: , print_hours: }
maturity: {last_commit: 2022-09-06, stars: 1531, active: false}
use_cases: [research, reinforcement-learning, competition, manipulation]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://arxiv.org/abs/2008.03596", title: "TriFinger: An Open-Source Robot for Learning Dexterity", accessed: 2026-11-18}
  - {url: "https://sites.google.com/view/trifinger", title: TriFinger project page, accessed: 2026-11-18}
  - {url: "https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/blob/master/mechanics/tri_finger_edu_v1/README.md", title: TriFingerEdu v1 hardware documentation, accessed: 2026-11-18}
  - {url: "https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/blob/master/mechanics/finger_edu_v1/README.md", title: FingerEdu v1 hardware documentation, accessed: 2026-11-18}
  - {url: "https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/blob/master/mechanics/actuator_module_v1/README.md", title: ODRI brushless actuator module core v1, accessed: 2026-11-18}
  - {url: "https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/blob/master/electronics/ti_electronics/README.md", title: ODRI Texas Instruments evaluation board electronics, accessed: 2026-11-18}
  - {url: "https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware", title: Open Robot Actuator Hardware repository README and licence, accessed: 2026-11-18}
  - {url: "https://github.com/open-dynamic-robot-initiative/trifinger_simulation", title: trifinger_simulation repository README, accessed: 2026-11-18}
  - {url: "https://open-dynamic-robot-initiative.github.io/trifinger_simulation/getting_started/finger_types.html", title: "TriFinger simulation documentation: finger types", accessed: 2026-11-18}
  - {url: "https://github.com/open-dynamic-robot-initiative/robot_properties_fingers", title: robot_properties_fingers repository README, accessed: 2026-11-18}
  - {url: "https://github.com/open-dynamic-robot-initiative/robot_fingers", title: robot_fingers repository and documentation, accessed: 2026-11-18}
  - {url: "https://real-robot-challenge.com/", title: Real Robot Challenge website, accessed: 2026-11-18}
  - {url: "https://proceedings.mlr.press/v220/gurtler23a.html", title: "Real Robot Challenge 2022: Learning Dexterous Manipulation from Offline Data in the Real World", accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2307.15690", title: Benchmarking Offline Reinforcement Learning on Real-Robot Hardware, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2108.09779", title: Transferring Dexterous Manipulation from GPU Simulation to a Remote Real-World TriFinger, accessed: 2026-11-18}
  - {url: "https://github.com/isaac-sim/IsaacGymEnvs/blob/main/isaacgymenvs/tasks/trifinger.py", title: IsaacGymEnvs Trifinger task, accessed: 2026-11-18}
  - {url: "https://github.com/Gepetto/example-robot-data/tree/master/robots/finger_edu_description", title: "Gepetto example-robot-data: finger_edu_description", accessed: 2026-11-18}
  - {url: "https://github.com/facebookresearch/differentiable-robot-model/tree/main/diff_robot_data/trifinger_edu_description", title: "differentiable-robot-model: trifinger_edu_description", accessed: 2026-11-18}
  - {url: "https://github.com/open-dynamic-robot-initiative/trifinger_simulation/blob/master/CHANGELOG.md", title: trifinger_simulation changelog, accessed: 2026-11-18}
---

# TriFinger

A manipulation platform of three identical robot fingers mounted on a frame so their tips meet
over a shared workspace, watched by three cameras [1][3]. The Max Planck Society and New York
University built it in the Open Dynamic Robot Initiative (ODRI), reusing the brushless actuator
modules of the Solo quadruped [2][4][7]. Hardware, drivers and simulator are open; a closed sibling,
TriFingerPro, ran the Real Robot Challenge, so many papers and public datasets come from it
[1][9][12][14].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | TriFingerEdu v1, the open version | [3][9] |
| Layout | 3 identical fingers on an aluminium frame; can also hang upside down | [3] |
| DoF | 9, all torque-controlled: 3 per finger | [1][3] |
| Actuators | T-Motor Antigravity 4004 300kV brushless motors, two-stage 3:1 timing-belt reduction (9:1) | [4][5] |
| Actuator core | 150 g, 2.5 N·m at 12 A (module core as documented for ODRI legs) | [5] |
| Joint speed | up to 416 rpm, derived from motor data and gearing | [1] |
| Encoders | optical, 5,000 lines per channel, 20,000 counts per motor turn | [5] |
| Motor drivers | TI LaunchPad F28069M with DRV8305 BoosterPacks; field-oriented control at 10 kHz | [6] |
| Control | 1 kHz torque control over CAN; each finger needs 24 V and two CAN channels | [1][4][6] |
| Cameras | 3 x Basler acA720-520uc, up to 525 fps; images usually taken at 100 Hz | [1][3] |
| Mass | 930 g per finger module; 21 kg for everything packed in its transport case | [3][4] |
| Objects | dynamic manipulation of objects up to a few hundred grams | [1] |
| Durability | one finger's belt broke after 79 days of continuous running, another's link shell after 72 days | [1] |

## How it works

Each finger is three ODRI actuator modules in printed shells, the same modules as the 12-DoF Solo
quadruped's legs [4]. Inside each module a brushless outrunner drives the joint through two timing
belts, with an optical encoder on the motor [5]. A rubber office thimble makes the fingertip, and a
finger folds back into its base for transport [4]. The fingers bolt to a frame of 40 mm T-slot
aluminium profiles, with polycarbonate walls to keep objects in reach and printed camera arms [3].

The motors run from Texas Instruments evaluation boards, LaunchPads with motor-driver
BoosterPacks, each LaunchPad driving up to two motors; each finger needs 24 V and two CAN channels
to a real-time PC [4][6]. ODRI also published smaller driver
boards with the same function [6]. The software stack, `robot_interfaces` and `robot_fingers`, gives
C++ and Python front-ends with time-indexed action and observation histories, and runs the driver,
front-end and logger as separate processes [1][2][11]. Its safety layer stops the robot if the 1 ms
loop overruns or commands stop arriving, pushes joints back inside their limits, clips torques and
adds damping, so the robot can run without supervision [1]. The packages build with colcon and start
with `ros2 run`, but robot data goes through `robot_interfaces`, not ROS topics [11].

The PyBullet simulator in `trifinger_simulation` has the same interface as the real robot and moved
from Gym to Gymnasium in version 2.0.0 [8][19]. URDF models for every version live in
`robot_properties_fingers` [10]; IsaacGymEnvs has a TriFinger task [16]; third-party URDFs exist in
Gepetto's example-robot-data and Meta's differentiable-robot-model [17][18].

| Variant | What it is | Open hardware | Source |
|---|---|---|---|
| FingerEdu | one 3-DoF finger module on its own base | yes | [4][9] |
| TriFingerEdu v1 | three FingerEdu modules on a frame, with cameras | yes | [3] |
| TriFingerOne | early prototype | models only | [9] |
| TriFingerPro | the Real Robot Challenge robot; same kinematics and actuation, more complex build | no, models only | [1][9] |

## What it is used for

- **Real Robot Challenge 2020 to 2022:** teams ran policies remotely on a cluster of TriFinger
  robots [12]; the 2022 edition at NeurIPS asked teams to learn from offline real-robot data [13].
- **Offline RL datasets:** pushing and lifting data from the real robots, published at ICLR 2023
  [14].
- **Sim-to-real RL:** policies trained in Isaac Gym and run on a remote TriFinger [15][16].
- **The paper's demos:** optimal control, RL from scratch, throwing and writing [1].

## Cost and BOM

About $5,000 for the hardware, per the 2020 paper and the project page [1][2]. The repository lists
every part with suppliers but no prices; some, such as the timing belts, are bought by emailed quote
from a supplier that ships only within Europe [5]. TriFingerPro and TriFingerEdu are not sold.

## Building it

**Difficulty 4:** machined parts and hand-built actuators.

- **Machining:** an aluminium motor pulley, an aluminium centre pulley and a stainless motor shaft
  per module, from PDF drawings [5].
- **Actuators:** step-by-step guides cover motor, shaft, encoder, pulley and shell preparation,
  then assembly and testing [7].
- **Electronics:** off-the-shelf TI boards, flashed over their on-board USB programmer, plus a
  real-time PC with CAN [6][7].
- **Time:** not stated.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Finger and frame mechanics | SolidWorks (zip), STL, PDF drawings, parts list | [tri_finger_edu_v1](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/tree/master/mechanics/tri_finger_edu_v1), [finger_edu_v1](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/tree/master/mechanics/finger_edu_v1) | BSD-3-Clause |
| Actuator module | STL, PDF drawings, BOM, build guides | [actuator_module_v1](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/tree/master/mechanics/actuator_module_v1) | BSD-3-Clause |
| Electronics | off-the-shelf TI boards; ODRI driver boards in Eagle | [electronics](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/tree/master/electronics) | BSD-3-Clause |
| Driver | C++, Python | [robot_fingers](https://github.com/open-dynamic-robot-initiative/robot_fingers) | BSD-3-Clause |
| Simulator | Python, PyBullet | [trifinger_simulation](https://github.com/open-dynamic-robot-initiative/trifinger_simulation) | BSD-3-Clause |
| Models | URDF/Xacro, meshes | [robot_properties_fingers](https://github.com/open-dynamic-robot-initiative/robot_properties_fingers) | BSD-3-Clause |

The hardware repository's last commit is 2022-09-06, while the driver and simulator were still
updated in 2025 and 2026 [7][8][11].

## Strengths and limits

- **Strengths:** everything for the Edu version is open under one permissive licence [7]; fast,
  impact-tolerant torque control at 1 kHz [1][2]; a safety layer built for unsupervised runs [1];
  the same interface in simulation and on hardware [8]; public challenge results and datasets
  [13][14].
- **Limits:** the robot behind the challenge and most datasets, TriFingerPro, is closed [1]; the
  build needs machining, and some parts ship only within Europe [5]; three fingertips, not a hand;
  the hardware design has been idle since 2022 [7]; the challenge site shows no edition after 2022
  [12].

## What to reuse

- One actuator module design shared across a quadruped's legs and a manipulator's fingers [4][5].
- A layered safety check (loop timing, command timeout, joint-limit push-back, torque clipping) so
  learning can run unattended [1].
- A front-end that looks the same to the real robot and the simulator, indexed by time step [1][8].

## Related robots

- [Aero Hand Open](aero-hand-open.md), [LEAP Hand](leap-hand.md) and [RUKA](ruka.md): open hands for
  the same kind of dexterity research.
- [Allegro Hand](allegro-hand.md) and [Shadow Dexterous Hand](shadow-dexterous-hand.md), whose
  DEX-EE is also a three-finger design.
- Solo and Bolt, ODRI's quadruped and biped, use the same actuator modules [7].

## Sources

1. [TriFinger: An Open-Source Robot for Learning Dexterity](https://arxiv.org/abs/2008.03596), accessed 2026-11-18
2. [TriFinger project page](https://sites.google.com/view/trifinger), accessed 2026-11-18
3. [TriFingerEdu v1 hardware documentation](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/blob/master/mechanics/tri_finger_edu_v1/README.md), accessed 2026-11-18
4. [FingerEdu v1 hardware documentation](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/blob/master/mechanics/finger_edu_v1/README.md), accessed 2026-11-18
5. [ODRI brushless actuator module core v1](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/blob/master/mechanics/actuator_module_v1/README.md), accessed 2026-11-18
6. [ODRI Texas Instruments evaluation board electronics](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/blob/master/electronics/ti_electronics/README.md), accessed 2026-11-18
7. [Open Robot Actuator Hardware repository README and licence](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware), accessed 2026-11-18
8. [trifinger_simulation repository README](https://github.com/open-dynamic-robot-initiative/trifinger_simulation), accessed 2026-11-18
9. [TriFinger simulation documentation: finger types](https://open-dynamic-robot-initiative.github.io/trifinger_simulation/getting_started/finger_types.html), accessed 2026-11-18
10. [robot_properties_fingers repository README](https://github.com/open-dynamic-robot-initiative/robot_properties_fingers), accessed 2026-11-18
11. [robot_fingers repository and documentation](https://github.com/open-dynamic-robot-initiative/robot_fingers), accessed 2026-11-18
12. [Real Robot Challenge website](https://real-robot-challenge.com/), accessed 2026-11-18
13. [Real Robot Challenge 2022: Learning Dexterous Manipulation from Offline Data in the Real World](https://proceedings.mlr.press/v220/gurtler23a.html), accessed 2026-11-18
14. [Benchmarking Offline Reinforcement Learning on Real-Robot Hardware](https://arxiv.org/abs/2307.15690), accessed 2026-11-18
15. [Transferring Dexterous Manipulation from GPU Simulation to a Remote Real-World TriFinger](https://arxiv.org/abs/2108.09779), accessed 2026-11-18
16. [IsaacGymEnvs Trifinger task](https://github.com/isaac-sim/IsaacGymEnvs/blob/main/isaacgymenvs/tasks/trifinger.py), accessed 2026-11-18
17. [Gepetto example-robot-data: finger_edu_description](https://github.com/Gepetto/example-robot-data/tree/master/robots/finger_edu_description), accessed 2026-11-18
18. [differentiable-robot-model: trifinger_edu_description](https://github.com/facebookresearch/differentiable-robot-model/tree/main/diff_robot_data/trifinger_edu_description), accessed 2026-11-18
19. [trifinger_simulation changelog](https://github.com/open-dynamic-robot-initiative/trifinger_simulation/blob/master/CHANGELOG.md), accessed 2026-11-18
