---
type: robot
name: AgiBot X1 (Lingxi X1)
summary: 1.3 m, 33 kg humanoid from AgiBot with 29 joint actuators and two grippers, published with STEP and SolidWorks files, drawings, BOM and assembly SOP but no hardware licence; its RL training and control code are open (BSD-3-Clause, Mulan PSL v2).
tags: [humanoid, agibot, zhiyuan, x1, lingxi, powerflow, aimrt, step, solidworks, bom, reinforcement-learning, isaac-gym, mujoco, ros2]
category: humanoid
tier: B
openness: partial
maker: AgiBot (Zhiyuan Robotics)
year: 2024
license: {hardware: , software: MulanPSL-2.0 AND BSD-3-Clause, docs: }
links: {repo: "https://github.com/AgibotTech/agibot_x1_hardware", docs: "https://www.agibot.com/DOCS/OS", cad: "https://github.com/AgibotTech/agibot_x1_hardware", paper: , site: "https://agibot.com/products/X1"}
specs: {dof: 31, payload_kg: 0.5, reach_mm: , mass_kg: 33, size_mm: , speed_mps: 1, runtime_h: 2}
stack: {actuators: "AgiBot PowerFlow: 6 x R86-3, 9 x R86-2, 10 x R52 rotary and 4 x L28 linear; 2 OmniPicker grippers", mcu: "2 x Xyber DCU (EtherCAT to FDCAN)", compute: "Intel i7-13620H mini PC", sensors: ["Intel RealSense D435", "2 x YIS320 IMU"], sim_models: ["URDF (agibot_x1_train, 12 leg joints)", "MJCF (agibot_x1_train and agibot_x1_infer, 12 leg joints)"], ros2: official}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2025-04-18, stars: 1083, active: false}
use_cases: [research, reinforcement-learning, locomotion]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://agibot.com/products/X1", title: "AgiBot X1 product page", accessed: 2026-11-18}
  - {url: "https://www.agibot.com/DOCS/OS", title: "AgiBot X1 development guide (open source)", accessed: 2026-11-18}
  - {url: "https://github.com/AgibotTech/agibot_x1_hardware", title: "agibot_x1_hardware repository (CAD, drawings, BOM, SOP)", accessed: 2026-11-18}
  - {url: "https://github.com/AgibotTech/agibot_x1_infer", title: agibot_x1_infer README, accessed: 2026-11-18}
  - {url: "https://github.com/AgibotTech/agibot_x1_train", title: agibot_x1_train README, accessed: 2026-11-18}
  - {url: "https://rbtx.de/en-GB/components/humanoid/agibot-x1-humanoid-robot-humanoid", title: "RBTX: AGIBOT X1 humanoid robot listing", accessed: 2026-11-18}
---

# AgiBot X1 (Lingxi X1)

A 1.3 m, 33 kg humanoid from AgiBot (Zhiyuan Robotics) [1], released with its full mechanical
design files, BOM and assembly guide in October 2024 [2][3], which is rare for a humanoid this size.
The files carry no licence, so you may study them but have no written permission to copy, change or
share them. The training and control software is licensed [4][5].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | X1 as listed in the development guide and the October 2024 BOM | [2][3] |
| Degrees of freedom | 29 joint actuators and 2 grippers, head extensible by 3; the product page says 34; `dof: 31` | [1][2] |
| Height, mass | 130 cm; 33 kg (maker's claims) | [1] |
| Speed, runtime, payload | walking 1 m/s; 2 h; 0.5 kg per arm (maker's claims) | [1] |
| R86-3 / R86-2 / R52 | peak 200 / 80 / 19 N·m; rated 60 / 20 / 6 N·m; 1.28 / 0.81 / 0.45 kg; 48 V (maker's claims) | [1] |
| L28 linear actuator | 110 N thrust, 50 mm/s, 24 V (maker's claims) | [1] |
| Joint bus | DCU: EtherCAT to 3 x FDCAN at 5 Mbps, 1 kHz, up to 16 in cascade | [1] |
| Gripper | OmniPicker: 30 N, 120 mm stroke, 0.43 kg (maker's claims) | [1] |
| Compute, sensors, battery | i7-13620H mini PC; RealSense D435; two YIS320 IMUs; 48 V 8 Ah battery | [3] |

## How it works

The shells are plastic (printed resin in the 2024 BOM, ABS in the 2025 one), the structure is
machined 6061-T6 aluminium and sheet metal, and the feet are rubber [3]. The BOM lists waist and
ankle linkage assemblies and four L28 linear actuators beside the rotary joints [3]. The October
2024 BOM and the guide count 9 R86-2 [2][3]; the March 2025 BOM lists 6 [3].

Two Xyber DCUs bridge EtherCAT from the PC to the actuators' FDCAN buses [1][4]. agibot_x1_infer
runs on AgiBot's AimRT middleware with an RL control module (ONNX Runtime), a DCU driver and a
joystick module; it needs ROS 2 Humble, can publish to native ROS 2 nodes, and has a MuJoCo
simulation mode [4]. It bundles SOEM, an EtherCAT master under GPL-2.0 [4].

agibot_x1_train builds on humanoid-gym: it trains walking in Isaac Gym Preview 4, checks it in
MuJoCo and exports JIT or ONNX policies [5]. Its URDF and MJCF models have only the 12 leg joints
[5]. There is no Menagerie model.

## What it is used for

- RL locomotion with a published stack: train, check in MuJoCo, then run on the robot [4][5].
- A reference design: the CAD, drawings, BOM and assembly SOP show how a 1.3 m humanoid is put
  together, part by part [3].

## Cost and BOM

Price on request: AgiBot's page offers only a contact link [1], and RBTX lists the X1 with "Contact
us" and a usual delivery of 3 weeks [6]. The BOMs give quantities, materials and shop links but no
prices [3], so `cost` and `build` stay empty.

## Building it

The hardware repo has three dated releases (2024-10-24, 2025-01-08, 2025-03-07) with whole-robot
and part STEP files, SolidWorks 2022 sources, drawings, BOMs, a tool-kit list with calibration
blocks, and an assembly SOP; assembly and bench-test videos are on Baidu Pan [3]. Printed and
machined parts must be made to the drawings; the PC, battery, IMUs and power parts have Taobao
links; the actuators, DCUs, grippers and cable sets are AgiBot kit parts [3]. The guide covers
actuator checks, a desk joint test, IMU setup, zero calibration and deployment [2]. Files and
BOMs are in Chinese; no build time is stated [3].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| CAD and drawings | STEP, SolidWorks 2022, 2D drawings (zipped) | [agibot_x1_hardware](https://github.com/AgibotTech/agibot_x1_hardware) [3] | None: no licence file in the repo, none in the guide |
| BOM, SOP, tool list | XLSX, videos on Baidu Pan | agibot_x1_hardware [3] | None |
| Control software | C++ on AimRT, ROS 2 Humble | [agibot_x1_infer](https://github.com/AgibotTech/agibot_x1_infer) [4] | MulanPSL-2.0; bundled SOEM GPL-2.0 |
| RL training, models | Python; URDF, MJCF | [agibot_x1_train](https://github.com/AgibotTech/agibot_x1_train) [5] | BSD-3-Clause in setup.py and file headers; no LICENSE file |
| Actuator and DCU firmware, electronics | — | Not published | Closed |

## Strengths and limits

- **Strengths:** full mechanical files, BOM and assembly SOP for a 1.3 m humanoid [3]; open RL
  training and control code with a ROS 2 bridge [4][5]; maker specs for every actuator [1].
- **Limits:** no hardware licence [2][3]; actuators, DCUs and their firmware are AgiBot's own [1][3];
  models cover the legs only [5]; BOM versions disagree [3]; no commits since April 2025 [3][4].

## Related robots

- [Berkeley Humanoid Lite](berkeley-humanoid-lite.md) and [ToddlerBot](toddlerbot.md): open
  humanoids with licensed hardware files.
- [Unitree G1](unitree-g1.md) and [Booster T1](booster-t1.md): commercial humanoids of similar size.

## Sources

1. [AgiBot X1 product page](https://agibot.com/products/X1), accessed 2026-11-18
2. [AgiBot X1 development guide (open source)](https://www.agibot.com/DOCS/OS), accessed 2026-11-18
3. [agibot_x1_hardware repository (CAD, drawings, BOM, SOP)](https://github.com/AgibotTech/agibot_x1_hardware), accessed 2026-11-18
4. [agibot_x1_infer README](https://github.com/AgibotTech/agibot_x1_infer), accessed 2026-11-18
5. [agibot_x1_train README](https://github.com/AgibotTech/agibot_x1_train), accessed 2026-11-18
6. [RBTX: AGIBOT X1 humanoid robot listing](https://rbtx.de/en-GB/components/humanoid/agibot-x1-humanoid-robot-humanoid), accessed 2026-11-18
