# Launch files and parameter files (Jazzy)

Patterns for [ros2-core](../SKILL.md), checked against `launch_ros` (`jazzy`) and the Jazzy launch
tutorials. Put launch files in `<pkg>/launch/` named `*.launch.py`, `*.launch.xml` or
`*.launch.yaml`, and install that directory (see [packages.md](packages.md)).

## Python launch file

```python
# my_robot_bringup/launch/nodes.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, SetParameter
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    namespace = LaunchConfiguration('namespace')
    params = PathJoinSubstitution([FindPackageShare('my_robot_bringup'), 'config', 'nodes.yaml'])

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false', choices=['true', 'false']),
        DeclareLaunchArgument('namespace', default_value=''),

        # Applies to every node started after this line in the same scope.
        SetParameter(name='use_sim_time', value=use_sim_time),

        IncludeLaunchDescription(
            PathJoinSubstitution(
                [FindPackageShare('my_robot_description'), 'launch', 'description.launch.py']),
            launch_arguments={'use_sim_time': use_sim_time}.items()),

        Node(
            package='my_robot_nodes',
            executable='range_filter',
            name='range_filter',
            namespace=namespace,
            parameters=[params, {'alpha': 0.2}],   # later entries override earlier ones
            remappings=[('range/raw', 'sonar/front')],
            output='screen',
        ),
    ])
```

- `ros2 launch my_robot_bringup nodes.launch.py --show-args` lists the arguments;
  `--print` shows the launch description without running it.
- Values coming from substitutions are parsed as YAML, so `'true'` becomes a bool. A long string
  that is not valid YAML (a URDF from `xacro`) must be wrapped:
  `ParameterValue(Command(['xacro ', path]), value_type=str)` from
  `launch_ros.parameter_descriptions`.
- `IncludeLaunchDescription` takes the file path directly; the format is inferred from the
  extension.
- Use `GroupAction([PushROSNamespace('robot1'), ...])` to put a block of nodes in a namespace.

## The same in XML and YAML

```xml
<!-- my_robot_bringup/launch/nodes.launch.xml -->
<launch>
  <arg name="use_sim_time" default="false"/>
  <set_parameter name="use_sim_time" value="$(var use_sim_time)"/>
  <include file="$(find-pkg-share my_robot_description)/launch/description.launch.py">
    <arg name="use_sim_time" value="$(var use_sim_time)"/>
  </include>
  <node pkg="my_robot_nodes" exec="range_filter" name="range_filter" output="screen">
    <param from="$(find-pkg-share my_robot_bringup)/config/nodes.yaml"/>
    <param name="alpha" value="0.2"/>
    <remap from="range/raw" to="sonar/front"/>
  </node>
</launch>
```

```yaml
# my_robot_bringup/launch/nodes.launch.yaml
launch:
- arg:
    name: use_sim_time
    default: "false"
- set_parameter:
    name: use_sim_time
    value: $(var use_sim_time)
- node:
    pkg: my_robot_nodes
    exec: range_filter
    name: range_filter
    output: screen
    param:
    - from: $(find-pkg-share my_robot_bringup)/config/nodes.yaml
    - name: alpha
      value: 0.2
    remap:
    - from: range/raw
      to: sonar/front
```

XML and YAML suit static wiring. Use Python when the file needs logic (`OpaqueFunction`, computed
paths, event handlers).

## Parameter YAML file

```yaml
# my_robot_bringup/config/nodes.yaml
/**:                      # every node
  ros__parameters:
    frame_id: base_link

range_filter:             # a node named range_filter, in any namespace
  ros__parameters:
    alpha: 0.3
    topics: [front, rear]
```

- The top key is the node name, or its full name (`/robot1/range_filter`), or a wildcard (`/**`).
  A key that matches no node is ignored without any warning.
- Keep the type of each value the same as its declared default: parameters are statically typed,
  so an integer `1` given for a parameter declared as `1.0` makes `declare_parameter` throw.
- Dump a running node's values to start a file: `ros2 param dump /range_filter > nodes.yaml`.

## Lifecycle nodes in a launch file

```python
from launch_ros.actions import LifecycleNode

LifecycleNode(
    package='my_robot_driver', executable='driver', name='driver', namespace='',
    parameters=[params], autostart=True, output='screen')
```

`name` and `namespace` are required. `autostart=True` configures and activates the node once it
starts; it arrived in a 2025 Jazzy update of launch_ros, so on an older install (or on Humble)
drive the transitions with `ros2 lifecycle set` or a lifecycle manager such as Nav2's.

## Composable nodes

```python
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

ComposableNodeContainer(
    name='sensor_container', namespace='',
    package='rclcpp_components', executable='component_container_mt',
    composable_node_descriptions=[
        ComposableNode(
            package='my_robot_driver', plugin='my_robot_driver::RangeFilter',
            name='range_filter', parameters=[params],
            extra_arguments=[{'use_intra_process_comms': True}]),
    ],
    output='screen')
```

`component_container` runs components on a single-threaded executor and `component_container_mt`
on a multi-threaded one. `ros2 component list` shows what each container loaded.
