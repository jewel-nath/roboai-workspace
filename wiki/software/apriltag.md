---
type: tool
name: AprilTag
summary: AprilTag 3 visual fiducials for pose, docking and calibration targets; the BSD-2-Clause C library from AprilRobotics (3.4.5) plus christianrauch's MIT-licensed apriltag_ros node, which is the package released for Humble to Rolling. AprilRobotics' own apriltag_ros is ROS 1 only.
tags: [apriltag, fiducial, marker, tag36h11, tagstandard41h12, apriltag-ros, apriltag-msgs, apriltag-detector, pose-estimation, docking, ros2]
kind: library
area: perception
support:
license: BSD-2-Clause
links: {repo: "https://github.com/AprilRobotics/apriltag", docs: "https://github.com/AprilRobotics/apriltag/wiki/AprilTag-User-Guide", site: "https://april.eecs.umich.edu/software/apriltag"}
version: {tested: , latest: 3.4.5, as_of: 2026-11-23}
platforms: [linux]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/AprilRobotics/apriltag", title: "AprilRobotics/apriltag: README, LICENSE.md, package.xml, tags, master history", accessed: 2026-11-23}
  - {url: "https://github.com/christianrauch/apriltag_ros", title: "christianrauch/apriltag_ros: README, LICENSE, package.xml, cfg/tags_36h11.yaml, AprilTagNode.cpp, tags", accessed: 2026-11-23}
  - {url: "https://github.com/AprilRobotics/apriltag_ros", title: "AprilRobotics/apriltag_ros (ROS 1 wrapper): README, package.xml, history", accessed: 2026-11-23}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro: humble, jazzy, kilted, lyrical and rolling distribution.yaml", accessed: 2026-11-23}
  - {url: "https://github.com/ros-misc-utilities/apriltag_detector", title: "ros-misc-utilities/apriltag_detector README; apriltag_mit package.xml", accessed: 2026-11-23}
---

# AprilTag

Printed square markers whose ID and 6-DoF pose a camera recovers, for docking, fixture and object
poses, ground truth and calibration boards. AprilTag 3 is a small C library with a Python wrapper,
BSD-2-Clause; last release v3.4.5 (2025-08-29), commits on master to August 2026 [1].

## Which apriltag_ros

**Use christianrauch/apriltag_ros** (MIT): rosdistro releases it as `apriltag_ros`, at 3.4.0
(2026-05-23) for Humble, Jazzy, Lyrical and Rolling, 3.2.2 for Kilted; commits to November 2026
[2][4]. **AprilRobotics/apriltag_ros** is a ROS 1 catkin package (Kinetic, Melodic), last commit
March 2023, with no ROS 2 branch; its tutorials do not apply [3].

## When to use it

For known places and objects found cheaply; [Kalibr](kalibr.md)'s Aprilgrid uses the same tags.
Natural objects need learned models such as [FoundationPose](../learning/models/foundationpose.md).

## Setup

```bash
sudo apt install ros-jazzy-apriltag-ros   # pulls apriltag 3.4.5, image_proc, camera_ros
ros2 run apriltag_ros apriltag_node --ros-args \
  -r image_rect:=/camera/image_rect -r camera_info:=/camera/camera_info \
  -p family:=36h11 -p size:=0.162 -p qos_profile:=sensor_data \
  -p tag.ids:="[0, 7]" -p tag.frames:="[dock, shelf]"
```

Alone, the library builds with CMake on Linux, its one official platform, plus a Python module
(`from apriltag import apriltag`) [1]. Print tags from the apriltag-imgs repo [1].

## How an agent works with it

The node needs rectified `image_rect` and `camera_info` with equal stamps (pose uses `P`). It
publishes TF from the image frame to `tag36h11:<id>` or the named frame, plus `detections` with
hamming distance and decision margin; `pose_estimation_method` is `pnp` or `homography` [2].
Check with `tf2_echo` and a tape measure; a higher `detector.decimate` (default 2.0) is faster with
less range [1][2]. Inputs come from [image_pipeline](image-pipeline.md).

## Traps

- **Wrong tag size.** `size` is the edge where the black and white borders meet, not the outside;
  newer layouts put data bits outside the border [1]. A wrong size scales every distance.
- **No images arrive.** The QoS default is reliable, which matches no best-effort camera: set
  `qos_profile: sensor_data`. Uncalibrated `camera_info` warns "The camera is not calibrated!" [2].
- **Family mismatch.** The node defaults to 36h11, the library recommends tagStandard41h12 [1][2];
  set the family of the tags you printed.
- **Docs ahead of releases.** ArUco families (library) and `tag_bundles` (node) exist only on
  master, after v3.4.5 and 3.4.0 [1][2]; build from source to use them.
- **Tag axes.** Seen from the camera, x points right, y down, z into the tag [1]; publish a static
  transform from the tag frame to the dock or object frame you need.

## Alternatives

- apriltag_detector (Apache-2.0, Jazzy 3.1.0): detection only, no pose; its MIT-detector plugin
  needs apriltag_mit, which is LGPL-2.1 [4][5]. NVIDIA's Isaac ROS has its own AprilTag package
  (Isaac ROS comes in a later batch); ArUco markers in [OpenCV](opencv.md).

## Sources

1. [AprilRobotics/apriltag: README, LICENSE.md, package.xml, tags, master history](https://github.com/AprilRobotics/apriltag), accessed 2026-11-23
2. [christianrauch/apriltag_ros: README, LICENSE, package.xml, cfg/tags_36h11.yaml, AprilTagNode.cpp, tags](https://github.com/christianrauch/apriltag_ros), accessed 2026-11-23
3. [AprilRobotics/apriltag_ros (ROS 1 wrapper): README, package.xml, history](https://github.com/AprilRobotics/apriltag_ros), accessed 2026-11-23
4. [rosdistro: humble, jazzy, kilted, lyrical and rolling distribution.yaml](https://github.com/ros/rosdistro), accessed 2026-11-23
5. [ros-misc-utilities/apriltag_detector README; apriltag_mit package.xml](https://github.com/ros-misc-utilities/apriltag_detector), accessed 2026-11-23
