---
type: part
name: PJRC Teensy 4.1
summary: PJRC's 600 MHz Cortex-M7 board (NXP i.MX RT1062) with 1 MB RAM, three CAN controllers (one CAN FD), an on-board 10/100 Ethernet PHY and four hardware quadrature decoders; the fast Arduino-compatible choice for control loops, now made and sold by SparkFun.
tags: [teensy, teensy-4-1, pjrc, imxrt1062, cortex-m7, can, can-fd, ethernet, quadrature-encoder, teensyduino, micro-ros, sparkfun]
category: mcu
subcategory: mcu-board
maker: PJRC
model: Teensy 4.1
specs: {cpu: "Arm Cortex-M7 (NXP i.MX RT1062)", clock_mhz: 600, fpu: double, flash_kb: 7936, sram_kb: 1024, eeprom_kb: 4, logic_v: 3.3, supply_v: "3.6-5.5 via VIN, 5 via USB", gpio: 55, adc_channels: 18, adc_bits: 12, pwm_channels: 35, uart: 8, i2c: 3, spi: 3, can: 3, usb: "480 Mbit/s device on micro-USB, 480 Mbit/s host on pins", board_mm: "60.96 x 17.78"}
interfaces: [uart, i2c, spi, can, usb, ethernet, sdio]
cost: {usd: 31.50, qty: 1, as_of: 2026-11-27, source: "https://www.sparkfun.com/teensy-4-1.html"}
where_to_buy:
  - {seller: PJRC (links to SparkFun), url: "https://www.pjrc.com/store/teensy41.html", as_of: 2026-11-27}
  - {seller: SparkFun, url: "https://www.sparkfun.com/teensy-4-1.html", as_of: 2026-11-27}
datasheet: "https://www.nxp.com/docs/en/nxp/data-sheets/IMXRT1060CEC.pdf"
alternatives: [st-nucleo-f446re, espressif-esp32-s3, raspberry-pi-rp2040, robotis-opencr]
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://www.pjrc.com/store/teensy41.html", title: "PJRC: Teensy 4.1 development board, with schematic and dimensions", accessed: 2026-11-27}
  - {url: "https://www.pjrc.com/teensy/card11a_rev4_web.pdf", title: "PJRC: Teensy 4.1 pinout card, front", accessed: 2026-11-27}
  - {url: "https://www.nxp.com/docs/en/nxp/data-sheets/IMXRT1060CEC.pdf", title: "NXP: i.MX RT1060 Crossover Processors for Consumer Products, Rev. 4, 04/2024", accessed: 2026-11-27}
  - {url: "https://www.sparkfun.com/teensy-4-1.html", title: "SparkFun: Teensy 4.1 (DEV-16771)", accessed: 2026-11-27}
  - {url: "https://www.pjrc.com/store/teensy35.html", title: "PJRC: Teensy 3.5, with the Teensy 3.x supply notice", accessed: 2026-11-27}
  - {url: "https://micro.vulcanexus.org/docs/overview/hardware/", title: "micro-ROS: Supported Hardware", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_setup", title: "micro_ros_setup README, kilted and jazzy branches", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_platformio", title: "micro_ros_platformio README", accessed: 2026-11-27}
---

# PJRC Teensy 4.1

PJRC's board for the NXP i.MX RT1062, an Arm Cortex-M7 at 600 MHz [1]. It suits robots with fast
control loops, many encoders, or a CAN or Ethernet link, such as legged robots and brushless arms.

## Specs

| Spec | Value | Source |
|---|---|---|
| Reference board | Teensy 4.1 with the Ethernet chip (TEENSY41), $31.50 at SparkFun, which now makes Teensy and to which PJRC's store links; TEENSY41_NE lacks the chip. 60.96 x 17.78 mm | [1][4] |
| Core and clock | Cortex-M7, 600 MHz, dual-issue; the FPU does 32-bit float and 64-bit double in hardware | [1] |
| Memory | 8 MB flash, 7936 KB of it for programs (the top 256 KB holds EEPROM data and a restore program); 1024 KB RAM, half tightly coupled; 4 KB emulated EEPROM; pads for two QSPI chips such as 8 MB PSRAM | [1] |
| Logic and power | 3.3 V; no pin is 5 V tolerant except VIN and VUSB; 4 mA recommended per output. VIN 3.6-5.5 V, joined to USB's VUSB until you cut the pads between them; the 3.3 V pin supplies up to 250 mA | [1][2] |
| GPIO, PWM, timers | 55 I/O pins, all with interrupts; 35 PWM pins on FlexPWM and QuadTimer modules, in 22 frequency groups; 4 interval timers | [1][2] |
| Encoder inputs | 4 hardware quadrature encoder/decoders | [1][3] |
| ADC | 2 ADCs; 18 analog pins, up to 12 bits, about 10 usable because of noise | [1][3] |
| UART, I2C, SPI | 8 serial, 3 I2C, 3 SPI; FlexIO can build more | [1] |
| CAN | 3 controllers on pins 22/23, 0/1 and 30/31; one supports CAN FD (64-byte frames, up to 8 Mbps); each needs an external transceiver | [1][2][3] |
| USB | 480 Mbit/s device on micro-USB; 480 Mbit/s host on 5 pins | [1] |
| Ethernet, storage | 10/100 Mbit, DP83825 PHY on board, RJ45 MagJack kit sold separately; micro SD socket on 4-bit SDIO | [1] |

## Using it

- **Toolchains:** the [Arduino](../../software/arduino.md) IDE with PJRC's Teensy add-on from Boards
  Manager is the main one; [PlatformIO](../../tools/platformio.md) (board `teensy41` [8]), Visual
  Micro, CircuitPython (not all hardware) and Makefiles also work [1].
- **micro-ROS:** the micro-ROS site lists Teensy 4.0/4.1 as officially supported on Arduino, over
  USB, UART and Ethernet UDP (4.1 only) [6]. `micro_ros_setup` has no Teensy in its build table and
  links the Arduino and PlatformIO libraries instead [7]. `micro_ros_platformio` builds `teensy41`
  with `serial` or `native_ethernet`, for Humble to Rolling [8].
  See [micro-ROS](../../software/micro-ros.md).
- **To a Linux computer:** USB serial at 480 Mbit/s [1]; Ethernet UDP once the MagJack kit is
  fitted [1][8]; or CAN through a transceiver to a USB-CAN adapter on the computer.
- **Older Teensys:** AutoRally's Teensy LC and Stanford Doggo's Teensy 3.5 are PJRC's Teensy 3.x
  (legacy) line, not recommended for new designs: PJRC does not expect the supply of their 90 nm
  chips to recover, and points users to the 4.0 and 4.1 [5]; the notice does not cover 4.x.

## Traps

- **5 V signals.** No pin is 5 V tolerant [1][2], unlike the Teensy 3.5's digital pins [5]: when
  porting a 3.5 design, level-shift its 5 V encoders and sensors.
- **Back-powered USB port.** VIN and VUSB are joined: do not power VIN while USB is plugged in, or
  cut the pads on the bottom first [1][2]. Feed servos from their own supply.
- **CAN silent on the bus.** Each controller needs a transceiver [1]; only one does CAN FD [3].
  Boards made before July 2021 carry the "A" chip; the "B" chip fixes obscure CAN bus bugs [1].
- **No Ethernet link.** TEENSY41_NE has no PHY; every 4.1 needs the separate MagJack kit [1].
- **Board vanishes from USB.** If running code ignores USB, auto-programming fails: press Program,
  which starts the bootloader; it is not a reset, and there is no reset signal [1].

## Alternatives

- [STM32 Nucleo-F446RE](st-nucleo-f446re.md): the STM32Cube and Zephyr route with CAN [7].
- [ESP32-S3](espressif-esp32-s3.md): Wi-Fi and Bluetooth for far less money; one CAN controller.
- [Raspberry Pi RP2040](raspberry-pi-rp2040.md): the cheapest; PIO for servos, but no FPU or CAN.
- [ROBOTIS OpenCR](robotis-opencr.md): Dynamixel ports and an IMU on the board [6].
- [Arduino Mega 2560](arduino-mega-2560.md): 5 V AVR for shield-based builds and old code.
- Compared in [Choose an MCU and firmware stack](../../guides/choose-an-mcu-and-firmware-stack.md).

## Sources

1. [PJRC: Teensy 4.1 development board, with schematic and dimensions](https://www.pjrc.com/store/teensy41.html), accessed 2026-11-27
2. [PJRC: Teensy 4.1 pinout card, front](https://www.pjrc.com/teensy/card11a_rev4_web.pdf), accessed 2026-11-27
3. [NXP: i.MX RT1060 Crossover Processors for Consumer Products, Rev. 4, 04/2024](https://www.nxp.com/docs/en/nxp/data-sheets/IMXRT1060CEC.pdf), accessed 2026-11-27
4. [SparkFun: Teensy 4.1 (DEV-16771)](https://www.sparkfun.com/teensy-4-1.html), accessed 2026-11-27
5. [PJRC: Teensy 3.5, with the Teensy 3.x supply notice](https://www.pjrc.com/store/teensy35.html), accessed 2026-11-27
6. [micro-ROS: Supported Hardware](https://micro.vulcanexus.org/docs/overview/hardware/), accessed 2026-11-27
7. [micro_ros_setup README, kilted and jazzy branches](https://github.com/micro-ROS/micro_ros_setup), accessed 2026-11-27
8. [micro_ros_platformio README](https://github.com/micro-ROS/micro_ros_platformio), accessed 2026-11-27
