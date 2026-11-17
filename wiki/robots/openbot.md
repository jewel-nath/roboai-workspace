---
type: robot
name: OpenBot
summary: A $50 printed four-wheel body that turns an Android phone into the robot's brain, with an app for person following and learned driving; MIT-licensed throughout.
tags: [smartphone, android, arduino, esp32, tt-motor, 3d-printed, tflite, imitation-learning]
category: mobile-base
tier: A
openness: full
maker: Intel Labs (Matthias Müller and Vladlen Koltun); now maintained by the OpenBot Foundation
year: 2020
license: {hardware: MIT, software: MIT, docs: MIT}
links: {repo: https://github.com/ob-f/OpenBot, docs: https://github.com/ob-f/OpenBot/tree/master/body, cad: https://github.com/ob-f/OpenBot/tree/master/body, paper: https://arxiv.org/abs/2008.10631, site: https://www.openbot.org}
specs: {dof: 2, payload_kg: , reach_mm: , mass_kg: 0.7, size_mm: "240 x 150 x 120", speed_mps: 1.5, runtime_h: 0.75}
stack: {actuators: 4x TT gear motors driven as a left pair and a right pair, mcu: Arduino Nano (ATmega328P) or ESP32 dev kit, compute: Android smartphone (iOS app in beta) linked over USB serial or Bluetooth, sensors: [phone camera, phone IMU and GPS, LM393 optical wheel speed sensors (optional), ultrasonic distance sensor (optional), battery voltage divider], sim_models: [], ros2: none}
cost: {type: bom, usd: 50, as_of: 2021-03-10, source: https://arxiv.org/abs/2008.10631}
build: {difficulty: 2, hours: , print_hours: 23}
maturity: {last_commit: 2026-11-16, stars: 3671, active: true}
use_cases: [education, research, imitation-learning, navigation, data-collection, teleop]
evidence: researched
last_verified: 2026-11-17
sources:
  - {url: https://github.com/ob-f/OpenBot, title: OpenBot repository README, accessed: 2026-11-17}
  - {url: https://arxiv.org/abs/2008.10631, title: "OpenBot: Turning Smartphones into Robots (ICRA 2021)", accessed: 2026-11-17}
  - {url: https://github.com/ob-f/OpenBot/tree/master/body, title: OpenBot robot body overview, accessed: 2026-11-17}
  - {url: https://github.com/ob-f/OpenBot/tree/master/body/diy, title: OpenBot DIY body and BOM, accessed: 2026-11-17}
  - {url: https://github.com/ob-f/OpenBot/tree/master/body/diy/cad/regular_body, title: OpenBot regular body print settings, accessed: 2026-11-17}
  - {url: https://github.com/ob-f/OpenBot/tree/master/body/diy/pcb, title: OpenBot custom PCB, accessed: 2026-11-17}
  - {url: https://github.com/ob-f/OpenBot/tree/master/body/rtr, title: OpenBot ready-to-run vehicles, accessed: 2026-11-17}
  - {url: https://github.com/ob-f/OpenBot/tree/master/body/compact, title: OpenBot Compact body, accessed: 2026-11-17}
  - {url: https://github.com/ob-f/OpenBot/tree/master/body/lite, title: OpenBot Lite and education curriculum, accessed: 2026-11-17}
  - {url: https://github.com/ob-f/OpenBot/tree/master/body/mtv, title: OpenBot multi-terrain vehicle, accessed: 2026-11-17}
  - {url: https://github.com/ob-f/OpenBot/tree/master/firmware, title: OpenBot firmware, accessed: 2026-11-17}
  - {url: https://github.com/ob-f/OpenBot/tree/master/robot, title: OpenBot robot apps, accessed: 2026-11-17}
  - {url: https://github.com/ob-f/OpenBot/tree/master/policy, title: OpenBot driving policy training, accessed: 2026-11-17}
  - {url: https://github.com/ob-f/OpenBot/blob/master/LICENSE, title: OpenBot licence, accessed: 2026-11-17}
  - {url: https://www.openbot.org/, title: openbot.org, accessed: 2026-11-17}
  - {url: https://github.com/ob-f, title: OpenBot Foundation GitHub organisation, accessed: 2026-11-17}
  - {url: https://arxiv.org/abs/2405.07515, title: "OpenBot-Fleet: A System for Collective Learning with Real Robots", accessed: 2026-11-17}
  - {url: https://github.com/ob-f/OpenBot/commits/master, title: OpenBot commit history, accessed: 2026-11-17}
---

# OpenBot

OpenBot is a cheap printed four-wheel car with a phone mount, built so that an ordinary smartphone does all the sensing and computing.
Matthias Müller and Vladlen Koltun at Intel Labs released it in 2020; the repo now lives in the OpenBot Foundation's GitHub organisation.
A builder gets a $50 body, a maintained phone app with person following and a trainable driving policy, and MIT licences on everything.

The project was first published as `isl-org/OpenBot`, under Intel's Intelligent Systems Lab; that address now resolves to `ob-f/OpenBot` [1]. The licence file still names Intel ISL as the 2020 copyright holder [14]. The `ob-f` organisation is named OpenBot Foundation and lists no public members [16]; openbot.org calls the project an OpenBot Foundation initiative [15]. Development is active: in October and November 2026 the commits added a new Compact body, browser-based firmware flashing and iOS fixes [18].

## Specs

Figures are from the paper's comparison table for the original DIY body and are the makers' claims [2].

| Item | Value | Source |
|---|---|---|
| Drive | 4 wheels, skid steering | [2][4] |
| Actuated joints (dof) | 2: four TT motors wired as a left pair and a right pair | [4] |
| Size | 24 x 15 x 12 cm (maker's claim) | [2] |
| Mass | 0.7 kg (maker's claim; the paper does not say if the phone is included) | [2] |
| Top speed | 1.5 m/s (maker's claim) | [2] |
| Battery life | 45+ min (maker's claim) | [2] |
| Battery | 3x 18650 Li-ion in series, 9.6 to 12.6 V | [2] |
| Microcontroller | Arduino Nano (ATmega328P) or ESP32 dev kit | [11] |
| Motor driver | L298N module (DIY) or custom PCB with two TI DRV8871 | [2][4] |
| Brain | Android phone over USB serial; Bluetooth on ESP32 bodies | [2][11] |
| Body BOM | $50 for one, $35 each for five (2020 prices) | [2] |

## How it works

### Mechanics and actuation

The DIY chassis is a printed bottom plate and a top cover that clip together with LEGO-like connectors [2]. Four TT gear motors bolt to the bottom plate with eight M3x25 screws. The two left motors share one driver channel and the two right motors share the other [2][4]. A spring-loaded phone mount sits on top; a tilting version raises the phone up to 30 degrees [4].

There are several bodies [3]:
- **DIY:** the original, in regular, slim, glueable and "blocky" variants for different print beds [4].
- **Compact:** a body added in November 2026 for an ESP32 DevKit V1 and an L298N, with a LEGO-compatible lid; every part fits a 180 mm bed [8][18].
- **Lite:** a simplified education version for a micro:bit or Arduino Nano, made by ITE's eSpace [9].
- **RC truck:** printed parts that turn a 1:16 RC toy truck into an OpenBot [3].
- **Multi-terrain vehicle (MTV):** a six-wheel rocker-bogie body with JGB37-520 12 V encoder motors, made with Ivy Tech LTD [10].
- **Ready-to-run (RTR):** a splash-proof ABS shell in a TT-motor and a 520-motor version, sold assembled [7].

### Electronics and firmware

The microcontroller is a bridge between phone and body. It turns drive commands into PWM for the motor driver, counts wheel-encoder interrupts on the front wheels, reads battery voltage through a divider, and reads an optional ultrasonic sensor [11]. In the DIY build everything is wired with Dupont cables to an L298N [4]. A custom carrier PCB (v2) takes the Arduino Nano, adds motor drivers and the divider, and is published as Gerber, BOM and centroid files for JLCPCB-style assembly [6].

One Arduino sketch serves every body; a `OPENBOT` setting picks the body and its default parts [11]. Since November 2026 a web page flashes the firmware from Chrome or Edge, and can change settings later without reflashing [11][18].

### Software and control

The phone runs the robot app: Android (install the APK or build it), iOS in beta via Xcode, or a Python version for a Linux computer with a camera [12]. The app streams video, logs phone and body sensors, and runs TensorFlow Lite networks for person following and for autonomous driving inspired by conditional imitation learning [2]. You drive it with a Bluetooth gamepad, a phone controller app or a web controller [1][2]. A Blockly "Playground" lets beginners program it [1]. The `policy/` folder trains your own driving policy from logged data on a desktop with a GPU [13].

There is no ROS or ROS 2 support in the repo.

### Simulation

No URDF, MJCF or other simulation model is published in the repo.

## What it is used for

- **Research:** the original paper tested person following and navigation on several Android phones and found recent mid-range phones good enough [2]. OpenBot-Fleet (2024) gave 72 of the robots to crowd workers, who collected navigation data in homes; policies learned in the cloud reached over 80% success in unseen homes [17].
- **Education:** ITE's eSpace built a curriculum around OpenBot Lite, with video guides; it says more than 100 students in South Korea and Germany have used it [9].
- **Hobby builds:** the README links community variants, including a tank, a 2WD car and a cardboard body [1].

## Cost and BOM

The paper's bill of materials, for one body without the phone [2]:

| Item | Qty | Unit price | Bulk price (5 units) |
|---|---|---|---|
| Printed body | 1 | $5.00 | $5.00 |
| Speed sensor | 2 | $2.00 | $1.00 |
| Motor and tyre | 4 | $3.50 | $2.00 |
| Motor driver | 1 | $3.00 | $2.50 |
| Arduino Nano | 1 | $8.00 | $3.50 |
| 18650 battery | 3 | $7.00 | $4.00 |
| Miscellaneous | 1 | $5.00 | $2.00 |
| **Total** | | **$50** | **$35** |

These are 2020 approximate prices; batteries are about 40% of the cost [2]. The DIY guide links each part on Amazon (EU and US) and AliExpress without prices [4]. The phone is extra; the paper points out that second-hand phones are cheap [2].

A ready-to-run vehicle can be ordered. The body guide says Amazon, but on 2026-11-17 the `buy.openbot.org/rtr-tt` link redirected to a Taobao listing that could not be read, so no RTR price is given [3][7].

## Building it

**Difficulty 2:** a printed shell with off-the-shelf modules on Dupont cables; the only soldering is motor leads, and the firmware flashes from a browser.

- **Printing:** the regular body needs a 240 x 150 mm bed and prints without supports in PLA, ABS or CPE at 0.2 mm layers and 20% infill [5]. On an Ultimaker S5 the paper reports 13.5 h for the bottom and 9.5 h for the top, using 146 g and 103 g of filament [2]. The Compact body needs about 12 h and 305 g of PLA [8].
- **Tools:** soldering iron for the motor leads, M3 screws and nuts, a USB OTG cable for the phone [4].
- **Custom PCB:** order it with SMT assembly from the Gerber, BOM and centroid files; the guide found JLCPCB the cheapest and fastest option [6].
- **Pitfalls in the docs:**
  - Clone Arduino Nanos need the CH340 USB driver [11].
  - ESP32 builds need the Arduino ESP32 core 2.0.17; version 3.x fails to compile [8][11].
  - At full speed, weak or alkaline batteries let the voltage dip and reset the board, which drops the app connection [11].
  - The Compact guide lists more: a robot that turns when it should go straight has one side's motor wires swapped, and parts on GPIO 5 or 12 can stop an ESP32 from booting [8].

The paper's table lists a setup time of 0.5 h, but does not say whether that includes assembly, so no build time is given here [2].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| DIY, Compact, RC truck, RTR, MTV bodies and phone mounts | STL and STEP | `body/` | MIT |
| DIY carrier PCB v1, v2 | Gerber, BOM, centroid (no EDA source) | `body/diy/pcb` | MIT |
| RTR boards | BOM on master; Gerbers linked from a `thias15/rtr` branch | `body/rtr/pcb` | MIT |
| MTV boards | Gerber and PDF | `body/mtv/pcb` | MIT |
| Firmware | Arduino sketch | `firmware/` | MIT |
| Robot apps | Android, iOS (beta), Linux Python | `robot/` | MIT |
| Controllers, Playground, policy training | Flutter, web, Node.js, Python | `controller/`, `open-code/`, `policy/` | MIT |
| Paper | PDF | `docs/paper`, arXiv | arXiv preprint |

Sources: [1][6][7][10][14]. Commercial use is allowed under MIT.

## Strengths and limits

**Strengths**
- A $50 body (2020 prices); a used phone supplies camera, IMU, GPS, compute and radios.
- MIT licences on hardware and software, so kits and derivatives can be sold.
- Many bodies share one firmware and one app, from a cardboard car to a six-wheel rover.
- A full learning loop: collect data with a gamepad, train, deploy on the phone.
- Active maintenance and a large community (3,671 stars).

**Limits**
- No ROS 2 support and no simulation model, so it sits outside the usual ROS toolchain.
- The phone is a closed part you do not control; in the paper's tests, frame rates and success varied widely between phone models [2].
- TT motors are cheap and imprecise; odometry is only an optical slot sensor on two wheels.
- PCB designs ship as Gerbers only, so you cannot easily change them.
- Speed, mass and battery figures are the makers' 2020 claims for the first body.

## What to reuse

- **Phone as brain:** offload sensing and compute to a phone over USB serial or Bluetooth, and keep the robot's MCU to motors and simple sensors.
- **One firmware, many bodies:** a single settings block with per-body defaults, plus a build-time pin-conflict check [11].
- **Browser flashing:** a web page that flashes and later reconfigures the firmware removes the Arduino IDE for beginners [11].
- **Print-bed variants:** offering slim and glueable versions of the same body widens who can print it [4].
- **Gamepad data collection:** teleoperate with a gamepad while logging, then train a policy on the logs [2].

## Related robots

- [NanoSaur](nanosaur.md): a small printed robot with a Jetson instead of a phone.
- [F1TENTH](f1tenth.md): an RC-car platform the OpenBot paper compares against, far more expensive.
- [TurtleBot3](turtlebot3.md): the ROS 2 teaching base OpenBot is often weighed against.
- [JPL Open Source Rover](jpl-open-source-rover.md): a larger rocker-bogie rover, like the OpenBot MTV.
- Duckiebot, NVIDIA JetBot and Donkey Car: other low-cost learning cars the paper compares with.

## Sources

1. [OpenBot repository README](https://github.com/ob-f/OpenBot), accessed 2026-11-17
2. [OpenBot: Turning Smartphones into Robots (ICRA 2021)](https://arxiv.org/abs/2008.10631), accessed 2026-11-17
3. [OpenBot robot body overview](https://github.com/ob-f/OpenBot/tree/master/body), accessed 2026-11-17
4. [OpenBot DIY body and BOM](https://github.com/ob-f/OpenBot/tree/master/body/diy), accessed 2026-11-17
5. [OpenBot regular body print settings](https://github.com/ob-f/OpenBot/tree/master/body/diy/cad/regular_body), accessed 2026-11-17
6. [OpenBot custom PCB](https://github.com/ob-f/OpenBot/tree/master/body/diy/pcb), accessed 2026-11-17
7. [OpenBot ready-to-run vehicles](https://github.com/ob-f/OpenBot/tree/master/body/rtr), accessed 2026-11-17
8. [OpenBot Compact body](https://github.com/ob-f/OpenBot/tree/master/body/compact), accessed 2026-11-17
9. [OpenBot Lite and education curriculum](https://github.com/ob-f/OpenBot/tree/master/body/lite), accessed 2026-11-17
10. [OpenBot multi-terrain vehicle](https://github.com/ob-f/OpenBot/tree/master/body/mtv), accessed 2026-11-17
11. [OpenBot firmware](https://github.com/ob-f/OpenBot/tree/master/firmware), accessed 2026-11-17
12. [OpenBot robot apps](https://github.com/ob-f/OpenBot/tree/master/robot), accessed 2026-11-17
13. [OpenBot driving policy training](https://github.com/ob-f/OpenBot/tree/master/policy), accessed 2026-11-17
14. [OpenBot licence](https://github.com/ob-f/OpenBot/blob/master/LICENSE), accessed 2026-11-17
15. [openbot.org](https://www.openbot.org/), accessed 2026-11-17
16. [OpenBot Foundation GitHub organisation](https://github.com/ob-f), accessed 2026-11-17
17. [OpenBot-Fleet: A System for Collective Learning with Real Robots](https://arxiv.org/abs/2405.07515), accessed 2026-11-17
18. [OpenBot commit history](https://github.com/ob-f/OpenBot/commits/master), accessed 2026-11-17
