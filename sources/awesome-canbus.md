---
type: source
name: Awesome CAN Bus
registry: awesome-canbus
url: https://github.com/iDoka/awesome-canbus
commit: "4e53b31"
read_on: 2026-11-26
counts: {entries: 255, pages: 3, waiting: 0, index_only: 56, deferred: 0, rejected: 196}
---

# Awesome CAN Bus: what it gives RoboAI

A curated list of 255 CAN bus tools, protocol libraries, database (DBC) tools and hardware designs
for MCUs, SBCs and FPGAs, written for reverse engineering cars and automotive controllers. Robots
use CAN for motor drives and for links between MCUs, so only the list's Linux, Python, DBC and
open-hardware parts help a builder. It gives Phase 5's firmware batch two pages: can-utils (with
the kernel's SocketCAN docs as its main source) and python-can. 56 entries are index only:
SocketCAN bindings, DBC tools, analyser GUIs, CANopen test tools, open USB-CAN adapter firmware and
hardware, MCU CAN libraries and bit-timing calculators. The other 196 are rejected: the
car-hacking, OBD-II, UDS, ISO-TP, J1939 and J2534 entries, car projects, and anything abandoned,
unlicensed or dead. The list holds no CANopen stack and no ROS 2 bridge.

## How it was read

- Read at commit `4e53b31` (2026-11-17, the merge that added BUSMASTER-NG) on 2026-11-26 from a
  shallow clone: the README in full (255 entries in 29 sections), `contributing.md`, `license`
  (CC0 1.0) and `.github/`. `archive.sh` and `README.url` are the maintainer's script and URL list
  for cloning every linked repo; they were read, not run. The plan counted about 290 items; the
  extra links sit inside entries (firmware beside its hardware, a kernel-module note) and are
  folded into their entry's row.
- Each of the 236 linked GitHub repos was shallow-cloned without file contents for its head
  commit date (six were gone), its github.com page read for stars, archived state, renames and
  forks, and its licence file read from raw.githubusercontent.com. Two Bitbucket repos were
  dated from Bitbucket's public commit list, the OpenCores core from its project page. "Last
  commit" is the head commit's date.
- Rules used. Off topic: car hacking, OBD-II, UDS, ISO-TP, J1939 and J2534 (vehicle diagnostics
  and trucks), car projects and automotive ECU suites, as the robotic-tooling note did for cabana,
  opendbc and python-udsoncan. A CAN entry a robot builder could use is index only unless it is
  abandoned and unimportant: no commit in 18 months (before 2025-05-26) and under 100 stars.
  Software without a licence file, forks of a listed or known original, and firmware that poses
  as a commercial adapter to use that vendor's drivers are rejected.
- Pages: can-utils and python-can take the shared slugs; the SocketCAN docs row points at the
  can-utils page. cantools (DBC decoding) belongs on the python-can page, candleLight_fw and the
  eLinux page on the can-utils page, and the CAN-dbs plugin on the existing PlotJuggler page.
  SavvyCAN (1,941 stars, maintained) is the most-starred analyser GUI here and stays index only.
- Parts rule: no USB-CAN adapter earns a page. On 2026-11-26 the Atlas names a PEAK PCAN-USB
  (Allegro Hand) and a CTRE CANivore (TidyBot) once each; PiPER, Berkeley Humanoid Lite and
  TriFinger name no model. candleLight_fw (CANable and similar boards, mainline Linux gs_usb
  driver) is the open option if the actuators batch wants one.
- Not in the list: CANopenNode, the Python canopen package, ros2_canopen or any other CANopen
  stack. CANopen appears only as test tools (CANopenTerm, CANopen Bench, and CANviz with CiA 402
  decoding), all index only; the stack and the ROS 2 bridge come from other notes.
- Dead on 2026-11-26: six GitHub repos return 404 (j2534-tcp, PythonVectorXL, can_decoder, the
  ELM327 and ELM329 adapters, BudgetCANv2's firmware and hardware); the pudn DBC spec PDF does not
  respond; Kvaser's classic bit-timing calculator returns 404 (its CAN FD one works).
- Moved: CTU-CAN-FD to SELOSYS, PlotJuggler to its own org, zubax_babel to Zubax/canface_cf1,
  eerimoq/cantools to cantools/cantools, canopy to can-explorer, and libwecan, esp32-cantroller,
  esp32_canbus_gateway, hadoucan-fw and CanDybugFW to new owners. O2OO, the CSS Electronics page
  and the Qt 5 docs redirect.
- Errors in the list: GVRET and can4python are listed twice; CanoPy and "cantools by Erik
  Moqvist" repeat can-explorer and cantools under old names; canerrsim now ships in can-utils, and
  can-utils' own J1939 tools replace the kurt-vd fork; ESP32RET is marked unmaintained but had a
  commit on 2026-10-22; the OpenCores CAN core is Verilog, not VHDL; CTU-CAN-FD's IP core licence
  allows only non-commercial use (its Linux driver is GPL-2.0), which the list does not say;
  TSMaster is closed source although its repo carries an LGPL-2.1 file.
- Agents: nothing in the fetched files addresses agents. One entry, dbc-matrix-audit, links the
  autosar-agent-skills repo, whose README presents its `SKILL.md` files as runbooks for AI agents.
  Only that README was read, nothing in it was followed, and the entry is rejected as off topic.

## Pages made

| Entry | Page | Tier |
|---|---|---|
| Linux CAN Utils | [can-utils and SocketCAN](../wiki/tools/can-utils.md) | B |
| SocketCAN | [can-utils and SocketCAN](../wiki/tools/can-utils.md) | B |
| python-can | [python-can](../wiki/software/python-can.md) | B |

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| can-explorer | Python GUI that plots CAN payloads live, for decoding unknown messages | 2026-04-22 | GPL-3.0 |
| CANopen Bench | Web bench for CANopen devices: EDS-driven SDO access, test cases, live trace; new | 2026-11-25 | MIT |
| CANopenTerm | CANopen CC test and analysis tool: SDO, NMT, trace, scripting | 2026-10-28 | MIT |
| CAN support in Linux | eLinux wiki page on Linux CAN drivers; a source for the can-utils page | — | — |
| CANdevStudio from GENIVI | Qt GUI that simulates and analyses CAN with drag-and-drop blocks | 2024-05-01 | MPL-2.0 |
| SavvyCAN | Cross-platform Qt GUI to capture, decode and replay CAN; works with SocketCAN | 2026-11-16 | MIT |
| CANgaroo | Qt CAN analyser for SocketCAN and candleLight; unmaintained since 2017 | 2017-05-17 | GPL-2.0 |
| CAN-X | Windows C# CAN analyser | 2025-11-14 | AGPL-3.0 |
| CAN++ | Windows CAN monitor that decodes signals from DBC or KCD files | 2026-09-18 | MIT |
| PlotJuggler | Time-series plotter; on the [PlotJuggler](../wiki/tools/plotjuggler.md) page; repo moved to the PlotJuggler org | 2026-11-25 | MPL-2.0 |
| PlotJuggler::CAN-dbs | PlotJuggler plugins that decode candump logs and live CAN with a DBC; belongs on the PlotJuggler page | 2026-03-25 | MIT |
| CANviz | Browser CAN analyser with CANopen (CiA 301/402) and J1939 decoding | 2026-07-08 | MIT |
| BUSMASTER-NG | Maintained Windows fork of BUSMASTER: CAN and LIN monitor, logging, DBC | 2026-11-21 | LGPL-3.0 |
| Canmetry | Browser viewer for BLF, ASC, MF4 and CSV CAN logs with DBC decoding; new | 2026-11-17 | MIT |
| cantraceviewer | Browser plotter for ASC, BLF, MF4 and TRC CAN logs with DBC decoding; new | 2026-11-19 | MIT |
| canscope | Terminal CAN inspection and reverse-engineering tool | 2026-06-25 | MIT |
| cantools | Python DBC, KCD and ARXML parser, encoder and decoder; belongs on the python-can page | 2026-11-20 | MIT |
| Robotell-USB-CAN-Python | Python program for the Robotell USB-CAN adapter | 2026-04-25 | MIT |
| cannelloni | SocketCAN tunnel over UDP, TCP or SCTP; its README says not for production | 2026-11-25 | GPL-2.0 |
| tincan | Shows CAN traffic received over a UDP interface | 2025-06-18 | MIT |
| can-hub | Encrypted CAN-over-IP hub for SocketCAN buses behind NAT | 2026-11-17 | AGPL-3.0 or commercial |
| Seeed-USB-CAN-Linux | Linux CLI for the cheap "USB-CAN Analyzer" adapter; a fork of kobolt/usb-can | 2025-07-30 | GPL-2.0 |
| libwecan | Header-only C library to encode and decode CAN signals; repo moved | 2026-11-10 | MIT |
| Qt CAN Bus | Qt's CAN module with SocketCAN, PEAK and other plugins; the Qt 5 link redirects to the 5.15 archive | — | — |
| JavaCAN | Java binding for SocketCAN (RAW, BCM, ISO-TP) | 2026-10-22 | MIT |
| CanKit | C#/.NET CAN library with one API over many adapters | 2026-11-22 | Apache-2.0 |
| CANvenient | C abstraction layer over several CAN APIs on Windows and Linux | 2026-09-30 | MIT |
| CAN-Examples | Short C examples for SocketCAN on Linux | 2020-02-01 | GPL-3.0 |
| DBC Format | SJSU wiki page on DBC sections and multiplexed signals | — | — |
| DBC File Explained | CSS Electronics' introduction to DBC files; the link redirects | — | — |
| cantools by Andreas Heitmann | C tools for DBC and log formats (ASC, BLF, MDF) | 2026-03-14 | GPL-3.0 |
| canmatrix | Converts CAN databases between DBC, ARXML, KCD, XLS and more | 2026-11-24 | BSD-2-Clause |
| CANBabel | Java translator between KCD and DBC | 2025-04-13 | GPL-3.0 |
| dbcc | Compiles DBC files to C pack and unpack code for MCUs | 2025-10-03 | MIT |
| dbcppp | C++ DBC parser with a C API | 2025-07-09 | MIT |
| CANdb from GENIVI | C++ CAN database library that CANdevStudio builds on | 2021-06-25 | MPL-2.0 |
| pydbc (christoph2) | Python tool to process vehicle network descriptions (DBC) | 2026-10-29 | GPL-2.0 |
| USB_CAN-FD on ATSAME51 | Open-hardware USB to CAN FD adapter, two isolated channels (ATSAME51) | 2025-11-28 | MIT |
| SuperCAN | Open USB to CAN FD firmware for ATSAME51 boards | 2026-10-27 | MIT |
| FlexCAN | Arduino CAN library for Teensy 3.x; a fork of pawelsky/FlexCAN_Library | 2021-07-22 | MIT |
| hadoucan-fw on STM32H750 | Firmware for the SM-1301 USB to CAN FD adapter (STM32H750); repo moved | 2026-09-23 | BSD-3-Clause |
| Arduino-STM32-CAN | CAN examples for the Arduino core on STM32 boards (F072 to F4) | 2026-11-26 | MIT |
| zubax_babel | Firmware for the Zubax Babel USB-CAN adapter (SLCAN); repo renamed canface_cf1 | 2025-08-29 | GPL-3.0 |
| candleLight_fw | Firmware for CANable, candleLight and similar USB-CAN adapters, driven by the mainline Linux gs_usb driver; belongs on the can-utils page | 2026-11-25 | MIT |
| candleLight | KiCad files of the original candleLight USB-CAN adapter (STM32F072) | 2016-05-12 | CERN-OHL-1.2 |
| cantact-hw | CANtact USB-CAN hardware files; CANable is a clone of it | 2017-06-09 | CC-BY-SA-4.0 |
| arduino-canhacker | Lawicel (slcan) adapter firmware for Arduino with an MCP2515 | 2024-01-19 | MIT |
| Arduino-canbus-monitor | Lawicel (slcan) monitor firmware for Arduino with a CAN shield | 2026-10-03 | MIT |
| arduino-mcp2515 | Arduino library for the MCP2515 SPI CAN controller | 2026-02-27 | MIT |
| ESP-IDF-CANBus-Monitor | ESP-IDF example that monitors CAN traffic on an ESP32 | 2026-06-09 | MIT |
| ESP32-Arduino-CAN | Arduino CAN library for the ESP32's built-in controller | 2019-05-08 | MIT |
| esp-idf-can2http | ESP-IDF example that bridges CAN to HTTP | 2026-09-25 | MIT |
| CAN-wizard | CAN sniffer console for ESP32 and ESP32-C3 with an SN65HVD230 (ESP-IDF) | 2026-08-26 | MIT |
| CTU-CAN-FD | CAN FD controller IP core in VHDL with a SocketCAN Linux driver; repo moved | 2026-11-23 | non-commercial only (IP core) |
| Bit Timing Calculator for CAN FD | Kvaser's online CAN FD bit-timing calculator | — | — |
| STMG431 FDCAN SOLVER | Online FDCAN bit-timing calculator for STM32G4 parts | — | — |

## Deferred

| Entry | What it is | Phase |
|---|---|---|

## Rejected

| Entry | Why | Date |
|---|---|---|
| CarHackingTools | Off topic: car-hacking tool collection; archived | 2026-11-26 |
| Caring Caribou | Off topic: car security exploration tool | 2026-11-26 |
| CAN_Reverse_Engineering | Off topic: vehicle CAN payload reverse engineering; no commit since 2022 | 2026-11-26 |
| carhacking | Off topic: car-hacking scripts; no licence | 2026-11-26 |
| ReCAN | Off topic: vehicle CAN reverse engineering; no commit since 2020 | 2026-11-26 |
| parse_can_logs | Off topic: car log reverse engineering; no commit since 2024 | 2026-11-26 |
| reversegear | Off topic: automotive reverse engineering; no commit since 2017 | 2026-11-26 |
| CANalyzat0r | Off topic: car protocol security analysis; no commit since 2020 | 2026-11-26 |
| CANToolz | Off topic: CAN security testing framework; no commit since 2021 | 2026-11-26 |
| GVRET | Off topic: Arduino firmware for EV reverse engineering; no licence, no commit since 2018 | 2026-11-26 |
| UDSim | Off topic: vehicle diagnostics (UDS) simulator and fuzzer | 2026-11-26 |
| uds-server | Off topic: vehicle diagnostics (UDS) simulator; UDSim replaces it | 2026-11-26 |
| CANalyse | Off topic: vehicle network attack tool; no commit since 2021 | 2026-11-26 |
| canhack | Off topic: CAN protocol attack research library | 2026-11-26 |
| canDrive | Off topic: tools for hacking a car | 2026-11-26 |
| Carpunk | Off topic: CAN injection toolkit for cars | 2026-11-26 |
| CANghost | Off topic: Carpunk replaces it; no licence | 2026-11-26 |
| canTot | Off topic: car-hacking framework | 2026-11-26 |
| CANanalyze | Off topic: automotive protocol (ISO-TP, UDS) framework | 2026-11-26 |
| Scapy | Off topic: general packet tool; its CAN layers serve car security work | 2026-11-26 |
| CAN-RE-Tool | Off topic: vehicle CAN reverse engineering; no licence, no commit since 2021 | 2026-11-26 |
| canerrsim | Duplicate: canerrsim now ships in can-utils | 2026-11-26 |
| ECU-simulator | Off topic: vehicle diagnostics simulator; archived | 2026-11-26 |
| ELM327-emulator | Off topic: OBD-II adapter emulator; non-commercial licence | 2026-11-26 |
| elmulator | Off topic: ELM327 emulator for testing OBD-II apps | 2026-11-26 |
| DDT4All | Off topic: car ECU parameter tool over ELM327 | 2026-11-26 |
| ELM327SLCAN | Off topic: car CAN sniffer on ELM327; no commit since 2019 | 2026-11-26 |
| Arduino-OBD2-Async | Off topic: OBD-II library; no licence, no commit since 2018 | 2026-11-26 |
| CAN-Shark | Off topic: OBD-II PIDs on Arduino; no licence | 2026-11-26 |
| OBD2-Scantool | Off topic: OBD-II scan tool; no licence, no commit since 2012 | 2026-11-26 |
| O2OO | Off topic: OBD-II car logger; link moved to vanheusden.com/electronics/O2OO/ | 2026-11-26 |
| freediag | Off topic: OBD-II car diagnostics | 2026-11-26 |
| pyvit | Off topic: vehicle interface toolkit; archived | 2026-11-26 |
| OBDium | Off topic: OBD-II car diagnostics app | 2026-11-26 |
| python-UDSonCAN | Off topic: car ECU diagnostics protocol (UDS) | 2026-11-26 |
| uds-c | Off topic: UDS and OBD-II C library; no commit since 2021 | 2026-11-26 |
| iso14229 | Off topic: UDS server and client for ECUs | 2026-11-26 |
| isotp-c | Off topic: ISO-TP diagnostics transport; no commit since 2021 | 2026-11-26 |
| python-can-IsoTP | Off topic: ISO-TP diagnostics transport for Python | 2026-11-26 |
| CanTp | Off topic: AUTOSAR ISO-TP module | 2026-11-26 |
| aioisotp | Off topic: ISO-TP for asyncio; archived | 2026-11-26 |
| J1939-CANBUS | Off topic: J1939 engine data; no licence, no commit since 2020 | 2026-11-26 |
| J1939-Framework | Off topic: J1939 for trucks and buses; no commit since 2021 | 2026-11-26 |
| python-j1939 | Off topic: J1939 for Python; no commit since 2023 | 2026-11-26 |
| can-utils with J1939 support | Obsolete fork: J1939 tools are now in can-utils; no commit since 2015 | 2026-11-26 |
| test-can-j1939 | Off topic: J1939 on Linux how-to; no commit since 2016 | 2026-11-26 |
| libj1939 | Off topic: J1939 for MCUs; no commit since 2021 | 2026-11-26 |
| Pretty-J1939 | Off topic: J1939 log pretty-printer | 2026-11-26 |
| TruckDevil | Off topic: J1939 truck ECU assessment tool | 2026-11-26 |
| python-can-j1939 | Off topic: J1939 for Python | 2026-11-26 |
| Open-SAE-J1939 | Off topic: J1939 stack for vehicles and machinery | 2026-11-26 |
| embr::j1939 | Off topic: J1939 library for MCUs | 2026-11-26 |
| j2534-tcp | Dead link (404); off topic (J2534 pass-thru) | 2026-11-26 |
| SharpWrap2534 | Off topic: J2534 wrapper; its licence file grants no rights | 2026-11-26 |
| gocanflasher | Off topic: Saab Trionic ECU flasher; no licence | 2026-11-26 |
| cantools (mwkpe) | Abandoned: C++ CLI tools, no commit since 2021, 24 stars; not the Python cantools | 2026-11-26 |
| BUSMASTER | Abandoned since 2017; BUSMASTER-NG is its maintained fork | 2026-11-26 |
| signalbroker-server | A fork; automotive signal broker; no commit since 2020 | 2026-11-26 |
| CANiBUS | Off topic: vehicle research server; archived, no commit since 2013 | 2026-11-26 |
| J1939 (kernel docs) | Off topic: J1939 for vehicles | 2026-11-26 |
| elmcan | Off topic: ELM327 dongles; merged into Linux 6.0 as can327 | 2026-11-26 |
| can-isotp | Off topic: ISO-TP diagnostics transport; part of Linux since 5.10 | 2026-11-26 |
| gs_usb | A fork of jxltom/gs_usb; 4 stars, no commit since 2023 | 2026-11-26 |
| CANAL-View | Vendor GUI for one adapter (TouCAN); no licence | 2026-11-26 |
| wxCAN-Sniffer | Abandoned and small: no commit since 2025-05-18, 47 stars | 2026-11-26 |
| CANLogger | Abandoned: no commit since 2019 | 2026-11-26 |
| Seeed-USB-CAN-Analyzer | Closed-source binary; no licence | 2026-11-26 |
| CANtact-app | Abandoned since 2016; a desktop app for CANtact hardware only | 2026-11-26 |
| openCanSuite | Abandoned since 2017; no licence | 2026-11-26 |
| Plotter and Scanner from SmartGauges | Off topic: car scanning tool; no licence | 2026-11-26 |
| ICSim | Off topic: car instrument-cluster simulator for security training | 2026-11-26 |
| CAN-Monitor-qt | Abandoned: no commit since 2019 | 2026-11-26 |
| CANBUS-Analyzer | No licence; no commit since 2020 | 2026-11-26 |
| SLSS-CANAnalyser | No licence | 2026-11-26 |
| TSMaster | Closed-source automotive tool; the repo is a download page | 2026-11-26 |
| CANcool | Abandoned and small: no commit since 2025-05-12, 73 stars | 2026-11-26 |
| Kayak | Archived; no commit since 2019 | 2026-11-26 |
| OpenSourceLogger | Off topic: J1939 data logger; no commit since 2023 | 2026-11-26 |
| EcuBus-Pro | Off topic: car ECU development tool (UDS, DoIP, LIN) | 2026-11-26 |
| Novo Bus Analyzer | BUSMASTER fork with no commit since 2025-03; BUSMASTER-NG is kept | 2026-11-26 |
| bootCAN | No licence; 1 star | 2026-11-26 |
| socanui | Abandoned and small: no commit since 2025-03, 15 stars | 2026-11-26 |
| canair | Off topic: UDS diagnostics over ELM327 or WiCAN dongles | 2026-11-26 |
| strym | Off topic: logs car CAN data through a comma.ai panda | 2026-11-26 |
| canviewer | Abandoned: no commit since 2021, 11 stars | 2026-11-26 |
| can4python | Abandoned: no commit since 2016 | 2026-11-26 |
| Python-Vector-CANoe | Off topic: drives Vector's proprietary CANoe; no commit since 2023 | 2026-11-26 |
| CanCat | Off topic: CAN security tool | 2026-11-26 |
| Pyfuzz_can | Off topic: attack tool for trucks; no commit since 2018 | 2026-11-26 |
| python-socketcan-monitor | A fork; no commit since 2019 | 2026-11-26 |
| CanoPy | Duplicate: renamed can-explorer, listed above | 2026-11-26 |
| PythonVectorXL | Dead link (404) | 2026-11-26 |
| py4can | Off topic: drives Vector's CANalyzer; no licence | 2026-11-26 |
| pican | Abandoned since 2017; no licence | 2026-11-26 |
| canny | Abandoned: no commit since 2023, 35 stars | 2026-11-26 |
| opendlv-device-can-replay | Archived; 1 star | 2026-11-26 |
| c0f | Off topic: fingerprints car makes from CAN traffic; no commit since 2015 | 2026-11-26 |
| canqv | Abandoned: no commit since 2020, 10 stars | 2026-11-26 |
| Candle.NET | Abandoned: no commit since 2021, 35 stars | 2026-11-26 |
| canSerializer | No licence; no commit since 2022 | 2026-11-26 |
| VCAN | Abandoned: no commit since 2020, 20 stars | 2026-11-26 |
| IMCTFD | No licence; no commit since 2018 | 2026-11-26 |
| go-socketcan | No licence; no commit since 2019 | 2026-11-26 |
| iso15765-canbus | Off topic: ISO-TP diagnostics transport | 2026-11-26 |
| socketcan-demo | A fork; no commit since 2016 | 2026-11-26 |
| DBC Format Specification v1.0 | Dead link (no response); a leaked proprietary document | 2026-11-26 |
| J1939 and DBC introduction | Off topic: J1939 for vehicles | 2026-11-26 |
| cabana | Off topic: car CAN reverse-engineering tool; archived | 2026-11-26 |
| KCD | Abandoned: no commit since 2023; no licence | 2026-11-26 |
| cantools by Erik Moqvist | Duplicate: redirects to cantools/cantools, listed above | 2026-11-26 |
| CanDB | No licence; no commit since 2018 | 2026-11-26 |
| can4python (second entry) | Duplicate entry | 2026-11-26 |
| convert_dbc_to_cpp_file | No licence; 4 stars | 2026-11-26 |
| Vector DBC | Abandoned: last Bitbucket commit 2021-04-19 | 2026-11-26 |
| can_decoder | Dead link (404) | 2026-11-26 |
| dbc-parser | Abandoned: no commit since 2022, 10 stars | 2026-11-26 |
| Vector CANdb++ DBC file parser | Abandoned copy of cantools' DBC parser; no commit since 2023 | 2026-11-26 |
| dbc_reader | Abandoned: no commit since 2018 | 2026-11-26 |
| CAN_BUS_DBC_VIEWER | Abandoned: no commit since 2022, 8 stars | 2026-11-26 |
| dbcview | No licence; no commit since 2019 | 2026-11-26 |
| VectorDbcChecker | No licence; 6 stars | 2026-11-26 |
| pydbc (Sauci) | Abandoned: no commit since 2020, 3 stars | 2026-11-26 |
| dbc-matrix-audit | Off topic: AUTOSAR DBC and ARXML audit, packaged as AI-agent skills | 2026-11-26 |
| ELM327 (allpro) | Dead link (404); off topic (OBD-II adapter) | 2026-11-26 |
| Open-OBD2-datalogger | Off topic: car engine data logger | 2026-11-26 |
| CANBootloader | No licence; no commit since 2019 | 2026-11-26 |
| PiCCANTE | Off topic: car-hacking tool | 2026-11-26 |
| panda | Off topic: comma.ai car interface for openpilot | 2026-11-26 |
| STM32duino_CAN_Library | No licence; no commit since 2021 | 2026-11-26 |
| pcan_pro_x | Poses as a PEAK adapter to use PEAK's drivers; no commit since 2022 | 2026-11-26 |
| CANnon | Abandoned: no commit since 2017 | 2026-11-26 |
| CANCAN | No licence; 0 stars | 2026-11-26 |
| stm32-CAN-bus-example-HAL-API | No licence; no commit since 2019 | 2026-11-26 |
| CAN-to-USB-lawicel-for-stm32 | No licence; no commit since 2019 | 2026-11-26 |
| stm32-slcan | No licence; no commit since 2022 | 2026-11-26 |
| cantact-pro-hw | Abandoned: no commit since 2020 | 2026-11-26 |
| STM32-CAN-Busadapter | No licence; 8 stars | 2026-11-26 |
| Ethernet-CAN converter | Abandoned: no commit since 2022, 27 stars | 2026-11-26 |
| CANBUS_UART | No licence; 3 stars | 2026-11-26 |
| eXoCAN | Abandoned: no commit since 2021 | 2026-11-26 |
| CAN-BUS-Man-In-The-Middle | Off topic: car man-in-the-middle device; no commit since 2020 | 2026-11-26 |
| CAN-Bus-Arduino_Core_STM32 | No licence; one example sketch | 2026-11-26 |
| BudgetCANv2 | Dead links (404): both the firmware and the hardware repo | 2026-11-26 |
| CanDybugFW | Abandoned: no commit since 2021; repo moved to benedekkupper | 2026-11-26 |
| CAN-USB-dongle-fw | No licence; no commit since 2021 | 2026-11-26 |
| CAN-RS485-adapter | No licence; 7 stars | 2026-11-26 |
| vector_can | Poses as a Vector VN1610 to use Vector's drivers; no commit since 2022 | 2026-11-26 |
| CAN_OMEGA | Off topic: car-hacking hardware; no commit since 2017 | 2026-11-26 |
| CANsniffer on STM32F042 | No licence; no commit since 2017 | 2026-11-26 |
| cantact | Abandoned: no commit since 2024-08, 59 stars | 2026-11-26 |
| USB2CAN | No licence; no commit since 2017 (candleLight_fw supports the board) | 2026-11-26 |
| CANAlyze | Abandoned: its firmware's last commit is from 2020 | 2026-11-26 |
| Cantact FW (x893) | A fork of linklayer/cantact-fw; no commit since 2015 | 2026-11-26 |
| ELM329 | Dead link (404); off topic (OBD-II) | 2026-11-26 |
| OBD2CAN | Off topic: OBD-II bridge; no commit since 2019 | 2026-11-26 |
| pcan_cantact | Poses as a PEAK adapter; candleLight_fw gives the same boards a mainline driver | 2026-11-26 |
| kvaser_cantact | Poses as a Kvaser adapter; candleLight_fw covers the same boards | 2026-11-26 |
| open-usb-can from Fabio Baltieri | Archived | 2026-11-26 |
| Arduino-CAN-bus-SD-logger | Archived; J1939 focus; no licence | 2026-11-26 |
| Arduino-psa-comfort-can-adapter | Off topic: Peugeot and Citroen car adapter | 2026-11-26 |
| epasuino | Off topic: car power steering; no commit since 2019 | 2026-11-26 |
| carfuino | Off topic: car performance computer; no commit since 2018 | 2026-11-26 |
| W203-canbus | Off topic: Mercedes car project | 2026-11-26 |
| CANBus-Triple | Off topic: car-hacking platform; no licence on the hardware | 2026-11-26 |
| GVRET (second entry) | Duplicate entry | 2026-11-26 |
| open-source-can-bridge | Abandoned: last Bitbucket commit 2022-02-20 | 2026-11-26 |
| slcanuino | No licence; no commit since 2019 | 2026-11-26 |
| CITM02 | Off topic: CAN man-in-the-middle adapter; no commit since 2021 | 2026-11-26 |
| arduino-OBD2 | Off topic: OBD-II car data | 2026-11-26 |
| arduino-ecu-logger | Off topic: OBD-II engine logger; no licence | 2026-11-26 |
| connected-car | Off topic: Nissan car to MQTT | 2026-11-26 |
| PSASteeringWheelAdapter | Off topic: car steering-wheel adapter | 2026-11-26 |
| esp32-slcan | No licence | 2026-11-26 |
| esp32s3-slcan | No licence; no commit since 2023 | 2026-11-26 |
| ESP32_CAN_Interface | No licence; no commit since 2021 | 2026-11-26 |
| esp32_canbus_gateway | No licence; repo moved; no commit since 2021 | 2026-11-26 |
| esp32-cantroller | Abandoned: no commit since 2022; repo moved | 2026-11-26 |
| esp32-canbus-logger | No licence; no commit since 2021 | 2026-11-26 |
| ESP32_CANViewer | Abandoned: no commit since 2021, 27 stars | 2026-11-26 |
| esp32-obd2-emulator | Off topic: OBD-II emulator; archived | 2026-11-26 |
| ESP32RET | Off topic: reverse-engineering firmware for car boards (EVTV ESP32, Macchina A0) | 2026-11-26 |
| ESP32S3RET | A fork of ESP32RET; no commit since 2023 | 2026-11-26 |
| esp32_obd2 | Off topic: OBD-II layer; a fork | 2026-11-26 |
| ESP32_OBD2_Emulator | Off topic: OBD-II emulator; no licence | 2026-11-26 |
| RejsaCAN-ESP32 | Off topic: a board made for car projects; no licence | 2026-11-26 |
| RejsaCAN-ESP32-C6 | Duplicate: an example folder of RejsaCAN-ESP32 | 2026-11-26 |
| beaglebone_black_socketcan | Abandoned: no commit since 2018, 5 stars | 2026-11-26 |
| rpi-can-logger | No licence; no commit since 2021 | 2026-11-26 |
| CANoPi | Abandoned: no commit since 2017 | 2026-11-26 |
| CAN (OpenCores) | No licence stated; last commit 2009; Verilog, though the list says VHDL | 2026-11-26 |
| Microchip CAN BUS Analyzer firmware | No licence; no commit since 2016 | 2026-11-26 |
| Microchip CAN BUS Analyzer driver | Abandoned: no commit since 2017 | 2026-11-26 |
| BB-to-STM32 | An LED-sync demo; no licence | 2026-11-26 |
| elm327_clone | Off topic: OBD-II clone firmware; no licence | 2026-11-26 |
| CAN Bus Bit Timing Calculator | Dead link (404) | 2026-11-26 |
| STM8S208 CAN Speed Calculator | STM8 only; no licence; no commit since 2017 | 2026-11-26 |
