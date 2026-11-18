---
type: robot
name: Petoi Nybble and Bittle
summary: Palm-sized servo robot cat (Nybble) and dog (Bittle) kits from Petoi on the MIT-licensed OpenCat firmware; a cheap first step into legged gaits. The current kits are the Bittle X V2 and Nybble Q on Petoi's ESP32 BiBoard; the original NyBoard models are discontinued.
tags: [quadruped, robot-pet, servo, kit, opencat, esp32, biboard, arduino, education, petoi]
category: legged
tier: B
openness: partial
maker: Petoi
year: 2018
license: {hardware: , software: MIT, docs: }
links: {repo: "https://github.com/PetoiCamp/OpenCatEsp32-Quadruped-Robot", docs: "https://docs.petoi.com", cad: "https://github.com/PetoiCamp/NonCodeFiles/tree/master/stl", paper: , site: "https://www.petoi.com"}
specs: {dof: 9, payload_kg: , reach_mm: , mass_kg: , size_mm: "190 x 153 x 107", speed_mps: , runtime_h: 1}
stack: {actuators: "9 Petoi digital PWM servos (P1L plastic-gear Lite or P1S alloy-gear), coreless motors, 8.4 V max", mcu: "BiBoard: ESP32-WROOM-32D, 12 PWM servo channels, Wi-Fi and Bluetooth", compute: "optional Raspberry Pi on the board socket", sensors: ["6-axis IMU (MPU6050 or ICM42670)"], sim_models: ["URDF and Gazebo for Bittle and Nybble (ROS 1, Petoi ros_opencat)"], ros2: none}
cost: {type: kit, usd: 319, as_of: 2026-11-18, source: "https://www.petoi.com/products/petoi-robot-dog-bittle-x-voice-controlled"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-11-18, stars: 552, active: true}
use_cases: [education, hobby, locomotion, reinforcement-learning, research]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://www.petoi.com/products/petoi-robot-dog-bittle-x-voice-controlled", title: "Petoi shop: Bittle X V2 (variants and prices)", accessed: 2026-11-18}
  - {url: "https://www.petoi.com/pages/robot-dog-bittle-x-technical-specifications", title: Petoi Bittle X technical specifications, accessed: 2026-11-18}
  - {url: "https://github.com/PetoiCamp/OpenCatEsp32-Quadruped-Robot", title: OpenCatESP32 README and licence, accessed: 2026-11-18}
  - {url: "https://github.com/PetoiCamp/OpenCat", title: OpenCat (NyBoard) README and licence, accessed: 2026-11-18}
  - {url: "https://docs.petoi.com/biboard/biboard-v0", title: Petoi docs, BiBoard V0, accessed: 2026-11-18}
  - {url: "https://github.com/PetoiCamp/NonCodeFiles/tree/master/stl", title: Petoi NonCodeFiles, printable parts, accessed: 2026-11-18}
  - {url: "https://github.com/PetoiCamp/ros_opencat", title: "ros_opencat (ROS 1) README and models", accessed: 2026-11-18}
  - {url: "https://www.petoi.com/products/petoi-nybble-q-robot-cat", title: "Petoi shop: Nybble Q", accessed: 2026-11-18}
  - {url: "https://www.petoi.com/blogs/blog/petoi-bittle-the-palm-sized-trick-playing-robot-dog-successfully-raised-567k-on-kickstarter", title: "Petoi blog: Bittle raised $567K on Kickstarter (2020)", accessed: 2026-11-18}
---

# Petoi Nybble and Bittle

Robot pets from Petoi: Nybble, a cat, and Bittle, a dog, sold as servo kits for a few hundred
dollars and run by OpenCat, Petoi's MIT-licensed quadruped firmware: a common first step into
legged gaits [1][3][4]. The original NyBoard models are **discontinued**; Petoi now sells the
ESP32-based Bittle X V2 and Nybble Q [3]. The firmware is open; the boards and frame CAD are not.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Bittle X V2, construction kit, Lite servos | [1] |
| Joints | 9 servos: 8 in the legs (two per leg), 1 in the neck | [2][4] |
| Servos | Petoi digital servos, P1L (plastic gears) or P1S (alloy gears); coreless motor, 8.4 V max | [2] |
| Size, mass | 190 x 153 x 107 mm standing; 269–353 g by version (maker's claims) | [2] |
| Controller | BiBoard: ESP32-WROOM-32D, 16 MB flash, 12 PWM channels, Wi-Fi, Bluetooth, 4 Grove ports | [2] |
| IMU | 6-axis MPU6050 or ICM42670, by chip availability | [2] |
| Battery, runtime | 7.4 V 1000 mAh Li-ion; about 1 hour; about 1.5 h to charge (maker's claims) | [2] |
| Programming | Block coding, Arduino IDE, OpenCat Python API over serial; desktop and mobile apps | [2] |
| Assembly | About 40 minutes for the construction kit (maker's claim); payload and speed not stated | [2] |

## How it works

Each leg has two servos on a plastic frame, driven by PWM from the controller board; OpenCat
handles gait coordination, servo control and IMU input [2][4]. OpenCat is Arduino code: the
NyBoard version (ATmega328P) lives in the OpenCat repo and the BiBoard version (ESP32) in
OpenCatESP32, both MIT [3][4]. A Raspberry Pi or another computer can sit on the robot and send
serial commands for vision or AI work [2][4].

Petoi's `ros_opencat` packages are ROS 1 only and include Bittle and Nybble URDF models with Gazebo
launch files [7]. No ROS 2 package or MuJoCo model from Petoi was found. Petoi publishes STLs of
many Bittle parts, the wooden Nybble and the Nybble Q, without a licence file [6].

| Variant | Joints | Board | Status | Price | Source |
|---|---|---|---|---|---|
| Nybble | 11: 8 legs, 2 head, 1 tail | NyBoard (ATmega328P) | Discontinued; first sold after OpenCat's 2018 Indiegogo | — | [4][9] |
| Bittle | 9 | NyBoard | Discontinued; 2020 Kickstarter | — | [4][9] |
| Bittle X V2 | 9 | BiBoard (ESP32) | Current; voice commands | $319–$399 (kit or assembled, Lite or alloy servos) | [1][3] |
| Bittle X V2 + Arm | 9 plus an arm | BiBoard | Current; alloy servos only | $449–$469 | [1] |
| Nybble Q | 11: 8 legs, 2 head, 1 tail | BiBoard V1 | Current | from $435 | [8] |
| Quaddle | 4 servos with position feedback | ESP32-S3 | Kickstarter, October 2026; code not yet public | — | [3] |

## What it is used for

- Teaching coding and robotics from school to university, with block coding, Arduino and Python [2][3].
- Gait, reinforcement-learning and sim-to-real experiments on a cheap robot; Petoi says 14 papers
  cite the platform (maker's claim) [3].
- ROS 1 SLAM and navigation with a Raspberry Pi on board [3][7]; hobby builds with printed add-ons [6].

## Cost and BOM

Petoi's shop lists the Bittle X V2 at $319 as a construction kit with Lite servos, $339
pre-assembled, $379 and $399 with alloy servos, and $449–$469 with the arm, on 2026-11-18 [1].
The Nybble Q starts at $435 [8]. No BOM is published.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Firmware, current boards | Arduino C++ for ESP32 | [OpenCatESP32](https://github.com/PetoiCamp/OpenCatEsp32-Quadruped-Robot) [3] | MIT |
| Firmware, NyBoard; Python API | Arduino C++, Python | [OpenCat](https://github.com/PetoiCamp/OpenCat) [4] | MIT |
| Printable parts | STL, some STEP and 3MF | [NonCodeFiles/stl](https://github.com/PetoiCamp/NonCodeFiles/tree/master/stl) [6] | No licence file; one community part is CC BY-SA |
| ROS 1 packages and models | ROS 1, URDF, Gazebo | [ros_opencat](https://github.com/PetoiCamp/ros_opencat) [7] | MIT |
| Boards (NyBoard, BiBoard) | Block diagrams only | [Petoi docs](https://docs.petoi.com/biboard/biboard-v0) [5] | Not published |

## Strengths and limits

- **Strengths:** a walking quadruped for about $300; actively maintained MIT firmware; many ways to
  program it; Wi-Fi, Bluetooth and a Raspberry Pi socket; 30,000+ robots shipped (maker's claim) [1][2][3].
- **Limits:** PWM hobby servos (Petoi presents readable position feedback as new in Quaddle) [3]; the
  board designs and frame CAD are closed, though Petoi calls the hardware open source [3][5]; ROS 1 only [7].

## Related robots

- [Pupper v3](pupper-v3.md): the next step up, a brushless quadruped with an RL policy.
- [Open Duck Mini](open-duck-mini.md) and [ToddlerBot](toddlerbot.md): open servo-driven walkers.

## Sources

1. [Petoi shop: Bittle X V2 (variants and prices)](https://www.petoi.com/products/petoi-robot-dog-bittle-x-voice-controlled), accessed 2026-11-18
2. [Petoi Bittle X technical specifications](https://www.petoi.com/pages/robot-dog-bittle-x-technical-specifications), accessed 2026-11-18
3. [OpenCatESP32 README and licence](https://github.com/PetoiCamp/OpenCatEsp32-Quadruped-Robot), accessed 2026-11-18
4. [OpenCat (NyBoard) README and licence](https://github.com/PetoiCamp/OpenCat), accessed 2026-11-18
5. [Petoi docs, BiBoard V0](https://docs.petoi.com/biboard/biboard-v0), accessed 2026-11-18
6. [Petoi NonCodeFiles, printable parts](https://github.com/PetoiCamp/NonCodeFiles/tree/master/stl), accessed 2026-11-18
7. [ros_opencat (ROS 1) README and models](https://github.com/PetoiCamp/ros_opencat), accessed 2026-11-18
8. [Petoi shop: Nybble Q](https://www.petoi.com/products/petoi-nybble-q-robot-cat), accessed 2026-11-18
9. [Petoi blog: Bittle raised $567K on Kickstarter (2020)](https://www.petoi.com/blogs/blog/petoi-bittle-the-palm-sized-trick-playing-robot-dog-successfully-raised-567k-on-kickstarter), accessed 2026-11-18
