---
type: tool
name: image_pipeline
summary: The standard ROS 2 packages between a camera driver and vision code (camera_calibration, image_proc, stereo_image_proc, depth_image_proc, image_view and more); released for Humble to Rolling, 5.0.13 on Jazzy, and used with image_transport and camera_info_manager from image_common.
tags: [ros2, camera, image-pipeline, camera-calibration, image-proc, rectify, debayer, stereo-image-proc, depth-image-proc, point-cloud, image-view, image-transport, camera-info, camera-info-manager]
kind: library
area: perception
support:
license: BSD-3-Clause AND Apache-2.0
links: {repo: "https://github.com/ros-perception/image_pipeline", docs: "https://docs.ros.org/en/jazzy/p/image_pipeline/", site: }
version: {tested: , latest: 5.0.13, as_of: 2026-11-23}
platforms: [linux]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/ros-perception/image_pipeline/tree/jazzy", title: "image_pipeline repository, jazzy branch: README, LICENSE, package.xml files, launch files, source, history", accessed: 2026-11-23}
  - {url: "https://docs.ros.org/en/jazzy/p/image_pipeline/", title: "image_pipeline docs (Jazzy): overview, Camera Info, tutorials, changelog notes", accessed: 2026-11-23}
  - {url: "https://docs.ros.org/en/jazzy/p/image_proc/", title: "image_proc docs (Jazzy): components and tutorials", accessed: 2026-11-23}
  - {url: "https://docs.ros.org/en/jazzy/p/camera_calibration/", title: "camera_calibration docs (Jazzy): nodes, monocular and stereo tutorials", accessed: 2026-11-23}
  - {url: "https://docs.ros.org/en/jazzy/p/depth_image_proc/", title: "depth_image_proc docs (Jazzy): components", accessed: 2026-11-23}
  - {url: "https://docs.ros.org/en/jazzy/p/stereo_image_proc/", title: "stereo_image_proc docs (Jazzy): components", accessed: 2026-11-23}
  - {url: "https://github.com/ros-perception/image_common/tree/jazzy", title: "image_common repository, jazzy branch: image_transport and camera_info_manager", accessed: 2026-11-23}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro: humble, jazzy, kilted, lyrical and rolling distribution.yaml", accessed: 2026-11-23}
  - {url: "https://github.com/ros-perception/image_pipeline/tree/jazzy/camera_calibration/src/camera_calibration", title: "camera_calibration source, jazzy branch: cameracalibrator options and calibrator.py", accessed: 2026-11-23}
  - {url: "https://github.com/ros-perception/vision_opencv/blob/rolling/image_geometry/src/pinhole_camera_model.cpp", title: "image_geometry pinhole_camera_model.cpp, vision_opencv rolling branch (Jazzy release 4.1.0)", accessed: 2026-11-23}
---

# image_pipeline

image_pipeline fills the gap between a camera driver's raw images and vision code: it calibrates
cameras (camera_calibration), debayers and rectifies (image_proc), turns stereo pairs into
disparity and point clouds (stereo_image_proc), and turns depth images into point clouds
(depth_image_proc); image_view, image_rotate and image_publisher view, rotate and replay images
[1][2]. It sits on image_transport and camera_info_manager from image_common [7]. Code is
BSD-3-Clause; the tracing package is Apache-2.0 [1].

## Releases

| Distro | image_pipeline | image_common | image_transport_plugins | vision_opencv |
|---|---|---|---|---|
| Humble | 3.0.9 | 3.1.13 | 2.5.5 | 3.2.1 |
| **Jazzy** | **5.0.13** | 5.1.8 | 4.0.7 | 4.1.0 |
| Kilted | 6.0.13 | 6.1.4 | 5.1.3 | 4.1.0 |
| Lyrical | 7.1.7 | 6.4.10 | 6.2.6 | 4.1.0 |
| Rolling | 8.0.2 | 7.0.5 | 7.0.1 | 4.1.0 |

Versions from rosdistro [8]; each distro has its own branch. The jazzy branch is active: 5.0.13
came on 2026-07-10 after backported fixes, April to June 2026, for crashes on malformed or
mismatched depth images [1]. There are no GitHub releases; use the distro packages.

## When to use it

- **Every camera on a ROS 2 robot** needs a calibration and a matching `camera_info`; most
  consumers ([AprilTag](apriltag.md), visual odometry, depth to cloud) want rectified images.
- **Depth cameras** whose driver does not publish a cloud, or whose depth must be registered to
  the colour camera first: depth_image_proc [5].
- **Stereo pairs** on a CPU: stereo_image_proc runs OpenCV block matching or SGBM [6].
- **Use something else** for multi-camera or camera-IMU extrinsics ([Kalibr](kalibr.md)), custom
  processing ([OpenCV](opencv.md) in your own node), and on NVIDIA Jetson, where the README points
  to NVIDIA's Isaac ROS image pipeline for accelerated `image_proc` features [1].

## Setup

```bash
sudo apt install ros-jazzy-image-pipeline ros-jazzy-image-transport-plugins
```

The metapackage pulls camera_calibration, depth_image_proc, image_proc, image_publisher,
image_rotate, image_view and stereo_image_proc [1]; the plugins add the `compressed`,
`compressedDepth`, `theora` and `zstd` transports [8]. Jazzy binaries are built for Ubuntu 24.04,
Debian 12 and RHEL 9 [8]; elsewhere, build from source with colcon.

## How an agent works with it

**Topic convention.** A camera publishes `<ns>/image_raw` and `<ns>/camera_info` with the same
header stamp; since Jazzy, remapping a node's `image` input moves its `camera_info` with it [2].
Every node is also a component, and one container avoids copying images between processes [3].
The [perception-camera](../../skills/perception-camera/SKILL.md) skill covers camera bring-up.

**Calibrate** [4][9]:

```bash
ros2 run camera_calibration cameracalibrator --size 8x6 --square 0.108 \
  image:=/camera/image_raw camera:=/camera
```

- `--size` is interior corners, `--square` the square edge in metres. `-p charuco` with
  `--charuco_marker_size` and `--aruco_dict` takes a ChArUco board; `circles` and `acircles` also
  work. Stereo: remap `left`, `right`, `left_camera`, `right_camera`, and add `--approximate 0.1`
  if the pair is not hardware-synchronised [4][9].
- Move the board across the view, near and far, and tilted, until **CALIBRATE** lights. **COMMIT**
  calls the driver's `camera/set_camera_info` service; **SAVE** writes
  `/tmp/calibrationdata.tar.gz`; without that service, start with `--no-service-check` [4][9].
- Drivers store it through camera_info_manager. The default URL is
  `file://${ROS_HOME}/camera_info/${NAME}.yaml` (`~/.ros/camera_info/` when `ROS_HOME` is unset);
  `package://<pkg>/<path>.yaml` loads a file shipped in a package [7].
- `cameracheck` prints an error estimate from rectified checkerboard images; straight edges in
  the world should look straight in `image_rect` [4].

**Rectify, debayer, view** [1][3]:

```bash
ros2 launch image_proc image_proc.launch.py namespace:=camera   # debayer + 2 rectify nodes
ros2 run image_proc rectify_node --ros-args -r __ns:=/camera -r image:=image_raw
ros2 run image_view image_view --ros-args -r image:=/camera/image_rect
```

The launch file chains `image_raw` into `image_mono` and `image_color`, then `image_rect` and
`image_rect_color`; `container:=<name>` loads them into an existing container [1].
`crop_decimate_node` bins and crops, `resize_node` scales image and `camera_info` together [3].

**Depth to point cloud** [5]: `point_cloud_xyz_node` reads `image_rect` and `camera_info` and
publishes `points`. For colour, `register_node` reprojects `depth/image_rect` into the RGB camera
using both calibrations and TF, then `point_cloud_xyzrgb_node` reads
`depth_registered/image_rect`, `rgb/image_rect_color` and `rgb/camera_info`. Depth in `16UC1` is
millimetres, `32FC1` metres; `convert_metric_node` turns the first into the second.

**Stereo** [6]: `ros2 launch stereo_image_proc stereo_image_proc.launch.py` with
`left_namespace` and `right_namespace` publishes `disparity` and `points2`; `stereo_algorithm`
picks block matching (0, default) or SGBM (1) [1]. Main knobs: `disparity_range` (64),
`correlation_window_size` (15), `uniqueness_ratio` (15.0), `speckle_size` (100) [6].

**Check the result:**

```bash
ros2 topic echo /camera/camera_info --once      # k[0] must not be 0; d, r, p filled in
ros2 topic hz /camera/image_rect                # should match the camera rate
ros2 topic info /camera/image_raw -v            # QoS of each publisher and subscriber
ros2 run image_transport list_transports        # which plugins are installed
```

## Traps

- **"Rectified topic ... requested but camera ... is uncalibrated."** `camera_info` has `k[0]` of
  0, so RectifyNode drops every frame [1]. Calibrate, then load the file through the driver's
  `camera_info_url` parameter; loading a file alone does not rectify, image_proc does [4].
- **Output topic exists but stays silent.** image_proc nodes subscribe to their input only while
  something subscribes to their output [1]; `ros2 topic hz` on the output is a fair test.
- **QoS mismatch.** Most nodes follow REP 2003: sensor-data (best effort) subscribers, reliable
  publishers [2]; image_proc copies the QoS of the input's first publisher, else sensor data [1].
  A reliable subscriber to a best-effort camera gets nothing: compare both ends with
  `ros2 topic info -v`, and fix with `qos_overrides` on the fully resolved topic name
  (reliability, history and depth only) [2].
- **Broken image and info pairing.** Image and `camera_info` are matched by stamp in a queue of
  5; over Wi-Fi raise `queue_size` [3]. stereo_image_proc wants exact stamps unless
  `approximate_sync` is true [6]. A driver whose info topic breaks the naming convention needs
  the fully resolved name remapped [2].
- **Humble launch files on Jazzy.** Jazzy renamed the radial depth nodes' inputs (to
  `depth/image_raw`, `rgb/image_raw`), renamed `transport` to `image_transport` in ExtractImages
  and StereoView, and in stereo_image_proc dropped `use_system_default_qos` and replaced
  `full_dp` with `sgbm_mode` [2].
- **No dots in the calibration window.** `--size` counts interior corners, not squares [4]. ChArUco
  is only for a single pinhole camera: fisheye and stereo are not implemented with it [9].
- **Depth units and resolutions.** Feed `16UC1` or `32FC1` only [5]. Since 5.0.13,
  `point_cloud_xyzrgb_node` skips a frame whose depth and RGB aspect ratios do not match,
  with an error, instead of crashing [1].
- **Distortion models.** Rectification goes through image_geometry, which knows `plumb_bob`,
  `rational_polynomial` and `equidistant` (fisheye) and fails on any other model [10]. Kalibr's
  omni, double-sphere and EUCM results cannot be rectified here. Choose the fisheye model with
  the calibration window's camera-type slider [9].

## Alternatives

- [OpenCV](opencv.md) in your own node; [Kalibr](kalibr.md) for multi-camera and camera-IMU
  calibration; NVIDIA's Isaac ROS image pipeline on Jetson [1].

## Sources

1. [image_pipeline repository, jazzy branch: README, LICENSE, package.xml files, launch files, source, history](https://github.com/ros-perception/image_pipeline/tree/jazzy), accessed 2026-11-23
2. [image_pipeline docs (Jazzy): overview, Camera Info, tutorials, changelog notes](https://docs.ros.org/en/jazzy/p/image_pipeline/), accessed 2026-11-23
3. [image_proc docs (Jazzy): components and tutorials](https://docs.ros.org/en/jazzy/p/image_proc/), accessed 2026-11-23
4. [camera_calibration docs (Jazzy): nodes, monocular and stereo tutorials](https://docs.ros.org/en/jazzy/p/camera_calibration/), accessed 2026-11-23
5. [depth_image_proc docs (Jazzy): components](https://docs.ros.org/en/jazzy/p/depth_image_proc/), accessed 2026-11-23
6. [stereo_image_proc docs (Jazzy): components](https://docs.ros.org/en/jazzy/p/stereo_image_proc/), accessed 2026-11-23
7. [image_common repository, jazzy branch: image_transport and camera_info_manager](https://github.com/ros-perception/image_common/tree/jazzy), accessed 2026-11-23
8. [rosdistro: humble, jazzy, kilted, lyrical and rolling distribution.yaml](https://github.com/ros/rosdistro), accessed 2026-11-23
9. [camera_calibration source, jazzy branch: cameracalibrator options and calibrator.py](https://github.com/ros-perception/image_pipeline/tree/jazzy/camera_calibration/src/camera_calibration), accessed 2026-11-23
10. [image_geometry pinhole_camera_model.cpp, vision_opencv rolling branch (Jazzy release 4.1.0)](https://github.com/ros-perception/vision_opencv/blob/rolling/image_geometry/src/pinhole_camera_model.cpp), accessed 2026-11-23
