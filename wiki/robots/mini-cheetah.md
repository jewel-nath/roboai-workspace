---
type: robot
name: MIT Mini Cheetah
summary: 9 kg quadruped from MIT's Biomimetic Robotics Lab built on low-cost, backdrivable actuators, the first four-legged robot to backflip; its MPC and whole-body control software and the motor driver design are open under MIT, the mechanical CAD is not.
tags: [quadruped, mini-cheetah, mit, proprioceptive-actuator, planetary-gearbox, motor-driver, mpc, whole-body-control, backflip, cheetah-software]
category: legged
tier: B
openness: partial
maker: MIT Biomimetic Robotics Lab
year: 2019
license: {hardware: , software: MIT, docs: }
links: {repo: "https://github.com/mit-biomimetics/Cheetah-Software", docs: , cad: , paper: "https://ieeexplore.ieee.org/document/8793865", site: "https://biomimetics.mit.edu/"}
specs: {dof: 12, payload_kg: , reach_mm: , mass_kg: 9, size_mm: , speed_mps: 3.7, runtime_h: }
stack: {actuators: "12 custom actuators: small drone and RC-plane motors with 6:1 planetary gearboxes; 9.33:1 at the knee in the software model", mcu: "one 3-phase motor driver with integrated position sensor per actuator (bgkatz/3phase_integrated)", compute: , sensors: ["motor position sensor on each driver", "orientation estimate for the body"], sim_models: ["Cheetah-Software simulator (C++, Qt) with OBJ meshes", "URDF (third-party mini_cheetah_urdf, via robot_descriptions)"], ros2: none}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2019-11-21, stars: 3336, active: false}
use_cases: [research, locomotion, reinforcement-learning]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://news.mit.edu/2019/mit-mini-cheetah-first-four-legged-robot-to-backflip-0304", title: "MIT News: Mini cheetah is the first four-legged robot to do a backflip (2019-03-04)", accessed: 2026-11-18}
  - {url: "https://ieeexplore.ieee.org/document/8793865", title: "Katz, Di Carlo, Kim: Mini Cheetah: A Platform for Pushing the Limits of Dynamic Quadruped Control (ICRA 2019)", accessed: 2026-11-18}
  - {url: "https://dspace.mit.edu/handle/1721.1/118671", title: "Katz: A low cost modular actuator for dynamic robots (MIT S.M. thesis, 2018)", accessed: 2026-11-18}
  - {url: "https://dspace.mit.edu/handle/1721.1/119863", title: "Wensing et al.: Proprioceptive Actuator Design in the MIT Cheetah (IEEE T-RO, 2017)", accessed: 2026-11-18}
  - {url: "https://github.com/mit-biomimetics/Cheetah-Software", title: Cheetah-Software repository, accessed: 2026-11-18}
  - {url: "https://github.com/bgkatz/3phase_integrated", title: "bgkatz/3phase_integrated: motor driver hardware", accessed: 2026-11-18}
  - {url: "https://github.com/bgkatz/motorcontrol", title: "bgkatz/motorcontrol: motor driver firmware", accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/1909.06586", title: Highly Dynamic Quadruped Locomotion via Whole-Body Impulse Control and Model Predictive Control, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2205.02824", title: Rapid Locomotion via Reinforcement Learning, accessed: 2026-11-18}
  - {url: "https://github.com/robot-descriptions/robot_descriptions.py", title: robot_descriptions model list, accessed: 2026-11-18}
---

# MIT Mini Cheetah

A 9 kg, 12-joint quadruped from Sangbae Kim's Biomimetic Robotics Lab at MIT, shown in 2019 as the
first four-legged robot to do a backflip [1][2]. Its cheap, backdrivable actuators, open control
code and public motor driver make it a design to learn from rather than a robot to buy: no source
read offers it for sale, and its mechanical CAD is not public [1][5][6].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Mini Cheetah as presented at ICRA 2019 | [2] |
| Degrees of freedom | 12, one motor per joint, three per leg (abduction, hip, knee) | [1][5] |
| Mass, height | 9 kg (20 lb); about 0.3 m tall | [1][2] |
| Actuators | small drone and RC-plane motors with a 6:1 planetary gearbox; each swaps out on its own | [1] |
| Software model | 6:1 at abduction and hip, 9.33:1 at the knee; 3 N·m motor torque limit; 24 V battery; legs 0.209 m upper, 0.195 m lower | [5] |
| Speed | 2.45 m/s with convex MPC [2]; 3.7 m/s with WBIC and MPC [8]; 3.9 m/s with a learned policy [9] | [2][8][9] |
| Control rate | 500 Hz robot controller (0.002 s step) in the default config | [5] |
| Motor driver | 3-phase driver with integrated position sensor; newer firmware targets an STM32F446 | [6][7] |

## How it works

The actuators carry over the proprioceptive design of the larger MIT Cheetah: backdrivable
electric drives that control contact forces at the joints and handle impacts about as well as legs
with series springs [4]. The Mini Cheetah builds them from hobby motors with a 6:1
planetary stage, cheap enough to swap after a crash [1]; Katz's thesis documents the actuator [3].

Each actuator has its own driver, Ben Katz's 3-phase Cheetah motor controller with an integrated
position sensor; he published its Eagle files, Gerbers, mbed firmware and newer STM32 firmware
[6][7]. Cheetah-Software runs on the robot's computer and talks over LCM; it holds convex MPC,
whole-body control, backflip and vision MPC controllers and a Qt simulator [5]. The WBIC paper pairs
MPC reaction forces with a whole-body controller and shows six gaits up to 3.7 m/s [8].

There is no official URDF or MJCF: Cheetah-Software uses its own simulator and OBJ meshes [5], and
robot_descriptions loads a third-party URDF (Derek-TH-Wang/mini_cheetah_urdf) [10]. The code has
no ROS interface, and its last commit is from 2019 [5].

## What it is used for

- Model-based control research: convex MPC, WBIC and the backflip [1][3][8].
- Learned locomotion: Margolis et al. (RSS 2022) reached 3.9 m/s on grass, ice and gravel [9].
- A shared platform: MIT planned about ten robots to loan to other labs [1].
- A reference for low-cost actuators and motor drivers [3][6][7].

## Cost and BOM

No price or BOM was found; MIT News calls the motors only low-cost [1]. `cost` stays empty.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Control software and simulator | C++, LCM, Qt | Cheetah-Software [5] | MIT |
| Motor driver board | Eagle, Gerbers | 3phase_integrated [6] | MIT |
| Motor driver firmware | C for STM32 (newer); mbed (older, linked) | motorcontrol [7] | MIT |
| Robot model | OBJ meshes; third-party URDF | Cheetah-Software [5]; mini_cheetah_urdf via robot_descriptions [10] | MIT; BSD per its package.xml |
| Mechanical CAD, gearbox and leg drawings | — | Not published in the sources read | — |

## Strengths and limits

- **Strengths:** light and rugged, with swappable actuators [1]; open MPC and whole-body control
  code [5][8]; open driver hardware and firmware [6][7]; strong learned-gait results [9].
- **Limits:** not for sale; no mechanical CAD, so it cannot be built from open files [5][6];
  code unmaintained since 2019 and without ROS [5]; no official URDF or MJCF [5][10].

## What to reuse

- A hobby outrunner motor with a 6:1 planetary stage as a cheap backdrivable joint [1][5].
- A driver with a position sensor on every motor, so each actuator is a self-contained module [6].

## Related robots

- [Unitree A1](unitree-a1.md) and [Unitree Go2](unitree-go2.md): small commercial quadrupeds.
- Open quadrupeds: [ODRI Solo](odri-solo.md), [Stanford Doggo](stanford-doggo.md), [Pupper v3](pupper-v3.md).

## Sources

1. [MIT News: Mini cheetah is the first four-legged robot to do a backflip (2019-03-04)](https://news.mit.edu/2019/mit-mini-cheetah-first-four-legged-robot-to-backflip-0304), accessed 2026-11-18
2. [Katz, Di Carlo, Kim: Mini Cheetah: A Platform for Pushing the Limits of Dynamic Quadruped Control (ICRA 2019)](https://ieeexplore.ieee.org/document/8793865), accessed 2026-11-18
3. [Katz: A low cost modular actuator for dynamic robots (MIT S.M. thesis, 2018)](https://dspace.mit.edu/handle/1721.1/118671), accessed 2026-11-18
4. [Wensing et al.: Proprioceptive Actuator Design in the MIT Cheetah (IEEE T-RO, 2017)](https://dspace.mit.edu/handle/1721.1/119863), accessed 2026-11-18
5. [Cheetah-Software repository](https://github.com/mit-biomimetics/Cheetah-Software), accessed 2026-11-18
6. [bgkatz/3phase_integrated: motor driver hardware](https://github.com/bgkatz/3phase_integrated), accessed 2026-11-18
7. [bgkatz/motorcontrol: motor driver firmware](https://github.com/bgkatz/motorcontrol), accessed 2026-11-18
8. [Highly Dynamic Quadruped Locomotion via Whole-Body Impulse Control and Model Predictive Control](https://arxiv.org/abs/1909.06586), accessed 2026-11-18
9. [Rapid Locomotion via Reinforcement Learning](https://arxiv.org/abs/2205.02824), accessed 2026-11-18
10. [robot_descriptions model list](https://github.com/robot-descriptions/robot_descriptions.py), accessed 2026-11-18
