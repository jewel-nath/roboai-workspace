# Lidar and lidar-inertial odometry: KISS-ICP, LIO-SAM, RKO-LIO

Part of [perception-slam](../SKILL.md). Checked against KISS-ICP `main` (ROS wrapper 1.3.0, commit
1ffa7d7), LIO-SAM `ros2` (commit 08af3f3, February 2025; one more fix landed 2026-11-19), the RKO-LIO README, and `ros/rosdistro`. Lidar
drivers, point-cloud filtering and the per-point time field belong to
[perception-lidar](../../perception-lidar/SKILL.md).

| | KISS-ICP | LIO-SAM | RKO-LIO |
|---|---|---|---|
| Sensors | 3D lidar (any) | 3D lidar + 9-axis IMU | 3D lidar + IMU |
| Output | odometry only, no loop closure | odometry, map, loop closure, optional GPS | odometry only |
| Jazzy binary | no, build from source | no, build from source | `ros-jazzy-rko-lio` |
| Upstream tested on | Humble, Jazzy, Kilted, Rolling (CI) | Foxy, Galactic, Humble (README) | Humble, Jazzy, Kilted, Lyrical, Rolling (README) |
| Licence | MIT | BSD-3-Clause | MIT |

For loop closure on top of an odometry-only system, feed it to RTAB-Map's lidar mode
([rtabmap.md](rtabmap.md)) as the `odom` input.

## Who owns `odom`

Each of these can publish TF. Decide first:

- **The lidar odometry is the robot's odometry** (no wheels, or wheels you do not trust): it publishes
  `odom` → `base_link`, and nothing else does.
- **Wheel odometry or the EKF owns `odom`**: the lidar odometry publishes no TF (or a separate frame), and
  its pose goes into the local EKF as `odom1` with `odom1_differential: true`
  ([robot-localization.md](robot-localization.md)).

## KISS-ICP

```bash
cd ~/ros2_ws/src && git clone https://github.com/PRBonn/kiss-icp.git
cd ~/ros2_ws && colcon build --packages-select kiss_icp   # fetches the core library at build time
source install/setup.bash
ros2 launch kiss_icp odometry.launch.py topic:=/points use_sim_time:=false visualize:=false \
  base_frame:=base_link lidar_odom_frame:=odom invert_odom_tf:=false
```

- The launch file defaults to **`use_sim_time:=true`** (made for bags). On a live robot pass `false`.
- Output: `kiss/odometry` (`nav_msgs/Odometry`, pose only, diagonal covariance from
  `position_covariance` and `orientation_covariance`, default 0.1 each); debug clouds on `kiss/frame`,
  `kiss/keypoints` and `kiss/local_map` when `visualize` is on. Service `reset` (`std_srvs/srv/Empty`)
  clears the map.
- TF defaults: `lidar_odom_frame: odom_lidar`, `invert_odom_tf: true`, which publishes `base_frame` →
  `odom_lidar` so the tree stays valid next to another `odom` owner. The command above makes KISS-ICP own
  `odom` → `base_link` instead. With `base_frame` empty the pose is the lidar's own.
- Deskewing (`data.deskew`) needs a per-point time field named `t`, `timestamp`, `time_stamp` or `time`.
- Algorithm parameters go in a YAML passed as `config_file:=` under the node name `kiss_icp_node`
  (`data.max_range`, `data.min_range`, `data.deskew`, `mapping.voxel_size`, default `max_range / 100`,
  `mapping.max_points_per_voxel`, `adaptive_threshold.*`, `registration.*`). ROS parameters set in that
  file override the launch arguments.
- Without ROS: `pip install kiss-icp` gives `kiss_icp_pipeline`, which reads datasets and bags directly,
  handy for a first look at a recording.

## LIO-SAM (ROS 2 branch)

Build from source; upstream has not tested it on Jazzy, so expect to fix the build:

```bash
sudo apt install ros-jazzy-gtsam ros-jazzy-perception-pcl ros-jazzy-pcl-msgs \
  ros-jazzy-vision-opencv ros-jazzy-xacro
cd ~/ros2_ws/src && git clone --branch ros2 https://github.com/TixiaoShan/LIO-SAM.git
cd ~/ros2_ws && colcon build --packages-select lio_sam
ros2 launch lio_sam run.launch.py params_file:=/path/to/my_lio_sam.yaml
```

The README installs GTSAM 4.1 from the borglab PPA; Jazzy's rosdistro has `gtsam` 4.2.0. Check the argument
name with `ros2 launch lio_sam run.launch.py --show-args` before relying on it.

Sensor requirements (README):

- **A 9-axis IMU** giving roll, pitch and yaw; the README recommends at least 200 Hz and says the 6-axis IMU
  inside Ouster lidars does not work.
- **Per-point relative time** in the cloud, in a field named `time`, from 0 to the sweep period.
- **IMU-to-lidar extrinsics** in the parameter file: `extrinsicRot` rotates gyro and accelerometer data into
  the lidar frame, `extrinsicRPY` rotates the IMU orientation (they differ when the IMU reports them in
  different axes), `extrinsicTrans` is the offset.

Parameters to check in a copy of `config/params.yaml` (top key `/**:`): `pointCloudTopic`, `imuTopic`,
`gpsTopic` (navsat odometry), `lidarFrame`, `baselinkFrame`, `odometryFrame`, `mapFrame`, `sensor`
(`velodyne`, `ouster`, `livox`), `N_SCAN`, `Horizon_SCAN`, the IMU noise values (`imuAccNoise`,
`imuGyrNoise`, `imuAccBiasN`, `imuGyrBiasN` from an Allan-variance run, see
[vio-calibration.md](vio-calibration.md)), `loopClosureEnableFlag`, `useImuHeadingInitialization` (true with
GPS).

Traps:

- `run.launch.py` also starts a static `map` → `odom` publisher and a `robot_state_publisher` on the
  package's own `config/robot.urdf.xacro`. On a real robot, write your own launch file with the four
  `lio_sam_*` nodes and your robot's description.
- Saving deletes first. Both `savePCD: true` (on exit, into `savePCDDirectory`) and the save service run
  `rm -r` on `$HOME` + the given directory before writing. Point them at a dedicated, empty folder:
  `ros2 service call /lio_sam/save_map lio_sam/srv/SaveMap
  "{resolution: 0.2, destination: /lio_sam_maps/run1}"` writes to `~/lio_sam_maps/run1`.
- Base frame jumping up and down at start: wrong IMU extrinsics (gravity with the wrong sign). Zigzag
  motion: lidar and IMU stamps not in sync (README troubleshooting).

## RKO-LIO

```bash
sudo apt install ros-jazzy-rko-lio
ros2 launch rko_lio odometry.launch.py autodetect:=false \
  imu_topic:=/imu/data lidar_topic:=/points base_frame:=base_link
ros2 launch rko_lio odometry.launch.py -s     # all arguments
```

It reads the IMU-to-lidar extrinsic from TF, so the URDF must place both sensors. It also runs without ROS
on bags (`pip install rko_lio rosbags`). It does odometry only; the same group's `rko_slam` adds loop
closure.

## Checks

- One owner of `odom` → `base_link` (`ros2 topic info -v /tf`).
- Driving a closed loop, the end pose returns near the start; compare runs with evo
  ([bags-evaluation.md](bags-evaluation.md)) rather than by eye.
- Standing still, the pose does not creep. Creep with an IMU points to wrong extrinsics or noise values.
- In the cloud, walls stay thin while turning (deskewing works) and the local map does not smear.
