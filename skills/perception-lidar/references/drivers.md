# Lidar drivers on Jazzy

Part of [perception-lidar](../SKILL.md): the driver for common 2D and 3D lidars, how to start it, the
frame and topic it uses, and the QoS it publishes with. Binary releases checked in rosdistro
`jazzy/distribution.yaml` on 2026-11-19; topics, frames and QoS read from each driver's source.

## Pick the driver

| Sensor | Jazzy package | Topic, message | Default frame | Publisher QoS |
|---|---|---|---|---|
| Slamtec RPLIDAR A1, A2, A3, S1 | `ros-jazzy-rplidar-ros` 2.1.0 (SDK 1.12) | `/scan`, LaserScan | `laser_frame` (its launch file sets `laser`) | reliable, depth 10 |
| Slamtec RPLIDAR C1, S2, S3, T1 | source: Slamtec `rplidar_ros`, branch `ros2` (2.1.4, SDK 2.0) | `/scan`, LaserScan | `laser` | reliable, depth 10 |
| Hokuyo URG, UST | `ros-jazzy-urg-node` 1.1.2 | `/scan`, LaserScan | `laser` | reliable, depth 20 |
| SICK (TiM, LMS, multiScan, picoScan, ...) | `ros-jazzy-sick-scan-xd` 3.10.0 | per launch file | per launch file | check `ros2 topic info -v` |
| Velodyne VLP-16, VLP-32C, VLS-128 | `ros-jazzy-velodyne` 2.5.1 | `/velodyne_points`, PointCloud2; `/scan` | `velodyne` | reliable, depth 10 |
| Ouster OS0, OS1, OS2 | `ros-jazzy-ouster-ros` 0.15.1 | `/ouster/points`, `/ouster/imu`, `/ouster/scan` | `os_sensor`; clouds in `os_lidar` | best effort (sensor data) |
| Hesai Pandar, XT, QT, AT128 | `ros-jazzy-nebula` 1.5.0 (`nebula_hesai`) | `/pandar_points`, PointCloud2 | `hesai` | best effort, depth 10 |
| RoboSense | `ros-jazzy-rslidar-sdk`, or `nebula_robosense` | see the package README | | |
| Livox MID-360, HAP, Avia2 | none: build Livox-SDK2 and `livox_ros_driver2` | `/livox/lidar`, `/livox/imu` | `livox_frame` | reliable |

- `ros2_ouster_drivers` (the older community Ouster driver) has no Jazzy binary; use `ouster_ros`. Its
  `driver_launch.py` keeps the old topic names for migration.
- Hesai's own driver, `HesaiLidar_ROS_2.0`, is source-only (`ros2 launch hesai_ros_driver start.py`,
  frame `hesai_lidar`). `nebula` is Autoware's multi-vendor driver (Apache-2.0) and has the binary.
- The QoS column matters downstream: a reliable subscriber (RViz's default) gets nothing from a
  best-effort publisher. Subscribe with the sensor-data profile, which accepts both.

## Serial 2D lidars

```bash
sudo usermod -aG dialout $USER          # access /dev/ttyUSB*; log out and back in
ls -l /dev/serial/by-id/                # stable names that survive replugging
```

Use the `/dev/serial/by-id/...` path, or a udev rule (`rplidar_ros` ships one in `scripts/`), so two
USB devices cannot swap `/dev/ttyUSB0` and `/dev/ttyUSB1`.

**RPLIDAR from the Jazzy binary** (A-series, S1). The shipped `rplidar.launch.py` hard-codes its
parameters, so run the node directly:

```bash
ros2 run rplidar_ros rplidar_composition --ros-args \
  -p serial_port:=/dev/serial/by-id/usb-Silicon_Labs_CP2102_...-port0 \
  -p serial_baudrate:=115200 -p frame_id:=lidar_link -p angle_compensate:=true
```

Baud rates: 115200 for A1 and A2 in the shipped launch file, 256000 for A3; S1 uses its own launch
file. Other parameters: `inverted`, `flip_x_axis`, `scan_mode`, `topic_name`, `auto_standby`,
`channel_type` (`serial` or `tcp`).

**RPLIDAR C1, S2, S3, T1.** The binary's 1.12 SDK predates them; Slamtec's `ros2` branch has SDK 2.0
and one launch file per model, with launch arguments:

```bash
cd ~/ros2_ws/src && git clone -b ros2 https://github.com/Slamtec/rplidar_ros.git
cd ~/ros2_ws && colcon build --packages-select rplidar_ros && source install/setup.bash
ros2 launch rplidar_ros rplidar_c1_launch.py serial_port:=/dev/ttyUSB0 frame_id:=lidar_link
```

The source package has the same name as the binary and overlays it; do not install both into one
workspace chain without knowing which one runs (`ros2 pkg prefix rplidar_ros`).

**Hokuyo.** The `urg_node` launch file on the Jazzy branch still passes `node_executable=`, which
Jazzy's launch_ros no longer accepts, and names an executable that does not exist. Run the node
with its parameter file instead:

```bash
ros2 run urg_node urg_node_driver --ros-args \
  --params-file $(ros2 pkg prefix urg_node)/share/urg_node/launch/urg_node_ethernet.yaml \
  -p ip_address:=192.168.0.10 -p laser_frame_id:=lidar_link
```

`urg_node_serial.yaml` holds the serial variant (`serial_port`, `serial_baud`).

## Ethernet 3D lidars

Ethernet lidars stream UDP to the host. Give the host NIC a static address in the sensor's subnet,
open the UDP ports in any firewall, and use a wired link: dropped packets show up as missing wedges
in the cloud. Ouster's repo has `util/network-configure.bash` to raise the receive buffers.

**Velodyne.** One launch file per model starts the driver (`velodyne_packets`), the transform node
(`velodyne_points`) and the laserscan node (`scan`):

```bash
ros2 launch velodyne velodyne-all-nodes-VLP16-launch.py
```

The launch files take no arguments; they read
`velodyne_driver/config/<MODEL>-velodyne_driver_node-params.yaml` (`device_ip` 192.168.1.201,
`port` 2368, `frame_id` velodyne, `rpm`) and the matching `velodyne_transform_node` file
(`min_range`, `max_range`, `organize_cloud: true`). To change the frame or IP, copy the launch file
and both YAML files into `my_robot_bringup`. Clouds carry `x y z intensity ring time`; organized
clouds keep NaN points, so `is_dense` is false.

**Ouster.**

```bash
ros2 launch ouster_ros sensor.launch.xml sensor_hostname:=os-122201000123.local
ros2 launch ouster_ros driver.launch.py params_file:=/path/to/driver_params.yaml   # Python form
```

Parameters (`ouster_ros/config/driver_params.yaml`): `sensor_hostname` (required), `lidar_mode`
(`1024x10`, `2048x10`, ...), `timestamp_mode`, `sensor_frame` (`os_sensor`), `lidar_frame`
(`os_lidar`), `imu_frame` (`os_imu`), `point_cloud_frame` (`os_lidar` by default), `pub_static_tf`
(true), `use_system_default_qos` (false means best effort), `point_type` (`original` gives
`x y z intensity t reflectivity ring ambient range`, with `t` in ns). The driver itself broadcasts
`os_sensor` → `os_lidar` and `os_sensor` → `os_imu` from the sensor's metadata, so the URDF stops
at `os_sensor`. Leave `timestamp_mode` empty and stamps come from the sensor's internal clock;
set `TIME_FROM_ROS_TIME`, or `TIME_FROM_PTP_1588` with PTP running, so stamps match the robot's
clock.

**Hesai through nebula.**

```bash
ros2 launch nebula nebula_launch.py sensor_model:=Pandar40P
```

Each model has `nebula_hesai/config/<model>.param.yaml` (`sensor_ip` 192.168.1.201, `host_ip`,
`frame_id` hesai, `return_mode`, `rotation_speed`); pass your copy with `config_file:=`. Nebula's
optional Agnocast zero-copy mode needs a kernel module and is off unless built with
`ENABLE_AGNOCAST=1`.

**Livox (source only).** Build and install Livox-SDK2 first (its README), then:

```bash
git clone https://github.com/Livox-SDK/livox_ros_driver2.git ~/ws_livox/src/livox_ros_driver2
cd ~/ws_livox/src/livox_ros_driver2 && source /opt/ros/jazzy/setup.sh && ./build.sh jazzy
ros2 launch livox_ros_driver2 rviz_MID360_launch.py      # msg_MID360_launch.py for CustomMsg
```

The clone must sit in `<ws>/src/` or `build.sh` fails. The launch file sets `xfer_format` (0:
PointCloud2 with `x y z intensity tag line timestamp`; 1: Livox `CustomMsg`, which many lidar SLAM
packages read; 2: plain PCL XYZI), `frame_id` (`livox_frame`), `publish_freq` and
`user_config_path`, a JSON file with the host and lidar IPs (`config/MID360_config.json`). Edit the
JSON to match your network. The driver is MIT-licensed (its bundled RapidJSON too).

## Recording

```bash
ros2 bag record -o lidar_run /scan /ouster/points /ouster/imu /tf /tf_static
```

Jazzy records to MCAP by default and matches each publisher's QoS. Always record `/tf` and
`/tf_static`, or the bag cannot be transformed later. 3D clouds make large bags; record only the
topics you need, and replay with `--clock` plus `use_sim_time` if nodes must follow bag time.

## Simulated lidars

Gazebo's `gpu_lidar` publishes LaserScan on `<topic>` and PointCloud2 on `<topic>/points`; the
sensor block and the bridge are in
[sim-gazebo sensors.md](../../sim-gazebo/references/sensors.md). Set `<gz_frame_id>` to the URDF
link so the simulated and real driver use the same frame name.
