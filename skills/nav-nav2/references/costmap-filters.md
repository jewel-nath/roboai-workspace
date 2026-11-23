# Keepout zones, preferred lanes and speed zones (Jazzy)

Part of [nav-nav2](../SKILL.md). Checked against `nav2_costmap_2d` and `nav2_map_server` 1.3.14 and the docs.nav2.org
keepout and speed filter tutorials. Jazzy's `nav2_bringup` does not start any of this; the launch file below does.

## How it fits together

A costmap filter reads a **mask**: an ordinary map image (PGM, PNG or BMP plus YAML) laid over the real map.

| Piece | Node | Publishes |
|---|---|---|
| Mask | `nav2_map_server/map_server`, its own name, `topic_name` | the mask as `OccupancyGrid` (values 0-100, -1 unknown) |
| Filter info | `nav2_map_server/costmap_filter_info_server` | `nav2_msgs/CostmapFilterInfo`: `type`, `mask_topic`, `base`, `multiplier` |
| Filter | `nav2_costmap_2d::KeepoutFilter` or `SpeedFilter` in a costmap's `filters` list | keepout: costs in the costmap; speed: `nav2_msgs/SpeedLimit` |

`type`: 0 keepout, 1 speed limit in percent of maximum, 2 speed limit in m/s, 3 binary (switches a `Bool` topic
inside zones). Filters go in `filters`, not `plugins`, so they apply after inflation and are not inflated.

## Drawing masks

1. Copy the real map's `.pgm` and `.yaml` to `maps/keepout_mask.pgm/.yaml` (same size, resolution and origin, so
   the mask lines up). A mask may cover a smaller area with its own `origin`; its yaw must be 0.
2. Paint in an image editor. In the default `trinary` mode, dark is occupied (100), light is free (0).
3. Edit the copied YAML: `image:` the mask file; for a speed mask `mode: scale`, `free_thresh: 0.0`,
   `occupied_thresh: 1.0` so every grey level maps to a value.

| Mask | Paint | Result |
|---|---|---|
| Keepout | black areas | lethal: planners route around, controllers will not enter |
| Weighted area | mid grey (scale mode) | allowed but costly; higher values push the robot out sooner |
| Preferred lanes | lanes white, everything else black | the robot may only drive in the lanes |
| Speed (`type: 1`, `base: 100.0`, `multiplier: -1.0`) | grey level g percent dark | limit = 100 - g percent; white (0) means no limit |

Speed limit = mask value x `multiplier` + `base`; mask value 0 always means "no limit".

## Parameters

```yaml
keepout_filter_mask_server:
  ros__parameters:
    topic_name: "keepout_filter_mask"
    frame_id: "map"
keepout_costmap_filter_info_server:
  ros__parameters:
    type: 0
    filter_info_topic: "keepout_costmap_filter_info"
    mask_topic: "keepout_filter_mask"     # equals the mask server's topic_name
    base: 0.0
    multiplier: 1.0
speed_filter_mask_server:
  ros__parameters:
    topic_name: "speed_filter_mask"
    frame_id: "map"
speed_costmap_filter_info_server:
  ros__parameters:
    type: 1
    filter_info_topic: "speed_costmap_filter_info"
    mask_topic: "speed_filter_mask"
    base: 100.0
    multiplier: -1.0

global_costmap:
  global_costmap:
    ros__parameters:
      # ...existing keys...
      filters: ["keepout_filter", "speed_filter"]
      keepout_filter:
        plugin: "nav2_costmap_2d::KeepoutFilter"
        filter_info_topic: "keepout_costmap_filter_info"
      speed_filter:
        plugin: "nav2_costmap_2d::SpeedFilter"
        filter_info_topic: "speed_costmap_filter_info"
        speed_limit_topic: "speed_limit"

local_costmap:
  local_costmap:
    ros__parameters:
      # ...existing keys...
      filters: ["keepout_filter"]          # keepout in both; speed in one costmap only
      keepout_filter:
        plugin: "nav2_costmap_2d::KeepoutFilter"
        filter_info_topic: "keepout_costmap_filter_info"

controller_server:
  ros__parameters:
    speed_limit_topic: "speed_limit"       # node default; must match the speed filter
```

- Keepout in the global costmap only: paths avoid the zone but the robot may cut through it. Local only: the
  robot refuses to enter, yet plans still lead in. Use both unless you mean that difference.
- The speed filter belongs in one costmap. In both, the two publish conflicting limits at zone borders and the
  robot jerks (Nav2 tutorial).
- `KeepoutFilter` also takes `override_lethal_cost` (false) and `lethal_override_cost` (252): when the robot finds
  itself inside a keepout zone, the zone's cells drop below lethal so it can still plan its way out.

## Launch file

```python
# my_robot_navigation/launch/zones.launch.py: mask servers and their lifecycle manager
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_dir = get_package_share_directory('my_robot_navigation')
    params = LaunchConfiguration('params_file')
    use_sim_time = LaunchConfiguration('use_sim_time')
    common = {'use_sim_time': use_sim_time}

    def mask_server(name, mask_arg):
        return Node(
            package='nav2_map_server', executable='map_server', name=name, output='screen',
            parameters=[params, common, {'yaml_filename': LaunchConfiguration(mask_arg)}])

    def info_server(name):
        return Node(
            package='nav2_map_server', executable='costmap_filter_info_server', name=name,
            output='screen', parameters=[params, common])

    managed = ['keepout_filter_mask_server', 'keepout_costmap_filter_info_server',
               'speed_filter_mask_server', 'speed_costmap_filter_info_server']

    return LaunchDescription([
        DeclareLaunchArgument(
            'params_file', default_value=os.path.join(pkg_dir, 'config', 'nav2_params.yaml')),
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument(
            'keepout_mask', default_value=os.path.join(pkg_dir, 'maps', 'keepout_mask.yaml')),
        DeclareLaunchArgument(
            'speed_mask', default_value=os.path.join(pkg_dir, 'maps', 'speed_mask.yaml')),
        mask_server('keepout_filter_mask_server', 'keepout_mask'),
        info_server('keepout_costmap_filter_info_server'),
        mask_server('speed_filter_mask_server', 'speed_mask'),
        info_server('speed_costmap_filter_info_server'),
        Node(
            package='nav2_lifecycle_manager', executable='lifecycle_manager',
            name='lifecycle_manager_zones', output='screen',
            parameters=[common, {'autostart': True, 'node_names': managed}]),
    ])
```

Include it from `navigation.launch.py` or run it beside Nav2. The filter info and mask topics are transient local,
so the start order does not matter. Composed bringup can load the same nodes into `nav2_container` as
`nav2_map_server::MapServer` and `nav2_map_server::CostmapFilterInfoServer` components.

## Checks

- `ros2 lifecycle get /keepout_filter_mask_server` is `active`; `ros2 topic echo --once /keepout_costmap_filter_info`
  shows the right `type` and `filter_mask_topic`.
- RViz: add `/keepout_filter_mask` as a Map display over `/map`; the zones sit where they were painted.
- `/global_costmap/costmap` shows the keepout areas as lethal; a goal behind a zone gets a path around it.
- Driving into a speed zone: `ros2 topic echo /speed_limit` reports the expected `percentage` and `speed_limit`,
  and the commanded speed drops.
