# Launching MoveIt for an arm (Jazzy)

Part of [manip-moveit2](../SKILL.md). Checked against `moveit_configs_utils` 2.12.4 (`moveit_configs_builder.py`,
`launches.py`) and `controller_manager` 4.50 (`jazzy`). General launch mechanics are in
[ros2-core](../../ros2-core/references/launch.md); the controller side in [ros2-control](../../ros2-control/SKILL.md).

## MoveItConfigsBuilder

`MoveItConfigsBuilder(robot_name, package_name=...)` finds `<package_name>` (default `<robot_name>_moveit_config`)
and reads its files when the launch file is **parsed**. Each method loads one part; anything not called is loaded
from the default path by `to_moveit_configs()`.

| Method | Default file | Parameter it fills |
|---|---|---|
| `robot_description(file_path, mappings)` | `config/<robot_name>.urdf.xacro`, else `.setup_assistant` | `robot_description` |
| `robot_description_semantic(file_path)` | `config/<robot_name>.srdf` or `.setup_assistant` | `robot_description_semantic` |
| `robot_description_kinematics(file_path)` | `config/kinematics.yaml` | `robot_description_kinematics.<group>.*` |
| `joint_limits(file_path)` | `config/joint_limits.yaml` | `robot_description_planning.*` |
| `trajectory_execution(file_path, moveit_manage_controllers=True)` | `config/*_controllers.yaml` | controller manager keys |
| `planning_pipelines(pipelines=[...], default_planning_pipeline=...)` | `config/<name>_planning.yaml`, else the shipped default | `planning_pipelines`, `<name>.*` |
| `pilz_cartesian_limits(file_path)` | `config/pilz_cartesian_limits.yaml` (only if Pilz is loaded) | `robot_description_planning.cartesian_limits.*` |
| `planning_scene_monitor(...)` | — | `publish_planning_scene` and the other publish flags |
| `sensors_3d(file_path)` | `config/sensors_3d.yaml` | `sensors`, per-sensor keys |
| `moveit_cpp(file_path)` | `config/moveit_cpp.yaml` (never loaded unless called) | MoveItPy keys |

- `planning_pipelines()` with no list loads every `*_planning.yaml` in `config/` plus all shipped defaults
  (OMPL, Pilz, CHOMP, STOMP). Pass `pipelines=[...]` to load only what you use. OMPL is the default pipeline
  when present.
- `to_dict()` merges everything except `move_group_capabilities`; pass capabilities to `move_group` separately.
- With string `mappings` the xacro is expanded at parse time; a mapping that is a `LaunchConfiguration` is
  expanded at launch time instead, which lets a launch argument pick the hardware plugin.
- Edits to installed config files need `colcon build` again unless the workspace uses `--symlink-install`.

## Who needs which parameters

| Node | Parameters |
|---|---|
| `move_group` | `moveit_config.to_dict()`, `publish_robot_description_semantic: True`, optional `capabilities` |
| RViz with the MotionPlanning display | `planning_pipelines`, `robot_description_kinematics`, `joint_limits` (description and SRDF arrive on topics) |
| Your `MoveGroupInterface` node | nothing for plan/execute; `robot_description_kinematics` if it solves IK itself; `joint_limits` for its default scaling |
| MoveItPy node | `to_dict()` including a `moveit_cpp(...)` file ([moveit-py.md](moveit-py.md)) |
| `servo_node` | description, SRDF, kinematics, joint limits, `moveit_servo` params ([servo.md](servo.md)) |
| MTC node | `to_dict()`; `move_group` also needs `move_group/ExecuteTaskSolutionCapability` |

## A bringup launch for mock, Gazebo and the real arm

Keep the generated `demo.launch.py` for quick tests and write one launch file for real use. It assumes the
xacro takes a `hardware` argument (`mock`, `gz`, `real`) that selects the `<plugin>` in the ros2_control tag,
as in [ros2-control](../../ros2-control/SKILL.md).

```python
# my_robot_moveit_config/launch/bringup.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    hardware = LaunchConfiguration("hardware")
    use_sim_time = LaunchConfiguration("use_sim_time")
    in_gazebo = PythonExpression(["'", hardware, "' == 'gz'"])
    sim_time = {"use_sim_time": use_sim_time}

    moveit_config = (
        MoveItConfigsBuilder("my_robot", package_name="my_robot_moveit_config")
        .robot_description(file_path="config/my_robot.urdf.xacro", mappings={"hardware": hardware})
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_pipelines(pipelines=["ompl", "pilz_industrial_motion_planner"])
        .to_moveit_configs()
    )
    controllers_file = str(moveit_config.package_path / "config" / "ros2_controllers.yaml")

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[moveit_config.robot_description, sim_time],
        output="screen",
    )
    # In Gazebo the controller manager runs inside the simulator instead
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[controllers_file],
        remappings=[("~/robot_description", "/robot_description")],
        condition=UnlessCondition(in_gazebo),
        output="screen",
    )
    # --param-file on the spawner works on Jazzy and is required on Lyrical
    spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "arm_controller", "gripper_controller",
                   "--param-file", controllers_file],
        output="screen",
    )
    move_group = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        parameters=[moveit_config.to_dict(), sim_time, {"publish_robot_description_semantic": True}],
        output="screen",
    )
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", str(moveit_config.package_path / "config" / "moveit.rviz")],
        parameters=[
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits,
            sim_time,
        ],
        condition=IfCondition(LaunchConfiguration("use_rviz")),
        output="log",
    )

    return LaunchDescription([
        DeclareLaunchArgument("hardware", default_value="mock", choices=["mock", "gz", "real"]),
        DeclareLaunchArgument("use_sim_time", default_value="false"),
        DeclareLaunchArgument("use_rviz", default_value="true"),
        robot_state_publisher, controller_manager, spawner, move_group, rviz,
    ])
```

- **Virtual joint:** if the SRDF has one, add a `tf2_ros` `static_transform_publisher` with
  `--frame-id world --child-frame-id base_link` (what `static_virtual_joint_tfs.launch.py` does).
- **Gazebo** (`hardware:=gz use_sim_time:=true`): start the world, spawn the robot from `/robot_description`
  with `ros_gz_sim create`, bridge `/clock`, and load `gz_ros2_control` with the same controller file, as in
  [sim-gazebo](../../sim-gazebo/SKILL.md). Every MoveIt node then runs on sim time.
- **Real arm** (`hardware:=real`): the plugin is your hardware interface or the vendor driver. Many vendor
  packages ship their own controller launch; then start only `move_group` and RViz from this file.
- **Capabilities:** add `{"capabilities": "move_group/ExecuteTaskSolutionCapability"}` for Task Constructor, or
  `"pilz_industrial_motion_planner/MoveGroupSequenceAction pilz_industrial_motion_planner/MoveGroupSequenceService"`
  for Pilz sequences, to the `move_group` parameters (one space-separated string).

## Check the bringup

```bash
ros2 launch my_robot_moveit_config bringup.launch.py hardware:=mock
ros2 control list_controllers                     # joint_state_broadcaster, arm_controller, gripper_controller active
ros2 action list | grep follow_joint_trajectory   # /arm_controller/follow_joint_trajectory
ros2 param get /move_group robot_description_kinematics.arm.kinematics_solver
ros2 param get /move_group planning_pipelines     # the pipelines you asked for
```

`move_group` prints `You can start planning now!` when ready, and logs
`Added FollowJointTrajectory controller for arm_controller` once it has read `moveit_controllers.yaml`.
In RViz, plan to `home` and execute: the arm moves and `/joint_states` follows.
