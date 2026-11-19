# Migrating from Gazebo Classic

Part of [sim-gazebo](../SKILL.md): what replaces each piece of a ROS 2 package written for Gazebo
Classic (Gazebo 11 with `gazebo_ros_pkgs`), and the Fortress-era names an agent meets in Humble
code. Gazebo Classic reached end of life in January 2025 and has no packages for Jazzy or Lyrical.
Checked against gazebosim.org's "Migrating ROS 2 packages that use Gazebo Classic" guide, gz-sim 8's
"Migration from Gazebo classic: SDF" tutorial and the gz-sim 8 system sources.

## The one idea that changes

Classic loaded ROS plugins (`libgazebo_ros_*.so`) inside the simulator; each one published ROS topics
itself. Gazebo Sim systems publish on Gazebo Transport, and `ros_gz_bridge` copies chosen topics to
and from ROS. So a Classic plugin usually becomes two things: a Gazebo system or sensor in the SDF,
and an entry in the bridge YAML. ros2_control is the exception: `gz_ros2_control` still runs a ROS
controller manager inside Gazebo.

## Packages, commands and files

| Gazebo Classic | Gazebo Harmonic with Jazzy |
|---|---|
| `gazebo_ros_pkgs`, `gazebo_ros`, `gazebo_plugins` | `ros_gz_sim`, `ros_gz_bridge`, `ros_gz_image` (metapackage `ros_gz`) |
| `gazebo`, `gzserver`, `gzclient` | `gz sim`, `gz sim -s`, `gz sim -g` |
| `gazebo_ros` `gazebo.launch.py world:=...` | `ros_gz_sim` `gz_sim.launch.py gz_args:="-r <world>"` |
| `gzserver.launch.py`, `gzclient.launch.py` | `gz_args:="-r -s <world>"` and `gz_args:="-g"`, or `gz_server.launch.py world_sdf_file:=...` |
| `spawn_entity.py -entity my_robot -topic robot_description` | `ros2 run ros_gz_sim create -name my_robot -topic robot_description` (`-file`, `-x -y -z -R -P -Y` as before) |
| `worlds/*.world` | The same SDF; `.sdf` by convention. Add the world systems ([world.md](world.md)) |
| `model://sun`, `model://ground_plane` | Not shipped: inline models or the Fuel `Sun` and `Ground Plane` |
| `GAZEBO_MODEL_PATH`, `GAZEBO_RESOURCE_PATH` | `GZ_SIM_RESOURCE_PATH` |
| `GAZEBO_PLUGIN_PATH` | `GZ_SIM_SYSTEM_PLUGIN_PATH` |
| `<gazebo_ros gazebo_model_path=.../>` export | Still read by `gz_sim.launch.py` and `gz_server.launch.py`, into `GZ_SIM_RESOURCE_PATH` |
| `/spawn_entity`, `/delete_entity`, `/set_entity_state` services | Gazebo services `/world/<name>/create`, `/remove`, `/set_pose` (bridge them with `ros_gz_interfaces` types), or `simulation_interfaces` on the `gzserver` node |
| `gazebo_ros2_control`: `libgazebo_ros2_control.so`, `gazebo_ros2_control/GazeboSystem` | `gz_ros2_control`: `gz_ros2_control-system` (`gz_ros2_control::GazeboSimROS2ControlPlugin`), `gz_ros2_control/GazeboSimSystem` |

Replace the dependencies in `package.xml` and `CMakeLists.txt` first, then the launch files, then
the world, then the model's plugins, then add the bridge.

## Plugins

| Classic plugin | Replacement in Gazebo Harmonic |
|---|---|
| `libgazebo_ros_diff_drive.so` | `diff_drive_controller` through gz_ros2_control; or `gz-sim-diff-drive-system` + bridge `cmd_vel`, `odom`, `tf` ([launch.md](launch.md)) |
| `libgazebo_ros_ackermann_drive.so` | `ackermann_steering_controller` through gz_ros2_control; or `gz-sim-ackermann-steering-system` |
| `libgazebo_ros_joint_state_publisher.so` | `joint_state_broadcaster`; or `gz-sim-joint-state-publisher-system` + bridge `gz.msgs.Model` to `sensor_msgs/msg/JointState` |
| `libgazebo_ros_joint_pose_trajectory.so` | `joint_trajectory_controller`; or `gz-sim-joint-position-controller-system` / `gz-sim-joint-trajectory-controller-system` |
| `libgazebo_ros_camera.so` (camera, depth) | `camera` / `depth_camera` sensor + Sensors system + bridge or `ros_gz_image` |
| `libgazebo_ros_ray_sensor.so` (`type="ray"`) | `gpu_lidar` sensor + Sensors system; `<ray>` may stay or become `<lidar>` |
| `libgazebo_ros_imu_sensor.so` | `imu` sensor + Imu system |
| `libgazebo_ros_gps_sensor.so` | `navsat` sensor + NavSat system + `<spherical_coordinates>` |
| `libgazebo_ros_bumper.so` | `contact` sensor + Contact system (`gz-sim-touchplugin-system` for a true/false touch topic) |
| `libgazebo_ros_ft_sensor.so` | `force_torque` sensor + ForceTorque system, or through gz_ros2_control |
| `libgazebo_ros_p3d.so` (ground-truth pose) | `gz-sim-odometry-publisher-system` or `gz-sim-pose-publisher-system` + bridge |
| `libgazebo_ros_init.so`, `libgazebo_ros_factory.so`, `libgazebo_ros_state.so` | Nothing to load: `create`, the bridge and the `gzserver` services cover them |

Plugin parameters do not carry over one to one; read each system's parameter list in the gz-sim API
docs (gazebosim.org/api/sim/8). Known changes:

- `<ros><namespace>` and `<ros><remapping>` go away; topic names move to the system's `<topic>` and
  to the bridge YAML.
- Camera and lidar `<frame_name>` becomes `<gz_frame_id>` on the `<sensor>`, plus
  `<optical_frame_id>` in `<camera>` ([sensors.md](sensors.md)).
- Diff drive: `<wheel_diameter>` becomes `<wheel_radius>`, `<odometry_frame>` becomes `<frame_id>`,
  `<robot_base_frame>` becomes `<child_frame_id>`, `<update_rate>` becomes
  `<odom_publish_frequency>`. Classic's per-wheel torque and acceleration limits have no direct
  equivalent: limits apply to the body, and wheel torque comes from the joint's effort limit.
- Classic Ogre material scripts: `Gazebo/<Colour>` names are turned into ambient, diffuse and
  specular colours with a warning; textures from material scripts are not. Write
  `<material><ambient>` and `<diffuse>` (or PBR) instead.

## Launch file, before and after

```python
# Classic
IncludeLaunchDescription(PythonLaunchDescriptionSource(
    PathJoinSubstitution([FindPackageShare('gazebo_ros'), 'launch', 'gazebo.launch.py'])),
    launch_arguments={'world': world}.items())
Node(package='gazebo_ros', executable='spawn_entity.py',
     arguments=['-entity', 'my_robot', '-topic', 'robot_description'])

# Harmonic
IncludeLaunchDescription(PythonLaunchDescriptionSource(
    PathJoinSubstitution([FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])),
    launch_arguments={'gz_args': ['-r ', world], 'on_exit_shutdown': 'true'}.items())
Node(package='ros_gz_sim', executable='create',
     arguments=['-name', 'my_robot', '-topic', 'robot_description'])
Node(package='ros_gz_bridge', executable='parameter_bridge',
     parameters=[{'config_file': bridge_yaml}])   # new: /clock and every sensor topic
```

Classic published `/clock` itself; now the bridge must, or every `use_sim_time` node stalls.

## Fortress and "Ignition" names (Humble code)

Gazebo was called Ignition until 2022; Fortress, the Humble pairing, still uses those names. When
porting Humble code to Jazzy, rename:

| Fortress (Humble) | Harmonic (Jazzy) |
|---|---|
| `ign gazebo`, `ign topic`, `ign service` | `gz sim`, `gz topic`, `gz service` |
| `ignition-gazebo-<name>-system`, `ignition::gazebo::systems::<Name>` | `gz-sim-<name>-system`, `gz::sim::systems::<Name>` |
| `ignition.msgs.<Type>` in bridge arguments | `gz.msgs.<Type>` |
| `IGN_GAZEBO_RESOURCE_PATH`, `IGN_GAZEBO_SYSTEM_PLUGIN_PATH` | `GZ_SIM_RESOURCE_PATH`, `GZ_SIM_SYSTEM_PLUGIN_PATH` |
| `<ignition_frame_id>` | `<gz_frame_id>` |
| `ros_ign_gazebo`, `ros_ign_bridge`, `ros_ign_image` | `ros_gz_sim`, `ros_gz_bridge`, `ros_gz_image` |
| `ign_args` launch argument | `gz_args` |
| `ign_ros2_control-system`, `ign_ros2_control/IgnitionSystem` | `gz_ros2_control-system`, `gz_ros2_control/GazeboSimSystem` |
| `~/.ignition/gazebo` | `~/.gz/sim` |

Jazzy still accepts some old names (`ign_args` and the `IGN_GAZEBO_RESOURCE_PATH` fallback, both
with a deprecation message, and the `ign_ros2_control` aliases); Lyrical drops the gz_ros2_control
aliases. Use the new names everywhere.
