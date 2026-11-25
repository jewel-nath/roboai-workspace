# Software

Libraries, frameworks and ROS 2 packages you build a robot's software on: navigation, SLAM,
motion planning, perception, control. Template: [templates/tool.md](../../templates/tool.md) with
`kind: library` or `kind: framework`.

- Name a file after the package: `nav2.md`, `slam-toolbox.md`, `moveit2.md`.
- Say which ROS 2 distros it supports and which one was tested.
- When several packages solve one problem, compare them in a decision guide in
  [guides/](../guides/) and link to it.

## Index

<!-- index:start -->
| Name | Kind | Area | Support | Licence | Tested | Agent access | Verified |
|---|---|---|---|---|---|---|---|
| [ros2_control](ros2-control.md) | framework | control | — | Apache-2.0 | — | script | 2026-11-18 |
| [TensorRT](tensorrt.md) | library | learning | — | Apache-2.0 | — | cli | 2026-11-25 |
| [cuRobo](curobo.md) | library | manip | — | Apache-2.0 | — | script | 2026-11-25 |
| [Drake](drake.md) | library | manip | — | BSD-3-Clause | — | script | 2026-11-25 |
| [MoveIt 2](moveit2.md) | framework | manip | — | BSD-3-Clause | — | cli | 2026-11-25 |
| [OMPL](ompl.md) | library | manip | — | BSD-3-Clause | — | script | 2026-11-25 |
| [Pinocchio](pinocchio.md) | library | manip | — | BSD-2-Clause | — | script | 2026-11-25 |
| [Robotics Toolbox for Python](robotics-toolbox-python.md) | library | manip | — | MIT | — | script | 2026-11-25 |
| [Autoware](autoware.md) | framework | nav | — | Apache-2.0 | — | cli | 2026-11-24 |
| [BehaviorTree.CPP](behaviortree-cpp.md) | library | nav | — | MIT | — | cli | 2026-11-24 |
| [grid_map](grid-map.md) | library | nav | — | BSD-3-Clause | — | cli | 2026-11-24 |
| [linorobot2](linorobot2.md) | framework | nav | — | Apache-2.0 | — | cli | 2026-11-24 |
| [Nav2](nav2.md) | framework | nav | — | Apache-2.0 AND BSD-3-Clause AND LGPL-2.1-or-later AND MIT | — | cli | 2026-11-24 |
| [Open-RMF](open-rmf.md) | framework | nav | — | Apache-2.0 | — | script | 2026-11-25 |
| [PythonRobotics](pythonrobotics.md) | library | nav | — | MIT | — | script | 2026-11-24 |
| [AprilTag](apriltag.md) | library | perception | — | BSD-2-Clause | — | cli | 2026-11-23 |
| [Cartographer](cartographer.md) | library | perception | — | Apache-2.0 | — | cli | 2026-11-23 |
| [GTSAM](gtsam.md) | library | perception | — | BSD-3-Clause | — | script | 2026-11-23 |
| [image_pipeline](image-pipeline.md) | library | perception | — | BSD-3-Clause AND Apache-2.0 | — | cli | 2026-11-23 |
| [Kalibr](kalibr.md) | tool | perception | — | BSD-4-Clause AND LGPL-3.0-or-later | — | cli | 2026-11-23 |
| [KISS-ICP](kiss-icp.md) | library | perception | — | MIT | — | cli | 2026-11-23 |
| [LIO-SAM](lio-sam.md) | library | perception | — | BSD-3-Clause | — | cli | 2026-11-23 |
| [OctoMap](octomap.md) | library | perception | — | BSD-3-Clause | — | cli | 2026-11-23 |
| [Open3D](open3d.md) | library | perception | — | MIT | — | script | 2026-11-23 |
| [OpenCV](opencv.md) | library | perception | — | Apache-2.0 | — | script | 2026-11-23 |
| [OpenVINS](openvins.md) | library | perception | — | GPL-3.0-or-later | — | cli | 2026-11-23 |
| [ORB-SLAM3](orb-slam3.md) | library | perception | — | GPL-3.0-or-later | — | cli | 2026-11-23 |
| [PCL (Point Cloud Library)](pcl.md) | library | perception | — | BSD-3-Clause | — | cli | 2026-11-23 |
| [robot_localization](robot-localization.md) | library | perception | — | BSD-3-Clause | — | cli | 2026-11-23 |
| [RTAB-Map](rtab-map.md) | library | perception | — | BSD-3-Clause | — | cli | 2026-11-23 |
| [SLAM Toolbox](slam-toolbox.md) | library | perception | — | LGPL-2.1-only AND LGPL-3.0-or-later | — | cli | 2026-11-23 |
| [VINS-Fusion](vins-fusion.md) | library | perception | — | GPL-3.0-only | — | cli | 2026-11-23 |
| [Cyclone DDS](cyclone-dds.md) | library | ros2 | — | EPL-2.0 OR BSD-3-Clause | — | cli | 2026-11-18 |
| [Fast DDS](fast-dds.md) | library | ros2 | — | Apache-2.0 | — | cli | 2026-11-18 |
| [MAVROS](mavros.md) | library | ros2 | — | BSD-3-Clause OR GPL-3.0-only OR LGPL-3.0-only | — | cli | 2026-11-18 |
| [rmw_zenoh](rmw-zenoh.md) | library | ros2 | — | Apache-2.0 | — | cli | 2026-11-18 |
| [rosbridge_suite](rosbridge-suite.md) | library | ros2 | — | BSD-3-Clause | — | api | 2026-11-18 |
| [SROS2](sros2.md) | tool | ros2 | — | Apache-2.0 | — | cli | 2026-11-25 |
| [tf2](tf2.md) | library | ros2 | — | BSD-3-Clause | — | cli | 2026-11-18 |
| [URDF and xacro](urdf.md) | library | ros2 | — | BSD-3-Clause | — | script | 2026-11-18 |
<!-- index:end -->
