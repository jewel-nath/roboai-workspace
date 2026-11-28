---
type: robot
name: Sesame
summary: A palm-sized ESP32 quadruped with eight MG90S servos and an OLED face, printed in PLA and built for about USD 50 to 60 in parts, a popular first walking robot.
tags: [quadruped, esp32, mg90s, hobby-servo, oled-face, 3d-printed, arduino, wifi, beginner]
category: legged
tier: A
openness: full
maker: Dorian Todd
year: 2026
license: {hardware: Apache-2.0, software: Apache-2.0, docs: Apache-2.0}
links: {repo: https://github.com/dorianborian/sesame-robot, docs: https://github.com/dorianborian/sesame-robot/tree/main/docs, cad: https://github.com/dorianborian/sesame-robot/tree/main/hardware/cad, paper: , site: https://www.doriantodd.com/sesame}
specs: {dof: 8, payload_kg: , reach_mm: , mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "8x MG90S 180-degree metal-gear micro servos (PWM)", mcu: [espressif-esp32-s3, "ESP32-S2 (Lolin S2 Mini) or ESP32-S3 (Sesame Distro Board V3.1)"], compute: , sensors: [], sim_models: ["URDF (Sesame Simulator, one-for-all)", "MJCF (lukehollis/sesame-ml)", "URDF (lukehollis/sesame-ml)"], ros2: none}
cost: {type: bom, usd: 60, as_of: 2026-11-17, source: https://github.com/dorianborian/sesame-robot}
build: {difficulty: 3, hours: , print_hours: }
maturity: {last_commit: 2026-11-08, stars: 5086, active: true}
use_cases: [hobby, education, companion]
evidence: researched
last_verified: 2026-11-17
sources:
  - {url: https://github.com/dorianborian/sesame-robot, title: Sesame Robot Project repository README, accessed: 2026-11-17}
  - {url: https://github.com/dorianborian/sesame-robot/blob/main/hardware/bom/README.md, title: Sesame bill of materials, accessed: 2026-11-17}
  - {url: https://github.com/dorianborian/sesame-robot/blob/main/docs/build-guide/README.md, title: Sesame build guide, accessed: 2026-11-17}
  - {url: https://github.com/dorianborian/sesame-robot/blob/main/docs/wiring-guide/README.md, title: Sesame wiring guide, accessed: 2026-11-17}
  - {url: https://github.com/dorianborian/sesame-robot/blob/main/hardware/pcb/README.md, title: Sesame Distro Board (PCB) README, accessed: 2026-11-17}
  - {url: https://github.com/dorianborian/sesame-robot/blob/main/hardware/printing/README.md, title: Sesame 3D printing guide, accessed: 2026-11-17}
  - {url: https://github.com/dorianborian/sesame-robot/blob/main/hardware/cad/README.md, title: Sesame CAD files README, accessed: 2026-11-17}
  - {url: https://github.com/dorianborian/sesame-robot/blob/main/firmware/README.md, title: Sesame firmware README, accessed: 2026-11-17}
  - {url: https://www.doriantodd.com/sesame, title: Sesame project page on doriantodd.com, accessed: 2026-11-17}
  - {url: https://www.doriantodd.com/sesame/kit, title: Sesame build kit page, accessed: 2026-11-17}
  - {url: https://hackaday.com/2026/01/24/building-a-little-quadruped-robot, title: "Hackaday, Building A Little Quadruped Robot (2026-01-24)", accessed: 2026-11-17}
  - {url: https://circuitdigest.com/news/sesame-robot-open-source-quadruped-for-every-maker, title: "Circuit Digest, Sesame Robot open-source quadruped (2026-01-19)", accessed: 2026-11-17}
  - {url: https://github.com/dorianborian/sesame-studio, title: Sesame Studio repository, accessed: 2026-11-17}
  - {url: https://one-for-all.github.io/sesame-robot-sim/, title: Sesame Simulator, accessed: 2026-11-17}
  - {url: https://github.com/lukehollis/sesame-ml, title: Sesame ML tools repository, accessed: 2026-11-17}
  - {url: https://github.com/dorianborian/sesame-robot/issues, title: Sesame GitHub issues, accessed: 2026-11-17}
---

# Sesame

Sesame is a small 3D-printed quadruped: eight hobby servos, an ESP32 and a 128x64 OLED face, driven
from a phone over Wi-Fi. Dorian Todd designed it as a first walking robot [1, 9]. A builder gets a
cheap, well-documented, Apache-licensed platform for gaits, expressive faces and voice-assistant toys [1, 8].

## Specs

| Item | Value | Source |
|---|---|---|
| Degrees of freedom | 8: two servos per leg, one hip and one leg joint | 1, 3 |
| Actuators | 8x MG90S metal-gear micro servos, 180-degree type (not continuous rotation) | 2 |
| Controller | Lolin ESP32-S2 Mini (hand-wired), or Sesame Distro Board V3.1 with an ESP32-S3 | 1, 5 |
| Display | 0.96 in SSD1306 I2C OLED, 128x64 | 2 |
| Sensors | None in the stock build | 2 |
| Power | Needs 5 V at 3 A on the servo rail; USB-C PD when tethered, or a battery through a 5 V buck converter. The recommended pack is a Bambu Lab 14500 7.4 V 800 mAh Li-ion | 2 |
| Printed parts | 11 (internal frame, top and bottom covers, eight leg joints) | 3, 6 |
| Mass, size, speed, runtime | Not published | — |
| Cost | USD 50 to 60 in parts (maker's claim; the BOM has no prices) | 1 |

## How it works

### Mechanics and actuation

Four servos sit in the printed internal frame and turn the hip joints. Each of the other four is
screwed inside a leg shell and moves that leg [3]. The legs are separate printed parts, R1 to R4 and
L1 to L4. Top and bottom covers screw on to close the body, and the top cover holds the OLED and
the power switch [3, 6]. Three top-cover styles exist, plus magnetic hats [6]. The servos are plain
PWM hobby servos with no position feedback, so all motion is open-loop keyframes [2, 8].

### Electronics and firmware

There are three wiring paths [4, 5]:

- **Lolin S2 Mini, hand-wired:** a protoboard with eight 3-pin headers, a 5 V and a ground rail,
  and a buck converter for battery use. This is the cheapest path and the one the maker recommends for DIY.
- **Sesame Distro Board V3.1:** an all-SMD board with an ESP32-S3, USB-C PD input and a connector for
  the Bambu Lab battery. You order it assembled from PCBway, or buy it ready-made in small batches.
- **Legacy boards:** V2 browns out on battery, so use it on USB only. V1 stacks on an
  ESP32-DevKitC-32E and cannot run on USB power.

The firmware is one Arduino sketch plus headers for faces, movement sequences and the web page [8].
It drives the servos at 50 Hz with hardware PWM timers, mapping 0 to 180 degrees to 732 to 2929 µs.
It staggers servo pulses (20 ms default) to avoid brownouts [8]. The OLED runs on I2C at 400 kHz,
with bitmap faces stored in flash and idle blinking when nothing happens [8].

### Software and control

The ESP32 opens its own access point with a captive-portal web remote. It can also join a home
network, reachable as `sesame-robot.local` [8]. A JSON API (`/api/status`, `/api/command`) sets
faces and triggers moves from Python, JavaScript or a voice assistant; a serial command line does the
same [1, 8]. Built-in moves include walking, waving, dancing, pointing and resting [1].

Three companion tools sit in their own repos [1]:

- **Sesame Studio:** a PySide6 desktop app that poses a 3D model built from the real STLs, sequences
  frames, paints OLED faces and exports C++ for the firmware [13].
- **Sesame Companion App:** Python voice control and expression sync over the JSON API.
- **Sesame ML (Luke Hollis):** MuJoCo tasks and policy evaluation [15].

### Simulation

Sesame ML provides an MJCF model derived from the CAD and a validated URDF, at
`src/sesame_ml/assets/` [15]. It defines stand, recovery, commanded-locomotion and navigation tasks,
with optional MJX/Brax PPO training. It warns that it ships no policy known to be safe on a real
robot [15]. Jay Li's Sesame Simulator is a separate browser-based simulator built on a URDF model [1, 14].

## What it is used for

- A first robot for learning servo gaits, soldering, ESP32 firmware and web control [1, 9].
- A desk companion: the face library includes talking variants for voice-assistant projects, and the
  companion app links it to speech [1].
- A remix base: the maker invites forks with new hardware, faces and sensors (gyro, ultrasonic) [1].
- Press coverage: Hackaday and Circuit Digest wrote about it in January 2026. Hackaday noted the
  simple mechanics and limited range of motion [11, 12].

## Cost and BOM

The BOM lists parts and links to Amazon searches but gives no prices. The USD 50 to 60 figure is the
maker's estimate from the README, not a summed BOM (type `bom`, as of 2026-11-17) [1, 2].

| Item | Qty | Note | Source |
|---|---|---|---|
| MG90S 180-degree metal-gear servos | 8 (10 suggested) | Must be the 180-degree type | 2 |
| ESP32 board: Lolin S2 Mini, or a Distro Board | 1 | The V3.1 board is ordered assembled from PCBway or bought ready-made | 2, 5 |
| SSD1306 0.96 in OLED | 1 | | 2 |
| Buck converter 5 V 3 A, rocker switch, wire, heat shrink, zip ties | — | The buck converter is only needed on battery with the S2 Mini | 2 |
| Bambu Lab 14500 7.4 V 800 mAh battery and charger | 1 | Optional, for untethered use | 2 |
| M2 x 5 self-tapping and M2.5 x 5 machine screws | ~40 and 10 | | 2 |
| PLA | 11 parts | | 6 |

**Kits:** pre-flashed Sesame Build Kits sell through Full Contact Engineering in production rounds.
On 2026-11-17 round 2 was sold out and no kit price was shown [9, 10]. Ready-made V3 boards are
listed at the same shop when in stock [5].

## Building it

**Difficulty 3:** printing plus soldering (a hand-wired harness or battery leads), flashing an ESP32
with Arduino IDE and calibrating servo zero positions. Kit boards come pre-flashed, which removes
the flashing step [3].

- **Printing:** PLA or PLA+, 8 to 10 % infill, two walls, honeycomb infill. Only the top cover needs
  supports, placed by hand [6]. No print time is given.
- **Time:** the build guide splits the work into five phases of one or two sessions each; it gives no hours [3].
- **Tools:** soldering iron with leaded solder and flux, flush cutters, a precision screwdriver and
  heat shrink [2]. The DIY harness uses 30 AWG wire for signals and 22 AWG for power [4].
- **Calibration:** run the motor-test firmware with the joints off. Set each servo to its pose, then
  press the joints on at the angles the guide shows [3].
- **Pitfalls the docs and issues name:**
  - Buy 180-degree MG90S servos. The BOM's Amazon search also returns continuous-rotation units
    that look the same (issue 79) [2, 16].
  - Pin ESP32Servo to v3.0.9; newer releases let one servo command leak to others [8].
  - Erratic or reversed motion almost always means a servo is in the wrong header [3].
  - On battery, the robot may crash when it moves. Raise the motor current delay or use a LiPo [3].
  - Original V3 boards had PD-chip interference on USB data and a reversed battery connector,
    fixed in V3.1; the README explains a manual fix [5].
  - Open issues report that V3 vias exceed JLCPCB's free limits, that PCBway ordering was disabled,
    and that femur walls are too thin for resin printing [16].
  - The access point ships with a default password, `12345678`. Change it in the code before using
    the robot on a shared network [8].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Mechanical CAD | STEP and Fusion 360 archive (`.f3z`); the README suggests FreeCAD or Onshape for STEP edits | `hardware/cad/` | Apache-2.0 [1, 7] |
| Printable parts | STL | `hardware/printing/stl/` | Apache-2.0 [1] |
| Distro Boards V1, V2, V3.1 | EasyEDA JSON (schematic; PCB for V3.1), Gerber, BOM and pick-and-place CSVs | `hardware/pcb/` | Apache-2.0 [1, 5] |
| Firmware | Arduino C++ | `firmware/` | Apache-2.0 [1] |
| Animation tool | Python (PySide6) | `dorianborian/sesame-studio` | See that repo [13] |
| Sim models | MJCF, URDF | `lukehollis/sesame-ml` | Apache-2.0 [15] |
| Docs | Markdown | `docs/`, `hardware/` | Apache-2.0 [1] |

Everything in the main repo is under one permissive Apache-2.0 licence, so commercial use and
selling kits are allowed with attribution [1].

## Strengths and limits

**Strengths**
- Very cheap and simple; a good first legged robot [1, 9].
- Thorough docs: BOM, build, wiring, printing and firmware guides, plus a Discord [1].
- Permissive licence across hardware, firmware and docs [1].
- A networked JSON API makes it easy to drive from other programs or a voice assistant [8].
- Popular and active: 5,086 GitHub stars and commits in November 2026.

**Limits**
- No sensors: no IMU, no feedback servos, so gaits are open-loop keyframes [2, 8].
- Two DoF per leg and hobby servos give a limited range of motion [11].
- Power is the weak spot: brownouts on battery, a legacy board that only works on USB, and a V3
  board that needed a fix [3, 5].
- No published mass, size, speed or runtime.
- Kits come in batches and sell out [10].

## What to reuse

- **Staggered servo pulses** to keep many hobby servos from collapsing a small 5 V rail [8].
- **Captive-portal web remote plus a JSON API** on one ESP32, for phone control without an app [8].
- **A face library on a cheap OLED**, driven by the same command as movement, to make a simple robot expressive [1, 8].
- **Calibrate with joints off**: hold the servos at a known pose, then press the printed joints on [3].
- **One design, several electronics paths** (hand-wired, custom PCB, legacy) so builders can match their skills and parts [4, 5].

## Related robots

- [Stack-chan](stack-chan.md): another open ESP32 robot built around an expressive face.
- [Open Duck Mini](open-duck-mini.md): a small expressive walker with feedback servos and an RL policy.
- [Microban](microban.md): a step up, a 19-DoF humanoid with serial-bus servos and an IMU.

## Sources

1. [Sesame Robot Project repository README](https://github.com/dorianborian/sesame-robot), accessed 2026-11-17
2. [Sesame bill of materials](https://github.com/dorianborian/sesame-robot/blob/main/hardware/bom/README.md), accessed 2026-11-17
3. [Sesame build guide](https://github.com/dorianborian/sesame-robot/blob/main/docs/build-guide/README.md), accessed 2026-11-17
4. [Sesame wiring guide](https://github.com/dorianborian/sesame-robot/blob/main/docs/wiring-guide/README.md), accessed 2026-11-17
5. [Sesame Distro Board (PCB) README](https://github.com/dorianborian/sesame-robot/blob/main/hardware/pcb/README.md), accessed 2026-11-17
6. [Sesame 3D printing guide](https://github.com/dorianborian/sesame-robot/blob/main/hardware/printing/README.md), accessed 2026-11-17
7. [Sesame CAD files README](https://github.com/dorianborian/sesame-robot/blob/main/hardware/cad/README.md), accessed 2026-11-17
8. [Sesame firmware README](https://github.com/dorianborian/sesame-robot/blob/main/firmware/README.md), accessed 2026-11-17
9. [Sesame project page on doriantodd.com](https://www.doriantodd.com/sesame), accessed 2026-11-17
10. [Sesame build kit page](https://www.doriantodd.com/sesame/kit), accessed 2026-11-17
11. [Hackaday, Building A Little Quadruped Robot (2026-01-24)](https://hackaday.com/2026/01/24/building-a-little-quadruped-robot), accessed 2026-11-17
12. [Circuit Digest, Sesame Robot open-source quadruped (2026-01-19)](https://circuitdigest.com/news/sesame-robot-open-source-quadruped-for-every-maker), accessed 2026-11-17
13. [Sesame Studio repository](https://github.com/dorianborian/sesame-studio), accessed 2026-11-17
14. [Sesame Simulator](https://one-for-all.github.io/sesame-robot-sim/), accessed 2026-11-17
15. [Sesame ML tools repository](https://github.com/lukehollis/sesame-ml), accessed 2026-11-17
16. [Sesame GitHub issues](https://github.com/dorianborian/sesame-robot/issues), accessed 2026-11-17
