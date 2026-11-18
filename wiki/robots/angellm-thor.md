---
type: robot
name: Thor (AngelLM)
summary: 3D-printed six-axis arm with a servo gripper, designed in FreeCAD by Ángel LM, driven by stepper motors through printed gears and belts, controlled with G-code from GRBL or RepRapFirmware, with a ROS 2 Humble MoveIt package; all files CC BY-SA 4.0, components about €350.
tags: [3d-printed, stepper, nema17, grbl, g-code, freecad, kicad, arduino-mega, moveit2, ros2, education]
category: arm
tier: B
openness: full
maker: Ángel LM (AngelLM)
year: 2016
license: {hardware: CC-BY-SA-4.0, software: CC-BY-SA-4.0 AND Apache-2.0, docs: CC-BY-SA-4.0}
links: {repo: "https://github.com/AngelLM/Thor", docs: "http://thor.angel-lm.com/documentation/", cad: "https://github.com/AngelLM/Thor/tree/main/freecad-src", paper: , site: "http://thor.angel-lm.com/"}
specs: {dof: 7, payload_kg: 0.75, reach_mm: , mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "7 NEMA 17 stepper motors (one 40 mm; three 34 mm with 5:1 reduction on axes 2 and 3; three 34 mm on axes 4 to 6) through printed gears and GT2 belts, plus an MG995 servo gripper", mcu: "Arduino Mega with the Thor ControlPCB and 8 A4988 drivers (GRBL 0.9j fork), or a Fly Super8Pro board (RepRapFirmware)", compute: "host PC sending G-code over USB serial (Asgard GUI or ROS 2)", sensors: ["4 optical endstops and a micro endstop for homing"], sim_models: ["URDF, MoveIt 2 config and Gazebo launch (Thor-ROS, ROS 2 Humble)"], ros2: official}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: 3, hours: 10, print_hours: 200}
maturity: {last_commit: 2025-05-09, stars: 1653, active: false}
use_cases: [education, hobby, manipulation]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/AngelLM/Thor", title: Thor repository README and licence, accessed: 2026-11-18}
  - {url: "http://thor.angel-lm.com/documentation/bom/", title: Thor bill of materials, accessed: 2026-11-18}
  - {url: "http://thor.angel-lm.com/faq/", title: Thor frequently asked questions, accessed: 2026-11-18}
  - {url: "http://thor.angel-lm.com/documentation/firmware/", title: "Thor firmware: installation and configuration", accessed: 2026-11-18}
  - {url: "https://github.com/AngelLM/Thor-ROS", title: Thor-ROS README and packages, accessed: 2026-11-18}
  - {url: "https://github.com/AngelLM/ThorControlPCB", title: ThorControlPCB repository, accessed: 2026-11-18}
  - {url: "https://hackaday.io/project/12989-thor", title: "Thor on Hackaday.io (2016 Hackaday Prize entry)", accessed: 2026-11-18}
---

# Thor (AngelLM)

A 3D-printed six-axis arm in the yaw-roll-roll-yaw-roll-yaw layout of many industrial arms, plus a
servo gripper [1][2]. Ángel LM designed it with open tools (FreeCAD, KiCad, GRBL) to teach robotics,
and entered it in the 2016 Hackaday Prize [1][7]. All files are CC BY-SA 4.0, parts cost about €350,
and it is still maintained: the ROS 2 package was updated in October 2025 [1][3][5].

## Specs

| Item | Value | Source |
|---|---|---|
| Axes | 6, plus an MG995 servo gripper; `dof: 7` counts the gripper as one | [1][2] |
| Payload | 750 g including the tool, also with the arm stretched out horizontally (maker's test) | [3] |
| Height | 624–625 mm stretched upright, without tool | [1][3] |
| Motors | 7 steppers: one 40 mm (40 N·cm) on axis 1; three 34 mm (121.2 N·cm with 5:1 reduction) on axes 2 and 3; three 34 mm (26 N·cm) on axes 4 to 6; printed gears, GT2 belts | [1][2] |
| Electronics | Arduino Mega with Thor ControlPCB and 8 A4988 drivers, or a Fly Super8Pro board | [2] |
| Homing | 4 optical endstops and one micro endstop; no encoders listed | [2] |
| Filament | 3–4 kg PLA or PETG, 0.5 kg ABS; mass, reach, speed and repeatability not published | [2] |

## How it works

Seven NEMA 17 steppers drive six joints; three with 5:1 reductions share axes 2 and 3, and axes 5
and 6 share one printed assembly (`Art56`) [1][2][7]. The steppers run open loop, with optical
endstops for homing, and the BOM lists eleven 12 V fans [2].

The arm is a G-code machine. The Thor ControlPCB is a KiCad-designed Arduino Mega shield with eight
A4988 drivers; the Mega runs a GRBL 0.9j fork with Thor's step and speed settings, and the Fly
Super8Pro board runs RepRapFirmware instead [1][4][6]. Asgard, a desktop GUI, moves the motors [1].

Thor-ROS holds ROS 2 Humble and MoveIt 2 packages: a URDF, a `ros2_control` interface that sends
G-code over serial, joystick control, Gazebo and a React web Asgard [5]. No MuJoCo model was found.

## What it is used for

- Robotics courses in schools and universities, its stated purpose, and hobby builds [1][7].
- Learning MoveIt 2 motion planning on a real arm or in Gazebo [5].

## Cost and BOM

The FAQ puts the components at about **€350**, without the 3D printer [3]; with no exchange rate or
date, the frontmatter `cost` stays empty. The BOM links every part, mostly to AliExpress and
StepperOnline, without prices [2]. There is no official kit [3].

## Building it

**Difficulty 3:** about 200 hours of printing on a 200 x 200 mm bed, then about 10 hours of
assembly once you know the steps, plus soldering the ControlPCB, flashing GRBL from the Arduino IDE
and setting its parameters [3][4]. Files: FreeCAD, STEP and STL per part, improved `mods`, assembly
videos [1]. Pitfalls: the project takes weeks or months, prints often need redoing, and AliExpress
links sometimes switch products [2][3].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| CAD | FreeCAD, STEP, STL | [Thor](https://github.com/AngelLM/Thor) [1] | CC BY-SA 4.0 |
| Control board | KiCad, Gerbers, schematic PDF | [ThorControlPCB](https://github.com/AngelLM/ThorControlPCB) [6] | No licence file; the FAQ puts all project files under CC BY-SA 4.0 [3] |
| ROS 2 packages, Asgard web GUI | C++, Python, React | [Thor-ROS](https://github.com/AngelLM/Thor-ROS) [5] | CC BY-SA 4.0; `thor_urdf` package Apache-2.0 |
| Firmware | GRBL fork (Arduino) | [Downloads on the site](http://thor.angel-lm.com/) [4] | Not checked |
| Docs, BOM | Web pages, videos | [thor.angel-lm.com](http://thor.angel-lm.com/documentation/) [2] | CC BY-SA 4.0 [3] |

## Strengths and limits

- **Strengths:** every file open in editable FreeCAD and KiCad formats; cheap common parts; G-code
  control like a 3D printer; maintained ROS 2 and MoveIt 2 support; a forum and Discord [1][5].
- **Limits:** open-loop steppers with no encoders; no published mass, reach or repeatability; about
  200 h of printing; CC BY-SA, a share-alike licence, even on its ROS code [1][2][3][5].

## What to reuse

- Driving a robot arm as a G-code machine with 3D-printer or CNC firmware [4].
- A `ros2_control` interface over a G-code serial link, for any G-code arm [5].

## Related robots

- [BCN3D Moveo](bcn3d-moveo.md): another printed stepper arm moved with G-code.
- [SO-101](so-101.md) and [Koch v1.1](koch-v1-1.md): printed arms on feedback servos with LeRobot.
- [OpenManipulator-X](openmanipulator-x.md): a small commercial teaching arm on Dynamixel servos.

## Sources

1. [Thor repository README and licence](https://github.com/AngelLM/Thor), accessed 2026-11-18
2. [Thor bill of materials](http://thor.angel-lm.com/documentation/bom/), accessed 2026-11-18
3. [Thor frequently asked questions](http://thor.angel-lm.com/faq/), accessed 2026-11-18
4. [Thor firmware: installation and configuration](http://thor.angel-lm.com/documentation/firmware/), accessed 2026-11-18
5. [Thor-ROS README and packages](https://github.com/AngelLM/Thor-ROS), accessed 2026-11-18
6. [ThorControlPCB repository](https://github.com/AngelLM/ThorControlPCB), accessed 2026-11-18
7. [Thor on Hackaday.io (2016 Hackaday Prize entry)](https://hackaday.io/project/12989-thor), accessed 2026-11-18
