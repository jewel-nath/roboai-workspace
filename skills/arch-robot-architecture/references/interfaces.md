# Interfaces between layers: kinds, types, names, QoS and health (Jazzy)

Part of [arch-robot-architecture](../SKILL.md). This file is about choosing interfaces; how to write
publishers, servers and clients, and how to build an interface package, is in
[ros2-core](../../ros2-core/SKILL.md) and its [packages.md](../../ros2-core/references/packages.md).

## Which kind of interface

| Kind | Use it for | Examples | Not for |
|---|---|---|---|
| Topic | Streams and current state, any number of readers | `scan`, `odom`, `joint_states`, `battery_state`, `mode` | Commands that must be acknowledged |
| Service | A call that returns at once | switch mode, enable a device, reset a counter, save a map | Anything that moves the robot or takes time |
| Action | A goal that takes time, reports progress, can fail midway or be cancelled | navigate, dock, pick, run a mission | Streaming data |
| Parameter | Configuration, read at start or changed rarely | speeds, limits, frame and topic names | State that changes while running |

A server must answer quickly (a slow handler holds up its own executor), and a call made inside a callback
must be asynchronous. Anything slow is an action.

## Standard types first

| Data | Type |
|---|---|
| Velocity command to a Jazzy `ros2_controllers` base | `geometry_msgs/msg/TwistStamped` |
| Odometry | `nav_msgs/msg/Odometry` |
| Joint positions, velocities, efforts | `sensor_msgs/msg/JointState` |
| Battery | `sensor_msgs/msg/BatteryState` |
| Health | `diagnostic_msgs/msg/DiagnosticArray` (through `diagnostic_updater`, below) |
| On/off switch; one-shot command | `std_srvs/srv/SetBool`; `std_srvs/srv/Trigger` |
| Go to a pose | `nav2_msgs/action/NavigateToPose` |
| Arm trajectory | `control_msgs/action/FollowJointTrajectory` |
| Gripper | `control_msgs/action/ParallelGripperCommand` or `GripperCommand` |

Standard types work with RViz, Foxglove, rosbag tooling and other people's nodes without extra code.
Define your own only for what has no standard type: the robot's modes, a mission, a device's own status.

## Custom interfaces worth defining

In `my_robot_interfaces` (build files in ros2-core):

```text
# msg/RobotMode.msg - published latched on ~/mode by the behavior layer
uint8 MANUAL=0
uint8 AUTONOMOUS=1
uint8 DOCKING=2
uint8 FAULT=3

builtin_interfaces/Time stamp
uint8 mode            # one of the constants above
string reason         # why it last changed, for the operator
```

```text
# srv/SetMode.srv
uint8 mode            # a RobotMode constant
---
bool success
string message        # why a change was refused
```

```text
# action/RunMission.action
string mission_id
geometry_msgs/PoseStamped[] waypoints
---
bool success
string message
---
uint32 current_waypoint
string current_step
```

Design rules:

- **Typed, not strings.** Modes and events as `std_msgs/String` fail silently on a typo and cannot be checked
  by `ros2 interface show`. Use constants in a message.
- **State latched, commands acknowledged.** Publish the current mode with transient-local durability so a node
  that starts late still gets it. Request a mode change through a service that can refuse it, not by
  publishing on a topic and hoping someone listens.
- **Units and frames in the definition.** Comment every field with its unit; carry a `header` (or stamp
  and frame) on anything spatial or time-sensitive.
- **Change with care.** Any change to a definition, even an added field, changes what goes on the wire, so
  every node and recorded bag using it must move together; rename or remove fields only with a plan.

## Names

- In node code, use relative names (`scan`, `cmd_vel`) or private ones (`~/mode`); remap in launch. An
  absolute name (`/scan`) ignores the node's namespace and breaks the second robot.
- Keep the conventional names other packages expect: `cmd_vel`, `odom`, `scan`, `imu/data`,
  `joint_states`, `robot_description`, `map`, `tf`, `tf_static`.
- Libraries that publish absolute names: tf2 (`/tf`, `/tf_static`), `diagnostic_updater` and
  `diagnostic_aggregator` (`/diagnostics`, `/diagnostics_agg`). Remap them per robot when namespacing
  ([multi-robot.md](multi-robot.md)).

## QoS by kind of data

API detail and the compatibility rules are in [ros2-core](../../ros2-core/SKILL.md) step 3.

| Data | Examples | Reliability | Durability | History |
|---|---|---|---|---|
| High-rate sensor streams | `scan`, `image_raw`, `points`, `imu/data` | best effort (`SensorDataQoS`) | volatile | keep last 5 |
| Commands | `cmd_vel`, `joint_trajectory` | reliable | volatile | keep last, small depth |
| State | `odom`, `joint_states`, `battery_state` | reliable | volatile | keep last 10 |
| Latched values | `robot_description`, `map`, `~/mode` | reliable | transient local | keep last 1 |
| TF | `/tf` (tf2_ros broadcaster) / `/tf_static` | reliable | volatile / transient local | 100 / 1 |
| Diagnostics | `/diagnostics` from `diagnostic_updater` | reliable | volatile | keep last 1 |
| Video to a remote operator | compressed images | best effort | volatile | keep last 1 ([ros2-web-bridge](../../ros2-web-bridge/SKILL.md)) |

- Sensor drivers usually publish best effort; a reliable subscriber to them gets nothing. Subscribe to
  sensors with `SensorDataQoS`, which accepts both.
- Both ends of a latched topic must be transient local.
- `deadline` and `liveliness` QoS can report a publisher that went quiet; what the robot does then is a
  safety decision ([arch-safety](../../arch-safety/SKILL.md)).

## Timestamps and frames

Stamp sensor data when it was captured (the driver's or device's time, converted to the node clock), not
when it was processed, and set `frame_id` to a frame that exists in TF. Use the node's clock (`now()`), so
`use_sim_time` works. Fusion, TF lookups and bag replay all depend on it.

## Health: `diagnostic_updater` and `diagnostic_aggregator`

Each driver reports its own state; the aggregator groups them for the operator. Both are in
`ros-jazzy-diagnostics` (4.2.7, BSD-3-Clause per its packages).

```python
# in a driver node (rclpy); seconds_since_last_scan() and scan_count are the driver's own
from diagnostic_msgs.msg import DiagnosticStatus
from diagnostic_updater import Updater
from rclpy.node import Node


class LidarDriver(Node):
    def __init__(self):
        super().__init__('lidar_driver')
        self.updater = Updater(self)            # publishes every diagnostic_updater.period (default 1.0 s)
        self.updater.setHardwareID('lidar_front')
        self.updater.add('stream', self.check_stream)

    def check_stream(self, stat):
        if self.seconds_since_last_scan() > 0.5:    # example limit: a few scan periods
            stat.summary(DiagnosticStatus.ERROR, 'no scans')
        else:
            stat.summary(DiagnosticStatus.OK, 'streaming')
        stat.add('scans', str(self.scan_count))
        return stat
```

The status name becomes `lidar_driver: stream`. Group statuses by name for the operator view:

```yaml
# my_robot_bringup/config/analyzers.yaml
/**/analyzers:
  ros__parameters:
    path: MyRobot
    sensors:
      type: diagnostic_aggregator/GenericAnalyzer
      path: Sensors
      contains: ['lidar_driver', 'camera_driver', 'imu_driver']
    base:
      type: diagnostic_aggregator/GenericAnalyzer
      path: Base
      contains: ['controller_manager']
```

Check: `ros2 topic echo /diagnostics_agg --once` lists every group; `ros2 run rqt_robot_monitor
rqt_robot_monitor` shows the tree; unplugging the lidar turns `Sensors` to ERROR.

Sources: docs.ros.org Jazzy (topics, services and actions; QoS; custom interfaces), `common_interfaces`
and `control_msgs` `jazzy` branches, `geometry2` `tf2_ros/qos.hpp`, `diagnostics` `ros2-jazzy` branch
(`diagnostic_updater`, `diagnostic_aggregator` README and example analyzers).
