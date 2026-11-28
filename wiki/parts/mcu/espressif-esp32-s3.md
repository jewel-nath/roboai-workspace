---
type: part
name: Espressif ESP32-S3
summary: Espressif's dual-core 240 MHz microcontroller with 2.4 GHz Wi-Fi, Bluetooth LE, native USB, one CAN (TWAI) controller and four pulse counters; the usual pick for a small wireless robot that talks to a host over Wi-Fi or USB.
tags: [esp32-s3, esp32, espressif, wifi, bluetooth-le, twai, can, usb, psram, devkitc-1, esp-idf, arduino, micro-ros]
category: mcu
subcategory: wireless-mcu
maker: Espressif
model: ESP32-S3
specs: {cpu: "2x Xtensa LX7", clock_mhz: 240, fpu: single, flash_kb: 32768, sram_kb: 512, psram_kb: 16384, logic_v: 3.3, supply_v: "5 via USB or 5V pin, 3.3 via 3V3 pin", gpio: 36, adc_channels: 20, adc_bits: 12, pwm_channels: 8, uart: 3, i2c: 2, spi: 2, can: 1, usb: "full-speed USB OTG with USB Serial/JTAG; second port through a USB-UART bridge", wireless: "Wi-Fi 802.11b/g/n 2.4 GHz, Bluetooth 5 LE", board_mm: "62.74 x 25.4"}
interfaces: [uart, i2c, spi, can, usb, wifi, bluetooth, sdio]
cost: {usd: 19.95, qty: 1, as_of: 2026-11-27, source: "https://www.adafruit.com/product/5364"}
where_to_buy:
  - {seller: Espressif, url: "https://www.espressif.com/en/contact-us/get-samples", as_of: 2026-11-27}
  - {seller: Adafruit, url: "https://www.adafruit.com/product/5364", as_of: 2026-11-27}
datasheet: "https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf"
alternatives: [raspberry-pi-rp2040, pjrc-teensy-4-1, st-nucleo-f446re, arduino-mega-2560]
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf", title: "ESP32-S3 Series Datasheet v2.2", accessed: 2026-11-27}
  - {url: "https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html", title: "ESP32-S3-DevKitC-1 v1.1 user guide, with its dimension drawing", accessed: 2026-11-27}
  - {url: "https://www.adafruit.com/product/5364", title: "Adafruit: ESP32-S3-DevKitC-1, ESP32-S3-WROOM-2, 32MB flash, 16MB PSRAM", accessed: 2026-11-27}
  - {url: "https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf", title: "ESP32 Series Datasheet v5.3", accessed: 2026-11-27}
  - {url: "https://docs.platformio.org/en/latest/boards/espressif32/esp32-s3-devkitc-1.html", title: "PlatformIO docs: Espressif ESP32-S3-DevKitC-1-N8", accessed: 2026-11-27}
  - {url: "https://micro.vulcanexus.org/docs/overview/hardware/", title: "micro-ROS: Supported Hardware", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_setup", title: "micro_ros_setup README, kilted and jazzy branches", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_espidf_component/tree/jazzy", title: "micro_ros_espidf_component README, jazzy branch", accessed: 2026-11-27}
---

# Espressif ESP32-S3

A dual-core Xtensa LX7 microcontroller with 2.4 GHz Wi-Fi and Bluetooth LE [1]. It suits small
wireless robots (desk robots, hands, servo quadrupeds) linked to a host over Wi-Fi or USB.

## Specs

| Spec | Value | Source |
|---|---|---|
| Reference board | ESP32-S3-DevKitC-1-N32R16V (ESP32-S3-WROOM-2 module), $19.95 at Adafruit; 62.74 x 25.40 mm | [2][3] |
| Core, clock, radio | 2x Xtensa LX7, up to 240 MHz; single-precision FPU. Wi-Fi 802.11b/g/n and Bluetooth 5 LE (no Bluetooth Classic) | [1] |
| Memory | Chip: 512 KB SRAM; flash or PSRAM in the package only on some variants. Board: 32 MB octal flash, 16 MB octal PSRAM (1.8 V). Other current variant: N16R8, with 16 MB and 8 MB; N8 and N8R2 are end of life. Octal-PSRAM chips are rated to 65 °C ambient, 85 °C with PSRAM ECC on | [1][2] |
| Logic and power | 3.3 V; supply 3.0-3.6 V; inputs at most VDD + 0.3 V, so not 5 V tolerant. Board: USB (either port), the 5V pin or the 3V3 pin, one at a time | [1][2] |
| GPIO | 45 on the chip; 36 on the headers, of which GPIO35-37 serve the octal memory | [1][2] |
| PWM and timers | LED PWM, 8 channels; 2 MCPWM units, each with 3 timers, 3 operators and capture; four 54-bit timers | [1] |
| Encoder inputs | Pulse counter: 4 units, each with 2 channels (edge input plus direction control), so one quadrature encoder per unit | [1] |
| ADC | Two 12-bit SAR ADCs, 20 channels; ADC2 cannot run while Wi-Fi does | [1] |
| UART, I2C, SPI, CAN | 3 UART, 2 I2C, 2 general-purpose SPI; 1 TWAI controller, CAN 2.0, external transceiver needed | [1] |
| USB | Native port: full-speed USB OTG (USB 1.1) and USB Serial/JTAG on GPIO19/20. UART port: bridge, up to 3 Mbps. Both micro-USB | [1][2][3] |

## Using it

- **Toolchains:** [ESP-IDF](../../software/esp-idf.md), [Arduino](../../software/arduino.md) and
  [PlatformIO](../../tools/platformio.md) (board `esp32-s3-devkitc-1`, either framework) [5].
- **micro-ROS:** the Jazzy ESP-IDF component is tested on the S3 (ESP-IDF v5.2 to v6.0), over Wi-Fi
  UDP by default or UART as a custom transport [8]. The board lists name only "Espressif ESP32":
  UART, Wi-Fi UDP and Ethernet UDP on the micro-ROS site [6]; UART and Wi-Fi UDP in
  `micro_ros_setup` [7]. None documents USB. See [micro-ROS](../../software/micro-ros.md).
- **Host link and wiring:** the UART port's bridge or the native USB serial device [1][2], or Wi-Fi.
  TWAI needs a 3.3 V CAN transceiver; a single supply should give 500 mA or more [1].

## Classic ESP32

The original ESP32 (dual Xtensa LX6, 240 MHz, 520 KB SRAM) has no USB peripheral, so its boards use
a USB-UART bridge. It adds Bluetooth Classic (4.2 BR/EDR), an Ethernet MAC, 8 pulse counters and 16
LED PWM channels against the S3's 4 and 8; both have one TWAI [1][4]. It is still the better buy for
Bluetooth Classic, wired Ethernet (the [ODRI Solo](../../robots/odri-solo.md) master board), more
than four hardware encoders, or firmware written for it, such as OpenCat on Petoi's BiBoard. Some
older variants are not recommended for new designs [4]; the micro-ROS component also lists the newer
ESP32-C6 and ESP32-P4 [8].

## Traps

- **Will not boot after wiring.** GPIO0, 3, 45 and 46 are strapping pins, latched at reset [1];
  keep driver inputs and pull resistors off them. Hold Boot and press Reset for download mode [2].
- **Pins that look free are not.** GPIO35-37 serve the octal memory [2]; GPIO19/20 are USB [1].
- **Battery reading fails with Wi-Fi on.** ADC2 cannot run with Wi-Fi: use ADC1, GPIO1-10 [1].
- **Resets when servos move.** Give servos their own supply; power the board one way only [2].
- **PSRAM missing in PlatformIO.** `esp32-s3-devkitc-1` describes the N8, with 8 MB flash and no
  PSRAM [5]: set your variant's flash size and octal PSRAM, or that memory goes unused.

## Alternatives

- [Raspberry Pi RP2040](raspberry-pi-rp2040.md): cheaper, no radio; PIO for many servos.
- [Teensy 4.1](pjrc-teensy-4-1.md): far faster; three CAN, Ethernet, four quadrature decoders.
- [STM32 Nucleo-F446RE](st-nucleo-f446re.md): the STM32Cube and Zephyr route, with CAN; no radio.
- [Arduino Mega 2560](arduino-mega-2560.md): 5 V AVR for shield-based builds and old code.
- [ROBOTIS OpenCR](robotis-opencr.md): Dynamixel ports and an IMU on the board [6].
- Compared in [Choose an MCU and firmware stack](../../guides/choose-an-mcu-and-firmware-stack.md).

## Sources

1. [ESP32-S3 Series Datasheet v2.2](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf), accessed 2026-11-27
2. [ESP32-S3-DevKitC-1 v1.1 user guide, with its dimension drawing](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html), accessed 2026-11-27
3. [Adafruit: ESP32-S3-DevKitC-1, ESP32-S3-WROOM-2, 32MB flash, 16MB PSRAM](https://www.adafruit.com/product/5364), accessed 2026-11-27
4. [ESP32 Series Datasheet v5.3](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf), accessed 2026-11-27
5. [PlatformIO docs: Espressif ESP32-S3-DevKitC-1-N8](https://docs.platformio.org/en/latest/boards/espressif32/esp32-s3-devkitc-1.html), accessed 2026-11-27
6. [micro-ROS: Supported Hardware](https://micro.vulcanexus.org/docs/overview/hardware/), accessed 2026-11-27
7. [micro_ros_setup README, kilted and jazzy branches](https://github.com/micro-ROS/micro_ros_setup), accessed 2026-11-27
8. [micro_ros_espidf_component README, jazzy branch](https://github.com/micro-ROS/micro_ros_espidf_component/tree/jazzy), accessed 2026-11-27
