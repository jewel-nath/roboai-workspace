---
type: part
name: ST NUCLEO-F446RE
summary: ST's Nucleo-64 board for the STM32F446RE, a 180 MHz Cortex-M4F with two CAN controllers, hardware encoder timers and an onboard ST-LINK debugger; the wiki's STM32 reference board, from the F4 family the Atlas's STM32 robots use.
tags: [mcu, stm32, stm32f4, nucleo, cortex-m4, can, bxcan, st-link, stm32cube, zephyr, micro-ros, freertos]
category: mcu
subcategory: dev-board
maker: STMicroelectronics
model: NUCLEO-F446RE
specs: {cpu: "Arm Cortex-M4 (STM32F446RET6)", clock_mhz: 180, fpu: single, flash_kb: 512, sram_kb: 128, logic_v: 3.3, supply_v: "5 via ST-LINK USB; external 3.3, 5 or 7-12", gpio: 50, adc_channels: 16, adc_bits: 12, uart: 6, i2c: 3, spi: 4, can: 2, usb: "ST-LINK/V2-1 (flashing, SWD debug, virtual COM port); OTG FS and HS on the chip", board_mm: }
interfaces: [uart, i2c, spi, can, usb]
cost: {usd: 18.82, qty: 1, as_of: 2026-11-27, source: "https://www.digikey.com/en/products/detail/stmicroelectronics/NUCLEO-F446RE/5347712"}
where_to_buy:
  - {seller: STMicroelectronics, url: "https://www.st.com/en/evaluation-tools/nucleo-f446re.html", as_of: 2026-11-27}
  - {seller: DigiKey, url: "https://www.digikey.com/en/products/detail/stmicroelectronics/NUCLEO-F446RE/5347712", as_of: 2026-11-27}
datasheet: "https://www.st.com/resource/en/datasheet/stm32f446re.pdf"
alternatives: [pjrc-teensy-4-1, espressif-esp32-s3, robotis-opencr, arduino-mega-2560, raspberry-pi-rp2040]
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://docs.zephyrproject.org/latest/boards/st/nucleo_f446re/doc/index.html", title: "Zephyr docs: ST Nucleo F446RE", accessed: 2026-11-27}
  - {url: "https://www.digikey.com/en/products/detail/stmicroelectronics/NUCLEO-F446RE/5347712", title: "DigiKey: STMicroelectronics NUCLEO-F446RE", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_setup", title: "micro_ros_setup README, kilted branch", accessed: 2026-11-27}
  - {url: "https://micro.vulcanexus.org/docs/overview/hardware/", title: "micro-ROS docs: supported hardware", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_stm32cubemx_utils", title: "micro_ros_stm32cubemx_utils README, kilted branch", accessed: 2026-11-27}
  - {url: "https://stm32duino.github.io/dev/supported-boards/", title: "STM32duino: supported boards", accessed: 2026-11-27}
  - {url: "https://docs.platformio.org/en/latest/boards/ststm32/nucleo_f446re.html", title: "PlatformIO docs: nucleo_f446re board", accessed: 2026-11-27}
  - {url: "https://docs.zephyrproject.org/latest/boards/st/nucleo_g474re/doc/index.html", title: "Zephyr docs: ST Nucleo G474RE", accessed: 2026-11-27}
---

# ST NUCLEO-F446RE

ST's Nucleo-64 board for the STM32F446RE: a 180 MHz Cortex-M4 with FPU, two CAN controllers and an
onboard ST-LINK debugger, with Arduino Uno and ST morpho headers [1]. It suits robots with CAN
motor drivers or quadrature encoders that talk to a Linux computer over USB or CAN. It is the
wiki's STM32 reference: [Crazyflie](../../robots/crazyflie.md) and
[ElectronBot](../../robots/electronbot.md) run STM32F405s from the same F4 family, and
TurtleBot3's [OpenCR](robotis-opencr.md) an STM32F7, so the same STM32Cube tools apply.

## Specs

| Spec | Value | Source |
|---|---|---|
| Core, memory | Cortex-M4 with FPU, 180 MHz maximum (Zephyr's board files default to 84 MHz); 512 KB flash, 128 KB SRAM | [1][7] |
| Logic, supply | 3.3 V I/O, chip supply 1.7-3.6 V; check each pin's 5 V tolerance in ST's datasheet. Board power from the ST-LINK USB port or an external 3.3 V, 5 V or 7-12 V source | [1] |
| Timers, encoders | 2 advanced-control, 10 general-purpose and 2 basic timers; hardware quadrature decoding (Zephyr driver `st,stm32-qdec`) | [1] |
| ADC, DAC | Three 12-bit ADCs over 16 channels; one 12-bit DAC with 2 channels | [1] |
| UART, I2C, SPI | 4 USART + 2 UART, 3, 4 | [1] |
| CAN | 2 bxCAN controllers, logic level only; CAN1 TX/RX on D14/D15 of connector CN5 | [1] |
| USB | ST-LINK/V2-1 for flashing, SWD debug and serial; the chip also has OTG FS and HS | [1] |
| Board | Arduino Uno V3 and ST morpho headers (every MCU pin), 50 GPIO; no radio; $18.82 at DigiKey | [1][2] |

## Using it

- **STM32Cube and Arduino.** Configure the chip in STM32CubeMX and build in STM32CubeIDE, the
  project type the micro-ROS STM32 utilities plug into [5]. The STM32duino core lists the board
  as `NUCLEO_F446RE` since core 1.1.1 [6]; see [Arduino](../../software/arduino.md).
- **[Zephyr](../../software/zephyr.md)** board `nucleo_f446re`, flashed with `west flash` through
  STM32CubeProgrammer, OpenOCD or J-Link [1]. **[PlatformIO](../../tools/platformio.md)**
  `board = nucleo_f446re` (`ststm32`), with Arduino, STM32Cube, Zephyr and other frameworks [7].
- **[micro-ROS](../../software/micro-ros.md): community support only.** The `micro_ros_setup`
  README lists the F446RE under FreeRTOS (STM32CubeMX) and Zephyr, as community supported [3]. The
  micro-ROS hardware page leaves it out and lists the NUCLEO-F446ZE, a 144-pin board with the
  same chip, as community supported on FreeRTOS over UART [4].
- **micro-ROS in a CubeMX project.** `micro_ros_stm32cubemx_utils` builds the library in Docker
  and offers UART (DMA or interrupt), USB CDC and UDP-over-LwIP transports; under FreeRTOS the
  task needs over 10 kB of stack, and the README calls it not ready for production [5].
- **Linking to Linux.** The ST-LINK USB port doubles as a serial port: Zephyr's UART2 console is
  read from `/dev/ttyACM0` [1]. For CAN, add a transceiver and a USB-CAN adapter on the Linux side.

## Traps

- **CAN that never acknowledges.** bxCAN pins are logic level: add a transceiver (Zephyr pairs
  the board with an RS485 CAN shield [1]), terminate both bus ends, and check with `candump`.
- **Half speed under Zephyr.** The board files clock the core at 84 MHz from the PLL [1]; raise it
  in the devicetree if a control loop needs 180 MHz.
- **5 V signals.** Not every pin tolerates 5 V: check ST's pin table before wiring 5 V encoders.
- **Community-only micro-ROS** [3][4]: expect to fix micro-ROS build problems yourself.

## Alternatives

- **Other Nucleo boards.** NUCLEO-G474RE keeps the Nucleo-64 layout with a 170 MHz Cortex-M4, CAN
  FD, op-amps and comparators, for a board that drives motors itself [6][8]. An H7 Nucleo-144 such
  as NUCLEO-H743ZI2 [6] suits heavier firmware; both micro-ROS lists include the H743ZI [3][4].
- [Teensy 4.1](pjrc-teensy-4-1.md): faster, with official micro-ROS over USB, UART, Ethernet [4].
- [ESP32-S3](espressif-esp32-s3.md) for Wi-Fi; [RP2040](raspberry-pi-rp2040.md), cheaper [4].
- [OpenCR](robotis-opencr.md): an STM32F7 with Dynamixel ports, an IMU and power outputs.
- [Arduino Mega 2560](arduino-mega-2560.md): 5 V logic and RAMPS, but 8-bit and without CAN.
- Compared in [Choose an MCU and firmware stack](../../guides/choose-an-mcu-and-firmware-stack.md).

## Sources

1. [Zephyr docs: ST Nucleo F446RE](https://docs.zephyrproject.org/latest/boards/st/nucleo_f446re/doc/index.html), accessed 2026-11-27
2. [DigiKey: STMicroelectronics NUCLEO-F446RE](https://www.digikey.com/en/products/detail/stmicroelectronics/NUCLEO-F446RE/5347712), accessed 2026-11-27
3. [micro_ros_setup README, kilted branch](https://github.com/micro-ROS/micro_ros_setup), accessed 2026-11-27
4. [micro-ROS docs: supported hardware](https://micro.vulcanexus.org/docs/overview/hardware/), accessed 2026-11-27
5. [micro_ros_stm32cubemx_utils README, kilted branch](https://github.com/micro-ROS/micro_ros_stm32cubemx_utils), accessed 2026-11-27
6. [STM32duino: supported boards](https://stm32duino.github.io/dev/supported-boards/), accessed 2026-11-27
7. [PlatformIO docs: nucleo_f446re board](https://docs.platformio.org/en/latest/boards/ststm32/nucleo_f446re.html), accessed 2026-11-27
8. [Zephyr docs: ST Nucleo G474RE](https://docs.zephyrproject.org/latest/boards/st/nucleo_g474re/doc/index.html), accessed 2026-11-27
