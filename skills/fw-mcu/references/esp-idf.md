# ESP32 with ESP-IDF and Arduino-ESP32

Part of [fw-mcu](../SKILL.md). Checked on 2026-11-27 against ESP-IDF `master` headers and the
v5.0 to v6.2 migration guides, the ESP-IDF 6.1.1 docs and examples (`ledc_basic`, `oneshot_read`,
`gptimer`), and Arduino-ESP32's 2.x→3.0 and 3.x→4.0 migration guides; not run. ESP-IDF is
Apache-2.0; the Arduino-ESP32 core is LGPL-2.1; the Wi-Fi and Bluetooth libraries are binary blobs
under Espressif's terms.

## Versions

| Line | Status on 2026-11-27 | Built on |
|---|---|---|
| ESP-IDF 6.1.1 | Latest stable (each release is supported 30 months: 12 service, 18 maintenance) | — |
| ESP-IDF 5.5.x | Maintained; check which line each third-party component supports (micro-ROS: [fw-rtos-micro-ros](../../fw-rtos-micro-ros/SKILL.md)) | — |
| Arduino-ESP32 4.0.0 | Latest, released 2026-11-19 | ESP-IDF 6.1.1 |
| Arduino-ESP32 3.3.x | Still released (3.3.13) | ESP-IDF 5.5 |
| PlatformIO `espressif32` 8.0.0 | Ships Arduino-ESP32 3.3.12 | ESP-IDF 5.5.5 (Arduino), 6.1 (`espidf` framework) |

Pick one line per project and pin it; most build breaks come from mixing them.

## What changed since ESP-IDF 4.x

| Old (4.x) | Now | When |
|---|---|---|
| `driver/adc.h` (`adc1_get_raw`) | `esp_adc/adc_oneshot.h`, `adc_continuous.h`, `adc_cali.h` | Deprecated 5.0, removed 6.0 |
| `driver/timer.h` (timer group) | `driver/gptimer.h` | Deprecated 5.0, removed 6.0 |
| `driver/pcnt.h` | `driver/pulse_cnt.h` (no longer sets pull-ups for you) | Deprecated 5.0, removed 6.0 |
| `driver/mcpwm.h` | `driver/mcpwm_prelude.h` | Deprecated 5.0, removed 6.0 |
| `driver/rmt.h` | `driver/rmt_tx.h`, `rmt_rx.h`, `rmt_encoder.h` | Deprecated 5.0, removed 6.0 |
| `driver/i2c.h` | `driver/i2c_master.h`, `i2c_slave.h` | New driver 5.2; old one end-of-life in 6.0, removal planned for 7.0 |
| `esp_task_wdt_init(timeout, panic)` | `esp_task_wdt_init(&esp_task_wdt_config_t)`; `CONFIG_ESP_TASK_WDT` became `_INIT` and `_EN` | 5.0 |
| One `driver` component | `esp_driver_gpio`, `esp_driver_ledc`, `esp_driver_gptimer`, `esp_driver_uart` and others | Split in 5.3; in 6.0 `driver` no longer pulls them in |
| Driver headers include FreeRTOS | Include `freertos/FreeRTOS.h` and friends yourself | 6.0 |
| `ledc_timer_set()`, `LEDC_SLOW_CLK_RTC8M` | `ledc_timer_config()` or `ledc_set_freq()`, `LEDC_SLOW_CLK_RC_FAST` | Removed 6.0 |
| `vTaskDelayUntil()` | `xTaskDelayUntil()` | Removed in the 6.x line |
| `idf.py size --format json` | `--format json2` | 6.0 |

List the driver components each source file uses:

```cmake
# main/CMakeLists.txt
idf_component_register(SRCS "main.c" "board.c" "control.c" "safety.c" "link.c"
                       INCLUDE_DIRS "."
                       REQUIRES esp_driver_gpio esp_driver_ledc esp_driver_gptimer esp_adc esp_driver_uart)
```

## GPIO interrupt

```c
#include "driver/gpio.h"

static volatile uint32_t s_limit_hits;
static void limit_isr(void *arg) { s_limit_hits++; }     // latch only

void board_inputs_init(void)
{
    gpio_config_t io = {
        .pin_bit_mask = 1ULL << PIN_LIMIT,
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .intr_type = GPIO_INTR_NEGEDGE,
    };
    ESP_ERROR_CHECK(gpio_config(&io));
    ESP_ERROR_CHECK(gpio_install_isr_service(0));
    ESP_ERROR_CHECK(gpio_isr_handler_add(PIN_LIMIT, limit_isr, NULL));
}
```

Handlers added this way no longer need `IRAM_ATTR` unless the service was installed with
`ESP_INTR_FLAG_IRAM`; such handlers are then deferred while flash is busy (NVS writes, OTA).

## PWM with LEDC

```c
#include "driver/ledc.h"

void pwm_init(void)
{
    ledc_timer_config_t t = {
        .speed_mode = LEDC_LOW_SPEED_MODE,       // the only mode on ESP32-S3
        .duty_resolution = LEDC_TIMER_10_BIT,
        .timer_num = LEDC_TIMER_0,
        .freq_hz = 20000,                        // example; resolution x frequency is limited by the clock
        .clk_cfg = LEDC_AUTO_CLK,
    };
    ESP_ERROR_CHECK(ledc_timer_config(&t));
    ledc_channel_config_t c = {
        .gpio_num = PIN_MOTOR_PWM, .speed_mode = LEDC_LOW_SPEED_MODE, .channel = LEDC_CHANNEL_0,
        .timer_sel = LEDC_TIMER_0, .duty = 0, .hpoint = 0,
    };
    ESP_ERROR_CHECK(ledc_channel_config(&c));
}

void pwm_set(float duty)                          // 0.0 .. 1.0; full on is 1 << resolution
{
    if (!(duty > 0.0f)) duty = 0.0f;
    if (duty > 1.0f) duty = 1.0f;
    ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, (uint32_t)(duty * 1024.0f));
    ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0);   // applies from the next PWM period
}
```

Half-bridges with dead time and encoders belong to MCPWM (`driver/mcpwm_prelude.h`) and PCNT
(`driver/pulse_cnt.h`), covered with motor control (`fw-motor-control`, a later batch).

## Control tick with gptimer

```c
#include "driver/gptimer.h"

static volatile bool s_tick_due;
static volatile uint32_t s_tick_overruns;

static bool on_tick(gptimer_handle_t t, const gptimer_alarm_event_data_t *e, void *ctx)
{
    if (s_tick_due) s_tick_overruns++;
    s_tick_due = true;                            // or give a task notification to the control task
    return false;                                 // true only if a higher-priority task was woken
}

void tick_start(void)
{
    gptimer_handle_t t;
    gptimer_config_t cfg = {
        .clk_src = GPTIMER_CLK_SRC_DEFAULT, .direction = GPTIMER_COUNT_UP,
        .resolution_hz = 1000000,                 // 1 us per count
    };
    ESP_ERROR_CHECK(gptimer_new_timer(&cfg, &t));
    gptimer_event_callbacks_t cbs = { .on_alarm = on_tick };
    ESP_ERROR_CHECK(gptimer_register_event_callbacks(t, &cbs, NULL));
    gptimer_alarm_config_t alarm = {
        .alarm_count = 1000, .reload_count = 0,   // 1 kHz (example)
        .flags.auto_reload_on_alarm = true,
    };
    ESP_ERROR_CHECK(gptimer_set_alarm_action(t, &alarm));
    ESP_ERROR_CHECK(gptimer_enable(t));
    ESP_ERROR_CHECK(gptimer_start(t));
}
```

The FreeRTOS tick in ESP-IDF defaults to 100 Hz (`CONFIG_FREERTOS_HZ`), so `vTaskDelay(pdMS_TO_TICKS(1))`
is a zero-tick delay: the old file's "1 ms" sensor task did not run at 1 ms. Use a hardware timer
or `esp_timer` for rates above the tick. With `CONFIG_GPTIMER_ISR_CACHE_SAFE`, the callback and what
it calls must be in IRAM.

## ADC one-shot

```c
#include "esp_adc/adc_oneshot.h"

adc_oneshot_unit_handle_t adc;
adc_oneshot_unit_init_cfg_t u = { .unit_id = ADC_UNIT_1 };
ESP_ERROR_CHECK(adc_oneshot_new_unit(&u, &adc));
adc_oneshot_chan_cfg_t ch = { .atten = ADC_ATTEN_DB_12, .bitwidth = ADC_BITWIDTH_DEFAULT };
ESP_ERROR_CHECK(adc_oneshot_config_channel(adc, ADC_CHANNEL_0, &ch));
int raw;
ESP_ERROR_CHECK(adc_oneshot_read(adc, ADC_CHANNEL_0, &raw));
```

Convert to millivolts through `esp_adc/adc_cali_scheme.h` (raw readings need calibration), and
read the ADC page's note on ADC2 and Wi-Fi for your chip before putting a sensor on ADC2.

## Task watchdog that actually resets

ESP-IDF starts the task watchdog at boot (`CONFIG_ESP_TASK_WDT_INIT=y`) watching the idle tasks,
but `CONFIG_ESP_TASK_WDT_PANIC` defaults to `n`, so a timeout only prints. For a robot, reset:

```c
#include "esp_task_wdt.h"

void safety_watchdog_start(void)                 // from the control task
{
    esp_task_wdt_config_t cfg = {
        .timeout_ms = 300,                       // example; above the slowest healthy loop
        .idle_core_mask = 0,                     // or keep watching the idle tasks
        .trigger_panic = true,                   // panic -> core dump if enabled -> reboot
    };
    ESP_ERROR_CHECK(esp_task_wdt_reconfigure(&cfg));   // init already ran at boot
    ESP_ERROR_CHECK(esp_task_wdt_add(NULL));           // subscribe this task
}
// in the control loop, after the tick and the checks: esp_task_wdt_reset();
```

Or set `CONFIG_ESP_TASK_WDT_PANIC=y` and `CONFIG_ESP_TASK_WDT_TIMEOUT_S` in `sdkconfig.defaults`
(the timeout there is whole seconds). Read the cause next boot with `esp_reset_reason()`
([debug.md](debug.md)).

## Arduino-ESP32

| API | 2.x | 3.x (IDF 5.x) | 4.0 (IDF 6.1) |
|---|---|---|---|
| PWM setup | `ledcSetup(ch, f, res)` + `ledcAttachPin(pin, ch)` | `ledcAttach(pin, f, res)`; functions take the pin | Same |
| PWM duty | `ledcWrite(ch, d)` | `ledcWrite(pin, d)`, full on `(1 << res) - 1` | `ledcWrite(pin, d)`, full on `1 << res`; `analogWrite()` unchanged |
| Timer | `timerBegin` with a divider, `timerAlarmWrite`, `timerAlarmEnable` | `timerBegin(freq_hz)`, `timerAttachInterrupt(t, fn)`, `timerAlarm(t, ticks, autoreload, 0)` | Same |
| ADC mV | `analogReadMilliVolts()` returns `uint32_t` | Same | Returns `int32_t` |
| IDF headers | IDF 4.4 | IDF 5.x | Removed legacy headers fail to compile (table above) |

`loop()` runs in an Arduino task; `enableLoopWDT()` subscribes it to the task watchdog and the core
feeds it between iterations. Whether a timeout resets depends on the prebuilt `sdkconfig`, so call
`esp_task_wdt_reconfigure()` with `trigger_panic = true` as above and test it.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| Undefined `gptimer_*`/`ledc_*` after moving to 6.x | Component not in `REQUIRES` | Add the `esp_driver_*` component |
| `portMAX_DELAY` or `TaskHandle_t` undeclared in 6.x | Driver headers no longer include FreeRTOS | `#include "freertos/FreeRTOS.h"` |
| Control tick jitters during NVS writes or OTA | Flash access disables the cache; non-IRAM ISRs wait | IRAM-safe ISR options; no flash writes while driving |
| Motor driver pin glitches at boot | Strapping or boot-time UART/JTAG pins | Use pins the chip datasheet lists as free at reset |
| USB-JTAG port vanishes | Firmware reconfigured the USB pins, or deep sleep | Keep the USB pins; hold BOOT and reset to recover |
| `CONFIG_*` change ignored | Edited `sdkconfig` lost on `set-target`, or not in `sdkconfig.defaults` | Put choices in `sdkconfig.defaults`; delete `sdkconfig` to regenerate |
