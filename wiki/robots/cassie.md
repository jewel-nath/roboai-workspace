---
type: robot
name: Agility Robotics Cassie
summary: Agility Robotics' 2017 research biped with spring legs and no torso or arms, the platform behind much bipedal reinforcement-learning work; no longer supported, with maker-supplied MIT MuJoCo model and open simulation library.
tags: [biped, cassie, agility-robotics, discontinued, reinforcement-learning, mujoco, spring-legs, udp]
category: legged
tier: B
openness: software-only
maker: Agility Robotics
year: 2017
license: {hardware: , software: ISC, docs: }
links: {repo: "https://github.com/osudrl/cassie-mujoco-sim", docs: "https://github.com/agilityrobotics/cassie-doc", cad: , paper: , site: }
specs: {dof: 10, payload_kg: , reach_mm: , mass_kg: 31, size_mm: , speed_mps: 4.0, runtime_h: 5}
stack: {actuators: "10 brushless DC motors with custom transmissions, 5 per leg; knee and heel springs", mcu: "custom microcontroller boards in the legs and pelvis (Medulla firmware)", compute: "Intel Atom real-time control computer; optional Intel NUC i5 for user code", sensors: ["MEMS IMU", "absolute and incremental joint encoders"], sim_models: ["MJCF (MuJoCo Menagerie agility_cassie, supplied by Agility, MIT)", "MJCF and C/Python simulation library (osudrl/cassie-mujoco-sim)", "URDF (robot-descriptions/cassie_description, MIT)"], ros2: none}
cost: {type: retail, usd: 250000, as_of: 2017-05-04, source: "https://oregonbusiness.com/?p=18182"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2023-04-13, stars: 309, active: false}
use_cases: [research, reinforcement-learning, locomotion]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://spectrum.ieee.org/agility-robotics-introduces-cassie-a-dynamic-and-talented-robot-delivery-ostrich", title: "IEEE Spectrum: Agility Robotics Introduces Cassie (2017-02-09)", accessed: 2026-11-18}
  - {url: "https://robotsguide.com/robots/cassie", title: "IEEE Robots guide: Cassie", accessed: 2026-11-18}
  - {url: "https://oregonbusiness.com/?p=18182", title: "Oregon Business: I, Robot (2017-05-04)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/the-evolution-of-digit-agility-robotics-journey-from-cassie-to-digit-5/", title: "The Robot Report: The evolution of Digit, from Cassie to Digit 5 (2026-09-16)", accessed: 2026-11-18}
  - {url: "https://github.com/agilityrobotics/cassie-doc", title: Agility Robotics Cassie documentation and software release repository, accessed: 2026-11-18}
  - {url: "https://github.com/osudrl/cassie-mujoco-sim", title: osudrl cassie-mujoco-sim README, accessed: 2026-11-18}
  - {url: "https://github.com/robot-descriptions/cassie_description", title: cassie_description README, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/agility_cassie", title: "MuJoCo Menagerie: agility_cassie", accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2103.14295", title: Reinforcement Learning for Robust Parameterized Locomotion Control of Bipedal Robots, accessed: 2026-11-18}
---

# Agility Robotics Cassie

A two-legged robot with no torso or arms from Agility Robotics, an Oregon State spin-off, sold to
research labs from 2017 [1] and common in bipedal reinforcement learning [9]; Digit followed it [4].
**Discontinued:** Agility built no later Cassie versions [4] and its archived docs repo says Cassie
is no longer supported [5]; no source found states when sales ended.

## Specs

| Item | Value | Source |
|---|---|---|
| Degrees of freedom | 10 motors, 5 per leg: hip roll, yaw and pitch, knee, foot; the springs add passive joints | [2][8] |
| Height, mass | 115 cm; 31 kg | [2] |
| Battery | 20.5 Ah at 48 V; about 5 h of mixed use (about 100 W standing, 300 W walking) | [2] |
| Speed | 5 km/h listed [2]; a learned gait ran 100 m in 24.73 s in 2022, about 4.0 m/s on average (the frontmatter value) [4] | [2][4] |
| Compute | Intel Atom real-time computer, microcontroller boards in each limb, optional Intel NUC i5 for users; control at 2 kHz | [2][6] |
| Sensors | MEMS IMU; absolute and incremental joint encoders | [2] |

## How it works

Cassie descends from Oregon State's ATRIAS but uses a new leg layout in which the motors no longer
work against each other, so they can be smaller [1]. Each hip has three degrees of freedom, so the
robot can steer, and powered ankles let it stand still [1]. Springs at the knee and heel make the
legs compliant; the URDF keeps the heel spring as its own link and closes the leg linkage with a
constraint, giving 22 unconstrained degrees of freedom [7].

An onboard real-time computer runs Agility's controller, and firmware for the leg and pelvis boards
ships in Agility's docs repo [2][5]. User code talks to the robot over UDP. cassie-mujoco-sim packs
and unpacks Cassie's UDP messages and mimics its internal safety checks and state estimation, so one
controller can drive the simulator or the robot [6]. There is no ROS 2 driver.

Models: Agility supplied the Menagerie MJCF under MIT [8]; cassie-mujoco-sim has its own MJCF variants
and a C library with a Python wrapper for MuJoCo 2.1 [6]; cassie_description is an MIT URDF [7].

## What it is used for

- Sim-to-real reinforcement learning: Berkeley trained walking policies in simulation for Cassie [9].
- Running: Oregon State's Cassie set the Guinness World Record for 100 m by a bipedal robot [4].
- Bipedal control research in university labs; the University of Michigan had one of the first [1].

## Cost and BOM

| Item | Price (USD) | Type | Date | Source |
|---|---|---|---|---|
| Cassie, Agility's planned first sale price ("approximately") | 250,000 | retail | 2017-05-04 | [3] |

IEEE's Robots guide lists $300,000, varying by application and quantity, with no date [2]. Agility
no longer supports Cassie [5]; used units are the only route, and no listing was checked.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Hardware design | — | Not published | Proprietary |
| Docs, firmware, software releases, drawings | PDF, binaries, STEP | [cassie-doc](https://github.com/agilityrobotics/cassie-doc) [5] | Agility licence agreement, proprietary |
| Simulation and UDP library | C, Python, MJCF | [cassie-mujoco-sim](https://github.com/osudrl/cassie-mujoco-sim) [6] | ISC-style notice in the headers; no licence file |
| MuJoCo model | MJCF | [Menagerie agility_cassie](https://github.com/google-deepmind/mujoco_menagerie/tree/main/agility_cassie) [8] | MIT |
| Description | URDF, meshes | [cassie_description](https://github.com/robot-descriptions/cassie_description) [7] | MIT |

## Strengths and limits

- **Strengths:** a light, spring-legged biped with proven sim-to-real RL and a 100 m record [4][9];
  a maker-supplied MuJoCo model and a simulator that speaks the robot's own UDP interface [6][8].
- **Limits:** discontinued and unsupported, with proprietary docs and firmware [5]; no arms, torso,
  cameras or ROS 2 driver [2]; the closed-chain legs need constraints in URDF [7].

## What to reuse

- One interface for simulator and robot: a simulator that speaks the robot's own UDP packets lets a
  controller move to hardware without changes [6].

## Related robots

- [Agility Digit](agility-digit.md): Agility's humanoid that followed Cassie [4].
- [Upkie](upkie.md) and [Berkeley Humanoid Lite](berkeley-humanoid-lite.md): open bipeds you can build.
- [Boston Dynamics Atlas](boston-dynamics-atlas.md): a hydraulic research humanoid of the same era.

## Sources

1. [IEEE Spectrum: Agility Robotics Introduces Cassie (2017-02-09)](https://spectrum.ieee.org/agility-robotics-introduces-cassie-a-dynamic-and-talented-robot-delivery-ostrich), accessed 2026-11-18
2. [IEEE Robots guide: Cassie](https://robotsguide.com/robots/cassie), accessed 2026-11-18
3. [Oregon Business: I, Robot (2017-05-04)](https://oregonbusiness.com/?p=18182), accessed 2026-11-18
4. [The Robot Report: The evolution of Digit, from Cassie to Digit 5 (2026-09-16)](https://www.therobotreport.com/the-evolution-of-digit-agility-robotics-journey-from-cassie-to-digit-5/), accessed 2026-11-18
5. [Agility Robotics Cassie documentation and software release repository](https://github.com/agilityrobotics/cassie-doc), accessed 2026-11-18
6. [osudrl cassie-mujoco-sim README](https://github.com/osudrl/cassie-mujoco-sim), accessed 2026-11-18
7. [cassie_description README](https://github.com/robot-descriptions/cassie_description), accessed 2026-11-18
8. [MuJoCo Menagerie: agility_cassie](https://github.com/google-deepmind/mujoco_menagerie/tree/main/agility_cassie), accessed 2026-11-18
9. [Reinforcement Learning for Robust Parameterized Locomotion Control of Bipedal Robots](https://arxiv.org/abs/2103.14295), accessed 2026-11-18
