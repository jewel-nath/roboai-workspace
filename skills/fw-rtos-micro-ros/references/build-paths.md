# Building micro-ROS into the firmware

Part of [fw-rtos-micro-ros](../SKILL.md). Checked on 2026-11-27 against the READMEs and build files of
`micro-ROS/micro_ros_platformio` (`main`, 2.0.0), `micro_ros_arduino`, `micro_ros_espidf_component`,
`micro_ros_stm32cubemx_utils`, `micro_ros_zephyr_module`, `micro_ros_raspberrypi_pico_sdk` and
`micro_ros_setup` (all `jazzy`), and `micro-ROS/freertos_apps` `jazzy`. The recipes were not run.
Flashing and debugging are in [fw-mcu](../../fw-mcu/SKILL.md).

## Pick a path

| Board | Path | Transports | Notes |
|---|---|---|---|
| Teensy 4.1, 4.0 | micro_ros_platformio (`teensy41`, `teensy40`) or micro_ros_arduino | serial; `native_ethernet` on 4.1 | Teensy cores need a `platform.txt` patch for micro_ros_arduino |
| ESP32 (classic) | micro_ros_platformio (`esp32dev`) or the ESP-IDF component | serial, `wifi`, `ethernet` (community) | |
| ESP32-S2, S3, C3, C6, P4 | ESP-IDF component | UDP over Wi-Fi or Ethernet; UART or USB-CDC as custom transports | not in micro_ros_platformio's board list |
| Raspberry Pi Pico, Pico 2 | micro_ros_platformio (`pico`, `pico2`) or micro_ros_raspberrypi_pico_sdk | USB serial; UART | PlatformIO needs the community `maxgerhardt/platform-raspberrypi` platform |
| STM32 Nucleo and custom STM32 | micro_ros_stm32cubemx_utils (CubeMX Makefile or CubeIDE) | UART with DMA or interrupts, USB CDC, UDP with LwIP | see the `micro_ros_setup` note below |
| Zephyr boards | micro_ros_zephyr_module | serial, USB CDC, UDP | tested on Zephyr 4.0 and 4.1 |
| Portenta H7, OpenCR, Due, Zero | micro_ros_platformio or micro_ros_arduino | serial (Portenta also Wi-Fi) | Due and Zero use the very-low-memory meta |
| AVR (Uno, Mega 2560) | none | — | no micro-ROS path supports AVR; use a serial protocol to the computer ([fw-serial-can](../../fw-serial-can/SKILL.md)) |
| Linux PC | `micro_ros_setup` `host` | UDP | test firmware logic with no board |

`micro_ros_setup` itself recommends the per-platform components above. On `jazzy`, its FreeRTOS
targets come from `freertos_apps` `jazzy` (last commit 2025-09-16): `esp32`, `crazyflie21`, the
Nucleo F446RE, F446ZE, F746ZG and F767ZI, and the Olimex STM32-E407, the same boards as `humble`.

## micro_ros_platformio

```ini
; platformio.ini
[env:teensy41]
platform = teensy
board = teensy41
framework = arduino
board_microros_distro = jazzy              ; the default is kilted: always set it
board_microros_transport = serial          ; serial | wifi | wifi_nina | native_ethernet | ethernet | custom
board_microros_user_meta = my_robot.meta   ; memory limits (memory-qos.md); path from the project folder
lib_deps =
    https://github.com/micro-ROS/micro_ros_platformio#<commit>   ; pin a commit for repeatable builds
```

Pico: `platform = https://github.com/maxgerhardt/platform-raspberrypi.git`, `board = rpipico`,
`board_build.core = earlephilhower`, and a user meta that sets `-DRCUTILS_NO_64_ATOMIC=OFF` under
`rcutils` (the project's CI uses this for `pico`, `pico2` and `nanorp2040connect`).

```bash
sudo apt install -y git cmake python3-pip    # PlatformIO Core 6.1.0 or later is required
pio run                                      # first build compiles micro-ROS: several minutes
pio run -t upload
pio run -t clean_microros                    # after changing the distro, the meta or extra packages
```

- The library build sources a Python venv with `.` and runs `colcon`, so build on Linux, macOS or
  WSL.
- Code: `#include <micro_ros_platformio.h>`; serial is `Serial.begin(115200);
  set_microros_serial_transports(Serial);`; Wi-Fi is `IPAddress agent_ip(...);
  set_microros_wifi_transports(ssid, psk, agent_ip, 8888);` (blocks until Wi-Fi joins).
  `MICRO_ROS_TRANSPORT_ARDUINO_SERIAL` and similar macros are defined for `#if` checks.
- Custom messages: package folders in `extra_packages/`, or repos in
  `extra_packages/extra_packages.repos`, then `clean_microros`.
- Licences: micro-ROS is Apache-2.0. The Arduino cores linked into the firmware are LGPL-2.1 for
  ESP32 (`arduino-esp32`) and the Pico (`arduino-pico`): shipping that firmware brings LGPL duties
  (let users relink against a changed core). The Teensy core uses a permissive MIT-style licence.
  The ESP32 Wi-Fi driver is shipped as binary-only libraries (Apache-2.0, no source).

### Wiring the skeleton

[firmware-skeleton.md](firmware-skeleton.md) on Arduino-ESP32 (`esp32dev`), all in C++ files so no
`extern "C"` is needed:

```cpp
// src/main.cpp; the skeleton sits in src/firmware.cpp and declares firmware_start() in firmware.h
#include <Arduino.h>
#include <micro_ros_platformio.h>
#include "firmware.h"

void board_transport_init(void)
{
    Serial.begin(115200);                  /* must match the agent's -b */
    set_microros_serial_transports(Serial);
}

void setup() { firmware_start(); }
void loop()  { vTaskDelay(portMAX_DELAY); }   /* all work happens in the two tasks */
```

- `Serial` now belongs to micro-ROS: no `Serial.print`; debug on another UART.
- Wi-Fi instead: `set_microros_wifi_transports(ssid, psk, agent_ip, 8888)` loops until Wi-Fi joins.
  Call it at the start of `micro_ros_task` instead of in `board_transport_init`, so the control task
  already runs (and holds the motors stopped) while Wi-Fi is down.

## micro_ros_arduino (Arduino IDE or arduino-cli)

- Download the release built for Jazzy from the repository's releases; Arduino IDE: *Sketch >
  Include Library > Add .ZIP Library*; arduino-cli: `arduino-cli lib install --zip-path <zip>`
  after `arduino-cli config set library.enable_unsafe_install true` (zip installs are off by default).
- Teensy and SAM boards need the `platform.txt` patch from `extras/patching_boards/` to link
  precompiled libraries.
- Code: `#include <micro_ros_arduino.h>`; `set_microros_transports();` for serial;
  `set_microros_wifi_transports("ssid", "pass", "192.0.2.10", 8888);` (here the agent address is a
  string).
- Memory limits or custom messages: edit `extras/library_generation/colcon*.meta`, then rebuild the
  library with `docker run -it --rm -v $(pwd):/project --env MICROROS_LIBRARY_FOLDER=extras
  microros/micro_ros_static_library_builder:jazzy`.
- Its PlatformIO support is deprecated in favour of micro_ros_platformio.

## ESP-IDF component

```bash
. $IDF_PATH/export.sh                         # in a shell WITHOUT /opt/ros/jazzy sourced
pip3 install catkin_pkg colcon-common-extensions lark
idf.py add-dependency "micro-ros/micro_ros_espidf_component^24"   # 24.x.y is the Jazzy line
idf.py set-target esp32s3
idf.py menuconfig                             # micro-ROS Settings: agent IP and port, Wi-Fi, transport
idf.py build flash monitor
idf.py clean-microros                         # after changing app-colcon.meta
```

- Tested with ESP-IDF v5.2 to v6.0 on ESP32, S2, S3, C3, C6 and P4. Or clone the `jazzy` branch into
  `components/`.
- Default transport is UDP; serial or USB-CDC needs `-DRMW_UXRCE_TRANSPORT=custom` and a custom
  transport (examples `int32_publisher_custom_transport` and `..._usbcdc`).
- Memory limits: an `app-colcon.meta` in the project folder is applied after the component's own
  `colcon.meta` (which allows 1 node, 2 publishers, 2 subscriptions, 1 service, 1 client).
- ESP-IDF is Apache-2.0; its Wi-Fi driver comes as binary-only libraries (`esp32-wifi-lib`).

## STM32CubeMX and STM32CubeIDE

1. Clone `micro_ros_stm32cubemx_utils` (`-b jazzy`) into the project; CubeMX project with the
   `Makefile` toolchain (or CubeIDE).
2. FreeRTOS on, micro-ROS task stack above 10 kB; transport configured in CubeMX: UART with DMA
   (TX and RX DMA at very high priority, RX circular, UART global interrupt), UART with
   interrupts, USB CDC, or Ethernet with LwIP (static IP, UDP on).
3. Add to the generated `Makefile`: `libmicroros.a`, its include folder, and
   `extra_sources/custom_memory_manager.c`, `microros_allocators.c`, `microros_time.c` and one
   transport from `extra_sources/microros_transports/`.
4. Build the library: `docker run -it --rm -v $(pwd):/project --env
   MICROROS_LIBRARY_FOLDER=micro_ros_stm32cubemx_utils/microros_static_library
   microros/micro_ros_static_library_builder:jazzy` (it reads the compiler flags from the Makefile
   and asks you to confirm them).
5. Write the task from `sample_main.c`: `rmw_uros_set_custom_transport(true, &huartN, ...)`, then
   `rcutils_set_default_allocator()` with the `microros_*` functions.

Memory limits: `microros_static_library/library_generation/colcon.meta` before step 4.
Licences: STM32CubeMX and STM32CubeIDE are ST tools under ST's own licence terms; the generated HAL
code in the sample is BSD-3-Clause; FreeRTOS is MIT.

## Zephyr module

```bash
pip3 install catkin_pkg lark-parser empy colcon-common-extensions
west build -b <board> -p
west build -t menuconfig     # Modules > micro-ROS support: transport, agent IP and port, entity counts
west flash
```

Kconfig sets the limits directly: `CONFIG_MICROROS_NODES`, `CONFIG_MICROROS_PUBLISHERS`,
`CONFIG_MICROROS_SUBSCRIBERS`, `CONFIG_MICROROS_CLIENTS`, `CONFIG_MICROROS_SERVERS`,
`CONFIG_MICROROS_RMW_HISTORIC`, `CONFIG_MICROROS_XRCE_DDS_MTU` (512) and
`CONFIG_MICROROS_XRCE_DDS_HISTORIC`; transports `CONFIG_MICROROS_TRANSPORT_SERIAL`, `_SERIAL_USB`
or `_UDP`. Zephyr is Apache-2.0.

## micro_ros_setup (agent, host tests, static libraries)

```bash
source /opt/ros/jazzy/setup.bash
mkdir -p ~/uros_ws/src && cd ~/uros_ws
git clone -b jazzy https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup
rosdep update && rosdep install --from-paths src --ignore-src -y
colcon build && source install/local_setup.bash

ros2 run micro_ros_setup create_firmware_ws.sh host         # firmware logic on the PC
ros2 run micro_ros_setup build_firmware.sh
source install/local_setup.bash
ros2 run micro_ros_setup create_agent_ws.sh && ros2 run micro_ros_setup build_agent.sh
source install/local_setup.bash
ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888 &
RMW_IMPLEMENTATION=rmw_microxrcedds ros2 run micro_ros_demos_rclc ping_pong
```

- One firmware workspace per folder: `create_firmware_ws.sh` refuses when `firmware/` exists.
- `configure_firmware.sh <app> -t serial|udp [-d dev] [-i ip] [-p port]`, `build_firmware.sh` and
  `flash_firmware.sh` complete the FreeRTOS `esp32` flow.
- `create_firmware_ws.sh generate_lib` builds a static library and headers for any CMake
  cross-toolchain.
