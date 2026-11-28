---
type: tool
name: Zephyr
summary: Apache-2.0 RTOS with its own build system (west, CMake, Kconfig, devicetree) and vendor-neutral driver APIs for CAN, sensors and USB on boards such as the ESP32-S3, Raspberry Pi Pico, STM32 Nucleo and Teensy 4; micro-ROS ships a Zephyr module.
tags: [zephyr, rtos, firmware, west, kconfig, devicetree, cmake, can, usb, sensors, esp32-s3, rp2040, stm32, teensy, micro-ros, lts]
kind: framework
area: firmware
support:
license: Apache-2.0
links: {repo: "https://github.com/zephyrproject-rtos/zephyr", docs: "https://docs.zephyrproject.org/latest/", site: "https://www.zephyrproject.org"}
version: {tested: , latest: "4.5.0", as_of: 2026-11-27}
platforms: [linux, windows, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://github.com/zephyrproject-rtos/zephyr", title: "Zephyr repository: LICENSE, README files, VERSION, SDK_VERSION, west.yml, arch/, Kconfig files and devicetree bindings (main and v4.5.0, v3.7.2 tags)", accessed: 2026-11-27}
  - {url: "https://docs.zephyrproject.org/latest/releases/index.html", title: "Zephyr docs: Releases and supported releases", accessed: 2026-11-27}
  - {url: "https://docs.zephyrproject.org/latest/project/release_process.html", title: "Zephyr docs: Release process, LTS and hardware support tiers", accessed: 2026-11-27}
  - {url: "https://docs.zephyrproject.org/latest/develop/getting_started/index.html", title: "Zephyr docs: Getting started guide", accessed: 2026-11-27}
  - {url: "https://docs.zephyrproject.org/latest/build/kconfig/setting.html", title: "Zephyr docs: Setting Kconfig configuration values", accessed: 2026-11-27}
  - {url: "https://docs.zephyrproject.org/latest/build/dts/howtos.html", title: "Zephyr docs: Devicetree how-tos", accessed: 2026-11-27}
  - {url: "https://github.com/zephyrproject-rtos/zephyr/tree/main/boards", title: "Zephyr board files and docs: esp32s3_devkitc and espressif/common, rpi_pico, teensy4, nucleo_f446re", accessed: 2026-11-27}
  - {url: "https://docs.zephyrproject.org/latest/contribute/bin_blobs.html", title: "Zephyr docs: Binary blobs", accessed: 2026-11-27}
  - {url: "https://docs.zephyrproject.org/latest/hardware/peripherals/can/index.html", title: "Zephyr docs: CAN controller and CAN shell", accessed: 2026-11-27}
  - {url: "https://docs.zephyrproject.org/latest/hardware/peripherals/sensor/index.html", title: "Zephyr docs: Sensors", accessed: 2026-11-27}
  - {url: "https://docs.zephyrproject.org/latest/releases/migration-guide-4.5.html", title: "Zephyr docs: Migration guide to Zephyr 4.5", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_zephyr_module", title: "micro-ROS module for Zephyr: README, Kconfig, sample and branches", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_setup", title: "micro_ros_setup README and Zephyr config (kilted branch)", accessed: 2026-11-27}
  - {url: "https://micro.vulcanexus.org/docs/overview/hardware/", title: "micro-ROS docs: Supported hardware", accessed: 2026-11-27}
---

# Zephyr

Zephyr is an RTOS that brings its own build system: west fetches the kernel and the vendor HALs,
CMake builds, Kconfig picks features and devicetree describes the board [4][5][6]. A robot builder
uses it to write firmware once against vendor-neutral APIs (GPIO, UART, I2C, CAN, sensors, USB)
and move it between chips from different vendors [7][9][10]. Zephyr is Apache-2.0, a permissive
licence: ship its licence text and notices with the firmware [1]. Some HALs fetch vendor binary
blobs under their own, mostly proprietary, licences, such as the ESP32 radio blobs [7][8].

## When to use it

- **Use it** when the firmware must run on more than one vendor's MCU, or you want ready drivers,
  a shell, USB and networking stacks rather than gluing a vendor SDK together [7][9][10]. The LTS
  line suits a product that must take fixes for years [3]. micro-ROS has a Zephyr module [12][14].
- **Use [FreeRTOS](freertos.md) with the vendor SDK** ([ESP-IDF](esp-idf.md), STM32CubeMX) when
  you need a vendor feature first, or the team knows that SDK; [Arduino](arduino.md) for a quick
  prototype. See [Choose an MCU and firmware stack](../guides/choose-an-mcu-and-firmware-stack.md).
- **Not for** the [Arduino Mega 2560](../parts/mcu/arduino-mega-2560.md): Zephyr has no AVR
  architecture [1]. There is no board file for [OpenCR](../parts/mcu/robotis-opencr.md) [7].

## Releases and maintenance

| Release | Date | End of life | Toolchain | Source |
|---|---|---|---|---|
| 4.5.0, latest stable | 2026-10-28 | 2027-10-28 | Zephyr SDK 1.0.1 | [1][2] |
| 4.4.0 | 2026-04-14 | 2027-04-12 | | [2] |
| 3.7 LTS3 (newest point release 3.7.2) | 2024-07-26 | 2029-07-27 | Zephyr SDK 0.16.9 | [1][2] |

- About two releases a year; 4.6 is due in April 2027. An LTS comes every 2.5 to 3 years and
  lives about 5: two years of bug and security fixes, then security and stability only [2][3].
- Hardware tiers (0 emulation, 1 supported, 2 community, 3 deprecated) are described but not
  formally enforced, and board pages carry no tier [3][7].
- Last commit 2026-11-27; 2,155 open issues; help through mailing lists and Discord [1].

## Boards a robot builder uses

| Board | Build target | Tested features in the board file (not every peripheral) [7] | Flash |
|---|---|---|---|
| [ESP32-S3](../parts/mcu/espressif-esp32-s3.md) DevKitC | `esp32s3_devkitc/esp32s3/procpu`; the second core is a separate `/appcpu` image | GPIO, UART, I2C, SPI, PWM, DMA, Wi-Fi (needs `west blobs fetch hal_espressif`) | `west flash` (esp32 runner); MCUboot optional |
| Raspberry Pi Pico ([RP2040](../parts/mcu/raspberry-pi-rp2040.md)) | `rpi_pico` | GPIO, UART, I2C, SPI, ADC, PWM, USB device; runs on one core only | Default OpenOCD needs a probe; else BOOTSEL and `west flash -r uf2` |
| [Nucleo F446RE](../parts/mcu/st-nucleo-f446re.md) | `nucleo_f446re` | GPIO, I2C, SPI, CAN, counter; console on UART2 at 115200 8N1 | Default STM32CubeProgrammer via ST-LINK; OpenOCD, J-Link |
| [Teensy 4.1](../parts/mcu/pjrc-teensy-4-1.md) and 4.0 | `teensy41`, `teensy40` | GPIO, I2C, USB device, SD, Ethernet (4.1); CAN pins in the pin table, CAN not listed | `teensy` runner after pressing reset; no debugging |

## Setup

Ubuntu 24.04 shown; the guide covers Windows (winget, or WSL) and Apple Silicon macOS, not Intel
Macs. Minimums: CMake 3.28, Python 3.12 [4].

```bash
sudo apt install --no-install-recommends git cmake ninja-build gperf ccache dfu-util \
  device-tree-compiler wget python3-dev python3-venv python3-tk xz-utils file make gcc \
  gcc-multilib g++-multilib libsdl2-dev libmagic1
python3 -m venv ~/zephyrproject/.venv && source ~/zephyrproject/.venv/bin/activate
pip install west
west init -m https://github.com/zephyrproject-rtos/zephyr --mr v4.5.0 ~/zephyrproject
cd ~/zephyrproject && west update && west packages pip --install && west zephyr-export
cd zephyr && west sdk install            # the SDK version this tree names
west build -p always -b nucleo_f446re samples/basic/blinky && west flash
```

`west update` fetches every HAL; west manifest groups skip the ones you do not need [4].

## How an agent works with it

Everything is CLI and text files; the [fw-rtos-micro-ros](../../skills/fw-rtos-micro-ros/SKILL.md)
and [fw-serial-can](../../skills/fw-serial-can/SKILL.md) skills hold the recipes.

- **An application** is `CMakeLists.txt`, `prj.conf` (Kconfig), `src/` and optional
  `boards/<board>.conf` and `boards/<board>.overlay` [5][6]. A CAN example of each:

  ```text
  # prj.conf
  CONFIG_CAN=y
  CONFIG_SHELL=y
  CONFIG_CAN_SHELL=y
  /* boards/nucleo_f446re.overlay */
  &can2 { bitrate = <500000>; };
  ```

- **Build and inspect:** `west build -b <board> -p auto <app>`; `west build -t menuconfig` finds a
  symbol and its dependencies; the merged results are `build/zephyr/.config` and
  `build/zephyr/zephyr.dts`. In CI add `-- -DKCONFIG_WARNING_AS_ERROR=y` [5][6].
- **Check on the board:** the console prints a boot banner; with the CAN shell, `can start <dev>`
  then `can send <dev> 010 1 2 3` puts a frame on the bus to watch with
  [can-utils](../tools/can-utils.md) [9]. Sensors are read through one API of channels and
  triggers [10].
- **micro-ROS** ([micro-ROS](micro-ros.md)): the module repo is a sample app plus
  `modules/libmicroros`. Install `catkin_pkg lark-parser empy colcon-common-extensions` in the
  Zephyr venv, build with `west build -b <board> -p`, and pick the transport (UART, USB CDC, or
  UDP with agent IP and Wi-Fi) under Modules, micro-ROS support in menuconfig. The build clones
  ROS 2 sources for the branch's distro: use the `jazzy` branch with the
  `microros/micro-ros-agent:jazzy` image [12]. Then `ros2 topic list` on the host shows the topics.
- **micro-ROS board lists differ:** the docs site lists the Olimex STM32-E407 and the STM32L4
  Discovery kit IoT for Zephyr [14]; `micro_ros_setup` adds Nucleo F446RE and H743ZI (community)
  and a host emulator, all pinned to Zephyr 2.6.0 [13].

## Traps

- **Overlay ignored.** If `boards/<board>.overlay` exists, `app.overlay` is not read, and a file
  named for the wrong board does nothing. The configure step prints each "Found devicetree
  overlay"; check the result in `build/zephyr/zephyr.dts` [6].
- **Links fail with `undefined reference to __device_dts_ord_N`.** The node exists but its driver
  is not built: enable the subsystem in Kconfig and make sure the node has `status = "okay"` [6].
- **A Kconfig line has no effect.** Assignments whose dependencies are unmet are dropped with only
  a warning; read `build/zephyr/.config`, or fail the build with `KCONFIG_WARNING_AS_ERROR` [5].
- **Version drift.** Each tree names its SDK in `SDK_VERSION` (1.0.1 for 4.5, 0.16.9 for 3.7);
  run `west sdk install` from that tree. `west packages pip --install` can change west itself.
  Pin the tree with `west init --mr`, and read the migration guide at each upgrade [1][4][11].
- **micro-ROS lags Zephyr.** The module was tested on Zephyr 4.0 and 4.1 (SDK 0.16.9-rc3); its last
  commit is 2025-12-15 and it has no Lyrical branch. Its USB transport selects
  `USB_DEVICE_STACK`, which Zephyr marks deprecated, and the sample's `app.overlay` sets STM32 USB
  pins (PA11, PA12): replace it on other boards [1][12]. The `micro_ros_setup` route installs
  Zephyr 2.6.0 with SDK 0.12.4 or 0.13.1, far behind both [13].
- **CAN is silent.** With no `bitrate` in devicetree the controller starts at 125 kbit/s; it must
  be started (`can_start()`) and stopped before retiming [1][9]. On the Nucleo F446RE the default
  bus is `can2` on PB12/PB13; `can1` on PB8/PB9 shares pins with I2C1. The board has no
  transceiver: its doc pairs it with an RS485 CAN shield [7]. SocketCAN works but costs memory [9].
- **ESP32-S3 Wi-Fi does not start.** Run `west blobs fetch hal_espressif` after `west update`.
  Blobs mark the image as tainted, shown in the boot banner [7][8].
- **APIs move.** Zephyr 4.5 moved CANopenNode support out to an external module (see
  [CANopenNode](canopennode.md)) [11]; the sensor docs expect fetch and get to give way to read
  and decode [10].
- **Learning curve.** Three configuration languages (CMake, Kconfig, devicetree) before the first
  line of C; start from a sample for your board and change one file at a time [5][6].

## Alternatives

- [FreeRTOS](freertos.md) with a vendor SDK such as [ESP-IDF](esp-idf.md); [Arduino](arduino.md)
  and [PlatformIO](../tools/platformio.md) for simpler builds.
- NuttX and ChibiOS, inside [PX4](px4.md) and [ArduPilot](ardupilot.md).

## Sources

1. [Zephyr repository: LICENSE, README files, VERSION, SDK_VERSION, west.yml, arch/, Kconfig files and devicetree bindings (main and v4.5.0, v3.7.2 tags)](https://github.com/zephyrproject-rtos/zephyr), accessed 2026-11-27
2. [Zephyr docs: Releases and supported releases](https://docs.zephyrproject.org/latest/releases/index.html), accessed 2026-11-27
3. [Zephyr docs: Release process, LTS and hardware support tiers](https://docs.zephyrproject.org/latest/project/release_process.html), accessed 2026-11-27
4. [Zephyr docs: Getting started guide](https://docs.zephyrproject.org/latest/develop/getting_started/index.html), accessed 2026-11-27
5. [Zephyr docs: Setting Kconfig configuration values](https://docs.zephyrproject.org/latest/build/kconfig/setting.html), accessed 2026-11-27
6. [Zephyr docs: Devicetree how-tos](https://docs.zephyrproject.org/latest/build/dts/howtos.html), accessed 2026-11-27
7. [Zephyr board files and docs: esp32s3_devkitc and espressif/common, rpi_pico, teensy4, nucleo_f446re](https://github.com/zephyrproject-rtos/zephyr/tree/main/boards), accessed 2026-11-27
8. [Zephyr docs: Binary blobs](https://docs.zephyrproject.org/latest/contribute/bin_blobs.html), accessed 2026-11-27
9. [Zephyr docs: CAN controller and CAN shell](https://docs.zephyrproject.org/latest/hardware/peripherals/can/index.html), accessed 2026-11-27
10. [Zephyr docs: Sensors](https://docs.zephyrproject.org/latest/hardware/peripherals/sensor/index.html), accessed 2026-11-27
11. [Zephyr docs: Migration guide to Zephyr 4.5](https://docs.zephyrproject.org/latest/releases/migration-guide-4.5.html), accessed 2026-11-27
12. [micro-ROS module for Zephyr: README, Kconfig, sample and branches](https://github.com/micro-ROS/micro_ros_zephyr_module), accessed 2026-11-27
13. [micro_ros_setup README and Zephyr config (kilted branch)](https://github.com/micro-ROS/micro_ros_setup), accessed 2026-11-27
14. [micro-ROS docs: Supported hardware](https://micro.vulcanexus.org/docs/overview/hardware/), accessed 2026-11-27
