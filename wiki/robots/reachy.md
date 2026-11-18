---
type: robot
name: Reachy and Reachy 2
summary: Pollen Robotics' research humanoid torso with two 7-DoF arms built from Orbita parallel actuators, a 3-DoF neck, stereo and depth cameras and an optional omnidirectional base; Reachy 2 has an Apache-2.0 ROS 2 Humble stack, Gazebo and MuJoCo simulation and LeRobot support, and sells for $70,000, while its hardware design is not published.
tags: [humanoid, torso, mobile-manipulator, orbita, parallel-actuator, ros2, lerobot, vr-teleoperation, pollen-robotics, hugging-face, gazebo, mujoco]
category: humanoid
tier: B
openness: software-only
maker: Pollen Robotics (part of Hugging Face since 2025)
year: 2020
license: {hardware: , software: Apache-2.0, docs: }
links: {repo: "https://github.com/pollen-robotics/reachy2_core", docs: "https://docs.pollen-robotics.com/", cad: , paper: , site: "https://www.pollen-robotics.com/reachy/"}
specs: {dof: 21, payload_kg: 3, reach_mm: , mass_kg: 50, size_mm: , speed_mps: , runtime_h: 8}
stack: {actuators: "Pollen Orbita 2D (shoulders, elbows) and Orbita 3D (wrists, neck) parallel actuators", mcu: , compute: "SolidRun Bedrock v3000 fanless industrial PC; AI runs on the user's own computer", sensors: ["stereo RGB cameras in the head", "RGB-D torso camera", "LiDAR on the mobile base"], sim_models: ["URDF/Xacro (reachy2_core, reachy_description)", "Gazebo (reachy2_core, reachy_gazebo)", "MuJoCo (reachy2_core Docker image)"], ros2: official}
cost: {type: retail, usd: 70000, as_of: 2025-04-14, source: "https://huggingface.co/blog/hugging-face-pollen-robotics-acquisition"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-04-07, stars: 25, active: false}
use_cases: [research, teleop, imitation-learning, manipulation, data-collection]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://www.pollen-robotics.com/reachy/", title: Pollen Robotics Reachy 2 product page, accessed: 2026-11-18}
  - {url: "https://docs.pollen-robotics.com/hardware-guide/specifications/general/", title: "Reachy 2 docs: general specifications", accessed: 2026-11-18}
  - {url: "https://docs.pollen-robotics.com/hardware-guide/specifications/mobile-base/", title: "Reachy 2 docs: mobile base specifications", accessed: 2026-11-18}
  - {url: "https://github.com/pollen-robotics/reachy2_core", title: reachy2_core ROS 2 workspace README, accessed: 2026-11-18}
  - {url: "https://github.com/pollen-robotics/reachy2-sdk", title: reachy2-sdk Python SDK README, accessed: 2026-11-18}
  - {url: "https://huggingface.co/docs/lerobot/reachy2", title: "LeRobot docs: Reachy 2", accessed: 2026-11-18}
  - {url: "https://huggingface.co/blog/hugging-face-pollen-robotics-acquisition", title: "Hugging Face blog: acquisition of Pollen Robotics (2025-04-14)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/pollen-robotics-debuts-reachy-2-humanoid-at-ces-2025/", title: "The Robot Report: Pollen Robotics debuts Reachy 2 humanoid at CES 2025 (2025-01-08)", accessed: 2026-11-18}
  - {url: "https://www.engadget.com/2020/01/05/reachy-is-an-expressive-open-source-robot/", title: "Engadget: Reachy is an expressive, open-source robot (2020-01-05)", accessed: 2026-11-18}
  - {url: "https://forum.pollen-robotics.com/t/3d-cad-models-release/90", title: "Pollen forum: 3D CAD models release (2020-07-07)", accessed: 2026-11-18}
---

# Reachy and Reachy 2

A human-scale research torso from Pollen Robotics of Bordeaux: two arms, an expressive head and,
on Reachy 2, an optional omnidirectional base [1][8]. The first Reachy debuted at CES 2020 [8][9];
Reachy 2 followed at CES 2025 [8], and Hugging Face bought Pollen in April 2025 [7]. Its software is
open and LeRobot supports it, but Reachy 2's mechanical design is not published.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Reachy 2, two arms on the mobile base | [1][8] |
| Degrees of freedom | 21 counted: two 7-DoF arms, two grippers, a 3-DoF neck, two antennas; the base's three omni wheels not counted | [2][6] |
| Height, mass | 136–166 cm, adjustable by hand; up to 50 kg for the full robot (maker's claims) | [1][2] |
| Arm payload | About 3 kg per arm (maker's claim) | [1] |
| Actuators | Per arm: 2 Orbita 2D (shoulder, elbow) and 1 Orbita 3D (wrist); neck: 1 Orbita 3D | [2] |
| Sensors | Stereo cameras in the head, RGB-D torso camera, LiDAR on the base | [1][6] |
| Mobile base | 3 omni wheels, 50 cm diameter, 25 kg, 80 kg payload, 8 h battery life (maker's claims) | [3] |
| Compute | SolidRun Bedrock v3000 fanless PC; AI runs on the user's computer for now | [2] |

## How it works

Each arm chains three parallel joints: Orbita 2D actuators at shoulder and elbow and an Orbita 3D
wrist, with cables routed through the joints; left and right arms are identical [2]. Another Orbita
3D moves the head, and each arm ends in a gripper [2]. Pollen sells one- or two-arm versions on a
fixed stand or the mobile base [8]; speed and arm reach are not published.

The robot runs ROS 2 Humble: `reachy2_core` holds the URDF, ros2_control controllers, launch files
and a Gazebo world under Apache-2.0 [4], and Pollen's Docker image also runs the robot in MuJoCo
[6]. Users program it with the Python SDK `reachy2-sdk` [5] or drive it from a VR teleoperation
app [1]. LeRobot records datasets from that app, then trains and evaluates policies such as ACT [6].

| Version | Shown | Arms and head | Base | Software | Price | Source |
|---|---|---|---|---|---|---|
| Reachy | CES 2020 | One or two 7-DoF arms with grippers or hands; head on a pan-tilt neck | — | Python | $9,000 one arm; about $17,000 two arms and head (2020) | [9] |
| Reachy 2 | CES 2025 | One or two 7-DoF Orbita arms with grippers, 3-DoF neck, antennas | Fixed or omnidirectional | ROS 2 Humble, Python SDK, VR app | $70,000 (2025) | [1][2][7][8] |

## What it is used for

- Teleoperated data collection and imitation learning through LeRobot [6].
- Research labs: users include Cornell, Carnegie Mellon and CNRS; Pollen claims 100 robots sold [8].

## Cost and BOM

**Reachy 2: $70,000**, retail, per Hugging Face's post of 2025-04-14 (currency shown only as "$") [7];
Pollen's product page gives no price [1]. The first Reachy cost $9,000 with one arm and about $17,000
with two arms and a head in January 2020 [9]. No BOM is published.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| ROS 2 stack: description, controllers, Gazebo | ROS 2 Humble packages, URDF/Xacro | [reachy2_core](https://github.com/pollen-robotics/reachy2_core) [4] | Apache-2.0 |
| Python SDK | Python, on PyPI | [reachy2-sdk](https://github.com/pollen-robotics/reachy2-sdk) [5] | Apache-2.0 |
| Simulation image | Docker, Gazebo or MuJoCo | `pollenrobotics/reachy2_core` on Docker Hub [6] | Not stated |
| Reachy 2 CAD, electronics, firmware | — | Not published; the docs' [CAD page](https://docs.pollen-robotics.com/hardware-guide/makers/cad-files/) is a placeholder | Closed |
| First Reachy CAD: arm, trunk, gripper, head | Onshape | [Pollen forum](https://forum.pollen-robotics.com/t/3d-cad-models-release/90) [10] | CC BY-SA, version not stated |

## Strengths and limits

- **Strengths:** human-scale bimanual torso with compact parallel joints, an official Apache-2.0
  ROS 2 stack, Gazebo and MuJoCo sims, VR teleoperation and LeRobot recording [1][2][4][6].
- **Limits:** $70,000 [7]; no CAD or electronics for Reachy 2, though Hugging Face calls its hardware
  open [7]; 3 kg arm payload [1]; no published speed or reach; VR teleoperation needs Windows [6].

## What to reuse

- Parallel actuators like Orbita that put two or three rotations in one compact joint [2].

## Related robots

- [Reachy Mini](reachy-mini.md): Pollen's desktop robot; [SO-101](so-101.md): the low-cost LeRobot arm.
- [iCub](icub.md), [PAL TALOS](pal-talos.md), [Pepper](pepper.md), [NAO](nao.md): research humanoids;
  [TIAGo](tiago.md), [Hello Robot Stretch](hello-robot-stretch.md): mobile manipulators for lab work.

## Sources

1. [Pollen Robotics Reachy 2 product page](https://www.pollen-robotics.com/reachy/), accessed 2026-11-18
2. [Reachy 2 docs: general specifications](https://docs.pollen-robotics.com/hardware-guide/specifications/general/), accessed 2026-11-18
3. [Reachy 2 docs: mobile base specifications](https://docs.pollen-robotics.com/hardware-guide/specifications/mobile-base/), accessed 2026-11-18
4. [reachy2_core ROS 2 workspace README](https://github.com/pollen-robotics/reachy2_core), accessed 2026-11-18
5. [reachy2-sdk Python SDK README](https://github.com/pollen-robotics/reachy2-sdk), accessed 2026-11-18
6. [LeRobot docs: Reachy 2](https://huggingface.co/docs/lerobot/reachy2), accessed 2026-11-18
7. [Hugging Face blog: acquisition of Pollen Robotics (2025-04-14)](https://huggingface.co/blog/hugging-face-pollen-robotics-acquisition), accessed 2026-11-18
8. [The Robot Report: Pollen Robotics debuts Reachy 2 humanoid at CES 2025 (2025-01-08)](https://www.therobotreport.com/pollen-robotics-debuts-reachy-2-humanoid-at-ces-2025/), accessed 2026-11-18
9. [Engadget: Reachy is an expressive, open-source robot (2020-01-05)](https://www.engadget.com/2020/01/05/reachy-is-an-expressive-open-source-robot/), accessed 2026-11-18
10. [Pollen forum: 3D CAD models release (2020-07-07)](https://forum.pollen-robotics.com/t/3d-cad-models-release/90), accessed 2026-11-18
