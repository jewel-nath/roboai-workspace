---
type: robot
name: Open Duck Mini v2
summary: A 42 cm, 3D-printed biped in the style of Disney's BD-X droid, with Onshape CAD, a BOM of about EUR 400 and an open RL sim-to-real pipeline on cheap Feetech servos.
tags: [biped, bd-x, feetech, sts3215, 3d-printed, reinforcement-learning, sim-to-real, mujoco, onshape, raspberry-pi]
category: legged
tier: A
openness: full
maker: Antoine Pirrone and contributors
year: 2024
license: {hardware: Apache-2.0, software: Apache-2.0, docs: Apache-2.0}
links: {repo: "https://github.com/apirrone/Open_Duck_Mini", docs: "https://tnkr.ai/explore/docs/open-duck-mini/open-duck-mini-v2", cad: "https://cad.onshape.com/documents/64074dfcfa379b37d8a47762/w/3650ab4221e215a4f65eb7fe/e/0505c262d882183a25049d05", paper: , site: }
specs: {dof: 16, payload_kg: , reach_mm: , mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "14 Feetech STS3215 serial-bus servos (7.4 V) and 2 9 g hobby servos", mcu: , compute: "Raspberry Pi Zero 2W", sensors: ["BNO055 IMU", "4 foot contact switches"], sim_models: ["URDF (Open_Duck_Mini repo)", "MJCF (Open_Duck_Mini repo and Open_Duck_Playground)"], ros2: none}
cost: {type: bom, usd: 437, as_of: 2026-11-17, source: "https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/edit?usp=sharing"}
build: {difficulty: 3, hours: , print_hours: }
maturity: {last_commit: 2026-01-31, stars: 4746, active: true}
use_cases: [reinforcement-learning, locomotion, hobby]
evidence: researched
last_verified: 2026-11-17
sources:
  - {url: "https://github.com/apirrone/Open_Duck_Mini", title: "Open_Duck_Mini repository README (v2 branch)", accessed: 2026-11-17}
  - {url: "https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/edit?usp=sharing", title: "Open Duck Mini v2 bill of materials (Google Sheet)", accessed: 2026-11-17}
  - {url: "https://cad.onshape.com/documents/64074dfcfa379b37d8a47762/w/3650ab4221e215a4f65eb7fe/e/0505c262d882183a25049d05", title: "Open Duck Mini v2 Onshape document", accessed: 2026-11-17}
  - {url: "https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/print_guide.md", title: "Open Duck Mini print guide", accessed: 2026-11-17}
  - {url: "https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/assembly_guide.md", title: "Open Duck Mini assembly guide", accessed: 2026-11-17}
  - {url: "https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/configure_motors.md", title: "Open Duck Mini motor configuration guide", accessed: 2026-11-17}
  - {url: "https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/sim2real.md", title: "Open Duck Mini sim2real notes", accessed: 2026-11-17}
  - {url: "https://github.com/apirrone/Open_Duck_Mini_Runtime/tree/v2", title: "Open_Duck_Mini_Runtime repository (v2 branch)", accessed: 2026-11-17}
  - {url: "https://github.com/apirrone/Open_Duck_Playground", title: "Open_Duck_Playground repository", accessed: 2026-11-17}
  - {url: "https://github.com/apirrone/Open_Duck_reference_motion_generator", title: "Open Duck reference motion generator", accessed: 2026-11-17}
  - {url: "https://arxiv.org/abs/2501.05204", title: "Grandia et al., Design and Control of a Bipedal Robotic Character (RSS 2024)", accessed: 2026-11-17}
  - {url: "https://github.com/rimim/AWD", title: "rimim/AWD repository README and LICENSE", accessed: 2026-11-17}
  - {url: "https://tnkr.ai/explore/docs/open-duck-mini/open-duck-mini-v2", title: "Tnkr Open Duck Mini v2 build guide and kit", accessed: 2026-11-17}
  - {url: "https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=2&format=csvdata", title: "ECB euro reference rate, USD", accessed: 2026-11-17}
  - {url: "https://hackaday.com/2025/04/05/disneys-bipedal-bdx-series-droid-gets-the-diy-treatment", title: "Hackaday, Disney's bipedal BDX-series droid gets the DIY treatment", accessed: 2026-11-17}
  - {url: "https://github.com/apirrone/Open_Duck_Mini/issues", title: "Open_Duck_Mini issue tracker", accessed: 2026-11-17}
  - {url: "https://techcrunch.com/2026/08/27/hugging-face-is-selling-a-cute-399-open-source-duck-robot-microduck/", title: "TechCrunch, Hugging Face is selling a 399 USD open-source duck robot", accessed: 2026-11-17}
---

# Open Duck Mini v2

A small 3D-printed biped that copies the look and gait of Disney's BD-X droid, about 42 cm tall.
Made by Antoine Pirrone with Grégoire Passault and other contributors, sponsored by Hugging Face and Pollen Robotics [1][15].
For a builder it is the cheapest complete open pipeline we know for a walking RL biped: Onshape CAD, a EUR 400 BOM, motor models and training code.

## Specs

| Item | Value | Source |
|---|---|---|
| Height | About 42 cm with legs extended (maker's claim) | 1 |
| Actuated joints (`dof`) | 16: five per leg (hip yaw, roll and pitch, knee, ankle), four in the neck and head, two antennas | 6, 1 |
| Leg and head servos | 14 Feetech STS3215, 7.4 V version (BOM notes 19 kg·cm) | 2 |
| Antenna servos | 2 × 9 g hobby servos | 2 |
| Compute | Raspberry Pi Zero 2W | 1, 2 |
| Sensors | BNO055 IMU, four SS-10 foot contact switches | 2, 5 |
| Battery | Two 18650 cells (2S) with a BMS, USB-C charging, 5 V regulator for the Pi | 2 |
| Mass | Not published. The training model (MJCF) sums to about 2.1 kg, with part masses taken from the slicer | 7, 9 |
| Speed, runtime | Not published | — |
| BOM cost | EUR 398.10 (main list), EUR 432.34 with the expression package | 2 |

## How it works

### Mechanics and actuation

The design lives in one public Onshape document [3]. Every main joint is a Feetech STS3215 serial-bus
servo bolted into PLA parts. The feet have a TPU sole and two press-fit microswitches each that close on
ground contact [4][5][2]. Each leg has five joints, with no separate ankle roll. The head sits on a
four-joint neck, and two 9 g servos move the antennas [6][2]. The head also carries expression parts: eye
LEDs, a small projector and a speaker; a microphone and camera are listed but not yet integrated [2].
Community mods in `print/mods/` add body covers, cable guides and a stand [1].

### Electronics and firmware

There is no custom board and no microcontroller of its own. A Waveshare bus servo adapter connects the
servo bus to the Pi over USB, and the BNO055 hangs on the Pi's I2C bus [2][8]. The servos run their stock
firmware; the motor guide sets each servo's ID and zero position with a script before assembly [6]. Power
comes from two Molicel 18650 cells in series through a 2S BMS [2].

### Software and control

The robot runs a neural-network policy, exported as ONNX, on the Pi. It reads joint positions and speeds,
the IMU and the foot switches, and outputs servo position targets [7][8]. The runtime repo sets up the Pi
(I2C, USB latency timer, Xbox controller over Bluetooth) and offers a pre-built SD-card image, release
0.2.3 [8]. Training happens in Open Duck Playground, built on MuJoCo Playground, with a joystick task and
optional imitation reward [9]. That reward follows Disney's BD-X paper; the reference motions come from
a parametric walk engine built on Rhoban's Placo [7][10][11]. Two trained walking policies ship in the
main repo [1].

### Simulation

The Onshape design is exported with onshape-to-robot to URDF and MJCF. A URDF and MJCF of v2 live in
`mini_bdx/robots/open_duck_mini_v2/`, and a lightweight MJCF for MJX training lives in the playground [1][7][9].
The servo model (damping, kp, friction, armature, force range) was identified with Rhoban's BAM, and the
fitted STS3215 parameters are published, so you do not need to redo the identification [7].

## What it is used for

- **RL locomotion on a hobby budget:** the project's whole aim is sim-to-real walking with cheap servos
  that are hard to model; Hackaday reported it stable when shoved in April 2025 [7][15].
- **Imitation-style training:** a worked example of Disney's reference-motion reward on open hardware [7][11].
- **Character robotics:** a desk-scale droid with expressive head, antennas and lights [2].
- An older Isaac Gym trainer, AWD by rimim, targets the duck and a full-size version; its last commit
  (2024-10-21) shows the project was public in 2024 [12].

## Cost and BOM

- **BOM (main list):** EUR 398.10, about USD 437 at the ECB rate of 1.0989 USD per EUR on 2026-11-17 [2][14].
  The sheet's own lowest-price estimate is EUR 331.10 (about USD 364) [2].
- **With the expression package:** EUR 432.34 (about USD 475); some of these parts only come in bulk packs [2].
- **Biggest item:** 14 STS3215 servos at EUR 14 each, EUR 196 in total, about half the BOM [2].
- **Kit:** Tnkr sells an Open Duck kit with parts, hardware and electronics, listed at USD 600 on
  2026-11-17 (seller's price) [13].
- The README rounds the target to "under $400" [1]; the itemised sheet is in euros and links to EU shops.
- **Buy instead:** Pollen Robotics announced Microduck, a 25 cm duck robot at USD 399, in August 2026.
  It is a separate product, not a kit of this design [17].

## Building it

**Difficulty 3:** printing plus soldering, a BMS battery pack, per-servo ID and zero setup, and IMU and
offset calibration. The project does not state build hours or print hours.

- **Printing:** about 40 STL parts in PLA at 15% infill; the foot soles are TPU at 40% [4].
- **Tools:** soldering iron, M3 heat-set inserts, Loctite 243 on metal-to-metal screws only [5].
- **Order of work:** configure each servo first, then assemble trunk, feet, shins, thighs and hips [5][6].
- **Pitfalls from the docs and issues:**
  - The assembly guide is marked incomplete, and the CAD-to-sim guide is flagged as outdated [5][1].
  - Buy the 7.4 V STS3215, not the 12 V one; the motor model was identified at 7.4 V [2][7].
  - Hip-pitch servo orientation matters for the zero position [5].
  - Servo-bus CRC errors, battery and servo voltage questions, and robots that fail to walk forward
    recur in the issue tracker [16].
  - Run the runtime checklist (joint offsets, IMU orientation, foot switches) before a policy [7][8].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Mechanical CAD | Onshape | [Onshape document](https://cad.onshape.com/documents/64074dfcfa379b37d8a47762/w/3650ab4221e215a4f65eb7fe/e/0505c262d882183a25049d05) | Apache-2.0 (repo licence) |
| Printable parts | STL; mods in STEP and 3MF | `print/` in the repo | Apache-2.0 |
| BOM | Google Sheet, EUR | [BOM sheet](https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/edit?usp=sharing) | None stated |
| Wiring | draw.io diagram; no custom PCB | `docs/` in the repo | Apache-2.0 |
| Robot models | URDF, MJCF | repo and Open_Duck_Playground | Apache-2.0 in the repo; none in the playground |
| Training code | Python (MuJoCo Playground) | [Open_Duck_Playground](https://github.com/apirrone/Open_Duck_Playground) | No licence file |
| Onboard runtime | Python | [Open_Duck_Mini_Runtime](https://github.com/apirrone/Open_Duck_Mini_Runtime) | No licence file |
| Reference motions | Python (Placo) | [reference motion generator](https://github.com/apirrone/Open_Duck_reference_motion_generator) | No licence file |
| Trained policies | ONNX | repo root | Apache-2.0 |
| AWD trainer (Isaac Gym) | Python | [rimim/AWD](https://github.com/rimim/AWD) | NVIDIA License: non-commercial, research or evaluation only |
| Docs | Markdown; Tnkr guide | `docs/`, Tnkr | Apache-2.0 for repo docs |

Disney's BD-X itself is closed: Disney has published the paper, not its CAD, firmware or code [11].
The AWD trainer that trains BD-X-style policies uses the NVIDIA License, which allows only
non-commercial use [12]. The runtime, playground and motion generator repos have no licence file,
so reuse rights for that code are unclear until the authors add one [8][9][10].

## Strengths and limits

**Strengths**
- Very low cost for a walking RL biped, from parts sold worldwide [2].
- Complete chain from CAD to policy: Onshape, onshape-to-robot, identified servo model, trainer, runtime [7].
- Large community: about 4,700 stars, a Discord, community mods and a third-party kit [1][13].

**Limits**
- Hobby servos limit torque and are hard to model; the authors call sim-to-real hard for this reason [7].
- Docs are a working log: the assembly guide is incomplete and some scripts are undocumented [1][5].
- The companion code repos carry no licence, and the BOM is in euros with EU links [2][8][9].
- No published mass, speed or battery life.

## What to reuse

- Identify your servos with BAM and put the fitted damping, armature and friction in the MJCF before training [7].
- Override CAD part masses with slicer estimates when parts are printed with infill [7].
- Use a reference-motion imitation reward from a parametric walk engine instead of motion capture [7][10].
- Foot microswitches as cheap contact sensing for the policy [5].
- Configure servo IDs and zero positions before assembly, then correct offsets in software [6].

## Related robots

- [ToddlerBot](toddlerbot.md): a larger printed humanoid for ML research, also on serial-bus servos.
- [Microban](microban.md): a 30 cm printable Dynamixel humanoid.
- [Berkeley Humanoid Lite](berkeley-humanoid-lite.md): RL-walking printed humanoid with custom actuators.
- [Upkie](upkie.md): open wheeled biped with a similar sim-to-real workflow.
- Disney BD-X: the closed original. Pollen Robotics Microduck: a commercial duck robot.

## Sources

1. [Open_Duck_Mini repository README (v2 branch)](https://github.com/apirrone/Open_Duck_Mini), accessed 2026-11-17
2. [Open Duck Mini v2 bill of materials (Google Sheet)](https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/edit?usp=sharing), accessed 2026-11-17
3. [Open Duck Mini v2 Onshape document](https://cad.onshape.com/documents/64074dfcfa379b37d8a47762/w/3650ab4221e215a4f65eb7fe/e/0505c262d882183a25049d05), accessed 2026-11-17
4. [Open Duck Mini print guide](https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/print_guide.md), accessed 2026-11-17
5. [Open Duck Mini assembly guide](https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/assembly_guide.md), accessed 2026-11-17
6. [Open Duck Mini motor configuration guide](https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/configure_motors.md), accessed 2026-11-17
7. [Open Duck Mini sim2real notes](https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/sim2real.md), accessed 2026-11-17
8. [Open_Duck_Mini_Runtime repository (v2 branch)](https://github.com/apirrone/Open_Duck_Mini_Runtime/tree/v2), accessed 2026-11-17
9. [Open_Duck_Playground repository](https://github.com/apirrone/Open_Duck_Playground), accessed 2026-11-17
10. [Open Duck reference motion generator](https://github.com/apirrone/Open_Duck_reference_motion_generator), accessed 2026-11-17
11. [Grandia et al., Design and Control of a Bipedal Robotic Character (RSS 2024)](https://arxiv.org/abs/2501.05204), accessed 2026-11-17
12. [rimim/AWD repository README and LICENSE](https://github.com/rimim/AWD), accessed 2026-11-17
13. [Tnkr Open Duck Mini v2 build guide and kit](https://tnkr.ai/explore/docs/open-duck-mini/open-duck-mini-v2), accessed 2026-11-17
14. [ECB euro reference rate, USD](https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=2&format=csvdata), accessed 2026-11-17
15. [Hackaday, Disney's bipedal BDX-series droid gets the DIY treatment](https://hackaday.com/2025/04/05/disneys-bipedal-bdx-series-droid-gets-the-diy-treatment), accessed 2026-11-17
16. [Open_Duck_Mini issue tracker](https://github.com/apirrone/Open_Duck_Mini/issues), accessed 2026-11-17
17. [TechCrunch, Hugging Face is selling a 399 USD open-source duck robot](https://techcrunch.com/2026/08/27/hugging-face-is-selling-a-cute-399-open-source-duck-robot-microduck/), accessed 2026-11-17
