---
type: robot
name: JPL Open Source Rover
summary: Six-wheel rocker-bogie rover from NASA JPL built from goBILDA aluminium parts, a KiCad control board and a Raspberry Pi; a fully open, well-documented build for rough ground.
tags: [rocker-bogie, six-wheel, mars-rover, gobilda, raspberry-pi, roboclaw, ros2, kicad, onshape, outdoor]
category: mobile-base
tier: A
openness: full
maker: NASA Jet Propulsion Laboratory (JPL)
year: 2018
license: {hardware: Apache-2.0, software: Apache-2.0, docs: Apache-2.0}
links: {repo: https://github.com/nasa-jpl/open-source-rover, docs: https://open-source-rover.readthedocs.io, cad: https://cad.onshape.com/documents/e4f00b1a3d2edb1a84bbba1c/w/8ab8f394324bcc586236ef5d/e/9191e5ad2a70f387b419bc55, paper: , site: https://jplopensourcerover.com/}
specs: {dof: 10, payload_kg: , reach_mm: , mass_kg: , size_mm: , speed_mps: 1.6, runtime_h: 3}
stack: {actuators: 6 goBILDA 5203 Yellow Jacket planetary gear motors (223 rpm with encoders) and 4 goBILDA 2000-series dual-mode servos for steering, mcu: 3 RoboClaw 2x7A motor controllers and a PCA9685 servo driver on the custom control board, compute: "Raspberry Pi 3, 4 or 5", sensors: [drive motor encoders, INA260 current and voltage monitor], sim_models: [URDF/xacro (osr-rover-code repo osr_gazebo package)], ros2: official}
cost: {type: bom, usd: 1421.18, as_of: 2026-11-17, source: https://github.com/nasa-jpl/open-source-rover/blob/master/parts_list/README.md}
build: {difficulty: 3, hours: 100, print_hours: }
maturity: {last_commit: 2026-11-06, stars: 9787, active: true}
use_cases: [education, hobby, research, teleop, navigation]
evidence: researched
last_verified: 2026-11-17
sources:
  - {url: https://github.com/nasa-jpl/open-source-rover, title: "JPL Open Source Rover repository README", accessed: 2026-11-17}
  - {url: https://github.com/nasa-jpl/open-source-rover/blob/master/parts_list/README.md, title: "OSR parts list", accessed: 2026-11-17}
  - {url: https://github.com/nasa-jpl/open-source-rover/blob/master/electrical/pcb/README.md, title: "OSR control board assembly v2.0.3", accessed: 2026-11-17}
  - {url: https://github.com/nasa-jpl/open-source-rover/blob/master/electrical/wiring/README.md, title: "OSR wiring guide", accessed: 2026-11-17}
  - {url: https://github.com/nasa-jpl/open-source-rover/blob/master/mechanical/README.md, title: "OSR mechanical overview", accessed: 2026-11-17}
  - {url: https://github.com/nasa-jpl/open-source-rover/blob/master/mechanical/wheel_assembly/README.md, title: "OSR wheel assembly guide", accessed: 2026-11-17}
  - {url: https://github.com/nasa-jpl/open-source-rover/blob/master/mechanical/servo_gear_replacement/README.md, title: "OSR servo gear replacement guide", accessed: 2026-11-17}
  - {url: https://github.com/nasa-jpl/open-source-rover/blob/master/mechanical/body/laser_cut_parts/README.md, title: "OSR laser-cut body plates", accessed: 2026-11-17}
  - {url: https://github.com/nasa-jpl/osr-rover-code, title: "OSR rover code repository README", accessed: 2026-11-17}
  - {url: https://github.com/nasa-jpl/osr-rover-code/blob/master/ROS/README.md, title: "OSR rover code: ROS overview", accessed: 2026-11-17}
  - {url: https://github.com/nasa-jpl/osr-rover-code/blob/master/ROS/osr_gazebo/README.md, title: "OSR rover code: Gazebo simulation package", accessed: 2026-11-17}
  - {url: https://github.com/nasa-jpl/osr-rover-code/blob/master/setup/rpi.md, title: "OSR rover code: Raspberry Pi setup", accessed: 2026-11-17}
  - {url: https://github.com/nasa-jpl/osr-rover-code/blob/master/setup/rover_bringup.md, title: "OSR rover code: rover bringup and servo calibration", accessed: 2026-11-17}
  - {url: https://certification.oshwa.org/us002551.html, title: "OSHWA certification US002551", accessed: 2026-11-17}
  - {url: https://techcrunch.com/2018/08/01/nasas-open-source-rover-lets-you-build-your-own-planetary-exploration-platform/, title: "TechCrunch: NASA's Open Source Rover (2018)", accessed: 2026-11-17}
  - {url: https://github.com/nasa-jpl/open-source-rover/blob/master/examples/README.md, title: "OSR builders' gallery", accessed: 2026-11-17}
  - {url: https://github.com/nasa-jpl/open-source-rover/blob/master/expansion/mast/README.md, title: "OSR mast expansion", accessed: 2026-11-17}
  - {url: https://github.com/0xD0M1M0/ExoMy, title: "ExoMy repository (community-maintained successor of ESA's version)", accessed: 2026-11-17}
  - {url: https://github.com/nasa-jpl/osr-rover-code/blob/master/ROS/osr_control/osr_control/kinematics.py, title: "OSR rover code: kinematics module", accessed: 2026-11-17}
---

# JPL Open Source Rover

The JPL Open Source Rover (OSR) is a build-it-yourself, scaled-down six-wheel rover modelled on
the rocker-bogie design JPL uses on Mars [1].
NASA's Jet Propulsion Laboratory published it in 2018, and it now uses goBILDA aluminium parts, a
two-board KiCad control PCB and a Raspberry Pi running ROS 2 [1][3][9][15].
For a builder it is a complete open rover build: every part has a link and a price, the build steps
have photos, and the design is certified open hardware [2][3][14].

## Specs

| Item | Value | Source |
|---|---|---|
| Layout | Six wheels on a rocker-bogie suspension with a differential pivot; the four corner wheels steer | 1 |
| Actuators | 10 motors: 6 drive gear motors and 4 steering servos; DOF counted as 10 | 1, 2 |
| Drive motors | goBILDA 5203 Yellow Jacket planetary gear motor, 26.9:1, 223 rpm, with encoder | 2 |
| Steering servos | goBILDA 2000-series dual-mode servo (25-2 torque), about 300 degrees of travel | 2, 13 |
| Wheels | goBILDA Wasteland wheel, 144 mm diameter, 52 mm wide | 2 |
| Structure | Aluminium goBILDA channel and beams; laser-cut plates (acrylic, MDF or wood, about 3 mm) on the body | 1, 2 |
| Top speed | About 1.6 m/s, depending on the motors chosen (maker's claim) | 1 |
| Runtime | At least 3 h on a 7.2 Ah battery over rough ground (maker's claim); shuts down below 13 to 14 V | 1 |
| Battery | LiPo above 14 V (4S suggested), 4000 mAh or more recommended | 2 |
| Computer | Raspberry Pi 3, 4 or 5 | 2 |
| Mass, size, payload | Not stated for the current version | |

## How it works

### Mechanics and actuation

Each side has a rocker and a bogie that keep all six wheels on the ground while climbing over
obstacles [1]. A differential pivot links the two rockers through the body and shifts load from one
side to the other while climbing [1]. The four corner wheels have steering servos, which gives
six-wheel Ackermann steering [1]; the kinematics code also has a rotate-in-place mode [19]. Almost
every structural part is a stock goBILDA item, and the base rover needs no metal machining [1][2].
The Onshape model shows where each part goes; it omits many screws to stay light [5].

### Electronics and firmware

The control board is two stacked PCBs, version 2.0.3: a motor board with a brain board mounted on
top. The motor board takes battery power through XT30 connectors and a fuse [3]. Together the boards
carry three RoboClaw 2x7A motor controllers (two drive motors each), a PCA9685 PWM driver for the four
steering servos, an INA260 power monitor, Pololu 5 V and 12 V regulators, LM358 buffers for the
encoder signals and an LED bar display; the Raspberry Pi connects by ribbon cable [2][3]. The parts
are through-hole and soldered by hand. The KiCad project, schematic PDF, Gerbers and BOM files are in
the repository [3].

The rover has no microcontroller firmware of its own: the Raspberry Pi drives the RoboClaws over
serial and the PCA9685 and INA260 over I2C [10]. Only the Raspberry Pi 5 has two full serial ports, so
it is the only model that can talk to the RoboClaws and use Bluetooth at the same time [2].

### Software and control

The code lives in a separate repository, `osr-rover-code` (Apache-2.0) [9]. It is ROS 2 and Python.
The README says it was tested on Foxy, and the Raspberry Pi guide installs Jazzy on Ubuntu; the
authors say the code should not depend on the ROS 2 version [9][12]. Its packages:

- `osr_control`: the `rover` node turns `/cmd_vel` into wheel speeds and corner angles with
  rocker-bogie inverse kinematics; other nodes wrap the RoboClaw library, drive the servos through
  the PCA9685 and publish the INA260 readings [10].
- `osr_interfaces`: custom drive, corner and status messages [10].
- `osr_bringup`: launch files and parameters, including rover dimensions and wheel radius [10].

A USB gamepad (Xbox-style or a Spektrum transmitter with a USB dongle) drives it by hand [2][13].
The servos must be calibrated once: a script finds the centre pulse width for each corner [13].

### Simulation

`osr_gazebo` holds a URDF/xacro model and a Gazebo Classic world. The simulated rover runs the same
kinematics code and reads the same dimension file as the hardware [11]. It still needs ROS 2 Humble
with Gazebo Classic 11 (not Jazzy), and it is excluded from the default build; a Dockerfile runs it
without a local install [9][11].

## What it is used for

- **Education:** JPL describes it as a teaching project for mechanical, electrical and software
  skills, needing no prior knowledge [1].
- **Rough-terrain research platform:** the README calls it suitable for research on rugged ground;
  the Pi leaves room for added sensors [1].
- **Community builds:** the builders' gallery shows over a dozen rovers; several add depth cameras
  with RTAB-Map, lidar SLAM, Nav2 or a robot arm, and one was used for coastal terrain surveys [16].
- **Expansions:** a documented pan-and-tilt mast for a camera, light or screen [17].

## Cost and BOM

The parts list links every item to its seller and is generated from two CSV files [2].

| Item | Cost (USD) | Type | Source |
|---|---|---|---|
| Parts list total (goBILDA mechanics plus Digi-Key electronics), no shipping, no education discount | 1,421.18 | bom | 2 |
| Six drive wheel assemblies | 527.70 | bom | 2 |
| Two rocker-bogie assemblies | 423.83 | bom | 2 |
| Body assembly | 253.67 | bom | 2 |
| Electrical parts from Digi-Key | 90.80 | bom | 2 |
| Extra parts not in the total (RoboClaws, Pi, battery, charger, PCBs, plates, wiring), project's estimate | about 500 | bom | 2 |

- Prices were read on 2026-11-17 from the parts list in the repository; goBILDA may change prices
  without notice [2].
- The README headline says about $1,600 total; the parts list plus its own estimate for extras comes
  to about $1,900 (our sum) [1][2].
- Educational builders can apply for a 15% goBILDA discount [1].
- Option: Traxxas wheels cost about $135 less than the default wheels but need drilling [2].
- At launch in 2018, JPL's estimate was about $2,500 [15].
- No kit is sold by JPL. PCBs are ordered from a fab such as JLCPCB (minimum 10), or shared through
  the community Slack [2].

## Building it

**Difficulty 3:** hand soldering of two through-hole PCBs, crimping many connectors, ordering
laser-cut plates, servo calibration and Pi setup; no machining, but a long build [1][3][4].

- Time: JPL says no less than 100 person-hours, more for beginners [1]. The wiring harness alone takes
  2 to 5 hours [4].
- Mandatory tools: metric hex keys, pliers, wire snips and strippers, soldering iron and a
  multimeter. A 3D printer, laser cutter and bench supply are optional [1].
- Build order: order parts, make the wiring, assemble and test the PCBs, build the mechanical
  subassemblies, then set up the software [1].

Pitfalls the docs mention:

- Hard crashes can shear the corner servo's gear shaft; goBILDA sells replacement gear sets [7].
- The Onshape model shows the corner wheel brackets facing the wrong way on one side; build the
  wheel assemblies as mirror images [6].
- Protect cables from sharp aluminium edges with sleeves or grommets [2].
- Use thread locker so screws do not loosen while driving [2].
- Do not over-discharge the LiPo battery [1].
- Parts go out of stock; the maintainers update the CSV lists when they do [2].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Rover CAD | Onshape (exports STEP) | [Onshape model](https://cad.onshape.com/documents/e4f00b1a3d2edb1a84bbba1c/w/8ab8f394324bcc586236ef5d/e/9191e5ad2a70f387b419bc55) [1] | Apache-2.0 (repository licence) |
| Body plates | DXF, SVG, PDF for engraving | `mechanical/body/laser_cut_parts/` [8] | Apache-2.0 |
| Control board | KiCad project, schematic PDF, Gerbers, STEP models of parts | `electrical/pcb/control_board/` [3] | Apache-2.0 |
| Wiring harnesses | WireViz YAML | `electrical/wiring/wireviz/` [4] | Apache-2.0 |
| BOM | CSV and Markdown, Digi-Key cart file | `parts_list/` [2] | Apache-2.0 |
| Software | ROS 2 Python packages | [osr-rover-code](https://github.com/nasa-jpl/osr-rover-code) [9] | Apache-2.0 |
| Robot model | URDF/xacro | `osr_gazebo` in osr-rover-code [11] | Apache-2.0 |
| Docs | Markdown, built with MkDocs | [open-source-rover.readthedocs.io](https://open-source-rover.readthedocs.io) [1] | Apache-2.0 |

The project is OSHWA-certified (US002551, October 2023). The certificate lists the hardware and
documentation licences as "Other" and the software as Apache, while the repository itself is
Apache-2.0 throughout [1][14].

## Strengths and limits

**Strengths**

- Fully open with a permissive licence and OSHWA certification [1][14].
- Off-the-shelf mechanics: no printing or machining for the base rover [1].
- Detailed docs with photos, harness diagrams and a priced parts list [2][3][4].
- Real rough-terrain mobility from the rocker-bogie and differential [1].
- Maintained, with a large builder community on Slack [1][16].

**Limits**

- Long build: 100 person-hours or more [1].
- Costly for a hobby robot: about $1,900 with extras (our sum from the parts list) [2].
- No sensors for autonomy in the base build; cameras and lidar are left to the builder [1].
- Simulation lags the hardware stack: Gazebo Classic on Humble only [11].
- Tied to the goBILDA catalogue; builders outside the US should check its shipping first [1].
- Mass and size are not published for the current version.

## What to reuse

- **Rocker-bogie with a differential pivot:** the reference design for keeping six wheels on uneven
  ground, built from stock channel [1].
- **Kinematics shared by sim and hardware:** one pure-Python kinematics module and one dimension file
  feed both the real rover and Gazebo [11].
- **Generated parts list:** CSV files compile into the Markdown BOM and a Digi-Key cart, so prices and
  links stay in one place [2].
- **WireViz harness drawings:** cables defined as YAML and drawn automatically [4].
- **Off-the-shelf motor controllers on a carrier PCB:** RoboClaws and a PCA9685 plug into one board
  instead of a custom motor driver [3].

## Related robots

- [TurtleBot3](turtlebot3.md): a smaller indoor ROS 2 base.
- [F1TENTH](f1tenth.md): a fast wheeled ROS 2 platform for flat tracks.
- ESA's ExoMy is a smaller, 3D-printed Mars rover in the same spirit (GPL-3.0); the OSR README lists
  it with Sawppy as cheaper alternatives [1][18].

## Sources

1. [JPL Open Source Rover repository README](https://github.com/nasa-jpl/open-source-rover), accessed 2026-11-17
2. [OSR parts list](https://github.com/nasa-jpl/open-source-rover/blob/master/parts_list/README.md), accessed 2026-11-17
3. [OSR control board assembly v2.0.3](https://github.com/nasa-jpl/open-source-rover/blob/master/electrical/pcb/README.md), accessed 2026-11-17
4. [OSR wiring guide](https://github.com/nasa-jpl/open-source-rover/blob/master/electrical/wiring/README.md), accessed 2026-11-17
5. [OSR mechanical overview](https://github.com/nasa-jpl/open-source-rover/blob/master/mechanical/README.md), accessed 2026-11-17
6. [OSR wheel assembly guide](https://github.com/nasa-jpl/open-source-rover/blob/master/mechanical/wheel_assembly/README.md), accessed 2026-11-17
7. [OSR servo gear replacement guide](https://github.com/nasa-jpl/open-source-rover/blob/master/mechanical/servo_gear_replacement/README.md), accessed 2026-11-17
8. [OSR laser-cut body plates](https://github.com/nasa-jpl/open-source-rover/blob/master/mechanical/body/laser_cut_parts/README.md), accessed 2026-11-17
9. [OSR rover code repository README](https://github.com/nasa-jpl/osr-rover-code), accessed 2026-11-17
10. [OSR rover code: ROS overview](https://github.com/nasa-jpl/osr-rover-code/blob/master/ROS/README.md), accessed 2026-11-17
11. [OSR rover code: Gazebo simulation package](https://github.com/nasa-jpl/osr-rover-code/blob/master/ROS/osr_gazebo/README.md), accessed 2026-11-17
12. [OSR rover code: Raspberry Pi setup](https://github.com/nasa-jpl/osr-rover-code/blob/master/setup/rpi.md), accessed 2026-11-17
13. [OSR rover code: rover bringup and servo calibration](https://github.com/nasa-jpl/osr-rover-code/blob/master/setup/rover_bringup.md), accessed 2026-11-17
14. [OSHWA certification US002551](https://certification.oshwa.org/us002551.html), accessed 2026-11-17
15. [TechCrunch: NASA's Open Source Rover (2018)](https://techcrunch.com/2018/08/01/nasas-open-source-rover-lets-you-build-your-own-planetary-exploration-platform/), accessed 2026-11-17
16. [OSR builders' gallery](https://github.com/nasa-jpl/open-source-rover/blob/master/examples/README.md), accessed 2026-11-17
17. [OSR mast expansion](https://github.com/nasa-jpl/open-source-rover/blob/master/expansion/mast/README.md), accessed 2026-11-17
18. [ExoMy repository (community-maintained successor of ESA's version)](https://github.com/0xD0M1M0/ExoMy), accessed 2026-11-17
19. [OSR rover code: kinematics module](https://github.com/nasa-jpl/osr-rover-code/blob/master/ROS/osr_control/osr_control/kinematics.py), accessed 2026-11-17
