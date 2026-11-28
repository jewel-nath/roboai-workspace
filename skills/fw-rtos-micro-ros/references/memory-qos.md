# micro-ROS memory limits, message size and QoS

Part of [fw-rtos-micro-ros](../SKILL.md). Checked on 2026-11-27 against `rmw_microxrcedds` `jazzy`
(`CMakeLists.txt`, `rmw_publish.c`, `config.h.in`), the Micro XRCE-DDS Client `ros2` branch
(`CMakeLists.txt`, `write_access.c`), `micro_ros_utilities` `jazzy`, `rclc_parameter` `jazzy`, the
default metas of each build path, and the micro-ROS docs (Middleware Configuration, QoS, micro-ROS
utilities). Message sizes below are computed from the message definitions, not measured.

## The model

rmw_microxrcedds allocates nothing at run time: every entity kind has a static pool whose size is a
CMake option fixed when the library is built. Creating one more publisher than the pool holds
makes `rclc_publisher_init_*` return an error; nothing grows. Changing a limit means rebuilding the
micro-ROS library.

## Where the limits are set

| Build path | File or setting | Rebuild |
|---|---|---|
| micro_ros_platformio | `board_microros_user_meta = my_robot.meta` (project folder) | `pio run -t clean_microros` |
| ESP-IDF component | `app-colcon.meta` in the project folder | `idf.py clean-microros` |
| STM32CubeMX utils | `microros_static_library/library_generation/colcon.meta` | rerun the library builder |
| micro_ros_arduino | `extras/library_generation/colcon*.meta` | rerun the library builder |
| Zephyr module | Kconfig `CONFIG_MICROROS_*` | `west build -p` |
| micro_ros_setup | `firmware/mcu_ws/colcon.meta`, after `configure_firmware.sh` (which rewrites it) | `build_firmware.sh` |

```json
{
    "names": {
        "rmw_microxrcedds": {
            "cmake-args": [
                "-DRMW_UXRCE_MAX_NODES=1",
                "-DRMW_UXRCE_MAX_PUBLISHERS=4",
                "-DRMW_UXRCE_MAX_SUBSCRIPTIONS=2",
                "-DRMW_UXRCE_MAX_SERVICES=0",
                "-DRMW_UXRCE_MAX_CLIENTS=0",
                "-DRMW_UXRCE_MAX_HISTORY=4",
                "-DRMW_UXRCE_TRANSPORT=custom"
            ]
        }
    }
}
```

Example `my_robot.meta` for one node with four publishers and two subscriptions. Keep the transport
line the build path uses (`custom` for PlatformIO and the STM32 utils, `udp` for the ESP-IDF
default). The file must be strict JSON: no comments.

## The options

| Option | Upstream default | What it limits |
|---|---|---|
| `RMW_UXRCE_MAX_NODES` | 4 | nodes |
| `RMW_UXRCE_MAX_PUBLISHERS` | 4 | publishers |
| `RMW_UXRCE_MAX_SUBSCRIPTIONS` | 4 | subscriptions |
| `RMW_UXRCE_MAX_SERVICES` / `_CLIENTS` | 4 / 4 | service servers / clients |
| `RMW_UXRCE_MAX_HISTORY` | 8 | received messages buffered per subscription, request and reply until taken |
| `RMW_UXRCE_MAX_WAIT_SETS`, `_GUARD_CONDITION` | 4, 4 | wait sets; guard conditions (one per rcl timer) |
| `RMW_UXRCE_MAX_TOPICS` | -1 (publishers + subscriptions + nodes) | topics |
| `RMW_UXRCE_STREAM_HISTORY` | 4 (power of two) | MTU-sized slots per reliable stream |
| `UCLIENT_SERIAL_TRANSPORT_MTU`, `_UDP_`, `_CUSTOM_` | 512 bytes each | one transport buffer |
| `RMW_UXRCE_PUBLISH_RELIABLE_TIMEOUT` | 1000 ms | how long a reliable publish waits for the acknowledgement |
| `RMW_UXRCE_ENTITY_CREATION_DESTROY_TIMEOUT` | 1000 ms | wait per entity create or destroy (0 = do not wait) |
| `UCLIENT_MAX_SESSION_CONNECTION_ATTEMPTS` | 10 | tries when opening the session |
| `RMW_UXRCE_NODE_NAME_MAX_LENGTH`, `_TOPIC_NAME_`, `_TYPE_NAME_` | 60, 60, 100 | name lengths |
| `RMW_UXRCE_ALLOW_DYNAMIC_ALLOCATIONS` | OFF | lets pools grow from the heap |

The build paths ship their own defaults, lower than upstream:

| Path | Nodes | Publishers | Subscriptions | Services | Clients | History |
|---|---|---|---|---|---|---|
| PlatformIO `colcon.meta` (Teensy 4, ESP32, Pico, Portenta) | 1 | 10 | 5 | 1 | 1 | 4 |
| PlatformIO `colcon_verylowmem.meta` (Due, Zero, Nano RP2040) | 1 | 2 | 1 | 0 | 1 | 1 |
| ESP-IDF component `colcon.meta` | 1 | 2 | 2 | 1 | 1 | 1 |
| Zephyr Kconfig defaults | 1 | 1 | 1 | 1 (servers) | 1 | 4 |

Count before you write code: one slot per publisher and subscription; the rclc parameter server
needs 5 services, an optional publisher and 6 executor handles. Each timer takes one
guard-condition slot (`RMW_UXRCE_MAX_GUARD_CONDITION`, 4 unless a meta changes it) and one
executor handle.

For faster reconnects the upstream example suggests `RMW_UXRCE_ENTITY_CREATION_DESTROY_TIMEOUT=0`
and `UCLIENT_MAX_SESSION_CONNECTION_ATTEMPTS=3`. With 0, creation no longer waits for the agent's
confirmation, so an `RCL_RET_OK` no longer proves the entity exists
([reconnect-timesync.md](reconnect-timesync.md)).

Check the values that were built in:

```bash
grep -E 'RMW_UXRCE_MAX_(NODES|PUBLISHERS|SUBSCRIPTIONS|HISTORY)' \
  .pio/libdeps/<env>/micro_ros_platformio/libmicroros/include/rmw_microxrcedds_c/config.h
```

## Message size

- **Best effort**: one message must fit in one transport buffer: at most MTU minus 12 bytes, about
  500 bytes at the default 512. The client cannot fragment on a best-effort stream, so a bigger
  message fails to publish (or is not received).
- **Reliable**: messages are split into fragments over the stream's slots; the upper bound is about
  MTU × `RMW_UXRCE_STREAM_HISTORY` (2 KB at the defaults).
- Bigger payloads (images, long arrays): reliable stream with a larger history, or the continuous
  serialization callbacks (`rmw_uros_set_continous_serialization_callbacks`, spelled that way).

Approximate serialized sizes (CDR, short frame names):

| Message | Bytes | Best effort at MTU 512 |
|---|---|---|
| `geometry_msgs/msg/Twist` | 48 | fits |
| `sensor_msgs/msg/JointState`, 2 joints | about 120 | fits |
| `sensor_msgs/msg/Imu` | about 320 (three 9-double covariances) | fits |
| `nav_msgs/msg/Odometry` | about 720 (two 36-double covariances) | **does not fit** |

RAM grows with the MTU (buffers per stream and per history slot): raise it only on boards with RAM
to spare, and set it in the meta for the transport you use.

## QoS

| rclc call | Reliability | Use for |
|---|---|---|
| `rclc_publisher_init_default` / `rclc_subscription_init_default` | reliable (`rmw_qos_profile_default`) | rare, must-arrive data; small messages that must not be lost |
| `rclc_publisher_init_best_effort` / `rclc_subscription_init_best_effort` | best effort | sensor streams; `cmd_vel` (the next command replaces a lost one, the timeout covers silence) |
| `rclc_publisher_init(&pub, &node, ts, "topic", &qos)` | from an `rmw_qos_profile_t` | custom depth, durability |

- A reliable publish blocks the calling task until the agent acknowledges, up to the reliable
  timeout; set it per publisher with
  `rmw_uros_set_publisher_session_timeout(rcl_publisher_get_rmw_handle(&pub), ms)`.
- Matching on the computer: a best-effort publisher reaches only best-effort subscribers. Use the
  sensor-data profile there (`rclcpp::SensorDataQoS()`, `qos_profile_sensor_data`); a reliable
  subscriber gets nothing. A reliable publisher reaches both. Rules and the
  `ros2 topic info -v` check: [ros2-core](../../ros2-core/SKILL.md).

## Message memory

The C message structs hold pointers for strings and sequences; the firmware must give them memory.

- **Publishing**: point `.data` at static buffers and set `.size` and `.capacity`, once at boot
  ([firmware-skeleton.md](firmware-skeleton.md)). Strings must end with `\0`; the serializer uses
  `strlen`.
- **Subscribing**: give every string and sequence a capacity before adding the subscription. An
  incoming string longer than its capacity is skipped, not truncated. Example: a
  `geometry_msgs/msg/TwistStamped` subscription (Nav2 on Kilted and Lyrical, `diff_drive_controller`
  setups) needs a buffer behind `header.frame_id`.
- **micro_ros_utilities**: `micro_ros_utilities_create_message_memory(type_support, &msg, conf)`
  sizes everything from a `micro_ros_utilities_memory_conf_t` (defaults: strings 20, sequences 5,
  overridable per field with rules such as `{"header.frame_id", 30}`), using the rcutils allocator;
  `micro_ros_utilities_create_static_message_memory(..., buffer, len)` uses your buffer instead;
  `micro_ros_utilities_get_static_size` tells you how big that buffer must be. These set capacity,
  not size.
- `micro_ros_string_utilities_set(str, "text")` returns the new string: assign it
  (`msg.header.frame_id = micro_ros_string_utilities_set(msg.header.frame_id, "imu_link");`).
- Allocate message memory once, outside the reconnect loop; entities are rebuilt on every
  reconnect, messages need not be.
