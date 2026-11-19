# World files, physics and resource paths (Gazebo Harmonic)

Part of [sim-gazebo](../SKILL.md): a world template for a ROS 2 robot, what each part does, and how
Gazebo finds models, meshes and plugins. Checked against gz-sim 8 (`gz-sim8` branch: example worlds,
the "Finding resources", "Server configuration" and "Physics engines" tutorials) and sdformat 14.

## `my_robot_gazebo/worlds/my_world.sdf`

```xml
<?xml version="1.0"?>
<sdf version="1.9">
  <world name="my_world">
    <!-- 1 ms steps at real time. real_time_factor 0 runs as fast as the CPU allows. -->
    <physics name="1ms" type="ignored">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>

    <!-- Listing any plugin drops the default set, so the first three are always needed. -->
    <plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"/>
    <plugin filename="gz-sim-user-commands-system" name="gz::sim::systems::UserCommands"/>
    <plugin filename="gz-sim-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster"/>
    <!-- Rendering sensors: camera, depth_camera, rgbd_camera, gpu_lidar -->
    <plugin filename="gz-sim-sensors-system" name="gz::sim::systems::Sensors">
      <render_engine>ogre2</render_engine>
    </plugin>
    <plugin filename="gz-sim-imu-system" name="gz::sim::systems::Imu"/>
    <plugin filename="gz-sim-navsat-system" name="gz::sim::systems::NavSat"/>
    <plugin filename="gz-sim-contact-system" name="gz::sim::systems::Contact"/>

    <scene>
      <ambient>0.4 0.4 0.4 1</ambient>
      <background>0.7 0.7 0.7 1</background>
      <shadows>true</shadows>
    </scene>

    <!-- Origin of the world in latitude/longitude; navsat sensors need it. Placeholder values. -->
    <spherical_coordinates>
      <surface_model>EARTH_WGS84</surface_model>
      <world_frame_orientation>ENU</world_frame_orientation>
      <latitude_deg>0.0</latitude_deg>
      <longitude_deg>0.0</longitude_deg>
      <elevation>0.0</elevation>
      <heading_deg>0</heading_deg>
    </spherical_coordinates>

    <light type="directional" name="sun">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry><plane><normal>0 0 1</normal><size>100 100</size></plane></geometry>
        </collision>
        <visual name="visual">
          <geometry><plane><normal>0 0 1</normal><size>100 100</size></plane></geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- A static obstacle built from primitives -->
    <model name="wall">
      <static>true</static>
      <pose>3 0 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry><box><size>0.2 4 1</size></box></geometry>
        </collision>
        <visual name="visual">
          <geometry><box><size>0.2 4 1</size></box></geometry>
          <material>
            <ambient>0.5 0.5 0.5 1</ambient>
            <diffuse>0.5 0.5 0.5 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- A model installed by a ROS package; found through GZ_SIM_RESOURCE_PATH (below). -->
    <include>
      <uri>package://my_robot_gazebo/models/shelf</uri>
      <name>shelf_1</name>
      <pose>2 -2 0 0 0 1.57</pose>
    </include>
  </world>
</sdf>
```

The robot is not in the world file: it comes from `/robot_description` through `create`, so the same
world serves several robots. Remove the systems and blocks you do not need; an unused system only
costs a little start-up time, a missing one silences its sensors.

Instead of the inline sun and ground plane you can include the Fuel versions:

```xml
<include><uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/Sun</uri></include>
<include><uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/Ground Plane</uri></include>
```

Gazebo Classic's `model://sun` and `model://ground_plane` are not shipped with Gazebo Sim.

## World systems

| Needed for | `filename` | `name` |
|---|---|---|
| Anything that moves | `gz-sim-physics-system` | `gz::sim::systems::Physics` |
| `create`, `remove`, `set_pose` services, GUI edits | `gz-sim-user-commands-system` | `gz::sim::systems::UserCommands` |
| GUI and `/world/<name>/pose/info` | `gz-sim-scene-broadcaster-system` | `gz::sim::systems::SceneBroadcaster` |
| `camera`, `depth_camera`, `rgbd_camera`, `gpu_lidar` | `gz-sim-sensors-system` | `gz::sim::systems::Sensors` |
| `imu` | `gz-sim-imu-system` | `gz::sim::systems::Imu` |
| `navsat` | `gz-sim-navsat-system` | `gz::sim::systems::NavSat` |
| `contact` | `gz-sim-contact-system` | `gz::sim::systems::Contact` |
| `force_torque` | `gz-sim-forcetorque-system` | `gz::sim::systems::ForceTorque` |
| `magnetometer` | `gz-sim-magnetometer-system` | `gz::sim::systems::Magnetometer` |
| `air_pressure` | `gz-sim-air-pressure-system` | `gz::sim::systems::AirPressure` |
| `altimeter` | `gz-sim-altimeter-system` | `gz::sim::systems::Altimeter` |

These load once per world. Gazebo Sim has no per-sensor camera or lidar plugin: a `<plugin>` inside a
`<sensor>` is only for custom sensor systems. The Sensors system's `<render_engine>` defaults to
`ogre2`; `ogre` (Ogre 1) is the fallback for GPUs without OpenGL 3.3.

Without any `<plugin>` in the world, Gazebo loads Physics, UserCommands and SceneBroadcaster from
`~/.gz/sim/8/server.config` (or `GZ_SIM_SERVER_CONFIG_PATH`). Gazebo creates that file on first run
and never overwrites it, so a stale copy can change behaviour between machines.

## Physics

| Element | Meaning | Notes |
|---|---|---|
| `<max_step_size>` | Physics step in seconds | 0.001 in the stock worlds. Smaller is steadier for stiff contacts and fast joints, and slower. The ros2_control update period must not be shorter than it. |
| `<real_time_factor>` | Target ratio of sim time to wall time | 1.0 for interactive work; 0 for unthrottled CI runs. The achieved value is on `/stats`. |
| `<physics type=...>` | Required by SDF, not read by Gazebo Sim | The stock worlds write `type="ignored"`. |
| `<real_time_update_rate>` | Classic only | Gazebo Sim derives the loop period from step and real-time factor. |
| `<ode>` solver block | Classic only | Not among the physics options Gazebo Sim reads. |
| `<dart><collision_detector>` | `ode` (default), `bullet`, `fcl`, `dart` | Read by the default DART engine. |
| `<dart><solver><solver_type>` | `dantzig` (default), `pgs` | Read by DART. |

The engine is DART unless chosen otherwise, either on the command line
(`gz sim --physics-engine gz-physics-bullet-featherstone-plugin`) or on the Physics system:

```xml
<plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics">
  <engine><filename>gz-physics-bullet-featherstone-plugin</filename></engine>
</plugin>
```

Bullet (`gz-physics-bullet-plugin`) and Bullet Featherstone are described upstream as preliminary;
test contacts and joint limits before switching. Friction, damping and contact stiffness per link
come from the robot description ([simulators.md](../../ros2-robot-description/references/simulators.md)).

## How Gazebo finds files

| Resource | Search order |
|---|---|
| `<include><uri>` models, lights, actors | `GZ_SIM_RESOURCE_PATH` (scheme stripped), then the working directory or absolute path, then Fuel (cache `~/.gz/fuel`, then the web) |
| `<mesh><uri>` | Working directory or absolute path, then `GZ_SIM_RESOURCE_PATH` |
| System plugins (`filename=`) | `GZ_SIM_SYSTEM_PLUGIN_PATH`, then `~/.gz/sim/plugins`, then the installed systems |
| Physics engine plugins | Installed engines, plus `GZ_SIM_PHYSICS_ENGINE_PATH` |

`model://shelf` and `package://my_robot_gazebo/models/shelf` both become a relative path looked up on
`GZ_SIM_RESOURCE_PATH`. With `<install>/share` on the path, `package://<pkg>/...` resolves like it
does in ROS, which is what URDF meshes need. Three ways to put it there:

1. **Launch file** (explicit, works with every launcher):

   ```python
   AppendEnvironmentVariable(
       'GZ_SIM_RESOURCE_PATH',
       PathJoinSubstitution([FindPackageShare('my_robot_description'), '..'])),
   ```

2. **colcon environment hook** (active whenever the workspace is sourced, so plain `gz sim` works
   too). In the package that owns the files:

   ```text
   # hooks/my_robot_gazebo.dsv.in
   prepend-non-duplicate;GZ_SIM_RESOURCE_PATH;@CMAKE_INSTALL_PREFIX@/share
   ```

   ```cmake
   ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/hooks/${PROJECT_NAME}.dsv.in")
   install(DIRECTORY worlds models DESTINATION share/${PROJECT_NAME})
   ```

3. **`package.xml` export**, read by `ros_gz_sim`'s `gz_sim.launch.py` and `gz_server.launch.py`
   (both scan every package for it):

   ```xml
   <export>
     <build_type>ament_cmake</build_type>
     <gazebo_ros gazebo_model_path="${prefix}/../"/>
   </export>
   ```

   `${prefix}` is the package's share directory; `plugin_path` adds to `GZ_SIM_SYSTEM_PLUGIN_PATH`.

Pass `debug_env:=true` to `gz_sim.launch.py` to print the variables it sets. A missing file shows as
`Unable to find uri[...]` (includes) or `Failed to load mesh` (meshes) at `-v 4`.

## Fuel models

- Browse at app.gazebosim.org; each model page gives an `<include>` snippet with its URL.
- The first load downloads into `~/.gz/fuel`; later loads use the cache. A world full of Fuel models
  starts slowly the first time and fails offline.
- For CI, fetch once (`gz fuel download -u "https://fuel.gazebosim.org/1.0/OpenRobotics/models/Sun"`)
  and cache `~/.gz/fuel`, or copy the model folder (`model.config`, `model.sdf`, `meshes/`) into
  `my_robot_gazebo/models/` after checking its licence on the model page.

## Checking a world

```bash
gz sdf -k worlds/my_world.sdf                         # schema and frame checks
gz sim -s -r -v 4 --iterations 2000 worlds/my_world.sdf   # loads, steps 2 s of sim time, exits
gz sim -v 4 worlds/my_world.sdf                       # with the GUI; press play or pass -r
```

While it runs: `gz topic -l`, `gz service -l | grep /world/my_world`, `gz model --list`, and
`gz topic -e -t /stats -n 1` for the real-time factor.
