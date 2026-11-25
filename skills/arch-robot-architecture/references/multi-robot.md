# Two or more robots: namespaces, TF and parameters (Jazzy)

Part of [arch-robot-architecture](../SKILL.md). How to run the same software stack for `robot_01`,
`robot_02` and so on in one ROS graph. Task allocation, traffic management and Open-RMF belong to
[ops-fleet](../../ops-fleet/SKILL.md); several robots in one Gazebo world to
[sim-gazebo](../../sim-gazebo/SKILL.md).

## Pick a scheme

| Scheme | How | Use when | Cost |
|---|---|---|---|
| Namespaces, one TF tree per robot | every node under `/robot_01`; `/tf` and `/tf_static` remapped to `tf` and `tf_static`; frames keep plain names (`base_link`) | each robot runs its own stack; Nav2's multi-robot launch works this way | a tool that needs every robot's pose subscribes to each robot's TF |
| Namespaces plus frame prefixes, one shared `/tf` | nodes namespaced; frames `robot_01/base_link` through `robot_state_publisher` `frame_prefix`, `diff_drive_controller` `tf_frame_prefix`, and every frame parameter (EKF, Nav2, sensors) | one node must see all robots in one tree, for example robots handing objects to each other | every frame name in every config and URDF-derived message needs the prefix |
| A ROS domain per robot | `ROS_DOMAIN_ID` per robot (0 to 101 on Linux), or separate Zenoh routers; `domain_bridge` (released for Jazzy) or a fleet layer passes chosen topics | many robots on one network; discovery traffic or isolation matters | a bridge to maintain; see the [middleware guide](../../../wiki/guides/choose-a-ros2-middleware.md) |

The rest of this file is the first scheme, the usual one.

## What changes per robot

- **Names.** Node code uses relative names only ([interfaces.md](interfaces.md)). Robot IDs follow one
  pattern: namespace `robot_01`, hostname `robot-01` (namespaces allow no hyphen).
- **Parameter files.** A section keyed with a bare node name (`controller_server:`) is read as
  `/controller_server` and does not reach `/robot_01/controller_server`. Key sections `/**/controller_server:`
  so one file serves every robot, or rewrite the file under the namespace at launch, as Nav2's bringup does
  (`RewrittenYaml(root_key=namespace)`). Inline dictionaries in launch files are not affected.
- **ros2_control.** Run `robot_state_publisher`, `ros2_control_node` and the spawners in the robot's
  namespace (the controller manager's own advice). Key `controllers.yaml` with `/**/` as above.
  Jazzy's `diff_drive_controller` prefixes `odom` and `base_link` with its namespace by default
  (`tf_frame_prefix_enable: true`, empty `tf_frame_prefix`); with a TF tree per robot set
  `tf_frame_prefix_enable: false`, or the controller publishes `robot_01/odom` → `robot_01/base_link`
  beside a URDF tree rooted at `base_link`.
- **Diagnostics.** `diagnostic_updater` and `diagnostic_aggregator` use absolute `/diagnostics` and
  `/diagnostics_agg`; remap them per robot, or keep one shared `/diagnostics` and set
  `diagnostic_updater.use_fqn: true` so each status carries its node's namespace.
- **Nav2.** Its `bringup_launch.py` pushes its own namespace and remaps TF when given `namespace` (and, on
  Jazzy, `use_namespace:=True`). Include it outside your own namespace group, or its nodes land in
  `/robot_01/robot_01`. The Jazzy `nav2_params.yaml` you copied has absolute topics (`odom_topic: /odom`,
  observation sources `topic: /scan`): make them relative. `nav2_multirobot_params_*.yaml` and
  `cloned_multi_tb3_simulation_launch.py` in `nav2_bringup` are worked examples.
- **Simulation time.** One `/clock` for all robots in one simulator; leave `/clock` un-namespaced.

## Launch one robot in its namespace

```python
# my_robot_bringup/launch/robot_ns.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, PushROSNamespace, SetRemap
from launch_ros.substitutions import FindPackageShare


def include(package, launch_file, arguments=None):
    return IncludeLaunchDescription(
        PathJoinSubstitution([FindPackageShare(package), 'launch', launch_file]),
        launch_arguments=(arguments or {}).items())


def generate_launch_description():
    namespace = LaunchConfiguration('namespace')
    share = FindPackageShare('my_robot_bringup')

    robot = GroupAction([
        PushROSNamespace(namespace),
        # Library topics with absolute names become per-robot
        SetRemap(src='/tf', dst='tf'),
        SetRemap(src='/tf_static', dst='tf_static'),
        SetRemap(src='/diagnostics', dst='diagnostics'),
        SetRemap(src='/diagnostics_agg', dst='diagnostics_agg'),
        include('my_robot_bringup', 'robot.launch.py', {'hardware': 'real'}),
        include('my_robot_bringup', 'sensors.launch.py'),
        include('my_robot_localization', 'ekf.launch.py'),
        Node(package='diagnostic_aggregator', executable='aggregator_node',
             parameters=[PathJoinSubstitution([share, 'config', 'analyzers.yaml'])]),
        include('my_robot_behavior', 'behavior.launch.py'),
    ])

    # Outside the group: Nav2 applies the namespace and the TF remaps itself
    navigation = include('nav2_bringup', 'bringup_launch.py', {
        'namespace': namespace,
        'use_namespace': 'True',              # Jazzy only; Lyrical removed the argument
        'map': LaunchConfiguration('map'),
        'params_file': PathJoinSubstitution(
            [FindPackageShare('my_robot_navigation'), 'config', 'nav2_params.yaml']),
    })

    return LaunchDescription([
        DeclareLaunchArgument('namespace', default_value='robot_01'),
        DeclareLaunchArgument('map'),
        robot,
        navigation,
    ])
```

- `PushROSNamespace` and `SetRemap` inside a `GroupAction` apply to every node in the group, including
  included files and composable nodes, and stop at the end of the group.
- A node given an absolute namespace (`namespace='/'` or `'/x'`) ignores the pushed one: keep
  `namespace=''` (or leave it out) in the layer launch files.
- RViz for one robot: `rviz2 --ros-args -r __ns:=/robot_01 -r /tf:=tf -r /tf_static:=tf_static`, or Nav2's
  `rviz_launch.py namespace:=robot_01`.
- Start the second robot with `namespace:=robot_02` on its own computer, or twice on one machine in
  simulation.

## Checks

```bash
ros2 node list                                   # every node under /robot_01 or /robot_02, each once
ros2 topic list | grep -v -e '^/robot_0' -e '^/rosout' -e '^/parameter_events' -e '^/clock'
                                                 # prints nothing: no topic is shared by accident
ros2 run tf2_tools view_frames --ros-args -r /tf:=/robot_01/tf -r /tf_static:=/robot_01/tf_static
                                                 # one complete tree for robot_01, plain frame names
ros2 param get /robot_01/diff_drive_controller tf_frame_prefix_enable    # False
```

Sources: docs.ros.org Jazzy (Using ROS 2 launch for large projects: namespaces and wildcards; Node
arguments: parameter file wildcards), `rclcpp` `jazzy` (`parameter_map.cpp`, the leading-slash rule),
`launch_ros` `jazzy` (`PushROSNamespace`, `SetRemap`, `LoadComposableNodes`), `ros2_control` `jazzy`
controller manager user doc (multiple controller managers), `ros2_controllers` `jazzy`
(`diff_drive_controller_parameter.yaml`, `diff_drive_controller.cpp`), `robot_state_publisher` `jazzy`
(`frame_prefix`), `navigation2` `jazzy` and `lyrical` (`bringup_launch.py`), `diagnostics` `ros2-jazzy`.
