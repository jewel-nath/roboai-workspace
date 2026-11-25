# Processes, components and lifecycle management (Jazzy)

Part of [arch-robot-architecture](../SKILL.md). How to group nodes into processes and how to start them in
order. Writing a component or a lifecycle node, and the basic launch syntax for both, is in
[ros2-core](../../ros2-core/references/cpp-nodes.md) and its [launch.md](../../ros2-core/references/launch.md).

## Process or component: decide per node

A component is a C++ node built as a shared library (`rclcpp_components`) and loaded into a container
process; rclpy has no components, so a Python node is always its own process. The ROS 2 docs make process
layout a deploy-time choice: separate processes isolate faults and are easier to debug; one process costs
less and allows intra-process (zero-copy) transport.

| Put the node in | When | Examples |
|---|---|---|
| Its own process | It talks to hardware that can hang or crash, needs its own priority or privileges, is Python, or must restart alone | `ros2_control_node`, a vendor lidar driver, the behavior node |
| A shared container | C++ nodes passing images or point clouds to each other; many small C++ nodes started together | camera driver, rectifier and detector; the Nav2 servers |

Containers in Jazzy (`rclcpp_components`):

| Executable | Runs components on |
|---|---|
| `component_container` | one `SingleThreadedExecutor` for all |
| `component_container_mt` | one `MultiThreadedExecutor` for all |
| `component_container_isolated` | one executor per component (`--use_multi_threaded_executor` for multi-threaded ones); Nav2's default |

A crash or a blocked callback in one component affects the whole container (all of it with the single
executor). Put a component whose callbacks can block into `component_container_isolated`, or into its own
process.

## A perception container

```python
# my_robot_bringup/launch/perception.launch.py (fragment)
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableLifecycleNode, ComposableNode

intra = [{'use_intra_process_comms': True}]

ComposableNodeContainer(
    name='perception_container', namespace='',
    package='rclcpp_components', executable='component_container_mt',
    composable_node_descriptions=[
        ComposableNode(package='my_robot_driver', plugin='my_robot_driver::CameraDriver',
                       name='camera_driver', extra_arguments=intra),
        ComposableLifecycleNode(package='my_robot_perception',
                                plugin='my_robot_perception::Detector',
                                name='detector', autostart=True, extra_arguments=intra,
                                remappings=[('image', 'camera_driver/image_raw')]),
    ],
    output='screen',
)
```

- Intra-process transport works only between components in the same container that both set
  `use_intra_process_comms`; other subscribers still get the normal path.
- `ComposableLifecycleNode` and `autostart` arrived in launch_ros 0.26.7 (Jazzy, April 2025); update an
  older install or use a lifecycle manager.
- `ros2 component list` shows what each container loaded; `ros2 component types` lists the plugins the
  environment can load.

## Lifecycle: who drives the transitions

Lifecycle nodes start `unconfigured`; `configure` allocates and checks (open the device, read parameters),
`activate` starts data flowing, `deactivate` and `cleanup` undo them. Make lifecycle nodes of drivers and
of anything that must start after something else. Three ways to drive them:

| Way | Order | Watches the nodes afterwards | Use for |
|---|---|---|---|
| `autostart=True` on `LifecycleNode` / `ComposableLifecycleNode` | none: each node configures and activates on its own | no | independent nodes |
| `nav2_lifecycle_manager` | configures every node in `node_names` order, then activates in order; shuts down in reverse | yes, by bond heartbeat | a group that must come up in order, and go down together |
| A supervisor node of your own | whatever you code against each node's `change_state` service | as you code it | recovery policies the manager does not have |

### `nav2_lifecycle_manager` for your own nodes

It works with any lifecycle node, not only Nav2's (Apache-2.0, in `ros-jazzy-nav2-lifecycle-manager`).
Parameters, from its Jazzy source:

| Parameter | Default | Meaning |
|---|---|---|
| `node_names` | (required) | nodes to manage, in start-up order; relative names resolve in the manager's namespace |
| `autostart` | `false` | start the group when the manager starts |
| `bond_timeout` | `4.0` s | wait this long for each node's bond after activating it; `0.0` turns bonds off |
| `attempt_respawn_reconnection` | `true` | after a bond breaks, wait for the node to come back and restart the group |
| `bond_respawn_max_duration` | `10.0` s | how long to wait for that |

```python
# my_robot_bringup/launch/sensors.launch.py
from launch import LaunchDescription
from launch_ros.actions import LifecycleNode, Node


def generate_launch_description():
    return LaunchDescription([
        LifecycleNode(package='my_robot_driver', executable='lidar_driver',
                      name='lidar_driver', namespace='', respawn=True, respawn_delay=2.0),
        LifecycleNode(package='my_robot_driver', executable='imu_driver',
                      name='imu_driver', namespace='', respawn=True, respawn_delay=2.0),
        Node(package='nav2_lifecycle_manager', executable='lifecycle_manager',
             name='lifecycle_manager_sensors', output='screen',
             parameters=[{'node_names': ['imu_driver', 'lidar_driver'],
                          'autostart': True,
                          'bond_timeout': 4.0}]),
    ])
```

**Bonds.** After activating a node the manager waits `bond_timeout` for a bond (a heartbeat on the `bond`
topic) from it; with no bond it logs `Server <node> was unable to be reached after 4.00s by bond` and
stops bringing the group up. Nav2's servers create one because they derive from `nav2_util::LifecycleNode`
and call `createBond()` in `on_activate` and `destroyBond()` in `on_deactivate`. For your nodes, either:

- derive C++ lifecycle nodes from `nav2_util::LifecycleNode` (depend on `nav2_util`) and make the same two
  calls, so a crashed driver brings its group down and, with respawn, back up; or
- set `bond_timeout: 0.0` for a group of plain `rclcpp_lifecycle` or rclpy nodes, and accept that the
  manager no longer notices a node dying.

**The manager's services.** `<manager>/manage_nodes` (`nav2_msgs/srv/ManageLifecycleNodes`: `STARTUP`,
`PAUSE`, `RESUME`, `RESET`, `SHUTDOWN`, `CONFIGURE`, `CLEANUP`) and `<manager>/is_active`
(`std_srvs/srv/Trigger`). A supervisor or the operator UI calls these instead of each node.

```bash
ros2 service call /lifecycle_manager_sensors/manage_nodes nav2_msgs/srv/ManageLifecycleNodes "{command: 0}"
ros2 service call /lifecycle_manager_sensors/is_active std_srvs/srv/Trigger
```

### Several groups

Split nodes into groups that can fail independently: sensors, localization, navigation (Nav2 already runs
two managers), manipulation. The behavior layer checks each group's `is_active` before a mission that
needs it, and asks the operator, not the motors, what to do when one is down.

**Cascades.** `cascade_lifecycle` (Apache-2.0, 2.0.7 on Jazzy and Lyrical) lets a C++ or Python lifecycle node
make other nodes follow its transitions, for trees of dependencies that a flat list does not express.

## Checks

```bash
ros2 lifecycle nodes                          # every lifecycle node in the graph
ros2 lifecycle get /lidar_driver              # active [3]
ros2 component list                           # containers and their components
kill -9 <pid of lidar_driver>                 # with bonds: the manager logs the failure and resets the group;
                                              # with respawn: the driver returns and the group comes back
```

Sources: docs.ros.org Jazzy (About composition; Composing multiple nodes in a single process; Managed
nodes demo), `rclcpp` `jazzy` branch (`rclcpp_components`), `launch_ros` `jazzy` branch and changelog
(0.26.7), `navigation2` `jazzy` branch (`nav2_lifecycle_manager`, `nav2_util/lifecycle_node`,
`nav2_msgs/srv/ManageLifecycleNodes.srv`), `cascade_lifecycle` README.
