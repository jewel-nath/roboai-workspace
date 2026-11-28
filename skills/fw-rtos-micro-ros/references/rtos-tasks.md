# RTOS tasks, priorities, queues and timing

Part of [fw-rtos-micro-ros](../SKILL.md). Checked on 2026-11-27 against the FreeRTOS-Kernel V11.3.3
headers (`task.h`, `queue.h`, `FreeRTOS.h`, `portable.h`, `stack_macros.h`, `History.txt`), the
ESP-IDF v6.1 guides (FreeRTOS (IDF), Speed Optimization), the Arduino-ESP32 core's `main.cpp`, and
the Zephyr kernel docs (latest, 4.5). Values marked "example" are choices to tune.

## A task layout for a robot MCU

| Task | Priority | Timing | Owns |
|---|---|---|---|
| `control` | highest application priority | periodic: `xTaskDelayUntil` or a timer-ISR notification | motor outputs, encoders, the command timeout, the watchdog feed |
| `sensors` | below `control` | periodic | its bus (behind a mutex if shared) |
| `micro_ros` | below both | blocks inside the executor spin and the ping | every `rcl_*`, `rclc_*` and `rmw_uros_*` call |
| logging, stats | lowest above idle | slow | debug output on a UART that is *not* the micro-ROS link |

- **One task owns micro-ROS.** The default build has `UCLIENT_PROFILE_MULTITHREAD=OFF`, and the
  rclc headers mark their calls "Thread-Safe: No". Other tasks hand data over through queues.
- **Control never waits on communication.** A reliable publish blocks until the agent acknowledges
  or `RMW_UXRCE_PUBLISH_RELIABLE_TIMEOUT` passes (1000 ms by default); a ping blocks up to
  timeout × attempts; creating entities waits up to 1000 ms each. Any of these inside the control
  loop stalls the motors.
- **Priorities.** FreeRTOS: a higher number is more urgent; 0 is the idle task; the top is
  `configMAX_PRIORITIES - 1`. Zephyr: a lower number is more urgent; negative numbers are
  cooperative (never preempted by other threads). ESP-IDF's own tasks: Wi-Fi 23 (core 0),
  `esp_timer` 22 (core 0), lwIP 18, `app_main` 1.
- Every task must block (delay, queue, notification). One that never blocks starves all lower
  tasks, including idle; on ESP-IDF the task watchdog can then fire.

## Periodic timing

```c
static void control_task(void *arg)
{
    (void)arg;
    TickType_t last_wake = xTaskGetTickCount();
    uint32_t overruns = 0;
    for (;;) {
        control_step();                                   /* read, decide, write */
        if (xTaskDelayUntil(&last_wake, pdMS_TO_TICKS(CONTROL_PERIOD_MS)) == pdFALSE) {
            overruns++;                                   /* deadline already passed: no delay */
        }
    }
}
```

- `vTaskDelay(n)` waits n ticks from the call, so the loop body's time adds to every period.
  `xTaskDelayUntil` wakes at fixed multiples of the period and returns `pdFALSE` when it did not
  block, which is how you count overruns.
- `xTaskDelayUntil` exists since V10.4.2 (`INCLUDE_xTaskDelayUntil 1`); older kernels, still in
  some vendor packages, only have `vTaskDelayUntil` (returns nothing). V11.3.1 added
  `xTaskPeriodicDelay`, which returns how many periods passed and never lets the wake time run away.
- `pdMS_TO_TICKS` rounds down to whole ticks: with `configTICK_RATE_HZ 100`, 5 ms becomes 0.
  Use a 1000 Hz tick, or a hardware timer for loops faster than about 1 kHz.

Jitter-sensitive loops: let a hardware timer wake the task (timer setup is in
[fw-mcu](../../fw-mcu/SKILL.md)).

```c
static TaskHandle_t control_handle;          /* from xTaskCreate */

void CONTROL_TIMER_IRQHandler(void)          /* board-specific name; clear the flag first */
{
    BaseType_t woken = pdFALSE;
    vTaskNotifyGiveFromISR(control_handle, &woken);
    portYIELD_FROM_ISR(woken);
}

/* in control_task: a missing tick means the timer died, so stop the motors */
if (ulTaskNotifyTake(pdTRUE, pdMS_TO_TICKS(2 * CONTROL_PERIOD_MS)) == 0) {
    motors_stop();
}
```

ISR rules: call only `...FromISR` functions in an ISR. On Cortex-M ports, an ISR that calls them
must have a priority numerically at or above `configMAX_SYSCALL_INTERRUPT_PRIORITY` (that is, no
more urgent); with `configASSERT` defined, `vPortValidateInterruptPriority` stops the firmware when
this is wrong. Choosing interrupt priorities belongs to [fw-mcu](../../fw-mcu/SKILL.md).

## Queues and shared data

```c
typedef struct { float v, w; TickType_t stamp; bool valid; } cmd_t;
static QueueHandle_t cmd_q;                          /* created before the scheduler starts */

cmd_q = xQueueCreate(1, sizeof(cmd_t));              /* length 1: latest value only */
configASSERT(cmd_q != NULL);

xQueueOverwrite(cmd_q, &cmd);                        /* writer: never blocks, replaces the old value */
if (xQueuePeek(cmd_q, &cmd, 0) == pdTRUE) { ... }    /* reader: reads without removing */
```

- Latest-value data (commands, current state): a queue of length 1 with `xQueueOverwrite` (only
  valid on length-1 queues) and `xQueuePeek`.
- Streams where every item counts: a longer queue, `xQueueSend(q, &item, 0)` (drop and count when
  full, never block the producer), `xQueueReceive` in the consumer.
- A bus shared by two tasks: `xSemaphoreCreateMutex()` (has priority inheritance), taken with a
  timeout, never in an ISR. A struct copied between tasks without a queue or lock can tear.

## Stack, heap and the debug hooks

- **Stack units.** Vanilla FreeRTOS `xTaskCreate` takes the depth in words (`StackType_t`, 4 bytes
  on Cortex-M); ESP-IDF takes **bytes**. 3000 means 12 KB on an STM32 and 3 KB on an ESP32.
- **micro-ROS task size.** micro_ros_stm32cubemx_utils asks for more than 10 kB (its sample uses
  3000 words); the ESP-IDF component's default is `CONFIG_MICRO_ROS_APP_STACK` = 16000 bytes; the
  Zephyr module's `prj.conf` sets `CONFIG_MAIN_STACK_SIZE=25000`. Measure, then keep a margin.
- **Arduino-ESP32** runs `setup()` and `loop()` in a task called `loopTask` (priority 1, 8192
  bytes by default). micro-ROS in `loop()` usually needs more: `SET_LOOP_TASK_STACK_SIZE(16 * 1024);`
  at file scope (example size).
- **Heap.** The scheme is chosen by compiling exactly one of `heap_1.c` to `heap_5.c`; there is no
  config macro for it. `heap_4` (first fit, merges free blocks) suits code that allocates and
  frees. `configTOTAL_HEAP_SIZE` is in bytes and lives in RAM next to the stacks and `.bss`.
  `xPortGetMinimumEverFreeHeapSize()` tells you the headroom after a long run.
- **micro-ROS allocations** go through the rcutils default allocator. On FreeRTOS set it to heap
  functions with `rcutils_set_default_allocator()` before `rclc_support_init` (the STM32 utils
  sample does). Their `custom_memory_manager.c` keeps its own `ucHeap[configTOTAL_HEAP_SIZE]`, a
  second heap of the same size next to FreeRTOS's.
- **Static allocation.** `xTaskCreateStatic` and `xQueueCreateStatic` need
  `configSUPPORT_STATIC_ALLOCATION 1`, which needs `vApplicationGetIdleTaskMemory` (and the timer
  task's) unless `configKERNEL_PROVIDED_STATIC_MEMORY 1` (V11.0 and later).

```c
/* FreeRTOSConfig.h, debug build */
#define configCHECK_FOR_STACK_OVERFLOW        2   /* 1: stack pointer check; 2: also checks a fill pattern at the stack end */
#define configUSE_MALLOC_FAILED_HOOK          1
#define configASSERT(x)                       if ((x) == 0) { taskDISABLE_INTERRUPTS(); for (;;) {} }
#define INCLUDE_uxTaskGetStackHighWaterMark   1
#define INCLUDE_xTaskDelayUntil               1
#define configUSE_TRACE_FACILITY              1   /* with the next line: vTaskListTasks */
#define configUSE_STATS_FORMATTING_FUNCTIONS  1
```

```c
void vApplicationStackOverflowHook(TaskHandle_t task, char *name)
{
    (void)task; (void)name;
    motors_stop();                  /* outputs safe first; then halt and let the watchdog reset */
    taskDISABLE_INTERRUPTS();
    for (;;) {}
}

void vApplicationMallocFailedHook(void)
{
    motors_stop();
    taskDISABLE_INTERRUPTS();
    for (;;) {}
}
```

The overflow check runs at context switches and does not catch every overflow; it is a debug aid.
`motors_stop()` here must be a plain register write that cannot block or allocate.

## Measuring

```c
UBaseType_t free_words = uxTaskGetStackHighWaterMark(NULL);   /* smallest free stack seen, in words (bytes on ESP-IDF) */
size_t heap_low = xPortGetMinimumEverFreeHeapSize();          /* heap_4 and heap_5 */
```

- `vTaskListTasks(buf, len)` and `vTaskGetRunTimeStatistics(buf, len)` print every task's state,
  stack and CPU share (V11; older kernels have `vTaskList(buf)` and `vTaskGetRunTimeStats(buf)`
  without a length). Run-time stats need `configGENERATE_RUN_TIME_STATS 1` and a counter at least
  ten times faster than the tick (`portCONFIGURE_TIMER_FOR_RUN_TIME_STATS`,
  `portGET_RUN_TIME_COUNTER_VALUE`).
- Both disable interrupts while they run: use them on the bench, not while driving.
- Read the high-water marks after a long run that includes agent restarts and reconnects; that is
  when the micro-ROS task uses the most stack.

## Without an RTOS

Teensy, SAMD and Pico Arduino builds run one `loop()`. The same split still applies:

- The control step runs from a hardware timer interrupt (Teensy `IntervalTimer`, or a timer set up
  as in [fw-mcu](../../fw-mcu/SKILL.md)): read the latest command, check its age, write the motors.
  Keep it short and free of micro-ROS calls.
- `loop()` runs the agent-state machine and `rclc_executor_spin_some` with short timeouts. Each
  ping blocks the loop for up to timeout × attempts, which is why control must not live there.
- Data shared between the interrupt and `loop()`: `volatile`, and copied with interrupts briefly
  disabled when wider than one machine word.

## ESP-IDF differences

- IDF FreeRTOS is based on V10.5.1 with SMP changes: stack sizes in bytes; `xTaskCreate` gives
  `tskNO_AFFINITY`; `xTaskCreatePinnedToCore(fn, name, bytes, arg, prio, &handle, core)` pins.
- Pin the control task to core 1, away from the Wi-Fi task on core 0:
  `xTaskCreatePinnedToCore(control_task, "control", 4096, NULL, 10, &control_handle, 1);` (sizes
  and priority are examples).
- Functions added in kernel V11 (`vTaskListTasks`, `xTaskPeriodicDelay`,
  `configKERNEL_PROVIDED_STATIC_MEMORY`) may be missing; check the IDF API reference.
- Headers are `freertos/FreeRTOS.h`, `freertos/task.h`, `freertos/queue.h`.

## Zephyr equivalents

| FreeRTOS | Zephyr |
|---|---|
| `xTaskCreate` | `K_THREAD_DEFINE(name, stack_bytes, entry, p1, p2, p3, prio, options, delay_ms)` or `k_thread_create` |
| priority: higher number more urgent | lower number more urgent; negative = cooperative |
| `xTaskDelayUntil` | `k_timer_start` + `k_timer_status_sync` in the thread, or `k_sleep` |
| length-1 queue + overwrite | `k_msgq` (`K_MSGQ_DEFINE(name, item_size, max_items, align)`); `k_msgq_purge` then `k_msgq_put(..., K_NO_WAIT)` |
| mutex | `k_mutex` (priority inheritance) |
| `vTaskNotifyGiveFromISR` | `k_sem_give` from the ISR |
| stack high-water mark | `CONFIG_INIT_STACKS` + `CONFIG_THREAD_STACK_INFO`, then `k_thread_stack_space_get` |

`k_msgq_put` with `K_NO_WAIT` may be called from an ISR; an ISR must never wait. The micro-ROS
Zephyr module was tested on Zephyr 4.0 and 4.1.
