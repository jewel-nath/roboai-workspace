# Firmware skeleton: control task, cmd_vel timeout, publisher and subscriber

Part of [fw-rtos-micro-ros](../SKILL.md). C for FreeRTOS with rclc on ROS 2 Jazzy, written for this
skill. API names checked on 2026-11-27 against `ros2/rclc` `jazzy` (6.1.2), `micro-ROS/rmw_microxrcedds`
`jazzy` (`rmw_microros/*.h`) and FreeRTOS-Kernel V11.3.3. Not compiled or run. Timing values and
limits are examples to tune.

- `control_task` (high priority, 100 Hz) drives the motors from the latest `cmd_vel` and stops them
  when that command is older than `CMD_TIMEOUT_MS`. It never calls micro-ROS. One timeout covers a
  silent publisher, a dead agent, a cut cable and a hung micro-ROS task.
- The micro-ROS side subscribes to `cmd_vel` and publishes `wheel_states` from a timer. Its task,
  the entity setup and the reconnect and time-sync logic are the second half of the same file:
  [reconnect-timesync.md](reconnect-timesync.md).

Valid as C and as C++ (an Arduino `.cpp`). `ESP32_FREERTOS` covers ESP-IDF and Arduino-ESP32.

```c
/* my_robot_firmware: control task + micro-ROS task (FreeRTOS, rclc, ROS 2 Jazzy) */
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

#if defined(ESP_PLATFORM) || defined(ARDUINO_ARCH_ESP32)
#define ESP32_FREERTOS 1
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#else
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#endif

#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <rmw_microros/rmw_microros.h>
#include <geometry_msgs/msg/twist.h>
#include <sensor_msgs/msg/joint_state.h>

/* Board layer, written per board (fw-mcu; motor drivers in the later fw-motor-control). */
void board_transport_init(void);      /* rmw_uros_set_custom_transport(...) or a path's helper */
void motors_set(float v, float w);    /* also clamps to the drive's own limits */
void motors_stop(void);               /* zero command; must not block */
void wheels_read(double pos[2], double vel[2]);
void watchdog_feed(void);             /* hardware watchdog, fed only from the control loop */

#define CONTROL_PERIOD_MS  10         /* example: 100 Hz */
#define PUBLISH_PERIOD_MS  20         /* example: 50 Hz */
#define CMD_TIMEOUT_MS     300        /* example: stop 300 ms after the last cmd_vel */
#define PING_PERIOD_MS     500        /* example */
#define SYNC_PERIOD_MS     10000      /* example: re-sync the clock every 10 s */
#define ROS_DOMAIN         0          /* must equal ROS_DOMAIN_ID on the robot computer */
#define MAX_V              0.5f       /* m/s, example limit */
#define MAX_W              2.0f       /* rad/s, example limit */

typedef struct { float v, w; TickType_t stamp; bool valid; } cmd_t;
typedef struct { double pos[2], vel[2]; } wheels_t;

static QueueHandle_t cmd_q;           /* length 1: latest command */
static QueueHandle_t wheels_q;        /* length 1: latest wheel state */

static void micro_ros_task(void *arg);   /* reconnect-timesync.md */

static float clampf(float x, float lim) { return x > lim ? lim : (x < -lim ? -lim : x); }

/* ---------------- control: no micro-ROS calls here ---------------- */

static void control_task(void *arg)
{
    (void)arg;
    TickType_t last_wake = xTaskGetTickCount();
    for (;;) {
        cmd_t cmd = {0};
        (void)xQueuePeek(cmd_q, &cmd, 0);
        TickType_t age = xTaskGetTickCount() - cmd.stamp;      /* unsigned: wraps safely */
        if (cmd.valid && age <= pdMS_TO_TICKS(CMD_TIMEOUT_MS)) {
            motors_set(cmd.v, cmd.w);
        } else {
            motors_stop();
        }
        wheels_t w;
        wheels_read(w.pos, w.vel);
        (void)xQueueOverwrite(wheels_q, &w);
        watchdog_feed();
        (void)xTaskDelayUntil(&last_wake, pdMS_TO_TICKS(CONTROL_PERIOD_MS));
    }
}

/* ---------------- micro-ROS entities and messages ---------------- */

static rcl_allocator_t allocator;
static rclc_support_t support;
static rcl_node_t node;
static rcl_publisher_t wheels_pub;
static rcl_subscription_t cmd_sub;
static rcl_timer_t pub_timer;
static rclc_executor_t executor;

static geometry_msgs__msg__Twist twist_in;
static sensor_msgs__msg__JointState js;          /* static memory, built once at boot */
static rosidl_runtime_c__String js_names[2];
static char js_name_buf[2][24];
static double js_pos[2], js_vel[2];

static void joint_state_init(void)
{
    static const char *const names[2] = {"left_wheel_joint", "right_wheel_joint"};
    for (size_t i = 0; i < 2; i++) {
        snprintf(js_name_buf[i], sizeof js_name_buf[i], "%s", names[i]);
        js_names[i].data = js_name_buf[i];
        js_names[i].size = strlen(js_name_buf[i]);
        js_names[i].capacity = sizeof js_name_buf[i];
    }
    js.name.data = js_names;   js.name.size = js.name.capacity = 2;
    js.position.data = js_pos; js.position.size = js.position.capacity = 2;
    js.velocity.data = js_vel; js.velocity.size = js.velocity.capacity = 2;
}

static void cmd_vel_cb(const void *msgin)
{
    const geometry_msgs__msg__Twist *t = (const geometry_msgs__msg__Twist *)msgin;
    if (!isfinite(t->linear.x) || !isfinite(t->angular.z)) {
        return;                                          /* ignore NaN and inf */
    }
    cmd_t c = { clampf((float)t->linear.x, MAX_V), clampf((float)t->angular.z, MAX_W),
                xTaskGetTickCount(), true };
    (void)xQueueOverwrite(cmd_q, &c);
}

static void publish_cb(rcl_timer_t *timer, int64_t last_call_time)
{
    (void)last_call_time;
    wheels_t w;
    if (timer == NULL || !rmw_uros_epoch_synchronized() ||
        xQueuePeek(wheels_q, &w, 0) != pdTRUE) {
        return;                                          /* no synced clock or no data: publish nothing */
    }
    int64_t ns = rmw_uros_epoch_nanos();                 /* stamped at publish time */
    js.header.stamp.sec = (int32_t)(ns / 1000000000LL);
    js.header.stamp.nanosec = (uint32_t)(ns % 1000000000LL);
    memcpy(js_pos, w.pos, sizeof js_pos);
    memcpy(js_vel, w.vel, sizeof js_vel);
    (void)rcl_publish(&wheels_pub, &js, NULL);           /* a dead link is caught by the ping */
}

/* ---------------- start ---------------- */

/* Call from main(), app_main() or setup() after clocks, pins and the transport hardware are set up. */
void firmware_start(void)
{
    cmd_q = xQueueCreate(1, sizeof(cmd_t));
    wheels_q = xQueueCreate(1, sizeof(wheels_t));
    configASSERT(cmd_q != NULL && wheels_q != NULL);
    motors_stop();
    joint_state_init();
    board_transport_init();
    /* Sizes and priorities are examples; measure the high-water marks (rtos-tasks.md). */
#ifdef ESP32_FREERTOS
    /* bytes; control pinned to core 1 (0 on single-core chips), away from Wi-Fi on core 0 */
    xTaskCreatePinnedToCore(control_task, "control", 4096, NULL, 10, NULL, 1);
    xTaskCreatePinnedToCore(micro_ros_task, "micro_ros", 16000, NULL, 5, NULL, 0);
#else
    /* words */
    xTaskCreate(control_task, "control", 512, NULL, configMAX_PRIORITIES - 2, NULL);
    xTaskCreate(micro_ros_task, "micro_ros", 3000, NULL, 2, NULL);
#endif
}

/* create_entities(), destroy_entities() and micro_ros_task(): reconnect-timesync.md */
```

## Choices in this code

- **Best effort both ways.** A lost `cmd_vel` is replaced by the next one and the timeout covers
  silence; a best-effort publisher never blocks the task waiting for an acknowledgement. Computer-side
  subscribers to `wheel_states` need sensor-data QoS ([memory-qos.md](memory-qos.md)).
- **`wheel_states`, not `joint_states`.** On a robot whose computer already runs
  `joint_state_broadcaster`, a second `/joint_states` publisher clashes; remap if the MCU is the
  only source.
- **Odometry on the computer.** `nav_msgs/msg/Odometry` is about 720 bytes, too big for a
  best-effort publisher at the default MTU. Publish wheel states and integrate on the computer.
- **Stamp age.** The stamp is the publish time; subtract the sample's age when it matters (keep the
  tick of `wheels_read` in `wheels_t`).
- **Limits twice.** The callback clamps to `MAX_V` and `MAX_W`; `motors_set` clamps again to what
  the drive allows. Current and torque limits belong to the drive or the later `fw-motor-control`.

## Adapting it

- Transport, Arduino-ESP32 `setup()` and `loop()`, Wi-Fi: [build-paths.md](build-paths.md#wiring-the-skeleton).
- More publishers or subscriptions, larger messages, `TwistStamped`, message memory:
  [memory-qos.md](memory-qos.md).
- Boards without an RTOS (Teensy `loop()`): [rtos-tasks.md](rtos-tasks.md#without-an-rtos).
