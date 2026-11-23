---
type: tool
name: Nav2
summary: The ROS 2 navigation stack; lifecycle-managed servers plan, follow and smooth paths over layered costmaps, run recovery behaviours, docking and routes, all driven by behaviour trees. Binaries for Humble to Lyrical, none for Rolling.
tags: [navigation, nav2, path-planning, path-following, costmap, behavior-tree, amcl, mppi, smac, collision-monitor, docking, route-server, lifecycle, ros2]
kind: framework
area: nav
support:
license: Apache-2.0 AND BSD-3-Clause AND LGPL-2.1-or-later AND MIT
links: {repo: "https://github.com/ros-navigation/navigation2", docs: "https://docs.nav2.org", site: }
version: {tested: , latest: 1.5.3, as_of: 2026-11-24}
platforms: [linux]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-24
sources:
  - {url: "https://github.com/ros-navigation/navigation2/tree/jazzy", title: "navigation2 jazzy branch: README, LICENSE, package.xml files, nav2_bringup launch and params, source", accessed: 2026-11-24}
  - {url: "https://github.com/ros-navigation/navigation2", title: "navigation2 repository: branches (humble, jazzy, kilted, lyrical, main), release tags, issue tracker", accessed: 2026-11-24}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/lyrical/getting_started/quickstart/quickstart/", title: "Nav2 docs: Quickstart", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/lyrical/configuration_and_development/first_time_robot_setup_guide/transformation/setup_transforms/", title: "Nav2 docs: Setting Up Transformations", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/lyrical/configuration_and_development/first_time_robot_setup_guide/odom/setup_odom/", title: "Nav2 docs: Setting Up Odometry", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/lyrical/configuration_and_development/navigation_plugins/", title: "Nav2 docs: Navigation Plugins", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/lyrical/configuration_and_development/migration_guides/Humble/", title: "Nav2 docs: Humble to Iron migration guide", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/lyrical/configuration_and_development/migration_guides/iron/Iron/", title: "Nav2 docs: Iron to Jazzy migration guide", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/lyrical/configuration_and_development/migration_guides/jazzy/Jazzy/", title: "Nav2 docs: Jazzy to Kilted migration guide", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/lyrical/configuration_and_development/migration_guides/kilted/Kilted/", title: "Nav2 docs: Kilted to Lyrical migration guide", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/lyrical/configuration_and_development/simple_commander_api/simple_commander_api/", title: "Nav2 docs: Simple Commander API", accessed: 2026-11-24}
---

# Nav2

Nav2 takes a goal pose and drives a ROS 2 ground robot there: it plans a path over a costmap,
follows it with a local controller, avoids obstacles, and runs recovery behaviours when stuck,
with behaviour trees deciding what runs when [1][7]. Builders use it to send a base to a pose,
through waypoints, onto a charging dock or along a route graph. Open Navigation LLC leads it [1];
`main` had a commit on 2026-11-23, Jazzy 1.3.14 and Lyrical 1.5.3 were tagged on 2026-10-16,
and 57 issues and 47 pull requests were open [2]. Licences differ per package: most are
Apache-2.0; DWB and code inherited from ROS 1 (costmap_2d, NavFn, map_server) is partly
BSD-3-Clause; `nav2_amcl` is LGPL-2.1-or-later; `nav2_mppi_controller` declares MIT [1].

## When to use it

- **Use it** for a ROS 2 robot on a floor or flat ground: differential, omni, mecanum or
  Ackermann bases, indoors or out, with a 2D lidar, depth camera or 3D lidar [7].
- **Pick plugins per robot.** Planners: NavFn, Smac 2D, Smac Hybrid-A\*, Smac Lattice, Theta\*.
  Controllers: DWB, Regulated Pure Pursuit, MPPI, Rotation Shim, Graceful [7]. See
  [Choose a Nav2 planner and controller](../guides/choose-a-nav2-planner-and-controller.md).
- **Use something else** for terrain that needs elevation ([grid_map](grid-map.md) plus your own
  layer), road vehicles ([Autoware](autoware.md)), arms (MoveIt 2) or fleet traffic (Open-RMF).

## Setup

```bash
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup 'ros-jazzy-nav2-minimal-tb*'
ros2 launch nav2_bringup tb3_simulation_launch.py headless:=False   # TurtleBot3 in Gazebo
```

In RViz, give a "2D Pose Estimate", then a goal with the Nav2 goal button [4]. Releases [3]:

| Distro | Release | Differences a builder meets |
|---|---|---|
| Humble | 1.1.20 | Docking is the separate `opennav_docking` 0.0.2; no loopback simulator |
| **Jazzy** | 1.3.14 | Route, docking, following and loopback simulator all released |
| Kilted | 1.4.2 (2025-09) | No following server; `cmd_vel` stamped by default; the branch has newer, unreleased backports [2] |
| Lyrical | 1.5.3 | Adds `nav2_ros_common`; stamped `cmd_vel` |
| Rolling | none | Build `main` from source [4] |

Branches are named after the distro; `main` is Rolling [2]. The docs give apt, source and Docker
installs for Linux only [4]; no package needs CUDA or a GPU [1]. Nav2's tutorials use the
[TurtleBot3](../robots/turtlebot3.md) [4].

## How an agent works with it

The skill [skills/nav-nav2/SKILL.md](../../skills/nav-nav2/SKILL.md) covers bring-up and tuning.
**Servers** (lifecycle nodes, composed into one process by default) [1][7]:

| Node | Job | Plugins it loads |
|---|---|---|
| `bt_navigator` | `navigate_to_pose`, `navigate_through_poses` actions; runs the BT XML | navigators, BT nodes |
| `planner_server` | Global path on the global costmap | `planner_plugins` (default NavFn) |
| `controller_server` | Follows the path on the local costmap | `controller_plugins` (MPPI in the shipped params; DWB if unset), goal and progress checkers |
| `smoother_server` | Smooths a path | Simple, Constrained, Savitzky-Golay |
| `behavior_server` | Recoveries | Spin, BackUp, DriveOnHeading, Wait, AssistedTeleop |
| `waypoint_follower` | Waypoint and GPS-waypoint missions | WaitAtWaypoint, PhotoAtWaypoint, InputAtWaypoint |
| `velocity_smoother`, `collision_monitor` | Limit acceleration; stop or slow on raw sensor data inside polygons | — |
| `docking_server`, `route_server` | Dock to chargers or other docks; route over a GeoJSON graph | dock plugins, edge scorers |

`localization_launch.py` adds `map_server` and `amcl`. `lifecycle_manager_navigation` and
`lifecycle_manager_localization` activate their `node_names` in order when `autostart` is true,
and bond to each (`bond_timeout` 4 s) [1]. In Jazzy, the controller and behaviours publish
`cmd_vel_nav`; `velocity_smoother` turns it into `cmd_vel_smoothed`; `collision_monitor`
publishes `cmd_vel` [1]. The global costmap (frame `map`) stacks static, obstacle and inflation
layers, the local one (`odom`, rolling) voxel and inflation [1]. Range and denoise layers exist,
and costmap filters add keepout zones, speed limits and binary toggles from mask maps [7].

**What the robot must provide** [5][6]:

- TF `map → odom` from a localizer (AMCL, [SLAM Toolbox](slam-toolbox.md)), `odom → base_link`
  from odometry (often [robot_localization](robot-localization.md)), and `base_link → <sensor>`
  from the [URDF](urdf.md) through robot_state_publisher, as REP 105 lays out.
- `nav_msgs/Odometry` on `odom`; a map (`map_server` YAML and image, or `/map` from SLAM);
  `LaserScan` on `scan`, or `PointCloud2` for the voxel layer.
- A base that obeys `cmd_vel`: `Twist` on Humble and Jazzy, `TwistStamped` from Kilted [9][10].

**Launch on a robot** (defaults: `slam` False, `use_sim_time` false, `autostart` true) [1]:

```bash
ros2 launch nav2_bringup bringup_launch.py map:=$HOME/maps/office.yaml \
  params_file:=$HOME/robot_ws/config/nav2.yaml   # or slam:=True to map while navigating
```

**Python** with `nav2_simple_commander`; tasks are non-blocking, so poll [12]:

```python
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
nav = BasicNavigator()
nav.waitUntilNav2Active()          # pass localizer='slam_toolbox' when mapping
nav.goToPose(goal)                 # goal: a PoseStamped in the map frame
while not nav.isTaskComplete():
    feedback = nav.getFeedback()
ok = nav.getResult() == TaskResult.SUCCEEDED
```

It also wraps waypoints, docking, spin, backup, `getPath`, costmap clearing and lifecycle
startup [1]. **Check:** `ros2 service call /lifecycle_manager_navigation/is_active
std_srvs/srv/Trigger` returns success; `ros2 run tf2_ros tf2_echo map base_link` resolves;
`ros2 topic info /cmd_vel -v` shows the type your base expects. In RViz the costmaps show the
walls with inflation, and the robot follows the path to the goal, in simulation first [4].

## Traps

- **Stuck inactive.** A costmap fails to activate if the robot base to global frame transform is
  missing for `initial_transform_timeout` (60 s) [1][9]. With AMCL there is no `map → odom` until
  an initial pose arrives: click "2D Pose Estimate", or set `set_initial_pose: true` [1].
- **Robot will not move.** Kilted and Lyrical publish `TwistStamped`; a base or Gazebo bridge
  that subscribes `Twist` never receives it [10]. Set `enable_stamped_cmd_vel` on every node that
  publishes or subscribes `cmd_vel`, or update the base [10]. Jazzy defaults to `Twist` [1].
- **Collision monitor blocks motion.** If a source has not published, is older than
  `source_timeout` (1.0 s in the Jazzy params) or cannot be transformed, it stops the robot
  [1][9]. Check sensor rates and TF first; `source_timeout: 0.0` disables the watchdog [9].
- **Humble configs on Jazzy.** Plugin names use `::` (`nav2_navfn_planner::NavfnPlanner`, not
  `/`) [9]; `progress_checker_plugin` became the list `progress_checker_plugins` [8]; BT XML moves
  from BehaviorTree.CPP 3 to 4 (a script converts it), and custom control or decorator nodes must
  handle `SKIPPED` [9]. See [BehaviorTree.CPP](behaviortree-cpp.md).
- **Jazzy configs on Kilted or Lyrical.** `map_topic` moves under the static layer [10]; MPPI
  needs a `motion_model` plugin entry such as `mppi::DiffDriveMotionModel` [11]; RPP's `stateful`
  moved to the goal checker [11]; `TruncatePathLocal` takes `robot_base_frame` [11]. Custom C++
  plugins must port to `nav2::LifecycleNode` from `nav2_ros_common` [11]. Start from your
  distro's `nav2_bringup/params/nav2_params.yaml`, never from `main`.
- **Footprint and frames.** The shipped params use `robot_radius: 0.22`, inflation radius 0.70 m
  and scaling 3.0, sized for a TurtleBot [1]. Set a `footprint` polygon or radius for your robot;
  too much inflation blocks doorways. AMCL and the collision monitor default to `base_footprint`,
  the costmaps to `base_link` [1]: match your URDF.
- **Sim time and bringup.** Pass `use_sim_time:=true` with Gazebo or bags, as a launch argument
  [1][8]. `nav2_bringup` pulls `ros_gz_sim`, `slam_toolbox` and the TurtleBot sims [1]; on a
  lean robot computer install `navigation2` and write your own launch.
- **Licence.** Only AMCL is LGPL: shipping a modified AMCL means sharing those changes. MPPI says
  MIT in `package.xml` and `LICENSE.md`, Apache-2.0 in its source headers [1].

## Alternatives

[linorobot2](linorobot2.md) configures Nav2 for a DIY base; [grid_map](grid-map.md) adds elevation;
[Autoware](autoware.md) drives road vehicles; [PythonRobotics](pythonrobotics.md) teaches planning.

## Sources

1. [navigation2 jazzy branch: README, LICENSE, package.xml files, nav2_bringup launch and params, source](https://github.com/ros-navigation/navigation2/tree/jazzy), accessed 2026-11-24
2. [navigation2 repository: branches (humble, jazzy, kilted, lyrical, main), release tags, issue tracker](https://github.com/ros-navigation/navigation2), accessed 2026-11-24
3. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-24
4. [Nav2 docs: Quickstart](https://docs.nav2.org/lyrical/getting_started/quickstart/quickstart/), accessed 2026-11-24
5. [Nav2 docs: Setting Up Transformations](https://docs.nav2.org/lyrical/configuration_and_development/first_time_robot_setup_guide/transformation/setup_transforms/), accessed 2026-11-24
6. [Nav2 docs: Setting Up Odometry](https://docs.nav2.org/lyrical/configuration_and_development/first_time_robot_setup_guide/odom/setup_odom/), accessed 2026-11-24
7. [Nav2 docs: Navigation Plugins](https://docs.nav2.org/lyrical/configuration_and_development/navigation_plugins/), accessed 2026-11-24
8. [Nav2 docs: Humble to Iron migration guide](https://docs.nav2.org/lyrical/configuration_and_development/migration_guides/Humble/), accessed 2026-11-24
9. [Nav2 docs: Iron to Jazzy migration guide](https://docs.nav2.org/lyrical/configuration_and_development/migration_guides/iron/Iron/), accessed 2026-11-24
10. [Nav2 docs: Jazzy to Kilted migration guide](https://docs.nav2.org/lyrical/configuration_and_development/migration_guides/jazzy/Jazzy/), accessed 2026-11-24
11. [Nav2 docs: Kilted to Lyrical migration guide](https://docs.nav2.org/lyrical/configuration_and_development/migration_guides/kilted/Kilted/), accessed 2026-11-24
12. [Nav2 docs: Simple Commander API](https://docs.nav2.org/lyrical/configuration_and_development/simple_commander_api/simple_commander_api/), accessed 2026-11-24
