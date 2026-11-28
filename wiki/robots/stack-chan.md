---
type: robot
name: Stack-chan
summary: Palm-sized M5Stack companion robot that nods and turns its screen face on two servos; Apache-2.0 case, servo board and JavaScript firmware, also sold assembled by M5Stack.
tags: [m5stack, esp32, pan-tilt, desk-robot, moddable, javascript, kawaii, 3d-printed]
category: social
tier: A
openness: full
maker: Shinya Ishikawa (meganetaaan) and the Stack-chan community
year: 2021
license: {hardware: Apache-2.0, software: Apache-2.0, docs: Apache-2.0}
links: {repo: https://github.com/stack-chan/stack-chan, docs: https://stack-chan.github.io/stack-chan/web/, cad: https://github.com/stack-chan/stack-chan/tree/develop/case, paper: , site: https://hackaday.io/project/181344-stack-chan-javascript-driven-super-kawaii-robot}
specs: {dof: 2, payload_kg: , reach_mm: , mass_kg: 0.187, size_mm: "54.0 x 70.5 x 61.5", speed_mps: , runtime_h: }
stack: {actuators: "Two servos for pan and tilt: Feetech SCS0009 serial-bus servos in M5StackChan; DIY builds use SG90 PWM, Futaba RS30X, Feetech SCS0009 or Dynamixel XL330", mcu: [espressif-esp32-s3, "M5Stack core module (ESP32); M5StackChan uses M5Stack CoreS3 (ESP32-S3)"], compute: "on the M5Stack's ESP32; speech and AI services over Wi-Fi", sensors: [camera (CoreS3), dual microphones (CoreS3), 9-axis IMU (CoreS3), capacitive touch screen, head touch panel (M5StackChan), proximity and light sensor (CoreS3), NFC reader (M5StackChan)], sim_models: ["three.js browser simulator with WebAssembly firmware (stack-chan web/simulator)", "URDF xacro (Ar-Ray-code/rostack-chan, community)"], ros2: community}
cost: {type: retail, usd: 99, as_of: 2026-11-17, source: https://shop.m5stack.com/products/stackchan-kawaii-co-created-open-source-ai-desktop-robot}
build: {difficulty: 3, hours: , print_hours: }
maturity: {last_commit: 2026-11-14, stars: 1884, active: true}
use_cases: [companion, hri, education, hobby]
evidence: researched
last_verified: 2026-11-17
sources:
  - {url: https://github.com/stack-chan/stack-chan, title: Stack-chan repository README, accessed: 2026-11-17}
  - {url: https://github.com/stack-chan/stack-chan/blob/develop/case/README.md, title: Stack-chan case v0 guide, accessed: 2026-11-17}
  - {url: https://github.com/stack-chan/stack-chan/blob/develop/case/v1/dynamixel.md, title: Stack-chan case v1.0 (DYNAMIXEL) assembly guide, accessed: 2026-11-17}
  - {url: https://github.com/stack-chan/stack-chan/blob/develop/schematics/README.md, title: Stack-chan schematics README, accessed: 2026-11-17}
  - {url: https://github.com/stack-chan/stack-chan/blob/develop/firmware/README.md, title: Stack-chan firmware README, accessed: 2026-11-17}
  - {url: https://github.com/stack-chan/stack-chan/blob/develop/firmware/docs/flashing-firmware.md, title: Stack-chan guide to building and writing programs, accessed: 2026-11-17}
  - {url: https://github.com/stack-chan/stack-chan/blob/develop/docs/release-notes/v2.0.0.md, title: Stack-chan v2.0.0 release notes, accessed: 2026-11-17}
  - {url: https://docs.m5stack.com/en/StackChan, title: M5Stack StackChan (K151) product documentation, accessed: 2026-11-17}
  - {url: https://github.com/m5stack/StackChan, title: M5Stack StackChan open-source repository, accessed: 2026-11-17}
  - {url: https://www.cnx-software.com/2026/01/13/m5stack-stackchan-is-a-cute-open-source-ai-desktop-robot/, title: "CNX Software: M5Stack StackChan is a cute open-source AI desktop robot (2026-01-13)", accessed: 2026-11-17}
  - {url: https://www.robotshop.com/products/m5stackchan-ai-desktop-robot-esp32-s3, title: RobotShop listing for the M5StackChan AI Desktop Robot, accessed: 2026-11-17}
  - {url: https://certification.oshwa.org/jp000017.html, title: OSHWA certification JP000017 for Stack-chan, accessed: 2026-11-17}
  - {url: https://hackaday.io/project/181344-stack-chan-javascript-driven-super-kawaii-robot, title: Stack-chan project page on Hackaday.io, accessed: 2026-11-17}
  - {url: https://github.com/Ar-Ray-code/rostack-chan, title: rostack-chan ROS 2 interface repository, accessed: 2026-11-17}
  - {url: https://github.com/A-Uta/StackChan_Minimal, title: StackChan Minimal repository, accessed: 2026-11-17}
  - {url: https://www.elektormagazine.com/articles/m5stack-stackchan-esp32-control, title: "Elektor: controlling M5Stack StackChan with ESP32 examples", accessed: 2026-11-17}
  - {url: https://github.com/stack-chan/stack-chan/issues, title: Stack-chan issue tracker, accessed: 2026-11-17}
  - {url: https://shop.m5stack.com/products/stackchan-kawaii-co-created-open-source-ai-desktop-robot, title: M5Stack store listing for M5StackChan K151, accessed: 2026-11-17}
---

# Stack-chan

Stack-chan is a palm-sized desk robot: an M5Stack core module forms its face and brain, and two
servos turn and tilt it. Shinya Ishikawa started it in 2021 and a large, mostly Japanese community
grew around it [1][13]. A builder can make a small, cheap expressive robot from its Apache-2.0
case, servo board and firmware, or buy M5Stack's assembled version and run the same open
firmware on it [1][8].

## Specs

| Item | Value | Source |
|---|---|---|
| Degrees of freedom | 2: pan at the feet (servo ID 1) and tilt at the face (servo ID 2); no gripper | [2] |
| Servo range, DIY case v0 | SG90 0 to 180°, RS30X -150 to 150°, SCS0009 0 to 200°; forward-facing reference angle differs per servo | [2] |
| Servo range, M5StackChan | Horizontal: 360° continuous with feedback. Vertical: 90°, kept within 5 to 85° (maker's claim) | [8] |
| Size, M5StackChan K151 | 54.0 x 70.5 x 61.5 mm, axis order not stated (maker's claim) | [8] |
| Mass, M5StackChan K151 | 187.2 g (maker's claim) | [8] |
| Battery, DIY | 3.7 V LiPo with a PH 2-pin cable; 400 mAh and 640 mAh packs tested | [2] |
| Battery, M5StackChan | 550 mAh (maker's claim) | [8] |
| Controller | M5Stack Basic, Gray, Go or Fire (case v0); M5Stack CoreS3 (case v1.0); M5StackChan uses CoreS3 with ESP32-S3, 16 MB flash, 8 MB PSRAM | [2][3][8] |
| Display | The M5Stack's screen; on CoreS3, a 2.0 in 320 x 240 IPS capacitive touch screen (maker's claim) | [8] |
| Runtime | Not stated by any source | — |

Payload, reach and speed do not apply to a pan-tilt head. CNX Software's January 2026 launch
report gave different M5StackChan figures (70 x 62 x 54 mm, 156 g, 700 mAh) [10]; the table uses
M5Stack's current product page.

## How it works

### Mechanics and actuation

Two servos sit one above the other inside a printed body. The lower servo turns the whole robot on
its feet (pan); the upper one tilts the M5Stack face (tilt). The M5Stack module stacks onto the
front of the shell, and a printed backpack holds the battery [2].

The original case (v0) has variants for three servos: cheap SG90 PWM servos, Futaba RS30X serial
servos and Feetech SCS0009 serial servos. Each servo is mounted at its reference angle, the middle
of its range; a servo mounted the wrong way hits the housing [2]. Case v1.0 is the new standard
but so far only fits Dynamixel XL330 servos. It adds printed gears and a horn, and a narrower
gear in case printed holes come out loose [2][3]. Community cases in `case/contributed/` add
magnetic shells and a version for the M5Go bottom board [2].

M5StackChan, the assembled version, uses two feedback servos; its datasheet list names the
SCS0009. Its firmware limits tilt to M5Stack's recommended 5 to 85° [7][8].

### Electronics and firmware

The Stack-chan board (`m5-pantilt`, KiCad) stacks under the M5Stack. It drives two PWM servos or
two serial servos, breaks out M5Stack Port B, takes external 5 V, and charges the battery through
the M5Stack, with an optional power switch [4]. The schematics page weighs the servo choice: SG90s
are cheap but jerky, draw a high inrush current that can reset the M5Stack, and can overheat when
pushed past the case limits; serial servos cost more but report their angle and allow speed
limits [4]. Takao Akaki's M5Bottom kit skips the custom board and wires the servos to the M5Stack's
own ports [6].

The firmware is TypeScript and JavaScript on the Moddable SDK for the ESP32. A host program holds
the drivers and services; user apps called MODs load separately, so changing an app does not mean
reflashing the host [5]. Drivers cover Feetech, Futaba, Dynamixel and PWM servos. Speech comes
from Stack-chan Voice, VOICEVOX, ElevenLabs or OpenAI, and CoreS3 builds can hold a WebRTC voice
conversation [5]. Release 2.0.0 moved everything to Moddable SDK 10.0.2 [7]. Prebuilt firmware
targets M5Stack Basic, Core2, CoreS3 and M5StackChan CoreS3; Stack-chan RT (Dynamixel) and Takao's
Core2 + SG90 version build from source [1][6].

M5StackChan ships with M5Stack's own factory firmware, a separate code base. M5Stack publishes it,
with the remote controller firmware, phone app and server, under MIT [9]. Flashing the Stack-chan
firmware replaces it; M5Burner restores it [1].

### Software and control

The browser tools need no local toolchain: a Web Serial firmware installer, BLE settings, a MOD
gallery, a Blockly block editor, a face editor, a simulator, and MediaPipe face and hand tracking
that steers the robot over BLE [1]. Other community firmware exists: AI Stack-chan by robo8080
(Arduino) and stack-chan-tester by Takao Akaki for PWM builds [5]. For ROS 2, the community
rostack-chan package drives SCS0009 servos through ros2_control on Humble; its last commit was
2023-08-26 [14].

### Simulation

The main repo has no URDF or MJCF. Its browser simulator runs the firmware compiled to WebAssembly
next to a three.js model built from the v1 shell STL [1]. The community rostack-chan repo has a
URDF (xacro) with the shell, feet and bracket meshes, made for RViz and ros2_control [14].

## What it is used for

- **Companion and voice assistant:** the screen shows the face while the robot looks around,
  tracks faces and talks through cloud or local speech services [1][5][12].
- **Teaching:** the block editor and MOD system suit beginners. Jim Solderitsch, an adjunct
  professor at Villanova University, ported his ESP32 teaching examples to StackChan so students
  move its servos over Wi-Fi [16].
- **Hobby variants:** many builders publish their own cases, boards and apps. StackChan Minimal,
  by A-Uta, is a tiny AtomS3R variant that hands speech recognition and the LLM to a local server
  [15].

No peer-reviewed paper about Stack-chan was found.

## Cost and BOM

The project publishes no BOM total; the board's parts list is marked as under construction [4].

| Option | Price | Type | Date | Source |
|---|---|---|---|---|
| M5StackChan K151, assembled, at the M5Stack store (in stock) | USD 99 | retail | 2026-11-17 | [18] |
| M5StackChan K151 at RobotShop (backorder, US tariffs included) | USD 112.80 | retail | 2026-11-17 | [11] |
| M5StackChan with joystick remote (K151-R) at the M5Stack store | USD 125 | retail | 2026-01-13 | [10] |
| RT Corporation kit with M5Stack | JPY 25,300 incl. tax | kit | not dated on the page | [13] |
| RT Corporation kit without M5Stack | JPY 18,150 incl. tax | kit | not dated on the page | [13] |

The K151-R price comes from a reply by CNX Software's author, not the article body [10]. The RT
Corporation prices are quoted on the Hackaday.io page without a date, so they may be out of
date [13]. For a DIY build, the main costs are an M5Stack core module, two servos, a 3.7 V LiPo
and the Stack-chan board; the case guide links Japanese shops for each [2].

## Building it

**Difficulty 3:** the DIY route means printing the case, having the SMD servo board made or
soldered, setting servo IDs and angles with the maker's tool, and flashing firmware. Buying
M5StackChan instead is a difficulty-1 path.

- **Printing:** STL and STEP files for every part; the case guide shows the print orientation [2].
  For case v1.0, a printing service is an option [3]. No print time is stated.
- **Servo setup:** serial servos share one line, so set IDs first (ID 1 pan, ID 2 tilt). SCS0009s
  are set with Feetech's GUI and a URT-1 adapter; XL330s with Dynamixel Wizard 2, a U2D2 and a 5 V
  supply, at 1 Mbps [2][3].
- **Pitfalls in the docs:** test the servos with firmware before fixing them in the case, since a
  wrongly mounted servo jams [2]. The case guide warns that the Recovery function in Feetech's
  tool left SCS0009s unusable in FD 1.9.8.1 and 1.9.8.2 [2]. Use a tagged release rather than
  `develop`, whose APIs change [5].
- **Pitfalls in the issues:** an SG90 case cracked when a servo was pushed in (#7), the board docs
  had a wrong JLCPCB part number (#173), and M5StackChan needed its tilt range limited (#703) [17].
- **Board files:** the repo's `gerber/` folder holds only silkscreen and drill files, and the
  ordering guide has no links yet; plan to export fabrication files from KiCad yourself [4].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Case v0 (SG90, RS30X, SCS0009) | STEP, STL; Fusion 360 source on A360 | `case/` | Apache-2.0 |
| Case v1.0 (Dynamixel XL330) | STEP, STL | `case/v1/` | Apache-2.0 |
| Battery backpacks, community cases | STEP, STL | `case/backpack/`, `case/contributed/` | Apache-2.0 |
| Servo board `m5-pantilt` | KiCad 7 project, PDF schematic, board STEP | `schematics/m5-pantilt/` | Apache-2.0 |
| Firmware and MODs | TypeScript, JavaScript (Moddable SDK) | `firmware/` | Apache-2.0 |
| Browser tools and simulator | Web app | `web/`, hosted on GitHub Pages | Apache-2.0 |
| Docs | Markdown, English and Japanese | repo | Apache-2.0 |
| M5StackChan factory firmware, remote, app, server | C++, Dart, Go source | `m5stack/StackChan` | MIT |
| M5StackChan body case and PCB | Not found in either repo | — | — |
| URDF | xacro, STL meshes | `Ar-Ray-code/rostack-chan` | Apache-2.0 |

The README puts every resource under Apache-2.0 [1]. Stack-chan holds OSHWA certification
JP000017 from 2022-09-15, whose record lists the hardware licence as "Other" [12].

## Strengths and limits

**Strengths**
- Cheap, small and fast to get running; the assembled M5StackChan costs USD 99 [18].
- Everything in the main repo is Apache-2.0, including the case and board, and it is OSHWA
  certified [1][12].
- Public since 2021 and still active: the last commit was 2026-11-14, and release notes for
  2.0.0 date from October 2026 [7][13].
- One firmware runs on several servo types and M5Stack models [5].
- Browser tools let a beginner flash, configure and program it with no toolchain [1].

**Limits**
- Two degrees of freedom; most of the expression is on the screen.
- DIY documentation lags: no BOM total, no board ordering guide, and case v1.0 fits only the
  more costly Dynamixel XL330 [3][4].
- M5StackChan, now the standard target, has open firmware but no published case or PCB files [9].
- Much of the community material and some design docs are only in Japanese.
- No official URDF or MJCF; the ROS 2 package is old and community-run [14].

## What to reuse

- **The controller as the head:** an off-the-shelf M5Stack gives the screen, speaker, microphones,
  camera, battery charging and Wi-Fi, so the robot body only adds servos and a small board.
- **One board for two servo buses:** the same PCB takes PWM or serial servos, which turns the
  servo choice into a cost decision rather than a redesign [4].
- **Host and MODs:** a stable firmware host with apps loaded separately keeps app work fast [5].
- **Browser-only tooling:** Web Serial flashing, BLE settings and a WebAssembly simulator
  remove the toolchain for users [1].
- **Mount servos at mid-range:** a forward-facing pose at the middle of each servo's range, with
  IDs fixed by joint, makes calibration repeatable [2].

## Related robots

- [Coglet](coglet.md): a larger desk companion with nine servos and mechanical eyes instead of a
  screen face.
- [Sesame](sesame.md): another small ESP32 robot with a face, on legs.
- In plain text: ElectronBot and Reachy Mini are other open desk robots.

## Sources

1. [Stack-chan repository README](https://github.com/stack-chan/stack-chan), accessed 2026-11-17
2. [Stack-chan case v0 guide](https://github.com/stack-chan/stack-chan/blob/develop/case/README.md), accessed 2026-11-17
3. [Stack-chan case v1.0 (DYNAMIXEL) assembly guide](https://github.com/stack-chan/stack-chan/blob/develop/case/v1/dynamixel.md), accessed 2026-11-17
4. [Stack-chan schematics README](https://github.com/stack-chan/stack-chan/blob/develop/schematics/README.md), accessed 2026-11-17
5. [Stack-chan firmware README](https://github.com/stack-chan/stack-chan/blob/develop/firmware/README.md), accessed 2026-11-17
6. [Stack-chan guide to building and writing programs](https://github.com/stack-chan/stack-chan/blob/develop/firmware/docs/flashing-firmware.md), accessed 2026-11-17
7. [Stack-chan v2.0.0 release notes](https://github.com/stack-chan/stack-chan/blob/develop/docs/release-notes/v2.0.0.md), accessed 2026-11-17
8. [M5Stack StackChan (K151) product documentation](https://docs.m5stack.com/en/StackChan), accessed 2026-11-17
9. [M5Stack StackChan open-source repository](https://github.com/m5stack/StackChan), accessed 2026-11-17
10. [CNX Software: M5Stack StackChan is a cute open-source AI desktop robot (2026-01-13)](https://www.cnx-software.com/2026/01/13/m5stack-stackchan-is-a-cute-open-source-ai-desktop-robot/), accessed 2026-11-17
11. [RobotShop listing for the M5StackChan AI Desktop Robot](https://www.robotshop.com/products/m5stackchan-ai-desktop-robot-esp32-s3), accessed 2026-11-17
12. [OSHWA certification JP000017 for Stack-chan](https://certification.oshwa.org/jp000017.html), accessed 2026-11-17
13. [Stack-chan project page on Hackaday.io](https://hackaday.io/project/181344-stack-chan-javascript-driven-super-kawaii-robot), accessed 2026-11-17
14. [rostack-chan ROS 2 interface repository](https://github.com/Ar-Ray-code/rostack-chan), accessed 2026-11-17
15. [StackChan Minimal repository](https://github.com/A-Uta/StackChan_Minimal), accessed 2026-11-17
16. [Elektor: controlling M5Stack StackChan with ESP32 examples](https://www.elektormagazine.com/articles/m5stack-stackchan-esp32-control), accessed 2026-11-17
17. [Stack-chan issue tracker](https://github.com/stack-chan/stack-chan/issues), accessed 2026-11-17
18. [M5Stack store listing for M5StackChan K151](https://shop.m5stack.com/products/stackchan-kawaii-co-created-open-source-ai-desktop-robot), accessed 2026-11-17
