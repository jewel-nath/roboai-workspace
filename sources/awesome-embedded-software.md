---
type: source
name: Awesome Embedded Resources for Developers
registry: awesome-embedded-software
url: https://github.com/iDoka/awesome-embedded-software
commit: "1954dd7"
read_on: 2026-11-26
counts: {entries: 268, pages: 3, waiting: 0, index_only: 141, deferred: 0, rejected: 124}
---

# Awesome Embedded Resources for Developers: what it gives RoboAI

A list of 268 libraries for microcontroller firmware in 13 sections: general C and C++ libraries,
memory and buffers, storage, protocols, maths and DSP, compression, TinyML, cryptography, RTOSes
and schedulers, CLIs and logging, GUIs, hardware stacks (USB, CAN, sensors), bootloaders and
compilers. It is broad general embedded material, and little of it is robot-specific. For Phase 5
it gives the firmware batch three pages, all shared slugs: micro-ROS, FreeRTOS and Zephyr. The
rest are index rows: the RTOSes behind PX4 and ArduPilot (NuttX, ChibiOS), the stacks that come
inside MCU SDKs (TinyUSB, lwIP, littlefs, Mbed TLS), and a few libraries robot firmware can use
for host links, filters and displays. Close to half the list is inactive, archived, dead or off
topic.

## How it was read

- Read at commit `1954dd7` (2026-11-17) on 2026-11-26 from a shallow clone: the README in full
  (268 list items; the plan's rough count was about 320), `contributing.md`, the CC0-1.0 licence
  and the `.github` files (awesome-lint CI, a stale-issue bot, a security note). The README links
  no other list or data file.
- All 253 GitHub entries were checked on 2026-11-26 with a blob-less shallow clone (head commit
  date, licence file at the repo root) and their github.com page (stars, archived banner,
  redirects). "Last commit" is that head commit's date; "Licence" is read from the root licence
  file, and `—` means there is none at the root. lwIP (Savannah git), Eigen (GitLab) and libdspl
  (SourceForge git) were cloned the same way. FatFs has no repo: its date is release R0.16
  (2025-07-22) from its updates page, and its licence note calls it equivalent to 1-clause BSD.
  wolfSSH and CherryUSB were checked at their GitHub repos (wolfSSL/wolfssh,
  cherry-embedded/CherryUSB).
- Rejection rule: archived, dead, no usable licence, off topic (desktop compilers, a phone OS,
  web and audio tools), tiny and little used, or no commit since before 2024 and small or
  superseded. Older entries stay as index rows only when widely used (heatshrink, 1,561 stars)
  or the newer of two listed forks of a well-known library (Adafruit's RadioHead).
- Only three entries earn a page; ESP-IDF is not in this list. NuttX (PX4) and ChibiOS
  (ArduPilot) stay index rows, for the PX4 and ArduPilot pages to name. Index rows the firmware
  batch may cite: nanoPB, MIN, TCOBS and lwpkt for host-to-MCU links; CMSIS-DSP, iir1 and
  kalman-clib for filtering; nanoMODBUS for RS-485 grippers; u8g2 for small displays; UF2 and
  MCUboot for flashing. CAN rows (libcanard, CanBoot) are index only and use no shared CAN slug.
- Checked for the pages: `micro-ROS/micro_ros_setup` at `565d3f1` (2026-11-19, Apache-2.0) lists
  Humble, Jazzy, Kilted, Lyrical and Rolling as supported, with FreeRTOS and Zephyr ports and no
  NuttX port. micro.ros.org forwards to micro.vulcanexus.org by a meta refresh. The FreeRTOS
  entry links `FreeRTOS/FreeRTOS` (MIT, 8,010 stars), which pulls the kernel from
  `FreeRTOS/FreeRTOS-Kernel` as a submodule. Zephyr is Apache-2.0.
- Arm Mbed: os.mbed.com's announcement link now lands on the ARMmbed GitHub organisation page,
  which says Mbed was sunset in July 2026 and Arm no longer maintains Mbed OS.
- Moved or renamed (github.com redirects): umlibc to rhempel/umm_libc; LevelX, ThreadX and GUIX
  to eclipse-threadx; libevhtp to Yellow-Camper; Paho to eclipse-paho; LwGSM to MaJerle/lwcell;
  libuecc to neocturne; citrus and vanilla to new names; NuttX and its apps to apache/nuttx and
  apache/nuttx-apps; eGUI to nxp-archive; libcanard to OpenCyphal; CanBoot to Arksine/katapult.
- Dead or unreachable on 2026-11-26: bsail/xmodem, strawberryhacker/chaos and arabine/qortos
  return 404; pcc.ludd.ltu.se does not respond. SourceForge (SDCC, libdspl) and dunkels.com
  (Protothreads) refused automated requests with a 403 or a firewall page, so they are not
  counted as dead; SDCC and Protothreads keep `—` for date and licence.
- Errors in the list: it says it covers no Linux topics, yet lists µClibc-ng, SWupdate, tslib,
  libμhttpd, libumqtt, RawTCP_Lib and C-Thread-Pool; it calls eCos closed source, but the eCos
  site reports its licence as OSI-approved; CherryUSB links an organisation of ports, not the
  stack; PicoTCP links a one-star copy (Tubbz-alt) and krypton a copy (ezhangle) of a removed
  repo; u8glib links an archived fork (pabigot), not olikraus/u8glib; two forks of RadioHead are
  listed; spelling slips ("does'nt", "manupulation").
- Suspicious: the eFLL link (zerokol/eFLL) now holds only a one-line README and a file whose
  name and text claim a "broken link hijacking", committed 2026-01-23; the library is gone from
  that URL. Several recent additions are tiny and new (ErdiLRF 1 star, Servomotor 0,
  aem-modbus-simulator 3), and ErdiLRF was added by its own maker in the head commit.
- Nothing fetched was addressed to agents. The Servomotor README carries a note for whoever
  edits its docs that reads like guidance for a coding assistant; it concerns that repo only and
  was not acted on. No code from any clone was run.

## Pages made

| Entry | Page | Tier |
|---|---|---|
| micro-ROS | [micro-ROS](../wiki/software/micro-ros.md) | A |
| FreeRTOS | [FreeRTOS](../wiki/software/freertos.md) | A |
| Zephyr | [Zephyr](../wiki/software/zephyr.md) | A |

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| ETLCPP | C++ template library with fixed-capacity containers and no heap | 2026-11-20 | MIT |
| sc | Portable C99 data structures and utilities | 2026-07-18 | BSD-3-Clause |
| MicroTBX | Feaser's MCU toolbox: assertions, critical sections, heap and lists | 2025-06-06 | MIT |
| µClibc-ng | C library for small embedded Linux systems, not MCUs | 2026-11-23 | LGPL-2.1 |
| Embedded Artistry's libc | Stripped-down C standard library for MCU bring-up | 2026-03-17 | MIT |
| ctl | Header-only, type-safe container templates for C99 | 2026-09-25 | MIT |
| FSMLang | State-machine description language that generates C | 2026-11-23 | GPL-2.0 |
| libmemory | malloc and free implementations for MCU heaps | 2025-03-17 | MIT |
| lwmem | Small dynamic memory manager for MCUs | 2026-10-24 | MIT |
| umm_malloc | Allocator for small heaps | 2026-06-25 | MIT |
| o1heap | Constant-time, deterministic allocator for hard real-time code | 2026-02-09 | MIT |
| EmbeddedProto | C++ Protocol Buffers for Cortex-M; GPL-3.0 or a paid licence | 2026-11-18 | GPL-3.0 |
| LwRB | Lightweight ring buffer, DMA-friendly | 2026-11-21 | MIT |
| lfbb | Lock-free bipartite buffer that always gives contiguous space | 2026-05-19 | MIT |
| lwext4 | ext2, ext3 and ext4 for MCUs | 2026-11-21 | GPL-2.0 |
| FatFS | ChaN's FAT and exFAT module for MCUs; latest release R0.16 | 2025-07-22 | BSD-1-Clause |
| LevelX | Flash wear levelling for ThreadX FileX; moved to eclipse-threadx/levelx | 2026-10-02 | MIT |
| SdFat | Arduino FAT16, FAT32 and exFAT library for SD cards, for data logging | 2025-08-12 | MIT |
| fat32 | Small FAT32 file system in C with no dependencies | 2025-04-03 | BSD-3-Clause |
| littlefs | Power-loss-safe flash file system for MCUs | 2026-03-24 | BSD-3-Clause |
| FlashDB | Key-value and time-series database on MCU flash | 2026-11-16 | Apache-2.0 |
| UnQLite | Embeddable NoSQL key-value and document store for applications | 2026-11-02 | BSD-2-Clause |
| microkvs | Tiny key-value store for configuration on MCU flash | 2025-11-15 | BSD-3-Clause |
| EasyFlash | Flash storage library for settings and logs, from the FlashDB author | 2025-03-14 | MIT |
| FCB | Zephyr's flash circular buffer, part of Zephyr (software/zephyr) | — | Apache-2.0 |
| nanoPB | Protocol Buffers in C for MCUs, for typed host-to-MCU messages | 2026-11-19 | Zlib |
| nanoMODBUS | Modbus RTU and TCP for MCUs, e.g. to drive RS-485 grippers | 2026-02-01 | MIT |
| Adafruit's RadioHead | Packet-radio library (LoRa, nRF24 and more) for Arduino; GPL-2.0 or a paid licence | 2023-05-12 | GPL-2.0 |
| LwIP | Small TCP/IP stack for MCUs, started by uIP's author | 2026-11-24 | BSD-3-Clause |
| CycloneTCP | Dual IPv4 and IPv6 stack for embedded systems | 2026-11-20 | GPL-2.0 |
| StaticNet | TCP/IP and SSH stack with only static allocation | 2025-07-17 | BSD-3-Clause |
| LiveKit | LiveKit SDK for real-time audio, video and data on ESP32 | 2026-11-18 | Apache-2.0 |
| mongoose | Embedded web server and networking library; GPL-2.0 or a paid licence | 2026-11-25 | GPL-2.0 |
| libμhttpd | HTTP server for embedded Linux on libev | 2026-10-13 | MIT |
| libumqtt | MQTT client for embedded Linux on libev | 2024-08-29 | MIT |
| Paho MQTT | Eclipse's MQTT client for MCUs; moved to eclipse-paho | 2026-07-03 | EPL-2.0 or EDL-1.0 |
| LwGSM | AT-command driver for cellular modules; renamed lwcell | 2026-09-27 | MIT |
| TinyGSM | Arduino library for GSM and LTE modems | 2026-11-14 | LGPL-3.0 |
| LwGPS | GPS NMEA parser for MCUs | 2026-11-01 | MIT |
| minmea | NMEA 0183 parser in C | 2026-09-20 | WTFPL |
| LwESP | Host-MCU driver for ESP8266 and ESP32 AT firmware | 2026-09-13 | MIT |
| lwpkt | Packet framing for multi-device RS-485 buses | 2026-11-25 | MIT |
| lwow | 1-Wire bus over a UART | 2026-10-24 | MIT |
| MIN | Framed MCU-to-host protocol with a Python host side | 2024-01-30 | MIT |
| libCoAP | CoAP (RFC 7252) in C | 2026-11-25 | BSD-2-Clause |
| Servomotor | One maker's Arduino and desktop library for its RS-485 integrated servomotors; no Atlas robot uses them | 2026-11-12 | MIT |
| FPM | Header-only fixed-point math for C++ | 2026-03-29 | MIT |
| Eigen | C++ linear algebra; under most C++ robotics libraries | 2026-11-22 | MPL-2.0 |
| liquid-dsp | DSP library for software-defined radio | 2026-09-26 | MIT |
| minfft | Small FFT library | 2025-08-11 | MIT |
| iir1 | Real-time IIR filters (Butterworth, Chebyshev) in C++, for sensor signals | 2026-10-29 | MIT |
| kalman-clib | Plain-C Kalman filter for MCUs | 2026-06-10 | MIT |
| pocketfft | Header-only C++ FFT | 2026-10-18 | BSD-3-Clause |
| KISS FFT | Simple mixed-radix FFT in C | 2026-11-18 | BSD-3-Clause |
| CMSIS-DSP | Arm's DSP, filter, matrix and PID functions for Cortex-M | 2026-11-19 | Apache-2.0 |
| heatshrink | LZSS compression in tiny RAM; inactive since 2015 but widely used | 2015-12-08 | ISC |
| shoco | Compression for short strings | 2026-02-16 | MIT |
| ECL | Small compression library with low-memory modes | 2026-03-01 | MIT |
| Unishox2 | Compression for short Unicode strings | 2026-10-28 | Apache-2.0 |
| TCOBS | COBS framing with run-length compression for short messages | 2026-04-29 | MIT |
| μTensor | TinyML inference library; low activity | 2024-09-06 | Apache-2.0 |
| nnom | Neural-network inference for MCUs | 2024-04-08 | Apache-2.0 |
| libonnx | Small ONNX inference engine in C99 | 2025-08-05 | MIT |
| TinyMaix | Small neural-network inference library for MCUs | 2025-02-05 | Apache-2.0 |
| edge-agents (ForestHub) | Young LLM-agent runtime for edge boards (Raspberry Pi, Jetson); AGPL | 2026-08-24 | AGPL-3.0 |
| trussed | Rust framework for crypto apps on MCUs | 2026-11-20 | Apache-2.0 |
| wolfSSH | SSH client and server for embedded systems; GPL-3.0 or a paid licence | 2026-11-22 | GPL-3.0 |
| LibHydrogen | Small, easy crypto library for constrained devices | 2026-11-18 | ISC |
| wolfTPM | TPM 2.0 library for embedded use | 2026-11-24 | GPL-3.0 |
| mbedTLS | TLS and PSA Crypto library for MCUs | 2026-11-17 | Apache-2.0 |
| liblithium | Portable lightweight crypto library | 2026-03-27 | Apache-2.0 |
| trezor-crypto | Crypto folder of the Trezor firmware repo (MIT inside a GPL-3.0 repo) | 2026-11-25 | MIT |
| arduinolibs | Arduino cryptography library | 2024-05-27 | — |
| tlse | Single-file TLS 1.2 and 1.3 | 2026-11-25 | Unlicense |
| LibTomCrypt | Broad, modular crypto toolkit in C | 2026-11-25 | Unlicense |
| Monocypher | Small, auditable crypto library in C | 2026-11-22 | CC0-1.0 |
| tiny-AES-c | Small portable AES in C | 2024-10-04 | Unlicense |
| µAES | Portable AES with many block-cipher modes | 2026-04-29 | Apache-2.0 |
| CycloneCRYPTO | Crypto toolkit for embedded systems, from the CycloneTCP maker | 2026-11-18 | GPL-2.0 |
| salty | Ed25519 signatures tuned for Cortex-M4 and M33 | 2026-03-23 | Apache-2.0 |
| micro-ecc | ECDH and ECDSA for 8- to 64-bit MCUs | 2026-11-17 | BSD-2-Clause |
| LK kernel | Little Kernel, a small SMP-aware kernel | 2026-11-14 | MIT |
| QuarkTS | Cooperative OS with state machines and coroutines | 2025-10-27 | MIT |
| Apache NuttX | POSIX-style RTOS that PX4 runs on; moved to apache/nuttx | 2026-11-26 | Apache-2.0 |
| ChibiOS/RT | RTOS and HAL that ArduPilot builds on for its STM32 boards | 2026-05-31 | GPL-3.0 |
| Azure RTOS ThreadX | Eclipse ThreadX (formerly Azure RTOS); moved to eclipse-threadx/threadx | 2026-11-01 | MIT |
| embox | Configurable RTOS that runs Linux software without Linux | 2026-11-21 | BSD-2-Clause |
| RIOT | RTOS for IoT devices from 8 to 32 bits | 2026-11-25 | LGPL-2.1 |
| Arm Mbed OS | Arm's Cortex-M OS; Arm sunset Mbed in July 2026; older robot firmware (Mini Cheetah's motor driver) used it | 2024-10-08 | Apache-2.0 |
| RT-Thread | RTOS with a large package ecosystem | 2026-11-25 | Apache-2.0 |
| distortos | Object-oriented C++ RTOS for MCUs | 2026-07-16 | MPL-2.0 |
| Tock Embedded OS | Rust OS for running untrusted apps side by side on MCUs | 2026-11-23 | Apache-2.0 |
| µC/OS-III | Micrium's preemptive kernel, now Apache-2.0 | 2026-07-15 | Apache-2.0 |
| QP/C | Active-object framework with hierarchical state machines; GPL-3.0 or a paid licence | 2026-11-17 | GPL-3.0 |
| uevloop | Small event loop for MCUs | 2026-11-03 | MIT |
| lwevt | Lightweight event manager | 2026-10-24 | MIT |
| Protothreads | Stackless cooperative threads built from C macros | — | — |
| vsf | Event-driven framework with optional preemption | 2026-11-25 | Apache-2.0 |
| terminal | Command-line interface for MCUs | 2025-07-02 | GPL-3.0 |
| embedded-cli | Single-header CLI with history and completion | 2026-03-11 | MIT |
| microshell | VT100 shell for MCUs | 2024-06-20 | MIT |
| lwprintf | Lightweight printf for MCUs | 2026-10-27 | MIT |
| Embedded_Printf | Small printf for MCUs | 2026-09-12 | MIT |
| tiny-printf | Small, self-contained printf | 2026-11-23 | MIT |
| tiny-printf new | Maintained fork of mpaland's printf | 2026-06-27 | MIT |
| nanoprintf | Very small single-header printf | 2026-09-25 | Unlicense |
| fmt | C++ formatting library, the basis of std::format | 2026-11-24 | MIT |
| emio | Small std::format-like formatting for C++20 | 2026-08-26 | MIT |
| EasyLogger | Very small C and C++ logger | 2026-11-05 | MIT |
| trice | Fast MCU trace logging that sends IDs instead of strings | 2026-11-19 | MIT |
| spdlog | Fast C++ logging library | 2026-11-25 | MIT |
| elog | Small logger for MCUs | 2026-05-18 | MIT |
| lvgl | Embedded GUI library with many widgets, for MCUs | 2026-11-25 | MIT |
| TouchGFX | ST's free, closed GUI designer for STM32 | — | Proprietary (free) |
| u8g2 | Library for monochrome OLED and LCD displays (SSD1306 and others) | 2026-11-22 | BSD-2-Clause |
| GUIX | ThreadX's GUI library; moved to eclipse-threadx/guix | 2026-10-15 | MIT |
| HAGL | Hardware-agnostic graphics library | 2026-10-12 | MIT |
| Embedded-graphics | Rust 2D graphics without frame buffers | 2026-09-26 | Apache-2.0 |
| LovyanGFX | Display library for ESP32, RP2040 and SAMD51 | 2026-11-05 | BSD-2-Clause |
| mcufont | Font rendering for MCUs | 2026-07-25 | MIT |
| lcd-image-converter | Desktop tool that turns images and fonts into C arrays | 2025-12-26 | GPL-3.0 |
| tinyusb | Cross-platform USB host and device stack | 2026-11-25 | MIT |
| libusb_stm32 | Small USB device stack for STM32 | 2025-10-06 | Apache-2.0 |
| CherryUSB | USB host and device stack; the link is an org of ports, the stack is cherry-embedded/CherryUSB | 2026-11-25 | Apache-2.0 |
| SFUD | Universal SPI flash driver (JEDEC SFDP) | 2025-05-30 | MIT |
| libcanard | Cyphal/CAN (formerly UAVCAN) in C; moved to OpenCyphal/libcanard | 2026-10-21 | MIT |
| CanBoot | Bootloader for Cortex-M made for Klipper's CAN nodes, now also USB and UART; renamed Katapult | 2026-10-01 | GPL-3.0 |
| stm32-async-1wire | Non-blocking 1-Wire for STM32 with a DS18B20 driver | 2026-11-25 | MIT |
| ErdiLRF | Vendor driver for ERDI laser rangefinders; no Atlas robot uses them | 2026-11-18 | MIT |
| C-Thread-Pool | POSIX thread pool in C, for Linux | 2025-05-18 | MIT |
| mcuboot | Secure bootloader for 32-bit MCUs, used with Zephyr | 2026-11-25 | Apache-2.0 |
| OpenBLT | Bootloader over UART, CAN, USB and TCP/IP; GPL-3.0 or a paid licence | 2026-11-19 | GPL-3.0 (modified) |
| TinyUF2 | UF2 drag-and-drop bootloader on TinyUSB | 2026-11-25 | MIT |
| wolfBoot | Secure bootloader with authenticated updates | 2026-11-25 | GPL-3.0 |
| UF2 | USB drag-and-drop flashing format, used by the RP2040 boot ROM | 2026-11-10 | MIT |
| SWupdate | Over-the-air updates for embedded Linux | 2026-11-24 | GPL-2.0 |
| tslib | Touchscreen library for embedded Linux | 2026-11-01 | LGPL-2.1 |
| SDCC | C compiler for 8-bit MCUs (8051, STM8, HC08, Z80, Padauk) | — | — |
| TinyGo | Go for MCUs and WebAssembly | 2026-11-25 | BSD-3-Clause |
| modm | C++ HAL generator for AVR, SAM and STM32 | 2026-11-24 | MPL-2.0 |
| incbin | Embeds binary files at compile time | 2025-05-26 | Unlicense |

## Deferred

| Entry | What it is | Phase |
|---|---|---|

## Rejected

| Entry | Why | Date |
|---|---|---|
| wiselib | Inactive since 2014; no licence file | 2026-11-26 |
| util.embedded | Archived on 2022-03-29 | 2026-11-26 |
| embxx | Inactive since 2019 | 2026-11-26 |
| embedded-libs | STM32 HAL helpers, inactive since 2020 | 2026-11-26 |
| eFLL | The linked repo was taken over: a 2026-01-23 commit replaced the library with a "hijacked" note | 2026-11-26 |
| Collection of miscellaneous portable C snippets | General C portability snippets, not embedded-specific; inactive since 2021 | 2026-11-26 |
| umlibc | Tiny (9 stars), quiet since 2024-12; the repo moved to rhempel/umm_libc | 2026-11-26 |
| HWlib | Small teaching library, inactive since 2021 | 2026-11-26 |
| protobuf-embedded-c | Inactive since 2015; nanoPB covers it | 2026-11-26 |
| RingBuffer | Small and inactive since 2020 | 2026-11-26 |
| fifofast | Small and inactive since 2022 | 2026-11-26 |
| ufat | Small and inactive since 2019 | 2026-11-26 |
| fat_io_lib | Small and inactive since 2019 | 2026-11-26 |
| emfat | Small and inactive since 2017 | 2026-11-26 |
| OpenFAT | Inactive since 2015; no licence file | 2026-11-26 |
| uC-FS | Inactive since 2021 | 2026-11-26 |
| UFFS | Inactive since 2015 | 2026-11-26 |
| PureDB | General constant-database library, not aimed at MCUs; little used | 2026-11-26 |
| Vedis | Inactive since 2021 | 2026-11-26 |
| FlashAlgo | For debug-probe tool makers only; inactive since 2023 | 2026-11-26 |
| interchange | An internal piece of the Rust Trussed project, not useful alone | 2026-11-26 |
| xmodem | Dead link: the repo returns 404 | 2026-11-26 |
| TinyFrame | Small and inactive since 2021 | 2026-11-26 |
| aem-modbus-simulator | Narrow test tool that emulates one industrial DC monitor; 3 stars | 2026-11-26 |
| rcobs | Small and inactive since 2021 | 2026-11-26 |
| RadioHead | Older duplicate fork of RadioHead, inactive since 2021; the Adafruit fork is kept | 2026-11-26 |
| uIP | Inactive since 2013; lwIP (listed) covers it | 2026-11-26 |
| HttpClient | Inactive since 2018 | 2026-11-26 |
| httpio | Small and inactive since 2016 | 2026-11-26 |
| PicoTCP | Links a one-star copy; the original (tass-belgium/picotcp) has had no commit since 2019-10-22 | 2026-11-26 |
| RawTCP_Lib | Raw-socket packets on desktop Linux; off-topic for MCUs | 2026-11-26 |
| LRNDIS | Inactive since 2021 | 2026-11-26 |
| libevhtp | Archived on 2021-06-30 | 2026-11-26 |
| sandbird | Inactive since 2019 | 2026-11-26 |
| libemqtt | Inactive since 2014 | 2026-11-26 |
| RegExp | Inactive since 2017; no licence file | 2026-11-26 |
| GSM_Engine | Inactive since 2017 | 2026-11-26 |
| atat | Archived on 2026-10-28 | 2026-11-26 |
| cAT | Inactive since 2023; serving AT commands is rare in robots | 2026-11-26 |
| gzat | Tiny and inactive since 2020 | 2026-11-26 |
| ATParser | Mbed-only and inactive since 2017 | 2026-11-26 |
| atcommander | Archived on 2022-04-13 | 2026-11-26 |
| panStamp-SWAP | Inactive since 2017 | 2026-11-26 |
| panStamp-uSWAP | Inactive since 2016 | 2026-11-26 |
| liquid-fpm | Inactive since 2014 | 2026-11-26 |
| libdspl | Small and inactive since 2023 | 2026-11-26 |
| SigLib | No usable licence: free only for personal and educational use | 2026-11-26 |
| lsp-dsp-lib | DSP for desktop audio plug-ins; off-topic | 2026-11-26 |
| SMAZ | Inactive since 2012; Unishox2, listed, does the job and is maintained | 2026-11-26 |
| Cranium | Inactive since 2017 | 2026-11-26 |
| Fido | Inactive since 2017 | 2026-11-26 |
| caffepresso | Research code for old embedded accelerator boards | 2026-11-26 |
| Embedded SOD | Inactive since 2023; robot vision runs OpenCV on the robot computer (software/opencv) | 2026-11-26 |
| QR-Image-embedded | Inactive since 2020 | 2026-11-26 |
| krypton | Links a copy of a removed project (cesanta/krypton gives 404); inactive since 2015 | 2026-11-26 |
| poly1305-donna | Inactive since 2016; no licence file | 2026-11-26 |
| minicrypt | Inactive since 2014 | 2026-11-26 |
| tinycrypt | Archived on 2024-03-05 | 2026-11-26 |
| libuecc | Little used (2 stars); moved to neocturne/libuecc | 2026-11-26 |
| c25519-and-ed25519 | Inactive: the latest package is dated 2017-10-05 | 2026-11-26 |
| pcg-c-basic | Inactive since 2014; pcg-c is the fuller version | 2026-11-26 |
| pcg-c | Inactive since 2019; random-number generation is off-topic for robot firmware | 2026-11-26 |
| citrus | Hobby OS, inactive since 2021 | 2026-11-26 |
| vanilla | Hobby OS, inactive since 2020 | 2026-11-26 |
| chaos | Dead link: the repo returns 404 | 2026-11-26 |
| scmRTOS | Inactive since 2021 | 2026-11-26 |
| eCos | Little activity: the site's latest news is from 2015-11-29 | 2026-11-26 |
| R3-OS | Archived on 2026-09-19 | 2026-11-26 |
| dandelion | No usable licence (CC BY-NC-SA 4.0); inactive since 2023 | 2026-11-26 |
| MuditaOS | An OS for one phone; off-topic | 2026-11-26 |
| µC/OS-II | Superseded by µC/OS-III from the same maker; inactive since 2023 | 2026-11-26 |
| Quite Ok RTOS | Dead link: the repo returns 404 | 2026-11-26 |
| async | Small and inactive since 2022 | 2026-11-26 |
| EventOS | Tiny and inactive since 2023 | 2026-11-26 |
| cli | Tiny and inactive since 2018 | 2026-11-26 |
| SerialMenu | Small and inactive since 2019 | 2026-11-26 |
| terminal-server | Small and inactive since 2021 | 2026-11-26 |
| microsh | Small and inactive since 2023 | 2026-11-26 |
| cmd-l | Tiny and inactive since 2021 | 2026-11-26 |
| microrl | Inactive since 2017 | 2026-11-26 |
| ProMenu | Tiny and inactive since 2020 | 2026-11-26 |
| BBmenu | Tiny; no licence file; inactive since 2022 | 2026-11-26 |
| micromenu-v2 | Inactive since 2015; no licence file | 2026-11-26 |
| tinyprintf | Inactive since 2014 | 2026-11-26 |
| xprintf-fp | Small and inactive since 2022 | 2026-11-26 |
| xprintf-io | A copy of ChaN's xprintf with no licence file; inactive since 2021 | 2026-11-26 |
| xprintf | Tiny and inactive since 2013 | 2026-11-26 |
| mini-printf | No licence file; inactive since 2020 | 2026-11-26 |
| scanf | Tiny and inactive since 2021 | 2026-11-26 |
| ft_scanf | A student exercise; inactive since 2017 | 2026-11-26 |
| embedded-log | Small and inactive since 2023 | 2026-11-26 |
| embedded-diagnostic-logger | Inactive since 2020; no licence file | 2026-11-26 |
| EasyGUI | Inactive since 2021 | 2026-11-26 |
| eGUI | Moved to nxp-archive; inactive since 2017 | 2026-11-26 |
| ESLowGraphics | No usable licence (non-commercial) | 2026-11-26 |
| ftk | Inactive since 2016 | 2026-11-26 |
| u8glib | An archived fork; u8g2 replaced u8glib | 2026-11-26 |
| SGFX | Inactive since 2020 | 2026-11-26 |
| GUILib | Inactive since 2015 | 2026-11-26 |
| HMI_Library | Inactive since 2013; no licence file | 2026-11-26 |
| AFGUI | Inactive since 2016 | 2026-11-26 |
| MakiseGUI | Inactive since 2021 | 2026-11-26 |
| emGUI | Inactive since 2018; no licence file | 2026-11-26 |
| UGUI (µGUI) | Inactive since 2016 | 2026-11-26 |
| lv_gui_designer | Archived on 2020-03-04 | 2026-11-26 |
| walv | Inactive since 2020 | 2026-11-26 |
| bitmap-OSD-font | Tiny; no licence file; inactive since 2023 | 2026-11-26 |
| ttf2mesh | Font tessellation; off-topic and inactive since 2023 | 2026-11-26 |
| sfam_generator | Inactive since 2016 | 2026-11-26 |
| picon | An icon font; off-topic | 2026-11-26 |
| embedded-driver | Small and inactive since 2020 | 2026-11-26 |
| FastIO | Tiny and inactive since 2020 | 2026-11-26 |
| Canbus-Message | Tiny and inactive since 2021 | 2026-11-26 |
| TimeLib | Inactive since 2019; no licence file | 2026-11-26 |
| μtz | Inactive since 2019 | 2026-11-26 |
| little | Small scripting language, inactive since 2022 | 2026-11-26 |
| tcc | A C compiler for desktop systems; off-topic for MCU firmware | 2026-11-26 |
| lcc | Classic desktop compiler under a restrictive licence; off-topic | 2026-11-26 |
| pcc | The site does not respond; the mirror's last commit is 2018-09-21 | 2026-11-26 |
| chibicc | Teaching compiler for x86-64 Linux; off-topic | 2026-11-26 |
| rvcc | Bootstrapped compiler for Linux ELF targets; off-topic | 2026-11-26 |
| Apache NuttX Apps | Duplicate: NuttX's own apps repo, covered by the NuttX row | 2026-11-26 |
| cembed | Small and inactive since 2020 | 2026-11-26 |
| WTX | Web tools in Rust; off-topic | 2026-11-26 |
