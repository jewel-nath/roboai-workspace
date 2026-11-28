---
type: source
name: A list of resources, projects and products useful for robot electronics
registry: list-of-robot-electronics
url: https://github.com/cajt/list_of_robot_electronics
commit: "e26414b"
read_on: 2026-11-26
counts: {entries: 66, pages: 1, waiting: 4, index_only: 39, deferred: 0, rejected: 22}
---

# A list of robot electronics: what it gives RoboAI

A short list of open robot electronics: motor drivers, actuators, a vision module, battery
management systems, FPGA boards, bus systems and sensors, then open robot projects, Eurobot teams
and student work. It is the only parts list Phase 5 found, but most of its hardware dates from
2011 to 2021 and is no longer worked on. It gives the actuators batch four BLDC controller pages
the choose-an-actuator guide will compare (VESC, ODrive, SimpleFOC, moteus) and the firmware batch
CANopenNode. Everything else is an index row or rejected: no other part here is used by two Atlas
robots.

## How it was read

- Read at commit `e26414b` (2025-07-26) on 2026-11-26 from a full clone: the README in full (65
  items in 13 sections); the repo holds nothing else but its BSD-2-Clause `LICENSE`. The item
  "ODrive & ODriveROS2" names two projects with different fates, so it is two rows: 66 rows.
- Dating and licences: each GitHub repo was shallow-cloned without blobs (depth 1) for its head
  commit date and licence file, or the README's licence section where there is no file. Org
  links (CVRA, RCA, ODRI, nanosaur) show the newest push on the org's github.com repository page.
  Non-GitHub links were checked with one HTTP request and their page title. The OSLRF-01 manual
  is dated by its PDF metadata (2014-02-06).
- Parts rule: Atlas `stack:` fields were searched for every part. VESC (F1TENTH), ODrive (Stanford
  Doggo), moteus (Upkie) and Mechaduino-derived boards (Hello Robot Stretch) appear once each;
  nothing else appears. The five page rows earn their pages through the plan instead: its
  actuators batch names ODrive, moteus, VESC and SimpleFOC for the actuator guide, and its
  firmware batch names CANopenNode. `software/simplefoc`, `parts/drivers/vesc-project-vesc`,
  `parts/drivers/mjbots-moteus` and `software/canopennode` are proposed slugs, not shared ones.
- Page candidates: VESC's list link is the 2016 hardware repo (CC-BY-SA-4.0); the firmware
  (`vedderb/bldc`, GPL-3.0) had a commit on 2026-11-25. ODrive's link moved from
  `madcowswe/ODrive` to `odriverobotics/ODrive` (MIT, 2026-01-20); the list notes that later
  ODrive boards have no open hardware. ODrive now ships its own `ros_odrive` (MIT, 2026-11-25).
  SimpleFOC was checked at `simplefoc/Arduino-FOC` (MIT, 2026-10-04); the list's second link is an
  AliExpress listing, not followed beyond the HTTP check. moteus: `mjbots/moteus` (Apache-2.0,
  2026-11-25). CANopenNode: Apache-2.0, 2026-07-10.
- `ros_canopen` is ROS 1 only (default branch `melodic-devel`), so it is an index row; its ROS 2
  line is the planned `software/ros2-canopen` page, which builds on Lely's `lely-core` (GitLab,
  Apache-2.0, 2025-08-25).
- Moved or superseded: the foxBMS link is foxBMS 1, which its README says is no longer supported;
  foxBMS 2 lives at `foxBMS/foxbms-2` (2026-10-06). LibreSolar's linked boards are from 2018 and
  2019; its current BMS C1 and Zephyr-based `bms-firmware` had commits in 2026-11. The hoverboard
  driver now targets the hoverboard-firmware-hack-FOC firmware; the bipropellant firmware the list
  names is on a branch. Mechaduino's and Evezor's page addresses changed but redirect.
  OtterControl's 2025-11-24 commit only adds pictures to its README.
- Dead on 2026-11-26: open-bldc.org returns 404 and krtkl.com (Snickerdoodle) does not respond.
  ValentF(x)'s own page marks the LOGI Bone retired. LightWare's site search finds no OSLRF
  product. Simple Robot is a blog whose last post is from 2022-07-05.
- Errors in the list: spelling ("Controler", "ditributed", "plattform", "mit" for "with").
- Nothing in the list was addressed to agents.

## Pages made

| Entry | Page | Tier |
|---|---|---|
| CANopenNode | [CANopenNode](../wiki/software/canopennode.md) | B |

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|
| VESC | `parts/drivers/vesc-project-vesc` | B | actuators | Open BLDC controller line with maintained GPL-3.0 firmware; drives F1TENTH and many wheeled builds, and the actuator guide compares it |
| ODrive | `parts/drivers/odrive-robotics-odrive` | B | actuators | The common BLDC controller of open legged robots (Stanford Doggo); the actuator guide compares it |
| Simple FOC | `software/simplefoc` | B | actuators | Maintained MIT Arduino library for field-oriented control on cheap boards; the low-cost end of the guide's BLDC comparison |
| Moteus | `parts/drivers/mjbots-moteus` | B | actuators | Maintained Apache-2.0 joint controller for quasi-direct-drive legs, used by Upkie; the actuator guide compares it |

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| Cheap FOCer 2 | Low-cost BLDC controller based on VESC 6, with assembly files | 2023-12-21 | CC-BY-SA-4.0 |
| OtterControl | Cheaper VESC-style DC and BLDC controller for hoverboard motors; Altium files and Gerbers | 2025-11-24 | none stated |
| stmbl | High-voltage AC servo drive | 2022-03-22 | GPL-3.0 |
| RCA's µMotor | Roboterclub Aachen's DC and BLDC driver up to 250 W, with firmware | 2025-02-16 | GPL-3.0; hardware CERN-OHL-1.2 |
| ODriveROS2 | Community `ros2_control` plugin for ODrive v3; ODrive's own `ros_odrive` belongs on the ODrive page | 2023-03-21 | Apache-2.0 |
| rp2040-motor-controller | Twisted Fields' RP2040 motor controller board | 2024-08-02 | CERN-OHL-P |
| Dagor | ESP32 BLDC controller with an on-board magnetic encoder; firmware built on SimpleFOC | 2024-06-19 | MIT |
| Betzdrive | BLDC driver of Berkeley's Blue arm project; inactive since 2022 | 2022-09-25 | MIT; hardware CERN-OHL-P |
| Mechaduino | Closed-loop stepper servo board; [Hello Robot Stretch](../wiki/robots/hello-robot-stretch.md) uses Mechaduino-derived boards | 2017-05-04 | CC-BY-SA-4.0 |
| OpenTorque Actuator | Compliant actuator for legged robots, an early open design | 2019-04-21 | CC-BY-SA-4.0 |
| 3D Printed Robot Actuator | Hackaday project: BLDC motor, cycloidal gearbox, controller and position sensing | — | — |
| ServoProject | New electronics and firmware that turn an RC servo into a closed-loop servo | 2024-04-01 | CC-BY-3.0-US |
| OpenMV | Open machine-vision camera module (STM32) with maintained firmware | 2026-11-24 | MIT, with GPL and non-commercial parts |
| PX4Flow | Optical-flow sensor board among PX4's open hardware designs | 2022-05-18 | CC-BY-SA-3.0 |
| LibreSolar Project | Two old BMS boards (5S, 48 V); LibreSolar's current BMS C1 and its firmware are maintained | 2019-05-16 | CC-BY-SA-4.0 (5S), GPL-3.0 (48 V) |
| ENNOID - BMS | Modular LTC68xx and STM32 BMS for packs up to 400 V, with firmware and a GUI | 2021-07-19 | GPL-3.0 |
| foxBMS | Fraunhofer IISB's modular BMS development platform; the link is foxBMS 1, superseded by foxBMS 2 | 2024-04-05 | — (foxBMS 2: BSD-3-Clause, CC-BY-4.0) |
| Green BMS | Modular SmartBMS for several cell chemistries | 2023-12-08 | CC-BY-SA-4.0 |
| flink | FPGA interface with VHDL IP cores, a Linux driver and a library | 2026-03-13 | Apache-2.0 |
| SAB | Sensor Actuator Bus module of modm, a maintained C++ library generator for microcontrollers | 2026-11-24 | MPL-2.0 |
| OpenCyphal | CAN protocol, formerly UAVCAN, for robotics and aerospace; libcanard is its C library | 2026-10-21 | MIT (libcanard) |
| Lely CANopen | CANopen stack under ros2_canopen; belongs on the planned `software/ros2-canopen` page | 2025-08-25 | Apache-2.0 |
| CANopen driver framework for ROS | `ros_canopen`, ROS 1 only; its ROS 2 line is the planned `software/ros2-canopen` page | 2026-11-18 | LGPL-3.0 |
| OpenSimpleLidar | Open-hardware scanning laser rangefinder: 4 m range, 5 scans a second | 2025-07-22 | MIT |
| Xaxxon OpenLIDAR | Rotating lidar on a Garmin LIDAR-Lite v3 with open software; still sold on 2026-11-26 | — | — |
| Reachy | Robot; on the [Reachy and Reachy 2](../wiki/robots/reachy.md) page | — | — |
| MORPH | Robot; not in the Atlas. Modular ROS platform on VESC drives | 2019-03-29 | GPL-3.0 |
| Evezor | Robot; not in the Atlas. Open SCARA manufacturing platform on Hackaday | — | — |
| Octanis Rover | Robot; not in the Atlas. Electronics of the Octanis 1 rover | 2016-06-23 | none stated |
| Linorobot | Robot; not in the Atlas. The ROS 1 stack; [linorobot2](../wiki/software/linorobot2.md) replaced it | 2022-07-11 | BSD-2-Clause |
| Bobble-Bot | Robot; not in the Atlas. Demo robot for real-time control (Raspberry Pi, RT Linux, ROS), on Hackaday | — | — |
| StanfordDoggoProject | Robot; on the [Stanford Doggo](../wiki/robots/stanford-doggo.md) page | 2024-07-08 | MIT |
| Open Dynamic Robot Initiative | Robots; on the [ODRI Solo-8, Solo-12 and Bolt](../wiki/robots/odri-solo.md) and [TriFinger](../wiki/robots/trifinger.md) pages | 2026-11-05 | — |
| Hoverboard + ROS | ROS driver that turns a hacked hoverboard into a cheap differential-drive base | 2023-10-31 | MIT |
| Hello Robot | Robot; on the [Hello Robot Stretch](../wiki/robots/hello-robot-stretch.md) page | — | — |
| nanosaur | Robot; on the [NanoSaur](../wiki/robots/nanosaur.md) page | 2026-10-16 | — |
| CVRA | Eurobot team's robot software and boards | 2024-03-20 | MIT (robot-software) |
| RCA | Roboterclub Aachen's Eurobot repos | 2025-05-13 | — |
| APBTeam | French Eurobot team's site with open robot designs | — | — |

## Deferred

| Entry | What it is | Phase |
|---|---|---|

## Rejected

| Entry | Why | Date |
|---|---|---|
| OpenBLDC | Dead link: the wiki page returns 404 | 2026-11-26 |
| HighPower-Mechaduino | One-off build, inactive since 2019 | 2026-11-26 |
| motor-control-board | CVRA's team board, inactive since 2018 | 2026-11-26 |
| MotCtrl | Small and inactive since 2018 | 2026-11-26 |
| Brushless DC motor controller board | A 2011 blog post, never maintained | 2026-11-26 |
| Closed Loop Motor Controller | Tarocco, a CNC step/dir board inactive since 2021 | 2026-11-26 |
| DC Servomotor Controller | An AVR design from the 2000s, not maintained | 2026-11-26 |
| STM_MotorController | Inactive since 2017 and no licence | 2026-11-26 |
| DirectServo | Inactive since 2018 and no licence | 2026-11-26 |
| DieBieMS | Inactive since 2019 and no licence file | 2026-11-26 |
| Ceech's BMS | Small and inactive since 2019 | 2026-11-26 |
| Battman BMS | Small and inactive since 2020 | 2026-11-26 |
| LOA | Niche FPGA IO framework, idle since 2015 apart from one 2025 migration commit | 2026-11-26 |
| Snickerdoodle | Dead link: krtkl.com does not respond | 2026-11-26 |
| Logi-Bone | Retired, by its maker's own page; its VHDL repo is inactive since 2016 | 2026-11-26 |
| UC4H: UAVCAN for Hobbyists | Inactive since 2020; OpenCyphal is the maintained line | 2026-11-26 |
| Simple Robot | A blog with no repo or licence; last post 2022-07-05 | 2026-11-26 |
| KaCanOpen | Inactive since 2019; a ROS 1 bridge that ros2_canopen replaces | 2026-11-26 |
| OSLRF-01 | A 2014 kit manual; LightWare's site search finds no OSLRF product | 2026-11-26 |
| OAP | Abandoned: inactive since 2008, as the list says | 2026-11-26 |
| Litter Bot | Student project, inactive since 2014 | 2026-11-26 |
| Zynq + OV7670 | Student HDL project, inactive since 2015 | 2026-11-26 |
