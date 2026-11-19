# ros2_control tag, controller YAML and launch (Jazzy)

One description, one controller file and one launch file that run the same robot on mock
hardware, in Gazebo Harmonic and on the real board. The example is a differential-drive base with
`left_wheel_joint` and `right_wheel_joint`; an arm variant follows. Values marked "example" are
placeholders: measure your robot.

## The `<ros2_control>` tag

```xml
<!-- my_robot_description/urdf/my_robot.ros2_control.xacro -->
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">
  <!-- hardware: mock | gz | real -->
  <xacro:macro name="my_robot_ros2_control" params="hardware port ticks_per_rad">
    <ros2_control name="my_robot_system" type="system">
      <hardware>
        <xacro:if value="${hardware == 'mock'}">
          <plugin>mock_components/GenericSystem</plugin>
          <!-- integrate velocity commands into positions, so odometry moves -->
          <param name="calculate_dynamics">true</param>
        </xacro:if>
        <xacro:if value="${hardware == 'gz'}">
          <plugin>gz_ros2_control/GazeboSimSystem</plugin>
        </xacro:if>
        <xacro:if value="${hardware == 'real'}">
          <plugin>my_robot_hardware/MyRobotSystem</plugin>
          <param name="port">${port}</param>
          <param name="baud_rate">115200</param>  <!-- example: your board's rate -->
          <param name="ticks_per_rad">${ticks_per_rad}</param>
        </xacro:if>
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

    <xacro:if value="${hardware == 'gz'}">
      <gazebo>
        <plugin filename="gz_ros2_control-system"
                name="gz_ros2_control::GazeboSimROS2ControlPlugin">
          <parameters>$(find my_robot_bringup)/config/controllers.yaml</parameters>
        </plugin>
      </gazebo>
    </xacro:if>
  </xacro:macro>
</robot>
```

In the top-level `my_robot.urdf.xacro`:

```xml
<xacro:arg name="hardware" default="mock"/>
<xacro:include filename="$(find my_robot_description)/urdf/my_robot.ros2_control.xacro"/>
<!-- ticks_per_rad = encoder counts per wheel revolution / (2 * pi); the plugin rejects the
     placeholder, so a real run cannot start with a made-up value -->
<!-- port: a fixed udev symlink, not /dev/ttyUSB0, which can change between boots -->
<xacro:my_robot_ros2_control hardware="$(arg hardware)" port="/dev/my_robot_motors"
                             ticks_per_rad="SET_FROM_DATASHEET"/>
```

Rules the controller manager enforces or relies on:

- Every `<joint>` in the tag must be a joint of the URDF, or loading stops with "not found in
  URDF". Configuration ports and other non-joint I/O go in a `<gpio name="...">` block.
- Mimic joints use the URDF `<mimic>` element on the joint, not params in this tag.
- `<param name="min">` / `<param name="max">` under a `command_interface`, plus the URDF `<limit>`,
  are enforced only when the controller manager has `enforce_command_limits: true` (default
  `false` on Jazzy, `true` on Lyrical).
- `<param name="initial_value">` under a `state_interface` sets the mock's start pose.
- `is_async="true"` on `<ros2_control>` runs a slow component in its own thread.
- ROS 1 `<transmission>` blocks with `<hardwareInterface>` do nothing in ROS 2; delete them.

## Controller YAML

Each controller gets its own section with its `type`. The spawner loads the file into the
controller with `--param-file`; on Jazzy, controllers do not see parameters given only to
`ros2_control_node`.

```yaml
# my_robot_bringup/config/controllers.yaml
controller_manager:
  ros__parameters:
    update_rate: 100  # Hz; read() + update + write() must fit in one period

joint_state_broadcaster:
  ros__parameters:
    type: joint_state_broadcaster/JointStateBroadcaster

diff_drive_controller:
  ros__parameters:
    type: diff_drive_controller/DiffDriveController
    left_wheel_names: ["left_wheel_joint"]
    right_wheel_names: ["right_wheel_joint"]
    wheel_separation: 0.30   # example: centre-to-centre distance of the wheels, m
    wheel_radius: 0.05       # example, m
    odom_frame_id: odom
    base_frame_id: base_link
    enable_odom_tf: true     # false if robot_localization publishes odom -> base_link
    publish_rate: 50.0
    cmd_vel_timeout: 0.5     # s without commands before the base stops
    linear.x.max_velocity: 0.5       # example limits; unset limits are NaN (off)
    linear.x.max_acceleration: 1.0
    angular.z.max_velocity: 2.0
    pose_covariance_diagonal: [0.001, 0.001, 0.001, 0.001, 0.001, 0.01]
    twist_covariance_diagonal: [0.001, 0.001, 0.001, 0.001, 0.001, 0.01]
```

The `controller_manager` section is read by Gazebo's plugin (it loads the file as the controller
manager's parameters); `ros2_control_node` gets `update_rate` from the launch file below.

Arm variant with a trajectory controller (MoveIt 2 sends goals to its action):

```yaml
arm_controller:
  ros__parameters:
    type: joint_trajectory_controller/JointTrajectoryController
    joints: [joint1, joint2, joint3]
    command_interfaces: [position]
    state_interfaces: [position, velocity]
    constraints:
      stopped_velocity_tolerance: 0.01
      goal_time: 0.0                       # 0 = no limit on overrun
      joint1: {trajectory: 0.2, goal: 0.05}  # rad; repeat per joint
```

`gains` are used only when the command interfaces are `velocity` or `effort` without `position`;
with `position` commands they are ignored.

## Launch: mock or real

```python
# my_robot_bringup/launch/robot.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    hardware = LaunchConfiguration("hardware")
    xacro_file = PathJoinSubstitution(
        [FindPackageShare("my_robot_description"), "urdf", "my_robot.urdf.xacro"])
    robot_description = ParameterValue(
        Command(["xacro ", xacro_file, " hardware:=", hardware]), value_type=str)
    controllers = PathJoinSubstitution(
        [FindPackageShare("my_robot_bringup"), "config", "controllers.yaml"])

    return LaunchDescription([
        DeclareLaunchArgument("hardware", default_value="mock", description="mock or real"),
        # Publishes /robot_description, which the controller manager subscribes to
        Node(package="robot_state_publisher", executable="robot_state_publisher",
             parameters=[{"robot_description": robot_description}]),
        Node(package="controller_manager", executable="ros2_control_node",
             parameters=[{"update_rate": 100}], output="both"),
        # One spawner, controllers activated in the order listed
        Node(package="controller_manager", executable="spawner",
             arguments=["joint_state_broadcaster", "diff_drive_controller",
                        "--param-file", controllers]),
    ])
```

To take commands on `/cmd_vel` instead of `/diff_drive_controller/cmd_vel`, add
`"--controller-ros-args", "-r ~/cmd_vel:=/cmd_vel"` to the spawner arguments. The message must
still be `TwistStamped`.

## Launch differences for Gazebo Harmonic

Install `ros-jazzy-gz-ros2-control` and `ros-jazzy-ros-gz`. Then, compared with the file above:

- Start Gazebo: include `ros_gz_sim`'s `launch/gz_sim.launch.py` with `gz_args` set to
  `-r empty.sdf` (or your world).
- Generate the description with `hardware:=gz`, and give `robot_state_publisher`
  `use_sim_time: True`.
- Do not start `ros2_control_node`: the Gazebo plugin runs the controller manager.
- Spawn the robot with `ros_gz_sim`'s `create` node, arguments `-topic robot_description -name
  my_robot`.
- Bridge the clock: `ros_gz_bridge`'s `parameter_bridge` with
  `/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock`.
- Start the spawner after `create` exits (`RegisterEventHandler(OnProcessExit(...))`), with the
  same `--param-file`.

## Drive it

```bash
# Base: TwistStamped on the controller's topic (teleop needs -p stamped:=true)
ros2 topic pub --rate 10 /diff_drive_controller/cmd_vel geometry_msgs/msg/TwistStamped \
  "{twist: {linear: {x: 0.1}, angular: {z: 0.0}}}"
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true \
  -r cmd_vel:=/diff_drive_controller/cmd_vel

# Arm: one point, reached in 2 s
ros2 topic pub --once /arm_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory \
  "{joint_names: [joint1, joint2, joint3], points: [{positions: [0.3, -0.2, 0.1], time_from_start: {sec: 2}}]}"
```

## The `ros2 control` CLI

```bash
ros2 control list_hardware_components -v        # components, lifecycle state, interfaces
ros2 control list_hardware_interfaces           # [claimed] marks command interfaces in use
ros2 control list_controllers                   # name, type, state
ros2 control list_controller_types              # plugins the manager can load
ros2 control load_controller --set-state active arm_controller /path/to/controllers.yaml
ros2 control set_controller_state arm_controller inactive     # unconfigured | inactive | active
ros2 control switch_controllers --deactivate arm_controller --activate other_controller
ros2 control set_hardware_component_state my_robot_system inactive   # releases the motors
ros2 control unload_controller arm_controller
```

Sources: control.ros.org Jazzy (controller_manager user doc, mock components, joint limiting,
asynchronous components, diff_drive_controller and joint_trajectory_controller user docs, the
ros2_controllers Humble to Jazzy migration guide); ros2_control_demos `jazzy` example 2;
gz_ros2_control `jazzy` docs and demos; ros2controlcli on the ros2_control `jazzy` branch.
