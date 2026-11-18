---
type: robot
name: Berkeley Humanoid Lite
summary: Open 0.8 m, 16 kg humanoid from UC Berkeley whose 22 joints use 3D-printed cycloidal actuators on drone motors, with Onshape CAD, a BOM of about USD 4,350 and RL walking.
tags: [humanoid, cycloidal-gearbox, 3d-printed-actuator, bldc, can-bus, isaac-lab, mujoco, onshape, reinforcement-learning, teleoperation]
category: humanoid
tier: A
openness: full
maker: Hybrid Robotics, UC Berkeley
year: 2025
license: {hardware: CC-BY-SA-4.0, software: MIT, docs: }
links: {repo: "https://github.com/HybridRobotics/berkeley-humanoid-lite", docs: "https://berkeley-humanoid-lite.gitbook.io/docs", cad: "https://cad.onshape.com/documents/fc6443b1d89dcba950e85b60/w/94a26479973a4098a5884426/e/be3fe37849edbeadc95b9bf8", paper: "https://arxiv.org/abs/2504.17249", site: "https://lite.berkeley-humanoid.org/"}
specs: {dof: 24, payload_kg: , reach_mm: , mass_kg: 16, size_mm: , speed_mps: , runtime_h: 0.5}
stack: {actuators: "22 printed cycloidal actuators (10 x 6512 on MAD M6C12 150KV, 12 x 5010 on MAD 5010 110KV) and 2 servo grippers", mcu: "ST B-G431B-ESC1 per actuator (Recoil firmware), Arduino for the IMU", compute: "Intel N95 mini PC", sensors: ["BNO085 IMU", "AS5600 magnetic encoder per actuator"], sim_models: ["URDF (Berkeley-Humanoid-Lite-Assets)", "MJCF (Berkeley-Humanoid-Lite-Assets)", "USD (Berkeley-Humanoid-Lite-Assets)"], ros2: none}
cost: {type: bom, usd: 4351, as_of: 2026-11-17, source: "https://docs.google.com/spreadsheets/d/1AQEHcH_nPkXYfor2-h7bwNIUMmsePtAm53epnsWgZXc/edit?usp=sharing"}
build: {difficulty: 4, hours: , print_hours: }
maturity: {last_commit: 2026-03-10, stars: 2016, active: false}
use_cases: [research, reinforcement-learning, locomotion, teleop, education]
evidence: researched
last_verified: 2026-11-17
sources:
  - {url: "https://github.com/HybridRobotics/berkeley-humanoid-lite", title: "berkeley-humanoid-lite repository README", accessed: 2026-11-17}
  - {url: "https://arxiv.org/abs/2504.17249", title: "Chi et al., Demonstrating Berkeley Humanoid Lite (RSS 2025)", accessed: 2026-11-17}
  - {url: "https://lite.berkeley-humanoid.org/", title: "Berkeley Humanoid Lite project site", accessed: 2026-11-17}
  - {url: "https://berkeley-humanoid-lite.gitbook.io/docs", title: "Berkeley Humanoid Lite documentation", accessed: 2026-11-17}
  - {url: "https://docs.google.com/spreadsheets/d/1AQEHcH_nPkXYfor2-h7bwNIUMmsePtAm53epnsWgZXc/edit?usp=sharing", title: "Berkeley Humanoid Lite bill of materials (Google Sheet)", accessed: 2026-11-17}
  - {url: "https://berkeley-humanoid-lite.gitbook.io/docs/releases", title: "Berkeley Humanoid Lite docs, Releases", accessed: 2026-11-17}
  - {url: "https://berkeley-humanoid-lite.gitbook.io/docs/getting-started-with-hardware/preparing-the-tools", title: "Berkeley Humanoid Lite docs, Preparing the tools", accessed: 2026-11-17}
  - {url: "https://berkeley-humanoid-lite.gitbook.io/docs/getting-started-with-hardware/3d-printing-instructions", title: "Berkeley Humanoid Lite docs, 3D printing instructions", accessed: 2026-11-17}
  - {url: "https://berkeley-humanoid-lite.gitbook.io/docs/getting-started-with-hardware/flashing-the-motor-controllers", title: "Berkeley Humanoid Lite docs, Flashing the motor controllers", accessed: 2026-11-17}
  - {url: "https://berkeley-humanoid-lite.gitbook.io/docs/getting-started-with-software/the-on-board-computer", title: "Berkeley Humanoid Lite docs, The on-board computer", accessed: 2026-11-17}
  - {url: "https://berkeley-humanoid-lite.gitbook.io/docs/in-depth-contents/joint-id-mapping", title: "Berkeley Humanoid Lite docs, Joint ID mapping", accessed: 2026-11-17}
  - {url: "https://github.com/HybridRobotics/Berkeley-Humanoid-Lite-Assets", title: "Berkeley-Humanoid-Lite-Assets repository", accessed: 2026-11-17}
  - {url: "https://github.com/HybridRobotics/Berkeley-Humanoid-Lite-Lowlevel", title: "Berkeley-Humanoid-Lite-Lowlevel repository", accessed: 2026-11-17}
  - {url: "https://github.com/T-K-233/Recoil-Motor-Controller-BESC", title: "Recoil Motor Controller BESC firmware repository", accessed: 2026-11-17}
  - {url: "https://github.com/HybridRobotics/berkeley-humanoid-lite/issues", title: "berkeley-humanoid-lite issue tracker", accessed: 2026-11-17}
  - {url: "https://arxiv.org/abs/2407.21781", title: "Liao et al., Berkeley Humanoid, A Research Platform for Learning-based Control", accessed: 2026-11-17}
  - {url: "https://berkeley-humanoid.com/", title: "Berkeley Humanoid project site", accessed: 2026-11-17}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie", title: "MuJoCo Menagerie README", accessed: 2026-11-17}
  - {url: "https://github.com/robot-descriptions/robot_descriptions.py", title: "robot_descriptions.py README", accessed: 2026-11-17}
  - {url: "https://berkeley-humanoid-lite.gitbook.io/docs/getting-started-with-hardware/materials-and-parts-bom", title: "Berkeley Humanoid Lite docs, Materials and parts (BOM)", accessed: 2026-11-17}
---

# Berkeley Humanoid Lite

A 0.8 m, 16 kg open humanoid whose 22 joints are driven by 3D-printed cycloidal actuators built from
drone motors and cheap motor boards [2]. Made by the Hybrid Robotics lab at UC Berkeley (Yufeng Chi,
Koushil Sreenath and others), shown at RSS 2025 [2]. For a builder it is a complete open humanoid, from
actuator CAD to RL walking policy, for about USD 4,350 in parts, and its actuators are reusable on their own.

## Specs

| Item | Value | Source |
|---|---|---|
| Height, mass | 0.8 m, 16 kg | 2 |
| Joints | 22: six per leg (hip roll, yaw, pitch; knee; ankle pitch, roll), five per arm (shoulder pitch, roll, yaw; two elbow joints) | 11, 12 |
| Grippers | Two servo-driven claws; `dof` 24 counts each as one | 5, 2 |
| Actuators | 10 × 6512 (MAD M6C12 150KV motor) and 12 × 5010 (MAD 5010 110KV), each with a printed cycloidal gearbox, a B-G431B-ESC1 driver and an AS5600 encoder | 2, 5 |
| Gear ratio | 15:1 on every joint in the shipped robot configuration; the paper gives none | 13 |
| Actuator stiffness, backlash | About 319 N·m/rad; maximum backlash 0.0229 rad over six new 6512 units | 2 |
| Arm repeatability | 3.433 mm standard deviation over 100 reaches, on a 5-joint test arm | 2 |
| Compute | Intel N95 mini PC (the docs name a Beelink unit), Ubuntu 22.04 | 2, 10 |
| Buses | Four 1 Mbps CAN 2.0 buses, one per limb, through USB-CAN adapters; 250 Hz to actuators and IMU | 2 |
| IMU | BNO085, read over USB through an Arduino | 2 |
| Battery | 6S 4000 mAh LiPo, about 30 minutes; tethered power also supported | 2 |
| Locomotion policy | MLP running onboard at 25 Hz | 2 |
| Speed, payload | Not published | — |
| BOM | USD 4,350.59 (sheet), USD 4,312 (paper table) | 5, 2 |

## How it works

### Mechanics and actuation

Both actuator sizes share one design: a drone outrunner motor drives a printed cycloidal reducer
(input shaft, cycloidal disk, output shaft, housing) on small ball bearings, with a large thin bearing
between output and housing [5]. The authors chose a cycloidal drive to make up for the lower strength of
plastic gears [2]. The legs use eight 6512 and four 5010 actuators; the arms use two 6512 and eight 5010
[5]. The leg pitch actuators act through a linkage, and the torso is aluminium extrusion with brackets [5].
In a 60-hour test lifting a 0.5 kg pendulum at 0.5 m, backlash grew slightly and efficiency recovered [2].
Stiffness is well below a carbon-fibre-nylon printed cycloid from earlier work, which the authors put down
to PLA [2]. The robot can also be built legs-only as a 12-joint biped, the configuration used in the paper's
walking demo [2][12]. The paper also shows an adult-size variant with 7-joint legs [2].

### Electronics and firmware

Each actuator has its own ST B-G431B-ESC1 board running the Recoil motor controller firmware (MIT),
flashed from STM32CubeIDE [9][14]. An AS5600 magnetic encoder reads a magnet glued to the motor shaft
[5][7]. With only that motor-side encoder, joint zeros must be calibrated after every power cycle by moving
each joint to its mechanical limits [13]. The mini PC reaches the four CAN buses through USB-CAN adapters;
power runs through a circuit breaker, voltage and current monitors, and 24-to-12 V and 12-to-5 V
regulators [5]. The docs warn that the design includes high-power electronics [4].

### Software and control

The workspace repo is organised as Isaac Lab extensions: tasks (velocity tracking for the biped and full
humanoid, PPO through rsl_rl), assets, and low-level code [1]. Its current dependencies pin Isaac Sim 5.1.0
and Isaac Lab 2.3.2 [1]; the paper describes its walking policy as trained in Isaac Gym [2]. Policies run as
ONNX, and six trained checkpoints ship in the repo [1]. On the robot, a C controller is recommended for
locomotion for its real-time behaviour, with a Python path for experiments; gamepad buttons switch between
idle, RL and damping modes [10][13]. Teleoperation uses SteamVR base stations and controllers, with
inverse kinematics from Pink and Pinocchio [2]. The docs also cover a LeRobot integration and motion capture [4].

### Simulation

URDF, MJCF and USD models of the full humanoid and the biped are in the assets repo, exported from
Onshape with onshape-to-robot [12]. The main repo has a MuJoCo sim-to-sim player for checking policies
before hardware [1][4].

## What it is used for

- **Learning-based locomotion:** zero-shot sim-to-real walking; the demo used only about 30% of the
  actuator torque limit [2].
- **Teleoperated manipulation:** demos include a Rubik's Cube, writing with a marker and playing with blocks [3].
- **Teaching:** the 6512 actuator is used in UC Berkeley's MECENG 102B class to show how a cycloidal drive works [2].
- **Custom robots:** each actuator needs only power and CAN, so the paper shows the same modules as a
  quadruped, a biped, a centaur-like robot and a mobile base [2].

## Cost and BOM

The BOM sheet has three tabs: the 6512 actuator, the 5010 actuator and the humanoid. It lists US
(Amazon) and China (Taobao, Tmall) prices side by side [5][20].

- **Full humanoid (type `bom`):** USD 4,350.59 from the US column, or CNY 23,244.19 from the China column [5].
  The paper's rounded table gives USD 4,312 and USD 3,236 for China [2].
- **Per actuator:** 6512 at USD 188.69 (the motor alone is USD 129); 5010 at USD 136.36 (motor USD 84) [5].
- **By section (our sums of the sheet rows):** base electronics and frame USD 538.19, legs USD 2,172.17,
  arms with grippers USD 1,640.23. A legs-only biped is about USD 2,710, still counting four USB-CAN adapters [5].
- **Filament:** PLA; the docs suggest Bambu Lab PLA Basic or Hatchbox [20].
- No official kit or assembled robot is sold.

## Building it

**Difficulty 4:** 22 custom actuators to print, assemble, flash and calibrate, glued encoder magnets,
CAN wiring and a high-power LiPo system. The paper puts assembly at about three days once parts are in,
with printing done within a week; the project gives no hour counts [2].

- **Printer:** at least 200 × 200 × 200 mm; profiles are tuned for a Bambu Lab X1C, and an Ender-3 V3 SE
  was also tested [7][8]. The upper and lower body plates are printed twice, one mirrored [8].
- **Tools:** soldering iron, heat-insert stand, hot glue gun, hex keys from M2 to M6 [7].
- **Firmware:** each board is flashed four times with different flags; a reversed motor is fixed by swapping
  two phases or a firmware setting [9].
- **Pitfalls from the issues:** confusion over actuator and motor variants, motor availability, gluing
  the magnet, mirrored plates, extrusion names that do not match the CAD, missing print parts (fixed in
  later releases), and PyTorch builds for new GPUs [15][6].
- The submodules use SSH URLs, so a recursive clone needs a GitHub SSH key [1].
- The paper flags heat in long runs as unstudied for the printed parts [2].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Robot and actuator CAD, USB-CAN case | Onshape | [Releases page](https://berkeley-humanoid-lite.gitbook.io/docs/releases) | CC-BY-SA-4.0 (README: assets other than code) |
| Print files | 3MF on MakerWorld | Releases page | CC-BY-SA-4.0 per the README |
| BOM | Google Sheet, USD and CNY | [BOM sheet](https://docs.google.com/spreadsheets/d/1AQEHcH_nPkXYfor2-h7bwNIUMmsePtAm53epnsWgZXc/edit?usp=sharing) | None stated |
| Motor controller firmware | C, STM32CubeIDE project | [Recoil-Motor-Controller-BESC](https://github.com/T-K-233/Recoil-Motor-Controller-BESC) | MIT |
| Motor controller board | ST B-G431B-ESC1 (bought, not open) | — | — |
| Low-level control | C and Python | [Lowlevel repo](https://github.com/HybridRobotics/Berkeley-Humanoid-Lite-Lowlevel) | MIT (package metadata) |
| Training and sim-to-sim | Python, Isaac Lab, MuJoCo | [main repo](https://github.com/HybridRobotics/berkeley-humanoid-lite) | MIT |
| Robot models | URDF, MJCF, USD | [Assets repo](https://github.com/HybridRobotics/Berkeley-Humanoid-Lite-Assets) | CC-BY-SA-4.0 |
| Trained policies | ONNX | `checkpoints/` in the main repo | Not stated separately |
| Docs | GitBook | [docs](https://berkeley-humanoid-lite.gitbook.io/docs) | None stated |

CC-BY-SA-4.0 is share-alike: a modified design must be published under the same licence, with credit.

## Strengths and limits

**Strengths**
- A complete research humanoid for about USD 4,350 in parts, sold in both the US and China [2][5].
- The actuator is a module: build one for USD 136–189 and test it alone [5].
- Complete chain: CAD, BOM, firmware, models, training, sim-to-sim, deployment and teleoperation [1][4].

**Limits**
- Printed PLA gearboxes are less stiff than reinforced ones, and long-run heat effects are unstudied [2].
- About 30 minutes per battery [2].
- Joint zeros need recalibration after every power-up [13].
- Heavy software stack: Isaac Sim and Isaac Lab need an Nvidia GPU, and version pins break on new cards [1][15].
- No published walking speed or payload.

## What to reuse

- A printed cycloidal reducer on a drone motor with a cheap FOC board and magnetic encoder [5][9].
- Two actuator sizes sharing one design, so parts and firmware are common [2][5].
- One CAN bus per limb to keep each bus short and fast [2].
- A legs-only build as a cheaper first stage of a humanoid [2][12].
- A MuJoCo sim-to-sim check of every policy before it runs on hardware [1].

## Related robots

- **Berkeley Humanoid (2024)**, the lab's earlier, closed robot: a mid-scale research humanoid built in-house
  for learning-based control [16][17]. We found no release of its hardware design. Its Isaac Lab training code, a
  URDF (BSD-3-Clause) and a 12-joint MuJoCo Menagerie model (BSD-3-Clause) are public [17][19][18].
  Lite is the open successor from the same lab.
- [ToddlerBot](toddlerbot.md): low-cost printed humanoid for ML research.
- [Microban](microban.md): 30 cm printable Dynamixel humanoid.
- [Open Duck Mini](open-duck-mini.md): much smaller printed biped with RL walking.
- [Upkie](upkie.md): wheeled biped on bought quasi-direct-drive actuators.

## Sources

1. [berkeley-humanoid-lite repository README](https://github.com/HybridRobotics/berkeley-humanoid-lite), accessed 2026-11-17
2. [Chi et al., Demonstrating Berkeley Humanoid Lite (RSS 2025)](https://arxiv.org/abs/2504.17249), accessed 2026-11-17
3. [Berkeley Humanoid Lite project site](https://lite.berkeley-humanoid.org/), accessed 2026-11-17
4. [Berkeley Humanoid Lite documentation](https://berkeley-humanoid-lite.gitbook.io/docs), accessed 2026-11-17
5. [Berkeley Humanoid Lite bill of materials (Google Sheet)](https://docs.google.com/spreadsheets/d/1AQEHcH_nPkXYfor2-h7bwNIUMmsePtAm53epnsWgZXc/edit?usp=sharing), accessed 2026-11-17
6. [Berkeley Humanoid Lite docs, Releases](https://berkeley-humanoid-lite.gitbook.io/docs/releases), accessed 2026-11-17
7. [Berkeley Humanoid Lite docs, Preparing the tools](https://berkeley-humanoid-lite.gitbook.io/docs/getting-started-with-hardware/preparing-the-tools), accessed 2026-11-17
8. [Berkeley Humanoid Lite docs, 3D printing instructions](https://berkeley-humanoid-lite.gitbook.io/docs/getting-started-with-hardware/3d-printing-instructions), accessed 2026-11-17
9. [Berkeley Humanoid Lite docs, Flashing the motor controllers](https://berkeley-humanoid-lite.gitbook.io/docs/getting-started-with-hardware/flashing-the-motor-controllers), accessed 2026-11-17
10. [Berkeley Humanoid Lite docs, The on-board computer](https://berkeley-humanoid-lite.gitbook.io/docs/getting-started-with-software/the-on-board-computer), accessed 2026-11-17
11. [Berkeley Humanoid Lite docs, Joint ID mapping](https://berkeley-humanoid-lite.gitbook.io/docs/in-depth-contents/joint-id-mapping), accessed 2026-11-17
12. [Berkeley-Humanoid-Lite-Assets repository](https://github.com/HybridRobotics/Berkeley-Humanoid-Lite-Assets), accessed 2026-11-17
13. [Berkeley-Humanoid-Lite-Lowlevel repository](https://github.com/HybridRobotics/Berkeley-Humanoid-Lite-Lowlevel), accessed 2026-11-17
14. [Recoil Motor Controller BESC firmware repository](https://github.com/T-K-233/Recoil-Motor-Controller-BESC), accessed 2026-11-17
15. [berkeley-humanoid-lite issue tracker](https://github.com/HybridRobotics/berkeley-humanoid-lite/issues), accessed 2026-11-17
16. [Liao et al., Berkeley Humanoid, A Research Platform for Learning-based Control](https://arxiv.org/abs/2407.21781), accessed 2026-11-17
17. [Berkeley Humanoid project site](https://berkeley-humanoid.com/), accessed 2026-11-17
18. [MuJoCo Menagerie README](https://github.com/google-deepmind/mujoco_menagerie), accessed 2026-11-17
19. [robot_descriptions.py README](https://github.com/robot-descriptions/robot_descriptions.py), accessed 2026-11-17
20. [Berkeley Humanoid Lite docs, Materials and parts (BOM)](https://berkeley-humanoid-lite.gitbook.io/docs/getting-started-with-hardware/materials-and-parts-bom), accessed 2026-11-17
