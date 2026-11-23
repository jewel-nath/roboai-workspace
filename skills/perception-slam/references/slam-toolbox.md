# slam_toolbox: 2D mapping, saving, localization

Part of [perception-slam](../SKILL.md). Checked against slam_toolbox 2.8.5 (`jazzy` branch, the Jazzy
binary): its README, `config/`, `launch/`, `srv/` and node sources. Licence LGPL-2.1.

## What it needs and gives

| | |
|---|---|
| Input | `sensor_msgs/LaserScan` on `scan_topic` (default `/scan`) |
| Input | TF `odom_frame` → `base_frame`, and `base_frame` → the scan's `frame_id`, at each scan's stamp |
| Output | TF `map_frame` → `odom_frame`, every `transform_publish_period` |
| Output | `/map` (`nav_msgs/OccupancyGrid`, transient local) every `map_update_interval`; `/pose` (`PoseWithCovarianceStamped`) |

Scans pass through a `tf2_ros::MessageFilter` that waits for the odom transform; a scan whose transform is
missing or late is dropped with `Message Filter dropping message: frame '...' ... for reason '...'`.

## Executables and launch files

| Launch file (in `slam_toolbox/launch`) | Executable | Use |
|---|---|---|
| `online_async_launch.py` | `async_slam_toolbox_node` | Live mapping; skips scans when busy. The default choice |
| `online_sync_launch.py` | `sync_slam_toolbox_node` | Processes every scan; may fall behind. Good for bags |
| `offline_launch.py` | `sync_slam_toolbox_node` | Offline processing of recorded data |
| `localization_launch.py` | `localization_slam_toolbox_node` | Localize in a serialized map |
| `lifelong_launch.py` | `lifelong_slam_toolbox_node` | Multi-session map refinement; the README calls it experimental |

In Jazzy these are lifecycle nodes. The launch files configure and activate them when `autostart:=true`
(default); `use_lifecycle_manager:=true` hands that to a Nav2 lifecycle manager instead. All of them
default to **`use_sim_time:=true`**: pass `use_sim_time:=false` on a real robot.

## Parameters to set

Copy `$(ros2 pkg prefix slam_toolbox)/share/slam_toolbox/config/mapper_params_online_async.yaml` to
`my_robot_localization/config/slam_toolbox_mapping.yaml` and change only what your robot needs:

| Key | Upstream file value | Set it to |
|---|---|---|
| `base_frame` | `base_footprint` | your URDF root (`base_link` or `base_footprint`) |
| `odom_frame`, `map_frame` | `odom`, `map` | REP 105 names, unless you namespace them |
| `scan_topic` | `/scan` | your lidar topic |
| `max_laser_range` | 20.0 | the usable range of your lidar (also limits rastering) |
| `resolution` | 0.05 | map cell size in metres |
| `minimum_travel_distance`, `minimum_travel_heading` | 0.5, 0.5 | how far the robot moves (m, rad) between processed scans |
| `ceres_loss_function` | `None` | `HuberLoss` if the wheels slip (the README's advice) |
| `do_loop_closing` | `true` | keep |
| `mode` | `mapping` | `localization` in the localization file (a solver optimization) |

The YAML top-level key must be `slam_toolbox`, the node name in the launch files.

```python
# my_robot_localization/launch/slam.launch.py
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    online_async = PathJoinSubstitution(
        [FindPackageShare('slam_toolbox'), 'launch', 'online_async_launch.py'])
    params = PathJoinSubstitution(
        [FindPackageShare('my_robot_localization'), 'config', 'slam_toolbox_mapping.yaml'])
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(online_async),
            launch_arguments={'use_sim_time': 'false', 'slam_params_file': params}.items()),
    ])
```

## Mapping

- Odometry quality decides the map. Check the wheel radius and separation first: drive a measured 5 m line
  and a 360° turn and compare `odom` with the tape and the start heading.
- Drive slowly, turn slowly, and close loops: come back through places already mapped, and finish where
  you started. Long featureless corridors give the scan matcher nothing to hold.
- Watch the map in RViz (Map display on `/map`, durability Transient Local). The `slam_toolbox` RViz panel
  (`slam_toolbox::SlamToolboxPlugin`) exposes the services below as buttons.

## Saving

Two different products; save both.

```bash
mkdir -p /home/<user>/maps
# Pose graph and scans: needed to continue mapping or to localize with slam_toolbox
ros2 service call /slam_toolbox/serialize_map slam_toolbox/srv/SerializePoseGraph \
  "{filename: '/home/<user>/maps/my_map'}"
# Occupancy image for Nav2 map_server and AMCL: my_map.pgm and my_map.yaml
ros2 service call /slam_toolbox/save_map slam_toolbox/srv/SaveMap \
  "{name: {data: '/home/<user>/maps/my_map'}}"
```

- `serialize_map` writes `my_map.posegraph` and `my_map.data`.
- `save_map` runs `ros2 run nav2_map_server map_saver_cli` for you, so `ros-jazzy-nav2-map-server` must be
  installed. It accepts only `A-Z a-z 0-9 _ . / -` in the path: `~` and spaces are rejected. Calling
  `map_saver_cli -f <path> --ros-args -p map_subscribe_transient_local:=true` yourself does the same.
- Relative file names land in the node's working directory; use absolute paths.

## Continuing a map

At start-up: set `map_file_name: /home/<user>/maps/my_map` (no extension) plus either `map_start_pose:
[x, y, yaw]` or `map_start_at_dock: true` (match the first scan against the map's first node). The pose
wins if both are set.

At run time:

```bash
ros2 service call /slam_toolbox/deserialize_map slam_toolbox/srv/DeserializePoseGraph \
  "{filename: '/home/<user>/maps/my_map', match_type: 2, initial_pose: {x: 0.0, y: 0.0, theta: 0.0}}"
```

`match_type`: 1 = start at the first node, 2 = start at `initial_pose`, 3 = localize at `initial_pose`.

## Localization in a saved map

1. Copy `config/mapper_params_localization.yaml` and make the same frame and topic changes as above.
   Set `mode: localization`, `map_file_name: /home/<user>/maps/my_map` and `map_start_pose` or
   `map_start_at_dock`.
2. `ros2 launch slam_toolbox localization_launch.py slam_params_file:=<file> use_sim_time:=false`.
3. Re-localize with RViz's 2D Pose Estimate: the node listens on `/initialpose`, like AMCL.
   `/slam_toolbox/clear_localization_buffer` (`std_srvs/srv/Empty`) clears its rolling scan buffer.

The localization node keeps the map fixed and matches a rolling window of recent scans against it; it does
not serialize. The upstream README notes that it needs good odometry and tuning, and recommends AMCL (Nav2)
on the `.pgm` map for a beginner's out-of-the-box setup; that path belongs to `nav-nav2`.

## Checks

- `ros2 topic hz /scan` steady; `ros2 run tf2_ros tf2_echo odom <scan frame>` answers.
- No `Message Filter dropping message` lines after start-up.
- `ros2 run tf2_ros tf2_echo map odom` is published, small, and changes in steps only at loop closures.
- After a closed loop the walls line up: no doubled or bent walls.
- Both `.posegraph`/`.data` and `.pgm`/`.yaml` exist; reloading with `map_file_name` puts the robot where it is.

**Humble** (slam_toolbox 2.6): plain nodes, not lifecycle; the launch files have no `autostart` or
`use_lifecycle_manager` arguments.
