---
type: part
name: ROBOTIS OpenCR 1.0
summary: ROBOTIS's open robot controller, an STM32F746 Cortex-M7 board with three TTL and three RS-485 Dynamixel ports, an IMU and 12 V and 5 V power outputs; the low-level board of TurtleBot3, which reads it over the Dynamixel protocol rather than micro-ROS.
tags: [mcu, stm32, stm32f7, cortex-m7, robotis, dynamixel, turtlebot3, robot-controller, imu, arduino, micro-ros]
category: mcu
subcategory: robot-controller
maker: ROBOTIS
model: OpenCR 1.0
specs: {cpu: "Arm Cortex-M7 (STM32F746ZGT6)", clock_mhz: 216, fpu: single, flash_kb: 1024, sram_kb: , logic_v: 3.3, supply_v: "5-24 via battery or SMPS, 5 via USB", gpio: 50, adc_channels: 6, adc_bits: 12, pwm_channels: 6, uart: 2, i2c: 1, spi: 1, can: 1, usb: "Micro-B, USB 2.0 OTG", board_mm: "105 x 75"}
interfaces: [uart, i2c, spi, can, usb]
cost: {usd: 247.14, qty: 1, as_of: 2026-11-27, source: "https://robotis.us/products/opencr1-0"}
where_to_buy:
  - {seller: ROBOTIS US, url: "https://robotis.us/products/opencr1-0", as_of: 2026-11-27}
  - {seller: RobotShop, url: "https://www.robotshop.com/products/robotis-opencr10-open-source-ros-controller-for-dynamixel", as_of: 2026-11-27}
datasheet: "https://www.st.com/resource/en/datasheet/stm32f746zg.pdf"
alternatives: [st-nucleo-f446re, pjrc-teensy-4-1, espressif-esp32-s3]
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://docs.robotis.com/docs/parts/controller/opencr10/", title: "ROBOTIS Docs: OpenCR 1.0", accessed: 2026-11-27}
  - {url: "https://github.com/ROBOTIS-GIT/OpenCR", title: "OpenCR repository: README, licence, board package index and commit history", accessed: 2026-11-27}
  - {url: "https://github.com/ROBOTIS-GIT/OpenCR-Hardware", title: "OpenCR-Hardware repository", accessed: 2026-11-27}
  - {url: "https://emanual.robotis.com/docs/en/platform/turtlebot3/opencr_setup/", title: "ROBOTIS e-Manual: TurtleBot3 OpenCR setup (Jazzy tab)", accessed: 2026-11-27}
  - {url: "https://github.com/ROBOTIS-GIT/turtlebot3/tree/jazzy/turtlebot3_node", title: "turtlebot3_node, jazzy branch: package.xml, param/burger.yaml, control_table.hpp", accessed: 2026-11-27}
  - {url: "https://micro.vulcanexus.org/docs/overview/hardware/", title: "micro-ROS docs: supported hardware", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_arduino", title: "micro_ros_arduino README, kilted branch", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_setup", title: "micro_ros_setup README, kilted branch", accessed: 2026-11-27}
---

# ROBOTIS OpenCR 1.0

ROBOTIS's open-source control board: an STM32F746 Cortex-M7 with Dynamixel TTL and RS-485 ports,
an IMU and 12 V and 5 V outputs, made to sit between a Linux computer and a Dynamixel bus [1].
[TurtleBot3](../../robots/turtlebot3.md) and [ROBOTIS OP3](../../robots/robotis-op3.md) (as a
sub-controller) use it; [OpenManipulator-X](../../robots/openmanipulator-x.md) can.

## Specs

| Spec | Value | Source |
|---|---|---|
| Core, memory | STM32F746ZGT6, Cortex-M7 with FPU, 216 MHz; 1 MB internal flash with the bootloader at its lowest address; ROBOTIS does not state the SRAM | [1] |
| IMU | ICM-20648 3-axis gyro and accelerometer since 2020; older boards carry an MPU9250 | [1] |
| Logic | 3.3 V; pins marked FT tolerate 5 V except in analog mode; all I/O together source or sink at most 120 mA | [1] |
| Supply | 5-24 V from a battery or SMPS (defaults: 11.1 V LiPo, 12 V 4.5 A SMPS), or 5 V from USB; 10 A input fuse; a switch hot-swaps between SMPS and battery | [1] |
| Power out | 12 V up to 4.5 A, 5 V up to 4 A (made from the 12 V rail), 3.3 V at 800 mA; 12 V and 5 V loads together at most 55 W | [1] |
| Ports | 3 Dynamixel TTL (3-pin), 3 Dynamixel RS-485 (4-pin), 2 UART, 1 CAN | [1] |
| I/O | 32 Arduino-header pins (6 PWM, 1 I2C, 1 SPI), an 18-pin GPIO header and 4 ROBOTIS 5-pin ports; 6 ADC inputs, 12-bit | [1] |
| USB, size | Micro-B USB 2.0 OTG; programming over JTAG/SWD, USB DFU or the serial bootloader; 105 x 75 mm, 60 g | [1] |

## Using it

- **[Arduino](../../software/arduino.md).** Add the `package_opencr_index.json` URL from the
  OpenCR repo's `arduino/opencr_release/` folder to the board manager [1][2]. The newest package is
  1.5.3, built with GCC ARM 5.4 (2016q2); its tools exist only for x86 Linux, Windows and macOS
  [2]. On Linux, add the `99-opencr-cdc.rules` udev rule and `libncurses5-dev:i386` [1].
- **Firmware.** The OpenCR repo holds the bootloader, the Arduino core and released TurtleBot3
  firmware under Apache-2.0; its last commit is from 2023-08-01 [2]. The bootloader updates over
  USB DFU with `dfu-util`; holding SW2 at power-on or reset keeps it in the bootloader [1].
- **TurtleBot3 on Jazzy.** On the Pi, add the `armhf` architecture and `libc6:armhf`, fetch
  `opencr_update.tar.bz2` from ROBOTIS's OpenCR-Binaries repo (`turtlebot3/ROS2/latest`), and run
  `./update.sh /dev/ttyACM0 burger.opencr` (or `waffle.opencr`) [4].
- **How TurtleBot3 talks to ROS 2: not micro-ROS.** `turtlebot3_node` on the Pi uses DynamixelSDK
  and reads the OpenCR over USB as Dynamixel ID 200 at 1 Mbit/s, Protocol 2.0 [4][5]. Its control
  table takes velocity commands and returns wheel positions, velocities and currents, IMU, battery
  voltage and buttons, which the node publishes as ROS 2 topics [5].
- **[micro-ROS](../../software/micro-ros.md)** for your own firmware: the micro-ROS hardware page
  lists OpenCR 1.0 as officially supported over USB and UART [6], micro_ros_arduino from board
  package 1.4.16 [7]; the `micro_ros_setup` README, which builds RTOS firmware, omits it [8].
- **Open hardware.** OpenCR-Hardware holds the OrCAD schematic (also a revision H PDF), layout,
  Gerbers and BOM; its README says they may be shared under open-source licences but names none,
  and the repo has no licence file [3]. Ask ROBOTIS before reusing the design.

## Traps

- **Upload fails on Linux.** After an upload the board re-enumerates and ModemManager sends it AT
  commands; purge `modemmanager` [1]. If it hangs, hold SW2 through a reset and reflash [1][4].
- **Building on a Pi.** The Arduino tools exist only for x86, Windows and macOS hosts [2]: build
  on a PC. The TurtleBot3 updater needs the 32-bit `armhf` C library on the Pi [4].
- **Overloaded outputs.** 12 V and 5 V share 55 W, and 5 V is made from 12 V [1]: count the SBC.
- **Stock.** On 2026-11-27 ROBOTIS US showed it sold out and RobotShop on backorder: order early.

## Alternatives

- [Nucleo-F446RE](st-nucleo-f446re.md): a bare STM32 board with two CAN controllers; you add the
  Dynamixel interface and power stage. [Teensy 4.1](pjrc-teensy-4-1.md): faster, official micro-ROS
  [6], no Dynamixel ports. [ESP32-S3](espressif-esp32-s3.md): micro-ROS over Wi-Fi.
- A U2D2 adapter and power hub drive Dynamixels from a PC, OpenManipulator-X's other option.
- Compared in [Choose an MCU and firmware stack](../../guides/choose-an-mcu-and-firmware-stack.md).

## Sources

1. [ROBOTIS Docs: OpenCR 1.0](https://docs.robotis.com/docs/parts/controller/opencr10/), accessed 2026-11-27
2. [OpenCR repository: README, licence, board package index and commit history](https://github.com/ROBOTIS-GIT/OpenCR), accessed 2026-11-27
3. [OpenCR-Hardware repository](https://github.com/ROBOTIS-GIT/OpenCR-Hardware), accessed 2026-11-27
4. [ROBOTIS e-Manual: TurtleBot3 OpenCR setup (Jazzy tab)](https://emanual.robotis.com/docs/en/platform/turtlebot3/opencr_setup/), accessed 2026-11-27
5. [turtlebot3_node, jazzy branch: package.xml, param/burger.yaml, control_table.hpp](https://github.com/ROBOTIS-GIT/turtlebot3/tree/jazzy/turtlebot3_node), accessed 2026-11-27
6. [micro-ROS docs: supported hardware](https://micro.vulcanexus.org/docs/overview/hardware/), accessed 2026-11-27
7. [micro_ros_arduino README, kilted branch](https://github.com/micro-ROS/micro_ros_arduino), accessed 2026-11-27
8. [micro_ros_setup README, kilted branch](https://github.com/micro-ROS/micro_ros_setup), accessed 2026-11-27
