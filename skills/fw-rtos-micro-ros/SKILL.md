---
name: fw-rtos-micro-ros
description: Split robot MCU firmware into FreeRTOS or Zephyr tasks (priorities, queues, xTaskDelayUntil, stacks, hooks) and put it on ROS 2 Jazzy with micro-ROS - rclc publisher, subscriber, timer and executor, the micro_ros_agent (source build or Docker), serial, USB and UDP transports,
  micro_ros_platformio, micro_ros_arduino, the ESP-IDF component, STM32CubeMX utils, micro_ros_setup, colcon.meta memory limits, MTU and QoS, time sync,
  a cmd_vel timeout that stops the motors, and reconnecting after the agent restarts (ping and agent-state machine).
license: Apache-2.0
metadata:
  sources: []
  evidence: researched
  last_verified: 2026-11-27
---

# RTOS tasks and micro-ROS

Lets an agent split MCU firmware into RTOS tasks with safe timing and put it on the ROS 2 graph
with micro-ROS: build the library for the board, run the agent, publish and subscribe through an
rclc executor, stop the motors when commands stop, rebuild the session after the agent drops, and
stamp messages with synced time. Checked on 2026-11-27 against the micro-ROS `jazzy` branches
(rclc 6.1.2, rmw_microxrcedds 5.0.1, micro_ros_agent 5.0.2 on Micro XRCE-DDS Agent 2.4.3),
micro_ros_platformio 2.0.0, FreeRTOS-Kernel V11.3.3 and ESP-IDF v6.1; the recipes were not run.

## When to use

- Laying out firmware tasks: priorities, stack sizes, a periodic control loop, queues between
  control and communication, ISR-to-task signalling (FreeRTOS, ESP-IDF FreeRTOS, Zephyr threads).
- Making an MCU a ROS 2 node: rclc publishers, subscriptions, timers and executor; the agent on the
  robot computer; serial, USB CDC or UDP transport.
- Choosing and running a micro-ROS build path: micro_ros_platformio, micro_ros_arduino, the ESP-IDF
  component, STM32CubeMX utils, the Pico SDK library, the Zephyr module, micro_ros_setup.
- Fixing: the node never appears, topics appear but carry nothing, publishing stops after an agent
  restart, the third publisher fails to init, the micro-ROS task overflows its stack, stamps are
  wrong, the robot keeps driving after the commands stop.

Elsewhere: board and toolchain choice, flash and debug, clocks, interrupts, timers, DMA and the
hardware watchdog in [fw-mcu](../fw-mcu/SKILL.md); UART and RS-485 framing, Linux serial and CAN in
[fw-serial-can](../fw-serial-can/SKILL.md); sensor drivers in the later `fw-peripherals` and
`fw-drivers`; motor control and encoders in the later `fw-motor-control`; PID in the later
`control-systems`. An MCU that speaks its own serial protocol to a ros2_control hardware interface
on the computer is the alternative to micro-ROS: [ros2-control](../ros2-control/SKILL.md) and
[choose an MCU and firmware stack](../../wiki/guides/choose-an-mcu-and-firmware-stack.md).

## Quick start

An ESP32 dev board on USB, PlatformIO with the Arduino framework, a robot computer on Jazzy.

```bash
# Robot computer: no apt package exists for the agent; build it in the robot workspace
cd /home/robot/ros2_ws && source /opt/ros/jazzy/setup.bash
git clone -b jazzy https://github.com/micro-ROS/micro-ROS-Agent.git src/micro-ROS-Agent
rosdep install --from-paths src --ignore-src -y && colcon build --packages-up-to micro_ros_agent
source install/setup.bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/my_robot_mcu -b 115200
```

```ini
; my_robot_firmware/platformio.ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
board_microros_distro = jazzy          ; the default is kilted
board_microros_transport = serial
lib_deps = https://github.com/micro-ROS/micro_ros_platformio
```

```bash
pio run -t upload        # firmware: references/firmware-skeleton.md, Serial.begin(115200) in board_transport_init
ros2 node list           # /my_robot_firmware
ros2 topic hz /wheel_states
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.1}}"   # wheels off the ground
```

Stop the `ros2 topic pub` with Ctrl-C: the wheels must stop within the command timeout.

## Workflow

1. **Pick the build path for the board.** Teensy 4, classic ESP32 and the Pico on
   micro_ros_platformio; ESP32-S3 and other new Espressif chips on the ESP-IDF component; STM32 on
   STM32CubeMX utils; Zephyr boards on the Zephyr module. No path supports AVR boards (Uno, Mega
   2560). Set the distro to `jazzy` wherever the path has a default.
   [references/build-paths.md](references/build-paths.md).
   *Check:* the first build links; on PlatformIO `pio run -v` shows `-DMICRO_ROS_DISTRO_JAZZY` and
   the `-DMICRO_ROS_TRANSPORT_...` you chose; on ESP-IDF `dependencies.lock` shows the component at `24.x`.

2. **Lay out the tasks.** A periodic `control` task at the highest application priority, paced by
   `xTaskDelayUntil` or a timer-ISR notification; a lower-priority `micro_ros` task that makes
   every rcl, rclc and rmw call; length-1 queues with `xQueueOverwrite` and `xQueuePeek` between
   them. Stack depth is in words on vanilla FreeRTOS and in bytes on ESP-IDF; give the micro-ROS
   task more than 10 kB. Turn on stack-overflow checking, the malloc-failed hook and `configASSERT`.
   [references/rtos-tasks.md](references/rtos-tasks.md).
   *Check:* after ten minutes that include two agent restarts, `uxTaskGetStackHighWaterMark` shows
   margin on every task, `xTaskDelayUntil` never returned `pdFALSE`, and no hook fired.

3. **Size the micro-ROS memory at build time.** Count nodes, publishers, subscriptions, services,
   clients and timers; set `RMW_UXRCE_MAX_*` in the path's meta file or Kconfig; check every
   message against the MTU (best effort carries at most about 500 bytes by default, so
   `nav_msgs/Odometry` does not fit). Rebuild the library after each change.
   [references/memory-qos.md](references/memory-qos.md).
   *Check:* the generated `rmw_microxrcedds_c/config.h` shows your limits, and every
   `rclc_*_init_*` returns `RCL_RET_OK`.

4. **Write the node.** `rclc_support_init_with_options` with the robot's domain ID, one node, a
   best-effort publisher on a timer for sensor data, a subscription for `cmd_vel`, and an executor
   whose handle count covers every subscription and timer. Give message strings and sequences
   static memory once at boot. Skeleton: [references/firmware-skeleton.md](references/firmware-skeleton.md).
   *Check:* `ros2 node list` shows `/my_robot_firmware`; `ros2 topic info -v /wheel_states` shows
   the QoS you chose; `ros2 topic hz` matches the timer.

5. **Stop the motors when commands stop.** The subscription callback rejects NaN, clamps, and
   stores the command with its tick; the control task drives only while the command is younger
   than the timeout (example: 300 ms) and calls `motors_stop()` otherwise. That one rule covers a
   silent publisher, a dead agent, a cut cable and a hung micro-ROS task. Feed the hardware
   watchdog only from the control loop. This is not a rated safety function: the E-stop chain is
   in [arch-safety](../arch-safety/SKILL.md).
   *Check:* wheels off the ground, publish `cmd_vel` at 10 Hz, then stop it, kill the agent, and
   unplug the USB in turn; each time the wheels stop within the timeout.

6. **Survive the agent dropping.** The micro-ROS task runs the agent-state machine: ping until the
   agent answers, create the entities, ping every 500 ms while connected, and on failure destroy
   everything with the destroy timeout set to 0, then start over. Re-sync the clock after every
   reconnect. [references/reconnect-timesync.md](references/reconnect-timesync.md).
   *Check:* restart the agent three times; each time `/my_robot_firmware` and its topic rates
   return within a few seconds, and the motors stay stopped while it is away.

7. **Stamp with synced time.** Call `rmw_uros_sync_session(timeout_ms)` after connecting and
   periodically (example: every 10 s); stamp from `rmw_uros_epoch_nanos()` split into `sec` and
   `nanosec`; publish stamped messages only while `rmw_uros_epoch_synchronized()` is true. The
   agent's computer must itself be synced ([ops-bringup time sync](../ops-bringup/references/time-sync.md)).
   Code and details: [references/reconnect-timesync.md](references/reconnect-timesync.md).
   *Check:* `ros2 topic delay /wheel_states` shows a small, steady delay, not seconds or years.

8. **Run the agent with the robot.** Native build for serial links (the agent README reports packet
   loss on serial inside Docker; Docker suits UDP), a udev name such as `/dev/my_robot_mcu` with
   ModemManager kept off, and the agent started by the bringup launch file or its own systemd unit
   with restart on failure. Keep the robot on a DDS middleware.
   [references/agent.md](references/agent.md).
   *Check:* after a reboot of the computer, and separately after a reset of the MCU, the node
   returns with no one touching anything.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| `apt install ros-jazzy-micro-ros-agent` finds nothing | The agent is not in rosdistro | Build the `jazzy` branch or use `microros/micro-ros-agent:jazzy` |
| Node never appears; agent prints nothing for the client | Wrong device or baud, TX/RX swapped, serial monitor or ModemManager holding the port | `-v6` on the agent; free the port; match `-b` to the firmware's UART |
| Agent shows `session established`, `ros2 node list` stays empty | Firmware's domain ID differs from the robot's; or the robot runs `rmw_zenoh_cpp` | `rcl_init_options_set_domain_id`; a DDS middleware on the robot |
| `ros2 topic echo` shows data, your node on the computer gets none | Best-effort publisher, reliable subscriber (the CLI adapts its QoS, your node does not) | Sensor-data QoS on the subscriber ([ros2-core](../ros2-core/SKILL.md)) |
| One topic never arrives, others do | Message larger than MTU minus 12 bytes on a best-effort stream | Smaller message, reliable publisher, or larger MTU ([memory-qos.md](references/memory-qos.md)) |
| Third publisher or second subscription returns `RCL_RET_ERROR` | Build-time pool full (ESP-IDF default: 2 publishers, 2 subscriptions) | Raise `RMW_UXRCE_MAX_*`, rebuild the library |
| Board built for the wrong distro | micro_ros_platformio defaults to `kilted` | `board_microros_distro = jazzy`, `pio run -t clean_microros` |
| Meta change has no effect | Library not rebuilt | `clean_microros`, `idf.py clean-microros`, or rerun the library builder |
| Publishing stops for good after an agent restart | No reconnect logic; old session gone | Ping and agent-state machine (step 6) |
| Reconnect takes seconds, control jitters | Entity destroy waits for the dead agent; control shares the micro-ROS task | Destroy timeout 0; separate control task |
| Motors keep the last command when the link dies | No command timeout in firmware | Step 5; never rely on the computer to send a stop |
| Robot jerks forward and stops under `teleop_twist_keyboard` | It publishes once per key press; the timeout stops the base between presses | Hold the key (auto-repeat), or use a teleop that publishes at a fixed rate; keep the timeout |
| Control loop stalls up to a second at a time | Reliable publish, ping or entity creation in the control path | Move every micro-ROS call to the micro-ROS task |
| Stack overflow hook names the micro-ROS task | Stack too small, or words vs bytes mixed up | More than 10 kB; ESP-IDF counts bytes |
| Malloc-failed hook at entity creation | Heap too small for rcl allocations, or the allocator not set | Larger `configTOTAL_HEAP_SIZE`; `rcutils_set_default_allocator` before `rclc_support_init` |
| Stamps near 1970, TF drops the data | Stamped before the first `rmw_uros_sync_session`, or not re-synced after a reconnect | Publish only while `rmw_uros_epoch_synchronized()`; split nanoseconds into `sec` and `nanosec` |
| `frame_id` empty, or a string field lost on receive | `micro_ros_string_utilities_set` result discarded; no capacity for incoming strings | Assign its return value; preallocate capacities |
| Firmware hangs at boot with Wi-Fi down | `set_microros_wifi_transports` waits for Wi-Fi forever | Stop the motors first; or call it at the start of the micro-ROS task so control keeps running |
| Garbage on the link, agent errors | `Serial.print` on the UART micro-ROS uses | Debug on another UART |
| Old example sets `configUSE_HEAP_SCHEME`, calls `vTaskDelayUntil` or `vTaskList` | The macro never existed; the two calls remain only for compatibility | Compile one `heap_N.c`; `xTaskDelayUntil`; `vTaskListTasks(buf, len)` on V11 |

## Checks

- Every `rclc_*_init_*` and `rclc_executor_add_*` returns `RCL_RET_OK`; the build's `config.h`
  limits match the entity count.
- `ros2 node list`, `ros2 topic info -v` and `ros2 topic hz` show the node, the intended QoS and the
  designed rates; `ros2 topic delay` is small and steady.
- Stopping `cmd_vel`, killing the agent and unplugging the link each stop the motors within the
  timeout (wheels off the ground); none of them resets the MCU.
- Three agent restarts and one MCU reset each recover with no manual step.
- Stack high-water marks and the minimum free heap leave margin after a long run with reconnects.
- No micro-ROS call outside the micro-ROS task; control timing unchanged while the agent is down.
- Firmware, agent and robot are on one distro; the agent and library commits are recorded.

## Distro differences

- **Humble:** rclc 4.0 has no `rclc_timer_init_default2`; use `rclc_timer_init_default` (it has no
  autostart flag). The other calls used here exist on the `humble` branches; use the `humble`
  Docker tag, `board_microros_distro = humble` and ESP-IDF component `^22`.
- **Lyrical:** micro_ros_setup, micro-ROS-Agent, rmw_microxrcedds, micro_ros_utilities and the
  demos have `lyrical` branches; its agent builds Micro XRCE-DDS Agent v3.0.2 (Jazzy: v2.4.3).
  No `microros/micro-ros-agent:lyrical` image on Docker Hub yet; micro_ros_platformio accepts only
  humble, jazzy, kilted and rolling; micro_ros_arduino, the ESP-IDF component (Registry line
  `26.x.y` reserved), STM32CubeMX utils and the Zephyr module have no `lyrical` branch. Pairing a
  firmware built for another distro with a Lyrical agent is untested. rclc 6.3 keeps the calls used
  here. Nav2 publishes `TwistStamped` by default from Kilted on: subscribe to that type.

## Related

- References: [rtos-tasks.md](references/rtos-tasks.md),
  [firmware-skeleton.md](references/firmware-skeleton.md),
  [reconnect-timesync.md](references/reconnect-timesync.md),
  [build-paths.md](references/build-paths.md), [agent.md](references/agent.md),
  [memory-qos.md](references/memory-qos.md).
- Skills: [fw-mcu](../fw-mcu/SKILL.md), [fw-serial-can](../fw-serial-can/SKILL.md),
  [ros2-core](../ros2-core/SKILL.md) (QoS, executors), [ros2-control](../ros2-control/SKILL.md),
  [ops-bringup](../ops-bringup/SKILL.md) (udev, systemd, clock sync),
  [ops-docker-ci](../ops-docker-ci/SKILL.md), [arch-safety](../arch-safety/SKILL.md). Later:
  `fw-peripherals`, `fw-drivers`, `fw-motor-control`, `control-systems`.
- Wiki: [micro-ROS](../../wiki/software/micro-ros.md), [FreeRTOS](../../wiki/software/freertos.md),
  [Zephyr](../../wiki/software/zephyr.md), [ESP-IDF](../../wiki/software/esp-idf.md),
  [Arduino](../../wiki/software/arduino.md), [PlatformIO](../../wiki/tools/platformio.md),
  [Fast DDS](../../wiki/software/fast-dds.md), [ROS 2](../../wiki/tools/ros2.md),
  [Docker](../../wiki/tools/docker.md); boards: [ESP32-S3](../../wiki/parts/mcu/espressif-esp32-s3.md),
  [RP2040](../../wiki/parts/mcu/raspberry-pi-rp2040.md), [Teensy 4.1](../../wiki/parts/mcu/pjrc-teensy-4-1.md),
  [Nucleo-F446RE](../../wiki/parts/mcu/st-nucleo-f446re.md), [OpenCR](../../wiki/parts/mcu/robotis-opencr.md),
  [Arduino Mega 2560](../../wiki/parts/mcu/arduino-mega-2560.md) (no micro-ROS);
  [choose a ROS 2 middleware](../../wiki/guides/choose-a-ros2-middleware.md).
- Upstream: micro.vulcanexus.org (micro-ROS docs: rcl/rclc tutorials, middleware configuration,
  QoS, utilities); the `micro-ROS/*` repos on `jazzy` and `ros2/rclc` `jazzy`; FreeRTOS-Kernel
  headers and freertos.org; the ESP-IDF FreeRTOS (IDF) guide; the Zephyr kernel docs.
