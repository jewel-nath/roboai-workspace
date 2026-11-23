# IMU setup for localization

Part of [perception-slam](../SKILL.md). Sources: REP 103, REP 145 (draft, "Conventions for IMU Sensor
Drivers"), robot_localization's `preparing_sensor_data.rst` (3.8.4), and the imu_tools 2.1.6 sources
(`jazzy` branch). The URDF side (the `imu_link` joint) is in
[ros2-robot-description](../../ros2-robot-description/SKILL.md); a simulated IMU is in
[sim-gazebo sensors.md](../../sim-gazebo/references/sensors.md).

## Conventions

- **Topics** (REP 145): `imu/data_raw` (`sensor_msgs/Imu` with acceleration and angular velocity),
  `imu/data` (the same plus `orientation`), `imu/mag` (`sensor_msgs/MagneticField`).
- **Units:** m/s², rad/s, tesla, radians; right-handed axes.
- **Acceleration is specific force.** At rest with the sensor's z axis up, `linear_acceleration.z` reads
  about +9.81, not 0 and not -9.81.
- **Orientation** is the sensor frame relative to a world frame. REP 103 uses ENU (x east, y north, z up);
  robot_localization assumes ENU and does not handle NED data, so convert NED in the driver. Without a
  magnetometer only roll and pitch are referenced (to gravity); yaw is relative to start-up.
- **Covariance:** all zeros means "unknown"; a first element of -1 means the field is not provided (an
  orientation from a 6-axis IMU without a filter, for example). REP 145 suggests driver parameters
  `linear_acceleration_stddev`, `angular_velocity_stddev`, `magnetic_field_stddev` and `orientation_stddev`
  that override what the sensor reports.

## Mounting and frames

- Describe the mount once, as a fixed joint `base_link` → `imu_link` in the URDF with the real rotation, and
  have the driver stamp `header.frame_id: imu_link`. robot_localization, RTAB-Map and the LIO packages rotate
  the data into the base frame through TF.
- Rotate in one place only. If the driver already remaps axes to the robot's, the URDF joint must have no
  rotation; doing both rotates twice.
- A wrong mount rotation shows as gravity on x or y when level, a robot that looks tilted in RViz, or a yaw
  rate with the wrong sign.

## Bring-up tests

| Test | Expect |
|---|---|
| Level, at rest | `linear_acceleration` ≈ (0, 0, +9.81); `angular_velocity` ≈ (0, 0, 0) |
| Rolled +90° (left side up) | `linear_acceleration.y` ≈ +9.81 |
| Pitched +90° (nose down) | `linear_acceleration.x` ≈ -9.81 |
| Turned left (counter-clockwise from above) | `angular_velocity.z` > 0, yaw increases |
| `imu/data` at rest, level | roll and pitch ≈ 0 and steady; yaw steady |
| Rate | steady at the configured rate, no gaps |

The acceleration rows are robot_localization's stated assumptions; the rest follow REP 103.

```bash
ros2 topic echo /imu/data_raw --field linear_acceleration
ros2 topic echo /imu/data_raw --field angular_velocity
ros2 topic hz /imu/data_raw
ros2 topic delay /imu/data_raw          # header stamp versus now: large or growing means a stamping problem
ros2 run tf2_ros tf2_echo base_link imu_link
```

## Orientation filters (imu_tools)

If the driver publishes only `imu/data_raw`, a filter adds the orientation. Both read `imu/data_raw` (and
`imu/mag` when `use_mag` is on) and publish `imu/data`.

| | `imu_complementary_filter` | `imu_filter_madgwick` |
|---|---|---|
| Executable | `complementary_filter_node` | `imu_filter_madgwick_node` |
| Licence | BSD-3-Clause | **GPL-3.0-or-later** |
| `use_mag` default | `false` | `true` |
| `publish_tf` default | `false` | `true`, from `fixed_frame` (default `odom`) to the IMU frame |
| World frame | ENU | `world_frame`: `enu` (default), `nwu`, `ned` |
| Gains | `gain_acc`, `gain_mag`, `do_bias_estimation`, `do_adaptive_gain`, `bias_alpha` | `gain`, `zeta`, `mag_bias_x/y/z`, `declination` |
| `orientation_stddev` default | 0.0 | 0.0 |

- Set `publish_tf: false` on Madgwick when a URDF or a filter already places the IMU frame. Its default
  publishes `odom` → `imu_link`, which gives `imu_link` a second parent and breaks the tree.
- Set `orientation_stddev`; at 0 the output orientation covariance is zero and robot_localization treats
  it as near-perfect.
- Keep Madgwick's `remove_gravity_vector` at its default `false` when robot_localization removes gravity
  (`imu0_remove_gravitational_acceleration: true`); removing it twice leaves an error of g.
- Shipping a product: the Madgwick package is GPL-3.0-or-later; the complementary filter is BSD.

```python
# in my_robot_localization/launch/imu.launch.py
from launch_ros.actions import Node

imu_filter = Node(
    package='imu_complementary_filter', executable='complementary_filter_node', name='imu_filter',
    parameters=[{'use_mag': False, 'publish_tf': False, 'do_bias_estimation': True,
                 'orientation_stddev': 0.05}],          # example: measure it (below)
    remappings=[('imu/data_raw', '/imu/data_raw'), ('imu/data', '/imu/data')])
```

## Magnetometers and heading

- Indoors, steel structure and motors bend the field. Fuse the yaw rate, not the yaw.
- Outdoors, navsat_transform needs an earth-referenced heading. Calibrate hard and soft iron (Madgwick takes
  `mag_bias_x/y/z`), set the declination, and check that yaw reads 0 facing east (ENU) before trusting it.
  A dual-antenna GNSS heading avoids the magnetometer altogether.

## Measuring noise

- **Covariances for the filter:** record a minute or more at rest, take the standard deviation of each axis,
  and set the driver's `*_stddev` parameters (or the covariance diagonals) from it. These are the sensor's
  measurement noise; they do not belong in robot_localization's `initial_estimate_covariance`, which is the
  filter's starting uncertainty.
- **Noise densities and random walks** for VIO, LIO and Kalibr come from an Allan-variance analysis of a long
  static recording: [vio-calibration.md](vio-calibration.md).

## Time stamps

VIO and LIO fail first on bad stamps. Prefer a driver that stamps with device time synchronized to the host;
a driver that stamps on reception adds USB or serial jitter. `ros2 topic delay` and the dt plot in Kalibr's
report show both.
