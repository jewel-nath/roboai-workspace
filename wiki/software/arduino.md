---
type: tool
name: Arduino
summary: The Arduino framework, a setup()/loop() C++ API and one core per chip family that implements it, driven by arduino-cli or the Arduino IDE; the quickest way to get an AVR, ESP32, RP2040, STM32 or Teensy board driving a robot's motors and sensors.
tags: [arduino, arduino-cli, arduino-ide, sketch, avr, arduino-esp32, arduino-pico, stm32duino, teensyduino, micro-ros, firmware]
kind: framework
area: firmware
support:
license: LGPL-2.1-or-later
links: {repo: "https://github.com/arduino/ArduinoCore-API", docs: "https://docs.arduino.cc", site: "https://www.arduino.cc"}
version: {tested: , latest: "1.5.2", as_of: 2026-11-27}
platforms: [linux, windows, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://github.com/arduino/ArduinoCore-API", title: "ArduinoCore-API repository: README, LICENSE and file headers", accessed: 2026-11-27}
  - {url: "https://github.com/arduino/arduino-cli", title: "arduino-cli repository: README, LICENSE.txt, docs (getting started, installation, sketch project file) and command flags", accessed: 2026-11-27}
  - {url: "https://github.com/arduino/arduino-ide", title: "Arduino IDE 2 repository: README and LICENSE.txt", accessed: 2026-11-27}
  - {url: "https://github.com/espressif/arduino-esp32", title: "Arduino-ESP32 repository: README, LICENSE.md, docs and releases", accessed: 2026-11-27}
  - {url: "https://github.com/earlephilhower/arduino-pico", title: "Arduino-Pico README and LICENSE", accessed: 2026-11-27}
  - {url: "https://github.com/stm32duino/Arduino_Core_STM32", title: "STM32duino Arduino_Core_STM32: README and License.md", accessed: 2026-11-27}
  - {url: "https://www.pjrc.com/teensy/td_download.html", title: "PJRC: Teensyduino download and install", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_arduino", title: "micro_ros_arduino README and branches", accessed: 2026-11-27}
---

# Arduino

A C++ API (`setup()`, `loop()`, `Serial`, `Wire`) plus a core per chip family; arduino-cli and the
IDE build and upload sketches [1][2]. Builders use it for a robot's motor and sensor board. Licences
differ: the API is LGPL-2.1-or-later, arduino-cli GPL-3.0, IDE 2 AGPL-3.0 [1][2][3].

## When to use it

- One loop on one MCU: PWM motors, encoders, servos, a few sensors, USB serial to the computer.
  [TurtleBot3](../robots/turtlebot3.md)'s OpenCR and [OpenBot](../robots/openbot.md) run sketches.
- micro-ROS on bigger boards: prebuilt for Teensy 4.1, 3.6 and 3.2, Portenta H7, Nano RP2040
  Connect, OpenCR and ESP32, but no 8-bit AVR board [8]; a Mega 2560 needs your own serial protocol.
- Not when you need the RTOS, both ESP32 cores or chip config: [ESP-IDF](esp-idf.md),
  [Zephyr](zephyr.md) or [FreeRTOS](freertos.md).

## Setup

arduino-cli 1.6.0 (2026-11-10) and IDE 2.3.11 (2026-11-12) run on Linux, macOS and Windows; the
IDE builds through arduino-cli [2][3]. macOS: `brew install arduino-cli`; Windows: msi or zip [2].

```bash
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh  # ./bin
arduino-cli core update-index && arduino-cli core install arduino:avr
arduino-cli board list --json                              # port and FQBN of attached boards
arduino-cli compile -u -p /dev/ttyACM0 --fqbn arduino:avr:mega MySketch   # build and upload
arduino-cli monitor -p /dev/ttyACM0 -c baudrate=115200
```

| Boards | Core, maintainer, latest | Boards Manager URL, for `--additional-urls` [2] |
|---|---|---|
| Uno, [Mega 2560](../parts/mcu/arduino-mega-2560.md) | `arduino:avr`, Arduino | default index |
| ESP32 family, such as the [ESP32-S3](../parts/mcu/espressif-esp32-s3.md) | Arduino-ESP32, Espressif, 4.0.0 [4] | `https://espressif.github.io/arduino-esp32/package_esp32_index.json` |
| [RP2040](../parts/mcu/raspberry-pi-rp2040.md), RP2350 | Arduino-Pico, Earle Philhower, 6.4.0 [5] | `https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json` |
| STM32, such as the [Nucleo-F446RE](../parts/mcu/st-nucleo-f446re.md) | STM32duino, STMicroelectronics, 3.1.0 [6] | `https://github.com/stm32duino/BoardManagerFiles/raw/main/package_stmicroelectronics_index.json` |
| [Teensy 4.1](../parts/mcu/pjrc-teensy-4-1.md), 4.0, 3.x, LC | Teensyduino, PJRC, 1.62 [7] | `https://www.pjrc.com/teensy/package_teensy_index.json` |

## Traps

- **Core majors break sketches.** Arduino-ESP32 3.x changed APIs from 2.x; 4.0.0 (2026-11-19) is
  built on ESP-IDF 6.1.1 [4]; OpenBot needs 2.0.17. Pin core and library versions in a `sketch.yaml`
  profile; `arduino-cli compile --profile <name>` fetches them into an isolated cache [2].
- **micro_ros_arduino is prebuilt** per board and distro (Humble, Jazzy, Kilted, Rolling; no
  Lyrical); its ESP32 build used core 2.0.2, and Teensyduino needs a patched `platform.txt` [8].
- **Upload fails on Linux:** join `dialout` [4]; Teensy also needs PJRC's `00-teensy.rules` [7].
- **Licences in shipped firmware.** LGPL-2.1 section 6 asks that users can relink your binary with
  a changed core, for example from your object files [1]. Arduino-ESP32 and Arduino-Pico are
  LGPL-2.1 [4][5]; STM32duino adds BSD-3 HALs and ST terms [6]; Teensyduino's vary per file [7].

## Alternatives

[PlatformIO](../tools/platformio.md) pins cores per project; MicroPython. The
[MCU guide](../guides/choose-an-mcu-and-firmware-stack.md) compares the stacks.

## Sources

1. [ArduinoCore-API repository: README, LICENSE and file headers](https://github.com/arduino/ArduinoCore-API), accessed 2026-11-27
2. [arduino-cli repository: README, LICENSE.txt, docs (getting started, installation, sketch project file) and command flags](https://github.com/arduino/arduino-cli), accessed 2026-11-27
3. [Arduino IDE 2 repository: README and LICENSE.txt](https://github.com/arduino/arduino-ide), accessed 2026-11-27
4. [Arduino-ESP32 repository: README, LICENSE.md, docs and releases](https://github.com/espressif/arduino-esp32), accessed 2026-11-27
5. [Arduino-Pico README and LICENSE](https://github.com/earlephilhower/arduino-pico), accessed 2026-11-27
6. [STM32duino Arduino_Core_STM32: README and License.md](https://github.com/stm32duino/Arduino_Core_STM32), accessed 2026-11-27
7. [PJRC: Teensyduino download and install](https://www.pjrc.com/teensy/td_download.html), accessed 2026-11-27
8. [micro_ros_arduino README and branches](https://github.com/micro-ROS/micro_ros_arduino), accessed 2026-11-27
