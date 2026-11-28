---
type: tool
name: ESP-IDF
summary: Espressif's official C framework for ESP32 chips, with a dual-core FreeRTOS, the idf.py build and flash CLI, Kconfig settings and a component manager; Arduino-ESP32 and micro-ROS's ESP32 component build on it.
tags: [esp-idf, esp32, esp32-s3, espressif, idf-py, eim, freertos, sdkconfig, menuconfig, component-manager, micro-ros, firmware]
kind: framework
area: firmware
support:
license: Apache-2.0
links: {repo: "https://github.com/espressif/esp-idf", docs: "https://docs.espressif.com/projects/esp-idf/en/stable/", site: "https://idf.espressif.com"}
version: {tested: , latest: "6.1.1", as_of: 2026-11-27}
platforms: [linux, windows, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://github.com/espressif/esp-idf", title: "ESP-IDF repository: README, SUPPORT_POLICY.md, LICENSE, .gitmodules and releases", accessed: 2026-11-27}
  - {url: "https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/get-started/linux-macos-start-project.html", title: "ESP-IDF docs: Start a project on Linux and macOS", accessed: 2026-11-27}
  - {url: "https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/get-started/linux-setup.html", title: "ESP-IDF docs: Installation on Linux with EIM", accessed: 2026-11-27}
  - {url: "https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/tools/idf-py.html", title: "ESP-IDF docs: IDF frontend, idf.py", accessed: 2026-11-27}
  - {url: "https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/build-system.html", title: "ESP-IDF docs: Build system", accessed: 2026-11-27}
  - {url: "https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/freertos_idf.html", title: "ESP-IDF docs: FreeRTOS (IDF)", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_espidf_component/tree/jazzy", title: "micro_ros_espidf_component README and manifest, jazzy branch", accessed: 2026-11-27}
  - {url: "https://docs.espressif.com/projects/arduino-esp32/en/latest/esp-idf_component.html", title: "Arduino-ESP32 docs: Arduino as an ESP-IDF component", accessed: 2026-11-27}
---

# ESP-IDF

Espressif's framework for its ESP32 chips: drivers, Wi-Fi and Bluetooth, a two-core FreeRTOS and
a CMake build driven by `idf.py` [1][6]. Builders use it for ESP32 motor, sensor or micro-ROS
firmware. Apache-2.0; the Wi-Fi, Bluetooth and PHY code ships as precompiled libraries [1].

## When to use it

- ESP32 firmware that needs the whole chip: both cores, any Kconfig option, micro-ROS over Wi-Fi
  [7]. [ODRI Solo](../robots/odri-solo.md)'s master board runs on it.
- [Arduino](arduino.md) is ESP-IDF underneath and can be an ESP-IDF component; it needs
  `CONFIG_FREERTOS_HZ=1000` [8]. See the [MCU guide](../guides/choose-an-mcu-and-firmware-stack.md).

## Setup

v6.1.1 (2026-11-16) is the newest release; v6.1 came out on 2026-08-27 [1]. A line gets 30 months:
12 of service, for new projects, then 18 of severe- and security-fix maintenance [1], so v6.1 is in
service to about 2027-08. All lines cover ESP32, -S2, -S3, -C2, -C3, -C6 and -H2; -P4 needs v5.3,
-C5 and -C61 v5.5.2, -S31 v6.1 [1]. EIM installs it on Linux, Windows or macOS; Python 3.10+ [1][3].

```bash
echo "deb [trusted=yes] https://dl.espressif.com/dl/eim/apt/ stable main" | sudo tee \
  /etc/apt/sources.list.d/espressif.list     # trusted=yes: apt skips signature checks [3]
sudo apt update && sudo apt install eim-cli && eim install   # latest stable; or `eim wizard`
source ~/.espressif/tools/activate_idf_v6.1.1.sh             # the exact command EIM prints [2]
cp -r $IDF_PATH/examples/get-started/hello_world . && cd hello_world
idf.py set-target esp32s3 && idf.py -p /dev/ttyUSB0 flash monitor   # Ctrl+] leaves the monitor
```

## How an agent works with it

- Keep changed options in `sdkconfig.defaults` and `sdkconfig.defaults.<target>` [5]: `set-target`
  regenerates `sdkconfig` [4]. `idf.py size-components` shows memory use per component [4].
- `idf.py add-dependency "<ns>/<name>^<ver>"` pins versions in `dependencies.lock` [5][7];
  `idf.py mcp-server` (EIM's `mcp` feature) gives an agent build, flash and set-target tools [4].
- **micro-ROS on Jazzy:** add `micro-ros/micro_ros_espidf_component^24` (the major is the distro's
  year), pip-install `catkin_pkg colcon-common-extensions lark` in the IDF environment, pick the
  transport in menuconfig, run `microros/micro-ros-agent:jazzy udp4 --port 8888` [7].

## Traps

- **Stack sizes are in bytes,** not vanilla FreeRTOS's words: 1024 meant as words is a quarter [6].
- **Two cores.** Suspending the scheduler is no lock; critical sections take a spinlock; a task
  using `float` is pinned to its core; no FPU in interrupts by default [6].
- **micro-ROS lags.** The Jazzy component is tested on v5.2 to v6.0, not v6.1; there is no Lyrical
  branch; build it in a shell without ROS 2 sourced [7]. See [micro-ROS](micro-ros.md).
- **"Permission denied" on the serial port** (Linux): join the `dialout` or `uucp` group [2].

## Alternatives

[PlatformIO](../tools/platformio.md), [Zephyr](zephyr.md), [FreeRTOS](freertos.md), MicroPython.
Board page: [ESP32-S3](../parts/mcu/espressif-esp32-s3.md).

## Sources

1. [ESP-IDF repository: README, SUPPORT_POLICY.md, LICENSE, .gitmodules and releases](https://github.com/espressif/esp-idf), accessed 2026-11-27
2. [ESP-IDF docs: Start a project on Linux and macOS](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/get-started/linux-macos-start-project.html), accessed 2026-11-27
3. [ESP-IDF docs: Installation on Linux with EIM](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/get-started/linux-setup.html), accessed 2026-11-27
4. [ESP-IDF docs: IDF frontend, idf.py](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/tools/idf-py.html), accessed 2026-11-27
5. [ESP-IDF docs: Build system](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/build-system.html), accessed 2026-11-27
6. [ESP-IDF docs: FreeRTOS (IDF)](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/freertos_idf.html), accessed 2026-11-27
7. [micro_ros_espidf_component README and manifest, jazzy branch](https://github.com/micro-ROS/micro_ros_espidf_component/tree/jazzy), accessed 2026-11-27
8. [Arduino-ESP32 docs: Arduino as an ESP-IDF component](https://docs.espressif.com/projects/arduino-esp32/en/latest/esp-idf_component.html), accessed 2026-11-27
