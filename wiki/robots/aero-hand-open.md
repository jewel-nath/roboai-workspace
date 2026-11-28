---
type: robot
name: Aero Hand Open
summary: Printable five-finger tendon-driven hand, 7 servos for 16 joints, about $316 in parts, with a MuJoCo model tuned for sim-to-real RL; design files are non-commercial (CC BY-NC-SA).
tags: [dexterous-hand, tendon-driven, feetech, esp32, 3d-printed, mujoco, sim-to-real, non-commercial]
category: gripper
tier: A
openness: full
maker: Chestnut Robotics (formerly TetherIA)
year: 2025
license: {hardware: CC-BY-NC-SA-4.0, software: Apache-2.0, docs: CC-BY-NC-SA-4.0}
links: {repo: "https://github.com/Chestnut-Robotics/aero-hand-open", docs: "https://docs.tetheria.ai/", cad: "https://cad.onshape.com/documents/afc7e0ca7eb6d412ec8771f8/w/bc4d7e45e17e23d622d2bad2/e/c711982b7882da925263fb55", paper: "https://arxiv.org/abs/2608.28578", site: "https://chestnut.bot"}
specs: {dof: 7, payload_kg: , reach_mm: , mass_kg: 0.374, size_mm: "198 x 95 x 53.5", speed_mps: , runtime_h: }
stack: {actuators: "7 x Feetech HLS3606M serial-bus servos pulling Kevlar/Vectran tendons", mcu: [espressif-esp32-s3, "Seeed XIAO ESP32-S3 on a custom KiCad carrier board"], compute: "host PC over USB-C", sensors: ["servo encoders (7)"], sim_models: ["MJCF (MuJoCo Menagerie, tetheria_aero_hand_open)", "MJCF (chestnut-robotics/aero-open-sim)", "MJCF (MuJoCo Playground, aero_hand environments)", "URDF (repo, ros2/src/aero_hand_open_description)"], ros2: official}
cost: {type: bom, usd: 316.48, as_of: 2026-11-17, source: "https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/hardware/Assembly/BOM.csv"}
build: {difficulty: 3, hours: , print_hours: 13}
maturity: {last_commit: 2026-09-15, stars: 1107, active: true}
use_cases: [research, reinforcement-learning, teleop, manipulation, education]
evidence: researched
last_verified: 2026-11-17
sources:
  - {url: "https://github.com/Chestnut-Robotics/aero-hand-open", title: Aero Hand Open repository README, accessed: 2026-11-17}
  - {url: "https://arxiv.org/abs/2608.28578", title: "Aero Hand Open: A Simulation-Ready Tendon-Driven Hand for Dexterous Manipulation Learning", accessed: 2026-11-17}
  - {url: "https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/hardware/Assembly/BOM.csv", title: Aero Hand Open bill of materials, accessed: 2026-11-17}
  - {url: "https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/hardware/Assembly/Tools.csv", title: Aero Hand Open tool list, accessed: 2026-11-17}
  - {url: "https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/LICENSE.md", title: Aero Hand Open licensing guide, accessed: 2026-11-17}
  - {url: "https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/RELEASE_NOTES.md", title: Aero Hand Open release notes, accessed: 2026-11-17}
  - {url: "https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/firmware/README.md", title: Aero Hand Open firmware README, accessed: 2026-11-17}
  - {url: "https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/ros2/README.md", title: Aero Hand Open ROS 2 README, accessed: 2026-11-17}
  - {url: "https://docs.tetheria.ai/docs/intro", title: Aero Hand Open documentation, introduction, accessed: 2026-11-17}
  - {url: "https://docs.tetheria.ai/docs/hardware_setup", title: Aero Hand Open documentation, hardware setup, accessed: 2026-11-17}
  - {url: "https://chestnut-robotics.github.io/aero-hand-open/", title: Aero Hand Open project page, accessed: 2026-11-17}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie", title: MuJoCo Menagerie model list, accessed: 2026-11-17}
  - {url: "https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/sim_rl/README.md", title: Aero Hand Open simulation and RL README, accessed: 2026-11-17}
  - {url: "https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/hardware/PCB/Aero_hand_open_right/Aero-Hand-Open-Right-BOM.csv", title: Aero Hand Open carrier board BOM (right hand), accessed: 2026-11-17}
  - {url: "https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/hardware/CAD/mount_adapters/readme.md", title: Aero Hand Open mount adapters, accessed: 2026-11-17}
  - {url: "https://shop.tetheria.ai/", title: Chestnut Robotics shop, accessed: 2026-11-17}
  - {url: "https://chestnut.bot", title: Chestnut Robotics website, accessed: 2026-11-17}
  - {url: "https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/ros2/src/manus_glove_pkg/README.md", title: Manus ROS 2 package README (in the Aero Hand repo), accessed: 2026-11-17}
---

# Aero Hand Open

A 3D-printed, five-finger robot hand in which seven servos pull tendons to move sixteen joints
[1][2]. TetherIA built it; the company renamed itself Chestnut Robotics in 2026 [5]. It is one of
the cheapest humanlike hands with full CAD, PCB, firmware, ROS 2 and a MuJoCo model tuned against
the real hand, but its design files are licensed for non-commercial use only [2][5].

## Specs

| Item | Value | Source |
|---|---|---|
| Degrees of freedom | 7 actuated: one per finger and three for the thumb; 16 joints, 9 of them passive | [2][9] |
| Size | 198 x 95 x 53.5 mm | [2] |
| Mass | 374 g in the paper; the README says 389 g, the project page under 400 g | [2][1][11] |
| Actuators | 7 x Feetech HLS3606M serial-bus servos, magnetic encoders, about 0.59 N·m stall each | [2] |
| Fingertip force | about 12 N per finger and thumb, measured at the tip; the project page says 10 N | [2][11] |
| Speed | full open-close cycle at about 1.2 Hz; 10 to 90% rise time 120 ms per finger | [2] |
| Endurance | over 400,000 full cycles (90 h) without cable failure; the project page claims 1 million | [2][11] |
| Tendons | braided Kevlar or Vectran, rated 69 kg, wound on 9.0 mm spools | [2] |
| Power | 6 V servo rail, up to 10 A; the paper says 24 V input instead | [7][9][10][2] |
| Host link | USB-C, fixed 16-byte binary serial protocol | [7] |
| Mounting | flat wrist face with four M3 threaded inserts | [2] |
| Payload | not specified; the maker shows a demo lifting a water jug of about 18 kg (maker's claim) | [11] |

The sources disagree on mass, force, endurance and supply voltage. The table gives the paper's
measured values first; the 6 V figure comes from the firmware README and the docs, and matches the
6 V servo in the BOM [3][7][9].

## How it works

### Mechanics and actuation

Each of the four fingers is a separate module with three flexion joints. One flexor cable closes
the whole finger; a coupling cable ties the two outer joints, and music-wire springs open it again
[2][3]. The base joint's spring is softer, so the finger closes from the base outwards [2]. The
thumb has four joints and three motors: a short linkage turns it across the palm, and two cables
flex it [2]. Each servo winds its cable on a printed spool [2][3]. The 23 small bearings and
steel pins form the hinges, and cast silicone pads give grip [3].

### Electronics and firmware

A Seeed XIAO ESP32-S3 sits on a small KiCad carrier board with seven servo connectors, an XT30
power input and buffer chips for the half-duplex servo bus [7][14]. Separate left-hand and
right-hand builds exist [7]. The Arduino firmware homes the hand on start-up and takes position,
velocity and torque commands; torque control works only in the closing direction [6][7][9]. Its
overheat protection has been set at 70 °C since v0.1.4 [6]. Prebuilt binaries can be flashed from the SDK's GUI [7].

### Software and control

The Apache-2.0 Python SDK (`aero-open-sdk` on PyPI) handles homing, calibration, joint and torque
control [1]. ROS 2 Humble packages add a hand node, URDF, retargeting and teleoperation from a
webcam, an Apple Vision Pro or Manus gloves [6][8]. The Manus package is Manus's own, copied in
for convenience with a prebuilt SDK library; check Manus's terms before redistributing it [18]. Firmware 0.2.0 changed thumb homing and broke backward compatibility [6].

### Simulation

The MuJoCo model has 16 hinge joints, 20 spatial tendons and 7 actuators, with an identified map
from motor to tendon travel [2]. It lives in its own repository and in MuJoCo Menagerie as
`tetheria_aero_hand_open` (Apache-2.0) [12][13]. MuJoCo Playground has Aero Hand environments for
RL training [6][13]. Finger cable travel matches the hardware within 1.4 mm; the thumb cables are
off by about 31 to 33% [2].

## What it is used for

- **Sim-to-real RL:** the paper trains a cube-rotation policy in MuJoCo Playground with PPO and
  runs it on the real hand with no fine-tuning, at about one turn per 55 s [2].
- **Teleoperation and data collection** with Manus gloves, a webcam or an Apple Vision Pro [8].
- **Arm and humanoid end effector:** printable adapters exist for the AgileX Piper arm, a tripod
  and the Unitree G1 [15].

## Cost and BOM

| Item | Price (USD) | Type | Date | Source |
|---|---|---|---|---|
| One hand from the project BOM | 316.48 | BOM | read 2026-11-17 | [3] |
| Seven HLS3606M servos | 208.81 | BOM | read 2026-11-17 | [3] |
| Headline price: "complete kit" in the README, BOM in the paper | 314 | kit (README), BOM (paper) | read 2026-11-17 | [1][2] |

The servos are two thirds of the cost; the ESP32-S3 board is $7.99 and the rest is springs, cable,
bearings, pins, screws, silicone and PLA [3]. The BOM total leaves out the custom carrier board
(fabricate it from the Gerbers, or hand-wire the optional proto board) [3][10]. On 2026-11-17 the
maker's shop said the Aero Hand Open is no longer sold, while the company site said it remains
available on request; no current price for an assembled hand was found [16][17].

## Building it

**Difficulty 3:** printing plus tendon routing, silicone casting, pressing pins, a custom PCB or
hand-soldered wiring, and flashing firmware.

- **Printing:** PLA on a Bambu X1C, 0.4 mm nozzle, 0.2 mm layers, tree supports on the build plate
  only; keep the given orientations [1]. A full set takes about 13 h; one finger about 45 min [2].
  Any printer with a 200 x 200 mm bed works, but tolerances may change [1][3].
- **Tools:** a floss threader for routing cables, silicone adhesive, a 2.1 mm drill, Torx drivers,
  a soldering iron for heat-set inserts, pliers and a marker for servo numbers [4].
- **Pitfalls:** pins and bearings vary by supplier, so buy undersized pins for a slip fit [3];
  tendons need regular re-tensioning [1]; overloading can deform parts or damage servos [1]; a
  hand-wired board may not deliver peak current to all servos [10]. Assembly time is not stated.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| CAD | STEP, Onshape, 3MF print plates, silicone moulds | [hardware/CAD/](https://github.com/Chestnut-Robotics/aero-hand-open/tree/main/hardware/CAD) | CC-BY-NC-SA-4.0 |
| BOM and tools | CSV | [hardware/Assembly/](https://github.com/Chestnut-Robotics/aero-hand-open/tree/main/hardware/Assembly) | CC-BY-NC-SA-4.0 |
| PCB | KiCad, Gerbers, BOM and placement files | [hardware/PCB/](https://github.com/Chestnut-Robotics/aero-hand-open/tree/main/hardware/PCB) | CC-BY-NC-SA-4.0 |
| Firmware | Arduino C++, prebuilt binaries | [firmware/](https://github.com/Chestnut-Robotics/aero-hand-open/tree/main/firmware) | Apache-2.0 |
| SDK | Python | [sdk/](https://github.com/Chestnut-Robotics/aero-hand-open/tree/main/sdk) | Apache-2.0 |
| ROS 2 | Humble packages, URDF | [ros2/](https://github.com/Chestnut-Robotics/aero-hand-open/tree/main/ros2) | Apache-2.0 |
| Sim model | MJCF | Menagerie, aero-open-sim | Apache-2.0 in Menagerie [12] |
| Docs | web docs, assembly PDF | [docs.tetheria.ai](https://docs.tetheria.ai/) | CC-BY-NC-SA-4.0 |

**Non-commercial hardware.** The design files are CC BY-NC-SA 4.0: you may not sell parts, kits or
hands made from them, or from modified versions, without a paid manufacturing licence [5].
Hands bought from the maker may go into commercial products [5]. GitHub shows no licence
(NOASSERTION) because `LICENSE.md` is a guide; the actual texts sit in each subfolder.

## Strengths and limits

- **Strengths:** light and cheap for a five-finger hand [2]; full CAD, PCB, firmware and SDK; a
  MuJoCo model in Menagerie with measured sim-to-real error [2][12]; three teleoperation inputs
  [8]; modular fingers that come off for repair [1].
- **Limits:** non-commercial design licence [5]; the paper lists only the motor encoders as
  sensors, so there is no touch sensing [2];
  coupled tendons limit independent joint control; thumb model error of about 30% [2]; tendons
  need upkeep [1]; spec figures disagree between sources; buying an assembled hand is unclear
  [16][17].

## What to reuse

- One motor per finger with a coupling cable and graded return springs gives a natural closing
  order without extra motors [2].
- Model tendons as MuJoCo spatial tendons with wrap cylinders taken from the CAD pulley positions,
  then identify the motor-to-tendon map on hardware [2].
- Cast silicone finger pads in printed moulds [3].
- Specify undersized dowel pins so they slip-fit cheap bearings [3].
- A tiny ESP32 carrier with tri-state buffers turns a UART into a half-duplex servo bus [14].

## Related robots

- [SO-101](so-101.md) and [SO-ARM 102](so-arm-102.md) use the same kind of Feetech serial-bus
  servo, but no SO-101 mount for this hand was found.
- Hands the paper compares it with, all named in plain text: InMoov, LEAP Hand, Amazing Hand,
  ORCA, RUKA, Allegro and Shadow [2].

## Sources

1. [Aero Hand Open repository README](https://github.com/Chestnut-Robotics/aero-hand-open), accessed 2026-11-17
2. [Aero Hand Open: A Simulation-Ready Tendon-Driven Hand for Dexterous Manipulation Learning](https://arxiv.org/abs/2608.28578), accessed 2026-11-17
3. [Aero Hand Open bill of materials](https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/hardware/Assembly/BOM.csv), accessed 2026-11-17
4. [Aero Hand Open tool list](https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/hardware/Assembly/Tools.csv), accessed 2026-11-17
5. [Aero Hand Open licensing guide](https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/LICENSE.md), accessed 2026-11-17
6. [Aero Hand Open release notes](https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/RELEASE_NOTES.md), accessed 2026-11-17
7. [Aero Hand Open firmware README](https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/firmware/README.md), accessed 2026-11-17
8. [Aero Hand Open ROS 2 README](https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/ros2/README.md), accessed 2026-11-17
9. [Aero Hand Open documentation, introduction](https://docs.tetheria.ai/docs/intro), accessed 2026-11-17
10. [Aero Hand Open documentation, hardware setup](https://docs.tetheria.ai/docs/hardware_setup), accessed 2026-11-17
11. [Aero Hand Open project page](https://chestnut-robotics.github.io/aero-hand-open/), accessed 2026-11-17
12. [MuJoCo Menagerie model list](https://github.com/google-deepmind/mujoco_menagerie), accessed 2026-11-17
13. [Aero Hand Open simulation and RL README](https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/sim_rl/README.md), accessed 2026-11-17
14. [Aero Hand Open carrier board BOM (right hand)](https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/hardware/PCB/Aero_hand_open_right/Aero-Hand-Open-Right-BOM.csv), accessed 2026-11-17
15. [Aero Hand Open mount adapters](https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/hardware/CAD/mount_adapters/readme.md), accessed 2026-11-17
16. [Chestnut Robotics shop](https://shop.tetheria.ai/), accessed 2026-11-17
17. [Chestnut Robotics website](https://chestnut.bot), accessed 2026-11-17
18. [Manus ROS 2 package README (in the Aero Hand repo)](https://github.com/Chestnut-Robotics/aero-hand-open/blob/main/ros2/src/manus_glove_pkg/README.md), accessed 2026-11-17
