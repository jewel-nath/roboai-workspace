---
type: robot
name: BCN3D Moveo
summary: Fully printed 5-axis arm with a servo gripper, driven by stepper motors from 3D-printer electronics (Arduino Mega, RAMPS, Marlin); open SolidWorks, STL and BOM since 2016, dormant since then.
tags: [3d-printed, stepper, nema17, nema23, arduino-mega, ramps, marlin, g-code, education, solidworks]
category: arm
tier: B
openness: full
maker: BCN3D Technologies, with the Departament d'Ensenyament of the Generalitat de Catalunya
year: 2016
license: {hardware: MIT, software: GPL-3.0-or-later, docs: MIT}
links: {repo: "https://github.com/BCN3D/BCN3D-Moveo", docs: "https://github.com/BCN3D/BCN3D-Moveo/tree/master/USER%20MANUAL", cad: "https://github.com/BCN3D/BCN3D-Moveo/tree/master/CAD%20files", paper: , site: }
specs: {dof: 6, payload_kg: , reach_mm: , mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "6 stepper motors (NEMA 17, one with a 5:1 planetary gearbox; 2 x NEMA 23; one smaller 35 mm motor) on T5 belts, plus a 13 kg·cm hobby servo for the gripper", mcu: "Arduino Mega 2560 with a RAMPS 1.4 shield and 6 x TB6560 stepper drivers", compute: "host PC sending G-code over USB", sensors: [], sim_models: ["URDF and MoveIt config (community moveo_ros, ROS 1)"], ros2: none}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: 3, hours: , print_hours: }
maturity: {last_commit: 2016-10-03, stars: 2025, active: false}
use_cases: [education, hobby]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/BCN3D/BCN3D-Moveo", title: BCN3D Moveo repository README and licence, accessed: 2026-11-18}
  - {url: "https://github.com/BCN3D/BCN3D-Moveo/tree/master/BOM", title: BCN3D Moveo BOM (PDF), accessed: 2026-11-18}
  - {url: "https://github.com/BCN3D/BCN3D-Moveo/tree/master/USER%20MANUAL", title: BCN3D Moveo user manual (PDF), accessed: 2026-11-18}
  - {url: "https://github.com/BCN3D/BCN3D-Moveo/tree/master/FIRMWARE/Marlin_BCN3D_Moveo", title: BCN3D Moveo Marlin firmware, accessed: 2026-11-18}
  - {url: "https://hackaday.io/project/3800-3d-printable-robot-arm", title: "Andreas Hölldorfer: 3D printable robot arm (Hackaday.io)", accessed: 2026-11-18}
  - {url: "https://github.com/jesseweisberg/moveo_ros", title: moveo_ros community ROS packages README, accessed: 2026-11-18}
---

# BCN3D Moveo

A 3D-printed arm with five axes and a gripper, driven by stepper motors through belts. BCN3D
Technologies designed it in 2016 with Catalonia's education department, as a cheap arm for
vocational schools, and published every file [1]. It is **dormant**: the last commit is from
October 2016. It still matters as a well-documented printed stepper arm that hobbyists build and
that community ROS packages target [6].

## Specs

| Item | Value | Source |
|---|---|---|
| Axes | 5, plus a servo gripper; `dof: 6` counts the gripper as one | [2][3] |
| Motors | 6 steppers: NEMA 17 (1.6 A), NEMA 17 with 5:1 planetary gearbox (2 N·m), 2 x NEMA 23 (3 A, 28 kg·cm), NEMA 17 (1.33 A), 35 mm stepper (1 A) | [2] |
| Gripper | Hobby servo, 13 kg·cm, 55 g | [2] |
| Electronics | Arduino Mega 2560, RAMPS 1.4, 6 x TB6560 drivers | [2] |
| Power | 24 V 320 W supply, 24 V to 12 V converter, two 24 V fans | [2] |
| Transmission | T5 timing belt (1.8 m) and T5 pulleys | [2] |
| Base | Wooden board, 550 x 550 x 16 mm | [2] |
| Host link | USB at 250,000 baud | [3][4] |
| Reach, payload, mass, precision | Not published | — |

## How it works

Printed housings hold the motors and bearings for each of four "articulations"; belts and pulleys
add reduction, and one NEMA 17 has a 5:1 planetary gearbox [2]. The BOM lists six steppers and six
drivers for five axes, two of them NEMA 23 motors [2][3]. A hobby servo opens and closes a printed
gear-driven gripper [2]. The BOM lists no encoders or limit switches, so the steppers run open loop
[2].

The electronics are a 3D printer's: an Arduino Mega with a RAMPS shield runs a modified Marlin
firmware, and the arm is moved with G-code [3][4]. The manual uses Pronterface to jog the axes and
then saves the found positions as a G-code sequence to replay [3]. BCN3D ships no kinematics or ROS
driver.

The community `moveo_ros` packages (ROS 1 Kinetic, MIT) add a URDF, a MoveIt config and an Arduino
sketch that follows MoveIt trajectories over rosserial, plus a webcam pick-and-place demo [6]. No
ROS 2 package or MuJoCo model was found.

## What it is used for

- Teaching mechanical design, automation and programming: BCN3D ran an assembly workshop for 15
  Catalan schools that then used the arm in class [1].
- Hobby builds and ROS 1 MoveIt practice with `moveo_ros` [6].

## Cost and BOM

No cost: the BOM lists parts and quantities but no prices or suppliers [2]. Parts are commodity
3D-printer and CNC items (steppers, RAMPS, TB6560 drivers, 608 bearings, T5 belts), plus filament
for 40 printed parts [1][2].

## Building it

**Difficulty 3:** print about 40 parts, wire six stepper drivers to a RAMPS board, flash Marlin with
the Arduino IDE and tune motion by hand [1][2][3].

- **Files:** STL per articulation, SolidWorks parts and assemblies, the BOM and a bilingual
  (Spanish and English) assembly and user manual [1][3].
- **Print settings and time:** not stated.
- **Pitfalls:** no STEP files, so non-SolidWorks users must work from the STLs; no homing switches
  in the BOM, so the start position is set by hand; the firmware is a 2016 Marlin fork [1][2][4][6].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| CAD | SolidWorks parts and assemblies | [CAD files/](https://github.com/BCN3D/BCN3D-Moveo/tree/master/CAD%20files) | MIT (repository LICENSE) |
| Print files | STL | [STL files/](https://github.com/BCN3D/BCN3D-Moveo/tree/master/STL%20files) | MIT |
| BOM | PDF, parts and quantities only | [BOM/](https://github.com/BCN3D/BCN3D-Moveo/tree/master/BOM) [2] | MIT |
| Firmware | Marlin fork, Arduino C++ | [FIRMWARE/](https://github.com/BCN3D/BCN3D-Moveo/tree/master/FIRMWARE/Marlin_BCN3D_Moveo) [4] | GPL-3.0-or-later in the file headers, although the repository LICENSE says MIT |
| Manual | PDF, Spanish and English | [USER MANUAL/](https://github.com/BCN3D/BCN3D-Moveo/tree/master/USER%20MANUAL) [3] | MIT |
| ROS packages, URDF | ROS 1 | [moveo_ros](https://github.com/jesseweisberg/moveo_ros) [6] | MIT (community) |

## Strengths and limits

- **Strengths:** every file open under a permissive licence; cheap, common 3D-printer electronics
  and G-code control; stepper motors with belt reduction; a printed design that BCN3D invites users
  to modify [1][2].
- **Limits:** dormant since 2016; no prices, reach, payload or precision figures; open-loop
  steppers with no encoders or homing switches [2]; SolidWorks-only CAD; no ROS 2 driver or modern
  sim model; the firmware licence conflicts with the repository LICENSE [4].

## What to reuse

- 3D-printer electronics (RAMPS and Marlin) as a cheap multi-axis stepper controller, driven with
  G-code [3][4].
- Belt-and-pulley reductions in printed housings, with a planetary gearbox only where torque is
  highest [2].

## Related robots

- [SO-101](so-101.md) and [Koch v1.1](koch-v1-1.md): today's printed arms, on serial-bus servos with
  position feedback and LeRobot support.
- [OpenManipulator-X](openmanipulator-x.md): a small commercial arm for classrooms, on Dynamixel
  servos.
- Andreas Hölldorfer's 3D printable robot arm (BetaBots): the 2015 printed six-axis stepper arm,
  also on TB6560 drivers and a RAMPS board, that the Moveo is based on [1][5].

## Sources

1. [BCN3D Moveo repository README and licence](https://github.com/BCN3D/BCN3D-Moveo), accessed 2026-11-18
2. [BCN3D Moveo BOM (PDF)](https://github.com/BCN3D/BCN3D-Moveo/tree/master/BOM), accessed 2026-11-18
3. [BCN3D Moveo user manual (PDF)](https://github.com/BCN3D/BCN3D-Moveo/tree/master/USER%20MANUAL), accessed 2026-11-18
4. [BCN3D Moveo Marlin firmware](https://github.com/BCN3D/BCN3D-Moveo/tree/master/FIRMWARE/Marlin_BCN3D_Moveo), accessed 2026-11-18
5. [Andreas Hölldorfer: 3D printable robot arm (Hackaday.io)](https://hackaday.io/project/3800-3d-printable-robot-arm), accessed 2026-11-18
6. [moveo_ros community ROS packages README](https://github.com/jesseweisberg/moveo_ros), accessed 2026-11-18
