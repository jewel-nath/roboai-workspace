---
type: tool
name: PlatformIO
summary: A Python build system and package manager for microcontroller firmware; one platformio.ini per project pins the platform, framework (Arduino, ESP-IDF and others), board and libraries, and the pio CLI builds, uploads, monitors and runs unit tests.
tags: [platformio, pio, platformio-ini, build-system, arduino, esp-idf, espressif32, pioarduino, teensy, unit-testing, micro-ros, firmware]
kind: tool
area: firmware
support: documented
license: Apache-2.0
links: {repo: "https://github.com/platformio/platformio-core", docs: "https://docs.platformio.org", site: "https://platformio.org"}
version: {tested: , latest: "6.2.0", as_of: 2026-11-27}
platforms: [linux, windows, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://github.com/platformio/platformio-core", title: "PlatformIO Core repository: README, LICENSE, HISTORY.rst and issues", accessed: 2026-11-27}
  - {url: "https://docs.platformio.org/en/latest/core/installation/methods/installer-script.html", title: "PlatformIO docs: installer script", accessed: 2026-11-27}
  - {url: "https://docs.platformio.org/en/latest/core/installation/udev-rules.html", title: "PlatformIO docs: 99-platformio-udev.rules", accessed: 2026-11-27}
  - {url: "https://docs.platformio.org/en/latest/core/userguide/cmd_test.html", title: "PlatformIO docs: pio test", accessed: 2026-11-27}
  - {url: "https://docs.platformio.org/en/latest/platforms/espressif32.html", title: "PlatformIO docs: Espressif 32 platform", accessed: 2026-11-27}
  - {url: "https://github.com/platformio/platform-espressif32", title: "platform-espressif32 repository: README, platform.json, boards, ESP-IDF builder and v8.0.0 release notes", accessed: 2026-11-27}
  - {url: "https://github.com/pioarduino/platform-espressif32", title: "pioarduino platform-espressif32: README, platform.json and releases", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_platformio", title: "micro_ros_platformio README and CI platformio.ini", accessed: 2026-11-27}
---

# PlatformIO

PlatformIO Core is a Python build system and package manager for firmware: `pio` fetches a
project's toolchain, framework and libraries, then builds, uploads, monitors and tests [1]. It keeps
Arduino or ESP-IDF robot firmware reproducible; the
[Robot Soccer Kit](../robots/robot-soccer-kit.md) uses it.

## When to use it

- Firmware that must build the same on every machine and in CI: `platformio.ini` pins platform,
  framework, board and libraries, one `[env:...]` per board [6]. A VS Code extension wraps it [8].
- micro-ROS on Teensy, Portenta H7, ESP32 (`esp32dev`), Pico or Pico 2 via micro_ros_platformio [8].

## Setup

Core 6.2.0 (2026-09-05) is Apache-2.0, needs Python 3.9 or newer, and is maintained by PlatformIO
Labs; 263 issues were open on 2026-11-27 [1]. `python3 get-platformio.py`, from the
platformio-core-installer repo, builds a virtual environment in `~/.platformio/penv` [2][7]:

```ini
[env:esp32s3]
platform = espressif32 @ 8.0.0      ; pin the platform version [6]
board = esp32-s3-devkitc-1
framework = arduino                 ; or espidf, or "arduino, espidf" [6]
```

## How an agent works with it

- `pio run -t upload -p /dev/ttyUSB0` builds and flashes; `pio device monitor` shows the log [1].
- ESP-IDF: `pio run -t menuconfig`; the generated `sdkconfig.<env>` is a build artifact, so commit
  `sdkconfig.defaults` and ignore `sdkconfig.*` [5][6]. Partitions: `board_build.partitions` [5].
- Tests in `test/`: `pio test -e <env>` builds, uploads and runs them on the board over serial;
  `--without-uploading`, `--junit-output-path` for CI [4]. Unity, GoogleTest, Doctest included [1].
- micro-ROS: `lib_deps = https://github.com/micro-ROS/micro_ros_platformio` and
  `board_microros_distro = jazzy`; check with the `microros/micro-ros-agent:jazzy` image [8].

## Traps

- **Which ESP32 platform.** The official `espressif32` shipped Arduino-ESP32 2.0.17 up to 7.1.3;
  8.0.0 (2026-10-19) has Arduino-ESP32 3.3.12 and ESP-IDF 6.1 but no ESP32-C5, -C61, -H2 or -P4
  boards [6]. The fork pioarduino (61.04.00, 2026-11-19) has Arduino-ESP32 4.0.0 on ESP-IDF 6.1.1
  and those boards [7]. Official 8.0.0 for 3.x on common chips; pioarduino for 4.x or new chips.
- **micro_ros_platformio defaults to Kilted**: set `board_microros_distro` (humble, jazzy, kilted,
  rolling; no Lyrical). It needs git, cmake and pip on the host; its last release is 2.0.0 (2023);
  its CI builds the Pico boards on the maxgerhardt platform-raspberrypi fork [8].
- **Upload fails on Linux:** add `99-platformio-udev.rules`, join `dialout` and `plugdev` [3].
- **Windows long paths** break package extraction with "FileNotFoundError"; enable long paths [1].

## Alternatives

[Arduino](../software/arduino.md); [ESP-IDF](../software/esp-idf.md) for the newest IDF;
[Zephyr](../software/zephyr.md); the [MCU guide](../guides/choose-an-mcu-and-firmware-stack.md).

## Sources

1. [PlatformIO Core repository: README, LICENSE, HISTORY.rst and issues](https://github.com/platformio/platformio-core), accessed 2026-11-27
2. [PlatformIO docs: installer script](https://docs.platformio.org/en/latest/core/installation/methods/installer-script.html), accessed 2026-11-27
3. [PlatformIO docs: 99-platformio-udev.rules](https://docs.platformio.org/en/latest/core/installation/udev-rules.html), accessed 2026-11-27
4. [PlatformIO docs: pio test](https://docs.platformio.org/en/latest/core/userguide/cmd_test.html), accessed 2026-11-27
5. [PlatformIO docs: Espressif 32 platform](https://docs.platformio.org/en/latest/platforms/espressif32.html), accessed 2026-11-27
6. [platform-espressif32 repository: README, platform.json, boards, ESP-IDF builder and v8.0.0 release notes](https://github.com/platformio/platform-espressif32), accessed 2026-11-27
7. [pioarduino platform-espressif32: README, platform.json and releases](https://github.com/pioarduino/platform-espressif32), accessed 2026-11-27
8. [micro_ros_platformio README and CI platformio.ini](https://github.com/micro-ROS/micro_ros_platformio), accessed 2026-11-27
