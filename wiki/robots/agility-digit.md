---
type: robot
name: Agility Digit
summary: Agility's bipedal humanoid with Cassie-style spring legs, used in humanoid reinforcement-learning papers and in warehouse tote handling (Digit 4, Digit 5); closed hardware and software, community models only, sold to businesses outright or as a service.
tags: [humanoid, biped, digit, agility-robotics, warehouse, raas, reinforcement-learning, commercial]
category: humanoid
tier: B
openness: closed-reference
maker: Agility Robotics (renamed Agility in 2026)
year: 2019
license: {hardware: , software: , docs: }
links: {repo: , docs: , cad: , paper: , site: "https://www.agilityrobotics.com/solutions/digit-5"}
specs: {dof: 20, payload_kg: 16, reach_mm: , mass_kg: 45, size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "20 motors (brushless DC with custom transmissions); passive shin and tarsus joints with leaf springs", mcu: , compute: "two Intel i7 CPUs; payload bay for a user computer such as an Intel NUC or NVIDIA Jetson", sensors: ["lidar", "four Intel RealSense depth cameras", "MEMS IMU", "absolute and incremental joint encoders"], sim_models: ["Agility simulator (proprietary)", "URDF (adubredu/DigitRobot.jl)", "MJCF (HumanoidBench, humanoid_bench/assets/digit)", "MJCF with a ROS 2 Humble wrapper (MindSpaceInc/Digit-MuJoCo-ROS2)"], ros2: none}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: , stars: , active: }
use_cases: [research, reinforcement-learning, locomotion, manipulation]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://www.agilityrobotics.com/solutions/digit-5", title: "Agility: Digit 5 product page (preliminary specifications)", accessed: 2026-11-18}
  - {url: "https://robotsguide.com/robots/digit", title: "IEEE Robots guide: Digit", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/the-evolution-of-digit-agility-robotics-journey-from-cassie-to-digit-5/", title: "The Robot Report: The evolution of Digit, from Cassie to Digit 5 (2026-09-16)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/agilitys-digit-5-humanoid-has-new-legs-batteries-safety-upgrades/", title: "The Robot Report: Agility's Digit 5 humanoid has new legs, batteries, safety upgrades (2026-09-15)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/agility-robotics-reports-18m-revenue-ahead-of-humanoid-spac/", title: "The Robot Report: Agility Robotics reports $1.8M revenue ahead of humanoid SPAC (2026-09-07)", accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2303.03381", title: Real-World Humanoid Locomotion with Reinforcement Learning, accessed: 2026-11-18}
  - {url: "https://github.com/adubredu/DigitRobot.jl", title: DigitRobot.jl README, accessed: 2026-11-18}
  - {url: "https://github.com/carlosferrazza/humanoid-bench", title: HumanoidBench repository, accessed: 2026-11-18}
  - {url: "https://github.com/MindSpaceInc/Digit-MuJoCo-ROS2", title: Digit-MuJoCo-ROS2 README, accessed: 2026-11-18}
  - {url: "https://en.wikipedia.org/wiki/Agility_Robotics", title: "Wikipedia: Agility Robotics", accessed: 2026-11-18}
---

# Agility Digit

A bipedal humanoid from Agility Robotics (renamed Agility in 2026) with Cassie-style spring legs,
a torso, arms and perception [3][6][10]. It appears in RL papers [6]; Digit 4 moves warehouse totes,
Digit 5 was announced in September 2026 [3][4], and Agility sells only to businesses [5].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Digit v3 (2019), the version before Digit 4 (2023) and the one the community models describe | [3][9] |
| Degrees of freedom | 30 in the floating-base model; 20 actuated: 6 of 8 joints per leg, 4 per arm | [6] |
| Height, mass | about 1.6 m and 45 kg (the frontmatter values) [6]; IEEE's Robots guide lists 175 cm and 65 kg [2] | [2][6] |
| Payload | up to 16 kg [2]; The Robot Report says Digit 3 stacked boxes up to 18 kg [3] | [2][3] |
| Battery | custom 1.2 kWh lithium-polymer pack; runtime not stated | [2] |
| Sensors | lidar, four Intel RealSense depth cameras, MEMS IMU, joint encoders | [2] |
| Compute | two Intel i7 CPUs, plus a payload bay for a user computer (NUC or Jetson) | [2] |
| Digit 5 (maker's preliminary claims) | 23 kg repeatable lift, 2.2 m reach, 10:1 run-to-charge ratio, 20 h of work in 24 h | [1] |

## How it works

Each leg has eight joints, six of them motorised. The shin and tarsus are passive, coupled by leaf
springs and a four-bar linkage, and rods from the tarsus drive the toe [6]. These closed chains are
hard for GPU simulators: the Berkeley team trained in Isaac Gym with approximations, then checked
policies in Agility's own high-fidelity simulator, which models the chains and sensor noise [6].

Agility's software and API are closed, and there is no ROS 2 driver. Community models: DigitRobot.jl
gives a URDF with inverse kinematics but no licence file [7]; HumanoidBench ships a Digit MJCF in an
MIT repo [8]; Digit-MuJoCo-ROS2 wraps a v3 MJCF in a ROS 2 Humble simulation, unlicensed, 2023 [9].

| Version | Year | Notes | Source |
|---|---|---|---|
| Digit 3 | 2019 | first commercial version; delivery and box stacking; Ford bought the first two | [3] |
| Digit 4 | 2023 | backward-bending knees; warehouse tote handling at GXO, Schaeffler, Toyota Canada and Amazon; 2:1 run-to-charge | [3][4] |
| Digit 5 | announced 2026-09-15 | new legs with cycloidal actuators; 1.81 m, 129 kg; 90 min run, 9 min charge; early access in the first half of 2027 | [4] |

## What it is used for

- Humanoid RL: Berkeley's transformer controller, trained in simulation, walked outdoors on Digit [6].
- Warehouse logistics: Digit runs at 9 customer sites with over 65,000 operating hours [5]; GXO
  signed the first humanoid robots-as-a-service contract with Agility in 2024 [10].
- Benchmarks: HumanoidBench includes Digit next to the Unitree H1 [8].

## Cost and BOM

No public price list exists, so the frontmatter `cost` stays empty. Agility's S-4 filing, as The
Robot Report described it, gave these Digit 5 terms; it calls the subscription rate illustrative [5]:

| Option | Price (USD) | Type | Date | Source |
|---|---|---|---|---|
| Robots-as-a-service | about 8,500 a month (about 102,000 a year) plus a 25,000 deployment fee | lease | 2026-09-07 | [5] |
| Outright purchase | about 200,000, plus 20,000 deployment and about 36,000 a year for software and maintenance | retail | 2026-09-07 | [5] |

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Hardware, firmware, robot software, Agility simulator | — | Not published | Proprietary |
| URDF and inverse kinematics | URDF, Julia | [DigitRobot.jl](https://github.com/adubredu/DigitRobot.jl) [7] | No licence file |
| MuJoCo model | MJCF | [HumanoidBench](https://github.com/carlosferrazza/humanoid-bench) [8] | MIT (repo licence) |
| ROS 2 simulation | ROS 2 packages, MJCF | [Digit-MuJoCo-ROS2](https://github.com/MindSpaceInc/Digit-MuJoCo-ROS2) [9] | No licence file |

## Strengths and limits

- **Strengths:** a humanoid in real paid warehouse work [5]; legs with published zero-shot sim-to-real
  RL results [6]; a maker simulator that models the closed-chain legs [6].
- **Limits:** closed hardware and software with no ROS 2 driver [6][9]; community models lack clear
  licences [7][9]; business-only pricing [5]; published height and mass differ [2][6].

## Related robots

- [Agility Robotics Cassie](cassie.md): Digit's legs-only predecessor [3].
- [Unitree H1](unitree-h1.md): the other humanoid in HumanoidBench [8].
- [Boston Dynamics Atlas](boston-dynamics-atlas.md) and [Unitree G1](unitree-g1.md): other humanoids.

## Sources

1. [Agility: Digit 5 product page (preliminary specifications)](https://www.agilityrobotics.com/solutions/digit-5), accessed 2026-11-18
2. [IEEE Robots guide: Digit](https://robotsguide.com/robots/digit), accessed 2026-11-18
3. [The Robot Report: The evolution of Digit, from Cassie to Digit 5 (2026-09-16)](https://www.therobotreport.com/the-evolution-of-digit-agility-robotics-journey-from-cassie-to-digit-5/), accessed 2026-11-18
4. [The Robot Report: Agility's Digit 5 humanoid has new legs, batteries, safety upgrades (2026-09-15)](https://www.therobotreport.com/agilitys-digit-5-humanoid-has-new-legs-batteries-safety-upgrades/), accessed 2026-11-18
5. [The Robot Report: Agility Robotics reports $1.8M revenue ahead of humanoid SPAC (2026-09-07)](https://www.therobotreport.com/agility-robotics-reports-18m-revenue-ahead-of-humanoid-spac/), accessed 2026-11-18
6. [Real-World Humanoid Locomotion with Reinforcement Learning](https://arxiv.org/abs/2303.03381), accessed 2026-11-18
7. [DigitRobot.jl README](https://github.com/adubredu/DigitRobot.jl), accessed 2026-11-18
8. [HumanoidBench repository](https://github.com/carlosferrazza/humanoid-bench), accessed 2026-11-18
9. [Digit-MuJoCo-ROS2 README](https://github.com/MindSpaceInc/Digit-MuJoCo-ROS2), accessed 2026-11-18
10. [Wikipedia: Agility Robotics](https://en.wikipedia.org/wiki/Agility_Robotics), accessed 2026-11-18
