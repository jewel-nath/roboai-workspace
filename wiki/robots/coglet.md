---
type: robot
name: Coglet
summary: Will Cogley's nine-servo animatronic desk companion with a camera in its eye, voice AI and a dual-MCU board; printable and sold as kits, under a non-commercial licence.
tags: [animatronic, desk-robot, esp32-s3, rp2040, pca9685, face-tracking, voice-assistant, xiaozhi, 3d-printed, non-commercial]
category: social
tier: A
openness: partial
maker: Will Cogley / NMRobotics Ltd
year: 2026
license: {hardware: CC-BY-NC-4.0, software: CC-BY-NC-4.0 AND MIT, docs: CC-BY-NC-4.0}
links: {repo: https://github.com/will-cogley/Coglet, docs: https://nmrobots.com/pages/coglet, cad: https://github.com/will-cogley/Coglet/tree/main/3D%20Printing%20Files, paper: , site: https://nmrobots.com/collections/coglet}
specs: {dof: 9, payload_kg: , reach_mm: , mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "9 micro servos, 9 g metal-gear PWM (Kpower M0090 in the parts list; TiankongRC TS90MD sold in the kit)", mcu: [espressif-esp32-s3, raspberry-pi-rp2040, "CogNog board: ESP32-S3 for AI, audio, vision and Wi-Fi; RP2040 for motion; PCA9685 PWM servo driver"], compute: "Grove Vision AI V2 for on-board face tracking; voice and LLM through the XiaoZhi cloud service or a local NMWorkbench server", sensors: [GC0308 camera (ESP32-S3), OV5647 camera in the eye (Grove Vision AI V2), I2S MEMS microphone], sim_models: [], ros2: none}
cost: {type: kit, usd: 189.38, as_of: 2026-11-17, source: https://nmrobots.com/products/coglet-2}
build: {difficulty: 3, hours: , print_hours: }
maturity: {last_commit: 2026-11-14, stars: 448, active: true}
use_cases: [companion, hri, hobby]
evidence: researched
last_verified: 2026-11-17
sources:
  - {url: https://github.com/will-cogley/Coglet, title: Coglet repository README and parts list, accessed: 2026-11-17}
  - {url: https://github.com/will-cogley/Coglet/blob/main/CogNogDatasheet.md, title: CogNog board datasheet, accessed: 2026-11-17}
  - {url: https://github.com/will-cogley/Coglet/blob/main/LICENSE, title: Coglet LICENSE file, accessed: 2026-11-17}
  - {url: https://github.com/will-cogley/Coglet/blob/main/CogletESP/docs/coglet-power.md, title: Coglet power-up and standby power notes, accessed: 2026-11-17}
  - {url: https://github.com/will-cogley/Coglet/blob/main/CogletESP/docs/coglet-web-flasher.md, title: Coglet web flasher guide, accessed: 2026-11-17}
  - {url: https://github.com/will-cogley/Coglet/tree/main/CogletESP/RP2040, title: Coglet RP2040 MicroPython firmware (servoclass.py, vision.py), accessed: 2026-11-17}
  - {url: https://github.com/will-cogley/Coglet/tree/main/3D%20Printing%20Files, title: Coglet 3D printing files (STL and Bambu Studio 3MF), accessed: 2026-11-17}
  - {url: https://nmrobots.com/pages/coglet, title: NMRobotics Coglet knowledge database, accessed: 2026-11-17}
  - {url: https://nmrobots.com/products/coglet-2, title: NMRobotics Coglet Complete Kit listing, accessed: 2026-11-17}
  - {url: https://nmrobots.com/collections/coglet, title: NMRobotics Coglet parts collection, accessed: 2026-11-17}
  - {url: "https://api.frankfurter.dev/v1/latest?from=GBP&to=USD", title: Frankfurter ECB reference rate GBP to USD for 2026-11-17, accessed: 2026-11-17}
  - {url: https://kicktraq.com/projects/willcogley/coglet-open-source-3d-printable-robot-companion-kit/, title: Kicktraq statistics for the Coglet Kickstarter campaign, accessed: 2026-11-17}
  - {url: https://www.roboticgizmos.com/coglet/, title: "Robotic Gizmos: Coglet (2026-03-23)", accessed: 2026-11-17}
  - {url: https://github.com/will-cogley/Coglet/issues, title: Coglet issue tracker, accessed: 2026-11-17}
  - {url: https://github.com/will-cogley/NMWorkbench, title: NMWorkbench local backend repository, accessed: 2026-11-17}
  - {url: https://github.com/will-cogley/Coglet/blob/main/CogletESP/README.md, title: CogletESP README (XiaoZhi AI chatbot firmware), accessed: 2026-11-17}
---

# Coglet

Coglet is a printed animatronic desk companion with nine servos that move its ears, eyelid, mouth,
eyes and neck, a camera inside one eye, and a voice assistant. Will Cogley and his company
NMRobotics designed it, crowdfunded it in 2026 and sell kits [1][9][12][13]. Builders get a
well-documented expressive head and a reusable dual-MCU servo board, under a licence that forbids
commercial use [3].

## Specs

| Item | Value | Source |
|---|---|---|
| Degrees of freedom | 9: right ear, left ear, eyelid, mouth, left eye, right eye, neck pitch, neck roll, base yaw; no gripper | [2] |
| Servos | 9 x 9 g metal-gear PWM micro servos; the listed ones fit tightly, and MG90S servos may also fit | [1] |
| Servo driver | PCA9685, 16 channels; the board powers up to 12 servos | [2] |
| Controller | CogNog V3.0: ESP32-S3 and RP2040, linked by UART | [2] |
| Board size | 72 x 81 mm, 4 layers, four M2.5 mounting holes | [2] |
| Cameras | GC0308 on the ESP32-S3 (a custom part with inverted pins); OV5647 on a Grove Vision AI V2 module, inside the eye, for face tracking | [2][6] |
| Audio | I2S microphone; MAX98357A I2S amplifier and speaker | [2] |
| Power | 5 V, 3 A through a JST-XH input, usually from a USB charger; no battery | [2][4] |
| Printed parts | 60 printed parts and 16 gears (press report) | [13] |
| Size, mass, runtime | Not stated by any source | — |

Payload, reach and speed do not apply to a stationary head.

## How it works

### Mechanics and actuation

Nine hobby servos move the face and neck. Three of them carry the head: base yaw, neck pitch and
neck roll. The other six drive the two ears, the eyelid, the mouth and the two eyeballs [2]. Each
servo output takes a TorqueStar, a spline adapter that NMRobotics sells and that can be printed in
resin [1]. The eyes are separate realistic eyeballs that leave room for a camera; NMRobotics sells
them, and they also fit Cogley's EyeMech eye mechanism [1][10]. Printed skin shells cover the
mechanism [8].

### Electronics and firmware

The CogNog board splits the work between two microcontrollers. The ESP32-S3 handles Wi-Fi, voice,
the GC0308 camera and the speaker; the RP2040 runs animations and servo timing, and drives the
PCA9685 over I2C. The ESP32 sends the RP2040 short text commands over UART that name preset
animations [2]. Each servo socket number is also its PCA9685 channel, so the firmware needs no
remapping table [6]. A USB-serial chip and a selector switch let one USB port program either MCU
[2].

The ESP32-S3 firmware is C++ on ESP-IDF, a fork of the XiaoZhi AI chatbot (MIT), which streams
speech to a cloud service and uses MCP so the language model can call device actions [2][16].
The RP2040 runs MicroPython: animations, dances to music, calibration and face tracking [6]. A
browser flasher updates the ESP32, which then updates the RP2040 by itself over UART [5].

The power code is worth noting. Switching all nine servos on at once can pull the 5 V rail low
enough to reset the board, so the firmware enables them one at a time, heavy axes first, and
releases servo torque when the robot is idle [4].

### Software and control

By default Coglet pairs with the XiaoZhi service (xiaozhi.me) for speech recognition, the language
model and speech output [5]. NMRobotics is building NMWorkbench, a local backend that runs Ollama,
Kokoro TTS and faster-whisper on a PC; its guide recommends Ubuntu, 16 GB RAM and an NVIDIA GPU
with 8 GB VRAM [8]. NMWorkbench's repo holds only a guide and a link to a v0.1.0 release, with no
source or licence file [15].

Face tracking runs on the Grove Vision AI V2. Because the camera moves with the eye, the RP2040
adds the eye's angle at capture time to the pixel error to get the face direction, smooths it,
and turns the base when the eyes reach their limit [6]. Board switches select calibration mode,
which puts every servo in its default pose, and face tracking; a button wiggles all servos to
check their range [2].

### Simulation

No URDF, MJCF or other simulation model was found in the repo or the knowledge database.

## What it is used for

- **Desk companion:** it talks, shows emotion with its face, tracks faces, sets reminders and
  dances to songs [1][5][6].
- **Animatronics practice:** the build covers mechanism printing, servo calibration and two kinds
  of firmware, and the kit page says it is meant for experienced makers [9].
- **Platform for local AI:** the planned offline backend makes it a body for a home-run language
  model [8].

The Kickstarter campaign raised £77,534 against a £10,000 goal from 512 backers [12]. No papers or
courses using Coglet were found.

## Cost and BOM

The README lists the parts with shop links but gives no total [1]. NMRobotics sells a kit built
around its own board. Prices below are as displayed on 2026-11-17, with taxes included and a
10-day lead time; delivery is £10 to most countries [9][10]. USD figures use the ECB reference
rate of 1 GBP = 1.3191 USD for 2026-11-17 [11].

| Kit option | GBP | USD | Type | Source |
|---|---|---|---|---|
| Complete Kit, base: CogNog board, GC0308 camera, Grove Vision AI V2 with camera, 9 servos, 9 TorqueStars, 65 screws, power PCB, microphone PCB, speaker; print the parts yourself | 143.57 | 189.38 | kit | [9] |
| Base kit plus internal printed parts and FDM skin parts, no eyes | 216.73 | 285.89 | kit | [9] |
| Base kit plus realistic eyes, internal printed parts and FDM skin parts | 252.36 | 332.89 | kit | [9] |

The kit page says the base kit is all you need if you own a 3D printer [9]. Parts are
also sold one by one, for example the CogNog board from £42.83 and a realistic eyeball at £39.15
[10]. A 5 V, 3 A USB supply is needed and is not in the list above [2].

## Building it

**Difficulty 3:** about 60 printed parts, nine servos to calibrate and firmware to flash; the
custom board is sold assembled, and assembling it yourself is much harder.

- **Printing:** the parts come as one generic STL and a Bambu Studio 3MF with five plates, set up
  for a Bambu Lab P1S with PLA, a 0.4 mm nozzle, 0.2 mm layers, 15% infill, three walls and
  supports [7]. The 3MF also opens in PrusaSlicer [8]. No print time is stated.
- **Guides:** a build video and the knowledge database; the datasheet's own guide section is a
  stub, and custom wake words are still to come [1][2][8].
- **Power:** use a plain 5 V, 3 A supply. Multi-port chargers and thin cables cause resets that
  look like a boot loop [4]. The USB-to-JST adapter needs a USB-A to USB-C cable, and the
  programming port alone does not power the servos [2].
- **Assembly:** fit the skin shells back first, then front [8]. The GC0308 used is a custom part
  with inverted pins; a datasheet fix covers over- or under-exposed images [2].
- **Pitfalls in the issues:** walls of 0.5 to 0.6 mm that are hard to print (#4), a part that kept
  failing (#10), 3MF files that failed to load in PrusaSlicer (#5, #8), random seams leaving zits
  on the skins (#12, open), and a self-assembled board that did not show up over USB (#7) [14].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Printed parts | STL (one combined file), Bambu Studio 3MF | `3D Printing Files/` | CC-BY-NC-4.0 |
| Editable CAD source | Not published | — | — |
| TorqueStar spline adapter | STL | `3D Printing Files/` | CC-BY-NC-4.0 |
| CogNog V3.0 board | EasyEDA Pro (`.epro2`), PDF schematic; older versions in `PCB/Deprecated/` | `PCB/` | CC-BY-NC-4.0 |
| ESP32-S3 firmware | C++, ESP-IDF; fork of XiaoZhi | `CogletESP/` | MIT for XiaoZhi-derived files, CC-BY-NC-4.0 for the rest |
| RP2040 firmware | MicroPython | `CogletESP/RP2040/` | CC-BY-NC-4.0 |
| Web flasher | HTML, JavaScript | `CogletESP/tools/web_flasher/` | CC-BY-NC-4.0 |
| Board datasheet, parts list | Markdown | repo root | CC-BY-NC-4.0 |
| Translated XiaoZhi guides | PDF | `Translated Docs for XiaoZhi AI/` | None stated |
| NMWorkbench local backend | Binary release only | `will-cogley/NMWorkbench` | None stated |

**Licence:** CC-BY-NC-4.0, a non-commercial licence. Personal, hobby and educational use is free;
selling builds, kits or derived designs needs written permission from NMRobotics [3]. The root
LICENSE says MIT covers only some files in `CogletESP/` derived from XiaoZhi, but does not list
them, while `CogletESP/LICENSE` is a plain MIT file [3]. Treat every Coglet-specific file as
non-commercial. GitHub reads this custom licence file as NOASSERTION. The datasheet points to
STEP files in the repo, but none are there [2].

## Strengths and limits

**Strengths**
- Nine joints give real facial expression with physical eyes, ears, lids and mouth, which a
  screen face cannot match [2].
- The board is documented like a product: block diagram, pinout, power ratings, servo map and
  troubleshooting [2].
- One maker sells every part, and the base kit costs £143.57 if you print the parts [9].
- Active development: the last commit was 2026-11-14, and the Kickstarter raised 7.75 times its
  goal [12].
- The browser flasher updates both MCUs with one click [5].

**Limits**
- Non-commercial licence: no selling builds or derived designs without permission [3].
- Meshes only: STL and 3MF, with no editable CAD, so changing a part means remodelling it.
- The board is in EasyEDA Pro format, with no Gerbers or board BOM in the repo.
- The default voice assistant depends on the XiaoZhi cloud; the local backend is early and needs
  a GPU PC [5][8].
- Tethered to a 5 V, 3 A supply; no battery [2].
- No published size or mass, no simulation model and no ROS 2 support.

## What to reuse

- **Split the MCUs by job:** a Wi-Fi and AI chip for voice and vision, and a second MCU that owns
  servo timing, with a short text protocol between them [2].
- **Socket number = driver channel:** label each servo socket with its PCA9685 channel and skip
  remapping tables [6].
- **Stagger servo power-up** and release torque when idle to avoid brown-outs on USB power [4].
- **Camera in a moving eye:** compute the target from eye angle at capture plus pixel error, then
  hand large motions to the base [6].
- **Bring-up controls on the board:** a calibration switch that sends every servo to its default
  pose and a wiggle-test button make assembly checks quick [2].
- **One-port updates:** let the main MCU update the coprocessor so users flash once from a
  browser [5].

## Related robots

- [Stack-chan](stack-chan.md): a much smaller desk companion with two servos and a screen face,
  fully Apache-2.0.
- [Sesame](sesame.md): another small ESP32 robot with a face, on legs.
- In plain text: Will Cogley's EyeMech eye mechanism, ElectronBot and Reachy Mini.

## Sources

1. [Coglet repository README and parts list](https://github.com/will-cogley/Coglet), accessed 2026-11-17
2. [CogNog board datasheet](https://github.com/will-cogley/Coglet/blob/main/CogNogDatasheet.md), accessed 2026-11-17
3. [Coglet LICENSE file](https://github.com/will-cogley/Coglet/blob/main/LICENSE), accessed 2026-11-17
4. [Coglet power-up and standby power notes](https://github.com/will-cogley/Coglet/blob/main/CogletESP/docs/coglet-power.md), accessed 2026-11-17
5. [Coglet web flasher guide](https://github.com/will-cogley/Coglet/blob/main/CogletESP/docs/coglet-web-flasher.md), accessed 2026-11-17
6. [Coglet RP2040 MicroPython firmware (servoclass.py, vision.py)](https://github.com/will-cogley/Coglet/tree/main/CogletESP/RP2040), accessed 2026-11-17
7. [Coglet 3D printing files (STL and Bambu Studio 3MF)](https://github.com/will-cogley/Coglet/tree/main/3D%20Printing%20Files), accessed 2026-11-17
8. [NMRobotics Coglet knowledge database](https://nmrobots.com/pages/coglet), accessed 2026-11-17
9. [NMRobotics Coglet Complete Kit listing](https://nmrobots.com/products/coglet-2), accessed 2026-11-17
10. [NMRobotics Coglet parts collection](https://nmrobots.com/collections/coglet), accessed 2026-11-17
11. [Frankfurter ECB reference rate GBP to USD for 2026-11-17](https://api.frankfurter.dev/v1/latest?from=GBP&to=USD), accessed 2026-11-17
12. [Kicktraq statistics for the Coglet Kickstarter campaign](https://kicktraq.com/projects/willcogley/coglet-open-source-3d-printable-robot-companion-kit/), accessed 2026-11-17
13. [Robotic Gizmos: Coglet (2026-03-23)](https://www.roboticgizmos.com/coglet/), accessed 2026-11-17
14. [Coglet issue tracker](https://github.com/will-cogley/Coglet/issues), accessed 2026-11-17
15. [NMWorkbench local backend repository](https://github.com/will-cogley/NMWorkbench), accessed 2026-11-17
16. [CogletESP README (XiaoZhi AI chatbot firmware)](https://github.com/will-cogley/Coglet/blob/main/CogletESP/README.md), accessed 2026-11-17
