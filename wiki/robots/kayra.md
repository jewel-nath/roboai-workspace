---
type: robot
name: Kayra
summary: Small 3D-printed community humanoid by Ramin Assadollahi, designed in FreeCAD, with 16 hobby servos on a Pimoroni Servo 2040 running MicroPython, a BNO055 IMU and a MuJoCo model of its legs; BSD-3-Clause, with a parts list but no priced BOM.
tags: [3d-printed, freecad, mujoco, hobby-servo, micropython, rp2040, servo-2040, biped, community]
category: humanoid
tier: B
openness: full
maker: Ramin Assadollahi and the Kayra community
year: 2022
license: {hardware: BSD-3-Clause, software: BSD-3-Clause, docs: BSD-3-Clause}
links: {repo: "https://github.com/assadollahi/kayra", docs: "https://github.com/assadollahi/kayra/blob/main/WIRING.md", cad: "https://github.com/assadollahi/kayra/tree/main/FCStd", paper: , site: }
specs: {dof: 16, payload_kg: , reach_mm: , mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "16 hobby servos; the 2023 parts list names DS3235MG (35 kg·cm class) for the main joints and CS-929MG for the small ones", mcu: "Pimoroni Servo 2040 (RP2040) running MicroPython", compute: "host PC over USB serial; optional ESP32-CAM in the head over Wi-Fi", sensors: ["BNO055 IMU", "ESP32-CAM camera (optional)"], sim_models: ["MJCF (kayra repo, mujoco/kayraLowerBody.xml: legs, 8 actuated servos)"], ros2: none}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: 3, hours: 2, print_hours: 20}
maturity: {last_commit: 2026-09-13, stars: 62, active: true}
use_cases: [hobby, education, locomotion]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/assadollahi/kayra", title: Kayra repository README and licence, accessed: 2026-11-18}
  - {url: "https://github.com/assadollahi/kayra/blob/main/WIRING.md", title: Kayra WIRING.md, accessed: 2026-11-18}
  - {url: "https://github.com/assadollahi/kayra/blob/main/software/README.md", title: Kayra software README and servoMap.json, accessed: 2026-11-18}
  - {url: "https://github.com/assadollahi/kayra/tree/main/mujoco", title: Kayra MuJoCo folder and readme, accessed: 2026-11-18}
  - {url: "https://web.archive.org/web/20231204203915/https://kayra.org/what-to-buy/", title: "kayra.org: Materials (archived 2023-12-04)", accessed: 2026-11-18}
  - {url: "https://web.archive.org/web/20231204201903/https://kayra.org/design-goals/", title: "kayra.org: Design Goals (archived 2023-12-04)", accessed: 2026-11-18}
  - {url: "https://web.archive.org/web/20240304192625/https://kayra.org/roadmap-4th-jan-2024/", title: "kayra.org: Roadmap 4th Jan 2024 (archived)", accessed: 2026-11-18}
---

# Kayra

A small 3D-printed humanoid that Ramin Assadollahi started in 2022 and hopes the community will
evolve [1][6]. It is designed in FreeCAD, runs on hobby servos and a MicroPython servo board, and has
a MuJoCo model of its legs [1][4]. The repo is active (last commit September 2026) [1], but the
documentation site kayra.org no longer resolves, so its guides survive only in web archives [5][6].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | the current design in the repo (September 2026) | [1] |
| Degrees of freedom | 16 of the board's 18 servo channels in use: per leg ankle, knee, hip pitch, hip yaw; per arm shoulder rotation, shoulder brace, elbow; pelvis rotation; head pitch | [2][3] |
| Servos | metal-gear, about 35 kg·cm at up to 7.4 V (DS3235MG); CS-929MG for small joints (2023 list) | [5] |
| Controller | Pimoroni Servo 2040 (RP2040), MicroPython; USB-C to the host at 115200 baud | [2][3] |
| IMU | BNO055 on I2C at 400 kHz | [2] |
| Power | separate servo and 5 V logic rails from BECs; a 10 A UBEC suggested; 2 x 18650 cells in the 2023 list | [2][5] |
| Print and assembly time | 20 h to print, 2 h to assemble (2023 design goals) | [6] |
| Height, mass, speed | not published | — |

## How it works

Each leg has four servos, and many leg segments are closed loops of four parts (knee, shin, calf
and foot joint), which the MuJoCo model has to close as well [2][4]. Each arm has three servos, plus
one for pelvis rotation and one for head pitch [2]. Parts come as FreeCAD files and STLs [1].

The Servo 2040 runs a MicroPython program that stores poses and animations in flash; tethered, it
takes commands over USB serial, and untethered it plays a stored animation at a button press [3]. A
Python pose and animation editor on the PC sends servo values and reads back the IMU [3].
`servoMap.json` names every channel, its limits and its MuJoCo actuator; the arm and pelvis entries
and all limits are still marked unverified [2][3]. An optional ESP32-CAM in the head can stream
video to the host over Wi-Fi [5][7]. In MuJoCo, `kayraLowerBody.xml` models the legs with the 8 leg
servos as actuators; the other files are smaller experiments [3][4]. The January 2024 roadmap names
inverse kinematics, simulation and reinforcement learning as next steps [7]. There is no URDF or
ROS package.

## What it is used for

- A low-cost hobby and school humanoid; the design goals ask for under €500 for a minimal system [6].
- Walking with scripted poses and animations, edited on the PC [3].
- Learning MuJoCo modelling of closed-loop legs, with a tutorial that was on kayra.org [4].

## Cost and BOM

No priced BOM: the 2023 parts list names the parts without prices [5] and the repo has no BOM file
[1]. The goal of under €500 is a target, not a price [6], so `cost` stays empty.

## Building it

**Difficulty 3:** print the parts, wire two BECs, mind the cut trace and 5 V solder pads on the
Servo 2040, copy the MicroPython files with Thonny and check servo limits by hand [1][2][3]. The 2023
design goals give 20 h of printing and 2 h of assembly [6]. The README points to PETG G-code for a
Prusa i3 MK3, but that folder is not in the repo [1].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| CAD | FreeCAD (FCStd) | [FCStd/](https://github.com/assadollahi/kayra/tree/main/FCStd) [1] | BSD-3-Clause |
| Print files | STL | [STL/](https://github.com/assadollahi/kayra/tree/main/STL) [1] | BSD-3-Clause |
| Firmware and host software | MicroPython, Python | [software/](https://github.com/assadollahi/kayra/tree/main/software) [3] | BSD-3-Clause |
| Simulation | MJCF | [mujoco/](https://github.com/assadollahi/kayra/tree/main/mujoco) [4] | BSD-3-Clause |
| Wiring guide | Markdown | [WIRING.md](https://github.com/assadollahi/kayra/blob/main/WIRING.md) [2] | BSD-3-Clause |

## Strengths and limits

- **Strengths:** everything in one permissive repo, with CAD in an open CAD tool [1]; cheap hobby
  servos and one off-the-shelf servo board [2][5]; a MuJoCo model and a clear servo map [3][4].
- **Limits:** no priced BOM, height or mass [1][5]; servo limits and some joint assignments are
  unverified [2]; only the legs are simulated [4]; the docs site is gone [5]; no ROS support.

## What to reuse

- One JSON servo map shared by firmware, host tools and simulation [3].
- Separate servo and logic power rails, so USB power never meets the servo supply [2].

## Related robots

- [Open Duck Mini](open-duck-mini.md) and [ToddlerBot](toddlerbot.md): small printed bipeds with sim models.
- [InMoov](inmoov.md) and [Poppy Humanoid](poppy-humanoid.md): other open printed humanoids.

## Sources

1. [Kayra repository README and licence](https://github.com/assadollahi/kayra), accessed 2026-11-18
2. [Kayra WIRING.md](https://github.com/assadollahi/kayra/blob/main/WIRING.md), accessed 2026-11-18
3. [Kayra software README and servoMap.json](https://github.com/assadollahi/kayra/blob/main/software/README.md), accessed 2026-11-18
4. [Kayra MuJoCo folder and readme](https://github.com/assadollahi/kayra/tree/main/mujoco), accessed 2026-11-18
5. [kayra.org: Materials (archived 2023-12-04)](https://web.archive.org/web/20231204203915/https://kayra.org/what-to-buy/), accessed 2026-11-18
6. [kayra.org: Design Goals (archived 2023-12-04)](https://web.archive.org/web/20231204201903/https://kayra.org/design-goals/), accessed 2026-11-18
7. [kayra.org: Roadmap 4th Jan 2024 (archived)](https://web.archive.org/web/20240304192625/https://kayra.org/roadmap-4th-jan-2024/), accessed 2026-11-18
