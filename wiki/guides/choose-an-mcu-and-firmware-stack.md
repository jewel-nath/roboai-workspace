---
type: guide
name: Choose an MCU and firmware stack
summary: Which microcontroller, firmware stack and ROS 2 link should run a robot's low-level loop - no MCU (a USB adapter to smart servos or CAN drives), ESP32-S3, RP2040, Teensy 4.1, STM32 Nucleo, Arduino Mega or OpenCR; Arduino, ESP-IDF, the vendor SDKs, Zephyr or FreeRTOS; micro-ROS, a framed serial link into ros2_control, CAN and CANopen, or an autopilot's bridge.
tags: [mcu, firmware, microcontroller, micro-ros, ros2-control, serial, can, canopen, esp32-s3, esp32, rp2040, teensy, stm32, arduino, esp-idf, zephyr, freertos, platformio, px4, ardupilot]
question: Which microcontroller and firmware stack should run my robot's low-level loop, and how should it talk to ROS 2?
options: [espressif-esp32-s3, raspberry-pi-rp2040, pjrc-teensy-4-1, st-nucleo-f446re, arduino-mega-2560, robotis-opencr, arduino, esp-idf, zephyr, freertos, platformio, micro-ros, ros2-canopen, canopennode, px4, ardupilot]
recommendation: "No MCU when smart serial-bus servos or CAN drives reach the computer through a USB adapter (ros2_control on the computer); otherwise an ESP32-S3 on ESP-IDF with micro-ROS on Jazzy, over USB or Wi-Fi, for a small base or servo robot; a Teensy 4.1 or STM32 Nucleo with a framed serial or CAN link into ros2_control for fast loops, many encoders or CAN joints; PX4 or ArduPilot on a flight controller for drones and outdoor rovers."
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://micro.vulcanexus.org/docs/overview/hardware/", title: "micro-ROS docs: Supported hardware", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro-ROS-Agent", title: "micro-ROS-Agent README and branches (humble, jazzy, kilted, lyrical): cmake/SuperBuild.cmake", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/rmw_microxrcedds/tree/jazzy", title: "rmw_microxrcedds README (jazzy branch)", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_espidf_component/tree/jazzy", title: "micro_ros_espidf_component README (jazzy branch)", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_platformio", title: "micro_ros_platformio README", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_setup", title: "micro_ros_setup README and config folder (kilted branch)", accessed: 2026-11-27}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files (humble, jazzy, kilted, lyrical)", accessed: 2026-11-27}
  - {url: "https://micro.vulcanexus.org/docs/overview/license/", title: "micro-ROS docs: License overview", accessed: 2026-11-27}
  - {url: "https://docs.px4.io/main/en/middleware/uxrce_dds.html", title: "PX4 docs: uXRCE-DDS (PX4-ROS 2/DDS bridge)", accessed: 2026-11-27}
  - {url: "https://docs.px4.io/main/en/ros2/user_guide.html", title: "PX4 docs: ROS 2 user guide", accessed: 2026-11-27}
  - {url: "https://ardupilot.org/dev/docs/ros2-interfaces.html", title: "ArduPilot dev docs: ROS 2 interfaces", accessed: 2026-11-27}
  - {url: "https://github.com/ArduPilot/ardupilot/blob/master/Tools/ros2/README.md", title: "ArduPilot Tools/ros2 README (master)", accessed: 2026-11-27}
  - {url: "https://ardupilot.org/dev/docs/ros2-pi.html", title: "ArduPilot dev docs: ROS 2 on Raspberry Pi", accessed: 2026-11-27}
  - {url: "https://github.com/ros-industrial/ros2_canopen", title: "ros2_canopen README, package.xml and LICENSE files (master)", accessed: 2026-11-27}
---

# Choose an MCU and firmware stack

Which board runs the motors, encoders and sensors under a ROS 2 computer, on which firmware, and
how does it reach ROS 2? For builders of a small base, an arm, a legged robot or a drone. Skills:
[fw-mcu](../../skills/fw-mcu/SKILL.md), [fw-rtos-micro-ros](../../skills/fw-rtos-micro-ros/SKILL.md)
and [fw-serial-can](../../skills/fw-serial-can/SKILL.md); the board pages are linked in the table.

## Short answer

- **Smart servos or CAN drives: no MCU.** A USB adapter puts the bus on the computer and a
  [ros2_control](../software/ros2-control.md) hardware interface drives it: a Waveshare adapter on
  [SO-101](../robots/so-101.md), a USB-to-CAN adapter on [AgileX PiPER](../robots/agilex-piper.md).
- **A small base or servo robot that should be a ROS 2 node:** an ESP32-S3 on ESP-IDF with
  [micro-ROS](../software/micro-ros.md) on Jazzy, over USB serial or Wi-Fi UDP [1][4]. Wired and
  cheaper: a Pico or classic ESP32 with micro_ros_platformio [5], as
  [linorobot2](../software/linorobot2.md) does.
- **Fast loops, many encoders, CAN joints** (legged robots, arms on your own motor drivers): a
  Teensy 4.1 or an STM32 Nucleo, with a framed serial or CAN link into ros2_control.
- **Drones, outdoor GNSS rovers and boats:** [PX4](../software/px4.md) or
  [ArduPilot](../software/ardupilot.md) on a flight controller, joined to ROS 2 through their DDS
  bridges or [MAVROS](../software/mavros.md). Dynamixel robots: OpenCR or a U2D2.
- **On any board** the firmware stops the motors when valid commands stop: a command timeout in
  the control tick plus a hardware watchdog ([fw-mcu](../../skills/fw-mcu/SKILL.md), step 8).

## What decides it

- **The bus the actuators speak.** Servo buses and CAN drives need only an adapter; the stop on
  link loss then comes from the drive (CiA 402: heartbeat consumer and 0x6007). Hobby servos,
  steppers, encoder motors and analog sensors need an MCU. CiA 402 drives join ros2_control
  through [ros2_canopen](../software/ros2-canopen.md), your own CANopen board runs
  [CANopenNode](../software/canopennode.md), and any CAN device is tried first with
  [can-utils](../tools/can-utils.md) or [python-can](../software/python-can.md).
- **Real time and I/O.** A hardware timer on the MCU sets the control tick whatever Linux does.
  Encoders: pin interrupts on the Mega, PIO on the RP2040, four pulse counters on the ESP32-S3
  (eight on the classic ESP32), four hardware decoders on the Teensy 4.1, decoding timers on the
  F446RE. ESP32-S3 ADC2 stops while Wi-Fi runs.
- **micro-ROS fit.** It needs tens of kB of RAM, so not the Mega's 8 KB [1]. The micro-ROS site
  lists ESP32, Teensy 4.x, Pico and OpenCR as official; the Nucleo-F446RE is community only [1][6].
  Entity pools are fixed at build time (the ESP-IDF component allows 2 publishers and 2
  subscriptions) and a reliable publish blocks up to 1000 ms by default [3][4]. A best-effort
  message must fit one 512-byte MTU, so `nav_msgs/Odometry` (about 720 bytes) does not
  ([memory-qos](../../skills/fw-rtos-micro-ros/references/memory-qos.md)).
- **The computer side.** rosdistro does not release the micro-ROS agent: build it, natively for
  serial links (its README warns of packet loss on serial in Docker), or run its image for UDP
  [2][7]. It speaks only Fast DDS, so a robot on rmw_zenoh never sees the MCU. A framed serial
  protocol (COBS, CRC-16, sequence numbers) into ros2_control needs no agent or distro pin, but you
  own framing, timeouts and reconnection; TurtleBot3's node reads its OpenCR this way, over
  Dynamixel Protocol 2.0. At 115200 baud the link carries about 11.5 bytes per ms.
- **Wireless.** Only the ESP32 family here has a radio; no micro-ROS route documents the Pico W's
  Wi-Fi. Over Wi-Fi, publish best effort and let the firmware timeout guard the motors.
- **Toolchain and team.** [Arduino](../software/arduino.md) starts fastest; ESP-IDF opens the
  whole ESP32; the [Pico SDK](../../skills/fw-mcu/references/pico-sdk.md) and
  [STM32CubeMX](../../skills/fw-mcu/references/stm32-hal.md) are the vendor routes; Zephyr spans
  vendors but asks for CMake, Kconfig and devicetree; FreeRTOS comes inside ESP-IDF or CubeMX;
  PlatformIO pins the whole build per project. Debug probes: ST-LINK on the Nucleo, USB-JTAG built
  into the ESP32-S3, none on the Teensy or Mega.
- **Supply.** OpenCR was sold out at ROBOTIS US on 2026-11-27; the Pico is made until at least
  January 2036; PJRC calls Teensy 3.x legacy; the DevKitC-1 N8 and N8R2 boards are end of life.
- **Licences in the image.** micro-ROS, ESP-IDF (radio code as binaries) and Zephyr are Apache-2.0,
  FreeRTOS MIT, the Pico SDK and STM32 HAL BSD-3-Clause; ST's CubeMX tools and some headers carry
  ST's own terms [8]. The Arduino cores for ESP32 and RP2040 are LGPL-2.1: users must be able to
  relink. ArduPilot is GPL-3.0, so a shipped modified build owes its source; PX4 is BSD-3-Clause;
  ros2_canopen's CiA 402 driver is LGPL-3.0 with GPL-3.0 file headers [14].

## Options compared

Boards; prices are one unit from each part page, checked 2026-11-27.

| Option | Cost | Strengths | Limits | Best when |
|---|---|---|---|---|
| [ESP32-S3](../parts/mcu/espressif-esp32-s3.md) | $19.95 (DevKitC-1 N32R16V, Adafruit) | Wi-Fi and BLE; native USB with JTAG; one CAN (TWAI) controller; four pulse counters; FPU; 16 MB PSRAM on this board | 3.3 V only; ADC2 off with Wi-Fi; strapping pins; one CAN controller | Wireless robots, micro-ROS over Wi-Fi; classic ESP32 for Bluetooth Classic, Ethernet or eight encoders |
| [RP2040](../parts/mcu/raspberry-pi-rp2040.md) | $4.00 (Pico, Adafruit); Pico W $6 | Cheapest; PIO for servos and encoders; UF2 drag-and-drop flashing; official micro-ROS over USB and UART | No FPU, CAN or quadrature decoder; three ADC pins on the Pico | Servo co-processor; a cheap wired base |
| [Teensy 4.1](../parts/mcu/pjrc-teensy-4-1.md) | $31.50 (SparkFun) | 600 MHz Cortex-M7, double-precision FPU, 1 MB RAM; three CAN (one FD); Ethernet PHY; four quadrature decoders; official micro-ROS over USB, UART and Ethernet | No debug port; no 5 V tolerant pins; VIN and USB power joined | Legged robots, brushless arms, many encoders, CAN |
| [Nucleo-F446RE](../parts/mcu/st-nucleo-f446re.md) | $18.82 (DigiKey) | 180 MHz Cortex-M4F; two bxCAN; encoder timers; on-board ST-LINK; STM32Cube, Zephyr, Arduino | Community-only micro-ROS; CAN needs a transceiver; Zephyr clocks it at 84 MHz by default | CAN motor drivers; an STM32 path to your own board |
| [Mega 2560](../parts/mcu/arduino-mega-2560.md) | $49.90 (DigiKey) | 5 V logic, 54 I/O, four UARTs; RAMPS stepper shield; GRBL and Marlin | 8-bit, 16 MHz, 8 KB SRAM, no FPU or CAN; no micro-ROS | G-code stepper arms ([Thor](../robots/angellm-thor.md), [Moveo](../robots/bcn3d-moveo.md)); many hobby servos ([InMoov](../robots/inmoov.md)) |
| [OpenCR 1.0](../parts/mcu/robotis-opencr.md) | $247.14 (ROBOTIS US, sold out) | STM32F746; three TTL and three RS-485 Dynamixel ports; IMU; 12 V and 5 V outputs; official micro-ROS | Price and stock; Arduino tools for x86 hosts only; repo quiet since 2023; no Zephyr board | Dynamixel robots: TurtleBot3, [OpenManipulator-X](../robots/openmanipulator-x.md) |

Firmware stack and link to ROS 2:

| Option | Cost | Strengths | Limits | Best when |
|---|---|---|---|---|
| [Arduino](../software/arduino.md) | Free; API and the ESP32 and RP2040 cores LGPL-2.1 | Quickest start; one API on AVR, ESP32, RP2040, STM32, Teensy; prebuilt micro-ROS for Teensy, OpenCR, ESP32 | Core majors break sketches (Arduino-ESP32 2.x, 3.x, 4.0); LGPL relink duty | Prototypes; one loop on one board |
| [ESP-IDF](../software/esp-idf.md) | Free, Apache-2.0; radio code binary | Whole chip: both cores, Kconfig, `idf.py`; micro-ROS component (`^24` for Jazzy) [4] | ESP32 only; stack sizes in bytes; micro-ROS tested to 6.0, not 6.1 | ESP32-S3 firmware you will ship |
| Pico SDK, STM32Cube ([fw-mcu](../../skills/fw-mcu/SKILL.md)) | Free; SDK and HAL BSD-3-Clause, ST tools under ST's terms | Every peripheral; CubeMX clocks and pin code; micro-ROS Pico library and STM32 utilities | One vendor each; the Pico micro-ROS library is precompiled for one GCC | RP2040 or STM32 past the prototype |
| [Zephyr](../software/zephyr.md) | Free, Apache-2.0 | One driver API (CAN, USB, sensors) across vendors; 3.7 LTS to 2029-07-27 | Three configuration languages; micro-ROS module tested on 4.0 and 4.1; no AVR or OpenCR | Firmware that must move between vendors |
| [FreeRTOS](../software/freertos.md) | Free, MIT | Small kernel in ESP-IDF and CubeMX; tasks for several rates; under the STM32 and ESP32 micro-ROS routes | Kernel only; interrupt-priority rules; stack overflows look random | micro-ROS beside a control task |
| [PlatformIO](../tools/platformio.md) | Free, Apache-2.0 | Pins platform, framework, board, libraries; `pio test`; micro_ros_platformio | That library: last release 2.0.0 (2023), defaults to Kilted, no ESP32-S3 target [5] | Reproducible Arduino or ESP-IDF builds in CI |
| [micro-ROS](../software/micro-ros.md) | Free, Apache-2.0 [8] | The MCU is a ROS 2 node; no driver node to write | Agent not in apt; fixed pools; best effort under 512 bytes; Fast DDS only; per-board routes stop at Kilted | Sensors out, `cmd_vel` in, on a 32-bit board |
| Framed serial into ros2_control ([fw-serial-can](../../skills/fw-serial-can/SKILL.md)) | Your own code | Any MCU, the Mega too; any distro and RMW; one exchange per control cycle | You own framing, CRC, timeouts, reconnection | ros2_control robots; Lyrical; rmw_zenoh |
| CAN: [ros2_canopen](../software/ros2-canopen.md), [CANopenNode](../software/canopennode.md), SocketCAN | Free; 402 driver LGPL-3.0, CANopenNode Apache-2.0 | Many nodes on one pair with arbitration; CiA 402 drives as ros2_control joints | ros2_canopen calls itself not yet ready for production [14]; its ros2_control plugin fails on Lyrical | CAN drives; several boards in a legged robot |
| [PX4](../software/px4.md), [ArduPilot](../software/ardupilot.md) | Free; BSD-3-Clause, GPL-3.0 | Tested estimation, modes, missions, failsafes; DDS bridges and MAVROS | Flight-controller hardware; ArduPilot's DDS needs an H7 [13]; `px4_msgs` must match the firmware [10] | Drones; ArduPilot Rover for outdoor bases and boats |

## Distros and agents

- micro-ROS's per-board routes (PlatformIO, Arduino, ESP-IDF, STM32Cube, Zephyr) cover Humble to
  Kilted; Lyrical reaches only micro_ros_setup and the agent [5][6]. Pin one distro everywhere:
  micro_ros_platformio and micro_ros_setup default to Kilted.
- `micro_ros_agent` bundles Micro XRCE-DDS Agent v2.4.2 on its `humble` branch, v2.4.3 on `jazzy`,
  v3.0.1 on `kilted` and v3.0.2 on `lyrical` [2]: build your distro's branch.
- PX4's own table pairs its client with a standalone `MicroXRCEAgent`: v2.4.2 for Humble, v2.4.3
  for Jazzy and Kilted, v3.0.2 for Lyrical with a PX4 build that sets `UXRCE_DDS_CLIENT_USE_DDS_V3`
  [9]. The lists cover different clients: on Kilted, PX4's default build pairs with 2.4.3, not the
  3.0.1 inside `micro_ros_agent`. PX4 recommends Jazzy [10].
- ArduPilot's AP_DDS client talks to `micro_ros_agent` [13]. Its dev docs name Humble [11]; its
  `Tools/ros2` README says Humble or Jazzy and ships a Jazzy repos file [12].

## When the answer changes

- **Lyrical:** no Lyrical agent image on Docker Hub, and firmware from another distro against a
  Lyrical agent is untested ([fw-rtos-micro-ros](../../skills/fw-rtos-micro-ros/SKILL.md)): stay on
  Jazzy or use a serial link. `canopen_ros2_control` does not build against Lyrical either
  ([ros2_canopen](../software/ros2-canopen.md)).
- **The robot moves to rmw_zenoh:** the MCU drops off the graph; use the serial or CAN route.
- **Many axes with sub-millisecond cycles:** EtherCAT, with GPL masters and no binary
  `ethercat_driver_ros2` ([ethercat.md](../../skills/fw-serial-can/references/ethercat.md)).
- **ESP-IDF 6.1:** the micro-ROS component is tested on 5.2 to 6.0 [4]; pin one of those.
- **Prototype to product:** Arduino to ESP-IDF, a vendor SDK or Zephyr's LTS; settle licences.
- **OpenCR out of stock:** a U2D2 adapter and a power hub drive Dynamixels from the computer.

## Sources

1. [micro-ROS docs: Supported hardware](https://micro.vulcanexus.org/docs/overview/hardware/), accessed 2026-11-27
2. [micro-ROS-Agent README and branches (humble, jazzy, kilted, lyrical): cmake/SuperBuild.cmake](https://github.com/micro-ROS/micro-ROS-Agent), accessed 2026-11-27
3. [rmw_microxrcedds README (jazzy branch)](https://github.com/micro-ROS/rmw_microxrcedds/tree/jazzy), accessed 2026-11-27
4. [micro_ros_espidf_component README (jazzy branch)](https://github.com/micro-ROS/micro_ros_espidf_component/tree/jazzy), accessed 2026-11-27
5. [micro_ros_platformio README](https://github.com/micro-ROS/micro_ros_platformio), accessed 2026-11-27
6. [micro_ros_setup README and config folder (kilted branch)](https://github.com/micro-ROS/micro_ros_setup), accessed 2026-11-27
7. [rosdistro distribution files (humble, jazzy, kilted, lyrical)](https://github.com/ros/rosdistro), accessed 2026-11-27
8. [micro-ROS docs: License overview](https://micro.vulcanexus.org/docs/overview/license/), accessed 2026-11-27
9. [PX4 docs: uXRCE-DDS (PX4-ROS 2/DDS bridge)](https://docs.px4.io/main/en/middleware/uxrce_dds.html), accessed 2026-11-27
10. [PX4 docs: ROS 2 user guide](https://docs.px4.io/main/en/ros2/user_guide.html), accessed 2026-11-27
11. [ArduPilot dev docs: ROS 2 interfaces](https://ardupilot.org/dev/docs/ros2-interfaces.html), accessed 2026-11-27
12. [ArduPilot Tools/ros2 README (master)](https://github.com/ArduPilot/ardupilot/blob/master/Tools/ros2/README.md), accessed 2026-11-27
13. [ArduPilot dev docs: ROS 2 on Raspberry Pi](https://ardupilot.org/dev/docs/ros2-pi.html), accessed 2026-11-27
14. [ros2_canopen README, package.xml and LICENSE files (master)](https://github.com/ros-industrial/ros2_canopen), accessed 2026-11-27
