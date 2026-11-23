---
type: tool
name: linorobot2
summary: Apache-2.0 recipe for a DIY ROS 2 mobile robot (2WD, 4WD skid-steer, mecanum); micro-ROS firmware for Pico and ESP32 boards plus launch files with Nav2, SLAM Toolbox and an EKF already configured, and a Gazebo twin. Source only for Jazzy and Lyrical, no rosdistro release.
tags: [mobile-robot, diy, differential-drive, skid-steer, mecanum, micro-ros, esp32, raspberry-pi-pico, nav2, slam-toolbox, gazebo, ros2]
kind: framework
area: nav
support:
license: Apache-2.0
links: {repo: "https://github.com/linorobot/linorobot2", docs: "https://linorobot.github.io/linorobot2/", site: }
version: {tested: , latest: , as_of: 2026-11-24}
platforms: [linux]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-24
sources:
  - {url: "https://github.com/linorobot/linorobot2", title: "linorobot2 repository, jazzy, lyrical and humble branches: README, LICENSE, install.bash, configs, launch files, tags, issues", accessed: 2026-11-24}
  - {url: "https://github.com/linorobot/linorobot2_hardware", title: "linorobot2_hardware repository, jazzy and lyrical branches: README, LICENSE, platformio.ini, firmware, tags, issues", accessed: 2026-11-24}
  - {url: "https://linorobot.github.io/linorobot2/", title: "linorobot2 documentation: overview, installation, base controller, navigation, Docker", accessed: 2026-11-24}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/lyrical/configuration_and_development/navigation_plugins/", title: "Nav2 docs: Navigation Plugins (controller drivetrain support)", accessed: 2026-11-24}
---

# linorobot2

linorobot2 takes a home-built 2WD, 4WD (skid-steer) or mecanum base from bare hardware to SLAM
and autonomous navigation: ROS 2 packages for the robot computer and micro-ROS firmware in
`linorobot2_hardware` [1][2]. [Nav2](nav2.md), [SLAM Toolbox](slam-toolbox.md) and a
[robot_localization](robot-localization.md) EKF come configured; the same YAML drives a Gazebo
twin [1]. Both repos are Apache-2.0 [1][2]. **Source only:** no rosdistro release or tag [4].
Last commits: `jazzy` 2026-09-29, `lyrical` 2026-10-05, firmware 2026-10-30 [1][2].

## When to use it

- **Use it** for a first autonomous base built from parts (Raspberry Pi 4 class computer, Pico
  or ESP32 board, encoder motors, IMU, 2D lidar or depth camera), or to learn Nav2: the docs walk
  through Nav2's setup guides [1][2][3]. The Gazebo half alone suits URDF and autonomy tests [1].
- **Use something else** for Ackermann steering (unsupported) [3], motors that already have a
  [ros2_control](ros2-control.md) driver, or a bought [TurtleBot3](../robots/turtlebot3.md).

## Setup

Branches: `jazzy` (default, Ubuntu 24.04) and `lyrical` (Ubuntu 26.04); `humble` last changed
on 2025-02-09 and is unsupported [1][2]. On the robot computer:

```bash
wget https://raw.githubusercontent.com/linorobot/linorobot2/jazzy/install.bash
bash install.bash --base 2wd --laser ld19 --depth realsense   # base: 2wd | 4wd | mecanum
cd ~/linorobot2_ws && colcon build
ros2 launch linorobot2_bringup bringup.launch.py      # micro-ROS agent, EKF, sensors
ros2 launch linorobot2_navigation slam.launch.py      # or navigation.launch.py map:=...
```

The script installs drivers and micro-ROS and exports `LINOROBOT2_BASE` and the sensors in
`~/.bashrc` [1]. Firmware: set pins, driver, IMU and wheel geometry in a config header, then
`pio run -e esp32 -t upload` [2]. Boards: Pico (RP2040, RP2350), ESP32, -S2, -S3, Waveshare
General Driver; IMUs: BNO085, GY-85, MPU6050/9150/9250, QMI8658 [2]. Lidars: RPLIDAR, LD06,
LD19, STL27L, YDLIDAR, XV11; depth: RealSense, ZED, OAK-D [1]. A Docker setup is documented [3].

The firmware subscribes `/cmd_vel` (`Twist`) and publishes `odom/unfiltered` and `/imu/data`;
the EKF fuses them into `odom` and TF `odom → base_footprint` [1][3]. Wait for the agent's
"session established", then drive with `teleop_twist_keyboard` [1]. `gazebo.launch.py` and
`sim:=true` run the same stack in Gazebo; `image_to_gazebo` turns a floor plan into a world [1].

## Traps

- **Footprint.** `navigation.yaml` sets `robot_radius: 0.22` in both costmaps; set your robot's
  radius or a `footprint` polygon [3].
- **Mecanum drives like a diff drive.** The config wraps Regulated Pure Pursuit, which Nav2 does
  not list for omni bases [5], and caps y velocity at 0.0 in the velocity smoother [1].
- **Stamped `cmd_vel` on Lyrical.** The firmware takes `Twist`, so the `lyrical` config sets
  `enable_stamped_cmd_vel: false` on every node [1][2]; keep it if you swap in Nav2's params.
- **Teensy is gone** from Jazzy and Lyrical, though the main README and `platformio.ini` still
  mention it [1][2]. Use a Pico or ESP32; on the Pico, prefer serial over its slow Wi-Fi [2].
- **Axes and wheels.** Mount the IMU X forward, Y left, Z up; run `test_motors` and
  `test_sensors` first, since a wrong axis or wheel direction corrupts the EKF and SLAM [2].

## Alternatives

[TurtleBot3](../robots/turtlebot3.md) as a bought base, or [Nav2](nav2.md) with your own
[ros2_control](ros2-control.md) driver; [skills/nav-nav2](../../skills/nav-nav2/SKILL.md) helps.

## Sources

1. [linorobot2 repository, jazzy, lyrical and humble branches: README, LICENSE, install.bash, configs, launch files, tags, issues](https://github.com/linorobot/linorobot2), accessed 2026-11-24
2. [linorobot2_hardware repository, jazzy and lyrical branches: README, LICENSE, platformio.ini, firmware, tags, issues](https://github.com/linorobot/linorobot2_hardware), accessed 2026-11-24
3. [linorobot2 documentation: overview, installation, base controller, navigation, Docker](https://linorobot.github.io/linorobot2/), accessed 2026-11-24
4. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-24
5. [Nav2 docs: Navigation Plugins (controller drivetrain support)](https://docs.nav2.org/lyrical/configuration_and_development/navigation_plugins/), accessed 2026-11-24
