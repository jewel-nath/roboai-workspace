# Health reporting: diagnostic_updater and diagnostic_aggregator

Part of [ops-bringup](../SKILL.md). Checked against `ros/diagnostics` 4.2 (`ros2-jazzy` branch):
`diagnostic_updater`, `diagnostic_aggregator`, `diagnostic_common_diagnostics`. All BSD-3-Clause,
released for Humble, Jazzy and Lyrical.

Every driver reports its own state on `/diagnostics`; one `aggregator_node` groups the reports and
publishes `/diagnostics_agg` and the single worst level on `/diagnostics_toplevel_state`. Levels:
OK 0, WARN 1, ERROR 2, STALE 3.

## Report from a Python driver

```python
from diagnostic_msgs.msg import DiagnosticStatus
from diagnostic_updater import FrequencyStatusParam, HeaderlessTopicDiagnostic, Updater
from rclpy.node import Node


class LidarDriver(Node):
    def __init__(self):
        super().__init__('lidar')
        self.updater = Updater(self)              # publishes once a second by default
        self.updater.setHardwareID('lidar-front')  # serial number or model of the device
        self.updater.add('Connection', self.check_connection)
        # Rate check on the published scans; bounds are examples for a 10 Hz lidar
        self.scan_diag = HeaderlessTopicDiagnostic(
            'scan', self.updater, FrequencyStatusParam({'min': 9.0, 'max': 11.0}, 0.1, 10))

    def check_connection(self, stat):
        if self.device_open:
            stat.summary(DiagnosticStatus.OK, 'Connected')
        else:
            stat.summary(DiagnosticStatus.ERROR, 'Port closed, reconnecting')
        stat.add('port', self.get_parameter('port').value)
        return stat                               # Python tasks must return the status

    def publish_scan(self, msg):
        self.scan_pub.publish(msg)
        self.scan_diag.tick()                     # once per published message
```

## Report from a C++ driver

```cpp
#include <diagnostic_updater/diagnostic_updater.hpp>
#include <diagnostic_updater/publisher.hpp>

// members
diagnostic_updater::Updater updater_{this};
double min_hz_{9.0}, max_hz_{11.0};               // examples
diagnostic_updater::HeaderlessTopicDiagnostic scan_diag_{
  "scan", updater_, diagnostic_updater::FrequencyStatusParam(&min_hz_, &max_hz_, 0.1, 10)};

// constructor
updater_.setHardwareID("lidar-front");
updater_.add("Connection", this, &LidarDriver::check_connection);

void LidarDriver::check_connection(diagnostic_updater::DiagnosticStatusWrapper & stat)
{
  if (device_open_) {
    stat.summary(diagnostic_msgs::msg::DiagnosticStatus::OK, "Connected");
  } else {
    stat.summary(diagnostic_msgs::msg::DiagnosticStatus::ERROR, "Port closed, reconnecting");
  }
  stat.add("port", port_);
}
```

Add `diagnostic_updater` to the package's dependencies. The updater names each status
`<node name>: <task name>` (`lidar: Connection`, `lidar: scan topic status`); the aggregator
matches on those names. The publishing period is the parameter `diagnostic_updater.period`.

## Already reporting

- `controller_manager` (ros2_control 4.50 on Jazzy) publishes `controller_manager: Controllers Activity`,
  `Hardware Components Activity` and `Controller Manager Activity`.
- `diagnostic_common_diagnostics` monitors the host: `cpu_monitor.py`, `ram_monitor.py`,
  `hd_monitor.py` (parameter `path`, default the home directory; warns under 5 % free, errors under
  1 %), `sensors_monitor.py` (needs `lm-sensors`) and `ntp_monitor.py` ([time-sync.md](time-sync.md)).
  Node names end in the host name, so each computer of the robot reports separately.

## Aggregate

```yaml
# my_robot_bringup/config/diagnostics.yaml
analyzers:                       # the aggregator node is named "analyzers"
  ros__parameters:
    path: my_robot
    pub_rate: 1.0
    drive:
      type: diagnostic_aggregator/GenericAnalyzer
      path: Drive
      startswith: ['controller_manager']
      expected: ['controller_manager: Hardware Components Activity']
    sensors:
      type: diagnostic_aggregator/GenericAnalyzer
      path: Sensors
      startswith: ['lidar', 'imu']
      timeout: 5.0               # seconds without an update before an item turns STALE
    computer:
      type: diagnostic_aggregator/GenericAnalyzer
      path: Computer
      startswith: ['cpu_monitor', 'ram_monitor', 'hd_monitor', 'NTP']
```

```python
# my_robot_bringup/launch/diagnostics.launch.py
from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    config = PathJoinSubstitution(
        [FindPackageShare('my_robot_bringup'), 'config', 'diagnostics.yaml'])
    return LaunchDescription([
        Node(package='diagnostic_aggregator', executable='aggregator_node',
             parameters=[config], output='both'),
        Node(package='diagnostic_common_diagnostics', executable='cpu_monitor.py'),
        Node(package='diagnostic_common_diagnostics', executable='ram_monitor.py'),
        # Free space where the ROS logs grow
        Node(package='diagnostic_common_diagnostics', executable='hd_monitor.py',
             parameters=[{'path': '/var/log/my_robot'}]),
    ])
```

- Match keys: `startswith`, `contains`, `name` (exact), `regex`; `expected` lists names that must be
  present (a missing one is reported); `timeout`, `num_items`, `discard_stale`,
  `find_and_remove_prefix` tune the rest.
- Items no analyzer matches go to an "Other" group and turn stale after 5 s; give every reporting
  node an analyzer.
- `critical: true` makes `/diagnostics_toplevel_state` publish at once when the level gets worse,
  for a supervisor that acts on it. Acting on it (stopping motion) belongs to
  [arch-safety](../../arch-safety/SKILL.md).

## Read it

```bash
ros2 topic echo --once /diagnostics_toplevel_state        # level and message of the worst item
ros2 topic echo /diagnostics_agg --field status --once | grep -E "name|level|message"
ros2 run rqt_robot_monitor rqt_robot_monitor              # tree view, on a computer with a display
```

Foxglove's diagnostics panels read the same topics ([Foxglove](../../../wiki/tools/foxglove.md)).

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| A node's items sit under "Other" and go stale | No analyzer matches its `<node>: <task>` names | Add `startswith` with the node name |
| A driver that never started is simply absent, the tree looks fine | No item exists until something reports | List its status names in `expected`; they show as missing |
| A crashed driver disappears instead of turning STALE | `discard_stale: true` | Keep the default `false` for hardware |
| Warning `No HW_ID was set` | `setHardwareID` never called | Set it, or `'none'` for software-only nodes |
| Python task crashes the updater | Task function returned nothing | `return stat` |
| Analyzer parameters ignored | YAML top key is not `analyzers` (the node's name) | Keep `analyzers: ros__parameters:` |
