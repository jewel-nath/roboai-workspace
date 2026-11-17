---
type: robot
name: F1TENTH (RoboRacer)
summary: A 1/10-scale autonomous race car built from an RC chassis, a lidar, a VESC and a Jetson; the shared platform behind the RoboRacer courses and races.
tags: [ros2, ackermann, rc-car, vesc, jetson, lidar, autonomous-racing, traxxas, roboracer]
category: mobile-base
tier: A
openness: partial
maker: RoboRacer community (formerly F1TENTH), started by the University of Pennsylvania, University of Virginia and UNIMORE
year: 2016
license: {hardware: , software: MIT, docs: CC-BY-NC-SA-4.0}
links: {repo: https://github.com/f1tenth/f1tenth_system, docs: https://f1tenth.readthedocs.io/en/main/, cad: https://drive.google.com/drive/folders/1NU4FZzvMEGKCOFzDBvnjyePnnSMvsZPG, paper: https://arxiv.org/abs/1901.08567, site: https://roboracer.ai/}
specs: {dof: 2, payload_kg: , reach_mm: , mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: stock Traxxas brushless drive motor and steering servo (Fiesta ST Rally VXL chassis), mcu: VESC 6 MkVI motor controller and the RoboRacer power board, compute: NVIDIA Jetson Orin Nano Super with a 500 GB NVMe SSD, sensors: [Hokuyo UST-10LX 2D lidar, IMU read through the VESC driver, Intel RealSense D435i depth camera (optional)], sim_models: [f1tenth_gym (Python 2D racing simulator), xacro car model (f1tenth_gym_ros repo)], ros2: official}
cost: {type: bom, usd: 3022.29, as_of: 2026-05-15, source: https://docs.google.com/spreadsheets/d/e/2PACX-1vRuF3GM3UmTwcYbOtr3AtgkkBH2fq1R16bCkxm6pkRqP4Z7zXDOd5xkseBmqETPhQ/pubhtml}
build: {difficulty: 3, hours: , print_hours: }
maturity: {last_commit: 2026-09-11, stars: 129, active: true}
use_cases: [education, research, competition, navigation, reinforcement-learning]
evidence: researched
last_verified: 2026-11-17
sources:
  - {url: https://github.com/f1tenth/f1tenth_system, title: "f1tenth_system repository README (jazzy-devel)", accessed: 2026-11-17}
  - {url: https://github.com/f1tenth/f1tenth_doc, title: "f1tenth_doc repository and licence", accessed: 2026-11-17}
  - {url: https://f1tenth.readthedocs.io/en/main/getting_started/intro.html, title: "RoboRacer build docs: introduction", accessed: 2026-11-17}
  - {url: https://f1tenth.readthedocs.io/en/main/getting_started/build_car/index.html, title: "RoboRacer build docs: building the car", accessed: 2026-11-17}
  - {url: https://f1tenth.readthedocs.io/en/main/getting_started/build_car/bom.html, title: "RoboRacer build docs: bill of materials", accessed: 2026-11-17}
  - {url: https://docs.google.com/spreadsheets/d/e/2PACX-1vRuF3GM3UmTwcYbOtr3AtgkkBH2fq1R16bCkxm6pkRqP4Z7zXDOd5xkseBmqETPhQ/pubhtml, title: "RoboRacer Master BOM (updated 2026-05-15)", accessed: 2026-11-17}
  - {url: https://f1tenth.readthedocs.io/en/main/getting_started/build_car/all_together.html, title: "RoboRacer build docs: putting it all together", accessed: 2026-11-17}
  - {url: https://f1tenth.readthedocs.io/en/main/getting_started/firmware/firmware_vesc.html, title: "RoboRacer build docs: configuring the VESC", accessed: 2026-11-17}
  - {url: https://f1tenth.readthedocs.io/en/main/getting_started/firmware/drive_workspace.html, title: "RoboRacer build docs: driver stack setup", accessed: 2026-11-17}
  - {url: https://f1tenth.readthedocs.io/en/main/getting_started/faq.html, title: "RoboRacer build docs: FAQ", accessed: 2026-11-17}
  - {url: https://roboracer.ai/, title: "RoboRacer website", accessed: 2026-11-17}
  - {url: https://arxiv.org/abs/1901.08567, title: "F1/10: An Open-Source Autonomous Cyber-Physical Platform (O'Kelly et al. 2019)", accessed: 2026-11-17}
  - {url: https://arxiv.org/abs/2506.15899, title: "Survey of the RoboRacer (F1TENTH) platform (2025)", accessed: 2026-11-17}
  - {url: https://github.com/f1tenth/f1tenth_gym, title: "f1tenth_gym repository", accessed: 2026-11-17}
  - {url: https://github.com/f1tenth/f1tenth_gym_ros, title: "f1tenth_gym_ros repository", accessed: 2026-11-17}
  - {url: https://news.mit.edu/2015/students-autonomous-robots-race-mit-tunnels-0406, title: "MIT News: student autonomous robots race in MIT tunnels (2015)", accessed: 2026-11-17}
  - {url: https://mit-racecar.github.io/hardware, title: "MIT RACECAR hardware page", accessed: 2026-11-17}
  - {url: https://github.com/mlab-upenn/f1tenthpublic, title: "mlab-upenn/f1tenthpublic (archived hardware files)", accessed: 2026-11-17}
  - {url: https://f1tenth-coursekit.readthedocs.io/en/latest/, title: "RoboRacer course kit", accessed: 2026-11-17}
  - {url: https://github.com/f1tenth/f1tenth_system/blob/jazzy-devel/f1tenth_stack/config/vesc.yaml, title: "f1tenth_stack VESC configuration", accessed: 2026-11-17}
  - {url: https://f1tenth.readthedocs.io/en/main/getting_started/software_setup/optional_software_nx.html, title: "RoboRacer build docs: configuring the Jetson", accessed: 2026-11-17}
  - {url: https://f1tenth.readthedocs.io/en/main/getting_started/build_car/lower_level_chassis.html, title: "RoboRacer build docs: lower level chassis", accessed: 2026-11-17}
  - {url: https://f1tenth.readthedocs.io/en/main/getting_started/build_car/upper_level_chassis.html, title: "RoboRacer build docs: upper level chassis", accessed: 2026-11-17}
---

# F1TENTH (RoboRacer)

F1TENTH is a 1/10-scale autonomous race car: a hobby RC chassis with a 2D lidar, a VESC motor
controller and an NVIDIA Jetson running a ROS 2 driver stack [4][12].
It started in 2016 at the University of Pennsylvania, University of Virginia and UNIMORE, and the
project now goes by RoboRacer; f1tenth.org redirects to roboracer.ai [11][12][13].
For a builder it is a proven recipe for a fast Ackermann-steered robot, with a dated BOM, step-by-step
build docs, a simulator and a community that races several times a year [6][11][13].

## Specs

The build docs describe one reference build, but the FAQ allows any compute or lidar that runs the
driver stack [10]. Values below are for the reference build.

| Item | Value | Source |
|---|---|---|
| Scale | 1/10 of a full-size car | 12 |
| Chassis | Traxxas Fiesta ST Rally VXL (1/10, brushless, 4WD) in the current BOM; the build pages still show a Traxxas Slash 4x4 | 4, 6 |
| Drive | Ackermann steering; DOF counted as 2 (drive motor and steering servo) | 8, 12 |
| Wheelbase | About 0.25 m (config file comment) | 20 |
| Motor controller | VESC 6 MkVI; drives the brushless motor and the steering servo | 6, 8 |
| Compute | Jetson Orin Nano Super in the BOM; build pages show a Jetson Xavier NX | 4, 6 |
| Lidar | Hokuyo UST-10LX (40 Hz per the BOM); SICK TiM571 named as a 15 Hz alternative | 6 |
| Other sensors | IMU and motor telemetry through the VESC driver; Intel RealSense D435i optional | 1, 6 |
| Battery | 3S LiPo, 6000 mAh (two packs in the BOM) | 6 |
| Top speed | Not stated for the current build. The 2019 paper says its Traxxas chassis can reach 40 mph (about 18 m/s) | 12 |
| Mass, size, runtime | Not stated in the docs or BOM | |

## How it works

### Mechanics and actuation

The lower level is the RC car with its stock electronics removed: builders take out the Traxxas
speed controller and receiver and keep the steering servo [22]. The drive motor stays a
brushless RC motor turning all four wheels through the stock drivetrain [6][12]. The upper level is
a laser-cut platform deck on standoffs, which carries the VESC, the power board, the Jetson and the
lidar [23]; a printed mount holds the Wi-Fi antennas [6]. The deck is not symmetric, so the VESC
holes must face the right way [23].

### Electronics and firmware

- **VESC:** an open-source brushless motor controller [17]. It drives the motor from battery power
  and drives the steering servo through a cable on its PPM port [7][8]. You flash its stock firmware
  with VESC Tool, enable servo output, load the motor configuration file the docs provide and run
  motor detection [8].
- **Power board:** a small board that keeps a stable supply as the battery voltage drops and gives
  12 V terminals for the Jetson and the lidar [7][12]. The current board is bought assembled for
  $125 [6]. Its barrel jack takes 9 to 16 V only [21].
- **Wiring:** the motor's three phase wires go to the VESC through bullet adapters; the Jetson connects
  to the VESC by USB and to the Hokuyo lidar by Ethernet [7][8].

### Software and control

`f1tenth_system` is the on-car driver stack. Its `f1tenth_stack` package launches joystick teleop,
the VESC driver, a node that turns Ackermann commands into motor speed and servo position, wheel
odometry from VESC data, the lidar driver and an Ackermann command multiplexer [1]. Autonomy code
publishes `AckermannDriveStamped` messages on `/drive` and reads `/scan`, `/odom` and the IMU [1].
On a Logitech F710 pad, one bumper is a dead-man switch for teleop and the other for autonomy [1].
Odometry depends on calibrating `speed_to_erpm_gain` and the steering servo gain and offset in
`vesc.yaml` [20].

The repository's default branch is `jazzy-devel`; the native setup guide currently installs ROS 2
Humble from the `humble-devel` branch, and a Docker route covers older Jetsons on ROS 2 Foxy [1][9].

### Simulation

- **f1tenth_gym:** a Python racing simulator with multi-car support (MIT) [14].
- **f1tenth_gym_ros:** wraps the gym as a ROS 2 simulation with the same topics as the real car, and
  holds a xacro model of the car (`launch/ego_racecar.xacro`) (MIT) [15].
- The 2025 survey also lists AutoDRIVE, CARLA, AWSIM and Gazebo setups used with the platform [13].

## What it is used for

- **Courses:** the 2019 paper names full-semester classes at UVA, Penn and Oregon State, with the
  material also taught at UT Austin and Clemson; the community publishes a course kit [12][19].
- **Racing:** competitions began at ES-Week 2016 and ran at CPS Week 2018 (Porto) and ES-Week 2018
  (Turin) [12]. The 2025 survey lists 2024 races at seven conferences, among them ICRA and IROS [13].
  The RoboRacer site advertises a race at IROS 2026 [11].
- **Research:** planning, control, perception and learning at high speed on a cheap, crashable car;
  the 2025 survey reviews this work [13].
- **Reinforcement learning:** the gym environment is built for training racing policies [14].

**History: MIT RACECAR.** The same recipe appeared a year earlier at MIT. In January 2015, MIT
AeroAstro and Lincoln Laboratory ran a course where four student teams raced 1:10 RC cars with a
Jetson TK1, a scanning lidar, a camera and an IMU through MIT's tunnels [16]. Its later hardware
(RACECAR 2.0) used a Traxxas rally chassis, a VESC, a Hokuyo UST-10LX and a Jetson TX1, which is
close to the F1TENTH build [17]. F1TENTH turned the idea into a shared, multi-university platform
with common rules and races [12].

## Cost and BOM

The Master BOM is a public Google Sheet, last updated 2026-05-15. Its stated total is **$3,022.29**
(estimated, type `bom`), including the optional $334 depth camera [6]. Without the camera, the same
line items add up to $2,688.29 (our sum). Main items:

| Item | Price (USD) | Source |
|---|---|---|
| Hokuyo UST-10LX lidar | 1,200.00 | 6 |
| Traxxas Fiesta ST Rally VXL chassis | 429.95 | 6 |
| Intel RealSense D435i (optional) | 334.00 | 6 |
| VESC 6 MkVI | 249.75 | 6 |
| Jetson Orin Nano Super | 249.00 | 6 |
| Power board | 125.00 | 6 |
| 500 GB NVMe SSD | 100.00 | 6 |
| Two 3S 6000 mAh LiPo packs | 89.99 | 6 |
| Laser-cut deck, printed antenna mount | 20.00 and 10.00 | 6 |
| Fasteners, cables, charger, gamepad and small parts | rest of total | 6 |

- The lidar is 40% of the cost. The BOM names the SICK TiM571 as a slower (15 Hz) alternative but
  gives no price for it; the FAQ allows any lidar that publishes a ROS 2 `LaserScan` [6][10].
- The BOM notes a Traxxas Slash 4x4 Ultimate ($529.95) also fits the deck [6].
- No complete kit is sold by the project; parts come from Traxxas, Amazon, McMaster, SparkFun,
  Trampa and a power-board seller [6].

## Building it

**Difficulty 3:** laser cutting and a small print, connector and screw-terminal wiring, flashing the
VESC and the Jetson, then odometry calibration; the docs rate it intermediate to advanced [3].

- Time: the docs estimate 10 to 15 hours overall, about 1.5 hours for the hardware and 1 hour for the
  VESC [3][4][8].
- Tools: an M5 hex key, the hex keys that come with the Traxxas, and a T3 Torx driver [5].
- The deck needs a laser cutter or a service such as Ponoko; the antenna mount is printed [5][6].
- Build videos exist for each stage [3][4].

Pitfalls the docs warn about:

- LiPo safety: charge in a fire-proof bag and never connect the battery backwards; doing so damages
  the VESC, the power board and likely the Jetson [4][7].
- Swapping the lidar's brown and blue wires destroys it [7].
- Do not plug the Jetson's own 19 V adapter into the power board [21].
- Keep cables away from the spinning driveshaft [7].
- If VESC motor detection fails, the FAQ suggests checking the firmware and battery voltage, and
  running detection with the motor gear moved out of mesh [10].
- The docs lag the BOM: build pages still describe the Xavier NX and Slash 4x4, and pages for the
  older Jetson TX2 and Ford Fiesta chassis are marked deprecated [4][5].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Platform deck | DXF for laser cutting | Google Drive folder linked from the BOM [5][6] | None stated |
| Antenna mount | Printable files | Google Drive folder linked from the BOM [6] | None stated |
| Power board | Not published for the current board; older v3 files in Altium | [mlab-upenn/f1tenthpublic](https://github.com/mlab-upenn/f1tenthpublic), archived 2020 [18] | None stated |
| BOM | Google Sheet | [Master BOM](https://docs.google.com/spreadsheets/d/e/2PACX-1vRuF3GM3UmTwcYbOtr3AtgkkBH2fq1R16bCkxm6pkRqP4Z7zXDOd5xkseBmqETPhQ/pubhtml) [6] | None stated |
| Driver stack | ROS 2 packages | [f1tenth_system](https://github.com/f1tenth/f1tenth_system) [1] | MIT |
| Simulator | Python, ROS 2 | [f1tenth_gym](https://github.com/f1tenth/f1tenth_gym), [f1tenth_gym_ros](https://github.com/f1tenth/f1tenth_gym_ros) [14][15] | MIT |
| Build docs | Sphinx (reStructuredText) | [f1tenth_doc](https://github.com/f1tenth/f1tenth_doc) [2] | CC-BY-NC-SA-4.0, **non-commercial** |
| VESC motor configuration | VESC Tool XML | Google Drive, linked from the VESC page [8] | None stated |

The build documentation is non-commercial: you may share and adapt it with credit, but not for
commercial purposes, and adaptations must use the same licence [2].

## Strengths and limits

**Strengths**

- Mostly off-the-shelf parts; only the deck and antenna mount are made, and both are simple [5][6].
- Fast and cheap to crash compared with a full-size test car, which is the point of the platform [12].
- One software interface (`/drive`, `/scan`, `/odom`) shared by the car and the simulator [1][15].
- A live community with courses, races and a dated BOM [6][11][19].

**Limits**

- Expensive for its size: about $3,000, mostly the lidar [6].
- Docs and BOM disagree on chassis and Jetson, and the docs mix ROS 2 Foxy, Humble and Jazzy
  branches [1][4][9].
- Hardware files have no named licence and live on Google Drive, outside version control [5][6].
- The current power board's design files are not published [18].
- Build docs are non-commercial [2].
- No published mass, top speed or runtime for the reference build.

## What to reuse

- **VESC for drive and steering:** one open controller runs the brushless motor, reads its speed for
  odometry and drives the steering servo [8].
- **Ackermann command mux:** joystick and autonomy feed one multiplexer with dead-man buttons, so a
  person can always take over [1].
- **Two-level layout:** keep the vehicle's drivetrain and put all autonomy parts on one flat deck that
  lifts off as a unit [4][7].
- **Sim-to-real by topic names:** the simulator publishes the same topics as the car, so code moves
  between them unchanged [15].

## Related robots

- [TurtleBot3](turtlebot3.md): a slower, cheaper ROS 2 learning robot.
- [JPL Open Source Rover](jpl-open-source-rover.md): another wheeled ROS 2 platform, built for rough
  ground instead of speed.
- [OpenBot](openbot.md): a far cheaper phone-driven car, also used for learned driving.
- [Nanosaur](nanosaur.md): a palm-sized Jetson robot for learning ROS 2.
- MIT RACECAR is the earlier project described above. MuSHR, the University of Washington race car,
  is a similar platform.

## Sources

1. [f1tenth_system repository README (jazzy-devel)](https://github.com/f1tenth/f1tenth_system), accessed 2026-11-17
2. [f1tenth_doc repository and licence](https://github.com/f1tenth/f1tenth_doc), accessed 2026-11-17
3. [RoboRacer build docs: introduction](https://f1tenth.readthedocs.io/en/main/getting_started/intro.html), accessed 2026-11-17
4. [RoboRacer build docs: building the car](https://f1tenth.readthedocs.io/en/main/getting_started/build_car/index.html), accessed 2026-11-17
5. [RoboRacer build docs: bill of materials](https://f1tenth.readthedocs.io/en/main/getting_started/build_car/bom.html), accessed 2026-11-17
6. [RoboRacer Master BOM (updated 2026-05-15)](https://docs.google.com/spreadsheets/d/e/2PACX-1vRuF3GM3UmTwcYbOtr3AtgkkBH2fq1R16bCkxm6pkRqP4Z7zXDOd5xkseBmqETPhQ/pubhtml), accessed 2026-11-17
7. [RoboRacer build docs: putting it all together](https://f1tenth.readthedocs.io/en/main/getting_started/build_car/all_together.html), accessed 2026-11-17
8. [RoboRacer build docs: configuring the VESC](https://f1tenth.readthedocs.io/en/main/getting_started/firmware/firmware_vesc.html), accessed 2026-11-17
9. [RoboRacer build docs: driver stack setup](https://f1tenth.readthedocs.io/en/main/getting_started/firmware/drive_workspace.html), accessed 2026-11-17
10. [RoboRacer build docs: FAQ](https://f1tenth.readthedocs.io/en/main/getting_started/faq.html), accessed 2026-11-17
11. [RoboRacer website](https://roboracer.ai/), accessed 2026-11-17
12. [F1/10: An Open-Source Autonomous Cyber-Physical Platform (O'Kelly et al. 2019)](https://arxiv.org/abs/1901.08567), accessed 2026-11-17
13. [Survey of the RoboRacer (F1TENTH) platform (2025)](https://arxiv.org/abs/2506.15899), accessed 2026-11-17
14. [f1tenth_gym repository](https://github.com/f1tenth/f1tenth_gym), accessed 2026-11-17
15. [f1tenth_gym_ros repository](https://github.com/f1tenth/f1tenth_gym_ros), accessed 2026-11-17
16. [MIT News: student autonomous robots race in MIT tunnels (2015)](https://news.mit.edu/2015/students-autonomous-robots-race-mit-tunnels-0406), accessed 2026-11-17
17. [MIT RACECAR hardware page](https://mit-racecar.github.io/hardware), accessed 2026-11-17
18. [mlab-upenn/f1tenthpublic (archived hardware files)](https://github.com/mlab-upenn/f1tenthpublic), accessed 2026-11-17
19. [RoboRacer course kit](https://f1tenth-coursekit.readthedocs.io/en/latest/), accessed 2026-11-17
20. [f1tenth_stack VESC configuration](https://github.com/f1tenth/f1tenth_system/blob/jazzy-devel/f1tenth_stack/config/vesc.yaml), accessed 2026-11-17
21. [RoboRacer build docs: configuring the Jetson](https://f1tenth.readthedocs.io/en/main/getting_started/software_setup/optional_software_nx.html), accessed 2026-11-17
22. [RoboRacer build docs: lower level chassis](https://f1tenth.readthedocs.io/en/main/getting_started/build_car/lower_level_chassis.html), accessed 2026-11-17
23. [RoboRacer build docs: upper level chassis](https://f1tenth.readthedocs.io/en/main/getting_started/build_car/upper_level_chassis.html), accessed 2026-11-17
