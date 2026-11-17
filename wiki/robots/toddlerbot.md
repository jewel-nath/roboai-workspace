---
type: robot
name: ToddlerBot
summary: Stanford's 0.56 m, 30-DoF 3D-printed Dynamixel humanoid with a Jetson Orin NX, built for RL and imitation learning, with a full sim-to-real and teleop stack.
tags: [humanoid, dynamixel, jetson, 3d-printed, reinforcement-learning, imitation-learning, mujoco, mjx, teleop, loco-manipulation]
category: humanoid
tier: A
openness: full
maker: Stanford University (Haochen Shi, Weizhuo Wang, Shuran Song, C. Karen Liu)
year: 2025
license: {hardware: CC-BY-NC-SA-4.0, software: MIT, docs: MIT}
links: {repo: https://github.com/hshi74/toddlerbot, docs: https://hshi74.github.io/toddlerbot/, cad: https://cad.onshape.com/documents/565bc33af293a651f66e88d2, paper: https://arxiv.org/abs/2502.00893, site: https://toddlerbot.github.io/}
specs: {dof: 30, payload_kg: 1.48, reach_mm: , mass_kg: 3.48, size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "Dynamixel XC330-T288, XC430-T240BB, XM430-W210, 2XL430-W250 and 2XC430-W250 (2XC variant)", mcu: , compute: NVIDIA Jetson Orin NX 16GB, sensors: ["2x fisheye USB camera (Arducam)", "BNO085 IMU", "2x microphone"], sim_models: ["MJCF (ToddlerBot repo, toddlerbot/descriptions)", "URDF (ToddlerBot repo, toddlerbot/descriptions)"], ros2: none}
cost: {type: bom, usd: 5728, as_of: 2026-11-17, source: "https://docs.google.com/spreadsheets/d/e/2PACX-1vQmoxJnTnUaQ_-WAAjnchBhaX5HZ4ElUV5pXksEV6GEbeEjiie1E_BdN9XCMt6FtfBaopXoaeSOeMDg/pubhtml"}
build: {difficulty: 3, hours: , print_hours: }
maturity: {last_commit: 2026-11-16, stars: 804, active: true}
use_cases: [research, reinforcement-learning, imitation-learning, teleop, locomotion, manipulation, data-collection]
evidence: researched
last_verified: 2026-11-17
sources:
  - {url: https://github.com/hshi74/toddlerbot, title: "ToddlerBot repository (README, pyproject.toml, source tree)", accessed: 2026-11-17}
  - {url: https://github.com/hshi74/toddlerbot/blob/main/CHANGELOG.md, title: ToddlerBot changelog (2.0 release), accessed: 2026-11-17}
  - {url: https://arxiv.org/abs/2502.00893, title: "ToddlerBot paper, arXiv 2502.00893 v4", accessed: 2026-11-17}
  - {url: https://toddlerbot.github.io/, title: ToddlerBot project website, accessed: 2026-11-17}
  - {url: https://hshi74.github.io/toddlerbot/, title: ToddlerBot documentation, accessed: 2026-11-17}
  - {url: "https://docs.google.com/spreadsheets/d/e/2PACX-1vQmoxJnTnUaQ_-WAAjnchBhaX5HZ4ElUV5pXksEV6GEbeEjiie1E_BdN9XCMt6FtfBaopXoaeSOeMDg/pubhtml", title: ToddlerBot BOM (Release) spreadsheet, accessed: 2026-11-17}
  - {url: https://hshi74.github.io/toddlerbot/hardware/03_3d_printing.html, title: ToddlerBot docs 3D printing, accessed: 2026-11-17}
  - {url: https://hshi74.github.io/toddlerbot/hardware/02_pcb8ch.html, title: ToddlerBot docs PCB (8ch) sourcing, accessed: 2026-11-17}
  - {url: https://hshi74.github.io/toddlerbot/hardware/04_assembly_manual.html, title: ToddlerBot docs assembly, accessed: 2026-11-17}
  - {url: https://hshi74.github.io/toddlerbot/sections/05_tips_and_tricks.html, title: ToddlerBot docs tips and tricks, accessed: 2026-11-17}
  - {url: https://hshi74.github.io/toddlerbot/features/03_diy_battery.html, title: ToddlerBot docs DIY battery, accessed: 2026-11-17}
  - {url: https://arxiv.org/abs/2601.03607, title: "Locomotion Beyond Feet, arXiv 2601.03607", accessed: 2026-11-17}
  - {url: https://cad.onshape.com/documents/565bc33af293a651f66e88d2, title: ToddlerBot Onshape document, accessed: 2026-11-17}
  - {url: https://makerworld.com/en/models/1733983, title: ToddlerBot MakerWorld release, accessed: 2026-11-17}
  - {url: https://github.com/hshi74/toddlerbot/issues, title: ToddlerBot GitHub issues, accessed: 2026-11-17}
---

# ToddlerBot

ToddlerBot is a 0.56 m, 30-DoF humanoid built from 3D-printed parts, Dynamixel servos and an NVIDIA
Jetson Orin NX. Haochen Shi, Weizhuo Wang, Shuran Song and C. Karen Liu made it at Stanford University [3, 4].
It is a full research platform for RL walking, diffusion-policy manipulation and teleop data collection, with a BOM of about USD 5,700 [3, 6].

## Specs

| Item | Value | Source |
|---|---|---|
| Height | About 0.56 m | 3 |
| Mass | 3,484 g (paper; its abstract rounds to 3.4 kg) | 3 |
| Degrees of freedom | 30 active, not counting end effectors: 7 per arm, 6 per leg, 2 neck, 2 waist. The optional parallel-jaw gripper adds one XC330 per hand | 3, 6 |
| Lift | Lifted up to 1,484 g in a whole-body lifting test | 3 |
| Actuators (2XC variant) | 2x 2XC430-W250 (hip roll and pitch), 6x 2XL430-W250 (shoulder roll and yaw, elbow, wrist), 6x XC330-T288 (neck, waist, hip yaw), 4x XC430-T240BB (shoulder pitch, ankle roll), 4x XM430-W210 (knee, ankle pitch) | 3, 6 |
| Actuators (2XM variant) | Stronger hips and arms: by the BOM counts, six 2XC430-W250 take the place of the arms' 2XL430s and four XM430-W350 take the place of the hips' two 2XC430s | 2, 6 |
| Compute | NVIDIA Jetson Orin NX 16GB | 3, 6 |
| Sensors | Two fisheye USB cameras, a BNO085 IMU in the chest, two microphones; also a speaker | 3, 6 |
| Battery | 2000 mAh LiPo (215 g), or a DIY 4S 21700 pack of 5000 mAh (330 g) | 3, 11 |
| Runtime | Not settled: the paper gives 3 to 5 h of intermittent use in one place and about 2 h in another; the longest untethered walk in its endurance test was 19 min | 3 |
| Control rates | RL policy at 50 Hz on the Jetson CPU; motor control loop 200 Hz since 2.0 | 2, 3 |
| Cost | USD 5,727.94 BOM for the 2XC variant, USD 7,293.56 for 2XM, without tools, the PCB or the parallel gripper | 6 |

## How it works

### Mechanics and actuation

The structure is fully 3D-printed; the BOM calls for two rolls of PLA-CF and one of PLA [3, 6]. Joints
use Dynamixel X-series servos on a TTL bus, with ball bearings, thrust needle bearings and bushings
at the joints [6]. Version 2.0 (August 2025) shortened the legs by 30 mm and simplified the knee by
removing its parallel links. It also reinforced the arms against impacts and added anti-slip rubber
on the feet [2]. Two end effectors swap in under two minutes: a compliant palm and a parallel-jaw
gripper [3]. Printed calibration jigs snap onto the arm, neck, hip and ankle joints to set the zero
pose in about a minute [3]. The authors call the robot robust: replacing a broken part took 21
minutes of printing and 14 minutes of assembly in their test [3].

### Electronics and firmware

A custom board (TTLPowerBoardV8) combines power distribution and servo communication. It gives the
Jetson eight USB channels to the servo chains and removes the need for a U2D2 adapter [2, 8]. You
order it assembled from JLCPCB with the Gerber, BOM and placement files in the docs [8]. Two Pololu
12 V step-down regulators, XT30 connectors and a rocker switch complete the power path [6]. The
servos keep their stock firmware. Since 2.0, a C++ driver with Python bindings runs the Dynamixel
loop at 200 Hz [2].

### Software and control

Everything is one pip-installable Python package, `toddlerbot`, with C++ extensions [1, 5]. It covers
low-level control, MuJoCo/MJX training (PPO via rsl_rl or Brax), diffusion-policy training and
deployment [1, 2]. Walking is a PPO policy trained across 1,024 parallel environments; it tracks
velocity commands and transferred to hardware zero-shot [3]. Version 2.0 added DeepMimic-style
motion tracking, used for crawling and cartwheels [2]. It also added terrain generation, ONNX
export and IMU noise modelling [2]. Teleop uses a second upper body as leader arms plus a handheld PC
(Steam Deck or ROG Ally X); since 2.0 a Meta Quest VR mode is also supported [2, 3]. A keyframe app
edits animations such as push-ups and pull-ups [1, 2]. Stereo depth runs with FoundationStereo at
10 Hz on the Jetson using TensorRT [2]. There is no ROS layer [1].

### Simulation

MJCF and URDF models for the `toddlerbot_2xc` and `toddlerbot_2xm` variants, with and without
grippers, live in `toddlerbot/descriptions` [1]. They are generated from the Onshape CAD with an
`onshape_to_robot` pipeline that you can rerun after editing the design [1, 2]. The same folder has a
system-identification folder for each motor type. Scene files cover flat ground, stairs, boxes and a
cart [1].

## What it is used for

- **RL locomotion**: velocity-tracking walking and keyframe-tracked skills such as crawling and
  cartwheels [2, 3].
- **Imitation learning**: with 60 teleoperated demonstrations, collected in about 20 minutes, a
  diffusion policy reached 90 % success on a bimanual task and 75 % on a full-body task, over 20
  trials each [3].
- **Follow-on research**: "Locomotion Beyond Feet" (2026) builds a multi-skill system on ToddlerBot.
  A depth-based skill classifier picks among trained policies to cross obstacles [1, 12].
- **Replication**: a computer-science student with no hardware experience built a second unit in
  three days, including printing. The paper also reports five community builds, about a week each [3].

## Cost and BOM

The BOM is a published Google Sheet with two quantity columns, one per variant [6]. Prices were read on
2026-11-17; the sheet shows no date of its own.

| Item | Price | Type | Source |
|---|---|---|---|
| Essentials, 2XC variant | USD 5,727.94 | bom | 6 |
| Essentials, 2XM variant | USD 7,293.56 | bom | 6 |
| Motors (2XC) | USD 4,069.96, about 71 % of the 2XC total | bom | 6 |
| Jetson Orin NX 16GB (reComputer J4012) | USD 955 | bom | 6 |
| Optional parallel-jaw gripper (2x XC330-T288) | USD 206.78, not in the totals above | bom | 6 |
| Tools: Bambu Lab X1-Carbon, bench supply, screwdrivers, soldering kit | USD 1,976.13 | bom | 6 |
| Extras: teleop leader arms with ROG Ally X, DIY battery, safety stand, sysID clamp | USD 2,252.73 | bom | 6 |
| ToddlerBot 2.0 fully assembled, WowRobo | USD 4,299, without Jetson, Wi-Fi card or battery | retail | 6 |

The paper says motors and computer make up about 90 % of the cost [3]. The assembled-robot listing
comes from the project's BOM, which says the team is not affiliated with that seller. We could not
open the seller's page to check the price [6]. The PCB is not in the BOM. The docs say its price
depends on JLCPCB fees and tariffs, and that five boards cost little more than two [8].

## Building it

**Difficulty 3:** printing, a fab-assembled PCB, soldered power cables, servo ID setup and
jig calibration. There is no machining and there are no custom actuators, but this is the upper end
of 3: a novice built one in three days and community builds averaged a week [3].

- **Printing:** the docs strongly recommend Bambu Lab printers for part tolerances [7]. The 3MF files
  on MakerWorld carry each part's orientation and print profile, which the docs call important for
  strength [7, 14]. The project gives no total print time.
- **Assembly:** a 2.0 interactive manual on tnkr.ai, overview videos, a YouTube playlist per
  subassembly and the Onshape document [9, 13]. The docs order the work as arms, legs, cables, head,
  waist, torso, motor IDs, wiring, power board, then a standing test [9].
- **Pitfalls the docs name:**
  - XC330s cannot sustain 4 Mbps on this setup; run every servo at 2 Mbps [10].
  - Intermittent bus faults are often a loose cable; one turned out to be at an ankle [10].
  - Waist gears wear. Reprint them in PLA-CF with more wall loops [10].
  - Repeated screwing strips printed holes; reprint the part [10].
  - A low battery cuts torque; watch the voltage tester to avoid over-discharge [10].
  - An HDMI cable cannot reach the Jetson inside the torso, so use SSH [10].
- **Issues:** a report of wrong servos in the BOM (issue 8) is closed. Two of the six issues are
  open, both questions about follow-on research code and motor modelling [15].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Mechanical CAD | Onshape, configuration-based parts and assemblies | Onshape document | CC-BY-NC-SA-4.0 (non-commercial) [1] |
| Print files | 3MF with print profiles | MakerWorld release | CC-BY-NC-SA-4.0 [1, 14] |
| Power and comms board | Gerber ZIP, BOM and placement CSVs for JLCPCB | `docs/_static/TTLPowerBoardV8.zip` | Not stated separately [8] |
| Software | Python with C++ extensions | the repo | MIT [1] |
| Robot models | MJCF, URDF, collision and visual meshes | `toddlerbot/descriptions` | MIT (part of the codebase) [1] |
| Motion library | keyframe `.lz4` files | `motion/` | MIT [1] |
| Docs and assembly manual | Sphinx site, tnkr.ai manual, YouTube | docs site | MIT for the docs [1, 9] |
| BOM | Google Sheet | linked from the docs | Not stated [6] |

The design files are **non-commercial** (CC BY-NC-SA); the code and docs are MIT [1].

## Strengths and limits

**Strengths**
- A complete ML stack in one repo: sim models, RL and diffusion training, teleop, deployment and sysID [1, 3].
- Proven reproducibility: a novice replication and several community builds [3].
- Repairs are fast: break a printed part, reprint it, recalibrate with a jig [3].
- Active development: 2.0 in August 2025, follow-on research in 2026, commits in November 2026 [1, 2].

**Limits**
- Expensive for its size: most of the USD 5,700 BOM is Dynamixel servos and the Jetson [3, 6].
- The paper says the off-the-shelf motors' speed, torque and bus speed limit agile behaviour. It
  adds that its actuator model ignores motor temperature [3].
- Small scale limits work with human-sized objects. Printed parts break on impact more readily
  than metal ones [3].
- Runtime figures in the paper conflict, and it gives no walking speed [3].
- Non-commercial hardware licence.
- Tied to Dynamixel motors and a Jetson; no ROS 2 interface [1].

## What to reuse

- **Snap-on zero-point calibration jigs** that set every joint's zero in about a minute [3].
- **One power-and-comms board** that replaces the U2D2 and splits the servos into USB chains for
  higher loop rates [2, 8].
- **Layered robot config**: global defaults, per-robot settings and a git-ignored per-instance
  motor file [2].
- **CAD-to-MJCF pipeline** that regenerates models, with tuned collision geometry, after each design change [2].
- **Leader-arm teleop** built from a second copy of the upper body, for cheap, matched-kinematics data collection [3].
- **Swappable end effectors** on a common wrist [3].

## Related robots

- [Microban](microban.md): a much smaller and cheaper Dynamixel humanoid with an RL walking policy.
- [Berkeley Humanoid Lite](berkeley-humanoid-lite.md): an open research humanoid with custom printed actuators.
- [Open Duck Mini](open-duck-mini.md): a small open robot trained with RL in MuJoCo.

## Sources

1. [ToddlerBot repository (README, pyproject.toml, source tree)](https://github.com/hshi74/toddlerbot), accessed 2026-11-17
2. [ToddlerBot changelog (2.0 release)](https://github.com/hshi74/toddlerbot/blob/main/CHANGELOG.md), accessed 2026-11-17
3. [ToddlerBot paper, arXiv 2502.00893 v4](https://arxiv.org/abs/2502.00893), accessed 2026-11-17
4. [ToddlerBot project website](https://toddlerbot.github.io/), accessed 2026-11-17
5. [ToddlerBot documentation](https://hshi74.github.io/toddlerbot/), accessed 2026-11-17
6. [ToddlerBot BOM (Release) spreadsheet](https://docs.google.com/spreadsheets/d/e/2PACX-1vQmoxJnTnUaQ_-WAAjnchBhaX5HZ4ElUV5pXksEV6GEbeEjiie1E_BdN9XCMt6FtfBaopXoaeSOeMDg/pubhtml), accessed 2026-11-17
7. [ToddlerBot docs 3D printing](https://hshi74.github.io/toddlerbot/hardware/03_3d_printing.html), accessed 2026-11-17
8. [ToddlerBot docs PCB (8ch) sourcing](https://hshi74.github.io/toddlerbot/hardware/02_pcb8ch.html), accessed 2026-11-17
9. [ToddlerBot docs assembly](https://hshi74.github.io/toddlerbot/hardware/04_assembly_manual.html), accessed 2026-11-17
10. [ToddlerBot docs tips and tricks](https://hshi74.github.io/toddlerbot/sections/05_tips_and_tricks.html), accessed 2026-11-17
11. [ToddlerBot docs DIY battery](https://hshi74.github.io/toddlerbot/features/03_diy_battery.html), accessed 2026-11-17
12. [Locomotion Beyond Feet, arXiv 2601.03607](https://arxiv.org/abs/2601.03607), accessed 2026-11-17
13. [ToddlerBot Onshape document](https://cad.onshape.com/documents/565bc33af293a651f66e88d2), accessed 2026-11-17
14. [ToddlerBot MakerWorld release](https://makerworld.com/en/models/1733983), accessed 2026-11-17
15. [ToddlerBot GitHub issues](https://github.com/hshi74/toddlerbot/issues), accessed 2026-11-17
