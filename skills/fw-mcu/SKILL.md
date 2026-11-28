---
name: fw-mcu
description: Build, flash and debug robot MCU firmware from the shell (ESP32-S3, STM32 Nucleo, RP2040/RP2350, Arduino Mega, Teensy 4.1) with PlatformIO, arduino-cli,
  ESP-IDF idf.py, STM32CubeMX + CMake, the Pico SDK, Zephyr west, esptool, picotool, OpenOCD, probe-rs and SWD; clocks, GPIO, interrupts, timers, PWM, DMA,
  watchdogs, superloop or RTOS, a command timeout that stops the motors, a stable /dev name. Use when starting, fixing or reviewing a motor or sensor board's firmware.
license: Apache-2.0
metadata:
  sources: []
  evidence: researched
  last_verified: 2026-11-27
---

# MCU firmware

Lets an agent pick a board and toolchain for a robot's low-level board, build, flash and debug it
without a GUI, and give it the structure and watchdogs that keep the motors safe. Checked on
2026-11-27 against ESP-IDF 6.1.1 (5.5 noted), Arduino-ESP32 4.0.0 and 3.3, PlatformIO Core 6.2,
arduino-cli 1.6, Pico SDK and picotool 2.3.1, Zephyr 4.5, esptool 5.7, OpenOCD 0.12.0, probe-rs
0.32 and the STM32F4 HAL 1.8.6; the recipes were researched, not run.

## When to use

- Choosing the MCU board and toolchain for motors, encoders and sensors behind a ROS 2 computer.
- Setting up a firmware project an agent can build, flash, read and debug from a shell.
- Writing or reviewing clock, GPIO, interrupt, timer/PWM, DMA or watchdog code (STM32 HAL,
  ESP-IDF drivers, Pico SDK, Arduino).
- Porting ESP-IDF 4.x or 5.x code (legacy `driver/*.h`) or Arduino-ESP32 2.x code that no longer
  compiles.
- The robot keeps moving when the computer, cable or driver node dies; the board resets or hangs.

Elsewhere: RTOS tasks, queues and micro-ROS in [fw-rtos-micro-ros](../fw-rtos-micro-ros/SKILL.md);
UART/RS-485 framing, pyserial and CAN in [fw-serial-can](../fw-serial-can/SKILL.md); the ROS 2 side
of the board in [ros2-control](../ros2-control/SKILL.md); udev and systemd in
[ops-bringup](../ops-bringup/SKILL.md); the stop chain above the firmware in
[arch-safety](../arch-safety/SKILL.md). I2C, SPI and sensor drivers (`fw-peripherals`,
`fw-drivers`), motor control, FOC and encoders (`fw-motor-control`) and PID (`control-systems`)
come in later batches.

## Quick start

An ESP32-S3 board with PlatformIO, on the robot computer or a laptop (Ubuntu 24.04):

```bash
pipx install platformio      # or PlatformIO's get-platformio.py installer; system pip is blocked (PEP 668)
curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core/develop/platformio/assets/system/99-platformio-udev.rules \
  | sudo tee /etc/udev/rules.d/99-platformio-udev.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
sudo usermod -aG dialout,plugdev "$USER"           # log in again
cd my_robot_firmware                                # platformio.ini: references/build-flash.md
pio run -e esp32s3                                  # build; prints RAM and flash use
pio run -e esp32s3 -t upload --upload-port /dev/serial/by-id/usb-Espressif*   # motor power off
stty -F /dev/serial/by-id/usb-Espressif* 115200 raw -echo
timeout 5 cat /dev/serial/by-id/usb-Espressif* | grep -m1 'build='   # the new build ID
```

The same loop for arduino-cli, `idf.py`, STM32 CMake, the Pico SDK and `west`:
[references/build-flash.md](references/build-flash.md).

## Workflow

1. **Choose the board and toolchain.** Pick by the jobs (PWM channels, encoder counters, CAN, ADC,
   USB, Wi-Fi) and the stack you will run; the comparison is in
   [choose an MCU and firmware stack](../../wiki/guides/choose-an-mcu-and-firmware-stack.md).

   | Board | Toolchain | Flash | Debug |
   |---|---|---|---|
   | [ESP32-S3](../../wiki/parts/mcu/espressif-esp32-s3.md) | [ESP-IDF](../../wiki/software/esp-idf.md) 6.1, or Arduino-ESP32 | `idf.py flash` (esptool) over USB | Built-in USB-JTAG: `idf.py openocd` + `idf.py gdb` |
   | [STM32 Nucleo](../../wiki/parts/mcu/st-nucleo-f446re.md) | STM32CubeMX → CMake + GCC, or Zephyr | ST-LINK: `STM32_Programmer_CLI`, OpenOCD, probe-rs | On-board ST-LINK (SWD) |
   | [RP2040 / RP2350](../../wiki/parts/mcu/raspberry-pi-rp2040.md) | Pico SDK (CMake) | `picotool load -x`, or UF2 copy | Debug Probe (CMSIS-DAP) + OpenOCD or probe-rs |
   | [Arduino Mega 2560](../../wiki/parts/mcu/arduino-mega-2560.md) | arduino-cli or PlatformIO | `arduino-cli upload` (avrdude) | Serial prints (no on-board probe) |
   | [Teensy 4.1](../../wiki/parts/mcu/pjrc-teensy-4-1.md) | Teensyduino via arduino-cli or PlatformIO | `teensy_loader_cli` | Serial prints (no debug port exposed) |

   Nordic nRF52/nRF53/nRF54: use the nRF Connect SDK (Zephyr, the `west` loop below); the nRF5 SDK
   is in maintenance mode. Licences: the STM32 HAL and Pico SDK are BSD-3-Clause, ESP-IDF and
   Zephyr Apache-2.0, but the Arduino cores for AVR and ESP32 are LGPL-2.1 (shipping a binary
   carries LGPL relinking duties) and STM32CubeMX, CubeProgrammer and CubeCLT are under ST's
   SLA0048 licence.
   *Check:* a blink built from the shell for the chosen board, flashed, with the LED blinking.

2. **Lay out the project.** One repository folder `my_robot_firmware/` in the robot's project:
   `board.*` (pins, clocks, the only file that names HAL handles), `link.*` (the host protocol,
   [fw-serial-can](../fw-serial-can/SKILL.md)), `control.*`, `safety.*` (the command watchdog),
   `main.*`, host unit tests in `test/`. Pin every version: the PlatformIO `platform`, the
   ESP-IDF release and `dependencies.lock`, the Pico SDK tag, the Zephyr manifest revision; commit
   `sdkconfig.defaults`, not `sdkconfig`. Embed the git describe output as a build ID.
   *Check:* a fresh clone builds with one documented command, and the board reports that build ID.

3. **Build, flash and read output from the shell.** Agents cannot drive `idf.py monitor` or
   `pio device monitor`; capture with `timeout` instead, and make the firmware print its build ID,
   reset cause and a status line on request or once a second in debug builds. Motor power stays
   off while flashing: pins float through reset and the bootloader.
   [references/build-flash.md](references/build-flash.md).
   *Check:* the flasher exits 0 and the captured output shows the new build ID.

4. **Connect a debug probe.** SWD (Cortex-M, RP2040) or JTAG (ESP32 built-in) with OpenOCD,
   probe-rs or `STM32_Programmer_CLI`; GDB in batch mode for a backtrace; a fault handler that
   saves the fault and stops the motors. Never halt or single-step with motor power on: timers
   keep driving PWM while the CPU is stopped. [references/debug.md](references/debug.md).
   *Check:* `gdb -batch` prints `main`'s backtrace after a halt, and a forced fault leaves its
   record for the next boot.

5. **Set clocks and pins.** Generate the clock tree (STM32CubeMX, `menuconfig`, the SDK default),
   then confirm it at run time; keep every pin in one header; give each motor-driver enable pin an
   external pull resistor to the off state and avoid boot-strapping pins for it.
   STM32: [references/stm32-hal.md](references/stm32-hal.md); ESP32:
   [references/esp-idf.md](references/esp-idf.md); RP2040: [references/pico-sdk.md](references/pico-sdk.md).
   *Check:* the printed core and bus clocks match the plan; a scope or logic analyser shows the
   PWM frequency and duty you set; driver enables stay off from power-on until the firmware enables them.

6. **Interrupts, timers and DMA.** One hardware timer sets the control tick; ISRs only latch data
   (a flag, a timestamp, a ring-buffer index) and return; DMA moves ADC and UART data, with a
   half/full or idle-line callback; shared data is `volatile` and read with interrupts briefly off
   or through a single-producer ring. Rate examples (a 1 kHz tick) are choices to measure, not rules.
   *Check:* a GPIO toggled in the tick shows steady period and jitter on a scope, with no tick
   overrun counted after a minute at full load.

7. **Pick the structure.** A superloop with a timer tick suits one control loop plus a serial link;
   an RTOS (FreeRTOS on ESP-IDF, Zephyr) suits Wi-Fi, micro-ROS or several rates. Either way one
   place owns the motor outputs and the safety state.
   Tasks and priorities: [fw-rtos-micro-ros](../fw-rtos-micro-ros/SKILL.md).
   *Check:* a written list of what runs where and at what rate, matching the code.

8. **Stop the motors when the computer goes quiet.** A command timeout in the control tick sets
   outputs to the safe state when no valid command arrived in time; the hardware watchdog is fed
   from the main loop only after the tick and the checks ran; boot starts with drives disabled
   and reports the reset cause. Skeleton, per-platform watchdog calls and the test:
   [references/command-watchdog.md](references/command-watchdog.md).
   *Check:* with wheels off the ground, killing the driver node or pulling the cable stops the
   motors within the timeout; a hung main loop resets the board and the motors stay off.

9. **Give the board a stable name on the computer.** Use `/dev/serial/by-id/...` or a udev link
   such as `/dev/my_robot_mcu`, matched on the USB serial number; native USB on the MCU (Pico SDK
   uses the flash unique ID) or an FTDI or ST-LINK bridge gives a unique one, cheap CH340 bridges
   give none. Keep ModemManager off the port. Rules and tests:
   [ops-bringup udev](../ops-bringup/references/udev.md).
   *Check:* after replugging and one reboot `ls -l /dev/my_robot_mcu` points at the board, and the
   driver node opens it as the robot user.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| Motors keep turning after the ROS node or cable dies | No firmware command timeout, or it is fed by any byte | Timeout on valid, checksummed commands in the control tick |
| Watchdog never resets a hung board | Fed from a timer ISR, which keeps running when the main loop hangs | Feed only from the main loop after the tick and checks |
| ESP32 task watchdog prints a warning, board keeps running | `CONFIG_ESP_TASK_WDT_PANIC` defaults to `n` | Set it, or `trigger_panic = true` via `esp_task_wdt_reconfigure` |
| Motors twitch at power-on or during flashing | Enable pins float in reset or are boot-strapping pins | External pull to off; move enables off strapping pins |
| Motor runs away while stopped at a breakpoint | Timers keep PWM going while the CPU is halted | Motor power off when debugging; fault handler kills outputs |
| Board resets each time the host opens the port | Arduino AVR auto-reset on DTR; ESP32 bridge boards wire DTR/RTS to EN and IO0 | Host waits for the banner; line handling in [fw-serial-can](../fw-serial-can/SKILL.md) |
| `fatal error: driver/adc.h` (or `timer.h`, `pcnt.h`, `mcpwm.h`, `rmt.h`) | Legacy ESP-IDF drivers removed in 6.0 | New driver headers: [esp-idf.md](references/esp-idf.md) |
| `ledcSetup` not declared; full duty one step short | Arduino-ESP32 3.0 API; 4.0 duty range `0..2^res` | `ledcAttach(pin, freq, res)`; full on is `1 << res` in 4.0 |
| PlatformIO builds Arduino-ESP32 2.0.17 | `espressif32` platform before 8.0.0 | `platform = espressif32 @ 8.0.0` (Arduino-ESP32 3.3) |
| STM32 hangs in `SystemClock_Config` on a Nucleo-64 | No HSE crystal; the ST-LINK feeds 8 MHz on MCO | `RCC_HSE_BYPASS`, or HSI |
| PWM or timer runs at twice the expected rate | STM32 timer clock is 2x PCLK when the APB prescaler is not 1 | Compute from the timer clock in CubeMX's clock tree |
| `HAL_GPIO_EXTI_Callback` never called on G0/U5/H5 | Those HALs split it into Rising and Falling callbacks | Implement `HAL_GPIO_EXTI_Rising_Callback`/`_Falling_` |
| G4/L4/H7 IWDG resets right after a refresh | `Init.Window` left 0 | `Init.Window = IWDG_WINDOW_DISABLE` |
| DMA data stale or corrupt on F7/H7 | D-cache, or buffer in DTCM, which H7 DMA cannot reach | Non-cacheable region or cache clean/invalidate; buffer in AXI or SRAM |
| ISR misses edges, control tick jitters | Long work or printing inside an ISR | Latch and return; work in the loop |
| Random crashes after adding code | Stack overflow | `-fstack-usage` and the map file; RTOS high-water mark |
| `/dev/ttyACM0` becomes `ttyACM1` | Re-enumeration after a reset or hub glitch | udev link on the USB serial number |
| Custom bootloader bricks boards | Hand-written jump and vector code | ROM bootloaders (STM32 system memory, ESP32 ROM, RP2040 BOOTSEL) or MCUboot |

## Checks

Before reporting the firmware done:

- A clean clone builds with the documented command; versions pinned; build ID reported by the board.
- Flash and capture run from the shell and exit 0; `-Wall` builds without new warnings.
- Clocks, PWM frequency and control-tick period measured, numbers recorded.
- Command-timeout test passed for each path (node killed, cable pulled, host frozen), with stop
  times; hung-loop test resets the board and the motors stay off; reset cause reported.
- Drive enables stay off through power-on, reset, flashing and a fault.
- `/dev/my_robot_mcu` (or the by-id path) survives replug and reboot.
- Licences of linked libraries and vendor tools noted in the project's README.

## Distro differences

The firmware does not depend on the ROS distro; only host tools differ. **Lyrical** (Ubuntu 26.04)
ships Python 3.14; ESP-IDF needs 3.10 or newer, but Zephyr's guide recommends 3.12 and warns newer
versions may fail, so make a 3.12 venv with uv if `west packages pip --install` breaks. **Humble**
(Ubuntu 22.04): Zephyr's guide covers Ubuntu 24.04 and later (CMake 3.28 and Python 3.12
minimum; 22.04 ships older ones), so install newer ones or build in a 24.04 container
([ops-docker-ci](../ops-docker-ci/SKILL.md)).

## Related

- References: [build-flash.md](references/build-flash.md), [debug.md](references/debug.md),
  [stm32-hal.md](references/stm32-hal.md), [esp-idf.md](references/esp-idf.md),
  [pico-sdk.md](references/pico-sdk.md), [command-watchdog.md](references/command-watchdog.md).
- Skills: [fw-rtos-micro-ros](../fw-rtos-micro-ros/SKILL.md), [fw-serial-can](../fw-serial-can/SKILL.md),
  [ros2-control](../ros2-control/SKILL.md), [ops-bringup](../ops-bringup/SKILL.md),
  [arch-safety](../arch-safety/SKILL.md), [ops-docker-ci](../ops-docker-ci/SKILL.md),
  [ros2-core](../ros2-core/SKILL.md).
- Wiki: [choose an MCU and firmware stack](../../wiki/guides/choose-an-mcu-and-firmware-stack.md),
  [ESP-IDF](../../wiki/software/esp-idf.md), [Arduino](../../wiki/software/arduino.md),
  [Zephyr](../../wiki/software/zephyr.md), [FreeRTOS](../../wiki/software/freertos.md),
  [micro-ROS](../../wiki/software/micro-ros.md), [PlatformIO](../../wiki/tools/platformio.md);
  parts: [ESP32-S3](../../wiki/parts/mcu/espressif-esp32-s3.md),
  [Nucleo-F446RE](../../wiki/parts/mcu/st-nucleo-f446re.md),
  [RP2040](../../wiki/parts/mcu/raspberry-pi-rp2040.md),
  [Arduino Mega 2560](../../wiki/parts/mcu/arduino-mega-2560.md),
  [Teensy 4.1](../../wiki/parts/mcu/pjrc-teensy-4-1.md), [OpenCR](../../wiki/parts/mcu/robotis-opencr.md).
- Upstream: ESP-IDF docs and migration guides (5.x, 6.x); Arduino-ESP32 migration guides
  (2.x→3.0, 3.x→4.0); PlatformIO docs; arduino-cli docs; Raspberry Pi `pico-sdk` and `picotool`;
  Zephyr getting started and `scripts/west_commands/runners`; esptool docs; probe-rs; OpenOCD;
  STMicroelectronics `stm32f4xx-hal-driver` and the board's reference manual and user manual.
