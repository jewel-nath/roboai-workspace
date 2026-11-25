# Package layout and the top-level launch (Jazzy)

Part of [arch-robot-architecture](../SKILL.md). Which packages a robot has, what goes in each, how they
depend on each other, and one launch file that starts the layers. `CMakeLists.txt`, `setup.py` and
`package.xml` for each build type are in [ros2-core](../../ros2-core/references/packages.md).

## The packages

| Package | Holds | Build type | Written up in |
|---|---|---|---|
| `my_robot_description` | `urdf/` (xacro), `meshes/`, `rviz/`, a display launch | `ament_cmake` | [ros2-robot-description](../../ros2-robot-description/SKILL.md) |
| `my_robot_interfaces` | `msg/`, `srv/`, `action/` and nothing else | `ament_cmake` + rosidl | [interfaces.md](interfaces.md) |
| `my_robot_hardware` | the ros2_control hardware interface plugin and its bus code | `ament_cmake`, C++ | [ros2-control](../../ros2-control/SKILL.md) |
| `my_robot_bringup` | `launch/`, `config/` (`controllers.yaml`, `analyzers.yaml`, lifecycle lists); no nodes | `ament_cmake` | this file |
| `my_robot_localization` | `config/ekf.yaml`, launch | `ament_cmake` | [perception-slam](../../perception-slam/SKILL.md) |
| `my_robot_perception` | your perception nodes | `ament_cmake` or `ament_python` | [perception-camera](../../perception-camera/SKILL.md), [perception-lidar](../../perception-lidar/SKILL.md) |
| `my_robot_navigation` | `config/nav2_params.yaml`, `maps/`, `behavior_trees/`, launch | `ament_cmake` | [nav-nav2](../../nav-nav2/SKILL.md) |
| `my_robot_behavior` | the mission node, its trees or state machines | `ament_cmake` (C++) or `ament_python` | [behavior-layer.md](behavior-layer.md) |

Only when the robot needs them:

| Package | Holds |
|---|---|
| `my_robot_driver` | a device node that is not a ros2_control component (a custom sensor, a display, a lift) |
| `my_robot_control` | your own controller plugins (most robots use `ros2_controllers` as shipped) |
| `my_robot_moveit_config` | MoveIt 2 configuration ([manip-moveit2](../../manip-moveit2/SKILL.md)) |
| `my_robot_gazebo` | worlds, bridge config, simulation launch ([sim-gazebo](../../sim-gazebo/SKILL.md)) |

Names follow REP 144: lowercase letters, digits and underscores, starting with a letter. Prefixing every
package with the robot's name keeps a workspace with two robots, or with upstream packages, readable.

## Dependency rules

```text
my_robot_bringup ──exec_depend──> every package it launches
my_robot_behavior ──> my_robot_interfaces, nav2_msgs, control_msgs
my_robot_navigation ──> nav2_bringup                 (configuration only)
my_robot_perception ──> my_robot_interfaces, sensor_msgs
my_robot_hardware ──> hardware_interface, pluginlib
my_robot_description ──> xacro, robot_state_publisher (exec)
my_robot_interfaces ──> std_msgs, geometry_msgs, ... (definitions only)
```

- Dependencies point down the layers. Nothing depends on `my_robot_bringup`, and no node package depends
  on another node package: they share `my_robot_interfaces`, never each other's code.
- `my_robot_interfaces` holds no nodes, so tools, a web UI or another robot can build against it alone.
- Config lives in the package whose launch file loads it. A package another robot could reuse (a driver,
  the hardware interface) takes its robot-specific values from launch arguments and parameter files, not
  from constants in code.
- Hardware-specific choices (which hardware plugin, mock or real) are launch arguments passed into the
  description, so the same packages run on the robot, on mock hardware and in Gazebo.

Check the graph:

```bash
colcon list --topological-order          # interfaces and description early, bringup late
colcon graph                             # look for cycles and for packages depending on bringup
rosdep install --from-paths src --ignore-src -y && colcon build    # clean workspace: rm -rf build install log first
```

## The top-level launch file

One entry point starts every layer by including each package's own launch file. The layer launch files
(`robot.launch.py` from [ros2-control](../../ros2-control/references/urdf-yaml-launch.md),
`ekf.launch.py` from [perception-slam](../../perception-slam/references/robot-localization.md),
`navigation.launch.py` from [nav-nav2](../../nav-nav2/references/launch.md)) stay usable on their own.

```python
# my_robot_bringup/launch/robot.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, SetParameter
from launch_ros.substitutions import FindPackageShare


def include(package, launch_file, arguments=None):
    """Include <package>/launch/<launch_file>, passing launch arguments."""
    return IncludeLaunchDescription(
        PathJoinSubstitution([FindPackageShare(package), 'launch', launch_file]),
        launch_arguments=(arguments or {}).items())


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    analyzers = PathJoinSubstitution(
        [FindPackageShare('my_robot_bringup'), 'config', 'analyzers.yaml'])

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument('hardware', default_value='real', description='mock or real'),
        DeclareLaunchArgument('map', description='Absolute path to the map YAML file'),
        DeclareLaunchArgument('use_behavior', default_value='true'),

        # Applies to every node below, including those in included files
        SetParameter(name='use_sim_time', value=use_sim_time),

        # Drivers and control: robot_state_publisher, ros2_control_node, spawners
        include('my_robot_bringup', 'robot.launch.py',
                {'hardware': LaunchConfiguration('hardware')}),
        # Drivers that are not ros2_control components, under their lifecycle manager
        include('my_robot_bringup', 'sensors.launch.py'),
        # Estimation: odom -> base_link
        include('my_robot_localization', 'ekf.launch.py'),
        # Planning, with AMCL for map -> odom
        include('my_robot_navigation', 'navigation.launch.py',
                {'map': LaunchConfiguration('map'), 'use_sim_time': use_sim_time}),
        # Health for the operator view
        Node(package='diagnostic_aggregator', executable='aggregator_node',
             parameters=[analyzers], output='screen'),
        # Behavior: the mission waits for the action servers it uses
        GroupAction([include('my_robot_behavior', 'behavior.launch.py')],
                    condition=IfCondition(LaunchConfiguration('use_behavior'))),
    ])
```

- Launch starts every process at once; the order of lines is not a start-up order. Order comes from
  lifecycle managers ([lifecycle-composition.md](lifecycle-composition.md)) and from clients waiting for
  their servers (`wait_for_action_server`, `action_server_is_ready()`).
- `IncludeLaunchDescription` takes a path to a `.py`, `.xml` or `.yaml` launch file directly in Jazzy;
  Humble needs `PythonLaunchDescriptionSource(...)` around it.
- `SetParameter` before the includes reaches every node in them; pass `use_sim_time` to Nav2 as well, since
  its bringup declares its own argument.
- Keep the arguments few (`use_sim_time`, `hardware`, `map`, feature switches). Everything else belongs in
  the parameter files, where it is reviewed and versioned.
- For two or more robots this file runs once per robot in its namespace: [multi-robot.md](multi-robot.md).
  Running it at boot under systemd: [ops-bringup](../../ops-bringup/SKILL.md).

Check:

```bash
ros2 launch my_robot_bringup robot.launch.py --show-args     # the four arguments, with defaults
ros2 launch my_robot_bringup robot.launch.py hardware:=mock map:=$HOME/maps/my_map.yaml
ros2 node list                                                  # each node once
```

Sources: docs.ros.org Jazzy (Using ROS 2 launch for large projects; Creating a package), REP 144,
the `launch` and `launch_ros` `jazzy` branches (`IncludeLaunchDescription`, `SetParameter`).
