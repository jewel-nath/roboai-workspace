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
| [Cyclone DDS](cyclone-dds.md) | library | ros2 | — | EPL-2.0 OR BSD-3-Clause | — | cli | 2026-11-18 |
| [Fast DDS](fast-dds.md) | library | ros2 | — | Apache-2.0 | — | cli | 2026-11-18 |
| [MAVROS](mavros.md) | library | ros2 | — | BSD-3-Clause OR GPL-3.0-only OR LGPL-3.0-only | — | cli | 2026-11-18 |
| [rmw_zenoh](rmw-zenoh.md) | library | ros2 | — | Apache-2.0 | — | cli | 2026-11-18 |
| [rosbridge_suite](rosbridge-suite.md) | library | ros2 | — | BSD-3-Clause | — | api | 2026-11-18 |
| [tf2](tf2.md) | library | ros2 | — | BSD-3-Clause | — | cli | 2026-11-18 |
| [URDF and xacro](urdf.md) | library | ros2 | — | BSD-3-Clause | — | script | 2026-11-18 |
<!-- index:end -->
