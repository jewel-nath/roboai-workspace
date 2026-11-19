# Sensors, the ros2_control block and the display launch file

The rest of the example package from [description-package.md](description-package.md), for
[ros2-robot-description](../SKILL.md). Values are placeholders.

## `urdf/sensors.xacro`

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">
  <link name="lidar_link">
    <visual><geometry><cylinder radius="0.035" length="0.04"/></geometry></visual>
    <collision><geometry><cylinder radius="0.035" length="0.04"/></geometry></collision>
    <xacro:cylinder_inertial m="0.17" r="0.035" h="0.04"><origin xyz="0 0 0"/></xacro:cylinder_inertial>
  </link>
  <joint name="lidar_joint" type="fixed">
    <parent link="base_link"/>
    <child link="lidar_link"/>
    <origin xyz="0.05 0 ${base_z + 0.02}" rpy="0 0 0"/>  <!-- frame at the scan plane -->
  </joint>

  <!-- camera_link follows REP 103 (x forward); images are stamped in the optical frame. -->
  <link name="camera_link"/>
  <joint name="camera_joint" type="fixed">
    <parent link="base_link"/>
    <child link="camera_link"/>
    <origin xyz="${base_x/2} 0 ${base_z}" rpy="0 0 0"/>
  </joint>
  <link name="camera_optical_frame"/>
  <joint name="camera_optical_joint" type="fixed">
    <parent link="camera_link"/>
    <child link="camera_optical_frame"/>
    <origin xyz="0 0 0" rpy="${-pi/2} 0 ${-pi/2}"/>  <!-- z forward, x right, y down -->
  </joint>
</robot>
```

## `urdf/my_robot.ros2_control.xacro`

The interfaces each joint offers; controllers and the hardware plugin itself are the
[ros2-control](../../ros2-control/SKILL.md) skill's job.

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">
  <ros2_control name="my_robot_base" type="system">
    <hardware>
      <xacro:if value="$(arg sim)">
        <plugin>gz_ros2_control/GazeboSimSystem</plugin>
      </xacro:if>
      <xacro:unless value="$(arg sim)">
        <plugin>my_robot_hardware/MyRobotBaseSystem</plugin>
        <param name="port">/dev/ttyACM0</param>
      </xacro:unless>
    </hardware>
    <joint name="left_wheel_joint">
      <command_interface name="velocity"/>
      <state_interface name="position"/>
      <state_interface name="velocity"/>
    </joint>
    <joint name="right_wheel_joint">
      <command_interface name="velocity"/>
      <state_interface name="position"/>
      <state_interface name="velocity"/>
    </joint>
  </ros2_control>
</robot>
```

`mock_components/GenericSystem` in place of the real plugin runs the controllers with no hardware.

## `launch/display.launch.py`

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg = FindPackageShare('my_robot_description')
    xacro_file = PathJoinSubstitution([pkg, 'urdf', 'my_robot.urdf.xacro'])
    # value_type=str stops launch from parsing the URDF text as YAML.
    robot_description = ParameterValue(
        Command(['xacro ', xacro_file, ' sim:=', LaunchConfiguration('sim')]), value_type=str)

    return LaunchDescription([
        DeclareLaunchArgument('sim', default_value='false'),
        DeclareLaunchArgument('gui', default_value='true'),
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': robot_description,
                          'use_sim_time': LaunchConfiguration('sim')}]),
        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui',
             condition=IfCondition(LaunchConfiguration('gui'))),
        Node(package='rviz2', executable='rviz2',
             arguments=['-d', PathJoinSubstitution([pkg, 'rviz', 'display.rviz'])]),
    ])
```

Without an RViz config of your own, `ros2 launch urdf_launch display.launch.py
urdf_package:=my_robot_description urdf_package_path:=urdf/my_robot.urdf.xacro` does the same job.
