# Getting the description into Gazebo and MuJoCo

Part of [ros2-robot-description](../SKILL.md): what a URDF needs so that simulators load it
correctly. Running and tuning the simulation itself is for the `sim-gazebo` and `sim-mujoco`
skills. Checked against `ros_gz` and `gz_ros2_control` (`jazzy` branches), sdformat 14 and the
MuJoCo docs (release 4.0.1, November 2026).

## Gazebo Harmonic (the Jazzy pairing)

Gazebo reads the URDF through sdformat, which converts it to SDF when the robot is spawned. Gazebo
Classic plugins (`libgazebo_ros_diff_drive.so`, `libgazebo_ros_camera.so`, ...) do not exist here;
use Gazebo Sim systems, `ros_gz_bridge`, or `gz_ros2_control`.

### What the conversion does to your URDF

- **Fixed joints are lumped**: the child link's mass, visuals and collisions merge into the parent.
  Sensor links on fixed joints are fine. To keep a fixed joint as a joint, add
  `<gazebo reference="joint_name"><preserveFixedJoint>true</preserveFixedJoint></gazebo>`; the
  child then needs real mass.
- **Massless links on moving joints are dropped**, together with their joint, with a `urdf2sdf`
  error naming the link. Every link on a non-fixed joint needs an `<inertial>` with mass > 0.
- A `<gazebo reference="link">` on a lumped link moves to the parent along with it.

Preview the result without starting Gazebo:

```bash
xacro urdf/my_robot.urdf.xacro sim:=true > /tmp/my_robot.urdf
gz sdf -p /tmp/my_robot.urdf > /tmp/my_robot.sdf   # conversion warnings go to the terminal
gz sdf --inertial-stats /tmp/my_robot.sdf          # total mass, centre of mass, inertia
```

### `urdf/my_robot.gazebo.xacro`

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">
  <!-- Loads ros2_control inside Gazebo; reads the <ros2_control> block of this same URDF. -->
  <gazebo>
    <plugin filename="gz_ros2_control-system" name="gz_ros2_control::GazeboSimROS2ControlPlugin">
      <parameters>$(find my_robot_bringup)/config/controllers.yaml</parameters>
    </plugin>
  </gazebo>

  <!-- Contact friction per link: a near-frictionless caster, grippy wheels. -->
  <gazebo reference="caster_link">
    <mu1>0.01</mu1>
    <mu2>0.01</mu2>
  </gazebo>

  <gazebo reference="lidar_link">
    <sensor name="lidar" type="gpu_lidar">
      <topic>scan</topic>
      <update_rate>10</update_rate>
      <gz_frame_id>lidar_link</gz_frame_id>
      <lidar>
        <scan>
          <horizontal>
            <samples>360</samples>
            <min_angle>${-pi}</min_angle>
            <max_angle>${pi}</max_angle>
          </horizontal>
        </scan>
        <range><min>0.12</min><max>12.0</max></range>
      </lidar>
    </sensor>
  </gazebo>

  <!-- The camera looks along camera_link's +x; images are stamped in the optical frame. -->
  <gazebo reference="camera_link">
    <sensor name="camera" type="camera">
      <topic>camera/image_raw</topic>
      <update_rate>30</update_rate>
      <gz_frame_id>camera_optical_frame</gz_frame_id>
      <camera>
        <horizontal_fov>1.2</horizontal_fov>
        <image><width>640</width><height>480</height></image>
        <clip><near>0.05</near><far>20</far></clip>
      </camera>
    </sensor>
  </gazebo>
</robot>
```

Sensor values above are placeholders; take them from the sensor's datasheet. `$(find
my_robot_bringup)` needs that package built and sourced before `xacro` runs.

- The world must load `gz-sim-sensors-system` (with `<render_engine>ogre2</render_engine>`) for
  cameras and lidars. The stock `empty.sdf` does not: it loads only physics, user commands, the
  scene broadcaster and contact. IMUs also need `gz-sim-imu-system`. A world that loads them is in
  [sim-gazebo's world reference](../../sim-gazebo/references/world.md).
- Without `<gz_frame_id>`, messages carry Gazebo's scoped name, which matches no TF frame.
- The `gz_ros2_control` plugin name and the hardware plugin `gz_ros2_control/GazeboSimSystem` are
  the same on Humble, Jazzy and Lyrical branches.

### Meshes

RViz resolves `package://my_robot_description/...` through the ament index. Gazebo looks the
package up in `GZ_SIM_RESOURCE_PATH`, so the folder that contains `my_robot_description` must be
on it. Either keep `<gazebo_ros gazebo_model_path="${prefix}/../"/>` in the package's `<export>`
(read by `ros_gz_sim`'s `gz_sim.launch.py`), or set it yourself:

```bash
export GZ_SIM_RESOURCE_PATH=$(ros2 pkg prefix my_robot_description)/share:$GZ_SIM_RESOURCE_PATH
```

Missing meshes show as an invisible or collision-less robot and an "Unable to find file" message.

### Spawn and bridge

```bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="-r /path/to/my_world.sdf"  # a world with the Sensors system
ros2 launch my_robot_description display.launch.py sim:=true gui:=false
ros2 run ros_gz_sim create -topic robot_description -name my_robot -z 0.05
ros2 run ros_gz_bridge parameter_bridge \
  /clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock \
  /scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan
```

In a bridge argument `[` means Gazebo to ROS, `]` ROS to Gazebo, `@` both ways. Every node needs
`use_sim_time: true` once `/clock` is bridged.

## MuJoCo

MuJoCo loads URDF directly but understands only part of it, so the usual path is: expand the
xacro, add a `<mujoco>` block, convert to MJCF once, then edit the MJCF.

```xml
<!-- inside <robot>, e.g. from a xacro file included only when mujoco:=true -->
<mujoco>
  <compiler meshdir="../meshes/collision/" strippath="true"/>
</mujoco>
```

```python
# Expand first, next to the xacro so the relative meshdir resolves:
#   xacro urdf/my_robot.urdf.xacro mujoco:=true > urdf/my_robot.mujoco.urdf
import mujoco

spec = mujoco.MjSpec.from_file('urdf/my_robot.mujoco.urdf')
spec.compile()                      # fails loudly on bad inertia or missing meshes
with open('urdf/my_robot.xml', 'w') as f:
    f.write(spec.to_xml())
```

View it with `python -m mujoco.viewer --mjcf=urdf/my_robot.xml`.

- A relative `meshdir` is resolved against the folder of the file being loaded.
- `package://` URIs are not resolved by released MuJoCo (a provider plugin exists only in source,
  unreleased as of 4.0.1). Use `strippath="true"` and `meshdir`, and keep mesh file names unique.
- `balanceinertia="true"` makes MuJoCo accept inertias that break the triangle inequality. Treat
  it as a stopgap; fix the numbers ([inertials.md](inertials.md)).
- Since MuJoCo 3.7.0 `strippath` defaults to false for URDF too; set it yourself.
- URDF defaults differ from MJCF: `fusestatic="true"` merges links on fixed joints into their
  parents (sensor frames vanish unless something references them), `discardvisual="true"` drops
  visual geometry (keep it with `discardvisual="false"`, and then every visual mesh must also be
  findable in `meshdir`), and angles are radians.
- URDF has no actuators: a joint's `effort` limit becomes `actuatorfrcrange`; add `<actuator>`
  elements to the MJCF. The parser reads `<link>`, `<joint>`, `<material>` and `<mujoco>`
  elements only, so `<gazebo>` and `<ros2_control>` content is ignored.
- MuJoCo does not schema-check URDF, so a misspelled attribute in the `<mujoco>` block is ignored
  without a message.
- For ros2_control on MuJoCo, Jazzy has a released `mujoco_ros2_control` package; the `sim-mujoco`
  skill covers it.
