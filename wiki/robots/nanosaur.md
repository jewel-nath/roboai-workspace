---
type: robot
name: NanoSaur
summary: A palm-sized, fully printed tracked robot on an NVIDIA Jetson Nano for learning ROS 2 and Isaac ROS; its mecanum redesign runs in simulation only so far.
tags: [jetson, ros2, isaac-ros, tracked, 3d-printed, docker, oled-eyes, education]
category: mobile-base
tier: A
openness: full
maker: Raffaello Bonghi
year: 2020
license: {hardware: CC-BY-NC-SA-4.0, software: MIT, docs: CC-BY-NC-ND-4.0}
links: {repo: https://github.com/rnanosaur/nanosaur, docs: https://nanosaur.ai/docs/, cad: https://github.com/rnanosaur/nanosaur/tree/master/nanosaur_description/meshes, paper: , site: https://nanosaur.ai}
specs: {dof: 2, payload_kg: , reach_mm: , mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "2x Pololu micro metal gearmotors (6 V, 150 RPM)", mcu: none; the Jetson drives an Adafruit motor FeatherWing over I2C, compute: NVIDIA Jetson Nano developer kit (2 GB or 4 GB), sensors: [MIPI CSI camera (Raspberry Pi Camera v2 or Waveshare IMX219-160), optional depth camera (Stereolabs ZED mini or Intel RealSense D435i)], sim_models: ["URDF (rnanosaur/nanosaur, master branch, tracked v1)", "URDF (rnanosaur/nanosaur, nanosaur2 branch, mecanum redesign)"], ros2: official}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: 3, hours: , print_hours: 15}
maturity: {last_commit: 2026-06-19, stars: 276, active: true}
use_cases: [education, hobby, navigation]
evidence: researched
last_verified: 2026-11-17
sources:
  - {url: https://github.com/rnanosaur/nanosaur, title: NanoSaur repository README (nanosaur2 branch), accessed: 2026-11-17}
  - {url: https://github.com/rnanosaur/nanosaur/blob/nanosaur2/CHANGELOG.md, title: NanoSaur changelog, accessed: 2026-11-17}
  - {url: https://nanosaur.ai/, title: nanosaur.ai home page, accessed: 2026-11-17}
  - {url: https://nanosaur.ai/make/bill-of-materials/, title: NanoSaur bill of materials, accessed: 2026-11-17}
  - {url: https://nanosaur.ai/make/3d-print/, title: NanoSaur 3D print guide, accessed: 2026-11-17}
  - {url: https://nanosaur.ai/make/electronics/, title: NanoSaur electronics guide, accessed: 2026-11-17}
  - {url: https://nanosaur.ai/make/expansion-board/, title: NanoSaur expansion board guide, accessed: 2026-11-17}
  - {url: https://nanosaur.ai/make/assembly/, title: NanoSaur assembly guide, accessed: 2026-11-17}
  - {url: https://nanosaur.ai/license/, title: NanoSaur licence page, accessed: 2026-11-17}
  - {url: https://github.com/rnanosaur/nanosaur-exp-board, title: NanoSaur expansion board repository, accessed: 2026-11-17}
  - {url: https://github.com/rnanosaur/nanosaur/tree/nanosaur2/nanosaur_description/urdf, title: NanoSaur 2 URDF (nanosaur2 branch), accessed: 2026-11-17}
  - {url: https://github.com/rnanosaur/nanosaur/tree/master/nanosaur_description, title: NanoSaur v1 description package (master branch), accessed: 2026-11-17}
  - {url: https://nanosaur.ai/events/MFR2020/, title: NanoSaur at Maker Faire Rome 2020, accessed: 2026-11-17}
  - {url: https://nanosaur.ai/posts/, title: "NanoSaur posts, courses and press", accessed: 2026-11-17}
  - {url: https://github.com/rnanosaur/nanosaur/issues, title: NanoSaur issue tracker, accessed: 2026-11-17}
  - {url: https://nanosaur.ai/buy/, title: NanoSaur buy page, accessed: 2026-11-17}
---

# NanoSaur

NanoSaur is a small tracked robot with a printed body, two OLED "eyes" and an NVIDIA Jetson Nano as its only computer.
Raffaello Bonghi designed it as a one-person project and shows it as a way to learn ROS 2 and NVIDIA Isaac ROS.
A builder gets a cheap-to-print Jetson robot with a full ROS 2, Docker and simulation pipeline, but under a non-commercial hardware licence.

Two generations exist. The buildable one is the tracked v1 (releases 1.0.0 to 1.7.0, 2021 to 2022), which the build guide on nanosaur.ai describes [2][4]. The repo's default branch, `nanosaur2`, holds a redesign that, per its changelog, "works only in Simulation" [2]. This page covers v1 unless it says otherwise.

## Specs

| Item | Value | Source |
|---|---|---|
| Drive | Two printed TPU tracks, skid steering | [5][8] |
| Actuated joints (dof) | 2: one gearmotor per track | [4][8] |
| Motors | 2x Pololu micro metal gearmotor, 6 V, 150 RPM | [4] |
| Motor driver | Adafruit DC Motor + Stepper FeatherWing, on I2C | [4][7] |
| Compute | NVIDIA Jetson Nano developer kit, 2 GB or 4 GB | [4] |
| Displays | 2x 128 x 64 px I2C OLED | [4][6] |
| Camera | Raspberry Pi Camera v2 or Waveshare IMX219-160; ZED mini or RealSense D435i heads | [4] |
| Power | USB power bank; the holder fits packs up to 66 x 94 x 24 mm since v1.1.0 | [2][4] |
| Printed parts | 14 pieces from 10 files, about 15 h in total (maker's figure) | [5] |
| Mass, size, speed, runtime | Not published | |
| nanosaur2 model | Body 182 x 123 x 103 mm and 0.5 kg, four 37 mm mecanum wheels: URDF parameters, not measurements | [11] |

The master branch has a dimensioned drawing of v1 (`nanosaur-datasheet.pdf`, drawn 2020-12-09), but its dimensions are not labelled as overall length, width and height, so no size is given here [12].

## How it works

### Mechanics and actuation

The body is a printed front and rear base, a cover, a flap at the back and a head [5]. Each track runs on a printed sprocket and wheel with F686ZZ bearings, six in all [4][8]. The two Pololu gearmotors sit in the front base and drive the sprockets [8]. Magnets (4 x 2 mm) hold the power bank holder, the body and the head together, so parts come off without tools [4][8]. The head is swappable: there are covers for a fisheye camera, the Pi camera v2, a ZED mini and a RealSense [8].

### Electronics and firmware

There is no microcontroller. A small expansion board (20 x 80 mm, KiCad 5) plugs into the Jetson's 40-pin header [7][10]. It routes I2C bus 0 (pins 27, 28) to the right OLED and I2C bus 1 (pins 3, 5) to the left OLED and the Adafruit motor board. Two buttons use GPIO 31 and 33, and a slide switch turns the robot on [7]. The motors and the FeatherWing need soldering: XT connectors on the board and leads on the motors [6].

### Software and control

Everything runs in Docker on the Jetson. v1 started on ROS 2 Foxy in a container based on `dustynv/ros:foxy-ros-base-l4t-r32.5.0`, and needs JetPack 4.6 from release 1.4.1 [2]. Release 1.6.0 (2022) added Isaac ROS integration through a separate `nanosaur_perception` repo [2]. The current branch targets ROS 2 Humble, Isaac ROS release-3.2 and Isaac Sim 4.1 to 4.5 [1].

The ROS 2 packages are split by role: `nanosaur_description` (URDF), `nanosaur_control` (gamepad teleop and `twist_mux`), `nanosaur_msgs` (eye messages) and `nanosaur_visualization` in this repo, plus `nanosaur_robot`, `nanosaur_perception` and `nanosaur_simulation` in their own repos [1]. A `nanosaur` command-line tool, published on PyPI, installs the stack and manages the containers [1][2]. Docker Hub has images for the robot, for perception with RealSense or ZED, and for Gazebo and Isaac Sim [1].

### Simulation

The master branch has a URDF of the tracked v1 with meshes for each camera head [12]. The `nanosaur2` branch has a xacro URDF of the redesign, with optional LD06 lidar and RealSense D435 heads [11]. The `nanosaur_simulation` repo loads the URDF into Isaac Sim (4.5 since 2.0.0-pre0) or Gazebo [1][2]. Tutorials for both simulators date from August 2022 [14].

## What it is used for

- **Learning ROS 2 and Isaac ROS:** a five-part live class series (TCS 130 to 134) on building and programming NanoSaur ran in November 2021, and a hands-on Isaac ROS Visual SLAM session followed in June 2022 [14].
- **Simulation teaching:** a webinar on moving ROS robot simulations from Ignition Gazebo to Isaac Sim used it (July 2022) [14].
- **Hobby and outreach:** shown at Maker Faire Rome in 2020, 2021 and 2022 [13][14]. It won "Best ROS Robot 2022" from the ROS Developers community [3].

No research papers that use it were found.

## Cost and BOM

The bill of materials on nanosaur.ai (page updated 2025-02-21) prices most parts in USD with Amazon links [4]:

| Item | Qty | Listed price (USD) |
|---|---|---|
| Jetson Nano developer kit | 1 | not given |
| microSD card, 64 GB | 1 | 9.99 |
| 5 GHz Wi-Fi dongle | 1 | 13.90 |
| Power bank | 1 | 29.99 |
| Pololu micro gearmotor, 6 V 150 RPM | 2 | 25.75 |
| Adafruit DC Motor + Stepper FeatherWing | 1 | 29.10 |
| 128 x 64 I2C OLED | 2 | 5.00 |
| F686ZZ bearings | 6 | 7.49 |
| Magnets 4 x 2 mm | 10 | 10.99 |
| PLA (green, black) and TPU filament | 3 spools | 15 + 15 + 40 |
| M2 hex screw set | 1 | 10.00 |

The priced lines add up to $212.21. That is not a build cost: the page gives no price for the Jetson Nano, the camera or the expansion board, and does not say whether a price covers one unit or the whole line [4]. So the frontmatter cost is left empty. The expansion board is ordered from PCBWay, where the page says the first five boards are free plus shipping [4][7]. Optional extras are a Noctua 40 mm fan ($15) and a Logitech F710 gamepad ($31) [4]. No kit is sold: the buy page lists parts but no prices and says it is under construction [16].

## Building it

**Difficulty 3:** printing TPU tracks, soldering the motor board and the expansion board, and setting up the Jetson image.

- **Printing:** PLA at 0.2 mm layers, 15% infill, 50 mm/s; tracks in TPU at 30 mm/s with no supports and no retraction [5]. The guide calls the tracks the hardest part and recommends a direct-drive printer or a flexible TPU such as NinjaTek [5]. Its total is 15 h, though some part times on the page disagree with the table [5].
- **Tools:** a small slotted screwdriver and an M2 hex key; an electric screwdriver is optional [8].
- **Pitfalls in the guide:** check magnet orientation before gluing; solder the expansion board before closing the flap; mind cable polarity on the flap connectors; dry-fit screws after printing; print the 1/4 in variants if you use imperial bearings [8].
- **Pitfalls in issues:** Jetson model and JetPack version checks (#37, #59), an open question on running it on a Xavier NX (#95) and a camera fault (#34) [15].
- **Branch trap:** cloning the repo gives the `nanosaur2` branch. The v1 STL files and URDF live on the `master` branch (last commit 2025-01-27) and in the 1.x release tags [1][12].

No assembly time is stated; the guide only says the steps are quick [8].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| v1 body, tracks, covers | STL only (no source CAD) | `nanosaur_description/meshes` on `master`, and a release zip | CC BY-NC-SA 4.0 (non-commercial) |
| nanosaur2 body | STL | `nanosaur_description/meshes` on `nanosaur2` | CC BY-NC-SA 4.0 (non-commercial) |
| Expansion board | KiCad 5 source, Gerber, STEP, schematic PDF | rnanosaur/nanosaur-exp-board | CC BY-NC-SA 4.0 (non-commercial) |
| ROS 2 packages, Dockerfiles, CLI | Python, C++, YAML | rnanosaur/nanosaur and sibling repos | MIT |
| Robot models | URDF and xacro | both branches | MIT (meshes CC BY-NC-SA 4.0) |
| BOM and build guide | Web pages | nanosaur.ai/make | CC BY-NC-ND 4.0 (website) |

Sources: [1][7][9][10]. The hardware licence forbids commercial use, and the website licence also forbids derivatives.

## Strengths and limits

**Strengths**
- A real Jetson GPU on a robot small enough for a desk, with a complete ROS 2 and Isaac ROS stack.
- Docker images and a CLI hide most of the Jetson setup work.
- Swappable camera heads, from a fisheye to a RealSense.
- Simulation in both Gazebo and Isaac Sim from the same URDF.

**Limits**
- Hardware and website are non-commercial (NC); you cannot sell kits or printed parts without permission.
- The body is published as STL only, so changing it means remodelling.
- The documented build uses the original Jetson Nano; the current software branch targets Isaac ROS 3.2 and a redesign with a Jetson Orin Nano model, which is simulation-only [1][2][11].
- The v1 BOM has no wheel encoders, IMU or lidar; motion estimates come from the camera, as in the Isaac ROS visual odometry demos [4][14].
- No published mass, speed or runtime; the BOM has no total.
- Recent commits are mostly dependency bumps; the last feature release was 2.0.0-pre2 in February 2025 [2].

## What to reuse

- **Magnet-held panels and battery holder:** tool-free access without wear on printed screw threads.
- **No-MCU drive:** an I2C motor board driven straight from the Linux computer removes a firmware layer on small robots.
- **OLED eyes:** two cheap displays give the robot expression and a status readout.
- **Swappable sensor head:** one body, several camera covers.
- **Container split:** separate core, perception and simulation images keep heavy GPU dependencies out of the base image.

## Related robots

- [OpenBot](openbot.md): an even cheaper wheeled robot that uses a phone instead of a Jetson.
- [TurtleBot3](turtlebot3.md): the standard ROS 2 teaching base, larger and sold as a kit.
- [F1TENTH](f1tenth.md): another Jetson-based platform, for racing at speed.
- NVIDIA JetBot: a Jetson Nano wheeled robot for AI teaching, often compared with NanoSaur.

## Sources

1. [NanoSaur repository README (nanosaur2 branch)](https://github.com/rnanosaur/nanosaur), accessed 2026-11-17
2. [NanoSaur changelog](https://github.com/rnanosaur/nanosaur/blob/nanosaur2/CHANGELOG.md), accessed 2026-11-17
3. [nanosaur.ai home page](https://nanosaur.ai/), accessed 2026-11-17
4. [NanoSaur bill of materials](https://nanosaur.ai/make/bill-of-materials/), accessed 2026-11-17
5. [NanoSaur 3D print guide](https://nanosaur.ai/make/3d-print/), accessed 2026-11-17
6. [NanoSaur electronics guide](https://nanosaur.ai/make/electronics/), accessed 2026-11-17
7. [NanoSaur expansion board guide](https://nanosaur.ai/make/expansion-board/), accessed 2026-11-17
8. [NanoSaur assembly guide](https://nanosaur.ai/make/assembly/), accessed 2026-11-17
9. [NanoSaur licence page](https://nanosaur.ai/license/), accessed 2026-11-17
10. [NanoSaur expansion board repository](https://github.com/rnanosaur/nanosaur-exp-board), accessed 2026-11-17
11. [NanoSaur 2 URDF (nanosaur2 branch)](https://github.com/rnanosaur/nanosaur/tree/nanosaur2/nanosaur_description/urdf), accessed 2026-11-17
12. [NanoSaur v1 description package (master branch)](https://github.com/rnanosaur/nanosaur/tree/master/nanosaur_description), accessed 2026-11-17
13. [NanoSaur at Maker Faire Rome 2020](https://nanosaur.ai/events/MFR2020/), accessed 2026-11-17
14. [NanoSaur posts, courses and press](https://nanosaur.ai/posts/), accessed 2026-11-17
15. [NanoSaur issue tracker](https://github.com/rnanosaur/nanosaur/issues), accessed 2026-11-17
16. [NanoSaur buy page](https://nanosaur.ai/buy/), accessed 2026-11-17
