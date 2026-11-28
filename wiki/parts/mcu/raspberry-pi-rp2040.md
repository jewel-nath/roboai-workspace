---
type: part
name: Raspberry Pi RP2040
summary: Raspberry Pi's dual Cortex-M0+ microcontroller with 264 KB SRAM and eight PIO state machines, sold on the Raspberry Pi Pico; a cheap, well-documented servo and sensor co-processor for a Linux computer, with no FPU, CAN or radio (the Pico W adds the radio).
tags: [rp2040, raspberry-pi-pico, pico-w, pio, cortex-m0plus, pico-sdk, micropython, arduino-pico, micro-ros, servo-2040, rp2350]
category: mcu
subcategory: mcu
maker: Raspberry Pi
model: RP2040
specs: {cpu: "2x Arm Cortex-M0+", clock_mhz: 133, fpu: none, flash_kb: 2048, sram_kb: 264, logic_v: 3.3, supply_v: "1.8-5.5 via VSYS, 5 via USB", gpio: 26, adc_channels: 3, adc_bits: 12, pwm_channels: 16, uart: 2, i2c: 2, spi: 2, usb: "USB 1.1 device or host, micro-USB", board_mm: "51 x 21"}
interfaces: [uart, i2c, spi, usb]
cost: {usd: 4.00, qty: 1, as_of: 2026-11-27, source: "https://www.adafruit.com/product/4864"}
where_to_buy:
  - {seller: Raspberry Pi (approved resellers), url: "https://www.raspberrypi.com/products/raspberry-pi-pico/", as_of: 2026-11-27}
  - {seller: Adafruit, url: "https://www.adafruit.com/product/4864", as_of: 2026-11-27}
datasheet: "https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf"
alternatives: [espressif-esp32-s3, pjrc-teensy-4-1, st-nucleo-f446re, arduino-mega-2560]
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf", title: "RP2040 Datasheet, build of 2026-11-19", accessed: 2026-11-27}
  - {url: "https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf", title: "Raspberry Pi Pico Datasheet, build of 2026-11-19", accessed: 2026-11-27}
  - {url: "https://www.raspberrypi.com/products/raspberry-pi-pico/", title: "Raspberry Pi Pico product page", accessed: 2026-11-27}
  - {url: "https://www.adafruit.com/product/4864", title: "Adafruit: Raspberry Pi Pico RP2040", accessed: 2026-11-27}
  - {url: "https://github.com/earlephilhower/arduino-pico", title: "arduino-pico README, Arduino core for RP2040 and RP2350", accessed: 2026-11-27}
  - {url: "https://micro.vulcanexus.org/docs/overview/hardware/", title: "micro-ROS: Supported Hardware", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_setup", title: "micro_ros_setup README, kilted and jazzy branches", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_raspberrypi_pico_sdk", title: "micro_ros_raspberrypi_pico_sdk README, kilted branch", accessed: 2026-11-27}
---

# Raspberry Pi RP2040

Raspberry Pi's dual Cortex-M0+ microcontroller with programmable I/O (PIO) state machines [1]. It
suits cheap servo-heavy robots and USB co-processors that need no radio, CAN or fast floating point.

## Specs

| Spec | Value | Source |
|---|---|---|
| Reference board | Raspberry Pi Pico, $4.00 at Adafruit; 51 x 21 x 1 mm, castellated to solder down as a module; in production until at least January 2036. The Pico W ($6) adds 2.4 GHz 802.11n Wi-Fi and Bluetooth 5.2 | [2][3][4] |
| Core and clock | 2x Cortex-M0+, up to 133 MHz, or 200 MHz with the core supply raised to 1.15 V; no FPU (the boot ROM has a fast software float library) | [1] |
| Memory | 264 KB SRAM in 6 banks. No on-chip flash: code runs from external QSPI flash, up to 16 MB; the Pico has 2 MB | [1][2] |
| Logic and power | 3.3 V; a pin takes at most IOVDD + 0.5 V, so not 5 V tolerant. Pico: VSYS 1.8-5.5 V into a buck-boost regulator, USB 5 V reaches VSYS through a Schottky diode, 3V3 loads under 300 mA | [1][2] |
| GPIO | 30 on the chip, 26 on the Pico headers; the board uses GPIO23 (regulator mode), 24 (VBUS sense), 25 (LED) and 29 (VSYS/3) | [1][2] |
| PIO and encoders | 2 blocks of 4 state machines, 32 instruction slots per block. No quadrature decoder: count encoders with PIO, or one channel with a PWM slice | [1] |
| PWM | 8 slices, 16 outputs; a slice can instead measure frequency or duty cycle on its B pin | [1] |
| ADC | 12-bit, 500 ksps, 4 inputs plus a temperature sensor; 3 on the Pico headers | [1][2] |
| UART, I2C, SPI, CAN | 2 UART, 2 I2C, 2 SPI; no CAN | [1] |
| USB | USB 1.1 host or device; micro-USB on the Pico | [1][2] |

## Using it

- **Toolchains:** the C/C++ Pico SDK [8]; MicroPython, as on [Kayra](../../robots/kayra.md)'s Servo
  2040 and [Coglet](../../robots/coglet.md); and the [Arduino](../../software/arduino.md) core
  arduino-pico (Boards Manager URL in its README), covering Pico, Pico W, Pico 2 and Servo2040, with
  jitter-free PIO servos, FreeRTOS SMP and [PlatformIO](../../tools/platformio.md) docs [5].
- **micro-ROS:** the micro-ROS site lists "Raspberry Pi Pico RP2040" as officially supported, on the
  Pico SDK, over USB and UART [6]. `micro_ros_setup`'s build table does not list it; it only links
  the standalone Pico SDK library [7], which ships a precompiled `libmicroros` and talks over USB,
  or UART once CMake moves stdio there [8]. Neither documents Wi-Fi for the Pico W.
  See [micro-ROS](../../software/micro-ros.md).
- **To a Linux computer:** USB serial, `micro-ros-agent serial --dev /dev/ttyACM0` [8]; or a 3.3 V
  UART straight to a Raspberry Pi's pins. To flash, hold BOOTSEL while plugging in USB and copy a
  UF2 file to the drive that appears; a 3-pin SWD port serves debugging [2].
- **Power:** feed VSYS from a 5 V regulator or one Li-ion cell; add a second source through another
  Schottky diode so neither back-powers the other [2]. In USB host mode, put 5 V on VBUS [2].
- **Successor:** the Pico 2 (from $5) uses the RP2350 [3], which arduino-pico runs on its Arm or
  RISC-V cores [5]; the micro-ROS site lists only the RP2040 [6].

## Traps

- **5 V on a pin or VSYS.** Level-shift 5 V encoders and sensors [1]. VSYS stops at 5.5 V [2]: a 2S
  pack needs a regulator first. Servos never run from 3V3 (300 mA budget) [2].
- **Noisy battery readings.** The ADC's reference is the board's 3.3 V switcher, offset about 30 mV;
  average, drive GPIO23 high to cut ripple, or fit a 3.0 V reference on ADC_VREF [2].
- **Phantom power.** ADC pins GPIO26-29 have a diode to 3V3, so a voltage on them leaks into the
  rail while the chip is unpowered; GPIO0-25 do not [2]. Power those sensors from the Pico's 3V3.
- **micro-ROS compiler mismatch.** The precompiled library was built with `arm-none-eabi-gcc` 9.3.1
  and expects a compatible one; use it, or rebuild the library with the builder Docker image [8].
- **Upload fails, port gone.** A hung sketch ignores auto-reset; hold BOOTSEL while plugging in [5].

## Alternatives

- [ESP32-S3](espressif-esp32-s3.md): Wi-Fi and Bluetooth, a CAN controller, PSRAM and an FPU.
- [Teensy 4.1](pjrc-teensy-4-1.md): 600 MHz with an FPU, three CAN, Ethernet, quadrature decoders.
- [STM32 Nucleo-F446RE](st-nucleo-f446re.md): the STM32Cube and Zephyr route, with CAN.
- [Arduino Mega 2560](arduino-mega-2560.md): 5 V AVR for shield-based builds and old code.
- [ROBOTIS OpenCR](robotis-opencr.md): Dynamixel ports and an IMU on the board [6].
- Compared in [Choose an MCU and firmware stack](../../guides/choose-an-mcu-and-firmware-stack.md).

## Sources

1. [RP2040 Datasheet, build of 2026-11-19](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf), accessed 2026-11-27
2. [Raspberry Pi Pico Datasheet, build of 2026-11-19](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf), accessed 2026-11-27
3. [Raspberry Pi Pico product page](https://www.raspberrypi.com/products/raspberry-pi-pico/), accessed 2026-11-27
4. [Adafruit: Raspberry Pi Pico RP2040](https://www.adafruit.com/product/4864), accessed 2026-11-27
5. [arduino-pico README, Arduino core for RP2040 and RP2350](https://github.com/earlephilhower/arduino-pico), accessed 2026-11-27
6. [micro-ROS: Supported Hardware](https://micro.vulcanexus.org/docs/overview/hardware/), accessed 2026-11-27
7. [micro_ros_setup README, kilted and jazzy branches](https://github.com/micro-ROS/micro_ros_setup), accessed 2026-11-27
8. [micro_ros_raspberrypi_pico_sdk README, kilted branch](https://github.com/micro-ROS/micro_ros_raspberrypi_pico_sdk), accessed 2026-11-27
