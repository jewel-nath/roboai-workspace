---
type: guide
name: Choose a SLAM system
summary: Which SLAM, odometry or state-estimation system a ROS 2 robot should run (SLAM Toolbox, Cartographer, RTAB-Map, KISS-ICP, LIO-SAM, ORB-SLAM3, VINS-Fusion, OpenVINS, robot_localization), decided by sensors, compute, Jazzy and Lyrical binaries, maintenance and licence; with how to measure the result.
tags: [slam, localization, odometry, state-estimation, sensor-fusion, 2d-lidar, 3d-lidar, rgbd, stereo, visual-inertial, lidar-inertial, imu, gps, ros2, nav2, evo]
question: Which SLAM, odometry or state-estimation system should my robot run?
options: [slam-toolbox, cartographer, rtab-map, kiss-icp, lio-sam, orb-slam3, vins-fusion, openvins, robot-localization]
recommendation: "Fuse wheel odometry and IMU with robot_localization first; then SLAM Toolbox for a 2D lidar, RTAB-Map for an RGB-D or stereo camera or a 3D lidar (KISS-ICP, or RKO-LIO when an IMU is fitted, as its odometry), and OpenVINS for a camera plus IMU if GPL-3.0 suits you."
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-23}
  - {url: "https://github.com/SteveMacenski/slam_toolbox/tree/jazzy", title: "slam_toolbox jazzy and ros2 branches: README, LICENSE, package.xml, config and launch files", accessed: 2026-11-23}
  - {url: "https://github.com/cartographer-project/cartographer", title: "Cartographer repository: README (A Note for ROS Users), LICENSE and history", accessed: 2026-11-23}
  - {url: "https://github.com/introlab/rtabmap", title: "RTAB-Map repository: README, LICENSE, CMakeLists.txt options and licence summary, tags", accessed: 2026-11-23}
  - {url: "https://github.com/PRBonn/kiss-icp", title: "KISS-ICP repository: README, LICENSE, ROS CI workflow, tags and history", accessed: 2026-11-23}
  - {url: "https://github.com/TixiaoShan/LIO-SAM/tree/ros2", title: "LIO-SAM ros2 and master branches: README, LICENSE and history", accessed: 2026-11-23}
  - {url: "https://github.com/hku-mars/FAST_LIO", title: "FAST_LIO repository, ROS2 branch: README, LICENSE and package.xml", accessed: 2026-11-23}
  - {url: "https://github.com/PRBonn/rko_lio", title: "RKO-LIO repository: README, LICENSE and package.xml", accessed: 2026-11-23}
  - {url: "https://github.com/UZ-SLAMLab/ORB_SLAM3", title: "ORB_SLAM3 repository: README, LICENSE, source headers, tags and history", accessed: 2026-11-23}
  - {url: "https://github.com/HKUST-Aerial-Robotics/VINS-Fusion", title: "VINS-Fusion repository: README, LICENCE, source headers and history", accessed: 2026-11-23}
  - {url: "https://github.com/rpng/open_vins", title: "open_vins repository: ReadMe, LICENSE, ROS 2 workflow, Dockerfiles, tags and history", accessed: 2026-11-23}
  - {url: "https://github.com/cra-ros-pkg/robot_localization", title: "robot_localization repository: jazzy-devel and lyrical-devel branches, LICENSE, package.xml, CHANGELOG, launch and params", accessed: 2026-11-23}
  - {url: "https://github.com/nvidia-isaac/cuVSLAM", title: "cuVSLAM repository: README (tracking modes, install) and LICENSE", accessed: 2026-11-23}
  - {url: "https://github.com/MichaelGrupp/evo", title: "evo repository: README, LICENSE, pyproject.toml, APE and RPE parsers", accessed: 2026-11-23}
---

# Choose a SLAM system

Which system should tell your robot where it is and build its map? For builders of a
[ROS 2](../tools/ros2.md) robot on Jazzy (Lyrical noted) with lidar, cameras, an IMU, wheels or
GPS. The setup steps are in the [perception-slam](../../skills/perception-slam/SKILL.md) skill.

## Short answer

- **Every wheeled robot, first:** [robot_localization](../software/robot-localization.md) fuses
  wheel odometry and the IMU into a smooth `odom → base_link` [1][12]; SLAM sits on top.
- **2D lidar, indoors, with Nav2:** [SLAM Toolbox](../software/slam-toolbox.md)
  (`ros-jazzy-slam-toolbox`) [1]; its README calls it the supported ROS 2 SLAM library [2].
- **RGB-D or stereo camera:** [RTAB-Map](../software/rtab-map.md) (`ros-jazzy-rtabmap-ros`) [1]:
  loop closure, a Nav2 grid and a saved database. BSD, but check its build licences [4].
- **3D lidar, no IMU:** RTAB-Map's `lidar3d.launch.py` (its own ICP odometry and loop closure, from
  apt), or [KISS-ICP](../software/kiss-icp.md), built from source, as its odometry [5].
- **3D lidar plus IMU:** RKO-LIO (MIT, apt) for odometry [1][8], RTAB-Map for loops;
  [LIO-SAM](../software/lio-sam.md) for a spinning lidar, a 9-axis IMU and GPS, from a branch
  tested to Humble [6].
- **Camera plus IMU, no wheels:** [OpenVINS](../software/openvins.md) from source,
  GPL-3.0-or-later [11], after a [Kalibr](../software/kalibr.md) calibration.
- **Not for new work:** [Cartographer](../software/cartographer.md) [3],
  [ORB-SLAM3](../software/orb-slam3.md) [9] and [VINS-Fusion](../software/vins-fusion.md) [10];
  keep them for an old setup or a paper baseline.

## What decides it

- **Sensors.** SLAM Toolbox needs a `LaserScan` plus odometry [2]. RGB-D and stereo give metric
  scale; one camera alone does not [13], so pair it with an IMU or depth. Deskewing a 3D lidar
  scan needs per-point timestamps [5]. LIO-SAM needs a mechanical lidar with ring and time fields
  and a 9-axis IMU at 200 Hz or more, not an Ouster's internal 6-axis one [6]; RKO-LIO needs the
  IMU-to-lidar transform in TF or a config [8]. GPS enters through robot_localization's
  `navsat_transform_node` or LIO-SAM's GPS factor [6][12].
- **Compute.** All nine run on the CPU: RTAB-Map's GPU features are off by default [4], and
  ORB-SLAM3 asks for an i7-class CPU [9]. Isaac ROS cuVSLAM needs CUDA on an NVIDIA GPU [13].
- **ROS 2 distro.** Jazzy and Lyrical ship SLAM Toolbox, Cartographer, RTAB-Map,
  robot_localization and RKO-LIO [1]. The rest are in no distro [1]: KISS-ICP's CI builds Humble,
  Jazzy, Kilted and Rolling [5]; LIO-SAM and OpenVINS stop at Humble [6][11]; ORB-SLAM3 and
  VINS-Fusion have only community ports.
- **Maintenance.** Commits this month: SLAM Toolbox, RTAB-Map, robot_localization, RKO-LIO
  [2][4][8][12]. Slow: KISS-ICP, OpenVINS and LIO-SAM's `ros2` branch [5][6][11]. Stopped:
  Cartographer ("no longer actively maintained", ROS forks kept "in a limited capacity") [3],
  ORB-SLAM3 since 2022 [9], VINS-Fusion since 2021 [10].
- **Licence.** Permissive: Cartographer (Apache-2.0) [3], KISS-ICP and RKO-LIO (MIT) [5][8],
  LIO-SAM and robot_localization (BSD-3-Clause) [6][12]. RTAB-Map is BSD, but its default build
  adds TORO (CC BY-NC-SA, non-commercial) and GPL parts [4]. SLAM Toolbox is LGPL [2]; ORB-SLAM3,
  VINS-Fusion and OpenVINS are GPL-3.0 [9][10][11]; cuVSLAM may run only on NVIDIA hardware [13].

## Options compared

| Option | Sensors | ROS 2 Jazzy binary? | Licence | Maintenance | Best when |
|---|---|---|---|---|---|
| [SLAM Toolbox](../software/slam-toolbox.md) | 2D lidar + odometry | Yes, 2.8.5; Lyrical 2.10.0 [1] | LGPL-2.1; bundled Karto LGPL-3.0+ [2] | Active; commits 2026-11-02 [2] | Indoor wheeled robot running Nav2 |
| [Cartographer](../software/cartographer.md) | 2D or 3D lidar; IMU (needed in 3D, on by default in 2D); odometry, GPS optional | Yes, 2.0.9004 [1] | Apache-2.0 [3] | Upstream stopped (last commit 2024-01-05); forks limited [3] | Keeping a robot with tuned Lua configs |
| [RTAB-Map](../software/rtab-map.md) | RGB-D, stereo, 2D or 3D lidar + odometry; IMU orientation only | Yes, 0.23.14 (library 0.24.2) [1][4] | BSD-3-Clause; GPL and non-commercial parts in the default build [4] | Active; commits 2026-11-21 and later [4] | Cameras, 3D lidar, loop closure, multi-session maps |
| [KISS-ICP](../software/kiss-icp.md) | 3D lidar only | No, source build [1][5] | MIT [5] | 1.3.0; last commit 2026-05-04 [5] | Lidar odometry without an IMU; dataset baseline |
| [LIO-SAM](../software/lio-sam.md) | Spinning 3D lidar, 9-axis IMU ≥200 Hz, GPS optional | No; `ros2` branch tested to Humble [1][6] | BSD-3-Clause [6] | `master` idle since 2023; `ros2` fix 2026-11-19 [6] | Lidar-inertial mapping with GPS outdoors |
| [ORB-SLAM3](../software/orb-slam3.md) | Mono, stereo or RGB-D, each ± IMU | No; community wrappers only [1] | GPL-3.0-or-later [9] | None since 2022-02-10 [9] | Visual SLAM baseline in research |
| [VINS-Fusion](../software/vins-fusion.md) | Mono + IMU, stereo, stereo + IMU; loose GPS | No; unofficial port [1] | GPL-3.0 [10] | None since 2021-07-26; ROS 1 upstream [10] | Reproducing a VIO paper result |
| [OpenVINS](../software/openvins.md) | One or more cameras + IMU | No; source, CI to Humble [1][11] | GPL-3.0-or-later [11] | Slow; last commit 2025-11-30 [11] | Camera-IMU odometry with evaluation tools |
| [robot_localization](../software/robot-localization.md) | Wheel odometry, IMU, any odometry or pose, GPS | Yes, 3.8.4; Lyrical 3.11.0 [1] | BSD-3-Clause (package.xml says Apache-2.0) [12] | Active; releases 2026-11-02 [12] | Always: the `odom` layer, and GPS in `map` |

Without a page here: RKO-LIO (lidar-inertial odometry, MIT, apt, commits this month) [1][8];
FAST-LIO2 (spinning and solid-state lidars, no ROS binary, GPL-2.0 by its LICENSE, BSD by its
package.xml) [1][7]; MOLA (lidar odometry, Jazzy binaries) [1]; cuVSLAM, the library inside Isaac
ROS Visual SLAM (mono, RGB-D, stereo or stereo plus IMU; NVIDIA GPUs only) [13]. Related:
[GTSAM](../software/gtsam.md) for your own smoother, [OctoMap](../software/octomap.md) for 3D maps.

## Fuse odometry first

SLAM owns `map → odom` and relies on `odom → base_link`: SLAM Toolbox subscribes to odometry [2],
and RTAB-Map takes any odometry on its `odom` input. On wheels, robot_localization provides it:

- One EKF with `world_frame: odom` fuses wheel velocities and the IMU yaw rate and publishes
  `odom → base_link` [12]. Turn off the drive controller's odometry TF, or `base_link` gets two
  parents and the robot jumps.
- Outdoors, a second EKF with `world_frame: map` fuses `odometry/gps` from `navsat_transform_node`
  and owns `map → odom` [12]; SLAM must then not publish it.
- Lidar or visual odometry either owns `odom` (no wheels) or feeds the EKF, never both; LIO-SAM's
  launch publishes its own `odom → base_link` and a static `map → odom` [6].

Check with `ros2 run tf2_ros tf2_echo odom base_link` (smooth, no jumps) and
`ros2 topic info -v /tf` (only the publishers you planned).

## Judge a result

Measure; "looks fine in RViz" is not a result. evo (GPL-3.0, Python 3.11+) reads TUM, KITTI and
EuRoC files and ROS 1 and ROS 2 bags [14]. ATE (`evo_ape` with `--align`) is global accuracy; RPE
(`evo_rpe` with `--delta` and `--delta_unit`) is drift per metre or frame; add `--correct_scale`
for monocular runs [14]. [TUM RGB-D](../learning/datasets/tum-rgbd.md) covers indoor RGB-D and
visual SLAM (motion-capture ground truth, CC BY 4.0); [KITTI](../learning/datasets/kitti.md)
covers outdoor stereo and 3D lidar (non-commercial; its official score is not evo's APE). On your
own robot, record raw sensors and TF once and replay that bag for every candidate; replaying it
twice must give the same numbers.

```bash
pipx install evo
evo_ape tum groundtruth.txt est.txt -va --plot                # ATE after alignment
evo_rpe tum groundtruth.txt est.txt -va -d 1 -u m             # RPE per metre
evo_ape bag2 run_bag /ground_truth /odometry/filtered -va     # two topics in a ROS 2 bag
```

## When the answer changes

- **Jazzy to Lyrical:** the same five binaries [1]; robot_localization 3.11.0's EKF and UKF are
  lifecycle nodes, so launch them with `autostart` or the package's launch files [12]. The
  source-only options are untested there.
- **A commercial product:** shipping ORB-SLAM3, VINS-Fusion, OpenVINS or FAST-LIO2 means releasing
  your derived code under the GPL [7][9][10][11]. Build RTAB-Map with `-DWITH_TORO=OFF`,
  `-DWITH_VERTIGO=OFF`, `-DWITH_ORB_OCTREE=OFF` and `-DWITH_MADGWICK=OFF`, then read its licence
  summary [4]. Share changes to SLAM Toolbox itself (LGPL) [2]. Test on TUM RGB-D, not KITTI.
- **A solid-state lidar:** LIO-SAM supports mechanical lidars only [6]; FAST-LIO2 handles Livox [7].
- **An NVIDIA Jetson with stereo cameras:** cuVSLAM runs the visual work on the GPU, but it is not
  in rosdistro [1] and its licence covers NVIDIA hardware only [13].
- **Status to watch:** a KISS-ICP or OpenVINS release in rosdistro, LIO-SAM tested past Humble,
  RTAB-Map 0.24 in the ROS binaries. Any of these reopens the choice.

## Sources

1. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-23
2. [slam_toolbox jazzy and ros2 branches: README, LICENSE, package.xml, config and launch files](https://github.com/SteveMacenski/slam_toolbox/tree/jazzy), accessed 2026-11-23
3. [Cartographer repository: README (A Note for ROS Users), LICENSE and history](https://github.com/cartographer-project/cartographer), accessed 2026-11-23
4. [RTAB-Map repository: README, LICENSE, CMakeLists.txt options and licence summary, tags](https://github.com/introlab/rtabmap), accessed 2026-11-23
5. [KISS-ICP repository: README, LICENSE, ROS CI workflow, tags and history](https://github.com/PRBonn/kiss-icp), accessed 2026-11-23
6. [LIO-SAM ros2 and master branches: README, LICENSE and history](https://github.com/TixiaoShan/LIO-SAM/tree/ros2), accessed 2026-11-23
7. [FAST_LIO repository, ROS2 branch: README, LICENSE and package.xml](https://github.com/hku-mars/FAST_LIO), accessed 2026-11-23
8. [RKO-LIO repository: README, LICENSE and package.xml](https://github.com/PRBonn/rko_lio), accessed 2026-11-23
9. [ORB_SLAM3 repository: README, LICENSE, source headers, tags and history](https://github.com/UZ-SLAMLab/ORB_SLAM3), accessed 2026-11-23
10. [VINS-Fusion repository: README, LICENCE, source headers and history](https://github.com/HKUST-Aerial-Robotics/VINS-Fusion), accessed 2026-11-23
11. [open_vins repository: ReadMe, LICENSE, ROS 2 workflow, Dockerfiles, tags and history](https://github.com/rpng/open_vins), accessed 2026-11-23
12. [robot_localization repository: jazzy-devel and lyrical-devel branches, LICENSE, package.xml, CHANGELOG, launch and params](https://github.com/cra-ros-pkg/robot_localization), accessed 2026-11-23
13. [cuVSLAM repository: README (tracking modes, install) and LICENSE](https://github.com/nvidia-isaac/cuVSLAM), accessed 2026-11-23
14. [evo repository: README, LICENSE, pyproject.toml, APE and RPE parsers](https://github.com/MichaelGrupp/evo), accessed 2026-11-23
