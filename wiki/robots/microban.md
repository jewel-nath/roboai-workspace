---
type: robot
name: Microban
summary: A 30 cm, 19-DoF humanoid with fully 3D-printed parts and Dynamixel XL330 servos, run from a Raspberry Pi Zero 2 W with an RL walking policy, for about USD 567 in parts.
tags: [humanoid, biped, dynamixel, xl330, raspberry-pi, 3d-printed, reinforcement-learning, mujoco, onnx]
category: humanoid
tier: A
openness: full
maker: Marc Duclusaud, Rhoban team (LaBRI, University of Bordeaux)
year: 2026
license: {hardware: CC-BY-NC-SA-4.0, software: GPL-3.0-or-later, docs: CC-BY-NC-SA-4.0}
links: {repo: https://github.com/Rhoban/microban, docs: https://github.com/Rhoban/microban/tree/main/docs, cad: https://cad.onshape.com/documents/d424992a192a8ce34ffce163, paper: , site: }
specs: {dof: 19, payload_kg: , reach_mm: , mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "19x Dynamixel XL330-M288-T serial-bus servos", mcu: , compute: "Raspberry Pi Zero 2 W with the Pollen RPI Robot HAT", sensors: ["IMU on the RPI Robot HAT (BMI088 driver)"], sim_models: ["MJCF (Microban repo, src/model/mjcf)", "URDF (Microban repo, src/model/urdf)"], ros2: none}
cost: {type: bom, usd: 567, as_of: 2026-11-17, source: https://github.com/Rhoban/microban/blob/main/docs/bom.md}
build: {difficulty: 3, hours: , print_hours: }
maturity: {last_commit: 2026-09-10, stars: 692, active: true}
use_cases: [education, research, reinforcement-learning, locomotion, hobby]
evidence: researched
last_verified: 2026-11-17
sources:
  - {url: https://github.com/Rhoban/microban, title: "Microban repository (README, pyproject.toml, source tree)", accessed: 2026-11-17}
  - {url: https://github.com/Rhoban/microban/blob/main/docs/bom.md, title: Microban bill of materials, accessed: 2026-11-17}
  - {url: https://github.com/Rhoban/microban/blob/main/docs/printing.md, title: Microban printing guide, accessed: 2026-11-17}
  - {url: https://github.com/Rhoban/microban/blob/main/docs/assembly.md, title: Microban assembly guide, accessed: 2026-11-17}
  - {url: https://github.com/Rhoban/microban/blob/main/docs/deployment.md, title: Microban deployment guide, accessed: 2026-11-17}
  - {url: https://github.com/Rhoban/microban/blob/main/docs/usage.md, title: Microban usage guide, accessed: 2026-11-17}
  - {url: https://github.com/Rhoban/microban/blob/main/LICENSE, title: Microban licence summary (LICENSE and cad/LICENSE), accessed: 2026-11-17}
  - {url: https://github.com/Rhoban/microban/tree/main/src/model, title: Microban MJCF and URDF models, accessed: 2026-11-17}
  - {url: https://github.com/MarcDcls/mjlab_microban, title: mjlab_microban training environments, accessed: 2026-11-17}
  - {url: https://github.com/pollen-robotics/elec_RPI_Robot_HAT, title: Pollen Robotics RPI Robot HAT repository, accessed: 2026-11-17}
  - {url: "https://en.robotis.com/shop_en/item.php?it_id=902-0163-000", title: ROBOTIS shop page for the XL330-M288-T, accessed: 2026-11-17}
  - {url: https://doi.org/10.5281/zenodo.20784789, title: Microban v1.0.0 Zenodo record, accessed: 2026-11-17}
  - {url: https://github.com/Rhoban/microban/discussions, title: Microban GitHub Discussions, accessed: 2026-11-17}
  - {url: https://github.com/Rhoban/microban/discussions/6, title: "Discussion 6, sim-to-real gap with Feetech STS3215", accessed: 2026-11-17}
  - {url: https://github.com/Rhoban/microban/discussions/16, title: "Discussion 16, a build that does not walk well", accessed: 2026-11-17}
---

# Microban

Microban is a 30 cm open-source humanoid with 19 Dynamixel XL330 servos, a Raspberry Pi Zero 2 W and
fully 3D-printed parts. Marc Duclusaud built it in the Rhoban team at LaBRI, University of Bordeaux [1].
It gives you a walking humanoid with a trained RL policy and a full sim-to-real path for about USD 567 in parts [2, 9].

## Specs

| Item | Value | Source |
|---|---|---|
| Height | About 30 cm (maker's claim) | 1 |
| Degrees of freedom | 19: 6 per leg (hip yaw, roll, pitch; knee; ankle pitch, roll), 3 per arm (shoulder pitch, roll; elbow), 1 head. No gripper | 4 |
| Actuators | 19x Dynamixel XL330-M288-T, 0.52 N·m stall at 5 V, 18 g each (ROBOTIS figures) | 2, 11 |
| Mass | Not published. The link masses in the repo's MJCF model sum to about 0.82 kg; this is a CAD figure, not a weighed robot | 8 |
| Compute | Raspberry Pi Zero 2 W | 1 |
| Power | 2x 18650 Li-ion cells in series (2S, 8.4 V full) with a BMS, charged over USB-C | 2, 4 |
| Control loop | 50 Hz | 6 |
| Bus | Dynamixel Protocol 2.0 at 1 Mbps | 4 |
| Runtime, speed | Not published | — |
| Cost | About USD 567 in parts; about USD 623 with the motor setup tools (maker's BOM) | 2 |

## How it works

### Mechanics and actuation

About 30 printed PLA parts carry the 19 servos [1, 3]. Hip and ankle pitch-roll pairs sit in
"double-motor blocks", two servos side by side in one printed housing [4]. Where a joint has no idler
horn, a POM washer between two steel shims acts as a plain bearing instead of a needle bearing [2].
The CAD has built-in stops that decide which self-collisions can happen [1]. Left and right
tibias, femurs and hip blocks are mirror parts with cable channels, so the daisy-chained servo cables
route inside the limbs [3, 4].

### Electronics and firmware

The Pi Zero 2 W sits under the Pollen Robotics RPI Robot HAT, an open board that drives the
Dynamixel TTL bus and carries an IMU [2, 10]. You must have the HAT made at a PCB assembly service;
it is not sold off the shelf [2]. Microban's code reads the HAT's IMU through a BMI088 driver [1].
The servos form daisy chains that start at hand-made splitter cables near the board [4]. The battery
module (2S holder plus BMS) plugs into the trunk top through an XT30 connector. The trunk top holds
the USB-C charger and the power switch, so the pack charges whether the robot is on or off [4].

There is no separate microcontroller firmware. The servos keep their stock firmware; you only set
each ID, the baud rate and a few registers once with Dynamixel Wizard and a U2D2 [4].

### Software and control

The Pi runs a Python control loop at 50 Hz [6]. Its dependencies include `rustypot` (Dynamixel
driver), `placo` (inverse kinematics), `onnxruntime` and Pollen's BMI088 IMU library [1]. A scheduler
runs "moves" on top of a neutral pose: walk, head and squat. Walk is an RL policy loaded from an
ONNX file and driven by `vx`, `vy` and `vtheta` commands; squat uses inverse kinematics [6]. You
drive the robot from a PC over SSH with `make` targets and the keyboard, or with a Bluetooth Xbox
controller, also headless [6]. A prebuilt SD-card image holds the OS and the code [5]. New behaviours
are subclasses of a small `Move` class [6].

### Simulation

The repo has MJCF and URDF models generated from the Onshape assembly with onshape-to-robot [8].
`make sim` runs the same scheduler against MuJoCo, with settable actuator and sensor delays [1, 6].
Policies are trained in the separate `mjlab_microban` repo (mjlab, one velocity-tracking task). That
repo exports ONNX and uses domain randomisation plus BAM actuator models for sim-to-real [9].

## What it is used for

- Learning humanoid locomotion end to end on a desk-sized robot: train a walking policy in
  simulation, export ONNX and run it on the Pi [6, 9].
- Teaching and student projects; the maker aims it at makers, students and hobbyists [1].
- A base for remixes. The Discussions show builds that scale it to 1.5 times the size, add
  eyes and a time-of-flight sensor, or swap in Feetech STS3215 servos [13].
- It is citable as Zenodo software record 10.5281/zenodo.20784789, v1.0.0 [12]. No paper describes it.

## Cost and BOM

The BOM lists approximate prices with mostly European shop links (Amazon France, Nkon, Screwerk,
AliExpress) [2]. Its line items sum to USD 567.35, matching its stated total of about USD 567 (type
`bom`, checked 2026-11-17) [2].

| Item | Price (BOM) | Note | Source |
|---|---|---|---|
| 19x Dynamixel XL330-M288-T | USD 454.10 (19 x 23.90) | 80 % of the robot; ROBOTIS still lists USD 23.90 on 2026-11-17 | 2, 11 |
| RPI Robot HAT | ~USD 30 | A rough figure; the cost depends on the fab and the order size | 2 |
| Raspberry Pi Zero 2 W | ~USD 15 | | 2 |
| Battery holder, BMS, switch, USB-C charger, 2x 18650 cells | ~USD 38 | Murata VTC6 cells suggested | 2 |
| Micro SD card, screws, shims, filament | ~USD 30 | Less than one roll of PLA | 2 |
| U2D2 + U2D2 Power Hub + 5 V supply | USD 56.10 | Tools for motor setup, one set for any number of robots | 2 |

The 19 servo kits hold 114 M2x6 screws but the build needs 124, so buy at least 10 more [2].
Optional extras, such as spare screws, crimp pins, a crimp tool, spare cables and a cell charger,
add about USD 115 [2]. No kit is sold. The licence forbids anyone but the author from selling parts,
kits or robots without a commercial licence [1].

## Building it

**Difficulty 3:** printing plus soldering (splitter cables, battery module, charger wiring), a
fab-assembled PCB, crimping, servo ID setup and flashing an SD image.

- **Printing:** PLA at 0.12 mm layers and 15 % infill [1]. Hip, pelvis, arm bearing supports and
  shoulders must print in set orientations so the shim bearings fit, even if that adds supports [3].
  The project gives no print time.
- **Tools:** soldering iron, heat shrink and hot glue. A JST EH crimp tool helps, because shortened
  servo cables are better re-crimped than spliced [2, 4].
- **Steps:** set the 19 motor IDs one at a time, make the cables, build the legs, torso and
  electronics, flash the image and set Wi-Fi [4, 5]. The project gives no total build time.
- **Pitfalls the docs name:**
  - Cut power only after `make shutdown`, or the SD card can corrupt [6].
  - The Pi Zero 2 W joins only 2.4 GHz Wi-Fi [5].
  - When ordering the HAT from JLCPCB, check that resistor R33 is in stock [2].
  - On the double-motor blocks, plug the cables in before sliding the servos into place [4].
- **From the Discussions:** a builder's knees oscillate at about twice the simulated gait frequency
  and the robot shuffles; no reply yet [15]. Swapping servos (for example Feetech STS3215) breaks the
  shipped policy. The maker says to re-measure delays, identify the new actuator with BAM and retrain [14].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Mechanical CAD | STEP (parts and full assembly), STL | `cad/` in the repo | CC-BY-NC-SA-4.0 (non-commercial) [7] |
| Assembly reference | Onshape (view online) | Onshape document linked from the README | Not stated separately [1] |
| Control software | Python | `src/` in the repo | GPL-3.0 (headers say GPL-3.0-or-later) [7] |
| Robot models | MJCF, URDF | `src/model/` in the repo | MJCF header says Apache-2.0 [8] |
| Walk policy | ONNX | `src/agents/walk.onnx` | GPL-3.0 (repo default) [7] |
| Training pipeline | Python (mjlab) | `MarcDcls/mjlab_microban` | Apache-2.0 [9] |
| Controller board | KiCad 9 | Pollen Robotics `elec_RPI_Robot_HAT` | Apache-2.0 per its repo page [10] |
| Docs | Markdown | `docs/` in the repo | README says CC-BY-NC-SA-4.0; LICENSE puts every non-`cad/` folder under GPL-3.0 [1, 7] |
| SD-card image | `.img.xz` | Releases on `MarcDcls/microban` | Not stated [5] |

The hardware licence is **non-commercial**: you may build and modify Microban, but you may not sell it,
its parts or kits without the author's written permission [1]. The Zenodo record lists CC-BY-4.0,
which does not match the repo [12].

## Strengths and limits

**Strengths**
- Cheap for a walking humanoid with a trained policy. Most of the cost is off-the-shelf servos at list price [2].
- Everything prints on a desktop printer in PLA. The full STEP assembly and every part are in the repo [1, 3].
- Short path from simulation to robot: one MJCF model, an mjlab training repo and ONNX on the Pi [6, 8, 9].
- Clean move API for adding behaviours, and headless gamepad control for demos [6].

**Limits**
- No published mass, speed, runtime or payload figures [1].
- No cameras or extra sensors yet; the head is cosmetic [3].
- The control board must be made to order, which is the main sourcing hurdle [2, 13].
- The XL330s are small, low-torque servos, and the policy is tuned to them; other actuators need re-identification and retraining [11, 14].
- Non-commercial hardware licence; the licence statements conflict on docs and models [1, 7, 8, 12].
- A young project: version 1.0.0 dates from mid-2026 [12].

## What to reuse

- **POM-on-steel shim bearings** in place of needle bearings or idler horns: cheap, printable seats [2, 3].
- **Double-motor blocks** that pack two servos for a 2-DoF hip or ankle into one printed part [4].
- **Mirrored limb parts with cable channels** so daisy-chained servo cables route inside the robot [3, 4].
- **Charge-while-off power path**: BMS pack, USB-C charger and switch wired so charging bypasses the switch [4].
- **The `Move` scheduler pattern**: independent behaviours layered on a neutral pose, with one
  normalised velocity command shared by keyboard, gamepad and simulation [6].
- **A simulator with delay knobs** for actuation and each sensor, to test policies before hardware [1].

## Related robots

- [Open Duck Mini](open-duck-mini.md): another small RL-walking robot run from a Pi Zero 2 W.
- [ToddlerBot](toddlerbot.md): a larger Dynamixel humanoid for ML research.
- [Berkeley Humanoid Lite](berkeley-humanoid-lite.md): an open humanoid with custom printed actuators.
- [Robot Soccer Kit](robot-soccer-kit.md): another open robot from the Rhoban team.
- [Sesame](sesame.md): a much cheaper servo walker, quadruped rather than biped.

## Sources

1. [Microban repository (README, pyproject.toml, source tree)](https://github.com/Rhoban/microban), accessed 2026-11-17
2. [Microban bill of materials](https://github.com/Rhoban/microban/blob/main/docs/bom.md), accessed 2026-11-17
3. [Microban printing guide](https://github.com/Rhoban/microban/blob/main/docs/printing.md), accessed 2026-11-17
4. [Microban assembly guide](https://github.com/Rhoban/microban/blob/main/docs/assembly.md), accessed 2026-11-17
5. [Microban deployment guide](https://github.com/Rhoban/microban/blob/main/docs/deployment.md), accessed 2026-11-17
6. [Microban usage guide](https://github.com/Rhoban/microban/blob/main/docs/usage.md), accessed 2026-11-17
7. [Microban licence summary (LICENSE and cad/LICENSE)](https://github.com/Rhoban/microban/blob/main/LICENSE), accessed 2026-11-17
8. [Microban MJCF and URDF models](https://github.com/Rhoban/microban/tree/main/src/model), accessed 2026-11-17
9. [mjlab_microban training environments](https://github.com/MarcDcls/mjlab_microban), accessed 2026-11-17
10. [Pollen Robotics RPI Robot HAT repository](https://github.com/pollen-robotics/elec_RPI_Robot_HAT), accessed 2026-11-17
11. [ROBOTIS shop page for the XL330-M288-T](https://en.robotis.com/shop_en/item.php?it_id=902-0163-000), accessed 2026-11-17
12. [Microban v1.0.0 Zenodo record](https://doi.org/10.5281/zenodo.20784789), accessed 2026-11-17
13. [Microban GitHub Discussions](https://github.com/Rhoban/microban/discussions), accessed 2026-11-17
14. [Discussion 6, sim-to-real gap with Feetech STS3215](https://github.com/Rhoban/microban/discussions/6), accessed 2026-11-17
15. [Discussion 16, a build that does not walk well](https://github.com/Rhoban/microban/discussions/16), accessed 2026-11-17
