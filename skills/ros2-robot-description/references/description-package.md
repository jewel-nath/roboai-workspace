# A description package, file by file

A small differential-drive robot laid out the way [ros2-robot-description](../SKILL.md) expects.
Dimensions and masses are placeholders: replace them with measured or CAD values
([inertials.md](inertials.md)). Gazebo tags live in their own file ([simulators.md](simulators.md)).

```text
my_robot_description/
  CMakeLists.txt
  package.xml
  urdf/my_robot.urdf.xacro           top level: args and includes only
  urdf/inertials.xacro               inertia macros
  urdf/base.xacro                    footprint, chassis, wheels, caster
  urdf/sensors.xacro                 lidar, camera and its optical frame
  urdf/my_robot.ros2_control.xacro   the <ros2_control> block
  urdf/my_robot.gazebo.xacro         <gazebo> tags, loaded only when sim:=true
  meshes/visual/  meshes/collision/
  launch/display.launch.py
  rviz/display.rviz
```

## Build files

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_description)
find_package(ament_cmake REQUIRED)
install(DIRECTORY urdf meshes launch rviz DESTINATION share/${PROJECT_NAME})
ament_package()
```

```xml
  <buildtool_depend>ament_cmake</buildtool_depend>
  <exec_depend>joint_state_publisher_gui</exec_depend>
  <exec_depend>launch_ros</exec_depend>
  <exec_depend>robot_state_publisher</exec_depend>
  <exec_depend>rviz2</exec_depend>
  <exec_depend>xacro</exec_depend>
  <export>
    <build_type>ament_cmake</build_type>
    <!-- lets ros_gz_sim resolve package://my_robot_description/... meshes -->
    <gazebo_ros gazebo_model_path="${prefix}/../"/>
  </export>
```

## `urdf/my_robot.urdf.xacro`

```xml
<?xml version="1.0"?>
<robot name="my_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">
  <xacro:arg name="sim" default="false"/>

  <!-- Relative includes resolve against this file's folder, so the file expands without a build. -->
  <xacro:include filename="inertials.xacro"/>
  <xacro:include filename="base.xacro"/>
  <xacro:include filename="sensors.xacro"/>
  <xacro:include filename="my_robot.ros2_control.xacro"/>
  <xacro:if value="$(arg sim)">
    <xacro:include filename="my_robot.gazebo.xacro"/>
  </xacro:if>
</robot>
```

## `urdf/inertials.xacro`

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">
  <!-- Solid box, sides x y z along the inertial frame's axes. -->
  <xacro:macro name="box_inertial" params="m x y z *origin">
    <inertial>
      <xacro:insert_block name="origin"/>
      <mass value="${m}"/>
      <inertia ixx="${m*(y*y+z*z)/12}" ixy="0" ixz="0"
               iyy="${m*(x*x+z*z)/12}" iyz="0" izz="${m*(x*x+y*y)/12}"/>
    </inertial>
  </xacro:macro>

  <!-- Solid cylinder, axis along the inertial frame's z. -->
  <xacro:macro name="cylinder_inertial" params="m r h *origin">
    <inertial>
      <xacro:insert_block name="origin"/>
      <mass value="${m}"/>
      <inertia ixx="${m*(3*r*r+h*h)/12}" ixy="0" ixz="0"
               iyy="${m*(3*r*r+h*h)/12}" iyz="0" izz="${m*r*r/2}"/>
    </inertial>
  </xacro:macro>

  <!-- Solid sphere. -->
  <xacro:macro name="sphere_inertial" params="m r *origin">
    <inertial>
      <xacro:insert_block name="origin"/>
      <mass value="${m}"/>
      <inertia ixx="${2*m*r*r/5}" ixy="0" ixz="0"
               iyy="${2*m*r*r/5}" iyz="0" izz="${2*m*r*r/5}"/>
    </inertial>
  </xacro:macro>
</robot>
```

## `urdf/base.xacro`

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">
  <xacro:property name="base_x" value="0.30"/>
  <xacro:property name="base_y" value="0.20"/>
  <xacro:property name="base_z" value="0.08"/>
  <xacro:property name="wheel_r" value="0.035"/>
  <xacro:property name="wheel_w" value="0.025"/>
  <xacro:property name="wheel_sep" value="0.23"/>  <!-- centre to centre -->
  <xacro:property name="caster_r" value="0.015"/>

  <!-- Root on the ground under the base; no <inertial> (KDL ignores a root link's inertia). -->
  <link name="base_footprint"/>

  <joint name="base_joint" type="fixed">
    <parent link="base_footprint"/>
    <child link="base_link"/>
    <origin xyz="0 0 ${wheel_r}" rpy="0 0 0"/>
  </joint>

  <link name="base_link">
    <visual>
      <origin xyz="0 0 ${base_z/2}" rpy="0 0 0"/>
      <geometry><mesh filename="package://my_robot_description/meshes/visual/base.dae"/></geometry>
    </visual>
    <collision>
      <origin xyz="0 0 ${base_z/2}" rpy="0 0 0"/>
      <geometry><box size="${base_x} ${base_y} ${base_z}"/></geometry>
    </collision>
    <xacro:box_inertial m="2.0" x="${base_x}" y="${base_y}" z="${base_z}">
      <origin xyz="0 0 ${base_z/2}" rpy="0 0 0"/>
    </xacro:box_inertial>
  </link>

  <xacro:macro name="wheel" params="side y">
    <link name="${side}_wheel_link">
      <visual>
        <origin xyz="0 0 0" rpy="${pi/2} 0 0"/>  <!-- cylinder z axis onto the link's y axis -->
        <geometry><cylinder radius="${wheel_r}" length="${wheel_w}"/></geometry>
      </visual>
      <collision>
        <origin xyz="0 0 0" rpy="${pi/2} 0 0"/>
        <geometry><cylinder radius="${wheel_r}" length="${wheel_w}"/></geometry>
      </collision>
      <xacro:cylinder_inertial m="0.1" r="${wheel_r}" h="${wheel_w}">
        <origin xyz="0 0 0" rpy="${pi/2} 0 0"/>
      </xacro:cylinder_inertial>
    </link>
    <!-- Same axis on both sides: positive velocity drives the robot forward. -->
    <joint name="${side}_wheel_joint" type="continuous">
      <parent link="base_link"/>
      <child link="${side}_wheel_link"/>
      <origin xyz="0 ${y} 0" rpy="0 0 0"/>
      <axis xyz="0 1 0"/>
    </joint>
  </xacro:macro>

  <xacro:wheel side="left" y="${wheel_sep/2}"/>
  <xacro:wheel side="right" y="${-wheel_sep/2}"/>

  <link name="caster_link">
    <collision><geometry><sphere radius="${caster_r}"/></geometry></collision>
    <visual><geometry><sphere radius="${caster_r}"/></geometry></visual>
    <xacro:sphere_inertial m="0.02" r="${caster_r}"><origin xyz="0 0 0"/></xacro:sphere_inertial>
  </link>
  <joint name="caster_joint" type="fixed">
    <parent link="base_link"/>
    <child link="caster_link"/>
    <origin xyz="${-base_x/2 + caster_r} 0 ${caster_r - wheel_r}" rpy="0 0 0"/>
  </joint>
</robot>
```

`pi` is built into xacro, with the other `math` names (`radians()`, `sqrt()`). Do not define your
own `pi` property: xacro warns about redefining a global symbol and the value is less exact.

Sensors, the `<ros2_control>` block and `launch/display.launch.py` continue in
[sensors-control-display.md](sensors-control-display.md).
