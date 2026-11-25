# Nav2 package, launch and lifecycle (Jazzy)

Part of [nav-nav2](../SKILL.md). Checked against `nav2_bringup` 1.3.14 (`jazzy` branch). Generic launch-file and
lifecycle mechanics are in [ros2-core](../../ros2-core/references/launch.md).

## Package layout

```text
my_robot_navigation/
  package.xml
  CMakeLists.txt
  config/nav2_params.yaml        # copied from nav2_bringup, then edited (params.md)
  maps/my_map.yaml, my_map.pgm   # from map_saver_cli or slam_toolbox save_map
  behavior_trees/                # custom trees, if any (behavior-trees.md)
  launch/navigation.launch.py
```

`package.xml`: `<buildtool_depend>ament_cmake</buildtool_depend>`, then `<exec_depend>` on `nav2_bringup`,
`navigation2` and, if used, `slam_toolbox` (LGPL-2.1) and `nav2_map_server`. `CMakeLists.txt`:

```cmake
install(DIRECTORY config launch maps behavior_trees DESTINATION share/${PROJECT_NAME})
```

`nav2_bringup` itself is an example; its README expects each robot to keep its own copy of the configuration and
launch files like this package.

## Launch file

```python
# my_robot_navigation/launch/navigation.launch.py
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    nav2_launch_dir = os.path.join(get_package_share_directory('nav2_bringup'), 'launch')
    pkg_dir = get_package_share_directory('my_robot_navigation')
    use_sim_time = LaunchConfiguration('use_sim_time')

    arguments = [
        DeclareLaunchArgument('map', default_value=os.path.join(pkg_dir, 'maps', 'my_map.yaml')),
        DeclareLaunchArgument(
            'params_file', default_value=os.path.join(pkg_dir, 'config', 'nav2_params.yaml')),
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        # nav2_bringup evaluates these as Python: pass True or False, capitalized
        DeclareLaunchArgument('slam', default_value='False'),
        DeclareLaunchArgument('use_localization', default_value='True'),
        DeclareLaunchArgument('use_composition', default_value='True'),
        DeclareLaunchArgument('use_respawn', default_value='False'),
        DeclareLaunchArgument('use_rviz', default_value='true'),
    ]

    bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_launch_dir, 'bringup_launch.py')),
        launch_arguments={
            'map': LaunchConfiguration('map'),
            'params_file': LaunchConfiguration('params_file'),
            'use_sim_time': use_sim_time,
            'slam': LaunchConfiguration('slam'),
            'use_localization': LaunchConfiguration('use_localization'),
            'use_composition': LaunchConfiguration('use_composition'),
            'use_respawn': LaunchConfiguration('use_respawn'),
            'autostart': 'true',
        }.items(),
    )

    rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_launch_dir, 'rviz_launch.py')),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
        condition=IfCondition(LaunchConfiguration('use_rviz')),
    )

    return LaunchDescription(arguments + [bringup, rviz])
```

Run it after the robot's own bringup (drivers, `robot_state_publisher`, drive controller):

```bash
ros2 launch my_robot_navigation navigation.launch.py map:=/home/<user>/maps/my_map.yaml
ros2 launch my_robot_navigation navigation.launch.py slam:=True              # navigate while mapping
ros2 launch my_robot_navigation navigation.launch.py use_localization:=False # localization started elsewhere
```

## What `bringup_launch.py` starts

| Part | Started when | Nodes |
|---|---|---|
| `nav2_container` (`component_container_isolated`) | `use_composition:=True` (its default) | holds the localization and navigation nodes; SLAM runs outside it |
| `localization_launch.py` | not `slam`, `use_localization` | `map_server` (`yaml_filename` from `map:=`), `amcl`, `lifecycle_manager_localization` |
| `slam_launch.py` | `slam` and `use_localization` | slam_toolbox `online_sync_launch.py`, `map_saver` server, `lifecycle_manager_slam` |
| `navigation_launch.py` | always | `controller_server`, `smoother_server`, `planner_server`, `route_server`, `behavior_server`, `velocity_smoother`, `collision_monitor`, `bt_navigator`, `waypoint_follower`, `docking_server`, `lifecycle_manager_navigation` |

- `navigation_launch.py` remaps `cmd_vel` to `cmd_vel_nav` on the controller, behavior server and velocity smoother;
  the collision monitor then writes `/cmd_vel`. The docking server is not remapped and writes `/cmd_vel` directly.
- `slam_launch.py` passes your parameter file to slam_toolbox only if it contains a `slam_toolbox:` section;
  otherwise slam_toolbox runs its own defaults. Mapping parameters: [perception-slam](../../perception-slam/references/slam-toolbox.md).
- For slam_toolbox in localization mode, launch its `localization_launch.py` yourself and this file with
  `use_localization:=False`, so no AMCL or `map_server` runs beside it.
- `use_sim_time` is applied to every node with `SetParameter`; RViz gets it from `rviz_launch.py`.

## Composition and respawn

- Composed (default for `bringup_launch.py`): one process, less CPU and memory, intra-process handoff. A crash in
  any node takes all of them down, and `use_respawn` has no effect.
- `use_composition:=False use_respawn:=True`: one process per server; a crashed server restarts after 2 s and the
  lifecycle manager reconnects within `bond_respawn_max_duration` (10 s).
- `navigation_launch.py` or `localization_launch.py` alone with `use_composition:=True` load into an existing
  container named `nav2_container`; without one they wait forever.

## Lifecycle manager

Each manager takes `node_names` (ordered) and `autostart`. It configures and activates the nodes in order,
deactivates them in reverse, and watches them with bonds (`bond_timeout`, 4.0 s). If a node fails a transition,
bringup stops (`Failed to bring up all requested nodes. Aborting bringup.`); a bond that does not form logs
`Server <name> was unable to be reached after 4.00s by bond.`; a bond that breaks later brings the group down.

```bash
ros2 service call /lifecycle_manager_navigation/is_active std_srvs/srv/Trigger
# command: 0 STARTUP, 1 PAUSE, 2 RESUME, 3 RESET, 4 SHUTDOWN
ros2 service call /lifecycle_manager_navigation/manage_nodes nav2_msgs/srv/ManageLifecycleNodes "{command: 0}"
ros2 lifecycle get /controller_server            # active [3]
ros2 lifecycle get /amcl
```

- With `autostart: false` the nodes wait in `unconfigured` (`Waiting on external lifecycle transitions to
  activate`); start them with the service above, the RViz Nav2 panel's Startup button, or
  `BasicNavigator.lifecycleStartup()`.
- Activation order matters: the global costmap (in `planner_server`) waits up to `initial_transform_timeout`
  (60 s) for `map` → `base_link`. With AMCL, give the initial pose inside that minute.
- A debugger, a slow disk or a starved CPU can miss the bond and take the stack down; raise `bond_timeout` while
  debugging rather than setting it to 0.

## Namespaces

`use_namespace:=True namespace:=robot1` pushes every node into `/robot1` and rewrites the parameter file under that
root key; `/tf` and `/tf_static` are remapped to relative names. The robot's own drivers and TF must use the same
namespace. Several robots on one network belong to [ops-fleet](../../ops-fleet/SKILL.md).

## In simulation

1. Start the robot in Gazebo with [sim-gazebo](../../sim-gazebo/SKILL.md): `/clock` bridged from Gazebo, the lidar
   with `gz_frame_id` set, odometry and `odom` → `base_link` from one source, a drive that takes `/cmd_vel`.
2. `ros2 launch my_robot_navigation navigation.launch.py use_sim_time:=True map:=<world map>`.
3. Command type: Gazebo's DiffDrive system through `ros_gz_bridge` takes `Twist`, Jazzy's default;
   `gz_ros2_control` with `diff_drive_controller` needs `enable_stamped_cmd_vel: true` ([params.md](params.md)).

Without physics: `ros2 launch nav2_bringup tb3_loopback_simulation.launch.py` runs Nav2 on
`nav2_loopback_sim`, which integrates `cmd_vel` into perfect odometry, publishes `map` → `odom`, teleports on
`/initialpose`, and fakes `/scan` by ray-casting the map, so only mapped obstacles exist. For your robot, run
`ros2 run nav2_loopback_sim loopback_simulator` with `base_frame_id`, `odom_frame_id`, `map_frame_id` and
`scan_frame_id` set, instead of Gazebo.

## Checks

- `ros2 node list` shows every node in the table above (or `/nav2_container` plus `ros2 component list`).
- Both lifecycle managers log `Managed nodes are active`; `is_active` returns `success: true`.
- `ros2 param get /bt_navigator use_sim_time` matches the run (true in simulation only).
