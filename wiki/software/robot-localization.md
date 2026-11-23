---
type: tool
name: robot_localization
summary: The standard ROS 2 state-estimation package; EKF and UKF nodes fuse wheel odometry, IMU, visual odometry and GPS (through navsat_transform_node) into odom- and map-frame estimates, with binaries from Humble to Rolling.
tags: [ros2, robot-localization, ekf, ukf, sensor-fusion, odometry, imu, gps, navsat-transform, rep-105, state-estimation]
kind: library
area: perception
support:
license: BSD-3-Clause
links: {repo: "https://github.com/cra-ros-pkg/robot_localization", docs: "https://docs.ros.org/en/jazzy/p/robot_localization/", site: }
version: {tested: , latest: 4.0.0, as_of: 2026-11-23}
platforms: [linux]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/cra-ros-pkg/robot_localization/tree/jazzy-devel", title: "robot_localization repository, jazzy-devel: README, LICENSE, package.xml, CHANGELOG, params, launch and src", accessed: 2026-11-23}
  - {url: "https://github.com/cra-ros-pkg/robot_localization/blob/rolling-devel/CHANGELOG.rst", title: "robot_localization CHANGELOG, rolling-devel (4.0.0)", accessed: 2026-11-23}
  - {url: "https://docs.ros.org/en/jazzy/p/robot_localization/state_estimation_nodes.html", title: "robot_localization docs: State estimation nodes", accessed: 2026-11-23}
  - {url: "https://docs.ros.org/en/jazzy/p/robot_localization/preparing_sensor_data.html", title: "robot_localization docs: Preparing your data", accessed: 2026-11-23}
  - {url: "https://docs.ros.org/en/jazzy/p/robot_localization/configuring_robot_localization.html", title: "robot_localization docs: Configuring robot_localization", accessed: 2026-11-23}
  - {url: "https://docs.ros.org/en/jazzy/p/robot_localization/integrating_gps.html", title: "robot_localization docs: Integrating GPS data", accessed: 2026-11-23}
  - {url: "https://docs.ros.org/en/jazzy/p/robot_localization/navsat_transform_node.html", title: "robot_localization docs: navsat_transform_node", accessed: 2026-11-23}
  - {url: "https://docs.nav2.org/jazzy/configuration_and_development/first_time_robot_setup_guide/odom/setup_robot_localization/", title: "Nav2 docs (Jazzy): Smoothing odometry using robot_localization", accessed: 2026-11-23}
  - {url: "https://control.ros.org/jazzy/doc/ros2_controllers/diff_drive_controller/doc/userdoc.html", title: "diff_drive_controller user documentation (Jazzy)", accessed: 2026-11-23}
  - {url: "https://www.ros.org/reps/rep-0103.html", title: "REP 103: Standard units of measure and coordinate conventions", accessed: 2026-11-23}
  - {url: "https://www.ros.org/reps/rep-0105.html", title: "REP 105: Coordinate frames for mobile platforms", accessed: 2026-11-23}
  - {url: "https://github.com/ros-infrastructure/rep/blob/master/rep-0145.rst", title: "REP 145: Conventions for IMU sensor drivers (draft)", accessed: 2026-11-23}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-23}
---

# robot_localization

Two nodes, `ekf_node` and `ukf_node`, fuse any number of odometry, pose, twist and IMU topics into
one 15-value state: position, orientation, their velocities and linear acceleration [3][5]. A third,
`navsat_transform_node`, turns GPS fixes into odometry they can fuse [7]. A wheeled robot uses it to
merge wheel odometry and an IMU into a smooth `odom → base_link`, which Nav2 expects [8]. The
LICENSE file and source headers are BSD-3-Clause, although `package.xml` says Apache-2.0 [1].
Maintained by Tom Moore and Steve Macenski, with outside contributors: Jazzy 3.8.4 and Rolling
4.0.0 came out on 2026-11-02 [1][2].

## When to use it

- **Use it** for wheel odometry plus IMU on a ground robot, one EKF in `odom` [3][8]; to add
  visual or lidar odometry, a second IMU or a localizer's pose [3]; and for GPS outdoors, with a
  second EKF in `map` and `navsat_transform_node` [6].
- **Not a map localizer.** `map → odom` from a lidar or camera map comes from
  [SLAM Toolbox](slam-toolbox.md), [Cartographer](cartographer.md), [RTAB-Map](rtab-map.md) or
  Nav2's AMCL; this package can fuse their pose output.
- **Not tight camera-IMU fusion.** Use [OpenVINS](openvins.md) or [VINS-Fusion](vins-fusion.md) and
  feed their odometry in; for lidar-inertial, [LIO-SAM](lio-sam.md) or [KISS-ICP](kiss-icp.md).

## Setup

```bash
sudo apt install ros-jazzy-robot-localization
ros2 launch robot_localization ekf.launch.py   # runs ekf_node with the package's params/ekf.yaml
```

Binaries, all marked maintained [13]: Humble 3.5.5, **Jazzy 3.8.4**, Kilted 3.9.5, Lyrical
3.11.0, Rolling 4.0.0; each distro has a `<distro>-devel` branch [1]. It runs on the CPU and pulls
Eigen, GeographicLib and yaml-cpp through apt [1]. From Lyrical 3.11.0 the EKF and UKF are
lifecycle nodes, with an `autostart` launch argument; Jazzy's are plain nodes. Rolling 4.0.0 also
adds Windows builds [2].

## How an agent works with it

The skill [skills/perception-slam/SKILL.md](../../skills/perception-slam/SKILL.md) covers where
fusion sits in a SLAM stack. The interface [1][3][7]:

- **`ekf_node` / `ukf_node`** subscribe to the topics named by `odom0`, `imu0`, `pose0`, `twist0`
  and so on (numbered from 0, no gaps). They publish `odometry/filtered`, `accel/filtered` when
  `publish_acceleration` is true, and TF: `odom → base_link` when `world_frame` equals
  `odom_frame`, `map → odom` when it equals `map_frame`. `set_pose` sets the state by hand.
- **`navsat_transform_node`** subscribes to `imu`, `gps/fix` and `odometry/filtered`, publishes
  `odometry/gps` (and `gps/filtered` if enabled), and offers the `datum`, `fromLL` and `toLL`
  services.
- **Defaults** in the Jazzy code: `frequency` 30 Hz, `sensor_timeout` 1/frequency, `two_d_mode`
  false, `publish_tf` true, `world_frame` = `odom_frame` [1].

Each input has a `<sensor>_config` list of 15 booleans in the order x, y, z, roll, pitch, yaw,
vx, vy, vz, vroll, vpitch, vyaw, ax, ay, az, read in the message's own `frame_id` [3]. A planar
diff-drive robot, following the configuration guide's worked example [5]:

```yaml
ekf_filter_node:
  ros__parameters:
    frequency: 30.0
    two_d_mode: true
    world_frame: odom            # map_frame: map, odom_frame: odom, base_link_frame: base_link
    odom0: wheel/odometry
    odom0_config: [false, false, false,  false, false, false,
                   true,  true,  false,  false, false, true,
                   false, false, false]   # vx, vy (a valid zero), vyaw
    imu0: imu/data
    imu0_config:  [false, false, false,  false, false, true,
                   false, false, false,  false, false, true,
                   true,  false, false]   # yaw, vyaw, ax
```

Fuse IMU yaw only if it is absolute and trusted; Nav2's example fuses only vyaw from the IMU [8].

**GPS, the two-filter setup** [6][11]: a local EKF (`world_frame: odom`, wheel odometry and IMU)
publishes `odom → base_link`. A global EKF (`world_frame: map`) fuses the same inputs plus
`odometry/gps` (x and y only, `_differential: false`) and publishes `map → odom`.
`navsat_transform_node` reads the IMU, the fix and the global EKF's output. The package's
`dual_ekf_navsat_example.launch.py` wires this up, remapping the outputs to `odometry/local` and
`odometry/global` [1].

**Check the result** [3][8]:

```bash
ros2 topic hz /odometry/filtered               # close to the configured frequency
ros2 run tf2_ros tf2_echo odom base_link       # continuous, no jumps
ros2 node info /ekf_filter_node                # every input topic listed as a subscription
ros2 topic echo /diagnostics                   # needs print_diagnostics: true
```

Plot each input against `odometry/filtered` in [PlotJuggler](../tools/plotjuggler.md). Drive a
closed loop back to the start mark and turn in place: yaw must follow the IMU without lag.

## Traps

- **Two publishers of `odom → base_link`.** diff_drive_controller publishes it by default
  (`enable_odom_tf`) [9], and a Gazebo `/tf` bridge can too [8]; with the EKF also publishing, the
  robot jitters between them. Turn the other one off [4].
- **A map-frame filter on its own.** With `world_frame: map` the filter needs another node to
  publish `odom → base_link`, and it publishes `map → odom`, never `map → base_link` [3][11].
  The three frame names must differ; the node logs "Invalid frame configuration" but runs on [1].
- **A sensor dropped in silence.** Inputs are read in their `frame_id`, so each needs a TF to
  `base_link`, usually a fixed joint in the [URDF](urdf.md) [4]. If the lookup fails, the Jazzy
  code ignores the measurement with only a debug message [1]. Check with
  `tf2_echo base_link imu_link`. QoS is rarely the cause: inputs subscribe best-effort, which
  matches both reliable and best-effort publishers [1].
- **Counting one sensor twice.** Wheel pose and wheel velocity come from the same encoders: fuse
  the velocities [5]. Two absolute yaw sources whose variances do not overlap make the estimate
  swing between them; set `_differential: true` on all but one [5].
- **Bad covariances.** A zero variance on a fused value is replaced by 1e-6; do not inflate a
  variance to hide a value (the old robot_pose_ekf habit), set it false in the config [4].
- **IMU conventions.** The nodes assume ENU data and do not work with NED [4]. REP 145, still a
  draft, asks NED-referenced IMUs to use the frame `imu_link_ned` [12]. At rest and level, z must
  read +9.81 m/s², and a counter-clockwise turn must raise yaw [4][10].
  `imuN_remove_gravitational_acceleration` needs orientation from the same IMU [3]. In 2D, do not
  fuse ay: it is noise on a robot that cannot slide sideways, and the estimate drifts [5].
- **navsat_transform heading.** It wants yaw zero facing east; most IMUs read zero facing north, so
  set `yaw_offset` to 1.5707963 and `magnetic_declination_radians` for your site [7]. GPS jumps, so
  fuse `odometry/gps` only into the map-frame filter [6].
- **navsat topic name.** The docs say it subscribes to `imu/data`; the Jazzy code subscribes to
  `imu`, and the example launch file remaps it [1][7]. Check with `ros2 node info`.
- **ROS 1 docs.** The README still points to the ROS 1 wiki, and the docs show `<rosparam>` XML.
  Write YAML under `ros__parameters`; the package's `params/` files are the ROS 2 reference [1].
- **Bags and simulation.** Set `use_sim_time` on the filter as on every node. Looping a bag sends
  time backwards; `reset_on_time_jump: true` resets the filter instead of stalling it [3].

## Alternatives

- **fuse** (Locus Robotics): factor-graph fusion for ROS 2, released for Jazzy [13].
- [GTSAM](gtsam.md) to write your own smoother; [LIO-SAM](lio-sam.md) builds on it with lidar, IMU
  and GPS.
- [OpenVINS](openvins.md), [VINS-Fusion](vins-fusion.md) and [ORB-SLAM3](orb-slam3.md) for camera
  and IMU. The [SLAM guide](../guides/choose-a-slam-system.md) compares the map-building options.

## Sources

1. [robot_localization repository, jazzy-devel: README, LICENSE, package.xml, CHANGELOG, params, launch and src](https://github.com/cra-ros-pkg/robot_localization/tree/jazzy-devel), accessed 2026-11-23
2. [robot_localization CHANGELOG, rolling-devel (4.0.0)](https://github.com/cra-ros-pkg/robot_localization/blob/rolling-devel/CHANGELOG.rst), accessed 2026-11-23
3. [robot_localization docs: State estimation nodes](https://docs.ros.org/en/jazzy/p/robot_localization/state_estimation_nodes.html), accessed 2026-11-23
4. [robot_localization docs: Preparing your data](https://docs.ros.org/en/jazzy/p/robot_localization/preparing_sensor_data.html), accessed 2026-11-23
5. [robot_localization docs: Configuring robot_localization](https://docs.ros.org/en/jazzy/p/robot_localization/configuring_robot_localization.html), accessed 2026-11-23
6. [robot_localization docs: Integrating GPS data](https://docs.ros.org/en/jazzy/p/robot_localization/integrating_gps.html), accessed 2026-11-23
7. [robot_localization docs: navsat_transform_node](https://docs.ros.org/en/jazzy/p/robot_localization/navsat_transform_node.html), accessed 2026-11-23
8. [Nav2 docs (Jazzy): Smoothing odometry using robot_localization](https://docs.nav2.org/jazzy/configuration_and_development/first_time_robot_setup_guide/odom/setup_robot_localization/), accessed 2026-11-23
9. [diff_drive_controller user documentation (Jazzy)](https://control.ros.org/jazzy/doc/ros2_controllers/diff_drive_controller/doc/userdoc.html), accessed 2026-11-23
10. [REP 103: Standard units of measure and coordinate conventions](https://www.ros.org/reps/rep-0103.html), accessed 2026-11-23
11. [REP 105: Coordinate frames for mobile platforms](https://www.ros.org/reps/rep-0105.html), accessed 2026-11-23
12. [REP 145: Conventions for IMU sensor drivers (draft)](https://github.com/ros-infrastructure/rep/blob/master/rep-0145.rst), accessed 2026-11-23
13. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-23
