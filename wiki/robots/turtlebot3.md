---
type: robot
name: TurtleBot3
summary: Small modular ROS 2 robot from ROBOTIS with Onshape CAD and an open controller board; the standard kit for learning SLAM and navigation on real hardware.
tags: [ros2, differential-drive, dynamixel, opencr, raspberry-pi, lidar, slam, nav2, onshape, kit]
category: mobile-base
tier: A
openness: partial
maker: ROBOTIS
year: 2017
license: {hardware: , software: Apache-2.0, docs: CC-BY-4.0}
links: {repo: https://github.com/ROBOTIS-GIT/turtlebot3, docs: https://docs.robotis.com/docs/systems/turtlebot3/overview/, cad: https://cad.onshape.com/documents/2586c4659ef3e7078e91168b/w/14abf4cb615429a14a2732cc/e/9ae9841864e78c02c4966c5e, paper: , site: https://www.turtlebot.com/}
specs: {dof: 2, payload_kg: 15, reach_mm: , mass_kg: 1, size_mm: "138 x 178 x 192", speed_mps: 0.22, runtime_h: 2.5}
stack: {actuators: DYNAMIXEL XL430-W250 smart servos (Burger) or XM430-W210 (Waffle Pi), mcu: OpenCR1.0 (STM32F7 Cortex-M7), compute: Raspberry Pi 4, sensors: [LDS-03 360-degree 2D lidar, 3-axis gyroscope and accelerometer on OpenCR, Raspberry Pi Camera v2.1 (Waffle Pi only)], sim_models: [URDF (turtlebot3 repo), SDF for Gazebo Sim (turtlebot3_simulations repo)], ros2: official}
cost: {type: kit, usd: 783.50, as_of: 2026-11-17, source: https://robotis.us/products/turtlebot-3-burger-rpi4-4gb-us}
build: {difficulty: 1, hours: , print_hours: }
maturity: {last_commit: 2026-11-12, stars: 2107, active: true}
use_cases: [education, research, navigation, teleop, manipulation, reinforcement-learning, competition]
evidence: researched
last_verified: 2026-11-17
sources:
  - {url: https://github.com/ROBOTIS-GIT/turtlebot3, title: "TurtleBot3 repository README", accessed: 2026-11-17}
  - {url: https://emanual.robotis.com/docs/en/platform/turtlebot3/features/, title: "ROBOTIS e-Manual: TurtleBot3 features", accessed: 2026-11-17}
  - {url: https://docs.robotis.com/docs/systems/turtlebot3/features, title: "ROBOTIS Docs: TurtleBot3 features", accessed: 2026-11-17}
  - {url: https://docs.robotis.com/docs/systems/turtlebot3/overview/, title: "ROBOTIS Docs: TurtleBot3 overview", accessed: 2026-11-17}
  - {url: https://emanual.robotis.com/docs/en/platform/turtlebot3/opensource/, title: "ROBOTIS e-Manual: TurtleBot3 open source and licences", accessed: 2026-11-17}
  - {url: https://github.com/ROBOTIS-GIT/OpenCR-Hardware, title: "OpenCR-Hardware repository README", accessed: 2026-11-17}
  - {url: https://github.com/ROBOTIS-GIT/OpenCR, title: "OpenCR firmware repository", accessed: 2026-11-17}
  - {url: https://discourse.openrobotics.org/t/tb3-turtlebot3-hardware-free-for-you/1444, title: "Open Robotics Discourse: TurtleBot3 hardware on Onshape", accessed: 2026-11-17}
  - {url: https://robotis.us/products/turtlebot-3-burger-rpi4-4gb-us, title: "ROBOTIS US store: TurtleBot 3 Burger RPi4 4GB", accessed: 2026-11-17}
  - {url: https://robotis.us/products/turtlebot-3-waffle-pi-rpi4-4gb-us, title: "ROBOTIS US store: TurtleBot 3 Waffle Pi RPi4 4GB", accessed: 2026-11-17}
  - {url: "https://robotis.us/search?q=turtlebot3&type=product", title: "ROBOTIS US store: TurtleBot3 products and spare parts", accessed: 2026-11-17}
  - {url: https://robotis.us/products/dynamixel-xl430-w250-t, title: "ROBOTIS US store: DYNAMIXEL XL430-W250-T", accessed: 2026-11-17}
  - {url: https://docs.robotis.com/docs/systems/turtlebot3/more_info/lds_03, title: "ROBOTIS Docs: LDS-03 laser distance sensor", accessed: 2026-11-17}
  - {url: https://github.com/ROBOTIS-GIT/turtlebot3/blob/main/turtlebot3/CHANGELOG.rst, title: "turtlebot3 package changelog", accessed: 2026-11-17}
  - {url: https://github.com/ROBOTIS-GIT/turtlebot3/blob/main/turtlebot3_bringup/launch/robot.launch.py, title: "turtlebot3_bringup robot launch file", accessed: 2026-11-17}
  - {url: https://github.com/ROBOTIS-GIT/turtlebot3_simulations, title: "turtlebot3_simulations repository", accessed: 2026-11-17}
  - {url: https://emanual.robotis.com/docs/en/platform/turtlebot3/hardware_setup/, title: "ROBOTIS e-Manual: TurtleBot3 hardware assembly", accessed: 2026-11-17}
  - {url: https://emanual.robotis.com/docs/en/platform/turtlebot3/faq/, title: "ROBOTIS e-Manual: TurtleBot3 FAQ", accessed: 2026-11-17}
  - {url: https://spectrum.ieee.org/review-robotis-turtlebot-3, title: "IEEE Spectrum: TurtleBot 3 launch prices (2017)", accessed: 2026-11-17}
---

# TurtleBot3

TurtleBot3 is a small two-wheeled ROS 2 robot that ROBOTIS has made and sold since 2017, the third
generation of the TurtleBot line [4]. It combines DYNAMIXEL smart servos, a 360-degree lidar, an open
controller board (OpenCR) and a Raspberry Pi, and its chassis CAD is public on Onshape [2][8].
For a builder it is a standard robot for learning SLAM and navigation: small, documented end to end,
and kept current with ROS 2 releases [1][14].

## Specs

Two models are sold: Burger (small tower) and Waffle Pi (wide flat base). The frontmatter gives Burger values.

| Item | Value | Source |
|---|---|---|
| Models | Burger and Waffle Pi; the first Waffle is discontinued because its Intel Joule computer reached end of life | 2 |
| Drive | Differential drive, one DYNAMIXEL servo per wheel; DOF counted as 2 (the two wheels) | 2 |
| Max speed | Burger 0.22 m/s and 2.84 rad/s; Waffle Pi 0.26 m/s and 1.82 rad/s (maker's claim) | 2 |
| Max payload | Burger 15 kg; Waffle Pi 30 kg (maker's claim) | 2 |
| Size (L x W x H) | Burger 138 x 178 x 192 mm; Waffle Pi 281 x 306 x 141 mm | 2 |
| Mass (with computer, battery, sensors) | Burger 1 kg; Waffle Pi 1.8 kg | 2 |
| Runtime | Burger about 2.5 h; Waffle Pi about 2 h; charging about 2.5 h (maker's estimate) | 2 |
| Obstacles | Climbs thresholds of 10 mm or less | 2 |
| Battery | LiPo 11.1 V, 1800 mAh (19.98 Wh) | 2 |
| Wheel servos | Burger XL430-W250; Waffle Pi XM430-W210 | 2 |
| Controller | OpenCR1.0: 32-bit Cortex-M7 at 216 MHz, 3-axis gyro and accelerometer, 3 TTL and 3 RS485 DYNAMIXEL ports | 2 |
| Computer | Raspberry Pi 4 (standard since September 2021) | 2 |
| Lidar | LDS-03 since 2025: 0.05 to 12 m, 10 Hz, 0.9 degree steps. Older kits have LDS-01 or LDS-02 | 3, 13 |
| Camera | Raspberry Pi Camera Module v2.1 (Waffle Pi only) | 2 |

The LDS-03 start year differs between sources: the store and the LDS-03 page say 2025, the features
page says 2026 [3][9][13].

## How it works

### Mechanics and actuation

The frame is a stack of flat plastic plates ("waffle plates") joined by PCB supports, with a ball
caster; ROBOTIS sells each of these as spare parts [11]. Each wheel is driven by its own DYNAMIXEL
servo [2]. The robot node computes odometry from the servos' reported wheel positions, optionally
fused with the IMU heading, so there are no separate wheel encoders [1]. The same parts can be
rebuilt into other shapes: ROBOTIS publishes "TurtleBot3 Friends" designs such as a Segway-style
balancer, tank, omni-wheel, mecanum, bike and a mount for the OpenMANIPULATOR-X arm [5].

### Electronics and firmware

OpenCR1.0 is the low-level board. It uses an STM32F7 (Cortex-M7 with FPU), provides 3.3 V, 5 V and
12 V outputs, Arduino-style headers and DYNAMIXEL ports, and carries the IMU [2][6]. Its firmware is
an Arduino-based project in the OpenCR repository (Apache-2.0) [7]. You flash it from the Raspberry
Pi with a script that targets the Burger or Waffle model; holding SW2 while pressing reset enters a
setup mode for testing and configuring the servos [18]. The Raspberry Pi 4 talks to OpenCR over USB
and reads the lidar through a USB adapter (USB2LDS), which ships in the kit [2][9].

### Software and control

The `turtlebot3` repository holds the ROS 2 packages: bringup, the robot node, the URDF description,
Cartographer SLAM, Nav2 launch files and parameters, teleop and examples [1]. The `turtlebot3_node`
runs on the Pi. It uses the DYNAMIXEL SDK to read and write a control table on OpenCR, publishes
odometry, IMU, joint states and battery state, and takes velocity commands; since version 2.2.6 a
parameter chooses between `Twist` and `TwistStamped` [1][14]. The bringup reads an `LDS_MODEL`
environment variable to pick the lidar driver: LDS-01, LDS-02 or LDS-03 (the changelog calls the
last one the COIN D4) [14][15]. The repository carries parameter files and Docker images for both
ROS 2 Humble and Jazzy; release 2.3.7 is dated 2026-06-15 [1][14].

Sister repositories cover messages, simulation, the OpenMANIPULATOR-X arm, machine learning,
the AutoRace lane-following course and a home-service challenge [1].

### Simulation

- URDF models for Burger, Waffle and Waffle Pi are in `turtlebot3_description` [1].
- `turtlebot3_simulations` has SDF models and worlds (the TurtleBot3 world, a house and a DQN
  training arena) for Gazebo Sim through `ros_gz`, plus a "fake node" that runs the robot interface
  without physics [16].

## What it is used for

- **Learning ROS 2:** the ROBOTIS docs walk from teleop to SLAM, navigation and simulation on the
  same robot [4][17].
- **Mobile manipulation:** a Waffle Pi with an OpenMANIPULATOR-X arm, used in the home-service
  challenge [1][5].
- **Autonomous driving practice:** the AutoRace packages follow lanes and signs on a small track;
  ROBOTIS lists AutoRace events in its docs [1][17].
- **Reinforcement learning:** the `turtlebot3_machine_learning` repository trains navigation
  policies in simulation, using a dedicated training arena [1][16].

## Cost and BOM

TurtleBot3 is bought as a kit; ROBOTIS publishes no priced BOM. Prices from the ROBOTIS US store,
read on 2026-11-17:

| Item | Price (USD) | Type | Source |
|---|---|---|---|
| TurtleBot 3 Burger, Raspberry Pi 4 4 GB | 783.50 | kit | 9 |
| TurtleBot 3 Waffle Pi, Raspberry Pi 4 4 GB | 1,933.61 | kit | 10 |
| TurtleBot 3 Waffle Pi, Raspberry Pi 4 2 GB | 1,908.31 | kit | 11 |
| OpenCR1.0 board (spare) | 247.14 | retail | 11 |
| LiPo 11.1 V 1800 mAh battery (spare) | 68.54 | retail | 11 |
| DYNAMIXEL XL430-W250-T (Burger wheel servo) | 27.50 each | retail | 12 |

- The Burger product page showed a lead time to mid-January 2027 [9].
- The LDS-03 lidar is not sold on its own in the US store; it comes in the kits [9][11].
- At launch in 2017 the list prices were $549 (Burger) and $1,799 (Waffle) [19].
- A scratch build saves little: OpenCR alone costs about a third of the Burger kit, and the servos
  and lidar come from ROBOTIS anyway.

## Building it

**Difficulty 1:** the kit arrives unassembled and goes together with hand tools; no printing or
soldering [17].

- Follow the PDF assembly manual and videos for your model [17].
- Then set up the Raspberry Pi image, install ROS 2 and flash OpenCR from the Pi [4][18].
- No build time is stated by ROBOTIS.
- For a scratch build, export STL or STEP from the Onshape documents. Exporting needs an Onshape
  account, which confused users in 2017 and 2018; ROBOTIS later put STL files on Thingiverse [8].

Pitfalls the docs and history show:

- Set `LDS_MODEL` to match your lidar; three lidar models have shipped [15].
- Do not charge and run on the battery at the same time; use the 12 V 5 A adapter on OpenCR while
  swapping batteries [18].
- Documentation is in transition: the e-Manual now points to ROBOTIS Docs, and older pages still
  show ROS 1 steps (catkin, Ubuntu MATE) [17][18].
- The Waffle Pi store page links the Burger Onshape document, not a Waffle Pi one [10].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Chassis CAD (Burger, Waffle) | Onshape (exports STL, STEP) | Onshape documents linked from the 2017 announcement [8] | Declared open hardware under the OSHW Definition 1.0; no licence named [5] |
| Printable parts | STL | ROBOTIS Thingiverse profile [8] | None named |
| OpenCR1.0 board | OrCAD schematics, Gerbers, BOM | [OpenCR-Hardware](https://github.com/ROBOTIS-GIT/OpenCR-Hardware) [6] | "Open-source licenses", none named; no LICENSE file |
| OpenCR firmware | Arduino C++ | [OpenCR](https://github.com/ROBOTIS-GIT/OpenCR) [7] | Apache-2.0 |
| ROS 2 software | ROS 2 packages | [turtlebot3](https://github.com/ROBOTIS-GIT/turtlebot3) and sister repos [1] | Apache-2.0; ROBOTIS says some sources are BSD-3-Clause or GPL-3.0 [5] |
| Robot models | URDF, SDF | `turtlebot3_description`, `turtlebot3_simulations` [1][16] | Apache-2.0 |
| Docs | Web | e-Manual [5]; moving to ROBOTIS Docs [4] | CC-BY-4.0 per the e-Manual; the new ROBOTIS Docs site shows only a copyright line |
| Servos, lidar | Closed commercial parts | ROBOTIS | Not open |

## Strengths and limits

**Strengths**

- Active upstream: ROS 2 Humble and Jazzy support, Docker images and regular releases [1][14].
- Small and light (1 kg Burger), so it runs on a desk or a classroom floor [2].
- Simulation models and the real robot share topics and launch files [1][16].
- The controller board and firmware are published, which few commercial kits do [6][7].
- Modular plates let one kit become several robot shapes [5].

**Limits**

- Slow and indoor only: 0.22 m/s and a 10 mm threshold for the Burger [2].
- Not cheap for its size, and prices have risen since launch [9][19].
- Depends on ROBOTIS parts (servos, lidar, OpenCR), so you cannot source a cheaper copy.
- No hardware licence is named, so reuse rights for the CAD are unclear [5].
- CAD lives only on Onshape and needs an account to export [8].
- Lidar and computer changes mean older robots differ from new ones [2][3].

## What to reuse

- **One bus protocol everywhere:** OpenCR exposes its sensors through a DYNAMIXEL-style control
  table, so the host reads the board with the same SDK it uses for the servos [1].
- **Smart servos as wheel motors:** position feedback from the servo gives odometry without extra
  encoders [2].
- **Plate-and-standoff frame:** a few flat parts rebuild into many robot shapes [5].
- **Swappable sensors by environment variable:** one launch file supports several lidar models [15].
- **Fake node:** test navigation logic without a physics engine [16].

## Related robots

- [F1TENTH](f1tenth.md): a faster ROS 2 learning platform built on an RC car.
- [JPL Open Source Rover](jpl-open-source-rover.md): a larger outdoor wheeled platform with ROS 2.
- [Nanosaur](nanosaur.md): a palm-sized, printed Jetson robot for learning ROS 2.
- [OpenBot](openbot.md): a low-cost printed body driven by an Android phone.
- TurtleBot 2 (Yujin Robot, Kobuki base) and TurtleBot 4 (Clearpath, iRobot Create 3 base) are the
  neighbouring generations [4].

## Sources

1. [TurtleBot3 repository README](https://github.com/ROBOTIS-GIT/turtlebot3), accessed 2026-11-17
2. [ROBOTIS e-Manual: TurtleBot3 features](https://emanual.robotis.com/docs/en/platform/turtlebot3/features/), accessed 2026-11-17
3. [ROBOTIS Docs: TurtleBot3 features](https://docs.robotis.com/docs/systems/turtlebot3/features), accessed 2026-11-17
4. [ROBOTIS Docs: TurtleBot3 overview](https://docs.robotis.com/docs/systems/turtlebot3/overview/), accessed 2026-11-17
5. [ROBOTIS e-Manual: TurtleBot3 open source and licences](https://emanual.robotis.com/docs/en/platform/turtlebot3/opensource/), accessed 2026-11-17
6. [OpenCR-Hardware repository README](https://github.com/ROBOTIS-GIT/OpenCR-Hardware), accessed 2026-11-17
7. [OpenCR firmware repository](https://github.com/ROBOTIS-GIT/OpenCR), accessed 2026-11-17
8. [Open Robotics Discourse: TurtleBot3 hardware on Onshape](https://discourse.openrobotics.org/t/tb3-turtlebot3-hardware-free-for-you/1444), accessed 2026-11-17
9. [ROBOTIS US store: TurtleBot 3 Burger RPi4 4GB](https://robotis.us/products/turtlebot-3-burger-rpi4-4gb-us), accessed 2026-11-17
10. [ROBOTIS US store: TurtleBot 3 Waffle Pi RPi4 4GB](https://robotis.us/products/turtlebot-3-waffle-pi-rpi4-4gb-us), accessed 2026-11-17
11. [ROBOTIS US store: TurtleBot3 products and spare parts](https://robotis.us/search?q=turtlebot3&type=product), accessed 2026-11-17
12. [ROBOTIS US store: DYNAMIXEL XL430-W250-T](https://robotis.us/products/dynamixel-xl430-w250-t), accessed 2026-11-17
13. [ROBOTIS Docs: LDS-03 laser distance sensor](https://docs.robotis.com/docs/systems/turtlebot3/more_info/lds_03), accessed 2026-11-17
14. [turtlebot3 package changelog](https://github.com/ROBOTIS-GIT/turtlebot3/blob/main/turtlebot3/CHANGELOG.rst), accessed 2026-11-17
15. [turtlebot3_bringup robot launch file](https://github.com/ROBOTIS-GIT/turtlebot3/blob/main/turtlebot3_bringup/launch/robot.launch.py), accessed 2026-11-17
16. [turtlebot3_simulations repository](https://github.com/ROBOTIS-GIT/turtlebot3_simulations), accessed 2026-11-17
17. [ROBOTIS e-Manual: TurtleBot3 hardware assembly](https://emanual.robotis.com/docs/en/platform/turtlebot3/hardware_setup/), accessed 2026-11-17
18. [ROBOTIS e-Manual: TurtleBot3 FAQ](https://emanual.robotis.com/docs/en/platform/turtlebot3/faq/), accessed 2026-11-17
19. [IEEE Spectrum: TurtleBot 3 launch prices (2017)](https://spectrum.ieee.org/review-robotis-turtlebot-3), accessed 2026-11-17
