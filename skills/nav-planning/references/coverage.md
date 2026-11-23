# Coverage paths with opennav_coverage

Part of [nav-planning](../SKILL.md). Checked against `open-navigation/opennav_coverage` (branches `jazzy`
and `jazzy-v2`, the latter at commit c02a41e, 2026-08-03), Fields2Cover 2.1.1 and ros/rosdistro on
2026-11-24. Not built for this skill.

## What it is

`opennav_coverage` (Apache-2.0, Open Navigation) wraps Fields2Cover (BSD-3-Clause) as Nav2 task servers:
given a field polygon it removes a headland, lays out parallel swaths, orders them (boustrophedon, snake,
spiral or custom) and joins them with Dubins or Reeds-Shepp turns. Its packages:

| Package | Gives |
|---|---|
| `opennav_coverage_msgs` | the actions and messages below |
| `opennav_coverage` | `coverage_server`: action `compute_coverage_path` (`opennav_coverage_msgs/action/ComputeCoveragePath`) for open fields |
| `opennav_row_coverage` | `row_coverage_server`: the same from pre-annotated rows (orchards, vineyards) |
| `opennav_coverage_navigator` | BT navigator plugin `opennav_coverage_navigator/CoverageNavigator`, action `navigate_complete_coverage` |
| `opennav_coverage_bt` | BT nodes and XMLs, e.g. `navigate_w_basic_complete_coverage.xml` |
| `opennav_coverage_demo` | Gazebo demo, params and a Python client |

It suits mowing, field work and large cleaning areas. For a room-cleaning robot with many obstacles, a cell
decomposition of the map plus waypoints (see the boustrophedon note in [prototyping.md](prototyping.md))
may be simpler.

## Install on Jazzy (source only)

No ROS distro releases `opennav_coverage`; Fields2Cover itself has a Jazzy binary
(`ros-jazzy-fields2cover`, 2.1.1). Two branches target Jazzy:

| Branch | Fields2Cover | Note |
|---|---|---|
| `jazzy-v2` | v2 (README: verified with v2.0.0; "available as a binary on Jazzy") | Use this first |
| `jazzy` | v1.2.1 from source (`v1.2.1-devel` branch) | Older API; last commit 2024-12 |

The Jazzy binary is 2.1.1, newer than the v2.0.0 the README names; if the build fails on Fields2Cover
API, build Fields2Cover v2.0.0 from source in the same workspace.

```bash
sudo apt install ros-jazzy-fields2cover libgdal-dev
mkdir -p ~/coverage_ws/src && cd ~/coverage_ws/src
git clone --branch jazzy-v2 https://github.com/open-navigation/opennav_coverage.git
cd ~/coverage_ws
rosdep install --from-paths src -i -y --rosdistro jazzy
colcon build --symlink-install
source install/setup.bash
```

Check: `ros2 pkg list | grep -E "opennav_(row_)?coverage"` lists the six packages; the demo
(`ros2 launch opennav_coverage_demo coverage_demo_launch.py`, Gazebo Harmonic) covers a field with a
simulated TurtleBot.

## Configure

Run `coverage_server` next to the controller server, BT navigator and velocity smoother (the demo's
`bringup_launch.py` composes them in one container and adds `coverage_server` to the lifecycle manager's
`node_names`). Server parameters (names from the README and demo params):

```yaml
coverage_server:
  ros__parameters:
    robot_width: 0.7                     # m
    operation_width: 0.7                 # m, the tool or brush width; swath spacing
    min_turning_radius: 0.35             # m, for the turns between swaths
    linear_curv_change: 200.0
    coordinates_in_cartesian_frame: true # false for GPS coordinates
    default_headland_width: 0.25         # m removed around the border
    default_swath_angle_type: "BRUTE_FORCE"   # or SET_ANGLE with default_swath_angle
    default_swath_type: "LENGTH"         # LENGTH, COVERAGE or NUMBER objective
    default_route_type: "BOUSTROPHEDON"  # SNAKE, SPIRAL, CUSTOM
    default_path_type: "DUBIN"           # REEDS_SHEPP if it may reverse in turns
    default_path_continuity_type: "CONTINUOUS"
    default_turn_point_distance: 0.1     # m between points in the turns

bt_navigator:
  ros__parameters:
    navigators: ["navigate_complete_coverage"]
    navigate_complete_coverage:
      plugin: "opennav_coverage_navigator/CoverageNavigator"
    error_code_names: ["compute_path_error_code", "follow_path_error_code", "compute_coverage_error_code"]
    plugin_lib_names:
      - opennav_compute_complete_coverage_action_bt_node
      - opennav_cancel_complete_coverage_action_bt_node
```

Each `default_*` value can be overridden per request through the `*_mode` fields of the action goal.
Follow the coverage path with a tracking controller (RPP, or MPPI with strong `PathAlignCritic`), not a
controller tuned to leave the path around obstacles.

## Run

The whole task through the navigator (closed polygon: repeat the first point):

```bash
ros2 action send_goal /navigate_complete_coverage opennav_coverage_msgs/action/NavigateCompleteCoverage \
  "{frame_id: map, polygons: [{points: [{x: 5.0, y: 5.0}, {x: 5.0, y: 15.0}, {x: 15.0, y: 15.0},
    {x: 10.0, y: 5.0}, {x: 5.0, y: 5.0}]}]}" --feedback
```

Only the path, to inspect or to follow with your own logic:

```bash
ros2 action send_goal /compute_coverage_path opennav_coverage_msgs/action/ComputeCoveragePath \
  "{frame_id: map, generate_headland: true, generate_route: true, generate_path: true,
    polygons: [{coordinates: [{axis1: 5.0, axis2: 5.0}, {axis1: 5.0, axis2: 15.0},
    {axis1: 15.0, axis2: 15.0}, {axis1: 5.0, axis2: 5.0}]}]}"
```

The result has `nav_path` (a `nav_msgs/Path` a controller can follow), `coverage_path` (swaths and turns
separately, for tool on/off), `planning_time` and `error_code` (801 to 803 on failure). Polygons can
also come from a GML file (`use_gml_file: true`, `gml_field`).

## Checks

- `coverage_server/field_boundary`, `planning_field`, `swaths` and `coverage_plan` line up with the map
  in RViz (they publish only while something subscribes).
- Swath spacing equals `operation_width`; turns respect `min_turning_radius`.
- The robot finishes the demo field without recoveries; repeat on your own polygon in simulation first.
