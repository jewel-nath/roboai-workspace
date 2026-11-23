# RTAB-Map: RGB-D, stereo and lidar SLAM

Part of [perception-slam](../SKILL.md). Checked against rtabmap_ros 0.23.13 (`jazzy-devel`, the Jazzy
binary) and RTAB-Map 0.23.14: the package READMEs, `rtabmap_slam/doc/rtabmap.md`, `rtabmap.launch.py`,
the examples and demos, and the core `Parameters.h`. Licence BSD. Camera drivers and image topics belong to
[perception-camera](../../perception-camera/SKILL.md), lidar drivers to
[perception-lidar](../../perception-lidar/SKILL.md).

## Packages and nodes

`sudo apt install ros-jazzy-rtabmap-ros` brings them all.

| Package | Node | Does |
|---|---|---|
| `rtabmap_sync` | `rgbd_sync`, `stereo_sync` | Packs a camera's image, depth (or right image) and info into one `rgbd_image` |
| `rtabmap_odom` | `rgbd_odometry`, `stereo_odometry`, `icp_odometry` | Visual or ICP odometry, when the robot has no better odometry |
| `rtabmap_slam` | `rtabmap` | Graph SLAM with appearance-based loop closure; publishes `map` → `odom` |
| `rtabmap_viz` | `rtabmap_viz` | RTAB-Map's own GUI: graph, loop closures, feature matches |
| `rtabmap_util` | `point_cloud_xyz`, `obstacles_detection`, `lidar_deskewing`, `imu_to_tf` | Helpers |
| `rtabmap_launch` | `rtabmap.launch.py` | One launch file for common setups |
| `rtabmap_examples`, `rtabmap_demos` | launch files | Camera, lidar and robot examples to copy from |

## Quick tries

```bash
# Handheld RGB-D camera, visual odometry, new database
ros2 launch rtabmap_launch rtabmap.launch.py args:="-d" frame_id:=camera_link \
  rgb_topic:=/camera/color/image_raw depth_topic:=/camera/aligned_depth_to_color/image_raw \
  camera_info_topic:=/camera/color/camera_info approx_sync:=false

# 3D lidar alone, ICP odometry
ros2 launch rtabmap_examples lidar3d.launch.py lidar_topic:=/points frame_id:=base_link
```

`args` passes flags and RTAB-Map parameters to the nodes (`-d` deletes the database on start; parameters go
as `--Reg/Strategy 1`); `rtabmap_args` is the older name for it. Other useful arguments: `localization`,
`database_path`, `visual_odometry`, `icp_odometry`, `odom_topic`, `subscribe_scan`, `scan_topic`,
`imu_topic`, `wait_imu_to_init`, `rgbd_sync`, `use_sim_time`, `qos`, `rviz`, `rtabmap_viz`. List them with
`ros2 launch rtabmap_launch rtabmap.launch.py --show-args`. The launch file puts the nodes in the
`rtabmap` namespace.

## Ground robot: RGB-D camera, 2D lidar, wheel or EKF odometry

Use the robot's odometry (the local EKF from [robot-localization.md](robot-localization.md)) rather than
visual odometry, so RTAB-Map only adds `map` → `odom`. Modelled on the `turtlebot3_rgbd_scan` demo:

```python
# my_robot_localization/launch/rtabmap.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    localization = LaunchConfiguration('localization')
    params = {
        'frame_id': 'base_link',
        'subscribe_rgbd': True,
        'subscribe_scan': True,
        'approx_sync': True,                  # scan, camera and odometry are not stamped together
        'use_sim_time': False,
        # RTAB-Map's own parameters are strings
        'Reg/Strategy': '1',                  # refine links with ICP on the scan
        'Reg/Force3DoF': 'true',              # planar robot: x, y, yaw only
        'RGBD/NeighborLinkRefining': 'true',  # correct odometry with the scan
        'Grid/Sensor': '2',                   # occupancy from scan and depth
        'Grid/3D': 'false',
        'Grid/RangeMax': '4.0',               # example: the depth range you trust
        'Optimizer/GravitySigma': '0',        # no IMU gravity constraints in 2D
    }
    remaps = [('rgb/image', '/camera/color/image_raw'),
              ('rgb/camera_info', '/camera/color/camera_info'),
              ('depth/image', '/camera/aligned_depth_to_color/image_raw'),
              ('scan', '/scan'),
              ('odom', '/odometry/filtered')]
    return LaunchDescription([
        DeclareLaunchArgument('localization', default_value='false'),
        # approx_sync false needs colour and depth with identical stamps; set true otherwise
        Node(package='rtabmap_sync', executable='rgbd_sync', output='screen',
             parameters=[{'approx_sync': False}], remappings=remaps),
        Node(package='rtabmap_slam', executable='rtabmap', output='screen',
             condition=UnlessCondition(localization),
             parameters=[params], remappings=remaps, arguments=['-d']),
        Node(package='rtabmap_slam', executable='rtabmap', output='screen',
             condition=IfCondition(localization),
             parameters=[params, {'Mem/IncrementalMemory': 'false',
                                  'Mem/InitWMWithAllNodes': 'true'}],
             remappings=remaps),
        Node(package='rtabmap_viz', executable='rtabmap_viz', output='screen',
             parameters=[params], remappings=remaps),
    ])
```

Drop `-d` from the mapping node once a map exists and you want to extend it over several sessions.

Parameter notes (from `Parameters.h`; `rtabmap --params` prints all of them with their defaults):

| Parameter | Values |
|---|---|
| `Reg/Strategy` | 0 = visual, 1 = ICP, 2 = visual then ICP |
| `Vis/FeatureType`, `Kp/DetectorStrategy` | 0 SURF, 1 SIFT, 2 ORB, 6 GFTT/BRIEF, 8 GFTT/ORB, 11 SuperPoint, ... |
| `Optimizer/Strategy` | 0 TORO, 1 g2o, 2 GTSAM, 3 Ceres (the default depends on what the build includes) |
| `Grid/Sensor` | 0 laser scan, 1 depth image, 2 both (replaces the old `Grid/FromDepth`) |
| `Mem/IncrementalMemory` | `true` mapping, `false` localization |
| `RGBD/LinearUpdate`, `RGBD/AngularUpdate` | minimum motion before a new node is added |
| `Odom/Strategy` | 0 frame-to-map, 1 frame-to-frame; higher values select third-party odometry built into RTAB-Map (5 ORB-SLAM, 9 VINS-Fusion, 10 OpenVINS, 14 LIO-SAM, ...) |

The third-party odometry strategies exist only in a source build of RTAB-Map with those libraries; ORB-SLAM,
VINS-Fusion and OpenVINS are GPL-3.0, and the build then carries their terms.

## Synchronization

- With odometry in TF, `odom_sensor_sync` (on by default) moves each camera image to where the robot was
  at the lidar's stamp and deskews 2D scans ray by ray when `time_increment` is set. With odometry only as a
  topic, sensors are used as they are, with a warning.
- `Did not receive data since 5 seconds! Make sure the input topics are published ...` means the
  synchronizer never matched a set: a topic is missing, its QoS does not match (`qos` argument: 0 system
  default, 1 reliable, 2 best effort), or `approx_sync: false` is set for topics with different stamps.
- A sensor whose frame is not connected to `frame_id`, or whose stamp is not in TF within
  `wait_for_transform`, is dropped.

## The database

- The map lives in `database_path`, `~/.ros/rtabmap.db` by default (under `$ROS_HOME` if set).
- It is written on shutdown. A node killed rather than shut down loses what was not yet written; the
  `backup` service saves now, copies to `<database_path>.back` and starts a new session.
- Restarting on an existing database continues it as a new session; a loop closure between sessions merges
  them. `-d` (`delete_db_on_start`) starts empty.
- The database remembers the parameters it was built with and restores them unless you set them again.
- Inspect a map offline with `rtabmap-databaseViewer ~/.ros/rtabmap.db` (installed with the rtabmap
  package); `rtabmap-export` writes clouds and meshes.

## Mapping and localization at run time

Services sit under the node's name: `/rtabmap/set_mode_localization` for a node named `rtabmap` in the
root namespace, `/rtabmap/rtabmap/set_mode_localization` under `rtabmap.launch.py`'s namespace. Find them
with `ros2 service list | grep rtabmap`.

```bash
ros2 service call /rtabmap/set_mode_localization std_srvs/srv/Empty
ros2 service call /rtabmap/set_mode_mapping std_srvs/srv/Empty   # starts a new session
ros2 service call /rtabmap/backup std_srvs/srv/Empty
ros2 service call /rtabmap/reset std_srvs/srv/Empty              # erases the map and the database
```

Localization mode keeps the map fixed: each update is matched against it and not added. `initial_pose`
(launch argument) or `RGBD/StartAtOrigin` sets where the robot starts on the map.

## Checks

- `ros2 topic echo --once /rtabmap/info` (in the node's namespace) shows `loop_closure_id` non-zero after
  revisiting a place; `rtabmap_viz` shows the loop closure links.
- `ros2 run tf2_ros tf2_echo map odom` comes from rtabmap only (`ros2 topic info -v /tf`).
- The occupancy grid (`map` in the node's namespace) is sharp after a loop: no doubled walls.
- After a clean shutdown the database file has grown, and a restart in localization mode localizes.
