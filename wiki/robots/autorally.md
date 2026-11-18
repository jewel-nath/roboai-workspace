---
type: robot
name: AutoRally
summary: Georgia Tech's 1:5-scale off-road autonomous rally car, an HPI Baja 5SC with RTK GPS, an IMU, two cameras and a GPU computer box, with open build instructions and ROS 1 code; the platform of the MPPI aggressive-driving papers.
tags: [autonomous-driving, rc-car, ackermann, off-road, mppi, rtk-gps, gtsam, gazebo, ros1, georgia-tech]
category: mobile-base
tier: B
openness: partial
maker: Georgia Institute of Technology (AutoRally project)
year: 2016
license: {hardware: , software: BSD-2-Clause, docs: }
links: {repo: "https://github.com/AutoRally/autorally", docs: "https://github.com/AutoRally/autorally/wiki", cad: "https://github.com/AutoRally/autorally_platform_instructions", paper: "https://arxiv.org/abs/1806.00678", site: "https://autorally.github.io/"}
specs: {dof: 3, payload_kg: , reach_mm: , mass_kg: 21, size_mm: "1000 x 600 x 400", speed_mps: 27, runtime_h: 1}
stack: {actuators: "Castle Creations 2028 brushless motor with Mamba XL-X ESC; Savox steering servo; Savox servo on Mecatech front hydraulic brakes", mcu: "Teensy LC boards (parts list)", compute: "Mini-ITX PC: quad-core Intel i7, 32 GB RAM, Nvidia GTX 750 Ti", sensors: ["MicroStrain 3DM-GX5-25 IMU", "Hemisphere P307 RTK GPS, 20 Hz", "Hall-effect wheel speed sensors, 70 Hz", "two FLIR Blackfly S global-shutter cameras, 1280 x 1024"], sim_models: ["URDF/xacro (autorally_description)", "Gazebo 9 vehicle and track (autorally_gazebo)"], ros2: none}
cost: {type: bom, usd: 14635.25, as_of: 2018-03-01, source: "https://github.com/AutoRally/autorally_platform_instructions/blob/V1.4/autorally_platform_parts_list.xlsx"}
build: {difficulty: 4, hours: 100, print_hours: }
maturity: {last_commit: 2021-08-16, stars: 793, active: false}
use_cases: [research, navigation, reinforcement-learning, data-collection]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://autorally.github.io/specs/", title: "AutoRally website: platform specs", accessed: 2026-11-18}
  - {url: "https://autorally.github.io/build/", title: "AutoRally website: build your own platform", accessed: 2026-11-18}
  - {url: "https://autorally.github.io/history/", title: "AutoRally website: project history", accessed: 2026-11-18}
  - {url: "https://github.com/AutoRally/autorally", title: "autorally repository (melodic-devel)", accessed: 2026-11-18}
  - {url: "https://github.com/AutoRally/autorally_platform_instructions", title: "autorally_platform_instructions repository (V1.4)", accessed: 2026-11-18}
  - {url: "https://github.com/AutoRally/autorally_platform_instructions/blob/V1.4/autorally_platform_parts_list.xlsx", title: "AutoRally platform parts list, version 1.4 (2018-03-01)", accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/1806.00678", title: "AutoRally: An Open Platform for Aggressive Autonomous Driving (Goldfain et al., IEEE Control Systems Magazine 2019)", accessed: 2026-11-18}
  - {url: "https://ieeexplore.ieee.org/document/7487277", title: "Aggressive driving with model predictive path integral control (Williams et al., ICRA 2016)", accessed: 2026-11-18}
---

# AutoRally

AutoRally is a 1:5-scale autonomous rally car from Georgia Tech, built on an off-road RC truck [1][7].
The project began in 2011; its first fast autonomous runs used the MPPI controller, published at ICRA
2016, and the lab grew a fleet of six cars [3][8]. For a builder it is a complete published recipe for a
large outdoor research car: manuals, parts list, STL and DXF parts, ROS 1 code and a Gazebo twin [2][5].

## Specs

| Item | Value | Source |
|---|---|---|
| Chassis | HPI Baja 5SC 1:5 RC truck, converted from gas to a brushless electric motor | 1, 6 |
| Size, mass | 1 m long, 0.6 m wide, 0.4 m high; 21 kg | 1 |
| Top speed | 27 m/s (60 mph), as the project states | 1 |
| Actuators | Drive motor, steering servo, front-brake servo; `dof: 3` | 6 |
| Sensors | IMU up to 1 kHz; RTK GPS at 20 Hz; Hall-effect wheel speed at 70 Hz; two global-shutter cameras, 1280 x 1024 at 70 fps | 1 |
| Compute box | Mini-ITX: quad-core Intel i7, 32 GB RAM, Nvidia GTX 750 Ti, Wi-Fi and XBee | 1 |
| Runtime | Chassis 4S pair: about 1 h typical, 15 min at full load (6500 mAh on the specs page, 9000 mAh in the parts list); compute box 6S 11000 mAh: about 3 h | 1, 6 |
| Safety | RC transmitter switches between manual and autonomous; remote run stop works in both modes | 1 |

## How it works

The chassis is a stock HPI Baja 5SC with off-the-shelf upgrades to carry the payload, a Castle Creations
motor and speed controller in place of the gas engine, servo-worked hydraulic front brakes, and printed
mounts and enclosures [1][6]. A separate aluminium Mini-ITX compute box with its own battery attaches
through a standard mount and interface, so any box pairs with any chassis [1]. Teensy boards sit in the
compute box and run-stop circuit; wiring diagrams and schematics are in the instructions repo [5][6].

The `autorally` repository is ROS 1 Melodic code for Ubuntu 18.04: core nodes, a GTSAM state estimator
fusing GPS and IMU, a GPS waypoint follower, a constant-speed controller, the MPPI controller (which needs
a CUDA GPU), an operator control station and the Gazebo simulation [1][2][4]. The simulator keeps the
car's ROS interface, with parameters measured on the real car [1]. We found no ROS 2 port or MuJoCo model.

## What it is used for

- **Aggressive autonomous driving:** MPPI samples thousands of trajectories on the GPU [4][8].
- **Research fleet:** six cars served several Georgia Tech labs; the platform paper describes their
  experiments and a driving dataset [3][7].
- **Simulation first:** the Gazebo twin runs the same controllers before track tests [1][4].

## Cost and BOM

The parts list, version 1.4 dated 2018-03-01, totals **$14,635.25** per car (type `bom`): chassis
$5,424.14, sensors and electronics $6,117.30, computing $3,093.81 [6]. A shared RTK GPS base station and
operator laptop add $8,658.01, tools $781.08 [6]. Parts come from about 25 suppliers, at 2018 prices [5].

## Building it

**Difficulty 4:** a small student team with soldering, 3D printing, Ubuntu and ROS skills; the sheet-metal
compute box may need a fabrication shop [5]. About 100 hours for one chassis and compute box [2]; print
time is not stated. Work through the chassis and compute box PDFs, then the operating procedures [5].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Build manuals, parts list, wiring diagrams | PDF, XLSX, PNG | [autorally_platform_instructions](https://github.com/AutoRally/autorally_platform_instructions) [5] | None stated |
| Printed and cut parts | STL, DXF | same repository, `models/` [5] | None stated |
| ROS code | ROS 1 (catkin), C++ and Python | [autorally](https://github.com/AutoRally/autorally) [4] | BSD-2-Clause in source headers; `autorally_gazebo` Apache-2.0 |

## Strengths and limits

- **Strengths:** everything needed to build the car is published, down to a priced parts list and wiring
  diagrams [5][6]; real field speed and sensing (RTK GPS, GPU) at 1:5 scale [1].
- **Limits:** about $14,600 per car plus a base station [6]; ROS 1 Melodic only, last commit 2021 [4];
  hardware files carry no licence [5]; it takes a 2 to 3 person team to operate [1].

## What to reuse

- **Detachable compute box:** a self-powered computer with one standard mount and interface lets any
  computer drive any chassis [1].

## Related robots

- [F1TENTH](f1tenth.md): a smaller 1/10-scale racing car with a current ROS 2 stack and BOM.
- [OpenBot](openbot.md): a far cheaper phone-driven car for learned driving.

## Sources

1. [AutoRally website: platform specs](https://autorally.github.io/specs/), accessed 2026-11-18
2. [AutoRally website: build your own platform](https://autorally.github.io/build/), accessed 2026-11-18
3. [AutoRally website: project history](https://autorally.github.io/history/), accessed 2026-11-18
4. [autorally repository (melodic-devel)](https://github.com/AutoRally/autorally), accessed 2026-11-18
5. [autorally_platform_instructions repository (V1.4)](https://github.com/AutoRally/autorally_platform_instructions), accessed 2026-11-18
6. [AutoRally platform parts list, version 1.4 (2018-03-01)](https://github.com/AutoRally/autorally_platform_instructions/blob/V1.4/autorally_platform_parts_list.xlsx), accessed 2026-11-18
7. [AutoRally: An Open Platform for Aggressive Autonomous Driving (Goldfain et al., IEEE Control Systems Magazine 2019)](https://arxiv.org/abs/1806.00678), accessed 2026-11-18
8. [Aggressive driving with model predictive path integral control (Williams et al., ICRA 2016)](https://ieeexplore.ieee.org/document/7487277), accessed 2026-11-18
