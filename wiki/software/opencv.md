---
type: tool
name: OpenCV
summary: The computer-vision library under most robot perception code (calibration, features, pose from points, stereo, image I/O); Apache-2.0 since 4.5.0, newest release 5.1.0, while ROS 2 Jazzy builds against Ubuntu 24.04's OpenCV 4.6.0 and reaches it through cv_bridge.
tags: [opencv, cv2, computer-vision, cv-bridge, vision-opencv, image-geometry, opencv-contrib, opencv-python, cuda, calibration, solvepnp, ros2]
kind: library
area: perception
support:
license: Apache-2.0
links: {repo: "https://github.com/opencv/opencv", docs: "https://docs.opencv.org/5.x/", site: "https://opencv.org"}
version: {tested: , latest: 5.1.0, as_of: 2026-11-23}
platforms: [linux, windows, macos]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/opencv/opencv", title: "opencv repository: LICENSE, release tags 4.4.0 to 5.1.0, 4.x and 5.x branches", accessed: 2026-11-23}
  - {url: "https://github.com/opencv/opencv/wiki/OpenCV-Change-Logs", title: "OpenCV change logs (5.1.0, 5.0-alpha licence note, 4.5.0)", accessed: 2026-11-23}
  - {url: "https://github.com/opencv/opencv/wiki/Branches", title: "OpenCV wiki: Branches and contribution policies", accessed: 2026-11-23}
  - {url: "https://github.com/opencv/opencv/wiki/OpenCV-4-to-5-migration", title: "OpenCV wiki: OpenCV 4 to 5 migration", accessed: 2026-11-23}
  - {url: "https://docs.opencv.org/4.x/db/d05/tutorial_config_reference.html", title: "OpenCV configuration options reference (CUDA, DNN backends)", accessed: 2026-11-23}
  - {url: "https://github.com/opencv/opencv_contrib", title: "opencv_contrib repository: LICENSE and module list, 4.x and 5.x branches", accessed: 2026-11-23}
  - {url: "https://github.com/opencv/opencv-python", title: "opencv-python repository: README, LICENSE, pyproject.toml", accessed: 2026-11-23}
  - {url: "https://pypi.org/project/opencv-python/", title: "PyPI: opencv-python release history", accessed: 2026-11-23}
  - {url: "https://packages.ubuntu.com/search?keywords=libopencv-dev&searchon=names&suite=all&section=all", title: "Ubuntu packages: libopencv-dev in jammy, noble and resolute", accessed: 2026-11-23}
  - {url: "https://www.ros.org/reps/rep-2000.html", title: "REP 2000: ROS 2 releases and target platforms", accessed: 2026-11-23}
  - {url: "https://github.com/ros-perception/vision_opencv", title: "vision_opencv repository (cv_bridge, image_geometry), rolling branch", accessed: 2026-11-23}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro: distribution files and rosdep base.yaml and python.yaml", accessed: 2026-11-23}
  - {url: "https://docs.ros.org/en/jazzy/How-To-Guides/Using-Python-Packages.html", title: "ROS 2 docs (Jazzy): Using Python packages with ROS 2", accessed: 2026-11-23}
  - {url: "https://github.com/ros-perception/image_pipeline/blob/jazzy/camera_calibration/src/camera_calibration/calibrator.py", title: "camera_calibration calibrator.py, jazzy branch (ArUco API switch)", accessed: 2026-11-23}
---

# OpenCV

OpenCV is the C++ library, with Python bindings (`cv2`), that most robot vision code is built on:
image I/O and filtering, camera calibration, feature detection and matching, pose from 2D-3D
points (`solvePnP`), stereo matching, optical flow and a DNN module [4]. In ROS 2 it is reached
through cv_bridge, which turns a `sensor_msgs/Image` into a `cv::Mat` or a NumPy array [11].
Apache-2.0 since 4.5.0 (October 2020); 4.4 and earlier, and all of 3.x, are BSD-3-Clause [1][2].

## Versions

| Line | Newest | Released | State |
|---|---|---|---|
| 5.x | 5.1.0 | 2026-11-05 | main development branch since 5.0.0 (2026-06-05) [1][3] |
| 4.x | 4.14.0 | 2026-07-17 | maintenance mode: fixes only, no new features [1][3] |
| 3.4 | — | — | end of life in 2023 [3] |

What a ROS user actually runs is the **system OpenCV**. ROS packages name the rosdep keys
`libopencv-dev` and `python3-opencv`, which resolve to the distribution's own apt packages [12],
and REP 2000 pins each ROS 2 release to the versions on its platforms: OpenCV 4.6.0 and NumPy
1.26.4 for Jazzy (and Kilted) on Ubuntu 24.04, 4.5.4 for Humble on 22.04 [10]. Ubuntu 26.04, the
Lyrical platform, ships 4.10.0 [9]. So every `ros-jazzy-*` binary that uses OpenCV, cv_bridge
included, is built against 4.6.0, a June 2022 release [1][11]. pip's `opencv-python` is on 5.1.0
(wheel 5.1.0.95, 2026-11-17) [8].

## When to use it

- **Classic vision on the robot:** undistortion, colour and threshold work, ORB or SIFT features,
  homographies, `solvePnP` for a known object, `StereoSGBM` disparity, video capture [4].
- **Inside a ROS 2 node:** convert with cv_bridge, process with OpenCV, publish the result. For the
  standard steps (debayer, rectify, depth to point cloud) run the ready nodes in
  [image_pipeline](image-pipeline.md) instead of writing them again.
- **Use something else** for point clouds ([PCL](pcl.md), [Open3D](open3d.md)), fiducials
  ([AprilTag](apriltag.md)), camera-IMU calibration ([Kalibr](kalibr.md)) and learned detection
  ([YOLO](../learning/models/yolo.md)). Visual SLAM systems such as [ORB-SLAM3](orb-slam3.md)
  link OpenCV themselves.
- **5.x or 4.x:** on Jazzy keep the system 4.6.0 for anything that touches ROS binaries; use 5.x
  in stand-alone Python tools or new C++ code built outside ROS.

## Setup

**Ubuntu 24.04, Jazzy** [10][11][12]:

```bash
sudo apt install libopencv-dev python3-opencv     # Ubuntu's OpenCV 4.6.0
sudo apt install ros-jazzy-vision-opencv          # cv_bridge and image_geometry
```

In `package.xml`, depend on `cv_bridge` plus the keys `libopencv-dev` (C++) or `python3-opencv`
(Python), then `rosdep install --from-paths src --ignore-src -y` [12][13]. vision_opencv 4.1.0
(April 2024) is the release in Jazzy, Kilted, Lyrical and Rolling; Humble has 3.2.1 [11][12].

**Without ROS** (Linux, Windows, macOS): pick exactly one of `opencv-python`,
`opencv-contrib-python`, `opencv-python-headless` or `opencv-contrib-python-headless`; the headless
ones drop the GUI (no `cv2.imshow`) and suit containers [7]. Wheels carry no CUDA and no patented
non-free algorithms such as SURF; SIFT is included since 4.3.0 [7].

**CUDA** needs a source build. Since 4.0 the CUDA modules (`cudaarithm`, `cudaimgproc`,
`cudafeatures2d`, `cudastereo`, `cudaoptflow` and more) live in opencv_contrib, on both 4.x and 5.x
[5][6]. Install the CUDA toolkit from NVIDIA, then configure with contrib; `OPENCV_DNN_CUDA` also
needs cuBLAS and cuDNN [5]:

```bash
cmake -S opencv -B build -D CMAKE_BUILD_TYPE=Release \
  -D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib/modules \
  -D WITH_CUDA=ON -D OPENCV_DNN_CUDA=ON     # set CUDA_ARCH_BIN to your GPU to cut build time
```

## How an agent works with it

A Python node converts each frame, works on it and publishes with the input's header, so the
timestamp and `frame_id` survive [11]:

```python
from cv_bridge import CvBridge
import cv2

bridge = CvBridge()

def on_image(msg):  # subscription callback for sensor_msgs/Image
    frame = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')      # NumPy array
    edges = cv2.Canny(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 50, 150)
    pub.publish(bridge.cv2_to_imgmsg(edges, encoding='mono8', header=msg.header))
```

- `desired_encoding='passthrough'` keeps the data as sent, which depth images need (`16UC1` in
  millimetres, `32FC1` in metres); `compressed_imgmsg_to_cv2` reads `CompressedImage` [11].
- C++: `cv_bridge::toCvShare(msg, "bgr8")->image`, from `cv_bridge/cv_bridge.hpp`; the old `.h`
  headers were removed in 4.0.0 [11].
- `image_geometry.PinholeCameraModel` loads a `CameraInfo` and projects or rectifies points, so a
  node does not hand-roll the K, D, R, P maths [11].
- **Check:** `python3 -c "import cv2; print(cv2.__version__, cv2.__file__)"` shows which OpenCV
  Python really loads; `print(cv2.getBuildInformation())` shows whether CUDA and contrib are in;
  `ros2 topic hz` on the output topic shows the node keeps up.

The [perception-camera](../../skills/perception-camera/SKILL.md) skill covers camera bring-up.

## Traps

- **A pip OpenCV on top of Jazzy.** `pip install opencv-python` brings OpenCV 5.1 and, on Python
  3.9 or newer, NumPy 2 [7][8]; Jazzy is built against NumPy 1.26.4 and OpenCV 4.6.0 [10]. The pip
  `cv2` then shadows `python3-opencv`, and compiled ROS Python modules built for NumPy 1.x can
  stop importing. Check `cv2.__file__`; keep pip packages in a virtualenv made with the system
  interpreter, as the ROS docs advise [13].
- **Two wheels at once.** All four pip packages install the same `cv2`; with two installed the
  module breaks. Uninstall all of them and install one [7].
- **Two OpenCVs in one process.** The apt cv_bridge links Ubuntu's libraries [11][12]; a node that
  also links your source-built OpenCV loads both. Build cv_bridge from source against your build.
  Its CMake asks for OpenCV 4, then 3, so it does not find 5.x without a patch [11].
- **4.x code on 5.x.** `calib3d` split into `geometry`, `calib`, `stereo` and `ptcloud`;
  `features2d` became `features`; `ml`, G-API, Haar and HOG moved to contrib; the C API and the
  Darknet and Caffe importers are gone; C++17 is required. Python calls are mostly unchanged and
  `#include <opencv2/calib3d.hpp>` still works [4].
- **Examples written for newer 4.x.** The ArUco API changed at 4.8.0 (`CharucoBoard_create`
  became `CharucoBoard`, detection moved to `CharucoDetector`); camera_calibration switches on the
  version for this reason [14]. Code copied from current tutorials can fail on Jazzy's 4.6.0.
- **Licence surprises.** OpenCV is Apache-2.0, but the pip wheels bundle FFmpeg under LGPL-2.1
  and the non-headless Linux wheels bundle Qt 5 under LGPL-3.0 [7]. Contrib's `xfeatures2d` holds
  non-free, patented algorithms [6]; check before shipping them.

## Alternatives

- [PCL](pcl.md) and [Open3D](open3d.md) for 3D data; [image_pipeline](image-pipeline.md) for the
  standard ROS 2 camera steps; [AprilTag](apriltag.md) for markers; scikit-image and Pillow for
  simple Python image work outside robots.

## Sources

1. [opencv repository: LICENSE, release tags 4.4.0 to 5.1.0, 4.x and 5.x branches](https://github.com/opencv/opencv), accessed 2026-11-23
2. [OpenCV change logs (5.1.0, 5.0-alpha licence note, 4.5.0)](https://github.com/opencv/opencv/wiki/OpenCV-Change-Logs), accessed 2026-11-23
3. [OpenCV wiki: Branches and contribution policies](https://github.com/opencv/opencv/wiki/Branches), accessed 2026-11-23
4. [OpenCV wiki: OpenCV 4 to 5 migration](https://github.com/opencv/opencv/wiki/OpenCV-4-to-5-migration), accessed 2026-11-23
5. [OpenCV configuration options reference (CUDA, DNN backends)](https://docs.opencv.org/4.x/db/d05/tutorial_config_reference.html), accessed 2026-11-23
6. [opencv_contrib repository: LICENSE and module list, 4.x and 5.x branches](https://github.com/opencv/opencv_contrib), accessed 2026-11-23
7. [opencv-python repository: README, LICENSE, pyproject.toml](https://github.com/opencv/opencv-python), accessed 2026-11-23
8. [PyPI: opencv-python release history](https://pypi.org/project/opencv-python/), accessed 2026-11-23
9. [Ubuntu packages: libopencv-dev in jammy, noble and resolute](https://packages.ubuntu.com/search?keywords=libopencv-dev&searchon=names&suite=all&section=all), accessed 2026-11-23
10. [REP 2000: ROS 2 releases and target platforms](https://www.ros.org/reps/rep-2000.html), accessed 2026-11-23
11. [vision_opencv repository (cv_bridge, image_geometry), rolling branch](https://github.com/ros-perception/vision_opencv), accessed 2026-11-23
12. [rosdistro: distribution files and rosdep base.yaml and python.yaml](https://github.com/ros/rosdistro), accessed 2026-11-23
13. [ROS 2 docs (Jazzy): Using Python packages with ROS 2](https://docs.ros.org/en/jazzy/How-To-Guides/Using-Python-Packages.html), accessed 2026-11-23
14. [camera_calibration calibrator.py, jazzy branch (ArUco API switch)](https://github.com/ros-perception/image_pipeline/blob/jazzy/camera_calibration/src/camera_calibration/calibrator.py), accessed 2026-11-23
