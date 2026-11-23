# robot_localization: local and global filters, GPS

Part of [perception-slam](../SKILL.md). Checked against robot_localization 3.8.4 (`jazzy-devel`): the
package docs (`state_estimation_nodes.rst`, `preparing_sensor_data.rst`, `navsat_transform_node.rst`,
`integrating_gps.rst`), its example parameter and launch files, and the node sources.

## Nodes

| Executable | Does | Output |
|---|---|---|
| `ekf_node` | Extended Kalman filter, 15-state omnidirectional model | `odometry/filtered`; TF `odom` → `base_link`, or `map` → `odom` when `world_frame` is `map` |
| `ukf_node` | Unscented filter, same parameters plus `alpha`, `kappa`, `beta` (keep the defaults); more CPU | same |
| `navsat_transform_node` | Turns `sensor_msgs/NavSatFix` into odometry in the filter's world frame | `odometry/gps`, optional `gps/filtered` |

The docs still say `ekf_localization_node`; the ROS 2 executables are `ekf_node` and `ukf_node`. Each node
reads the YAML block under the `name=` it gets in the launch file. Inputs are subscribed with the sensor-data
QoS profile, so reliable and best-effort publishers both connect.

## The `_config` vector

Each input (`odomN`, `twistN`, `poseN`, `imuN`, numbered from 0 without gaps) has a 15-boolean `<input>_config`:

```text
x, y, z, roll, pitch, yaw, vx, vy, vz, vroll, vpitch, vyaw, ax, ay, az
```

The booleans refer to the sensor's own frames: pose data in `header.frame_id`, twist data in
`child_frame_id`. The filter moves every measurement into `world_frame` (pose) or `base_link_frame`
(velocity) through TF, so every sensor frame must be in the TF tree.

## What to fuse

| Source | Fuse | Reason |
|---|---|---|
| Wheel odometry (`diff_drive_controller`) | vx, vy, vyaw | Its pose is integrated velocity. vy = 0 is a true constraint on a differential base |
| IMU, no trusted heading | vroll, vpitch, vyaw; roll, pitch in 3D | Integrated gyro yaw drifts; it is not absolute |
| IMU with a trusted earth-referenced heading | add yaw | navsat_transform needs it outdoors |
| IMU acceleration | ax (ay, az) only after the gravity test in [imu.md](imu.md) | A bad gravity removal pushes the estimate at rest |
| Visual or lidar odometry that gives a pose only | x, y, yaw with `_differential: true` | Two absolute pose sources fight unless both covariances are right |
| GPS through navsat_transform (map filter only) | x, y (z if `zero_altitude: false`) | Keep `_differential: false` for it |
| SLAM or AMCL pose (map filter only) | x, y, yaw | |

Rules from the package docs:

- **Covariances matter.** Do not inflate a variance to make the filter ignore a value; set its `_config`
  entry to `false`. A fused value with zero variance gets 1e-6 added, so it dominates the estimate.
- **Two absolute yaw sources** (wheel odometry pose and an IMU, for example): fuse the better one, and give
  the other `_differential: true` or fuse its rate instead.
- `_differential: true` turns pose into velocity; that state's covariance then grows without bound unless
  another absolute source exists. `_relative: true` only starts the input at zero.
- `two_d_mode: true` fuses 0 for z, roll, pitch and their rates. Use it for ground robots on flat floors.
- `process_noise_covariance` (Q) and `initial_estimate_covariance` (P0) take 15 diagonal values or a full
  225-value matrix. Keep the defaults until everything else works. A larger Q relative to a measurement's
  variance makes the filter follow that measurement faster; a tiny P0 entry for a value that is measured with
  large variance makes the filter slow to trust it.
- **Outliers:** `odomN_pose_rejection_threshold`, `odomN_twist_rejection_threshold`,
  `poseN_rejection_threshold`, `twistN_rejection_threshold`, `imuN_pose_rejection_threshold`,
  `imuN_twist_rejection_threshold` and `imuN_linear_acceleration_rejection_threshold` are Mahalanobis
  distances; unset means no rejection. Use these, not a hand-written filter.
- **Late inputs** (scan-matcher poses that arrive after newer data): `smooth_lagged_data: true` and
  `history_length` at least as long as the lag.
- `print_diagnostics: true` reports problems on `/diagnostics`. `publish_tf: false` when another node owns
  the edge.

## Local filter (odom → base_link)

`my_robot_localization/config/ekf.yaml`, for a differential-drive robot with an IMU and no magnetometer:

```yaml
ekf_filter_node:
  ros__parameters:
    frequency: 30.0
    sensor_timeout: 0.1
    two_d_mode: true
    publish_tf: true
    print_diagnostics: true
    map_frame: map
    odom_frame: odom
    base_link_frame: base_link            # base_footprint if that is the URDF root
    world_frame: odom

    odom0: /diff_drive_controller/odom    # enable_odom_tf: false in the controller
    odom0_config: [false, false, false,
                   false, false, false,
                   true,  true,  false,
                   false, false, true,
                   false, false, false]
    odom0_queue_size: 10

    imu0: /imu/data
    imu0_config: [false, false, false,
                  false, false, false,    # yaw only with a trusted absolute heading
                  false, false, false,
                  false, false, true,
                  false, false, false]    # ax only after the gravity test
    imu0_queue_size: 20
    imu0_remove_gravitational_acceleration: true
```

```python
# my_robot_localization/launch/ekf.launch.py
from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    params = PathJoinSubstitution([FindPackageShare('my_robot_localization'), 'config', 'ekf.yaml'])
    return LaunchDescription([
        Node(package='robot_localization', executable='ekf_node', name='ekf_filter_node',
             output='screen', parameters=[params, {'use_sim_time': False}]),
    ])
```

## Two filters and GPS

The package's recommended outdoor layout: a local filter fuses only continuous data in `odom`; a global
filter fuses the same raw inputs plus GPS in `map`; `navsat_transform_node` converts fixes using the global
filter's output and an earth-referenced IMU heading. Feed both filters the raw sensors. Do not fuse the
local filter's output into the global one.

```yaml
# my_robot_localization/config/dual_ekf_navsat.yaml
ekf_filter_node_odom:
  ros__parameters:
    frequency: 30.0
    two_d_mode: true
    world_frame: odom
    odom0: /diff_drive_controller/odom
    odom0_config: [false, false, false,  false, false, false,  true, true, false,
                   false, false, true,   false, false, false]
    imu0: /imu/data
    imu0_config: [false, false, false,  false, false, true,  false, false, false,
                  false, false, true,   false, false, false]
    imu0_remove_gravitational_acceleration: true

ekf_filter_node_map:
  ros__parameters:
    frequency: 30.0
    two_d_mode: true
    world_frame: map
    odom0: /diff_drive_controller/odom
    odom0_config: [false, false, false,  false, false, false,  true, true, false,
                   false, false, true,   false, false, false]
    odom1: odometry/gps
    odom1_config: [true, true, false,  false, false, false,  false, false, false,
                   false, false, false,  false, false, false]
    odom1_differential: false
    imu0: /imu/data
    imu0_config: [false, false, false,  false, false, true,  false, false, false,
                  false, false, true,   false, false, false]
    imu0_remove_gravitational_acceleration: true

navsat_transform:
  ros__parameters:
    frequency: 30.0
    delay: 3.0
    magnetic_declination_radians: 0.0     # your site's declination, in radians
    yaw_offset: 0.0                       # the IMU must read 0 facing east; pi/2 if it reads 0 facing north
    zero_altitude: true
    broadcast_cartesian_transform: false
    publish_filtered_gps: true
    use_odometry_yaw: false
    wait_for_datum: false
```

Here the IMU yaw is fused because outdoors it comes from a calibrated magnetometer or GNSS heading; without
one, fuse only vyaw and give navsat_transform a datum instead (below).

```python
# my_robot_localization/launch/dual_ekf_navsat.launch.py
from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    params = PathJoinSubstitution(
        [FindPackageShare('my_robot_localization'), 'config', 'dual_ekf_navsat.yaml'])
    return LaunchDescription([
        Node(package='robot_localization', executable='ekf_node', name='ekf_filter_node_odom',
             parameters=[params], remappings=[('odometry/filtered', 'odometry/local')]),
        Node(package='robot_localization', executable='ekf_node', name='ekf_filter_node_map',
             parameters=[params], remappings=[('odometry/filtered', 'odometry/global')]),
        Node(package='robot_localization', executable='navsat_transform_node',
             name='navsat_transform', parameters=[params],
             remappings=[('imu', '/imu/data'), ('gps/fix', '/gps/fix'),
                         ('odometry/filtered', 'odometry/global')]),
    ])
```

navsat_transform details:

- It subscribes to `imu` (not `imu/data`), `gps/fix` and `odometry/filtered`; remap all three. It does
  nothing until it has a fix, a heading and an odometry message.
- The datum (where the world frame sits on Earth) comes from the first fix by default. For a fixed origin, set
  `wait_for_datum: true` and `datum: [lat_deg, lon_deg, yaw_rad]`, or call the `datum` service
  (`robot_localization/srv/SetDatum`, a `geographic_msgs/GeoPose`).
- `broadcast_cartesian_transform` replaces `broadcast_utm_transform` (still read, with a deprecation warning)
  and publishes a `utm` frame under the world frame; `use_local_cartesian: true` uses a local tangent plane
  instead of UTM.
- `fromLL` and `toLL` services convert between latitude/longitude and the world frame, for GPS waypoints.

## Resetting and checking

```bash
ros2 topic pub --once /set_pose geometry_msgs/msg/PoseWithCovarianceStamped \
  "{header: {frame_id: odom}, pose: {pose: {orientation: {w: 1.0}}}}"
ros2 service call /reset std_srvs/srv/Empty      # back to the uninitialized state
ros2 topic echo /diagnostics                     # with print_diagnostics: true
```

`set_pose` is both a topic and a service (`robot_localization/srv/SetPose`), relative to the node's namespace.
With bags in simulated time, `reset_on_time_jump: true` resets the filter when the bag loops.

**Lyrical:** robot_localization 3.11 makes `ekf_node` and `ukf_node` lifecycle nodes that start
unconfigured. Launch them with `launch_ros.actions.LifecycleNode(package='robot_localization',
executable='ekf_node', name='ekf_filter_node', namespace='', autostart=True, parameters=[params])`, or
configure and activate them with `ros2 lifecycle set`.
