---
type: robot
name: Robot Soccer Kit (RSK)
summary: A small three-omniwheel robot with a solenoid kicker, located by an overhead camera, for teaching coordinates, control and soccer strategy in Python; non-commercial licence.
tags: [omniwheel, holonomic, esp32, kicker, aruco, overhead-camera, robocup, python, education]
category: mobile-base
tier: A
openness: full
maker: Rhoban team (LaBRI, University of Bordeaux)
year: 2022
license: {hardware: CC-BY-NC-2.0, software: CC-BY-NC-2.0, docs: CC-BY-NC-2.0}
links: {repo: https://github.com/robot-soccer-kit/robot-soccer-kit, docs: https://robot-soccer-kit.github.io/, cad: https://cad.onshape.com/documents/81e7adfaf4d8d74f2936fbd5/w/97141f458dee8c3b80cbf3d2/e/5e1ff591ff562de3da8ed2af, paper: https://arxiv.org/abs/2510.11552, site: https://robot-soccer-kit.github.io/}
specs: {dof: 3, payload_kg: , reach_mm: , mass_kg: , size_mm: , speed_mps: 0.2, runtime_h: }
stack: {actuators: "3x GA12-N20 gearmotors (6 V, 1:100) with Hall encoders, plus a JF-0530B solenoid kicker", mcu: ESP32-WROOM-32E on a custom board, compute: host PC running the Python game controller, sensors: [GA12-N20 Hall wheel encoders, battery voltage sense, overhead USB camera with ArUco markers (off-board)], sim_models: ["MJCF (MuJoCo Menagerie)", "URDF (Rhoban/onshape-to-robot-examples)", "2D simulator (rsk game controller)"], ros2: none}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: 3, hours: , print_hours: }
maturity: {last_commit: 2026-05-28, stars: 49, active: true}
use_cases: [education, competition, navigation]
evidence: researched
last_verified: 2026-11-17
sources:
  - {url: https://github.com/robot-soccer-kit/robot-soccer-kit, title: Robot Soccer Kit repository README and licence, accessed: 2026-11-17}
  - {url: https://robot-soccer-kit.github.io/, title: Robot Soccer Kit documentation, accessed: 2026-11-17}
  - {url: https://robot-soccer-kit.github.io/hardware-robots, title: RSK robot hardware, accessed: 2026-11-17}
  - {url: https://robot-soccer-kit.github.io/electronics, title: RSK electronics, accessed: 2026-11-17}
  - {url: https://robot-soccer-kit.github.io/hardware-setup, title: RSK field setup hardware, accessed: 2026-11-17}
  - {url: https://arxiv.org/abs/2510.11552, title: "Robot Soccer Kit: Omniwheel Tracked Soccer Robots for Education (ICARSC 2022)", accessed: 2026-11-17}
  - {url: https://github.com/robot-soccer-kit/robot-soccer-kit/blob/master/firmware/src/config.h, title: RSK firmware configuration, accessed: 2026-11-17}
  - {url: https://github.com/robot-soccer-kit/robot-soccer-kit/blob/master/rsk/constants.py, title: RSK game controller constants, accessed: 2026-11-17}
  - {url: https://github.com/robot-soccer-kit/robot-soccer-kit/blob/master/pyproject.toml, title: RSK Python package metadata, accessed: 2026-11-17}
  - {url: https://github.com/robot-soccer-kit/robot-soccer-kit/tree/master/electronics/rev3, title: RSK mainboard rev3 files and BOM, accessed: 2026-11-17}
  - {url: https://pypi.org/project/robot-soccer-kit/, title: robot-soccer-kit on PyPI, accessed: 2026-11-17}
  - {url: https://github.com/google-deepmind/mujoco_menagerie/tree/main/robot_soccer_kit, title: MuJoCo Menagerie Robot Soccer Kit model, accessed: 2026-11-17}
  - {url: https://github.com/Rhoban/onshape-to-robot-examples/tree/master/rsk_urdf, title: Rhoban onshape-to-robot RSK URDF example, accessed: 2026-11-17}
  - {url: https://github.com/robot-descriptions/awesome-robot-descriptions, title: awesome-robot-descriptions, accessed: 2026-11-17}
  - {url: https://ent2d.ac-bordeaux.fr/disciplines/sti-college/2024/10/24/concours-robot-soccer-kit/2/, title: Académie de Bordeaux Robot Soccer Kit competition, accessed: 2026-11-17}
  - {url: https://github.com/robot-soccer-kit/robot-soccer-kit/issues, title: RSK issue tracker, accessed: 2026-11-17}
  - {url: https://robot-soccer-kit.github.io/assembly, title: RSK assembly instructions, accessed: 2026-11-17}
  - {url: https://www.proceedings.com/64195.html, title: ICARSC 2022 proceedings listing, accessed: 2026-11-17}
---

# Robot Soccer Kit (RSK)

RSK is a small holonomic robot on three printed omniwheels, with a solenoid kicker and an ESP32 board, plus an overhead camera that tracks every robot and the ball.
It comes from the Rhoban team at LaBRI, University of Bordeaux; the paper's authors are Grégoire Passault, Clément Gaspard and Olivier Ly [6][9].
A builder gets a complete classroom setup where students program robots by field coordinates in Python, but the whole repo is under a non-commercial licence.

The robot carries no camera or range sensor. A fixed camera above the field reads an ArUco marker on each robot, and a Python "game controller" on a PC sends speed and kick commands over the radio [6]. This is a pocket version of the RoboCup Small Size League idea, aimed at school students [6].

## Specs

| Item | Value | Source |
|---|---|---|
| Drive | 3 omniwheels, holonomic | [2][6] |
| Actuated joints (dof) | 3: one gearmotor per wheel (the kicker solenoid is not counted) | [3] |
| Motors | GA12-N20, 6 V, 1:100, Hall encoders with 7 CPR | [3] |
| Wheels | Printed, 20 passive rollers each on V623ZZ bearings; 35 mm radius in the code | [3][6][8] |
| Wheel to centre | 59.5 mm (kinematics constant) | [7][8] |
| Height | 76 mm (game controller constant) | [8] |
| Mass | Not published; the built-in simulator assumes 0.71 kg | [8] |
| Top speed | 0.2 m/s translation, 180 deg/s rotation (2022 paper) | [6] |
| Kicker | MT3608 boost to 20 V into two 2200 µF capacitors, dumped into a JF-0530B solenoid; pulse capped at 5 ms | [3][4][6] |
| Kick | Ball leaves at about 1 m/s and travels 80% of the field length (maker's claim) | [6] |
| Battery | 2x 18650 Li-ion (2S) with an on-board protection IC | [3][4] |
| Controller | ESP32-WROOM-32E-N8, FT232RL USB-serial | [4][10] |
| Radio | Bluetooth in the 2022 paper; current firmware also speaks Wi-Fi (UDP) | [6][7] |
| Field | 1.84 x 1.23 m playing area on a 2.45 x 1.84 m carpet (code); camera about 2 m up | [6][8] |
| Tracking | 30 Hz at 1280 x 720, about 3 mm per pixel on an Intel i7-7820HQ laptop | [6] |
| Runtime | Not published | |

## How it works

### Mechanics and actuation

The frame is two plates of 3 mm MDF or PMMA, cut from DXF files and held apart by M3 spacers [3]. Three GA12-N20 motors sit in printed motor boxes at 120 degrees [3][7]. Each omniwheel is printed in two halves around 20 small rollers on V623ZZ bearings, so a robot uses 60 bearings [3][6]. Wheels and motor boxes print on a filament printer, or as one SLS "stack" file [3]. The kicker tip is laser-cut or CNC-cut from MDF or PMMA [3].

### Electronics and firmware

One custom mainboard carries everything [4][10]:
- an ESP32-WROOM-32E module with Bluetooth and Wi-Fi;
- three Toshiba TB67H450FNG H-bridges with built-in current limiting;
- the kicker boost converter, capacitors and MOSFET;
- a 2S battery protection IC, a 5 V switching regulator and a 3.3 V LDO;
- six WS2812B RGB LEDs, a buzzer and an FT232RL for USB flashing.

The board is designed in Eagle and has gone through four revisions (rev0 to rev3) [10]. The firmware is Arduino C++ built with PlatformIO [4]. It runs the inverse kinematics on the robot, so the PC sends chassis speeds rather than wheel speeds, and it closes the wheel speed loop on the encoders at 1 kHz [6][7]. It warns of a low battery with red LEDs and beeps [4].

### Software and control

The `robot-soccer-kit` Python package (on PyPI since February 2022) provides the game controller: camera detection with OpenCV ArUco, a web interface, a referee, and the link to the robots [9][11]. Clients connect over the network and get robot and ball positions in metres and radians in the field frame [6]. They can send chassis speeds and kick orders, and call a `goto` helper that drives a robot to a pose [6]. The game controller enforces rules itself, such as penalising a robot that stays too long near the ball, and it can log games for replay [6][8]. The `bluetooth/` folder holds pairing scripts and a driver for an RTL8761B USB dongle [1].

There is no ROS or ROS 2 integration.

### Simulation

- **Built-in:** the game controller has a `--simulated` mode with simple 2D physics, using the mass and acceleration constants in the code [1][8].
- **MJCF:** MuJoCo Menagerie has a model converted from the Onshape assembly with onshape-to-robot. Each wheel's 20 rollers are passive joints. The Menagerie README warns that no system identification was done [12].
- **URDF:** Rhoban's onshape-to-robot examples include an RSK URDF and MuJoCo XML [13].

## What it is used for

- **School teaching:** the paper sets out exercises that build to a playing robot: `atan2` and quadrants, angle wrapping, proportional control, frame changes, predicting where a rolling ball stops, and calibrating kick strength from logs [6].
- **A regional study:** in 2022 the team gave kits to teachers in 10 high schools with the Nouvelle-Aquitaine education authority, to study learning and the effect of competition [6].
- **Competitions:** the Académie de Bordeaux runs an RSK tournament within its RoboCupJunior event. For 2024 to 2025, 8 schools and 12 teams registered, and the tournament was held on 10 April 2025 [15].
- **Non-soccer scenarios:** the field graphics are cosmetic, so the same setup can model a warehouse or a restaurant with obstacle markers [6].

## Cost and BOM

- **Whole setup:** the 2022 paper puts the total price at about $1,250 for the setup, with a 2.5 x 2 m footprint and the camera 2 m up [6]. It does not break this down or say how many robots it includes, dated to the ICARSC conference on 29 to 30 April 2022 [18]. Because it is not a per-robot price, the frontmatter cost is left empty.
- **Mainboard BOM:** `BOM.xlsx` for rev2 and rev3 lists every part with manufacturer part numbers, but no prices [10].
- **Mechanical parts:** listed on the hardware page, also without prices: 3 motors, 60 V623ZZ bearings, optional O-rings, M3 screws and spacers, 2x 18650 cells and holder [3].
- **Field:** a thick green carpet of about 2 x 2.5 m, a Spedal MF920Pro webcam (1080p, 120 degrees), a 3 m USB extension, a photo background stand (about $40 on Amazon per the docs), and a TP-Link Archer C6 router [5].
- **Kits:** none for sale were found. The non-commercial licence means a third party cannot sell kits without the authors' permission.

## Building it

**Difficulty 3:** an SMD mainboard best ordered assembled, laser-cut plates, 60 bearings in printed wheels, and PlatformIO flashing.

- **Mainboard:** order rev2 or rev3 from the Gerber and centroid files with SMT assembly [4][10].
- **Cutting and printing:** laser-cut the frame, markers and kicker tip from the DXF files. Print the wheels and motor boxes, or order the SLS stack [3]. No print time is stated.
- **Firmware:** run `pio run -t upload` in `firmware/`, after editing `src/config.h` for the board revision and the Wi-Fi network [4][7].
- **Instructions:** the full assembly manual is in French; the English one is marked "coming soon" [17].
- **Pitfalls in open issues** [16]:
  - R19 to R21 do not match the BOM (#87);
  - a flyback diode is missing from the BOM (#105);
  - a diode is needed between VM and Q7 (#93);
  - robots sometimes reset while pairing (#86);
  - the wheel sits too far from the motor bearing (#79), and a counter-axis support is planned to limit radial load (#108).

The rev3 BOM already lists a kicker freewheel diode, which may answer #105 [10].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Full robot assembly | Onshape (public document) | Onshape link on the hardware page | CC BY-NC 2.0 (repo licence; non-commercial) |
| Printed parts | STL (wheels, motor boxes, coupler, battery blocker, SLS stack) | `mechanics/` | CC BY-NC 2.0 |
| Frame, markers, kicker tip | DXF; STEP for one kicker tip part | `mechanics/` | CC BY-NC 2.0 |
| Mainboard rev0 to rev3 | Eagle `.sch` and `.brd`, Gerbers, centroids, BOM, schematic PDF | `electronics/` | CC BY-NC 2.0 |
| Firmware | Arduino C++ with PlatformIO | `firmware/` | CC BY-NC 2.0 |
| Game controller and client | Python package with web UI | `rsk/`, PyPI | CC BY-NC 2.0 |
| Field and marker prints | PDF | `docs/` | CC BY-NC 2.0 |
| MJCF model | MJCF with meshes | MuJoCo Menagerie | MIT |
| URDF model | URDF with MuJoCo XML | Rhoban/onshape-to-robot-examples | MIT per awesome-robot-descriptions; no licence seen on the repo page |

Sources: [1][3][4][12][13][14]. Creative Commons Attribution-NonCommercial 2.0 covers the hardware, the firmware and the software alike. It forbids commercial use, and a Creative Commons licence on code leaves software-specific terms unclear.

## Strengths and limits

**Strengths**
- The overhead camera gives students true field coordinates, so they can work on navigation and strategy without SLAM.
- Holonomic drive makes motion maths direct: a chassis speed vector and a turn rate.
- A complete, tested system: robots, tracking, referee, game rules and replays in one package.
- Real use in schools and a regional competition; the software is still released regularly (PyPI 2.6.1, May 2026) [11].
- Ready simulation models in MuJoCo Menagerie.

**Limits**
- Non-commercial licence on everything in the repo, code included.
- Needs the field setup (camera, stand, carpet, router) to be useful; the robot alone has no perception.
- Slow: 0.2 m/s in the 2022 paper, limited by the 1:100 gearing [3][6].
- No runtime figure, no per-robot cost, and the BOM has no prices.
- English build instructions are not finished, and several open issues are about BOM and PCB fixes.
- No ROS 2.

## What to reuse

- **External tracking:** one overhead camera with ArUco markers replaces onboard localisation for teaching and multi-robot work [6].
- **Kinematics on the robot:** accept chassis velocities over the radio and do inverse kinematics in firmware [6].
- **A central controller:** route every command through one process that can pre-empt robots, enforce rules and log for replay [6].
- **Printed omniwheels:** two printed halves with 20 bearing-mounted rollers make a cheap omniwheel [3][6].
- **Safe kicker:** a small boost converter charging capacitors through a current-limiting resistor, with a capped pulse length [4][6].

## Related robots

- [Microban](microban.md): a small humanoid from the same Rhoban group.
- [OpenBot](openbot.md): another low-cost teaching robot whose brain sits off the chassis, in a phone.
- [TurtleBot3](turtlebot3.md): a ROS 2 teaching base with onboard lidar, for comparison.
- RoboCup Small Size League robots: the full-size, research version of this design.

## Sources

1. [Robot Soccer Kit repository README and licence](https://github.com/robot-soccer-kit/robot-soccer-kit), accessed 2026-11-17
2. [Robot Soccer Kit documentation](https://robot-soccer-kit.github.io/), accessed 2026-11-17
3. [RSK robot hardware](https://robot-soccer-kit.github.io/hardware-robots), accessed 2026-11-17
4. [RSK electronics](https://robot-soccer-kit.github.io/electronics), accessed 2026-11-17
5. [RSK field setup hardware](https://robot-soccer-kit.github.io/hardware-setup), accessed 2026-11-17
6. [Robot Soccer Kit: Omniwheel Tracked Soccer Robots for Education (ICARSC 2022)](https://arxiv.org/abs/2510.11552), accessed 2026-11-17
7. [RSK firmware configuration](https://github.com/robot-soccer-kit/robot-soccer-kit/blob/master/firmware/src/config.h), accessed 2026-11-17
8. [RSK game controller constants](https://github.com/robot-soccer-kit/robot-soccer-kit/blob/master/rsk/constants.py), accessed 2026-11-17
9. [RSK Python package metadata](https://github.com/robot-soccer-kit/robot-soccer-kit/blob/master/pyproject.toml), accessed 2026-11-17
10. [RSK mainboard rev3 files and BOM](https://github.com/robot-soccer-kit/robot-soccer-kit/tree/master/electronics/rev3), accessed 2026-11-17
11. [robot-soccer-kit on PyPI](https://pypi.org/project/robot-soccer-kit/), accessed 2026-11-17
12. [MuJoCo Menagerie Robot Soccer Kit model](https://github.com/google-deepmind/mujoco_menagerie/tree/main/robot_soccer_kit), accessed 2026-11-17
13. [Rhoban onshape-to-robot RSK URDF example](https://github.com/Rhoban/onshape-to-robot-examples/tree/master/rsk_urdf), accessed 2026-11-17
14. [awesome-robot-descriptions](https://github.com/robot-descriptions/awesome-robot-descriptions), accessed 2026-11-17
15. [Académie de Bordeaux Robot Soccer Kit competition](https://ent2d.ac-bordeaux.fr/disciplines/sti-college/2024/10/24/concours-robot-soccer-kit/2/), accessed 2026-11-17
16. [RSK issue tracker](https://github.com/robot-soccer-kit/robot-soccer-kit/issues), accessed 2026-11-17
17. [RSK assembly instructions](https://robot-soccer-kit.github.io/assembly), accessed 2026-11-17
18. [ICARSC 2022 proceedings listing](https://www.proceedings.com/64195.html), accessed 2026-11-17
