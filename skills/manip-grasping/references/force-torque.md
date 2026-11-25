# Force-torque sensing

Part of [manip-grasping](../SKILL.md). A wrist force-torque (F/T) sensor through ros2_control:
the URDF tag, `force_torque_sensor_broadcaster`, filtering, zeroing and gravity compensation.
Checked against ros2_controllers 4.43.1, control_toolbox 4.11.1 (`control_filters`), ros2_control
4.50.0 and gz_ros2_control 1.2.20, all `jazzy`. Not run.

## In the description

The chain should be serial: `tool0` -> `ft_sensor_link` (the sensor's measuring frame, from its
datasheet) -> `gripper_base_link` -> ... -> `tcp`. The admittance controller needs every frame it
uses on one chain from `base_link` to its tip.

```xml
<ros2_control name="wrist_ft" type="sensor">
  <hardware>
    <plugin>my_ft_driver/MyFtSensorHardware</plugin>  <!-- the vendor's or your own plugin -->
    <param name="device">/dev/my_ft_sensor</param>     <!-- udev symlink -->
  </hardware>
  <sensor name="ft_sensor">
    <state_interface name="force.x"/>
    <state_interface name="force.y"/>
    <state_interface name="force.z"/>
    <state_interface name="torque.x"/>
    <state_interface name="torque.y"/>
    <state_interface name="torque.z"/>
    <param name="frame_id">ft_sensor_link</param>
  </sensor>
</ros2_control>
```

- Those six names with the sensor name as prefix are what the `ForceTorqueSensor` semantic
  component (and so the broadcaster and the admittance controller) expects by default.
- Arms with a built-in wrist sensor export it from their own driver; the UR driver, for example,
  calls it `tcp_fts_sensor` and ships a broadcaster for it in its controller YAML.
- **Mock hardware:** `mock_components/GenericSystem` with `<param name="mock_sensor_commands">true</param>`
  adds command interfaces with the sensor's own interface names, so a
  `forward_command_controller` can feed fake readings to test the rest of the chain.
- **Gazebo:** a `force_torque` sensor on the joint plus the world's ForceTorque system; see
  [sim-gazebo](../../sim-gazebo/SKILL.md) (`references/sensors.md`, `references/world.md`).

## The broadcaster

```yaml
# my_robot_bringup/config/controllers.yaml
ft_broadcaster:
  ros__parameters:
    type: force_torque_sensor_broadcaster/ForceTorqueSensorBroadcaster
    sensor_name: ft_sensor        # or interface_names.force.x ... for odd names; not both
    frame_id: ft_sensor_link      # stamped on the messages; required, read-only
    offset:                       # ADDED to each reading; updated live with ros2 param set
      force: {x: 0.0, y: 0.0, z: 0.0}
      torque: {x: 0.0, y: 0.0, z: 0.0}
    sensor_filter_chain:          # optional; adds ~/wrench_filtered
      filter1:
        name: gravity_compensation
        type: control_filters/GravityCompensationWrench
        params:
          world_frame: base_link            # fixed frame where gravity is gravity_field
          sensor_frame: ft_sensor_link      # frame of the CoG below
          tool:
            mass: 0.9                       # example: weigh gripper + adapter + fingers, kg
            CoG: [0.0, 0.0, 0.06]           # example: from CAD, m, in sensor_frame
            gravity_field: [0.0, 0.0, -9.81]   # default
      filter2:
        name: low_pass
        type: control_filters/LowPassFilterWrench
        params:
          sampling_frequency: 500.0         # = controller manager update_rate, Hz
          damping_frequency: 20.5           # control_toolbox test value; tune on a plot
          damping_intensity: 1.25           # control_toolbox test value
```

- Topics: `/ft_broadcaster/wrench` (offset and `multiplier` applied, no filters) and, with a
  chain, `/ft_broadcaster/wrench_filtered`, both `geometry_msgs/msg/WrenchStamped` in `frame_id`.
- The filter plugins live in `control_toolbox` (`ros-jazzy-control-toolbox`, pulled in by
  `ros-jazzy-ros2-controllers`). Each filter's own keys go under `params:`. The control_filters
  Markdown doc still names the gravity keys `CoG.pos` and `CoG.force`; the parameter file in
  4.11.1, used above, has `tool.mass`, `tool.CoG` and `tool.gravity_field`.
- The gravity filter looks up TF from `world_frame` to `sensor_frame` on every update; with no TF
  it passes nothing through and logs "GravityCompensation update failed".
- Plot raw against filtered in [PlotJuggler](../../../wiki/tools/plotjuggler.md) and lower
  `damping_frequency` only until the noise you care about is gone: every filter adds delay to a
  contact you want to stop on.

Express the wrench in another frame with the standalone node shipped in the same package:

```bash
ros2 run force_torque_sensor_broadcaster wrench_transformer_node base_link tcp \
  --ros-args -r ~/wrench:=/ft_broadcaster/wrench_filtered
# publishes /fts_wrench_transformer/base_link/wrench_filtered and .../tcp/wrench_filtered
```

## Zero the sensor

Strain-gauge sensors drift with temperature and after mounting, so zero at the start of each
session and before a delicate task, with nothing in the gripper and the arm still.

```python
#!/usr/bin/env python3
# ft_zero.py: average the compensated wrench, print the offsets that cancel it
import numpy as np
import rclpy
from geometry_msgs.msg import WrenchStamped

rclpy.init()
node = rclpy.create_node('ft_zero')
samples = []


def on_wrench(msg):
    f, t = msg.wrench.force, msg.wrench.torque
    samples.append([f.x, f.y, f.z, t.x, t.y, t.z])


node.create_subscription(WrenchStamped, '/ft_broadcaster/wrench_filtered', on_wrench, 10)
while rclpy.ok() and len(samples) < 500:  # a few seconds at typical rates
    rclpy.spin_once(node, timeout_sec=1.0)
mean = np.mean(samples, axis=0)
names = ['force.x', 'force.y', 'force.z', 'torque.x', 'torque.y', 'torque.z']
for name, value in zip(names, mean):
    print(f'ros2 param set /ft_broadcaster offset.{name} {-value:.4f}')  # add to existing offsets
rclpy.shutdown()
```

Add the printed values to the current offsets (they are added before the filters; with the
gravity filter configured, zeroing the filtered output with the tool attached is valid in any
orientation only if `tool.mass` and `tool.CoG` are right). Without a gravity filter, zero with the
tool pointing straight down and expect errors when it tilts. A sensor with its own tare command
(through the driver) is better: use it, and leave the offsets at zero.

## Checks

- Still arm, nothing held, tool tilted to several orientations: the compensated force stays near
  zero. If it swings with orientation, `tool.mass` is wrong; if only torque swings, `tool.CoG` is.
- Hang or place a known mass on the gripper: the force in `base_link` changes by its weight
  (mass x 9.81 N) along z.
- Press the fingertips by hand along tcp z: `/fts_wrench_transformer/tcp/wrench_filtered` shows the
  force mostly on z with the sign your monitor code expects. Write the sign down.
- `ros2 topic hz /ft_broadcaster/wrench` close to the controller manager's `update_rate`.

The admittance controller reads the sensor's state interfaces directly: the broadcaster's offsets
and filters do not reach it ([admittance.md](admittance.md)).

Sources: ros2_controllers `jazzy` (force_torque_sensor_broadcaster userdoc, parameter YAML,
`force_torque_sensor_broadcaster.cpp`, `wrench_transformer.cpp`, CHANGELOG 4.35.0); control_toolbox
`jazzy` (`control_filters.xml`, `gravity_compensation_filter_parameters.yaml`,
`low_pass_filter_parameters.yaml` and its test file, `doc/control_filters.md`); ros/filters `ros2`
(`filter_chain.hpp`: `filterN.params`); ros2_control `jazzy` (`hardware_interface_types_userdoc.rst`,
`mock_components_userdoc.rst`); Universal_Robots_ROS2_Driver `jazzy` (`ur_controllers.yaml`);
gz_ros2_control `jazzy` docs.
