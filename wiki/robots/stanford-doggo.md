---
type: robot
name: Stanford Doggo
summary: Eight-joint quasi-direct-drive quadruped from Stanford Student Robotics (ICRA 2019) that jumped 1.14 m, with Fusion 360 CAD, a BOM of about $2,970 and ODrive and Teensy code; its makers ended support in 2024 to build Pupper v3.
tags: [quadruped, quasi-direct-drive, brushless, odrive, teensy, belt-drive, jumping, five-bar-leg, stanford]
category: legged
tier: B
openness: partial
maker: Stanford Student Robotics (Nathan Kau, Aaron Schultz, Natalie Ferrante, Patrick Slade)
year: 2019
license: {hardware: MIT, software: , docs: MIT}
links: {repo: "https://github.com/Nate711/StanfordDoggoProject", docs: "https://github.com/Nate711/StanfordDoggoProject", cad: "https://a360.co/30j7ANn", paper: "https://arxiv.org/abs/1905.04254", site: }
specs: {dof: 8, payload_kg: , reach_mm: , mass_kg: 4.8, size_mm: , speed_mps: 0.9, runtime_h: }
stack: {actuators: "8 T-Motor MN5212 brushless motors with 3:1 GT2 belt reduction, two per leg driving a coaxial five-bar leg", mcu: "Teensy 3.5 main controller; four ODrive v3.5 dual-motor controllers with custom firmware", compute: , sensors: ["AS5047P magnetic encoder per motor (incremental mode)", "BNO080 IMU"], sim_models: [], ros2: none}
cost: {type: bom, usd: 2971.02, as_of: 2026-11-18, source: "https://docs.google.com/spreadsheets/d/1MQRoZCfsMdJhHQ-ht6YvhzNvye6xDXO8vhWQql2HtlI/edit#gid=726381752"}
build: {difficulty: 4, hours: , print_hours: }
maturity: {last_commit: 2024-07-08, stars: 2580, active: false}
use_cases: [research, locomotion, education, hobby]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/Nate711/StanfordDoggoProject", title: StanfordDoggoProject README and licence, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/1905.04254", title: "Stanford Doggo: An Open-Source, Quasi-Direct-Drive Quadruped (ICRA 2019)", accessed: 2026-11-18}
  - {url: "https://docs.google.com/spreadsheets/d/1MQRoZCfsMdJhHQ-ht6YvhzNvye6xDXO8vhWQql2HtlI/edit#gid=726381752", title: Stanford Doggo bill of materials (Google Sheets), accessed: 2026-11-18}
  - {url: "https://github.com/Nate711/Doggo", title: Doggo Teensy code repository, accessed: 2026-11-18}
  - {url: "https://github.com/Nate711/ODrive/tree/PD_CONTROL", title: "Doggo ODrive firmware fork (PD_CONTROL branch)", accessed: 2026-11-18}
---

# Stanford Doggo

A shoebox-sized quadruped from Stanford Student Robotics, presented at ICRA 2019, with a belt-driven
quasi-direct-drive on hobby brushless motors; it then had the highest vertical jumping agility of
any robot, matching the galago [1][2]. CAD, BOM and code are published [1]. It is **no longer
supported**: in 2024 the makers ended it to build [Pupper v3](pupper-v3.md) [1].

## Specs

| Item | Value | Source |
|---|---|---|
| Degrees of freedom | 8: four legs, each a five-bar linkage driven by two coaxial motors | [1][2] |
| Mass, leg length | 4.8 kg; 0.160 m leg | [2] |
| Actuators | T-Motor MN5212 with a 3:1 GT2 belt (16 to 48 teeth); 0.27 kg and $120 per actuator in the paper | [1][2] |
| Motor control | Four ODrive v3.5 (two motors each), custom firmware, field-oriented control at 10 kHz | [1][2] |
| Main controller | Teensy 3.5: state machine, sends leg targets and gains at 100 Hz over UART (500 kbaud) | [1][2] |
| Sensors | AS5047P encoder per motor (incremental mode only); BNO080 IMU | [1] |
| Power | Two 1000 mAh 6S LiPo packs; relay for an off-board e-stop | [1] |
| Jumping | 1.14 m maximum jump; vertical jumping agility 2.23 m/s | [2] |
| Running, bandwidth | 0.9 m/s steady trot; cost of transport 3.2; torque bandwidth about 150 Hz (estimate) | [2] |

## How it works

Each leg is a five-bar linkage whose two upper links turn on coaxial shafts, driven by two motors
on the carbon-fibre side panel through belts and SLS-printed pulleys [1]. The single 3:1 stage
keeps the leg backdrivable, so foot force can be estimated from motor current; the paper checks
this against a load cell [2]. The frame is two waterjet-cut 4 mm carbon-fibre panels joined by
folded aluminium sheet; the feet are cast silicone [1].

Gaits are open loop. The Teensy computes sinusoidal foot paths for walking, trotting, bounding and
pronking, converts them to a virtual leg angle and length with set stiffness and damping, and
sends them to the ODrives at 100 Hz; each ODrive runs a PD loop in leg coordinates and maps it to
motor torques through the leg Jacobian [1][2]. Commands come over an XBee radio [1]. No URDF,
MuJoCo model or ROS package was found in the project repos.

## What it is used for

- Research on agile, jumping legged robots: the paper compares Doggo with Minitaur, MIT Cheetah 2
  and others on jump height, speed and cost of transport [2].
- Student and hobby builds; the team asked others to build and improve it, and went on to Pupper v3 [1].

## Cost and BOM

The BOM sheet totals **$2,971.02** with prices given as plus or minus 5% [3]; it is labelled a work
in progress and is undated, published with the 2019 project. Waterjet leg links ($306) and
four ODrives ($476) are the largest items [3]. The paper puts materials and machining under $3000 [2].

## Building it

**Difficulty 4:** order waterjet carbon-fibre and aluminium parts and SLS-printed pulleys, drill
and tap set-screw holes, cast the feet, wire four ODrives to the Teensy, flash the custom ODrive
firmware and the Teensy code; assembly needs only hand tools [1][2]. Build time is not stated.
Pitfalls: belt tension adds friction; legs must be horizontal at power-on for calibration; the
Fusion 360 download has broken before; the BOM lists 24 V ODrives, the README 48 V [1][3].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| CAD | Fusion 360 share link | [DoggoHardware/FullCAD](https://github.com/Nate711/StanfordDoggoProject/tree/master/DoggoHardware) [1] | MIT for the repository; the CAD itself is an external link |
| BOM | Google Sheets | [BOM](https://docs.google.com/spreadsheets/d/1MQRoZCfsMdJhHQ-ht6YvhzNvye6xDXO8vhWQql2HtlI/edit#gid=726381752) [3] | None stated |
| Teensy code | PlatformIO C++ | [Doggo](https://github.com/Nate711/Doggo) [4] | No licence file |
| ODrive firmware fork | C/C++, Python setup script | [ODrive PD_CONTROL](https://github.com/Nate711/ODrive/tree/PD_CONTROL) [5] | No licence file at the fork root |
| Design write-up | Markdown | [README](https://github.com/Nate711/StanfordDoggoProject) [1] | MIT |

## Strengths and limits

- **Strengths:** record-setting jumps from cheap parts; a clear belt-drive QDD design with a
  detailed write-up and paper; under $3000 in materials [1][2][3].
- **Limits:** unsupported since 2024; open-loop gaits, slow turning and fiddly calibration; code
  repos without licences; Fusion-only CAD; no simulation model [1][4][5].

## What to reuse

- A single 3:1 belt stage on a hobby brushless motor for a backdrivable leg [2].
- Virtual-leg PD control (angle and length) run on the motor drivers, with targets from a cheap MCU [1].

## Related robots

- [Pupper v3](pupper-v3.md): the team's current brushless teaching quadruped.
- [Mini Cheetah](mini-cheetah.md): MIT's quasi-direct-drive quadruped with 12 joints.
- [ODRI Solo](odri-solo.md): an open torque-controlled quadruped with belt-driven modules.

## Sources

1. [StanfordDoggoProject README and licence](https://github.com/Nate711/StanfordDoggoProject), accessed 2026-11-18
2. [Stanford Doggo: An Open-Source, Quasi-Direct-Drive Quadruped (ICRA 2019)](https://arxiv.org/abs/1905.04254), accessed 2026-11-18
3. [Stanford Doggo bill of materials (Google Sheets)](https://docs.google.com/spreadsheets/d/1MQRoZCfsMdJhHQ-ht6YvhzNvye6xDXO8vhWQql2HtlI/edit#gid=726381752), accessed 2026-11-18
4. [Doggo Teensy code repository](https://github.com/Nate711/Doggo), accessed 2026-11-18
5. [Doggo ODrive firmware fork (PD_CONTROL branch)](https://github.com/Nate711/ODrive/tree/PD_CONTROL), accessed 2026-11-18
