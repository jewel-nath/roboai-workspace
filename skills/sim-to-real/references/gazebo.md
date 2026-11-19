# Gazebo: the full ROS 2 stack as a sim-to-sim stage

Part of [sim-to-real](../SKILL.md). Checked against `gz-sim8`, `gz-sensors8`, sdformat 14 (SDF 1.11)
and `gz_ros2_control` on the `jazzy` branch, for ROS 2 Jazzy with Gazebo Harmonic. Spawning,
bridging and `<gazebo>` tags are in
[ros2-robot-description simulators](../../ros2-robot-description/references/simulators.md);
worlds and tuning are for the [sim-gazebo](../../sim-gazebo/SKILL.md) skill.

## What Gazebo tests, and what it does not

Use Gazebo to run the **exact robot software**: the same launch files, controllers, topic names,
policy node and deploy spec, with only the hardware plugin switched (`sim:=true` selects
`gz_ros2_control/GazeboSimSystem`). It finds wiring faults: wrong topic, wrong joint order, wrong
frame, a missing `use_sim_time`, a policy node that cannot keep its rate with everything running.

It is a weak dynamics check when the controller uses a **position** command interface:
`gz_ros2_control` turns a position command into a velocity command,
`-position_proportional_gain * error`, not the torque-level PD the policy was trained with. For a
dynamics sim-to-sim, run the policy in MuJoCo ([mujoco.md](mujoco.md)), or command the `effort`
interface from a controller that runs the trained PD.

## Clock and rate

- Bridge `/clock` and set `use_sim_time: true` on every node, the policy node included. A ROS 2
  timer on a node with sim time follows `/clock`, so the policy rate stays right when Gazebo runs
  slower than real time.
- Check the real-time factor in the Gazebo GUI or with `gz topic -e -t /stats`; if it drops well
  below 1, the test still runs, but wall-clock jitter numbers from it mean nothing.

## Sensor noise in SDF

Gazebo adds noise inside the sensor. An IMU with white noise and a bias, inside the robot's
xacro (values are placeholders; use your measurements from
[reality-gap.md](reality-gap.md#3-sensor-noise-and-bias)):

```xml
<xacro:macro name="gyro_noise">
  <noise type="gaussian">
    <mean>0.0</mean>
    <stddev>0.01</stddev>          <!-- white noise, rad/s -->
    <bias_mean>0.002</bias_mean>   <!-- bias, rad/s -->
    <bias_stddev>0.001</bias_stddev>
  </noise>
</xacro:macro>

<gazebo reference="imu_link">
  <sensor name="imu" type="imu">
    <always_on>true</always_on>
    <update_rate>200</update_rate>
    <topic>imu</topic>
    <gz_frame_id>imu_link</gz_frame_id>
    <imu>
      <angular_velocity>
        <x><xacro:gyro_noise/></x>
        <y><xacro:gyro_noise/></y>
        <z><xacro:gyro_noise/></z>
      </angular_velocity>
    </imu>
  </sensor>
</gazebo>
```

- The bias is drawn once when the sensor loads, from a normal distribution with `bias_mean` and
  `bias_stddev`, and given a random sign; it changes per launch, not per episode.
- `dynamic_bias_stddev` with `dynamic_bias_correlation_time` makes the bias drift as a first-order
  Gauss-Markov process; `precision` quantises the output.
- `linear_acceleration` takes the same per-axis `<noise>` blocks. The world must load
  `gz-sim-imu-system` (and `gz-sim-sensors-system` for cameras and lidars).
- Bridge it: `ros2 run ros_gz_bridge parameter_bridge /imu@sensor_msgs/msg/Imu[gz.msgs.IMU`.

## Joint friction and damping

URDF `<dynamics damping="..." friction="..."/>` on a joint becomes the SDF joint axis
`<dynamics>`. Contact friction per link uses `<gazebo reference="..."><mu1>`/`<mu2>` (see the
simulators reference above).

## Perturbing parameters per run

Gazebo has no per-episode randomisation API for masses or friction. Make them xacro arguments and
sample them in the script that launches each test run:

```xml
<xacro:arg name="mass_scale" default="1.0"/>
<xacro:arg name="foot_mu" default="0.9"/>
<xacro:property name="mass_scale" value="$(arg mass_scale)"/>

<link name="base_link">
  <inertial>
    <mass value="${3.2 * mass_scale}"/>   <!-- 3.2 kg: placeholder for the weighed mass -->
    <!-- scale the inertia tensor by mass_scale too -->
  </inertial>
</link>
<gazebo reference="left_foot">
  <mu1>$(arg foot_mu)</mu1>
  <mu2>$(arg foot_mu)</mu2>
</gazebo>
```

Pass the arguments through your bringup launch file to the `xacro` command, and record the sampled
values in the run's bag (`--custom-data` on `ros2 bag record` stores key-value pairs in the bag
metadata).

## Pushes

Load the wrench system in the world:

```xml
<plugin filename="gz-sim-apply-link-wrench-system" name="gz::sim::systems::ApplyLinkWrench"/>
```

Then push the base for one step (world frame force, link named `model::link`):

```bash
gz topic -t /world/default/wrench -m gz.msgs.EntityWrench \
  -p "entity: {name: 'my_robot::base_link', type: LINK}, wrench: {force: {x: 40, y: 0, z: 0}}"
```

`/world/<world>/wrench/persistent` keeps applying a wrench every step until
`/world/<world>/wrench/clear` removes it. The force value is a placeholder; size pushes by the
velocity change they cause on your robot ([ranges.md](ranges.md#disturbances)).

## Latency

Gazebo does not model command or sensor latency. To test the stack with it, delay commands in the
policy node (a ring buffer of N policy steps), using the latency measured on the robot.

## Distro differences

- **Lyrical with Gazebo Jetty:** unchanged in the sources checked: `ApplyLinkWrench` and its
  example (`gz-sim10`), the bias sampling (`gz-sensors10`), and the position-to-velocity handling
  (`gz_ros2_control`, `lyrical`).
- **Humble with Fortress:** use `ign topic`, message type `ignition.msgs.EntityWrench`, plugin
  file `ignition-gazebo-apply-link-wrench-system`, and `ignition-gazebo-imu-system`.

## Sources

- gz-sim `src/systems/apply_link_wrench/ApplyLinkWrench.hh` and
  `examples/worlds/apply_link_wrench.sdf` (`gz-sim8`, `gz-sim10`, `ign-gazebo6`).
- gz-sensors `src/GaussianNoiseModel.cc` (`gz-sensors8`); sdformat `sdf/1.11/noise.sdf`,
  `imu.sdf`, `joint.sdf` (`sdf14`).
- gz_ros2_control `gz_ros2_control/src/gz_system.cpp` (`jazzy`): position commands become
  velocity commands with `position_proportional_gain`.
- rosbag2 `ros2bag/verb/record.py` (`jazzy`) for `--custom-data`.
