---
type: robot
name: ElectronBot
summary: Peng Zhihui's palm-sized USB desk robot in the style of EVE, with a round screen face, six joints on modified micro servos with custom I2C driver boards, and a PC-side SDK; STEP, Altium PCBs, firmware and Unity app published under GPL-3.0, inactive since early 2025.
tags: [desk-robot, usb, stm32, round-display, gc9a01, servo-hack, i2c, unity, altium, step, fusion-360, gpl]
category: social
tier: B
openness: full
maker: Peng Zhihui (Zhihuijun)
year: 2022
license: {hardware: GPL-3.0-only, software: GPL-3.0-only, docs: GPL-3.0-only}
links: {repo: "https://github.com/peng-zhihui/ElectronBot", docs: "https://github.com/peng-zhihui/ElectronBot/blob/main/enREADME.md", cad: "https://github.com/peng-zhihui/ElectronBot/tree/main/4.CAD-Model", paper: , site: }
specs: {dof: 6, payload_kg: , reach_mm: , mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "6 modified micro servos (small 3 g servos among them), each with a custom ServoDrive board (STM32F042P6, FM116B driver, potentiometer feedback, PID) on an I2C bus", mcu: "STM32F405RGT6 head board with USB3300 USB-HS PHY", compute: "host PC over USB (C++ SDK, Unity app)", sensors: [USB camera, gesture sensor, MPU6050 accelerometer and gyroscope], sim_models: [], ros2: none}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: 4, hours: , print_hours: }
maturity: {last_commit: 2025-02-08, stars: 9609, active: false}
use_cases: [companion, hobby, education]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/peng-zhihui/ElectronBot", title: ElectronBot repository README (Chinese) and files, accessed: 2026-11-18}
  - {url: "https://github.com/peng-zhihui/ElectronBot/blob/main/enREADME.md", title: ElectronBot English README, accessed: 2026-11-18}
  - {url: "https://github.com/peng-zhihui/ElectronBot/blob/main/LICENSE", title: ElectronBot LICENSE file, accessed: 2026-11-18}
  - {url: "https://en.wikipedia.org/wiki/AgiBot", title: "Wikipedia: AgiBot", accessed: 2026-11-18}
---

# ElectronBot

A palm-sized desk robot by Peng Zhihui (稚晖君), styled after EVE from WALL-E, with a round screen
face, six joints and a single USB cable to a PC [1][2]. He published the whole design in 2022,
with CAD, PCBs, firmware and a PC app, and the README links community build videos and a voice
rebuild [1]. Peng later co-founded AgiBot [4]. The repo's last commit was 2025-02-08.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | the original design in `peng-zhihui/ElectronBot` | [1] |
| Degrees of freedom | 6: roll and pitch in each arm, neck, waist; no gripper | [1] |
| Actuators | modified micro servos; each stock board is replaced by a ServoDrive board (STM32F042P6, FM116B motor driver) that reads the potentiometer, runs PID and talks I2C | [1] |
| Main controller | STM32F405RGT6 in the head, with a USB3300 high-speed USB PHY and an SD card | [1] |
| Display | round GC9A01 screen behind a 31.5 mm clear watch-style cover | [1] |
| Sensors | USB camera, gesture sensor and MPU6050 accelerometer and gyroscope on the body board | [1] |
| Connection | USB-C in the base; a USB hub inside joins head, camera and sensors | [1] |

## How it works

The body is printed; Peng recommends HP nylon because the gears need more accuracy than FDM
gives. Arm pitch runs through gears; arm roll uses a T-shaped push rod made from an M2 x 25 mm
half-thread screw, guided in a groove in the arm. An 8-pin flexible cable carries USB past the
turning waist, and some servo tabs must be trimmed to fit [1].

The robot is a USB device, not a computer. The head board drives the screen as a custom USB-CDC
device; an STM32F4 is needed because cheaper families lack high-speed USB with an external PHY.
Each ServoDrive answers I2C commands at its own ID or broadcast address 0, and the head waits 2 s
at power-up for the servos. Firmware is STM32 HAL with CubeMX files, plus an LL servo build for
16 KB parts [1].

The PC does the rest: an SDK stacks a USB layer, a player and a Unity bridge under the Unity app,
with an unsigned Windows USB driver. Emoji clips come as enter, loop and exit parts that chain
smoothly [1]. There is no ROS driver, URDF or simulation model.

## What it is used for

- **Desk companion and PC accessory:** shows animations and video from the PC on its screen [1].
- **Learning embedded design:** a documented example of high-speed USB, servo retrofits and a
  layered host SDK; community guides and a voice version build on it [1].

## Cost and BOM

No BOM total or USD price is published, so `cost` is empty. The README (2022, undated figures)
says the HP nylon parts cost about CNY 200 to 300 at a JLC 3D print service, and each
STM32F042P6 over CNY 10, so Peng suggests a cheaper 8-bit MCU for the servos [1][2].

## Building it

**Difficulty 4:** three custom boards, six servos rebuilt with tiny driver boards, firmware on
each, precise printed gears and a cramped assembly [1].

- **Servos:** swap each board for a ServoDrive, check motor wire polarity, flash it through three
  SH1.0 contacts (a DK board helps debugging), and test servos one at a time, or the bus blocks [1].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Body and storage box | STEP; Fusion 360 source via an A360 link | `4.CAD-Model/` [1] | GPL-3.0 |
| Head, body, base, servo and debug PCBs | Altium Designer, Gerber | `1.Hardware/` [1] | GPL-3.0 |
| Firmware | C/C++, STM32 HAL, CubeMX | `2.Firmware/` [1] | GPL-3.0 |
| SDK, Unity app, USB driver, servo tool | C++, C#, libusb-win32 driver | `3.Software/` [1] | GPL-3.0; bundled third-party parts keep their terms |
| Emoji animations, chip datasheets | video, PDF | `4.CAD-Model/Emoji/`, `5.Docs/` [1] | GPL-3.0; datasheets are the vendors' |

One GPL-3.0 LICENSE covers the repo and the README adds no terms [1][3]. Bundled Unity packages
(Battlehub, UI Widgets, ProceduralUIImage), a font asset (`msyh`) and OpenCV keep their own [1].

## Strengths and limits

- **Strengths:** every layer is published, from STEP and PCBs to firmware and SDK [1]; clever
  mechanics in a palm-sized body [1]; copyleft keeps derivatives open [3].
- **Limits:** a hard build with modified servos and custom boards [1]; Windows host tools with an
  unsigned driver [1]; editing PCBs needs Altium; no size, mass or BOM total; inactive since 2025.

## What to reuse

- **Smart servo retrofit:** a tiny MCU board reads the servo's pot, runs PID and joins an I2C bus
  with IDs [1].
- **Robot as a USB device:** compute stays on the PC; one cable and an internal hub carry it [1].

## Related robots

- [Stack-chan](stack-chan.md), [Coglet](coglet.md), [Reachy Mini](reachy-mini.md): open desk robots.
- [AgiBot X1](agibot-x1.md): an open humanoid from the company Peng co-founded [4].

## Sources

1. [ElectronBot repository README (Chinese) and files](https://github.com/peng-zhihui/ElectronBot), accessed 2026-11-18
2. [ElectronBot English README](https://github.com/peng-zhihui/ElectronBot/blob/main/enREADME.md), accessed 2026-11-18
3. [ElectronBot LICENSE file](https://github.com/peng-zhihui/ElectronBot/blob/main/LICENSE), accessed 2026-11-18
4. [Wikipedia: AgiBot](https://en.wikipedia.org/wiki/AgiBot), accessed 2026-11-18
