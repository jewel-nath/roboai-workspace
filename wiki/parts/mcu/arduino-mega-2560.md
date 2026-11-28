---
type: part
name: Arduino Mega 2560 Rev3
summary: Arduino's 8-bit ATmega2560 board with 54 I/O pins and 5 V logic; still the base of RAMPS stepper arms and servo-heavy hobby robots, but with 8 KB of SRAM it cannot run micro-ROS.
tags: [mcu, arduino, avr, atmega2560, 8-bit, 5v-logic, ramps, grbl, marlin, stepper, servo, ch340]
category: mcu
subcategory: mcu-board
maker: Arduino
model: Mega 2560 Rev3
specs: {cpu: "8-bit AVR (ATmega2560)", clock_mhz: 16, fpu: none, flash_kb: 256, sram_kb: 8, eeprom_kb: 4, logic_v: 5, supply_v: "7-12 via VIN or barrel jack, 5 via USB", gpio: 54, adc_channels: 16, adc_bits: 10, pwm_channels: 15, uart: 4, i2c: 1, spi: 1, usb: "USB-B through an ATmega16U2 USB-serial chip", board_mm: "101.5 x 53.3"}
interfaces: [uart, i2c, spi, usb]
cost: {usd: 49.90, qty: 1, as_of: 2026-11-27, source: "https://www.digikey.com/en/products/detail/arduino/A000067/2639006"}
where_to_buy:
  - {seller: Arduino Store, url: "https://store.arduino.cc/products/arduino-mega-2560-rev3", as_of: 2026-11-27}
  - {seller: DigiKey, url: "https://www.digikey.com/en/products/detail/arduino/A000067/2639006", as_of: 2026-11-27}
datasheet: "https://ww1.microchip.com/downloads/en/devicedoc/atmel-2549-8-bit-avr-microcontroller-atmega640-1280-1281-2560-2561_datasheet.pdf"
alternatives: [pjrc-teensy-4-1, st-nucleo-f446re, espressif-esp32-s3, raspberry-pi-rp2040]
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://docs.arduino.cc/hardware/mega-2560/", title: "Arduino Docs: Mega 2560 Rev3, tech specs and datasheet", accessed: 2026-11-27}
  - {url: "https://ww1.microchip.com/downloads/en/devicedoc/atmel-2549-8-bit-avr-microcontroller-atmega640-1280-1281-2560-2561_datasheet.pdf", title: "Microchip: ATmega640/1280/1281/2560/2561 datasheet", accessed: 2026-11-27}
  - {url: "https://www.digikey.com/en/products/detail/arduino/A000067/2639006", title: "DigiKey: Arduino A000067 (Mega 2560 Rev3)", accessed: 2026-11-27}
  - {url: "https://micro.vulcanexus.org/docs/overview/hardware/", title: "micro-ROS docs: supported hardware", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_arduino", title: "micro_ros_arduino README, kilted branch", accessed: 2026-11-27}
  - {url: "https://reprap.org/wiki/RAMPS_1.4", title: "RepRap wiki: RAMPS 1.4", accessed: 2026-11-27}
  - {url: "https://docs.platformio.org/en/latest/boards/atmelavr/megaatmega2560.html", title: "PlatformIO docs: megaatmega2560 board", accessed: 2026-11-27}
  - {url: "https://www.digikey.com/en/maker/tutorials/2026/how-to-install-ch340-drivers", title: "Maker.io (SparkFun): How to install CH340 drivers", accessed: 2026-11-27}
---

# Arduino Mega 2560 Rev3

Arduino's ATmega2560 board: an 8-bit, 16 MHz MCU with 54 I/O pins, four UARTs and 5 V logic, in
the long Mega layout that the RAMPS stepper shield plugs onto [1]. It suits G-code stepper arms
and hobby-servo robots driven from a PC over USB; for a new ROS 2 robot, pick a 32-bit board.

## Specs

| Spec | Value | Source |
|---|---|---|
| Reference board | Arduino A000067, $49.90 at DigiKey; 101.5 x 53.3 mm, 37 g | [1][3] |
| Core and clock | ATmega2560, 8-bit AVR, 16 MHz; no FPU, so float maths runs in software | [1][2] |
| Memory | 256 KB flash, 8 KB of it the bootloader (PlatformIO counts 248 KB); 8 KB SRAM; 4 KB EEPROM | [1][2][7] |
| Logic, pin current | 5 V (IOREF is tied to 5 V); 20 mA per pin in the board spec, absolute maximum 40 mA per pin and 200 mA per VCC or GND pin | [1][2] |
| Supply | 7-12 V on VIN or the barrel jack, through a 5 V linear regulator; 4.8-5.5 V on USB | [1] |
| I/O | 54 digital (15 with PWM), 16 analog inputs on a 10-bit ADC | [1][2] |
| Timers, encoders | Two 8-bit and four 16-bit timers; no quadrature decoder, so encoders are counted in pin interrupts | [2] |
| UART, I2C, SPI, CAN | 4, 1, 1; no CAN and no radio | [1][2] |
| USB | USB-B into an ATmega16U2 that bridges USB to the main chip's serial port | [1] |

## Using it

- **Toolchains.** The Arduino IDE, arduino-cli and Cloud Editor with the `arduino:avr` core [1];
  [PlatformIO](../../tools/platformio.md) board `megaatmega2560` on `atmelavr` [7]. See
  [Arduino](../../software/arduino.md).
- **micro-ROS: no.** The micro-ROS hardware page targets 32-bit MCUs and says the client needs
  "tens of kilobytes of RAM memory" [4]; the Mega has 8 KB [2]. Neither that page nor the
  micro_ros_arduino board table names an AVR board [4][5].
- **Talking to Linux.** USB serial, with your own protocol or G-code: the
  [Thor arm](../../robots/angellm-thor.md) runs a GRBL 0.9j fork on a Mega, and Marlin has a RAMPS
  1.4 profile (`BOARD_RAMPS_14_EFB`) [6]. On the PC, a ROS 2 node or a
  [ros2_control](../../software/ros2-control.md) hardware interface speaks that protocol.
- **Why it persists.** RAMPS 1.4 adds four Pololu-style stepper driver sockets (A4988, DRV8825)
  plus an optional fifth, three MOSFET outputs and 12 V power [6]; the
  [BCN3D Moveo](../../robots/bcn3d-moveo.md) pairs it with external TB6560 drivers. 5 V logic
  drives servo signals and 5 V modules directly, and 54 pins and four UARTs leave room for many
  servos [1]: [InMoov](../../robots/inmoov.md) uses two Megas. Give motors their own supply.

## Traps

- **Out of memory, silently.** Globals, the stack and serial buffers share 8 KB [2]; an overflow
  shows as random resets or garbled values. Keep buffers small, constant strings in `PROGMEM`.
- **Resets when servos move.** The board's 5 V comes from USB or a linear regulator off VIN [1];
  servo current browns it out. Power servos separately, with a common ground.
- **RAMPS on 24 V.** RAMPS feeds its 12 V input to the Mega through diode D1, and the Mega is not
  rated above 12 V: for 24 V, remove D1 and power the Mega on its own [6].
- **CH340 clones.** The Rev3 uses an ATmega16U2 for USB [1]; boards with WCH's CH340 instead show
  as "USB-SERIAL CH340" on Windows, `/dev/ttyUSB*` on Linux. Without a port, install WCH's
  driver; on Linux, add your user to the `dialout` group [8].
- **5 V into 3.3 V parts.** Outputs swing to 5 V [1]: level-shift to 3.3 V sensors and SBC GPIO.

## Alternatives

- [Teensy 4.1](pjrc-teensy-4-1.md): many pins and real speed at 3.3 V; micro-ROS over USB [4][5].
- [Nucleo-F446RE](st-nucleo-f446re.md): CAN motor drivers, hardware encoder timers, a debugger.
- [ESP32-S3](espressif-esp32-s3.md): micro-ROS over Wi-Fi.
- [RP2040](raspberry-pi-rp2040.md): a cheap 32-bit step, with micro-ROS over USB or UART [4].
- Arduino's 32-bit Due and GIGA R1 are in micro_ros_arduino's community board list [5].
- Compared in [Choose an MCU and firmware stack](../../guides/choose-an-mcu-and-firmware-stack.md).

## Sources

1. [Arduino Docs: Mega 2560 Rev3, tech specs and datasheet](https://docs.arduino.cc/hardware/mega-2560/), accessed 2026-11-27
2. [Microchip: ATmega640/1280/1281/2560/2561 datasheet](https://ww1.microchip.com/downloads/en/devicedoc/atmel-2549-8-bit-avr-microcontroller-atmega640-1280-1281-2560-2561_datasheet.pdf), accessed 2026-11-27
3. [DigiKey: Arduino A000067 (Mega 2560 Rev3)](https://www.digikey.com/en/products/detail/arduino/A000067/2639006), accessed 2026-11-27
4. [micro-ROS docs: supported hardware](https://micro.vulcanexus.org/docs/overview/hardware/), accessed 2026-11-27
5. [micro_ros_arduino README, kilted branch](https://github.com/micro-ROS/micro_ros_arduino), accessed 2026-11-27
6. [RepRap wiki: RAMPS 1.4](https://reprap.org/wiki/RAMPS_1.4), accessed 2026-11-27
7. [PlatformIO docs: megaatmega2560 board](https://docs.platformio.org/en/latest/boards/atmelavr/megaatmega2560.html), accessed 2026-11-27
8. [Maker.io (SparkFun): How to install CH340 drivers](https://www.digikey.com/en/maker/tutorials/2026/how-to-install-ch340-drivers), accessed 2026-11-27
