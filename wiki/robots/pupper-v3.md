---
type: robot
name: Stanford Pupper v3
summary: Twelve-joint brushless teaching quadruped from Stanford with a Raspberry Pi 5, a reinforcement-learning walking policy, ROS 2 Jazzy software and a public BOM of about $2,160; the CAD is shared on Onshape and Fusion 360 but no hardware licence was found.
tags: [quadruped, brushless, raspberry-pi, ros2, reinforcement-learning, mujoco, education, companion, stanford]
category: legged
tier: B
openness: partial
maker: Stanford University students (Nathan Kau, Gabrael Levine), supported by Hands-On Robotics
year: 2024
license: {hardware: , software: GPL-3.0-only AND MIT, docs: }
links: {repo: "https://github.com/Nate711/pupperv3-monorepo", docs: "https://pupper-v3-documentation.readthedocs.io/en/latest/", cad: "https://cad.onshape.com/documents/97a1bc3e752ec66822dbb5bb/w/c7f9232ccbc53a2e3f6ee909/e/74c0b3caf828b9fd1994bcd6", paper: , site: }
specs: {dof: 12, payload_kg: , reach_mm: , mass_kg: 3, size_mm: "250 x 220 x 200", speed_mps: , runtime_h: }
stack: {actuators: "12 Steadywin GIM4305 brushless motors with 10:1 planetary gearbox and driver (about 3.5 N·m peak, 1.0 N·m continuous)", mcu: "custom Raspberry Pi HAT control board with BNO086 IMU", compute: "Raspberry Pi 5 (8 GB); M.2 slot for an AI accelerator", sensors: ["BNO086 IMU", "IMX296 global-shutter fisheye camera (222° field of view)", "microphone", "joint angle, velocity and effort from the motor drivers", "battery voltage"], sim_models: ["URDF and MJCF, MJX-ready (pupper_v3_description)", "MuJoCo simulator package (pupperv3_mujoco_sim)"], ros2: official}
cost: {type: bom, usd: 2158.91, as_of: 2026-11-18, source: "https://docs.google.com/spreadsheets/d/1e6Hyhc8V6_9mfPMaPCI1v3W4uGBJp4r0xIzH3rUtAeI/edit?usp=sharing"}
build: {difficulty: 3, hours: , print_hours: }
maturity: {last_commit: 2026-07-25, stars: 77, active: true}
use_cases: [education, reinforcement-learning, locomotion, companion, research, hobby]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://pupper-v3-documentation.readthedocs.io/en/latest/", title: Pupper v3 documentation (home), accessed: 2026-11-18}
  - {url: "https://pupper-v3-documentation.readthedocs.io/en/latest/learn_more/tech_specs.html", title: Pupper v3 tech specs, accessed: 2026-11-18}
  - {url: "https://pupper-v3-documentation.readthedocs.io/en/latest/guide/sourcing_parts.html", title: Pupper v3 sourcing parts, accessed: 2026-11-18}
  - {url: "https://docs.google.com/spreadsheets/d/1e6Hyhc8V6_9mfPMaPCI1v3W4uGBJp4r0xIzH3rUtAeI/edit?usp=sharing", title: Pupper v3 bill of materials (Google Sheets), accessed: 2026-11-18}
  - {url: "https://pupper-v3-documentation.readthedocs.io/en/latest/guide/building.html", title: "Pupper v3 building guide (CAD links, flashing)", accessed: 2026-11-18}
  - {url: "https://github.com/Nate711/pupperv3-monorepo", title: pupperv3-monorepo README and licences, accessed: 2026-11-18}
  - {url: "https://pupper-v3-documentation.readthedocs.io/en/latest/course/course.html", title: "Pupper v3 docs: Robotics & AI course (Stanford CS 123)", accessed: 2026-11-18}
  - {url: "https://github.com/Nate711/StanfordDoggoProject", title: "Stanford Doggo README (2024 end-of-life notice with early Pupper v3 specs)", accessed: 2026-11-18}
  - {url: "https://github.com/stanfordroboticsclub/Pupper-Raspi-PDB", title: Pupper power distribution board for Raspberry Pi, accessed: 2026-11-18}
---

# Stanford Pupper v3

A small brushless quadruped built through years of robotics teaching at Stanford, with support from
Hands-On Robotics. It walks with a policy trained by reinforcement learning in simulation, talks
through the OpenAI Realtime API, and costs about $2000 to build; the docs call everything open
source [1]. The software is licensed, but **no hardware licence was found** for the CAD or PCBs.

## Specs

| Item | Value | Source |
|---|---|---|
| Degrees of freedom | 12, three per leg; two optional 9 g ear servos are not counted | [2][4] |
| Mass, size | About 3 kg; 250 mm long, 220 mm wide, 200 mm high, crouched | [2] |
| Actuators | Steadywin GIM4305: 4005 brushless motor, 10:1 planetary gearbox, about 3.5 N·m peak, 1.0 N·m continuous with air cooling, about 30 rad/s | [2] |
| Compute, face | Raspberry Pi 5 (8 GB), M.2 slot for an AI accelerator; 4 x 4 in LCD; 3 W speaker | [2] |
| Sensors | BNO086 IMU; IMX296 fisheye camera (222°) in the nose; microphone; joint angle, velocity and effort; battery voltage | [2] |
| Power | Two DeWalt 20 V 1.7 Ah power-tool batteries; payload, speed and runtime not published | [4] |

## How it works

Each leg has hip abduction, hip and knee joints, each a GIM4305 geared motor with its own driver;
the drivers need Pupper-specific firmware and settings [2][5]. Body and legs are PETG prints, the
feet are squash balls, and a stand is optional [4][5]. A custom HAT on the Raspberry Pi 5 carries
the BNO086 IMU and runs its own firmware; a second custom board distributes power [4][5].

The software is one ROS 2 Jazzy monorepo, flashed as a custom Raspberry Pi OS image: a `ros2_control`
interface for the control board, a neural controller that runs the walking policy, URDF and MuJoCo
XML (with MJX and fixed-base versions), a MuJoCo simulation package and a voice bridge [6].

Earlier Puppers drove hobby servos from the Raspberry Pi; the power board linked from the v3 specs
page is that older servo board [2][9]. A July 2024 notice in the Stanford Doggo repo gave early v3
plans: Raspberry Pi 5, an RL policy, a Luxonis depth camera and a BOM of roughly $1000 [8].

## What it is used for

- Stanford's Robotics & AI course (CS 123), with hands-on labs on Pupper [1][7].
- Reinforcement-learning locomotion and sim-to-real on a cheap brushless robot [1][6].
- A talking companion robot with a face screen [1][2].

## Cost and BOM

The BOM sheet totals **$2,158.91**, or $1,785.91 at its minimum; the 12 motors with drivers are
$1,320 of that [4]. The sheet has no date, so `as_of` is the day it was read. Kits are sold by
Present Perfection (USA) and AIFitLab (China) [3]; their prices were not checked.

## Building it

**Difficulty 3:** print the PETG and TPU parts (the BOM gives settings per part), order the two
custom boards as PCB assembly from JLCPCB, flash the motor drivers and the control board, set heat
inserts, then follow the build slides [3][4][5]. Build and print times are not stated.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| CAD | Onshape and Fusion 360 shares | [Building guide](https://pupper-v3-documentation.readthedocs.io/en/latest/guide/building.html) [5] | None found |
| PCBs | Manufacturing files linked from the BOM | [BOM sheet](https://docs.google.com/spreadsheets/d/1e6Hyhc8V6_9mfPMaPCI1v3W4uGBJp4r0xIzH3rUtAeI/edit?usp=sharing) [4] | None found |
| Software | ROS 2 C++ and Python, Rust GUI | [pupperv3-monorepo](https://github.com/Nate711/pupperv3-monorepo) [6] | GPL-3.0 text at the root, no version clause |
| Description, controller, hardware interface | URDF, MJCF, C++ | `pupper_v3_description`, `neural_controller`, `control_board_hardware_interface` [6] | MIT |
| Docs, BOM, build slides | Read the Docs, Google Sheets and Slides | [Docs](https://pupper-v3-documentation.readthedocs.io/en/latest/) [1] | None stated |

## Strengths and limits

- **Strengths:** a modern brushless quadruped with a learned walking policy, ROS 2 and MuJoCo models
  for about $2,160; full BOM with links and print settings; a course built around it [1][4][6][7].
- **Limits:** no hardware licence, so the right to reuse or sell the CAD and boards is unclear; build
  files live in Google Docs and CAD shares, not a repo; no published speed or runtime [4][5].

## Related robots

- [Stanford Doggo](stanford-doggo.md): the earlier jumping quadruped from the same team.
- [Mini Cheetah](mini-cheetah.md) and [ODRI Solo](odri-solo.md): research quadrupeds with open designs.
- [Petoi Nybble and Bittle](petoi-nybble-bittle.md): cheaper servo kits, a step below.

## Sources

1. [Pupper v3 documentation (home)](https://pupper-v3-documentation.readthedocs.io/en/latest/), accessed 2026-11-18
2. [Pupper v3 tech specs](https://pupper-v3-documentation.readthedocs.io/en/latest/learn_more/tech_specs.html), accessed 2026-11-18
3. [Pupper v3 sourcing parts](https://pupper-v3-documentation.readthedocs.io/en/latest/guide/sourcing_parts.html), accessed 2026-11-18
4. [Pupper v3 bill of materials (Google Sheets)](https://docs.google.com/spreadsheets/d/1e6Hyhc8V6_9mfPMaPCI1v3W4uGBJp4r0xIzH3rUtAeI/edit?usp=sharing), accessed 2026-11-18
5. [Pupper v3 building guide (CAD links, flashing)](https://pupper-v3-documentation.readthedocs.io/en/latest/guide/building.html), accessed 2026-11-18
6. [pupperv3-monorepo README and licences](https://github.com/Nate711/pupperv3-monorepo), accessed 2026-11-18
7. [Pupper v3 docs: Robotics & AI course (Stanford CS 123)](https://pupper-v3-documentation.readthedocs.io/en/latest/course/course.html), accessed 2026-11-18
8. [Stanford Doggo README (2024 end-of-life notice with early Pupper v3 specs)](https://github.com/Nate711/StanfordDoggoProject), accessed 2026-11-18
9. [Pupper power distribution board for Raspberry Pi](https://github.com/stanfordroboticsclub/Pupper-Raspi-PDB), accessed 2026-11-18
