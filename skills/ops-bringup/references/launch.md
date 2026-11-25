# The bringup package and its launch layers (Jazzy)

Part of [ops-bringup](../SKILL.md). Checked against launch 3.4 and launch_ros 0.26 (`jazzy`
branches). General launch syntax is in [ros2-core](../../ros2-core/references/launch.md); the
controller YAML in [ros2-control](../../ros2-control/references/urdf-yaml-launch.md).

## Layout

```text
my_robot_bringup/
  package.xml               # exec_depend on every package the launch files start, and the RMW
  CMakeLists.txt
  launch/
    robot.launch.py         # top level: includes the layers below
    description.launch.py   # robot_state_publisher from my_robot_description
    control.launch.py       # ros2_control_node and the spawner
    drivers.launch.py       # sensors and other device drivers
    localization.launch.py  # robot_localization EKF
    diagnostics.launch.py   # aggregator and host monitors (diagnostics.md)
  config/                   # controllers.yaml, drivers.yaml, ekf.yaml, diagnostics.yaml
  scripts/wait_ready.py     # readiness check (readiness.md)
  host/                     # copies of the files installed on the robot computer:
                            # systemd units, env.sh, udev rules, chrony and journald snippets
```

Navigation and manipulation keep their own packages (`my_robot_navigation`,
`my_robot_moveit_config`) and come in as layers. The `host/` folder is not installed by colcon; it
is the source the setup steps copy into `/etc` (and what `ops-fleet` deploys).

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_bringup)
find_package(ament_cmake REQUIRED)
install(DIRECTORY launch config DESTINATION share/${PROJECT_NAME})
install(PROGRAMS scripts/wait_ready.py DESTINATION lib/${PROJECT_NAME})
ament_package()
```

`package.xml` lists `<exec_depend>` for `robot_state_publisher`, `xacro`, `controller_manager`,
`robot_localization`, `diagnostic_aggregator`, `diagnostic_common_diagnostics`, `rclpy`,
`tf2_ros_py`, `rosidl_runtime_py`, your own packages, and the RMW you use (`rmw_cyclonedds_cpp`
or `rmw_zenoh_cpp`), so `rosdep install` puts all of them on the robot.

## Top level: `robot.launch.py`

```python
# my_robot_bringup/launch/robot.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import EqualsSubstitution, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import SetParameter
from launch_ros.substitutions import FindPackageShare

ARGUMENTS = [  # name, default, description
    ('hardware', 'real', 'real, mock or gz'),
    ('use_sim_time', 'false', 'true when running in Gazebo'),
    ('use_localization', 'true', 'start the EKF'),
    ('use_navigation', 'false', 'include my_robot_navigation'),
    ('use_manipulation', 'false', 'include move_group from my_robot_moveit_config'),
    ('use_diagnostics', 'true', 'aggregator and host monitors'),
    ('map', '/home/robot/maps/my_map.yaml', 'map for navigation (example path)'),
]


def layer(package, file, arguments=None, condition=None):
    """Include launch/<file> from <package> with explicit arguments only."""
    return IncludeLaunchDescription(
        PathJoinSubstitution([FindPackageShare(package), 'launch', file]),
        launch_arguments=(arguments or {}).items(),
        condition=condition)


def enabled(name):
    return IfCondition(LaunchConfiguration(name))


def generate_launch_description():
    hardware = LaunchConfiguration('hardware')
    return LaunchDescription([
        *[DeclareLaunchArgument(n, default_value=d, description=t) for n, d, t in ARGUMENTS],
        # Applies to every node started after this line, in every layer
        SetParameter(name='use_sim_time', value=LaunchConfiguration('use_sim_time')),
        layer('my_robot_bringup', 'description.launch.py', {'hardware': hardware}),
        layer('my_robot_bringup', 'control.launch.py', {'hardware': hardware}),
        layer('my_robot_bringup', 'drivers.launch.py',
              condition=IfCondition(EqualsSubstitution(hardware, 'real'))),
        layer('my_robot_bringup', 'localization.launch.py', condition=enabled('use_localization')),
        layer('my_robot_bringup', 'diagnostics.launch.py', condition=enabled('use_diagnostics')),
        # Nav2 sets use_sim_time on its nodes itself, so pass it on; it reads the
        # last three as Python, so they are True/False, capitalized
        layer('my_robot_navigation', 'navigation.launch.py',
              {'map': LaunchConfiguration('map'), 'use_rviz': 'false',
               'use_sim_time': LaunchConfiguration('use_sim_time'),
               'use_localization': 'True', 'use_respawn': 'True', 'use_composition': 'False'},
              condition=enabled('use_navigation')),
        layer('my_robot_moveit_config', 'move_group.launch.py',
              condition=enabled('use_manipulation')),
    ])
```

- Each layer also runs on its own: `ros2 launch my_robot_bringup drivers.launch.py`. That is how
  the first power-on check brings the robot up one layer at a time.
- `ros2 launch my_robot_bringup robot.launch.py --show-args` lists the arguments.
- Includes are not scoped: an argument declared in one layer stays set for the layers after it.
  Pass everything a layer needs explicitly, or wrap the include in `GroupAction(scoped=True)`.
- The navigation layer is [nav-nav2](../../nav-nav2/references/launch.md)'s `navigation.launch.py`.
  On a headless robot keep `use_rviz` off and run RViz or Foxglove on a laptop.
- The manipulation layer starts only `move_group` (the file the MoveIt Setup Assistant generates):
  `robot_state_publisher` and the controllers already run in this package's layers. Never start
  them twice; see [manip-moveit2](../../manip-moveit2/references/launch.md).

## Description and control layers

```python
# my_robot_bringup/launch/description.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    xacro_file = PathJoinSubstitution(
        [FindPackageShare('my_robot_description'), 'urdf', 'my_robot.urdf.xacro'])
    # xacro runs at launch time; never read the .xacro file as plain text
    description = ParameterValue(
        Command(['xacro ', xacro_file, ' hardware:=', LaunchConfiguration('hardware')]),
        value_type=str)
    return LaunchDescription([
        DeclareLaunchArgument('hardware', default_value='real'),
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': description}], output='both'),
    ])
```

```python
# my_robot_bringup/launch/control.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import UnlessCondition
from launch.substitutions import EqualsSubstitution, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    controllers = PathJoinSubstitution(
        [FindPackageShare('my_robot_bringup'), 'config', 'controllers.yaml'])
    in_gazebo = EqualsSubstitution(LaunchConfiguration('hardware'), 'gz')
    return LaunchDescription([
        DeclareLaunchArgument('hardware', default_value='real'),
        # In Gazebo the gz_ros2_control plugin runs the controller manager
        Node(package='controller_manager', executable='ros2_control_node',
             parameters=[controllers], output='both', condition=UnlessCondition(in_gazebo)),
        # The spawner waits for the controller manager; the timeout makes a dead one visible
        Node(package='controller_manager', executable='spawner',
             arguments=['joint_state_broadcaster', 'diff_drive_controller',
                        '--param-file', controllers, '--controller-manager-timeout', '30']),
    ])
```

## Drivers layer: restart, fail fast, lifecycle

```python
# my_robot_bringup/launch/drivers.launch.py
from launch import LaunchDescription
from launch.actions import Shutdown
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import LifecycleNode, Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    params = PathJoinSubstitution(
        [FindPackageShare('my_robot_bringup'), 'config', 'drivers.yaml'])
    return LaunchDescription([
        # A sensor that may drop off the USB bus: restart it, a few times (values are examples)
        Node(package='my_robot_drivers', executable='lidar_driver', name='lidar',
             parameters=[params], respawn=True, respawn_delay=2.0, respawn_max_retries=5),
        # A driver written as a lifecycle node: configured and activated once it starts
        LifecycleNode(package='my_robot_drivers', executable='imu_driver', name='imu',
                      namespace='', parameters=[params], autostart=True),
        # The robot is useless without this one: stop the whole launch so systemd restarts it
        Node(package='my_robot_drivers', executable='battery_monitor', name='battery',
             parameters=[params], on_exit=Shutdown(reason='battery_monitor exited')),
    ])
```

```yaml
# my_robot_bringup/config/drivers.yaml
lidar:
  ros__parameters:
    port: /dev/my_robot/lidar      # udev symlink (udev.md), never /dev/ttyUSB0
    frame_id: lidar_link
imu:
  ros__parameters:
    port: /dev/my_robot/imu
    frame_id: imu_link
```

- A node that dies inside `ros2 launch` does not stop the launch, so systemd never sees it. Pick
  per node: `respawn=True` (launch restarts it), or `on_exit=Shutdown()` (the launch ends and
  systemd restarts everything).
- `Shutdown()` makes `ros2 launch` exit with code 0, which `Restart=on-failure` treats as a clean
  stop. The unit in [systemd.md](systemd.md) uses `Restart=always` for that reason.
- `respawn_max_retries` exists in Jazzy and Lyrical; Humble has only `respawn` and `respawn_delay`.

## Localization layer

```python
# my_robot_bringup/launch/localization.launch.py
from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    ekf = PathJoinSubstitution([FindPackageShare('my_robot_bringup'), 'config', 'ekf.yaml'])
    return LaunchDescription([
        Node(package='robot_localization', executable='ekf_node', name='ekf_filter_node',
             parameters=[ekf], output='both'),
    ])
```

The EKF configuration and the rule that only one node publishes each TF edge are in
[perception-slam](../../perception-slam/SKILL.md). If the EKF publishes `odom` → `base_link`, set
`enable_odom_tf: false` on the drive controller.

## Running it

```bash
ros2 launch my_robot_bringup robot.launch.py hardware:=mock                 # no hardware
ros2 launch my_robot_bringup robot.launch.py                                # the real robot
ros2 launch my_robot_bringup robot.launch.py use_navigation:=true map:=/home/robot/maps/lab.yaml
ros2 launch my_robot_bringup robot.launch.py --print                        # show what it would start
```

In Gazebo (`hardware:=gz use_sim_time:=true`) the world, the spawn and the `/clock` bridge come
from [sim-gazebo](../../sim-gazebo/SKILL.md); the drivers layer is skipped.
