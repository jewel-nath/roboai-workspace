---
type: tool
name: FreeRTOS
summary: The small MIT-licensed RTOS kernel that ESP-IDF builds on and STM32 and RP2040 projects add; tasks, queues, mutexes and timers on Cortex-M, ESP32 and RP2040, and the base micro-ROS runs on for STM32 and ESP32.
tags: [freertos, rtos, kernel, firmware, mcu, cortex-m, stm32, esp32, esp-idf, rp2040, smp, micro-ros, aws, lts]
kind: library
area: firmware
support:
license: MIT
links: {repo: "https://github.com/FreeRTOS/FreeRTOS-Kernel", docs: "https://www.freertos.org/Documentation/00-Overview", site: "https://www.freertos.org"}
version: {tested: , latest: "11.3.3", as_of: 2026-11-27}
platforms: [linux, windows, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-27
sources:
  - {url: "https://github.com/FreeRTOS/FreeRTOS-Kernel", title: "FreeRTOS-Kernel repository: README, LICENSE.md, History.txt, template FreeRTOSConfig.h, headers and portable/ThirdParty ports", accessed: 2026-11-27}
  - {url: "https://github.com/FreeRTOS/FreeRTOS-LTS", title: "FreeRTOS-LTS repository: README and CHANGELOG, 202604-LTS and 202406-LTS branches", accessed: 2026-11-27}
  - {url: "https://www.freertos.org/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/04-Licensing", title: "FreeRTOS: License details", accessed: 2026-11-27}
  - {url: "https://www.freertos.org/Why-FreeRTOS/FAQs/Amazon", title: "FreeRTOS FAQ: Amazon", accessed: 2026-11-27}
  - {url: "https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4", title: "FreeRTOS: Running the RTOS on an ARM Cortex-M core", accessed: 2026-11-27}
  - {url: "https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management", title: "FreeRTOS: Heap memory management", accessed: 2026-11-27}
  - {url: "https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking", title: "FreeRTOS: Stack usage and stack overflow checking", accessed: 2026-11-27}
  - {url: "https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes", title: "FreeRTOS: Mutexes", accessed: 2026-11-27}
  - {url: "https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS/Demo/Posix_GCC", title: "FreeRTOS repository: Posix_GCC demo README and Makefile", accessed: 2026-11-27}
  - {url: "https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/freertos.html", title: "ESP-IDF v6.1.1 (ESP32-S3): FreeRTOS overview", accessed: 2026-11-27}
  - {url: "https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/freertos_idf.html", title: "ESP-IDF v6.1.1 (ESP32-S3): FreeRTOS (IDF)", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_setup", title: "micro_ros_setup README and config folder (kilted branch)", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_stm32cubemx_utils", title: "micro-ROS utils for STM32CubeMX and STM32CubeIDE: README and branches", accessed: 2026-11-27}
  - {url: "https://github.com/micro-ROS/micro_ros_espidf_component", title: "micro-ROS component for ESP-IDF: README, examples (jazzy and rolling branches)", accessed: 2026-11-27}
---

# FreeRTOS

FreeRTOS is a small preemptive kernel for microcontrollers: tasks, queues, semaphores, mutexes,
software timers and event groups in a few C files, plus one port per chip and compiler [1]. A
robot builder meets it inside ESP-IDF, in STM32CubeMX projects and under micro-ROS on STM32 and
ESP32 [10][12][13]. The kernel is MIT: shipping it asks you neither to open your application or
your kernel changes nor to document that the product uses it [3]. The RP2040 port is
BSD-3-Clause and some demos bundle libraries under other licences; keep each notice [1][3].

## When to use it

- **Use it** when the SDK brings it (ESP-IDF on an [ESP32-S3](../parts/mcu/espressif-esp32-s3.md),
  CubeMX on a [Nucleo F446RE](../parts/mcu/st-nucleo-f446re.md)) or when you want only a kernel
  around your vendor HAL, build system and drivers [10][13].
- **Use it for micro-ROS** on STM32 or ESP32, where the maintained routes run on it [12][13][14].
- **Use [Zephyr](zephyr.md)** when you want one driver API, board model and build system across
  vendors, and can afford its learning curve. Use [Arduino](arduino.md) or bare metal for a single
  loop with no blocking I/O. Compare them in
  [Choose an MCU and firmware stack](../guides/choose-an-mcu-and-firmware-stack.md).

## Versions and who stands behind it

| Line | Kernel | Fixes until | Source |
|---|---|---|---|
| Current release | V11.3.3, 2026-10-29 | next release | [1] |
| 202604 LTS | 11.3.0, patched to 11.3.1 in 202604.01 | 2028-04-30 | [2] |
| 202406 LTS (the kernel README still names it) | 11.1.0 | ended 2026-06-30 | [1][2] |

- **SMP** reached the mainline in V11.0.0 (2023-12-18): one kernel schedules tasks across identical
  cores that share memory, set by `configNUMBER_OF_CORES` and `configUSE_CORE_AFFINITY`. V11.3.1
  added SMP for Armv8-M ports and `xTaskPeriodicDelay()` [1].
- **What AWS stewardship means in practice.** V10.0.0 was the first release under AWS and under
  MIT [1][4]. You need no AWS account, may use any cloud, and Amazon has not forked it [4]. AWS
  keeps LTS bundles (kernel, TCP, coreMQTT, AWS IoT libraries) fixed for two years and sells an
  Extended Maintenance Plan for up to ten more [2]. Under licence from AWS, WITTENSTEIN sells
  OPENRTOS (same code, with warranty and IP indemnity) and SAFERTOS (safety-certified) [3].
- **Maintenance:** last commit 2026-11-25; 57 open issues on 2026-11-27; help on the forum [1].

## Ports a robot builder meets

| Chip | Port | Supported by | Notes |
|---|---|---|---|
| Cortex-M0/M3/M4F/M7/M33 (STM32, most others) | `portable/GCC/ARM_CM*` | FreeRTOS team | Interrupt rules below [1][5] |
| ESP32, ESP32-S3 | ESP-IDF's own copy | Espressif | Based on V10.5.1 with SMP changes, at most two cores [10][11] |
| RP2040 | `portable/ThirdParty/GCC/RP2040` | FreeRTOS team | SMP, for the Pico SDK; BSD-3-Clause (Raspberry Pi); tickless idle untested [1] |
| RP2350 (Arm, RISC-V) | Community-Supported-Ports submodule | Community | Not reviewed by the FreeRTOS team [1] |

## Setup

There is no installer: the kernel is source you add to a firmware project. Run it on the host
first; the POSIX port needs only gcc and make, on Linux, macOS, or Windows through MSYS2 or WSL [9]:

```bash
sudo apt install -y build-essential gcc gdb make
git clone --depth 1 https://github.com/FreeRTOS/FreeRTOS.git && cd FreeRTOS
git submodule update --init --depth 1 FreeRTOS/Source            # the kernel
cd FreeRTOS/Demo/Posix_GCC && make USER_DEMO=BLINKY_DEMO && ./build/posix_demo
```

- **Your own CMake project:** `FetchContent_Declare` the kernel at a tag (`GIT_TAG V11.3.3`), add a
  `freertos_config` INTERFACE library whose include path holds `FreeRTOSConfig.h`, and set
  `FREERTOS_PORT` (`GCC_ARM_CM4F`, `GCC_RP2040`, `GCC_POSIX`) and `FREERTOS_HEAP` (`4`) [1].
- **STM32:** enable FreeRTOS as CubeMX middleware [13]. **RP2040:** include the port's
  `FreeRTOS_Kernel_import.cmake` [1]. **ESP32:** nothing to add; [ESP-IDF](esp-idf.md) starts the
  scheduler before `app_main` runs [10].

## How an agent works with it

Recipes: [fw-rtos-micro-ros](../../skills/fw-rtos-micro-ros/SKILL.md). Edit `FreeRTOSConfig.h` (on
ESP-IDF, `idf.py menuconfig`), build with the SDK's CLI. Key settings, template values [1]:

| Setting | Template | What it does |
|---|---|---|
| `configTICK_RATE_HZ` | 100 | Tick rate: one tick is 10 ms; convert with `pdMS_TO_TICKS(ms)` |
| `configMAX_PRIORITIES` | 5 | Priorities 0 to N-1; 0 is the lowest |
| `configMINIMAL_STACK_SIZE` | 128 | Idle task stack, in **words** |
| `configCHECK_FOR_STACK_OVERFLOW` | 2 | 1 checks the stack pointer, 2 a fill pattern, 3 the ISR stack on some ports [7] |
| `configTOTAL_HEAP_SIZE` | 4096 | Size of the FreeRTOS heap; pick one `heap_N.c` [6] |
| `configSUPPORT_STATIC_ALLOCATION` | 1 | Lets you create tasks and queues with no heap at all [6] |
| `configMAX_SYSCALL_INTERRUPT_PRIORITY` | 0 (placeholder) | Highest ISR priority that may call `...FromISR()` APIs [5] |
| `configASSERT()` | defined | Catches bad NVIC priorities and arguments; keep it on in development [5] |

**Check the result** over the serial log: print `uxTaskGetStackHighWaterMark(NULL)` per task (set
`INCLUDE_uxTaskGetStackHighWaterMark`), `xPortGetMinimumEverFreeHeapSize()`, and `vTaskListTasks()`
(needs `configUSE_TRACE_FACILITY` and `configUSE_STATS_FORMATTING_FUNCTIONS`) [1][6]. Test task
logic on the POSIX port in CI before flashing [9].

**micro-ROS on FreeRTOS** (details in [micro-ROS](micro-ros.md)):

- `micro_ros_setup` builds for Nucleo F446RE, F446ZE, F746ZG and F767ZI (community), ESP32 and
  [Crazyflie](../robots/crazyflie.md) 2.1, but points to the packages below instead [12].
- **STM32:** give the micro-ROS task more than 10 kB of stack, swap `heap_4.c` for the utils'
  `custom_memory_manager.c`, use UART with DMA or USB CDC; no Lyrical branch yet [13].
- **ESP-IDF:** `idf.py add-dependency "micro-ros/micro_ros_espidf_component^24"` for Jazzy; tested
  on ESP-IDF 5.2 to 6.0 with ESP32, S2, S3, C3, C6 and P4; example task stack 16000 bytes; build
  without ROS 2 sourced; agent from the `microros/micro-ros-agent:jazzy` image [14].

## Traps

- **Stack overflow looks like random crashes.** Each task has its own stack, sized at creation.
  Turn on check 2 with a `vApplicationStackOverflowHook()`, read the high-water marks, then trim
  [7]. Vanilla FreeRTOS sizes stacks in words; ESP-IDF in **bytes**, so a value copied between
  them is off by four [1][11].
- **An ISR calls the API and the system hangs or asserts.** Only `...FromISR()` functions are
  allowed in ISRs, and only from interrupts at or below `configMAX_SYSCALL_INTERRUPT_PRIORITY`.
  On Cortex-M a lower number is a higher priority, and every interrupt defaults to 0, the highest:
  set each one explicitly. The config value sits in the top bits of the 8-bit register (shifted by
  `8 - __NVIC_PRIO_BITS`); some HAL calls take it shifted, others not. With ST's driver library,
  make every bit a preempt bit (`NVIC_PriorityGroup_4`) before the scheduler starts [5]. M0 and
  M0+ have no BASEPRI, so these nesting rules do not apply there [5].
- **Priority inversion.** Guard shared buses with a mutex, not a binary semaphore: only mutexes
  have priority inheritance. Inheritance only shortens the inversion, and mutexes cannot be taken
  in an ISR [8]. On SMP or ESP-IDF a higher priority no longer keeps a lower task off the CPU, and
  `vTaskSuspendAll()` stops only the calling core [11].
- **Heap fragmentation.** heap_1 never frees, heap_2 is legacy and does not merge free blocks,
  heap_3 wraps `malloc()`, heap_4 merges neighbours, heap_5 spans several RAM regions. heap_4 is
  much less likely to fragment but is not deterministic: allocate at boot, prefer static
  creation, and watch the minimum-ever free heap [6].
- **ESP-IDF is not upstream** [10][11]: never call `vTaskStartScheduler()`; `FreeRTOSConfig.h` is
  private, so settings come from menuconfig; `pvPortMalloc()` maps to `heap_caps_malloc()` and
  `heap_N.c` is unused; critical sections take a `portMUX_TYPE` spinlock; a task that uses
  `float` is pinned to its core. Upstream SMP (`CONFIG_FREERTOS_SMP`) is experimental, ESP32 only.

## Alternatives

- [Zephyr](zephyr.md): an RTOS with drivers, devicetree and the west build tool.
- [ESP-IDF](esp-idf.md) (FreeRTOS inside), [Arduino](arduino.md), and
  [PlatformIO](../tools/platformio.md) as a build front end.
- NuttX and ChibiOS, inside [PX4](px4.md) and [ArduPilot](ardupilot.md); Azure RTOS (ThreadX),
  which micro-ROS also supports [12].

## Sources

1. [FreeRTOS-Kernel repository: README, LICENSE.md, History.txt, template FreeRTOSConfig.h, headers and portable/ThirdParty ports](https://github.com/FreeRTOS/FreeRTOS-Kernel), accessed 2026-11-27
2. [FreeRTOS-LTS repository: README and CHANGELOG, 202604-LTS and 202406-LTS branches](https://github.com/FreeRTOS/FreeRTOS-LTS), accessed 2026-11-27
3. [FreeRTOS: License details](https://www.freertos.org/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/04-Licensing), accessed 2026-11-27
4. [FreeRTOS FAQ: Amazon](https://www.freertos.org/Why-FreeRTOS/FAQs/Amazon), accessed 2026-11-27
5. [FreeRTOS: Running the RTOS on an ARM Cortex-M core](https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4), accessed 2026-11-27
6. [FreeRTOS: Heap memory management](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management), accessed 2026-11-27
7. [FreeRTOS: Stack usage and stack overflow checking](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking), accessed 2026-11-27
8. [FreeRTOS: Mutexes](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes), accessed 2026-11-27
9. [FreeRTOS repository: Posix_GCC demo README and Makefile](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS/Demo/Posix_GCC), accessed 2026-11-27
10. [ESP-IDF v6.1.1 (ESP32-S3): FreeRTOS overview](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/freertos.html), accessed 2026-11-27
11. [ESP-IDF v6.1.1 (ESP32-S3): FreeRTOS (IDF)](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/freertos_idf.html), accessed 2026-11-27
12. [micro_ros_setup README and config folder (kilted branch)](https://github.com/micro-ROS/micro_ros_setup), accessed 2026-11-27
13. [micro-ROS utils for STM32CubeMX and STM32CubeIDE: README and branches](https://github.com/micro-ROS/micro_ros_stm32cubemx_utils), accessed 2026-11-27
14. [micro-ROS component for ESP-IDF: README, examples (jazzy and rolling branches)](https://github.com/micro-ROS/micro_ros_espidf_component), accessed 2026-11-27
