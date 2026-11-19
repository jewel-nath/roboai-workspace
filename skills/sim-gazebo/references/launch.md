# Launch file, bridge YAML and gz_ros2_control (Jazzy + Harmonic)

Part of [sim-gazebo](../SKILL.md): one launch file that starts a world, spawns the robot from
`/robot_description`, bridges its topics and starts its controllers, with the GUI or headless.
Checked against `ros_gz` (`jazzy`: `gz_sim.launch.py`, `create`, the bridge README and demos) and
`gz_ros2_control` (`jazzy`: docs and `diff_drive_example.launch.py`). The URDF is expected to take a
`hardware` xacro argument whose `gz` value selects `gz_ros2_control/GazeboSimSystem`, as in
[ros2-control's urdf-yaml-launch.md](../../ros2-control/references/urdf-yaml-launch.md).

## `my_robot_gazebo/package.xml` (dependencies)

```xml
<exec_depend>ros_gz_sim</exec_depend>
<exec_depend>ros_gz_bridge</exec_depend>
<exec_depend>ros_gz_image</exec_depend>
<exec_depend>gz_ros2_control</exec_depend>
<exec_depend>robot_state_publisher</exec_depend>
<exec_depend>controller_manager</exec_depend>
<exec_depend>xacro</exec_depend>
<exec_depend>my_robot_description</exec_depend>
<exec_depend>my_robot_bringup</exec_depend>
```

## `my_robot_gazebo/launch/sim.launch.py`

```python
from launch import LaunchDescription
from launch.actions import (AppendEnvironmentVariable, DeclareLaunchArgument,
                            IncludeLaunchDescription, RegisterEventHandler)
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    gazebo_share = FindPackageShare('my_robot_gazebo')
    description_share = FindPackageShare('my_robot_description')
    world = LaunchConfiguration('world')
    gz_flags = LaunchConfiguration('gz_flags')

    robot_description = ParameterValue(
        Command(['xacro ',
                 PathJoinSubstitution([description_share, 'urdf', 'my_robot.urdf.xacro']),
                 ' hardware:=gz']),
        value_type=str)

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution(
            [FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])),
        launch_arguments={
            # The parts are joined with no separator, so keep the space.
            'gz_args': [gz_flags, ' ', world],
            'on_exit_shutdown': 'true',
        }.items())

    robot_state_publisher = Node(
        package='robot_state_publisher', executable='robot_state_publisher', output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}])

    spawn = Node(
        package='ros_gz_sim', executable='create', output='screen',
        arguments=['-topic', 'robot_description', '-name', 'my_robot', '-z', '0.05'])

    bridge = Node(
        package='ros_gz_bridge', executable='parameter_bridge', output='screen',
        parameters=[{'config_file': PathJoinSubstitution(
            [gazebo_share, 'config', 'bridge.yaml'])}])

    # Images through image_transport; camera_info stays in bridge.yaml.
    image_bridge = Node(
        package='ros_gz_image', executable='image_bridge', output='screen',
        arguments=['/camera/image_raw'])

    # The controller manager lives inside Gazebo; start the spawner once the robot exists.
    spawner = Node(
        package='controller_manager', executable='spawner', output='screen',
        arguments=['joint_state_broadcaster', 'diff_drive_controller', '--param-file',
                   PathJoinSubstitution([FindPackageShare('my_robot_bringup'),
                                         'config', 'controllers.yaml'])])

    return LaunchDescription([
        DeclareLaunchArgument(
            'world', default_value=PathJoinSubstitution([gazebo_share, 'worlds', 'my_world.sdf'])),
        DeclareLaunchArgument(
            'gz_flags', default_value='-r -v 3',
            description="gz sim flags; headless: '-r -s --headless-rendering -v 3'"),
        # <install>/share on the path resolves package:// meshes and model includes
        AppendEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH', PathJoinSubstitution([description_share, '..'])),
        AppendEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH', PathJoinSubstitution([gazebo_share, '..'])),
        gazebo,
        robot_state_publisher,
        spawn,
        bridge,
        image_bridge,
        RegisterEventHandler(OnProcessExit(target_action=spawn, on_exit=[spawner])),
    ])
```

- `world` takes a path, or a bare file name found on `GZ_SIM_RESOURCE_PATH` or among Gazebo's
  installed worlds (`empty.sdf`).
- RViz, Nav2 and every other node started with the simulation also need `use_sim_time: True`.
- `ros_gz_sim` also has `gz_server.launch.py` (`world_sdf_file`, `world_sdf_string`,
  `use_composition`) and Python launch actions `ros_gz_sim.actions.GzServer` and
  `ros_gz_bridge.actions.RosGzBridge` (`bridge_name`, `config_file`); with `use_composition` the
  server and bridge share one component container. The server node starts unpaused and has no
  `--headless-rendering` option.
- Kill leftovers after a crash (`pkill -f "gz sim"`); a lingering server keeps publishing `/clock`.

## `my_robot_gazebo/config/bridge.yaml`

Gazebo topic names are the `<topic>` of each sensor (see [sensors.md](sensors.md)). One list entry per
topic; install the file with `install(DIRECTORY config ...)`.

```yaml
# Gazebo must be the only /clock publisher: GZ_TO_ROS, never BIDIRECTIONAL.
- ros_topic_name: /clock
  gz_topic_name: /clock
  ros_type_name: rosgraph_msgs/msg/Clock
  gz_type_name: gz.msgs.Clock
  direction: GZ_TO_ROS

- ros_topic_name: /scan
  gz_topic_name: /scan
  ros_type_name: sensor_msgs/msg/LaserScan
  gz_type_name: gz.msgs.LaserScan
  direction: GZ_TO_ROS

- ros_topic_name: /scan/points          # gpu_lidar also publishes <topic>/points
  gz_topic_name: /scan/points
  ros_type_name: sensor_msgs/msg/PointCloud2
  gz_type_name: gz.msgs.PointCloudPacked
  direction: GZ_TO_ROS
  lazy: true                            # only bridged while someone subscribes

- ros_topic_name: /imu
  gz_topic_name: /imu
  ros_type_name: sensor_msgs/msg/Imu
  gz_type_name: gz.msgs.IMU
  direction: GZ_TO_ROS

- ros_topic_name: /camera/camera_info
  gz_topic_name: /camera/camera_info
  ros_type_name: sensor_msgs/msg/CameraInfo
  gz_type_name: gz.msgs.CameraInfo
  direction: GZ_TO_ROS

- ros_topic_name: /navsat
  gz_topic_name: /navsat
  ros_type_name: sensor_msgs/msg/NavSatFix
  gz_type_name: gz.msgs.NavSat
  direction: GZ_TO_ROS
```

Per-entry keys: `topic_name` (same name both sides) or `ros_topic_name` plus `gz_topic_name`;
`ros_type_name`, `gz_type_name`; `direction` (`BIDIRECTIONAL` default, `GZ_TO_ROS`, `ROS_TO_GZ`);
`lazy`; `publisher_queue`, `subscriber_queue` (10 by default); `qos_profile` (`SENSOR_DATA`, `CLOCK`,
`SYSTEM_DEFAULT`, `BEST_AVAILABLE`, ...); `frame_id`, which overwrites the ROS header's `frame_id`.
The YAML takes no substitutions; for world or robot names that vary, use the XML launch tag
`<ros_gz_bridge>` with `<topic .../>` children, or generate the file.

On the command line the same bridge is `parameter_bridge /scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan`,
where `[` is Gazebo to ROS, `]` ROS to Gazebo and `@` both ways. The supported type pairs are listed
in the `ros_gz_bridge` README; a pair that is not listed cannot be bridged without writing a
converter. Useful node parameters: `expand_gz_topic_names` (apply the ROS namespace to Gazebo topics
too), `override_timestamps_with_wall_time`, `lazy` (all topics given on the command line).

`image_bridge` takes Gazebo image topics as arguments and republishes them under the same names
through image_transport, so `compressed` topics appear when the plugin is installed. QoS:
`--ros-args -p qos:=sensor_data` (`default`, `system_default`, `sensor_data`).

## Without ros2_control: Gazebo's own systems

For a quick prototype, the DiffDrive and JointStatePublisher systems in the robot's SDF (or a
`<gazebo>` block) can stand in for ros2_control. Set the frames, which otherwise default to
`<model>/odom` and `<model>/<link>`:

```xml
<plugin filename="gz-sim-diff-drive-system" name="gz::sim::systems::DiffDrive">
  <left_joint>left_wheel_joint</left_joint>
  <right_joint>right_wheel_joint</right_joint>
  <wheel_separation>0.30</wheel_separation>   <!-- example: measure your robot -->
  <wheel_radius>0.05</wheel_radius>           <!-- example -->
  <topic>cmd_vel</topic>
  <odom_topic>odom</odom_topic>
  <tf_topic>tf</tf_topic>
  <frame_id>odom</frame_id>
  <child_frame_id>base_footprint</child_frame_id>
  <odom_publish_frequency>50</odom_publish_frequency>
</plugin>
<plugin filename="gz-sim-joint-state-publisher-system" name="gz::sim::systems::JointStatePublisher">
  <topic>joint_states</topic>
</plugin>
```

Bridge entries: `/cmd_vel` `geometry_msgs/msg/Twist` to `gz.msgs.Twist` `ROS_TO_GZ`; `/odom`
`nav_msgs/msg/Odometry` from `gz.msgs.Odometry`; `/tf` `tf2_msgs/msg/TFMessage` from `gz.msgs.Pose_V`;
`/joint_states` `sensor_msgs/msg/JointState` from `gz.msgs.Model`, all `GZ_TO_ROS` except the
command. Move to gz_ros2_control before the controllers have to match the real robot.

## gz_ros2_control: the Gazebo side

The `<ros2_control>` tag and the controller YAML are in the ros2-control skill. In the URDF, next to
the tag:

```xml
<gazebo>
  <plugin filename="gz_ros2_control-system" name="gz_ros2_control::GazeboSimROS2ControlPlugin">
    <parameters>$(find my_robot_bringup)/config/controllers.yaml</parameters>
  </plugin>
</gazebo>
```

Optional children of `<plugin>` (gz_ros2_control `jazzy` source):

| Element | Default | Effect |
|---|---|---|
| `<parameters>` | required | YAML for the controller manager; may repeat |
| `<controller_manager_name>` | `controller_manager` | Node name of the manager |
| `<ros><namespace>` / `<ros><remapping>` | none | Namespace and remaps for the manager and its controllers |
| `<hold_joints>` | `true` | Holds joints whose command interface no controller has claimed |
| `<position_proportional_gain>` | 0.1 | Position commands become `gain * error * update_rate` joint velocity |

- `update_rate` comes from the `controller_manager` section of the YAML; its period must be at least
  `max_step_size` (an error is logged otherwise, a warning when it is slower).
- The plugin forces `use_sim_time` on the manager and blocks until `/robot_description` is published.
- With `<ros><namespace>`, write the YAML keys as `/**/controller_manager:` and
  `/**/diff_drive_controller:` so one file matches any namespace, and pass the spawner
  `--controller-manager /<ns>/controller_manager`.
- A `mimic` joint gets state interfaces only, no command interface.
- `GazeboSimSystem` also exposes `imu` and `force_torque` sensors declared in the `<ros2_control>`
  tag, for broadcasters such as `imu_sensor_broadcaster`.
