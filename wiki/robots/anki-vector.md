---
type: robot
name: Vector (Anki, Digital Dream Labs)
summary: Palm-sized tracked home robot with a lift, a screen face and a time-of-flight sensor, launched by Anki in 2018 and sold as Vector 2.0 by Digital Dream Labs; programmable through Anki's Apache-2.0 Python SDK and kept alive by the MIT wire-pod voice server.
tags: [anki, digital-dream-labs, desk-robot, companion, screen-face, tracked, python-sdk, wire-pod, cloud-dependent, commercial]
category: social
tier: B
openness: software-only
maker: Anki (2018–2019); Digital Dream Labs since 2019
year: 2018
license: {hardware: , software: Apache-2.0 AND MIT, docs: }
links: {repo: "https://github.com/kercre123/wire-pod", docs: "https://github.com/anki/vector-python-sdk", cad: , paper: , site: }
specs: {dof: 4, payload_kg: , reach_mm: , mass_kg: , size_mm: , speed_mps: , runtime_h: 1}
stack: {actuators: "4 motors: left and right treads, head tilt, lift", mcu: , compute: "Qualcomm APQ8009 quad-core on board; speech and knowledge through a cloud or self-hosted server over Wi-Fi", sensors: ["HD camera (1280 x 720 on Vector 1.0, 2 MP on 2.0)", "time-of-flight distance sensor", "four cliff sensors", "four microphones", "touch sensor", "accelerometer and gyroscope"], sim_models: ["Webots worlds and controllers (digital-dream-labs/vector, Webots R2018a/R2020a, DDL licence)"], ros2: community}
cost: {type: retail, usd: 265.98, as_of: 2026-11-18, source: "https://www.robotshop.com/products/vector-20-ai-robot-companion"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-11-17, stars: 849, active: true}
use_cases: [companion, hri, education, hobby]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://techcrunch.com/2018/08/08/vector-is-cozmo-for-grownups/", title: "TechCrunch: Vector is Cozmo for grownups (2018-08-08)", accessed: 2026-11-18}
  - {url: "https://en.wikipedia.org/wiki/Anki_(American_company)", title: "Wikipedia: Anki (American company)", accessed: 2026-11-18}
  - {url: "https://www.robotics247.com/article/digital_dream_labs_ships_upgraded_vector_2_0_social_robot", title: "Robotics 24/7: Digital Dream Labs to ship upgraded Vector 2.0 social robot (2022-12-29)", accessed: 2026-11-18}
  - {url: "https://www.techtimes.com/articles/316086/20260422/anki-back-this-time-timing-might-actually-right.htm", title: "TechTimes: Anki Is Back, and This Time the Timing Might Actually Be Right (2026-04-22)", accessed: 2026-11-18}
  - {url: "https://github.com/kercre123/wire-pod", title: wire-pod repository README and LICENSE, accessed: 2026-11-18}
  - {url: "https://github.com/anki/vector-python-sdk", title: Anki Vector Python SDK repository and module docs, accessed: 2026-11-18}
  - {url: "https://www.robotshop.com/products/vector-20-ai-robot-companion", title: "RobotShop: Vector 2.0 AI Robot Companion (Black)", accessed: 2026-11-18}
  - {url: "https://github.com/digital-dream-labs/vector", title: Digital Dream Labs Vector robot source repository and LICENSE, accessed: 2026-11-18}
  - {url: "https://github.com/CtfChan/vector_ros2", title: vector_ros2 community ROS 2 driver, accessed: 2026-11-18}
---

# Vector (Anki, Digital Dream Labs)

A palm-sized home robot on treads with a lift and a screen face, launched by Anki in 2018 [1].
Anki went bankrupt in 2019 and Digital Dream Labs (DDL) bought its assets [2]; DDL sells Vector
2.0 [3] and in 2026 described a rebuilt cloud service [4]. It is the mass-market reference for
small expressive robots, hackable through an Apache-2.0 SDK and the MIT wire-pod server [5][6].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Vector 2.0 (DDL, 2022), the version sold now; Vector 1.0 is Anki's 2018 robot | [3] |
| Degrees of freedom | 4 motors: left and right treads, head tilt (−22° to 45°), lift (32 to 92 mm) | [6] |
| Processor | Qualcomm APQ8009, quad-core | [2] |
| Camera | 1280 x 720, 90° x 50° field of view (SDK docs, Vector 1.0); 2 MP, 120° on Vector 2.0 (maker's claim) | [6][7] |
| Distance sensing | time-of-flight sensor, about 30 to 1,200 mm (useful to about 300 mm), 25° field of view; four cliff sensors | [6] |
| Other sensors | four microphones [1]; touch sensor, accelerometer and gyroscope [6] | [1][6] |
| Display | 184 x 96 pixel colour screen showing the eyes | [6] |
| Runtime | "1 hour and up" on Vector 2.0, up to 30% more than 1.0 (maker's claim) | [3] |
| Parts | about 700 parts, twice as many as Cozmo | [1] |

## How it works

Two tread motors drive the robot, a head motor tilts the face and camera, and a lift motor raises
the arms it uses to pick up its light cube [6]. DDL's published source splits the robot software
into an engine, an animation process with canned animations, a BLE client for the cube and a web
server [8]. Voice commands go to a server over Wi-Fi [5]; it needs no constant phone link [1].

Anki's Python SDK (last commit 2020-04-26) drives the motors and screen and reads the camera,
distance, touch and motion sensors; its setup fetches a token from Anki's account server [6].
wire-pod, built from DDL's open-sourced chipper server, replaces that cloud for voice commands on
any Vector 1.0 or 2.0 at no fee [5]. DDL's robot source repo is under its own Software Asset
License: use only with Vector robots, derivatives sold only for Vector; last changed 2022-05-28,
it still lacks third-party code, and holds Anki's Webots simulator setup (R2018a or R2020a) [8].
No URDF or MJCF exists. vector_ros2 wraps the SDK for ROS 2 Crystal on Ubuntu 18.04; last commit
2019-05-05, no licence stated [9].

## What it is used for

- **Home companion:** it recognises faces, drives back to its charger and, with a subscription,
  answers questions through ChatGPT [2][7].
- **Programming:** Python tutorials drive the motors, read sensors and draw on the screen [6].
- **Self-hosting:** wire-pod keeps robots working without any company cloud [5].

## Cost and BOM

| Item | Price | Type | Date | Source |
|---|---|---|---|---|
| Vector 2.0 at RobotShop, in stock | USD 265.98 | retail | 2026-11-18 | [7] |
| DDL subscription for "Hey Vector" voice and ChatGPT; basic use needs none | USD 9.99 a month or 99.99 a year; one month free | — | 2026-11-18 | [7] |
| Vector 2.0 at launch, plus a subscription | USD 399.99 | retail | 2022-12-29 | [3] |
| Vector 1.0 at launch | USD 250 | retail | 2018-08-08 | [1] |

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Python SDK, examples, docs | Python | [anki/vector-python-sdk](https://github.com/anki/vector-python-sdk) [6] | Apache-2.0 |
| Voice and cloud server | Go | [kercre123/wire-pod](https://github.com/kercre123/wire-pod) [5] | MIT |
| Robot software source | C++, Webots files | [digital-dream-labs/vector](https://github.com/digital-dream-labs/vector) [8] | DDL Software Asset License: Vector-only use, not open source |
| ROS 2 wrapper | ROS 2 Python package | [CtfChan/vector_ros2](https://github.com/CtfChan/vector_ros2) [9] | None stated |
| Hardware | — | Not published | Proprietary |

## Strengths and limits

- **Strengths:** a cheap, finished robot with a lift, depth sensing and an animated face [1][6];
  a documented Apache-2.0 SDK [6]; wire-pod removes the dependence on the company's cloud and is
  active in 2026 [5].
- **Limits:** the maker failed once and the 2026 recovery claims are DDL's own [2][4]; the SDK is
  unmaintained since 2020 [6]; the firmware licence ties code to Vector [8]; no published size,
  mass or robot model, and only a 2019 ROS 2 wrapper [9].

## Related robots

- [Jibo](jibo.md): another consumer social robot whose maker folded and whose servers went dark.
- [Stack-chan](stack-chan.md) and [ElectronBot](electronbot.md): open desk robots with screen faces.

## Sources

1. [TechCrunch: Vector is Cozmo for grownups (2018-08-08)](https://techcrunch.com/2018/08/08/vector-is-cozmo-for-grownups/), accessed 2026-11-18
2. [Wikipedia: Anki (American company)](https://en.wikipedia.org/wiki/Anki_(American_company)), accessed 2026-11-18
3. [Robotics 24/7: Digital Dream Labs to ship upgraded Vector 2.0 social robot (2022-12-29)](https://www.robotics247.com/article/digital_dream_labs_ships_upgraded_vector_2_0_social_robot), accessed 2026-11-18
4. [TechTimes: Anki Is Back, and This Time the Timing Might Actually Be Right (2026-04-22)](https://www.techtimes.com/articles/316086/20260422/anki-back-this-time-timing-might-actually-right.htm), accessed 2026-11-18
5. [wire-pod repository README and LICENSE](https://github.com/kercre123/wire-pod), accessed 2026-11-18
6. [Anki Vector Python SDK repository and module docs](https://github.com/anki/vector-python-sdk), accessed 2026-11-18
7. [RobotShop: Vector 2.0 AI Robot Companion (Black)](https://www.robotshop.com/products/vector-20-ai-robot-companion), accessed 2026-11-18
8. [Digital Dream Labs Vector robot source repository and LICENSE](https://github.com/digital-dream-labs/vector), accessed 2026-11-18
9. [vector_ros2 community ROS 2 driver](https://github.com/CtfChan/vector_ros2), accessed 2026-11-18
