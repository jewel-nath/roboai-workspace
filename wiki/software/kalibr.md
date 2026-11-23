---
type: tool
name: Kalibr
summary: ETH Zurich's calibration toolbox for multi-camera rigs, camera-IMU extrinsics and time offset, IMU-IMU and rolling-shutter cameras; ROS 1 only (newest Noetic, end of life May 2025), untagged, last commit March 2024, so ROS 2 users convert their bags and run it in its Docker image.
tags: [kalibr, calibration, camera-imu, multi-camera, extrinsics, time-offset, aprilgrid, visual-inertial, rolling-shutter, docker, rosbags, ros1]
kind: tool
area: perception
support:
license: BSD-4-Clause AND LGPL-3.0-or-later
links: {repo: "https://github.com/ethz-asl/kalibr", docs: "https://github.com/ethz-asl/kalibr/wiki", site: }
version: {tested: , latest: , as_of: 2026-11-23}
platforms: [linux]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/ethz-asl/kalibr", title: "ethz-asl/kalibr: README, LICENSE, Dockerfiles, package.xml files, source headers, history and issue list", accessed: 2026-11-23}
  - {url: "https://github.com/ethz-asl/kalibr/wiki/ROS2-Calibration-Using-Kalibr", title: "Kalibr wiki: ROS2 Calibration Using Kalibr, Installation, Bag format", accessed: 2026-11-23}
  - {url: "https://github.com/ethz-asl/kalibr/wiki", title: "Kalibr wiki: Camera IMU calibration, Multiple camera calibration, Calibration targets, Supported models, YAML formats", accessed: 2026-11-23}
  - {url: "https://ternaris.gitlab.io/rosbags/topics/convert.html", title: "rosbags: Convert docs and convert CLI source (cli.py)", accessed: 2026-11-23}
  - {url: "https://www.ros.org/reps/rep-0003.html", title: "REP 3: Target platforms (Noetic, May 2020 to May 2025)", accessed: 2026-11-23}
---

# Kalibr

ETH Zurich's toolbox for multi-camera intrinsics and extrinsics, camera-to-IMU pose and time
offset, IMU-to-IMU and rolling-shutter cameras [1]: the usual source of the camera-IMU transform
[VINS-Fusion](vins-fusion.md) and [OpenVINS](openvins.md) need. **It runs on ROS 1 only**, up to
Noetic on Ubuntu 20.04 [2], end of life since May 2025 [5]. Last commit 2024-03-08, no tagged
releases, 119 open issues, recent ones unanswered [1]. BSD with an advertising clause
(BSD-4-Clause); its incremental_calibration packages are LGPL-3.0-or-later [1].

## When to use it

For camera-IMU calibration and multi-camera or fisheye rigs (pinhole, omni, double-sphere, EUCM
models) [3]. For one camera or a stereo pair, [image_pipeline](image-pipeline.md) is simpler.

## Setup

```bash
git clone https://github.com/ethz-asl/kalibr.git && cd kalibr
docker build -t kalibr -f Dockerfile_ros1_20_04 .    # build it yourself; Noetic base [2]
pip install rosbags && rosbags-convert --src calib_ros2 --dst calib.bag   # ROS 2 bag to ROS 1
xhost +local:root && docker run -it -e DISPLAY -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw -v "$PWD:/data" kalibr   # then: source devel/setup.bash
```

This is the wiki's route for ROS 2 users; `kalibr_bagcreater` builds a bag from images instead [2].

## How an agent works with it

```bash
rosrun kalibr kalibr_calibrate_cameras --bag /data/calib.bag --target /data/april.yaml \
  --models pinhole-radtan pinhole-radtan --topics /cam0/image_raw /cam1/image_raw
rosrun kalibr kalibr_calibrate_imu_camera --bag /data/calib.bag --target /data/april.yaml \
  --cam /data/camchain-calib.yaml --imu /data/imu.yaml
```

- **Target:** an Aprilgrid (partial views are fine, no pose flips) from `kalibr_create_target_pdf`;
  its YAML gives rows, columns, `tagSize` in metres and `tagSpacing` as a ratio [3].
- **Data:** ~4 Hz images for cameras only; 20 Hz images and 200 Hz IMU, every axis excited, for
  camera-IMU. `imu.yaml` holds noise density and bias random walk (Allan deviation) [3].
- **Result:** a PDF report, a summary and a camchain YAML with `T_cn_cnm1`, `T_cam_imu` and
  `timeshift_cam_imu` (t_imu = t_cam + shift); read its reprojection and IMU timing plots [3].

## Traps

- **No ROS 2 build.** Use Docker, not a Jazzy shell; bags may hold only standard message types [2].
- **Old convert syntax.** The wiki shows `rosbags-convert <bag> --dst ...`; current rosbags takes
  `--src` and `--dst`, and `--exclude-topic` drops non-standard topics [2][4].
- **Bad IMU timestamps.** Bursts of buffered, republished IMU messages wreck camera-IMU results;
  camera and IMU need one clock with low jitter [3].
- **Inverted transforms.** `T_cam_imu` takes IMU coordinates into the camera frame, whose z is the
  optical axis, the ROS `_optical` frame ([tf2](tf2.md)) [3]. Check the URDF with `tf2_echo`.
- **Unusable models, failed starts.** image_pipeline cannot rectify omni, double-sphere or EUCM
  results, so use `pinhole-radtan` or `pinhole-equi` for ROS cameras. A run that diverges on a
  bad focal guess can simply be rerun [3]; Docker sets `KALIBR_MANUAL_FOCAL_LENGTH_INIT=1` [1].

## Alternatives

camera_calibration in [image_pipeline](image-pipeline.md); [OpenCV](opencv.md) calibration calls.

## Sources

1. [ethz-asl/kalibr: README, LICENSE, Dockerfiles, package.xml files, source headers, history and issue list](https://github.com/ethz-asl/kalibr), accessed 2026-11-23
2. [Kalibr wiki: ROS2 Calibration Using Kalibr, Installation, Bag format](https://github.com/ethz-asl/kalibr/wiki/ROS2-Calibration-Using-Kalibr), accessed 2026-11-23
3. [Kalibr wiki: Camera IMU calibration, Multiple camera calibration, Calibration targets, Supported models, YAML formats](https://github.com/ethz-asl/kalibr/wiki), accessed 2026-11-23
4. [rosbags: Convert docs and convert CLI source (cli.py)](https://ternaris.gitlab.io/rosbags/topics/convert.html), accessed 2026-11-23
5. [REP 3: Target platforms (Noetic, May 2020 to May 2025)](https://www.ros.org/reps/rep-0003.html), accessed 2026-11-23
