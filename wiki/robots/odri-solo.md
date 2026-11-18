---
type: robot
name: ODRI Solo-8, Solo-12 and Bolt
summary: Open torque-controlled research quadrupeds from the Open Dynamic Robot Initiative, built from one 3D-printed brushless actuator module, with full CAD, electronics and BOM under BSD licences; PAL Robotics sold the Solo-12 but has stopped, and the hardware repo has been idle since 2022.
tags: [quadruped, biped, torque-control, brushless, belt-drive, 3d-printed, odri, solo-12, bolt, open-hardware, research]
category: legged
tier: B
openness: full
maker: Open Dynamic Robot Initiative (Max Planck Institute for Intelligent Systems, New York University, LAAS-CNRS)
year: 2019
license: {hardware: BSD-3-Clause, software: BSD-3-Clause, docs: BSD-3-Clause}
links: {repo: "https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware", docs: "https://github.com/open-dynamic-robot-initiative/open-dynamic-robot-initiative.github.io/wiki", cad: "https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/tree/master/mechanics/quadruped_robot_12dof_v1", paper: "https://arxiv.org/abs/1910.00093", site: "https://open-dynamic-robot-initiative.github.io/"}
specs: {dof: 12, payload_kg: , reach_mm: , mass_kg: 2.5, size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "12 ODRI actuator modules: T-Motor Antigravity 4004 300 kV brushless motor, two-stage 9:1 timing-belt reduction, 2.5 N·m at 12 A", mcu: "ODRI master board (ESP32) and six BLMC µDriver dual-motor boards", compute: "external real-time PC over Ethernet or Wi-Fi", sensors: ["optical encoder per motor (Broadcom AEDT-9810)", "IMU (MicroStrain 3DM-CX5-25)"], sim_models: ["URDF/Xacro and PyBullet wrappers (robot_properties_solo: Solo-8, Solo-12)"], ros2: community}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: 4, hours: , print_hours: }
maturity: {last_commit: 2022-09-06, stars: 1531, active: false}
use_cases: [research, locomotion, reinforcement-learning]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware", title: "ODRI open_robot_actuator_hardware repository (README; Solo-8, Solo-12, Bolt, actuator and µDriver pages)", accessed: 2026-11-18}
  - {url: "https://github.com/open-dynamic-robot-initiative/master-board", title: ODRI master board README, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/1910.00093", title: An Open Torque-Controlled Modular Robot Architecture for Legged Locomotion Research, accessed: 2026-11-18}
  - {url: "https://solo.pal-robotics.com/solo", title: PAL Robotics SOLO 12 page, accessed: 2026-11-18}
  - {url: "https://github.com/open-dynamic-robot-initiative/robot_properties_solo", title: robot_properties_solo README, accessed: 2026-11-18}
  - {url: "https://github.com/stack-of-tasks/ros2_hardware_interface_odri", title: ros2_hardware_interface_odri README, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2309.16683", title: Controlling the Solo12 Quadruped Robot with Deep Reinforcement Learning, accessed: 2026-11-18}
---

# ODRI Solo-8, Solo-12 and Bolt

Small torque-controlled legged robots from the Open Dynamic Robot Initiative (ODRI): labs at MPI-IS,
NYU and LAAS-CNRS. Every joint is the same mostly 3D-printed brushless module, and CAD, electronics,
BOM and software are BSD-licensed [1][3]. PAL Robotics sold the Solo-12, but sales are
**discontinued** [4], and the hardware repo has been idle since September 2022.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Solo-12 v1: body module and four identical 3-DoF legs, 2.5 kg | [1] |
| Actuator module | T-Motor Antigravity 4004 300 kV, two 3:1 belt stages (9:1), 150 g, 2.5 N·m at 12 A, 160 mm segment | [1] |
| Encoder | Broadcom AEDT-9810 optical, 5000 lines (20,000 counts per motor turn) | [1] |
| Range of motion | Hip abduction 215° (325° with hip flexion); hip flexion and knee turn several full turns, limited by wiring | [1] |
| Motor drivers | µDriver: two motors per board, torque control at 10 kHz, 5–32 V input (run at 24 V) | [1] |
| Master board | ESP32; SPI to up to 8 µDrivers; Ethernet round trip 0.2 ms, Wi-Fi (ESP-NOW) 1.2 ms; 1 kHz loop | [2] |
| IMU, power | MicroStrain 3DM-CX5-25; v1 is tethered for 24 V power and Ethernet | [1] |
| Payload, size, speed, runtime | Not published in the sources read | — |

## How it works

Each joint is one module: a drone outrunner motor, an optical encoder and two timing-belt stages in
3D-printed shells, with three small machined parts [1]. The low 9:1 ratio keeps joints backdrivable,
so torque is set through motor current, with no joint torque sensor [1]. The founding paper reports
a maximum dimensionless leg stiffness of 10.8 without active damping [3].

µDriver boards close the current loop at 10 kHz and talk over SPI to the master board, which links
to a real-time PC by raw Ethernet frames or Wi-Fi [1][2]. A community `ros2_control` interface was
tested on Bolt [6]. robot_properties_solo has Solo-8 and Solo-12 URDF/Xacro and PyBullet wrappers [5];
no MuJoCo Menagerie model was found.

| Variant | DoF | Mass | Notes | Source |
|---|---|---|---|---|
| Solo-8 | 8 | 2.2 kg (v1), 1.7 kg (v2) | v1 in the founding paper; v2 lighter, new electronics | [1][3] |
| Solo-12 | 12 | 2.5 kg; v1.1 about 300 g more (ODRI estimate) | v1 tethered, sold by PAL; v1.1 adds LiPo packs and wireless | [1][4] |
| Bolt (biped) | 6 | 1.34 kg | Three joints per leg, passive ankle, 200 mm leg segments | [1] |

## What it is used for

- Torque-controlled legged locomotion research at the ODRI labs, and bipeds with Bolt [1][3][6].
- Learning-based control: a 2023 LAAS paper trained a PPO policy that outputs joint impedance
  targets on Solo-12 and ran it indoors and outdoors [7].
- The same module builds manipulators such as the TriFinger platform [1].

## Cost and BOM

The BOM tables list parts and ordering links but no prices [1]. PAL sold kits and assembled robots
with no public price and has stopped [4], so `cost` stays empty.

## Building it

**Difficulty 4:** print the shells (pulleys need SLA or multijet prints), machine or buy three small
metal parts per module, prepare motors and encoders, order the 6-layer µDriver boards from Gerbers,
and calibrate with a jig, following the step-by-step guides [1]. Build time is not stated.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Mechanics, BOM, guides | SolidWorks (zip), eDrawings, STL, PDF drawings | [mechanics/](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/tree/master/mechanics) [1] | BSD-3-Clause |
| µDriver electronics | Eagle files, Gerbers, assembly packet | [electronics/](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware/tree/master/electronics) [1] | BSD-3-Clause |
| Master board | Hardware files, ESP-IDF firmware, C++/Python SDK | [master-board](https://github.com/open-dynamic-robot-initiative/master-board) [2] | BSD-2-Clause |
| Models | URDF/Xacro, meshes, PyBullet | [robot_properties_solo](https://github.com/open-dynamic-robot-initiative/robot_properties_solo) [5] | BSD-3-Clause |
| ROS 2 interface | `ros2_control` SystemInterface | [ros2_hardware_interface_odri](https://github.com/stack-of-tasks/ros2_hardware_interface_odri) [6] | BSD-3-Clause in package.xml; no LICENSE file |

## Strengths and limits

- **Strengths:** every file open under permissive licences; one module for every joint, reused in a
  biped and a manipulator; 10 kHz current control and 1 kHz loops; light and backdrivable [1][2].
- **Limits:** idle since 2022 and no longer sold [4]; SolidWorks-only CAD; precision prints and
  machined parts; v1 is tethered; no payload, speed or runtime figures; community ROS 2 only [6].

## Related robots

- [TriFinger](trifinger.md): manipulation platform built from the same actuator module.
- [Mini Cheetah](mini-cheetah.md): the larger proprioceptive-actuator quadruped from MIT.
- [Stanford Doggo](stanford-doggo.md) and [Pupper v3](pupper-v3.md): other open brushless quadrupeds.

## Sources

1. [ODRI open_robot_actuator_hardware repository (README; Solo-8, Solo-12, Bolt, actuator and µDriver pages)](https://github.com/open-dynamic-robot-initiative/open_robot_actuator_hardware), accessed 2026-11-18
2. [ODRI master board README](https://github.com/open-dynamic-robot-initiative/master-board), accessed 2026-11-18
3. [An Open Torque-Controlled Modular Robot Architecture for Legged Locomotion Research](https://arxiv.org/abs/1910.00093), accessed 2026-11-18
4. [PAL Robotics SOLO 12 page](https://solo.pal-robotics.com/solo), accessed 2026-11-18
5. [robot_properties_solo README](https://github.com/open-dynamic-robot-initiative/robot_properties_solo), accessed 2026-11-18
6. [ros2_hardware_interface_odri README](https://github.com/stack-of-tasks/ros2_hardware_interface_odri), accessed 2026-11-18
7. [Controlling the Solo12 Quadruped Robot with Deep Reinforcement Learning](https://arxiv.org/abs/2309.16683), accessed 2026-11-18
