---
type: tool
name: KITTI and KITTI-360
summary: The classic driving datasets from Karlsruhe (stereo cameras, a Velodyne HDL-64E, GPS/IMU) with benchmarks for odometry, 3D detection and more; licensed CC BY-NC-SA 3.0, so non-commercial; evo and MOLA's ROS 2 packages replay and score it.
tags: [kitti, kitti-360, dataset, benchmark, odometry, slam, lidar, velodyne, stereo, 3d-detection, evo, mola, non-commercial]
kind: dataset
area: perception
support:
license: CC-BY-NC-SA-3.0
links: {repo: , docs: "https://www.cvlibs.net/datasets/kitti/eval_odometry.php", site: "https://www.cvlibs.net/datasets/kitti/"}
version: {tested: , latest: , as_of: 2026-11-23}
platforms: []
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://www.cvlibs.net/datasets/kitti/", title: "KITTI Vision Benchmark Suite website: overview, licence, changelog and sensor setup pages", accessed: 2026-11-23}
  - {url: "https://www.cvlibs.net/datasets/kitti/eval_odometry.php", title: "KITTI visual odometry / SLAM benchmark", accessed: 2026-11-23}
  - {url: "https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d", title: "KITTI 3D object detection benchmark", accessed: 2026-11-23}
  - {url: "https://www.cvlibs.net/datasets/kitti-360/", title: "KITTI-360 website: sensors, annotations, benchmarks, licence, changelog", accessed: 2026-11-23}
  - {url: "https://github.com/MichaelGrupp/evo", title: "evo repository: README, LICENSE, KITTI file reader and APE checks", accessed: 2026-11-23}
  - {url: "https://github.com/MOLAorg/mola_academic_datasets", title: "mola_academic_datasets repository: kitti_metrics_eval and mola_input_kitti_dataset", accessed: 2026-11-23}
  - {url: "https://github.com/MOLAorg/mola", title: "MOLA repository: mola_demos KITTI replay launch and config", accessed: 2026-11-23}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro: mola and mola_academic_datasets entries, humble to rolling", accessed: 2026-11-23}
---

# KITTI and KITTI-360

Driving recordings from Karlsruhe, its countryside and highways, with benchmarks for stereo, flow,
depth, odometry, 2D and 3D object detection, tracking, road and semantics [1]. Builders use the
odometry sequences to test lidar or visual odometry and SLAM against ground truth.
**Licence: non-commercial.** KITTI and KITTI-360 are CC BY-NC-SA 3.0, and the KITTI site says
academic use only [1][4]: test research setups, keep it out of products. Downloads need a login [2].

## When to use it

- Lidar or stereo odometry outdoors on a car-like platform, compared with published methods.
- Indoor RGB-D: [TUM RGB-D](tum-rgbd.md). The KITTI changelog stops at 2021-02-25 [1].

## How an agent works with it

- **Sensors** [1]: two grayscale and two colour Point Grey Flea 2 cameras (1.4 MP) triggered at
  10 Hz by a Velodyne HDL-64E (about 100k points per scan), and an OXTS RT 3003 GPS/IMU.
- **Odometry** [2]: 22 stereo sequences; 00 to 10 have ground-truth poses (in `cam0`, the left
  grayscale camera [6]), 11 to 21 are scored on upload. Grayscale 22 GB, colour 65 GB, Velodyne
  80 GB. The score averages translation (%) and rotation (deg/m) errors over 100 to 800 m runs.
- **3D objects** [3]: 7,481 training and 7,518 test frames; cars need 3D IoU 0.7, pedestrians and
  cyclists 0.5; ranked on the moderate level, AP over 40 recall points since 2019-10-08.
- **KITTI-360** [4]: 73.7 km of suburbs with fisheye, stereo, a Velodyne HDL-64E, a pushbroom
  laser and GPS/IMU; 320k+ images and 100k scans with 2D and 3D labels and boxes.
- **Tools on Jazzy:** MOLA is released for Humble to Lyrical and Rolling
  (`mola_academic_datasets` 3.1.1; `mola` 3.6.0, or 3.5.0 on Kilted) [8]:

```bash
sudo apt install ros-jazzy-mola-demos ros-jazzy-mola-academic-datasets
export KITTI_BASE_DIR=~/data/kitti    # holds sequences/00/... and poses/00.txt
ros2 launch mola_demos ros-kitti-play.launch.py kitti_sequence:=00   # lidar, images, GT
kitti-metrics-eval -s 00 -r my_traj_tum.txt                          # official KITTI metric
pipx install evo && evo_ape kitti gt_00.txt est_00.txt -va --plot --plot_mode xz
```

The replay publishes lidar, both grayscale images and ground truth [7]; `kitti-metrics-eval`
(BSD-3-Clause) moves TUM-format paths into `cam0` [6]; evo is GPL-3.0, version 1.38.1 [5].

## Traps

- **Wrong frame, huge error.** Ground truth is in `cam0`; a path in the Velodyne frame must be
  moved with the calibration first, which `kitti-metrics-eval` does [6].
- **No timestamps:** evo's KITTI mode needs equal pose counts [5]; if frames drop, write TUM [6].
- **evo's APE is not the KITTI score.** Papers report the 100 to 800 m errors [2][6].
- **Wrong apt name.** The kitti_metrics_eval README says `mola-metrics-eval`; the package is
  `ros-jazzy-kitti-metrics-eval` [6][8]. `mola_input_kitti_dataset` is GPL-3.0 [6].

## Alternatives

[TUM RGB-D](tum-rgbd.md); to test: [KISS-ICP](../../software/kiss-icp.md),
[LIO-SAM](../../software/lio-sam.md), [ORB-SLAM3](../../software/orb-slam3.md). Older readers
such as pykitti exist. See the [perception-slam skill](../../../skills/perception-slam/SKILL.md).

## Sources

1. [KITTI Vision Benchmark Suite website: overview, licence, changelog and sensor setup pages](https://www.cvlibs.net/datasets/kitti/), accessed 2026-11-23
2. [KITTI visual odometry / SLAM benchmark](https://www.cvlibs.net/datasets/kitti/eval_odometry.php), accessed 2026-11-23
3. [KITTI 3D object detection benchmark](https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d), accessed 2026-11-23
4. [KITTI-360 website: sensors, annotations, benchmarks, licence, changelog](https://www.cvlibs.net/datasets/kitti-360/), accessed 2026-11-23
5. [evo repository: README, LICENSE, KITTI file reader and APE checks](https://github.com/MichaelGrupp/evo), accessed 2026-11-23
6. [mola_academic_datasets repository: kitti_metrics_eval and mola_input_kitti_dataset](https://github.com/MOLAorg/mola_academic_datasets), accessed 2026-11-23
7. [MOLA repository: mola_demos KITTI replay launch and config](https://github.com/MOLAorg/mola), accessed 2026-11-23
8. [rosdistro: mola and mola_academic_datasets entries, humble to rolling](https://github.com/ros/rosdistro), accessed 2026-11-23
