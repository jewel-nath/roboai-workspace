# Reconnecting after the agent drops, and time sync

Part of [fw-rtos-micro-ros](../SKILL.md). The second half of the file started in
[firmware-skeleton.md](firmware-skeleton.md). Checked on 2026-11-27 against `rmw_microxrcedds`
`jazzy` (`rmw_microros/ping.h`, `time_sync.h`, `timing.h`, `rmw_init.c`), `ros2/rclc` `jazzy`,
`micro-ROS/rcl` `jazzy`, the micro_ros_arduino `jazzy` examples `micro-ros_reconnection_example`
and `micro-ros_time_sync`, and the micro-ROS docs (micro-ROS utilities). Not compiled or run.

## Why it is needed

Everything the firmware creates (node, publishers, subscriptions) lives in an XRCE session on the
agent. When the agent restarts, the session is gone: `rcl_publish` starts failing and nothing
arrives, but nothing on the MCU notices unless it asks. The pattern from the upstream reconnection
example: ping the agent, create the entities, keep pinging, and on failure destroy everything
without waiting for the dead agent, then start over.

```c
#define TRY(fn) do { if ((fn) != RCL_RET_OK) { return false; } } while (0)

static bool create_entities(void)
{
    memset(&support, 0, sizeof support);
    node = rcl_get_zero_initialized_node();
    wheels_pub = rcl_get_zero_initialized_publisher();
    cmd_sub = rcl_get_zero_initialized_subscription();
    pub_timer = rcl_get_zero_initialized_timer();
    executor = rclc_executor_get_zero_initialized_executor();

    allocator = rcl_get_default_allocator();
    rcl_init_options_t opts = rcl_get_zero_initialized_init_options();
    TRY(rcl_init_options_init(&opts, allocator));
    /* UDP builds: rmw_uros_options_set_udp_address(ip, port, rcl_init_options_get_rmw_init_options(&opts)); */
    rcl_ret_t rc = rcl_init_options_set_domain_id(&opts, ROS_DOMAIN);
    if (rc == RCL_RET_OK) {
        rc = rclc_support_init_with_options(&support, 0, NULL, &opts, &allocator);
    }
    (void)rcl_init_options_fini(&opts);                  /* rcl_init keeps its own copy */
    TRY(rc);

    TRY(rclc_node_init_default(&node, "my_robot_firmware", "", &support));
    TRY(rclc_publisher_init_best_effort(&wheels_pub, &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(sensor_msgs, msg, JointState), "wheel_states"));
    TRY(rclc_subscription_init_best_effort(&cmd_sub, &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(geometry_msgs, msg, Twist), "cmd_vel"));
    TRY(rclc_timer_init_default2(&pub_timer, &support,
        RCL_MS_TO_NS(PUBLISH_PERIOD_MS), publish_cb, true));
    TRY(rclc_executor_init(&executor, &support.context, 2, &allocator));   /* 1 subscription + 1 timer */
    TRY(rclc_executor_add_subscription(&executor, &cmd_sub, &twist_in, &cmd_vel_cb, ON_NEW_DATA));
    TRY(rclc_executor_add_timer(&executor, &pub_timer));
    return true;
}

static void destroy_entities(void)
{
    rmw_context_t *rmw_ctx = rcl_context_get_rmw_context(&support.context);
    if (rmw_ctx != NULL) {
        (void)rmw_uros_set_context_entity_destroy_session_timeout(rmw_ctx, 0);  /* agent gone: do not wait */
    }
    (void)rcl_publisher_fini(&wheels_pub, &node);
    (void)rcl_subscription_fini(&cmd_sub, &node);
    (void)rcl_timer_fini(&pub_timer);
    (void)rclc_executor_fini(&executor);
    (void)rcl_node_fini(&node);
    (void)rclc_support_fini(&support);
}

typedef enum { WAITING_AGENT, AGENT_AVAILABLE, AGENT_CONNECTED, AGENT_DISCONNECTED } agent_state_t;

static void micro_ros_task(void *arg)
{
    (void)arg;
    agent_state_t state = WAITING_AGENT;
    TickType_t last_ping = 0, last_sync = 0;
    for (;;) {
        TickType_t now = xTaskGetTickCount();
        switch (state) {
        case WAITING_AGENT:
            if (rmw_uros_ping_agent(100, 1) == RMW_RET_OK) {
                state = AGENT_AVAILABLE;
            } else {
                vTaskDelay(pdMS_TO_TICKS(500));
            }
            break;
        case AGENT_AVAILABLE:
            if (create_entities()) {
                (void)rmw_uros_sync_session(100);
                last_ping = last_sync = now;
                state = AGENT_CONNECTED;
            } else {
                destroy_entities();
                state = WAITING_AGENT;
            }
            break;
        case AGENT_CONNECTED:
            if (now - last_ping >= pdMS_TO_TICKS(PING_PERIOD_MS)) {
                last_ping = now;
                if (rmw_uros_ping_agent(100, 3) != RMW_RET_OK) {   /* 3 tries: one lost packet is not a drop */
                    state = AGENT_DISCONNECTED;
                    break;
                }
            }
            if (now - last_sync >= pdMS_TO_TICKS(SYNC_PERIOD_MS)) {
                last_sync = now;
                (void)rmw_uros_sync_session(100);
            }
            (void)rclc_executor_spin_some(&executor, RCL_MS_TO_NS(10));  /* RCL_RET_TIMEOUT is normal */
            break;
        case AGENT_DISCONNECTED:
            destroy_entities();
            state = WAITING_AGENT;
            break;
        }
    }
}
```

## Details that matter

- `rmw_uros_ping_agent(timeout_ms, attempts)` returns `RMW_RET_OK` (an `rmw_ret_t`, not
  `RCL_RET_OK`) when the agent answers; the timeout is per attempt. It works before any entity
  exists, and must not run at the same time as `rmw_init` or `rmw_shutdown`: keep it in the
  micro-ROS task.
- The connected-state ping is the only reliable sign of a lost agent. Best-effort publishes report
  success into a dead link; reliable ones fail only after their timeout.
- `rmw_uros_set_context_entity_destroy_session_timeout(ctx, 0)` before the `fini` calls stops each
  of them waiting for the agent (1000 ms each by default). Without it, a reconnect takes seconds.
- Zero-initialize every entity before creating it, so a partial `create_entities` can be torn down
  safely by `destroy_entities`.
- `rclc_executor_spin_some` returns `RCL_RET_TIMEOUT` when nothing was ready; that is not an error.
  While it waits, the custom transport's read must block (yield), not busy-poll, or lower tasks
  starve.
- The upstream example notes that creating and destroying can take seconds and suggests building
  with `RMW_UXRCE_ENTITY_CREATION_DESTROY_TIMEOUT=0` and `UCLIENT_MAX_SESSION_CONNECTION_ATTEMPTS=3`;
  with 0, creation stops waiting for the agent's confirmation ([memory-qos.md](memory-qos.md)).
- **MCU reset.** The firmware boots into `WAITING_AGENT` and the agent accepts the new session
  (client keys are random per boot unless set with `rmw_uros_options_set_client_key`).
- **Over Wi-Fi** a few lost pings are normal; raise the attempts or the period rather than tearing
  the session down on one miss. The motor timeout is what keeps the robot safe meanwhile.
- **Superloop builds** (Arduino `loop()` without an RTOS): the same state machine, but each ping
  blocks the loop for up to timeout × attempts; the control step must run from a timer interrupt.

## Time sync

```c
(void)rmw_uros_sync_session(100);              /* NTP-style exchange with the agent, 100 ms timeout */
if (rmw_uros_epoch_synchronized()) {
    int64_t ns = rmw_uros_epoch_nanos();       /* agent computer's epoch time, int64 nanoseconds */
    msg.header.stamp.sec = (int32_t)(ns / 1000000000LL);
    msg.header.stamp.nanosec = (uint32_t)(ns % 1000000000LL);
}
```

- `rmw_uros_sync_session` needs a live session (call it after `create_entities`), corrects for the
  transport delay, and returns `RMW_RET_ERROR` on failure. `rmw_uros_epoch_millis()` gives
  milliseconds.
- Before the first successful sync, the epoch functions return the MCU's own clock (or 0 without a
  session): stamps near 1970 that make TF and message filters drop the data. Do not publish stamped
  messages until `rmw_uros_epoch_synchronized()` is true.
- `header.stamp` is a `builtin_interfaces/msg/Time` struct (`int32_t sec`, `uint32_t nanosec`);
  assigning the `int64_t` to it directly does not compile.
- The MCU crystal drifts, so re-sync periodically (example: every 10 s) and after every reconnect.
- The agent's computer is the time source: sync it with the robot's other computers first
  ([ops-bringup time sync](../../ops-bringup/references/time-sync.md)).
- Platform time source: micro-ROS needs a POSIX `clock_gettime` with at least 1 ms resolution for
  executor timing and reliable streams; micro_ros_platformio and the STM32 utils provide one.

## Checks

```bash
ros2 topic delay /wheel_states      # small and steady; seconds or years means no sync
sudo systemctl restart my-robot-uros-agent && sleep 5 && ros2 node list    # /my_robot_firmware is back
```

With the wheels off the ground and `cmd_vel` running, restart the agent: the wheels stop within the
command timeout, the node returns, and driving resumes only when commands flow again.
