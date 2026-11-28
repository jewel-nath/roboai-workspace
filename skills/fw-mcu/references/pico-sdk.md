# Raspberry Pi Pico SDK patterns (RP2040, RP2350)

Part of [fw-mcu](../SKILL.md). Checked on 2026-11-27 against `raspberrypi/pico-sdk` 2.3.1 headers
(`hardware_gpio`, `hardware_pwm`, `hardware_dma`, `hardware_watchdog`, `pico_time`,
`pico_stdio_usb`); not run. The SDK is BSD-3-Clause. Build and flash commands are in
[build-flash.md](build-flash.md).

## Project

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.13)
include(pico_sdk_import.cmake)            # copy of $PICO_SDK_PATH/external/pico_sdk_import.cmake
project(my_robot_firmware C CXX ASM)
pico_sdk_init()

add_executable(my_robot_firmware src/main.c src/board.c src/control.c src/safety.c src/link.c)
target_link_libraries(my_robot_firmware pico_stdlib hardware_pwm hardware_dma hardware_watchdog)
pico_enable_stdio_usb(my_robot_firmware 1)  # USB CDC: VID 2E8A, PID 000A (RP2040) or 0009 (RP2350)
pico_enable_stdio_uart(my_robot_firmware 0)
pico_add_extra_outputs(my_robot_firmware)   # .uf2, .bin, .hex, .map beside the .elf
```

`PICO_BOARD` (`pico`, `pico_w`, `pico2`, `pico2_w`, or your own board header) picks the chip, flash
size and default pins. To pin the SDK, check out a tag (`git -C ~/pico-sdk checkout 2.3.1 && git
submodule update --init`) or set `PICO_SDK_FETCH_FROM_GIT=on` with `PICO_SDK_FETCH_FROM_GIT_TAG=2.3.1`.

The stdio USB descriptor uses the flash's unique ID as the USB serial number, so each Pico gets a
distinct `/dev/serial/by-id/usb-Raspberry_Pi_..._<id>-if00` without extra work.

## GPIO interrupt

```c
static volatile uint32_t g_estop_edges;

static void gpio_cb(uint gpio, uint32_t events)
{
    if (gpio == PIN_ESTOP_SENSE && (events & GPIO_IRQ_EDGE_FALL)) g_estop_edges++;
}

void board_inputs_init(void)
{
    gpio_init(PIN_ESTOP_SENSE);
    gpio_set_dir(PIN_ESTOP_SENSE, GPIO_IN);
    gpio_pull_up(PIN_ESTOP_SENSE);
    gpio_set_irq_enabled_with_callback(PIN_ESTOP_SENSE, GPIO_IRQ_EDGE_FALL, true, &gpio_cb);
}
```

There is one GPIO callback per core: `gpio_set_irq_enabled_with_callback()` replaces it, so
dispatch on `gpio` inside one function, or use `gpio_add_raw_irq_handler()` per pin. A firmware
e-stop input only reports; the e-stop itself cuts motor power in hardware
([arch-safety](../../arch-safety/SKILL.md)).

## PWM

```c
// 20 kHz (example) on a GPIO. Default system clock: 125 MHz on RP2040 (200 MHz with
// PICO_USE_FASTEST_SUPPORTED_CLOCK), 150 MHz on RP2350; read it, do not assume it
void pwm_init_pin(uint pin, uint32_t freq_hz)
{
    gpio_set_function(pin, GPIO_FUNC_PWM);
    uint slice = pwm_gpio_to_slice_num(pin);
    uint32_t wrap = clock_get_hz(clk_sys) / freq_hz - 1u;   // must fit 16 bits; else set a clkdiv
    pwm_set_wrap(slice, (uint16_t)wrap);
    pwm_set_chan_level(slice, pwm_gpio_to_channel(pin), 0); // start at zero duty
    pwm_set_enabled(slice, true);
}

void pwm_set(uint pin, float duty)                          // 0.0 .. 1.0, clamped
{
    if (!(duty > 0.0f)) duty = 0.0f;
    if (duty > 1.0f) duty = 1.0f;
    uint slice = pwm_gpio_to_slice_num(pin);
    uint16_t top = (uint16_t)(pwm_hw->slice[slice].top);
    pwm_set_chan_level(slice, pwm_gpio_to_channel(pin), (uint16_t)(duty * (float)(top + 1u)));
}
```

`clock_get_hz()` needs `hardware_clocks` (pulled in by `pico_stdlib`). Two pins on the same slice
share its frequency; plan the pin map so each motor's channels sit on their own slice when they
need different settings.

## Control tick

```c
static repeating_timer_t tick_timer;
static volatile bool g_tick_due;
static volatile uint32_t g_tick_overruns;

static bool tick_cb(repeating_timer_t *rt)
{
    if (g_tick_due) g_tick_overruns++;
    g_tick_due = true;
    return true;                                  // keep repeating
}

void tick_start(void)
{
    // Negative delay: period measured start to start, so the rate does not drift
    add_repeating_timer_us(-1000, tick_cb, NULL, &tick_timer);   // 1 kHz (example)
}
```

The callback runs in an interrupt (the alarm pool's IRQ); keep it short like any ISR.

## DMA

```c
int ch = dma_claim_unused_channel(true);
dma_channel_config_t c = dma_channel_get_default_config(ch);
channel_config_set_transfer_data_size(&c, DMA_SIZE_16);
channel_config_set_read_increment(&c, false);                 // ADC FIFO
channel_config_set_write_increment(&c, true);
channel_config_set_dreq(&c, DREQ_ADC);
dma_channel_configure(ch, &c, adc_buf, &adc_hw->fifo, ADC_SAMPLES, true);
```

The SDK 2.x name of the count argument is `encoded_transfer_count`; a plain count works for the
normal mode. Wait with `dma_channel_wait_for_finish_blocking()` or an IRQ on `DMA_IRQ_0`.

## Watchdog

```c
void safety_watchdog_start(void)
{
    if (watchdog_enable_caused_reboot()) report_reset("watchdog");   // a timeout of our watchdog
    watchdog_enable(200, true);   // ms (example); true pauses it while a debugger halts the core
}
// main loop, after the tick and the checks: watchdog_update();
```

Limits from the SDK header: up to 8388 ms on RP2040 (erratum RP2040-E1) and 16777 ms on RP2350.
`watchdog_caused_reboot()` is also true after a UF2 load or `watchdog_reboot()`; use
`watchdog_enable_caused_reboot()` to tell a real timeout apart.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| Control loop stalls for half a second when the computer is unplugged | `printf` over stdio USB blocks up to `PICO_STDIO_USB_STDOUT_TIMEOUT_US` (default 500 ms) when nobody reads | No `printf` in the control path; buffered, non-blocking telemetry |
| No output after flashing until a terminal opens | stdio USB waits for DTR before sending (`PICO_STDIO_USB_CONNECTION_WITHOUT_DTR` is 0) | Open the port first (pyserial and `cat` assert DTR) |
| `picotool load -f` cannot find the device | Firmware does not link `pico_stdio_usb`, or USB is busy with TinyUSB device code | Hold BOOTSEL while plugging in; or add the reset interface to your own TinyUSB descriptors |
| PWM frequency off by the clock change | Assumed 125 MHz on an RP2350 or after `set_sys_clock_khz()` | Compute from `clock_get_hz(clk_sys)` |
| Second motor changes frequency with the first | Both pins on one PWM slice | Re-map pins to separate slices |
