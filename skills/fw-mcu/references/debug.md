# Debugging: probes, GDB, faults and reset causes

Part of [fw-mcu](../SKILL.md). Checked on 2026-11-27 against OpenOCD 0.12.0's configuration files,
the probe-rs 0.32 command sources, the ESP-IDF 6.1 `idf.py` sources and Kconfig, the STM32F4 HAL
1.8.6, the Pico SDK 2.3.1, Zephyr 4.5's `hwinfo.h` and the avr-libc watchdog page. Not run.

**Safety first.** A halted CPU does not stop the timers: PWM keeps its last duty while you sit at a
breakpoint or single-step. Debug with motor power off or the wheels off the ground, and keep the
hardware watchdog paused while halted (`__HAL_DBGMCU_FREEZE_IWDG()` on STM32, `pause_on_debug` in
`watchdog_enable` on the Pico, `WDT_OPT_PAUSE_HALTED_BY_DBG` on Zephyr) so a breakpoint does not
read as a hang.

## Wiring

| Link | Pins | Probes |
|---|---|---|
| SWD (Cortex-M: STM32, RP2040/RP2350, nRF; Teensy 4.x exposes none) | SWDIO, SWCLK, GND, plus NRST and the target's VTref | ST-LINK (on Nucleo boards), Raspberry Pi Debug Probe (CMSIS-DAP), J-Link |
| JTAG over USB (ESP32-S3, ESP32-C3/C6 built-in) | The chip's own USB D+/D- | None: the USB-Serial-JTAG unit is the probe |
| JTAG (classic ESP32) | TMS, TCK, TDI, TDO, GND | ESP-Prog, FT2232H boards |

Share ground between the probe, the board and the motor driver logic; a probe on a board powered
from a different supply with no common ground fails to connect or damages pins.

## GDB from the shell (Cortex-M)

Ubuntu's `gcc-arm-none-eabi` has no GDB; install `gdb-multiarch` or use the `arm-none-eabi-gdb`
in STM32CubeCLT or Arm's toolchain. Run GDB in batch mode so it exits:

```bash
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg >/tmp/openocd.log 2>&1 &   # GDB server on :3333
gdb-multiarch -batch build/Debug/my_robot_firmware.elf \
  -ex "target extended-remote :3333" -ex "monitor reset halt" \
  -ex "break main" -ex "continue" -ex "bt" -ex "info registers pc sp"
kill %1
```

probe-rs offers the same without OpenOCD:

```bash
probe-rs gdb --chip STM32F446RETx &           # GDB server on localhost:1337
timeout 20 probe-rs run --chip STM32F446RETx build/Debug/my_robot_firmware.elf   # flash, run, stream RTT
```

`probe-rs run` catches hard faults and resets by default and prints a stack trace when one
happens; `timeout` ends the session. `probe-rs list` shows the connected probes; select one with
`--probe VID:PID:Serial` when there are several.

For one-off reads without GDB: `openocd ... -c "init; halt; mdw 0xE000ED28 1; resume; exit"` reads
the Configurable Fault Status Register; `arm-none-eabi-addr2line -pfiC -e fw.elf 0x08001234` turns
a saved PC into a source line.

## ESP32 (ESP-IDF)

```bash
idf.py -p /dev/my_robot_mcu openocd &       # uses the built-in USB-JTAG on ESP32-S3
idf.py gdb                                    # GDB attached through that OpenOCD
```

- **Panics** print a register dump and backtrace on the console, then reboot
  (`CONFIG_ESP_SYSTEM_PANIC_PRINT_REBOOT`, the default). Decode a captured backtrace with the
  toolchain's `addr2line`, whose path CMake records:
  `$(grep -oP 'CMAKE_ADDR2LINE:FILEPATH=\K.*' build/CMakeCache.txt) -pfiaC -e build/my_robot_firmware.elf 0x...`.
- **Core dumps:** `CONFIG_ESP_COREDUMP_ENABLE_TO_FLASH=y` plus a `coredump` partition saves the
  crash; read it later with `idf.py coredump-info`, even from a board in the field.
- **Watchdogs:** the interrupt watchdog (`CONFIG_ESP_INT_WDT`, on by default) catches an ISR or
  critical section that never ends; the task watchdog only warns unless
  `CONFIG_ESP_TASK_WDT_PANIC=y` ([esp-idf.md](esp-idf.md)).
- `CONFIG_ESP_SYSTEM_PANIC_GDBSTUB` halts in a GDB stub on the console port instead of rebooting:
  useful on the bench, wrong on a robot.

## Cortex-M hard fault handler

Peripherals keep running after a fault, so the handler's first job is to make the outputs safe,
then keep a record and reset. `board_outputs_off()` must use direct register writes (GPIO BSRR,
timer output enable), not HAL calls that may depend on the broken state.

```c
// fault.c - Cortex-M3/M4/M7 (STM32F4, F7, H7, G4, Teensy 4.x)
#include <stdint.h>
#include "board.h"     // board_outputs_off(); CMSIS device header for SCB

#define FAULT_MAGIC 0x46415554u   // "FAUT"

typedef struct {
    uint32_t magic, pc, lr, cfsr, hfsr, mmfar, bfar;
} fault_record_t;

// Survives a reset, not a power cycle. Needs a NOLOAD .noinit section in RAM in the linker script.
__attribute__((section(".noinit"))) volatile fault_record_t g_fault;

__attribute__((used)) void hard_fault_report(const uint32_t *frame)
{
    board_outputs_off();
    g_fault.pc = frame[6];          // stacked r0, r1, r2, r3, r12, lr, pc, xpsr
    g_fault.lr = frame[5];
    g_fault.cfsr = SCB->CFSR;
    g_fault.hfsr = SCB->HFSR;
    g_fault.mmfar = SCB->MMFAR;
    g_fault.bfar = SCB->BFAR;
    g_fault.magic = FAULT_MAGIC;
    NVIC_SystemReset();
}

__attribute__((naked)) void HardFault_Handler(void)
{
    __asm volatile(
        "tst lr, #4            \n"   // which stack was in use
        "ite eq                \n"
        "mrseq r0, msp         \n"
        "mrsne r0, psp         \n"
        "b hard_fault_report   \n");
}
```

At boot, if `g_fault.magic == FAULT_MAGIC`, report the record once over the link and clear the
magic. Cortex-M0/M0+ (RP2040, STM32G0, STM32C0) has no `ite` or CFSR: branch with `movs`/`tst`/`bne`
instead and record only PC and LR. Where the framework has its own handler (ESP-IDF, Zephyr's
fatal error hook `k_sys_fatal_error_handler`), override that instead of the vector. Other
sections for data that survives a reset: Pico SDK `__uninitialized_ram(name)`, ESP-IDF
`__NOINIT_ATTR` (or `RTC_NOINIT_ATTR` where supported), Zephyr `__noinit`.

Read CFSR as three fields: MemManage (bits 0-7), BusFault (8-15), UsageFault (16-31). Common
robot causes: a NULL handle from a skipped init (bus fault at a low address), an unaligned or
out-of-range DMA buffer, a stack overflow into another variable, an uninitialised function pointer
(`INVSTATE`), integer divide by zero when `DIV_0_TRP` is set.

## Reset cause at boot

Report it in the first message after boot; a watchdog or brownout reset on a robot is an event
worth logging on the computer side.

| Platform | Read | Then |
|---|---|---|
| STM32 HAL | `__HAL_RCC_GET_FLAG(RCC_FLAG_IWDGRST)`, `RCC_FLAG_PORRST`, `RCC_FLAG_PINRST`, `RCC_FLAG_SFTRST`, `RCC_FLAG_BORRST` | `__HAL_RCC_CLEAR_RESET_FLAGS()` |
| ESP-IDF | `esp_reset_reason()`: `ESP_RST_POWERON`, `ESP_RST_PANIC`, `ESP_RST_INT_WDT`, `ESP_RST_TASK_WDT`, `ESP_RST_WDT`, `ESP_RST_BROWNOUT` | Nothing to clear |
| Pico SDK | `watchdog_enable_caused_reboot()` (a timeout of the watchdog you armed), `watchdog_caused_reboot()` (any watchdog reboot, including UF2 loads) | Nothing to clear |
| Zephyr | `hwinfo_get_reset_cause(&cause)`: `RESET_POR`, `RESET_PIN`, `RESET_WATCHDOG`, `RESET_BROWNOUT`, `RESET_SOFTWARE` | `hwinfo_clear_reset_cause()` |
| AVR (Mega 2560) | `MCUSR` saved by a function in `.init3` (avr-libc's documented pattern) | Clear `MCUSR`, then `wdt_disable()` early |

On STM32 F4 a power-on sets both the POR and BOR flags; check the watchdog flag first.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| Debugger connects once, then never again | Firmware reuses SWD pins or sleeps | Connect under reset; keep SWD pins free; no sleep in debug builds |
| Board resets every time you stop at a breakpoint | Watchdog keeps counting while halted | Freeze it in debug (table above) |
| Backtrace shows only `HardFault_Handler` | Handler is not `naked`, or the frame pointer is lost | The handler above; build with `-g` and `-Og` for debug |
| `.noinit` record is zero or garbage after reset | Section missing from the linker script, so it is zeroed or placed in flash | Add a NOLOAD `.noinit` output section in RAM; check the map file |
| ESP32 backtrace addresses decode to nothing | ELF does not match the flashed build | Decode with the ELF of the same build ID |
| `gdb`: `Remote 'g' packet reply is too long` | GDB for the wrong architecture | `gdb-multiarch` or the target's own GDB |
