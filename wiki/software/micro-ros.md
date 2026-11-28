---
type: tool
name: micro-ROS
summary: ROS 2 on microcontrollers - rclc nodes on the MCU speak Micro XRCE-DDS over serial, USB or UDP to an agent on the robot computer, which puts them on the ROS 2 graph; Apache-2.0, static memory sized at build time, Jazzy on every build route, Lyrical only in micro_ros_setup and the agent.
tags: [micro-ros, ros2, rclc, micro-xrce-dds, micro-ros-agent, mcu, freertos, zephyr, esp32, teensy, stm32, platformio, serial, udp]
kind: framework
area: firmware
support:
license: Apache-2.0
links: {repo: "https://github.com/micro-ROS/micro_ros_setup", docs: "https://micro.vulcanexus.org/docs/overview/features/", site: "https://micro.vulcanexus.org"}
version: {tested: , latest: 7.0.0, as_of: 2026-11-27}
platforms: [linux, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://github.com/micro-ROS/micro_ros_setup", title: "micro_ros_setup README, branches, tags, configs and issues", accessed: 2026-11-27}
  - {url: "https://micro.vulcanexus.org/docs/overview/hardware/", title: "micro-ROS docs: Supported hardware", accessed: 2026-11-27}
  - {url: "https://micro.vulcanexus.org/docs/overview/license/", title: "micro-ROS docs: License overview", accessed: 2026-11-27}
  - {url: "https://micro.vulcanexus.org/docs/concepts/benchmarking/memo_prof/", title: "micro-ROS docs: Memory profiling", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro-ROS-Agent", title: "micro-ROS-Agent README, branches, tags and source", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/docker", title: "micro-ROS Docker images: README, agent Dockerfile and Docker Hub tags", accessed: 2026-11-27}
  - {url: "https://micro-xrce-dds.docs.eprosima.com/en/latest/agent.html", title: "Micro XRCE-DDS docs: Agent", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/rmw_microxrcedds/tree/jazzy", title: "rmw_microxrcedds README (jazzy branch)", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_platformio", title: "micro_ros_platformio README, metas and platform code", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_arduino", title: "micro_ros_arduino README, tags and examples", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_espidf_component/tree/jazzy", title: "micro_ros_espidf_component README and examples (jazzy branch), ESP Component Registry versions", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_stm32cubemx_utils", title: micro_ros_stm32cubemx_utils README, accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_zephyr_module", title: "micro_ros_zephyr_module README, Kconfig and prj.conf", accessed: 2026-11-27}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files (humble, jazzy, kilted, lyrical)", accessed: 2026-11-27}
---

# micro-ROS

micro-ROS runs ROS 2 nodes on a microcontroller. The firmware links ROS 2's C client library
(`rcl`, with the `rclc` layer) over `rmw_microxrcedds`, which speaks DDS-XRCE to the micro-ROS
agent on the robot computer; the agent creates the DDS entities, so the MCU's topics and services
join the ROS 2 graph [5][8]. All of it is Apache-2.0 [3], maintained by eProsima [1]. The docs
moved to micro.vulcanexus.org [2]; the READMEs' old `micro.ros.org/docs/` links now return 404.

## When to use it

- **Use it** when the MCU should be a ROS 2 node: sensor data out, `cmd_vel` or setpoints in, no
  driver node to write, as in [linorobot2](linorobot2.md). It needs tens of kB of RAM [2]: an
  [ESP32-S3](../parts/mcu/espressif-esp32-s3.md), [Teensy 4.1](../parts/mcu/pjrc-teensy-4-1.md),
  [RP2040](../parts/mcu/raspberry-pi-rp2040.md) or [Nucleo](../parts/mcu/st-nucleo-f446re.md);
  no list names an 8-bit AVR like the [Mega 2560](../parts/mcu/arduino-mega-2560.md) [1][2][9].
- **Use a custom serial protocol and a node instead**, often a [ros2_control](ros2-control.md)
  hardware interface, when computer-side controllers close the loop, the MCU is small, or the link
  must outlive distro upgrades. No agent, pools or distro pin, but you own framing, checksums,
  reconnection and timestamps ([fw-serial-can](../../skills/fw-serial-can/SKILL.md)).
- **Use the autopilot's link** for [PX4](px4.md) or [ArduPilot](ardupilot.md), and
  [ros2_canopen](ros2-canopen.md) for CANopen drives.

## Setup

**Distros.** `micro_ros_setup` supports Humble, Jazzy, Kilted, Lyrical and Rolling, one branch
each; its default branch is `kilted` [1]. Lyrical stops at the core:

| Piece | Humble | Jazzy | Kilted | Lyrical |
|---|---|---|---|---|
| `micro_ros_setup`, newest tag [1] | 3.1.3 | 5.0.2 (2026-05-27) | 6.1.0 | 7.0.0 (2026-10-09) |
| Micro XRCE-DDS Agent inside `micro_ros_agent` [5] | v2.4.2 | v2.4.3 | v3.0.1 | v3.0.2 |
| `microros/micro-ros-agent` image, amd64 and arm64 [6] | yes | yes | yes | no tag |
| PlatformIO, Arduino, ESP-IDF, STM32Cube, Zephyr routes [9]-[13] | yes | yes | yes | no |

rosdistro releases `rclc` and `micro_ros_msgs` but not the agent or `micro_ros_setup`: there is
no `ros-jazzy-micro-ros-agent` apt package [14]. **Run the agent** from Docker [6]:

```bash
docker run -it --rm --net=host -v /dev:/dev --privileged \
  microros/micro-ros-agent:jazzy serial --dev /dev/ttyACM0 -v6
```

Or build it: `micro_ros_setup` (branch `jazzy`), then `create_agent_ws.sh` and `build_agent.sh` [1].
Transports: `serial --dev <tty> -b <baud>` (USB CDC too), `udp4`/`udp6`/`tcp4`/`tcp6 --port <n>`,
`canfd --dev <iface>`; `-v 0..6` sets the log level [7].

**Firmware build routes**, all Apache-2.0 (last commit: newest on any branch):

| Route | Targets, as upstream lists them | Distros | Last commit |
|---|---|---|---|
| `micro_ros_platformio` [9] | Arduino framework: Teensy 3.x/4.x, ESP32 Dev, Pico, Pico 2, Nano RP2040 Connect, Portenta H7, Due, Zero, Olimex E407 | Humble, Jazzy, Kilted (default), Rolling; one `main` branch | 2025-09-17 |
| `micro_ros_espidf_component` [11] | ESP32, -S2, -S3, -C3, -C6, -P4 on ESP-IDF 5.2 to 6.0 | Registry 22.x Humble, 24.x Jazzy, 25.x Kilted, Rolling pre-releases | 2026-10-02 |
| `micro_ros_arduino` [10] | Precompiled: Portenta H7, Nano RP2040 Connect, OpenCR, Teensy 3.2/3.6/4.1, ESP32 Dev (core 2.0.2); 12 community boards | Humble, Jazzy, Kilted (`v2.0.8-<distro>`) | 2025-12-09 |
| `micro_ros_stm32cubemx_utils` [12] | Any CubeMX or CubeIDE project: UART (DMA or IRQ), USB CDC, UDP over LwIP | Humble, Jazzy, Kilted, Rolling | 2025-09-15 |
| `micro_ros_zephyr_module` [13] | Zephyr boards, tested on Zephyr 4.0 and 4.1: UART, USB serial, UDP | Humble, Jazzy, Kilted, Rolling | 2025-12-15 |
| `micro_ros_setup` [1] | FreeRTOS: ESP32, Crazyflie 2.1, Olimex E407, Nucleo F446RE/ZE, F746ZG, F767ZI. Zephyr: Olimex E407, Nucleo F446RE, H743ZI, B-L475E-IOT01A, emulator. Linux host, static library | All five | 2026-11-26 |

`micro_ros_setup` calls its own support basic; 57 issues are open, and 2026 ones got replies [1].
The other routes are quiet since late 2025, ESP-IDF aside. **The docs list other boards:** Renesas
RA6M5, Portenta H7, Pico, OpenCR and Teensy (other routes), NuttX on the Olimex E407 (gone from
`micro_ros_setup`), H743ZI on FreeRTOS not Zephyr, and no Nucleo F446RE or F767ZI [1][2].

**First firmware with PlatformIO** (needs git, cmake and pip; macOS also `brew install binutils`):
in the board's `[env]` set `board_microros_distro = jazzy`, `board_microros_transport = serial`
and `lib_deps = https://github.com/micro-ROS/micro_ros_platformio`; in `setup()` call
`Serial.begin(115200); set_microros_serial_transports(Serial);`; `pio run -t upload` [9].
ESP-IDF: `idf.py add-dependency "micro-ros/micro_ros_espidf_component^24"` (Jazzy) in a shell
without ROS 2 sourced [11].

## How an agent works with it

Skill: [fw-rtos-micro-ros](../../skills/fw-rtos-micro-ros/SKILL.md). Tools: `pio`, `idf.py`, `west`.

**Memory is fixed at build time.** `rmw_microxrcedds` keeps each entity type in a static pool
sized by CMake flags in a colcon `.meta` file; pools grow only with
`RMW_UXRCE_ALLOW_DYNAMIC_ALLOCATIONS` [8]. Nodes: 4 by default, 1 in PlatformIO and ESP-IDF.

| Flag | rmw default [8] | PlatformIO `colcon.meta` [9] | ESP-IDF [11] |
|---|---|---|---|
| `RMW_UXRCE_MAX_PUBLISHERS` / `_SUBSCRIPTIONS` | 4 / 4 | 10 / 5 | 2 / 2 |
| `RMW_UXRCE_MAX_SERVICES` / `_CLIENTS` | 4 / 4 | 1 / 1 | 1 / 1 |
| `RMW_UXRCE_MAX_HISTORY` (subscription slots) | 8 | 4 | 1 |

The meta: PlatformIO `board_microros_user_meta` [9]; Arduino `extras/library_generation/*.meta`
plus a `micro_ros_static_library_builder` rebuild [10]; ESP-IDF and STM32 `colcon.meta` [11][12];
Zephyr `modules/libmicroros/colcon.meta` [13]; `micro_ros_setup` `config/<rtos>/<board>/` [1].

**Upstream's footprint** (ESP32, FreeRTOS, UDP, defaults): about 400 B per publisher, 500 B per
subscriber, 300 B per service or client; each RMW history slot adds MTU × XRCE history, 2 KB at
the 512 B default MTU [4]. Give a FreeRTOS micro-ROS task over 10 kB of stack [12].

**Check the result:** the agent log at `-v4` shows `session established`, then `participant
created` and `datawriter created`; then `ros2 topic list` and `ros2 topic echo`, with
`ROS_DOMAIN_ID` matching the firmware's `rcl_init_options_set_domain_id` call [11]. Through Fast
DDS the agent joins that domain [5]; nodes on [rmw_zenoh](rmw-zenoh.md) never see it.

## Traps

- **Distro mismatch.** Pin one distro everywhere. PlatformIO and `micro_ros_setup` default to
  Kilted; Arduino tags and ESP-IDF majors name it (`v2.0.8-jazzy`, `^24`) [1][9][10][11].
- **Entities fail at boot.** Suspect a full pool [8]; check every return code. After a meta
  change run `pio run -t clean_microros` or `idf.py clean-microros`, or the old build stays [9][11].
- **Big messages.** Best-effort streams do not fragment: a message must fit one 512 B MTU; reliable
  ones reach MTU × `RMW_UXRCE_STREAM_HISTORY` (a power of two), 2 KB by default [4][8].
- **Reliable publishing blocks** for the agent's acknowledgement, up to 1000 ms by default
  (`RMW_UXRCE_PUBLISH_RELIABLE_TIMEOUT`) [8]. Publish fast sensor data best effort, as the Wi-Fi
  examples do [10], keep motor loops in another task, and subscribe best effort on the computer.
- **Time since boot.** The Arduino port's clock counts `micros()` from power-on [9]. Once
  connected, call `rmw_uros_sync_session(timeout_ms)`; stamp with `rmw_uros_epoch_millis()` [10].
- **Agent restarts.** The firmware must rebuild its entities: the Arduino example pings with
  `rmw_uros_ping_agent(100, 1)` every 200 ms and on failure destroys them and waits again [10].
- **Serial and USB.** The transport owns `Serial`; debug prints there corrupt it [9]. The agent
  defaults to 115200 baud, waits for the device, and runs serial only on Linux (WSL on Windows)
  [7][12]. ESP32-S2/S3: the ESP-IDF example runs on native USB, not the USB-UART port you flash
  through, with logs on a second CDC port [11]. Name ports by `/dev/serial/by-id/`.
- **Agent in Docker or a snap.** Upstream warns of packet loss on serial ports passed into a Docker
  agent and of serial bugs in the snap; a source build avoids both [5]. The image disables Fast DDS
  shared memory so host nodes get data over UDP [6]; keep `--net=host`.
- **Licences in one image.** Apache-2.0 asks you to ship its licence and the NOTICE texts, not your
  source [3]. RTOS and HAL code keep their own terms: the docs flag ST-licensed headers in the
  FreeRTOS apps and GPL build scripts (not linked) in ESP-IDF and Zephyr [3].

## Alternatives

- A custom serial or CAN link: [ros2_control](ros2-control.md), [python-can](python-can.md),
  [can-utils](../tools/can-utils.md). [PX4](px4.md) has its own XRCE-DDS client; ArduPilot's
  uses `micro_ros_agent` ([MAVROS](mavros.md)).
- Under it: [FreeRTOS](freertos.md), [Zephyr](zephyr.md), [ESP-IDF](esp-idf.md),
  [Arduino](arduino.md), [PlatformIO](../tools/platformio.md); guide:
  [Choose an MCU and firmware stack](../guides/choose-an-mcu-and-firmware-stack.md).

## Sources

1. [micro_ros_setup README, branches, tags, configs and issues](https://github.com/micro-ROS/micro_ros_setup), accessed 2026-11-27
2. [micro-ROS docs: Supported hardware](https://micro.vulcanexus.org/docs/overview/hardware/), accessed 2026-11-27
3. [micro-ROS docs: License overview](https://micro.vulcanexus.org/docs/overview/license/), accessed 2026-11-27
4. [micro-ROS docs: Memory profiling](https://micro.vulcanexus.org/docs/concepts/benchmarking/memo_prof/), accessed 2026-11-27
5. [micro-ROS-Agent README, branches, tags and source](https://github.com/micro-ROS/micro-ROS-Agent), accessed 2026-11-27
6. [micro-ROS Docker images: README, agent Dockerfile and Docker Hub tags](https://github.com/micro-ROS/docker), accessed 2026-11-27
7. [Micro XRCE-DDS docs: Agent](https://micro-xrce-dds.docs.eprosima.com/en/latest/agent.html), accessed 2026-11-27
8. [rmw_microxrcedds README (jazzy branch)](https://github.com/micro-ROS/rmw_microxrcedds/tree/jazzy), accessed 2026-11-27
9. [micro_ros_platformio README, metas and platform code](https://github.com/micro-ROS/micro_ros_platformio), accessed 2026-11-27
10. [micro_ros_arduino README, tags and examples](https://github.com/micro-ROS/micro_ros_arduino), accessed 2026-11-27
11. [micro_ros_espidf_component README and examples (jazzy branch), ESP Component Registry versions](https://github.com/micro-ROS/micro_ros_espidf_component/tree/jazzy), accessed 2026-11-27
12. [micro_ros_stm32cubemx_utils README](https://github.com/micro-ROS/micro_ros_stm32cubemx_utils), accessed 2026-11-27
13. [micro_ros_zephyr_module README, Kconfig and prj.conf](https://github.com/micro-ROS/micro_ros_zephyr_module), accessed 2026-11-27
14. [rosdistro distribution files (humble, jazzy, kilted, lyrical)](https://github.com/ros/rosdistro), accessed 2026-11-27
