# Sensors in Gazebo Harmonic

Part of [sim-gazebo](../SKILL.md): sensor blocks for a URDF robot, the world system each needs, the
topics and message types they produce, and how their frames reach TF. Checked against sdformat 14
(`sdf/1.11`), gz-sensors 8 and gz-sim 8 sources, the Harmonic sensors tutorial and the `ros_gz_sim_demos`
launch files. How sensor links survive the URDF-to-SDF conversion is in
[simulators.md](../../ros2-robot-description/references/simulators.md).

## What each sensor needs

`T` is the sensor's `<topic>`. Gazebo topics are absolute: `scan` becomes `/scan`.

| `type` | World system | Gazebo topics | Gazebo message | ROS message |
|---|---|---|---|---|
| `gpu_lidar` | Sensors | `T`, `T/points` | `gz.msgs.LaserScan`, `gz.msgs.PointCloudPacked` | `sensor_msgs/msg/LaserScan`, `sensor_msgs/msg/PointCloud2` |
| `camera` | Sensors | `T`, and `camera_info` beside it (`camera/image_raw` gives `/camera/camera_info`) | `gz.msgs.Image`, `gz.msgs.CameraInfo` | `sensor_msgs/msg/Image`, `sensor_msgs/msg/CameraInfo` |
| `depth_camera` | Sensors | `T` (depth image), `T/points`, `camera_info` beside `T` | `gz.msgs.Image`, `gz.msgs.PointCloudPacked` | `Image`, `PointCloud2` |
| `rgbd_camera` | Sensors | `T/image`, `T/depth_image`, `T/points`, `T/camera_info` | as above | as above |
| `imu` | Imu | `T` | `gz.msgs.IMU` | `sensor_msgs/msg/Imu` |
| `navsat` | NavSat + `<spherical_coordinates>` | `T` | `gz.msgs.NavSat` | `sensor_msgs/msg/NavSatFix` |
| `contact` | Contact | `T` | `gz.msgs.Contacts` | `ros_gz_interfaces/msg/Contacts` |
| `force_torque` | ForceTorque | `T` | `gz.msgs.Wrench` | `geometry_msgs/msg/WrenchStamped` |
| `magnetometer` | Magnetometer | `T` | `gz.msgs.Magnetometer` | `sensor_msgs/msg/MagneticField` |
| `air_pressure` | AirPressure | `T` | `gz.msgs.FluidPressure` | `sensor_msgs/msg/FluidPressure` |

All of these bridge `GZ_TO_ROS`. Without `<topic>`, a sensor publishes on a long scoped topic such as
`/world/my_world/model/my_robot/link/base_link/sensor/imu/imu`. The CPU `ray` and `lidar` sensor types
of Gazebo Classic are not implemented in Gazebo Sim; use `gpu_lidar`. Rendering sensors (cameras,
`gpu_lidar`) need a GPU or EGL headless rendering.

## Frames

- Every sensor stamps `header.frame_id` with `<gz_frame_id>` when set, otherwise with its scoped
  name (`my_robot::base_link::lidar`), which matches no TF frame. Set `<gz_frame_id>` to the URDF
  link the `<gazebo reference>` names. It stays correct after the conversion lumps that link into
  its parent, because TF still has the link from `robot_state_publisher`.
- Gazebo cameras look along +x of their link. ROS image consumers expect an optical frame (z
  forward, x right, y down). Set `<camera><optical_frame_id>` to the optical frame from the
  description: images and `camera_info` then carry it while the sensor itself stays on
  `camera_link`.
- The sensor sits at the referenced link's origin. Do not repeat the mount offset in a sensor
  `<pose>`; it is already in the URDF joint.
- Last resort: the bridge's `frame_id` key (YAML) or `override_frame_id` parameter rewrites the frame
  on the ROS side.

## URDF blocks

Values marked "example" are placeholders: take ranges, rates, resolution and noise from the sensor's
datasheet or measure them. Put these in `my_robot.gazebo.xacro`, included only for simulation.

### 2D lidar

```xml
<gazebo reference="lidar_link">
  <sensor name="lidar" type="gpu_lidar">
    <topic>scan</topic>
    <gz_frame_id>lidar_link</gz_frame_id>
    <update_rate>10</update_rate>                  <!-- example -->
    <always_on>true</always_on>
    <visualize>false</visualize>
    <lidar>
      <scan>
        <horizontal>
          <samples>360</samples>                     <!-- example -->
          <resolution>1</resolution>
          <min_angle>${-pi}</min_angle>
          <max_angle>${pi}</max_angle>
        </horizontal>
      </scan>
      <range>
        <min>0.12</min>                              <!-- example -->
        <max>12.0</max>                              <!-- example -->
        <resolution>0.01</resolution>
      </range>
      <noise>
        <type>gaussian</type>
        <mean>0.0</mean>
        <stddev>0.01</stddev>                        <!-- example, metres -->
      </noise>
    </lidar>
  </sensor>
</gazebo>
```

`<ray>` is accepted in place of `<lidar>`. For a 3D lidar, add a `<vertical>` block (`samples` is the
number of rings) and consume `T/points`; `LaserScan` suits single-ring sensors. Lidar and camera noise
use a `<type>` child element.

### Camera

```xml
<gazebo reference="camera_link">
  <sensor name="camera" type="camera">
    <topic>camera/image_raw</topic>
    <gz_frame_id>camera_link</gz_frame_id>
    <update_rate>30</update_rate>                  <!-- example -->
    <always_on>true</always_on>
    <camera>
      <optical_frame_id>camera_optical_frame</optical_frame_id>
      <camera_info_topic>camera/camera_info</camera_info_topic>
      <horizontal_fov>1.2</horizontal_fov>         <!-- example, rad -->
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>
      </image>
      <clip><near>0.05</near><far>20.0</far></clip>
      <noise>
        <type>gaussian</type>
        <mean>0.0</mean>
        <stddev>0.007</stddev>                     <!-- example, of the 0..1 pixel range -->
      </noise>
    </camera>
  </sensor>
</gazebo>
```

`camera_info_topic` is optional; the default already puts `camera_info` beside the image topic.
For depth, change `type` to `depth_camera` (topic `T` is a 32-bit float depth image) or to
`rgbd_camera` (colour, depth, points and info under `T/`). Bridge colour images with
`ros_gz_image image_bridge` or the YAML, `camera_info` with the YAML.

### IMU

```xml
<gazebo reference="imu_link">
  <sensor name="imu" type="imu">
    <topic>imu</topic>
    <gz_frame_id>imu_link</gz_frame_id>
    <update_rate>100</update_rate>                 <!-- example -->
    <always_on>true</always_on>
    <imu>
      <angular_velocity>
        <x><noise type="gaussian"><mean>0</mean><stddev>0.0002</stddev></noise></x>
        <y><noise type="gaussian"><mean>0</mean><stddev>0.0002</stddev></noise></y>
        <z><noise type="gaussian"><mean>0</mean><stddev>0.0002</stddev></noise></z>
      </angular_velocity>
      <linear_acceleration>
        <x><noise type="gaussian"><mean>0</mean><stddev>0.017</stddev></noise></x>
        <y><noise type="gaussian"><mean>0</mean><stddev>0.017</stddev></noise></y>
        <z><noise type="gaussian"><mean>0</mean><stddev>0.017</stddev></noise></z>
      </linear_acceleration>
    </imu>
  </sensor>
</gazebo>
```

The stddev values are examples (rad/s and m/s²); derive them from the datasheet's noise density and
the update rate. IMU noise is an attribute (`<noise type="gaussian">`) and also takes `bias_mean` and
`bias_stddev`. Without the Imu system in the world, the topic never appears.

### GPS (NavSat)

```xml
<gazebo reference="gps_link">
  <sensor name="gps" type="navsat">
    <topic>navsat</topic>
    <gz_frame_id>gps_link</gz_frame_id>
    <update_rate>5</update_rate>                   <!-- example -->
    <always_on>true</always_on>
  </sensor>
</gazebo>
```

The world needs the NavSat system and a `<spherical_coordinates>` block ([world.md](world.md)) that
places the world origin on the globe; without it the log says `Spherical coordinates not set`. The bridge
maps `gz.msgs.NavSat` to `sensor_msgs/msg/NavSatFix` (or `gps_msgs/msg/GPSFix`).

### Contact (bumper)

```xml
<gazebo reference="bumper_link">
  <sensor name="bumper" type="contact">
    <topic>bumper</topic>
    <update_rate>50</update_rate>                  <!-- example -->
    <contact>
      <!-- the collision's name in the converted SDF, not in the URDF -->
      <collision>bumper_link_collision</collision>
    </contact>
  </sensor>
</gazebo>
```

The conversion renames collisions: an unnamed URDF collision on `bumper_link` becomes
`bumper_link_collision` (further ones get `_1`, `_2`), a named one gets `_collision` appended, and
when the link is lumped into its parent the converter rewrites a `<link>_collision` reference to the
parent's merged name. Confirm the name in `gz sdf -p` output. Needs the Contact system.

## Checking a sensor

```bash
gz topic -l | grep -E 'scan|camera|imu'      # the topics exist
gz topic -i -t /scan                         # publisher and message type
gz topic -e -t /scan -n 1                    # one message, Gazebo side
ros2 topic echo --once /scan --field header  # frame_id and a sim-time stamp, ROS side
ros2 run tf2_ros tf2_echo base_link lidar_link
```

In RViz (with `use_sim_time`), a scan must line up with the walls in Gazebo when the robot turns;
a scan that rotates with the robot while the walls stay put means a wrong frame or a wrong joint
axis. Camera images in RViz's Camera display must show the scene upright with the TF axes overlaid
correctly.
