# Command watchdog: stop the motors when the computer goes quiet

Part of [fw-mcu](../SKILL.md). The firmware timeout is the last layer of the stop chain in
[arch-safety](../../arch-safety/SKILL.md): the only one that still works when Linux, the USB
cable or the ROS driver is dead. Watchdog calls checked on 2026-11-27 against the STM32F4 HAL
1.8.6, ESP-IDF `esp_task_wdt.h`, Pico SDK 2.3.1, Zephyr 4.5 `watchdog.h` and avr-libc; the code
is a skeleton written for this skill, not run. It is not a safety function in the ISO 13849 sense;
the e-stop must still cut motor power in hardware.

## Two watchdogs, two failures

| Failure | Caught by | Reaction |
|---|---|---|
| Computer, cable, driver node or link stops sending valid commands | **Command timeout** in the control tick | Outputs to the safe state, report `timeout`, wait for a fresh enable |
| Firmware hangs (deadlock, endless loop, ISR storm) | **Hardware watchdog**, fed only by a healthy main loop | Chip reset; boot starts with drives off and reports the reset cause |
| Firmware faults | Fault handler ([debug.md](debug.md)) | Outputs off, record, reset |

Both rely on the hardware keeping the drive off while the MCU is in reset or booting: an external
pull resistor on each driver enable (or PWM) line to the off state, and no strapping pins for
those lines.

## Rules

- **Only valid commands count.** Reset the timer on a frame that passed its checksum and sequence
  check ([fw-serial-can](../../fw-serial-can/SKILL.md)), never on any received byte. A heartbeat
  frame from the host counts only if the host sends it from the same loop that computes commands.
- **Check it in the control tick,** not in the receive path: no bytes means no receive event.
- **Unsigned time arithmetic:** `(uint32_t)(now - last) > timeout` survives the `millis()`
  wrap after about 49.7 days.
- **Pick the timeout from the stopping budget,** not by habit: above two or three command periods
  (a host at 50 Hz gives 20 ms periods), below what lets the robot travel too far. 200 ms below
  is an example.
- **Safe state is the driver's off,** decided per drive: zero duty and enable low for brushed
  drives, a velocity of zero then disable for smart drives, a hold or brake where gravity loads a
  joint (an arm must not drop; ask the mechanical design).
- **Resume only on intent.** After a timeout, a new command must carry the enable flag that the
  host sets in `on_activate` ([ros2-control](../../ros2-control/SKILL.md)), so a reconnecting
  host does not restart the motors with a stale target.
- **Feed the hardware watchdog in one place,** the main loop after the control step ran; never in
  a timer ISR, which keeps running when the loop is stuck. Under an RTOS, feed it when every
  monitored task has checked in ([fw-rtos-micro-ros](../../fw-rtos-micro-ros/SKILL.md)).

## Skeleton

```c
// safety.h
#include <stdbool.h>
#include <stdint.h>

typedef enum { SAFETY_DISABLED, SAFETY_ACTIVE, SAFETY_TIMED_OUT, SAFETY_FAULT } safety_state_t;

void safety_init(void);
void safety_on_command(uint32_t now_ms, bool enable);   // called by link.c for each valid frame
void safety_on_fault(uint32_t code);                     // over-current, driver fault pin, e-stop sense
void safety_tick(uint32_t now_ms);                       // called first in every control tick
bool safety_outputs_allowed(void);
safety_state_t safety_state(void);
```

```c
// safety.c - no HAL calls; board.c supplies board_outputs_off()
#include "safety.h"
#include "board.h"

#define CMD_TIMEOUT_MS 200u          // example: set from the stopping budget, then measure

static volatile safety_state_t s_state;
static volatile uint32_t s_last_cmd_ms;
static volatile uint32_t s_fault_code;

void safety_init(void)
{
    board_outputs_off();
    s_state = SAFETY_DISABLED;
}

void safety_on_command(uint32_t now_ms, bool enable)
{
    s_last_cmd_ms = now_ms;
    if (s_state == SAFETY_FAULT) return;                 // only a reset or an explicit clear leaves FAULT
    if (!enable) {
        s_state = SAFETY_DISABLED;
    } else if (s_state != SAFETY_ACTIVE) {
        s_state = SAFETY_ACTIVE;                         // control.c starts from zero, not the old target
    }
}

void safety_on_fault(uint32_t code)
{
    board_outputs_off();
    s_fault_code = code;
    s_state = SAFETY_FAULT;
}

void safety_tick(uint32_t now_ms)
{
    if (s_state == SAFETY_ACTIVE && (uint32_t)(now_ms - s_last_cmd_ms) > CMD_TIMEOUT_MS) {
        s_state = SAFETY_TIMED_OUT;
    }
    if (s_state != SAFETY_ACTIVE) board_outputs_off();   // every tick, not once
}

bool safety_outputs_allowed(void) { return s_state == SAFETY_ACTIVE; }
safety_state_t safety_state(void) { return s_state; }
```

```c
// main.c - superloop with a timer tick
int main(void)
{
    board_init();                    // clocks and pins; driver enables low before anything else
    safety_init();
    report_boot(board_reset_cause(), FW_BUILD_ID);
    link_init();
    control_init();
    tick_start();                    // hardware timer sets g_tick_due
    board_watchdog_start();          // after init, so a slow init does not trip it

    for (;;) {
        link_poll();                 // parse received bytes; valid frames call safety_on_command()
        if (!g_tick_due) continue;
        g_tick_due = false;

        uint32_t now = board_millis();
        safety_tick(now);
        if (safety_outputs_allowed()) {
            control_step();          // reads encoders, computes, writes outputs
        }
        telemetry_send_if_due(now, safety_state(), g_tick_overruns);
        board_watchdog_feed();       // the only feed: reached only when the loop and tick both run
    }
}
```

`control_step()` resets its targets and integrators when the state turns `ACTIVE` again, so it
never resumes the last command from before the timeout. Telemetry carries the safety state, so
the ROS side can report `timeout` and `fault` through diagnostics
([ops-bringup](../../ops-bringup/SKILL.md)).

## Hardware watchdog per platform

| Platform | Start | Feed | Notes |
|---|---|---|---|
| STM32 HAL | `HAL_IWDG_Init()` ([stm32-hal.md](stm32-hal.md)) | `HAL_IWDG_Refresh()` | Cannot be stopped once started; LSI is imprecise; `__HAL_DBGMCU_FREEZE_IWDG()` for debugging |
| ESP-IDF | `esp_task_wdt_reconfigure()` with `trigger_panic = true`, `esp_task_wdt_add(NULL)` ([esp-idf.md](esp-idf.md)) | `esp_task_wdt_reset()` | Default config only warns |
| Arduino-ESP32 | `enableLoopWDT()` plus the reconfigure above | Fed between `loop()` calls | Test that a timeout resets |
| Pico SDK | `watchdog_enable(ms, true)` ([pico-sdk.md](pico-sdk.md)) | `watchdog_update()` | Max 8388 ms on RP2040, 16777 ms on RP2350 |
| Zephyr | `wdt_install_timeout()` with `.window.max`, `.flags = WDT_FLAG_RESET_SOC`; then `wdt_setup(dev, WDT_OPT_PAUSE_HALTED_BY_DBG)` | `wdt_feed(dev, channel)` | Device from the devicetree alias `watchdog0` |
| AVR (Mega 2560) | `wdt_enable(WDTO_250MS)` (`<avr/wdt.h>`) | `wdt_reset()` | After a watchdog reset it stays on at the shortest period: clear `MCUSR` and `wdt_disable()` early (`.init3`), or the board can reset-loop |

## Test before trusting it

Wheels off the ground or the joint unloaded, a person at the power switch, the stop times written
down in the project's test log:

1. **Node killed.** Drive slowly, `pkill -9 -f ros2_control_node` (or the driver node). Motors stop
   within `CMD_TIMEOUT_MS` plus one tick; telemetry, once the node is back, says `timeout`.
2. **Cable pulled.** Same, with the USB or CAN cable unplugged mid-motion.
3. **Host frozen.** `kill -STOP` the node (it holds the port but sends nothing): same result.
4. **Resume.** Restart the node; the motors stay off until the controller is activated again.
5. **Hung loop.** A test-only build command (`HANG`) enters `for (;;) {}` with outputs on; the
   hardware watchdog resets the board, enables stay low through reset and boot (check with a scope
   on the enable pin), and the boot report says `watchdog`.
6. **Fault.** A test-only command dereferences a NULL pointer; outputs go off at once and the
   record appears on the next boot.

Measure each stop time from the moment of the event to zero output on a scope or logic analyser
(an enable pin and a GPIO toggled when the event is injected) rather than by eye.
