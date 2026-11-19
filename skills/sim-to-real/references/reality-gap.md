# Measuring the reality gap on the robot

Part of [sim-to-real](../SKILL.md): each source of the gap, how it shows up, how to measure it on
the robot, and where it lives in the simulator. Measure before you randomise; the numbers feed
[system-identification.md](system-identification.md) and [ranges.md](ranges.md).

Log every test with `ros2 bag record` (see [deployment.md](deployment.md#logging)) so the same
data can drive a fit later. Write each measured value, its spread and the date into the project's
notes; a guessed value is marked as a guess.

## 1. Actuator dynamics and limits

**Symptoms:** the policy oscillates or chatters on the robot but not in sim; legs sag or cannot lift
the body; fast motions fall short; a joint "sticks" at low speed.

| What | How to measure | Where it goes in sim |
|---|---|---|
| Torque limit and its drop with speed | Datasheet stall torque and no-load speed at your supply voltage; check with current x torque constant while driving a known load | MuJoCo `<dcmotor>` (`nominal`, `saturation`) or `forcerange`; Isaac Lab `DCMotorCfg` (`saturation_effort`, `actuator_effort_limit`, `actuator_velocity_limit`) |
| Velocity limit | Command a large step unloaded; read the plateau of measured velocity | Isaac Lab `actuator_velocity_limit`; MuJoCo: emerges from `<dcmotor>` back-EMF, or clip targets |
| Drive-side PD loop | Step and chirp tests per joint, limb unloaded, then loaded; compare to a sim replay of the same commands | MuJoCo `<position kp kv>`; Isaac Lab `stiffness`, `damping` |
| Friction (Coulomb, viscous) | Slow constant-velocity sweeps in both directions at several speeds; torque (or current) vs velocity gives the Coulomb offset and the viscous slope. Note the breakaway torque from rest | MuJoCo joint `frictionloss`, `damping`; Isaac Lab `friction`, `dynamic_friction`, `viscous_friction` |
| Reflected rotor inertia | Rotor inertia from the motor datasheet times gear ratio squared, or fit it | MuJoCo joint `armature`; Isaac Lab `armature` |
| Backlash | Hold the motor, rock the output by hand, read the play on an output-side encoder, a dial gauge or an IMU on the link | No simulator here has a backlash primitive: randomise a small target offset, or add a short limited passive joint in series |
| Supply voltage sag | Log battery voltage during hard motions | Scales available torque; randomise motor strength |
| Heating | Repeat a hard test until the drive derates; log temperature | Randomise motor strength downwards |

- For a DC motor the available torque falls linearly with speed, from stall torque at zero speed
  to zero at no-load speed. Isaac Lab's `DCMotor` and MuJoCo's `<dcmotor>` both implement this
  curve; an ideal PD actuator does not, and lets the policy use torque the motor cannot give at speed.
- The drive's own PD runs in the drive's units (ticks, percent). Find the gain mapping to N·m/rad by
  fitting, not by reading the register value.
- Hobby servos (Dynamixel, Feetech) have load-dependent and Stribeck friction that the usual
  Coulomb plus viscous model misses; see BAM in [system-identification.md](system-identification.md).
- When the actuator is too complex to model (series elasticity, cascaded loops, unknown firmware),
  learn it: an actuator network ([system-identification.md](system-identification.md)).

## 2. Latency and control rate

**Symptoms:** oscillation that grows with gain; a policy that is stable in sim limit-cycles on the
robot. Tan et al. (RSS 2018) name latency as one of the main causes of instability after transfer.

- **Command-to-motion latency.** Send a one-step spike in the command and time-stamp when the
  resulting motion appears in the measured state; Tan et al. measured their robot this way. Repeat
  it many times, under load, and keep the distribution, not one value.
- **Sensor-to-action latency.** Stamp the sensor sample when it is read (`header.stamp`) and the
  command when it is sent; the difference is what the policy really sees.
- **Loop period and jitter.** Log the time between successive commands from the policy loop under
  full load (all nodes, logging on). Plot the histogram in PlotJuggler or Foxglove.
- **Rates.** Policy rate in sim is `1 / (physics dt * decimation)`; the robot must run at that rate.
  The drive's PD runs faster on the robot than the physics step in sim: identify the PD at the
  rate the sim uses, or model it explicitly.
- In sim: MuJoCo actuator and sensor `delay` with `nsample`; Isaac Lab `DelayedPDActuatorCfg`
  (`min_delay`, `max_delay` in physics steps) and observation `delay_min_lag`, `delay_max_lag`
  (in policy steps). Randomise around the measured distribution.

## 3. Sensor noise and bias

**Symptoms:** a policy that reacts to noise (twitching while standing), slow drift, a robot that
leans in one direction.

- **IMU:** leave the robot still on a level surface and record several minutes. The mean of the gyro
  is its bias, the standard deviation its noise; the accelerometer mean shows mounting tilt. For
  long-term gyro drift, compute an Allan variance from a long still recording (the method is
  defined in IEEE Std 952).
- **Mounting:** tilt the robot nose down and check the sign of the projected gravity the policy will
  get; then roll it. A wrong IMU frame is a description error, not noise (section 6).
- **Encoders:** note the resolution (quantisation step) and whether velocity is measured or
  differentiated from position. Differentiated velocity is noisy; use the same filter in sim as on
  the robot, or add matching noise.
- **Velocity estimates** (base linear velocity from an estimator): compare against motion capture
  or a measured path; if the error is large, drop the observation or train with it noisy.
- In sim: MuJoCo's sensor `noise` attribute is metadata only and does not change the readings;
  add noise in your observation code. Isaac Lab adds noise per observation term (`noise=`), with
  per-episode bias through `NoiseModelWithAdditiveBiasCfg`. Gazebo adds noise in the sensor's SDF.

## 4. Contact and friction

**Symptoms:** feet slip on the robot but not in sim (or the reverse); wheels spin; grasps slide.

- **Tilt test:** put the foot (or a sample of its material, loaded like the foot) on a board of the
  floor material and raise it until it slides; the static friction coefficient is the tangent of
  that angle.
- **Pull test:** drag a weighted foot sample at constant speed with a force gauge; kinetic friction
  is pulling force over normal force.
- Measure every surface you will test on; carpet, lab floor and outdoor ground differ.
- Simulators combine two surfaces' friction differently: MuJoCo uses the element-wise maximum of
  the two geoms (unless one has higher `priority`); PhysX uses each material's combine mode
  (Isaac Lab's locomotion terrain sets `multiply`). Set the floor value so the combination gives the
  measured coefficient.
- Foot compliance, rolling and torsional friction are rarely worth identifying; randomise them
  lightly if contacts matter for the task.

## 5. Mass, centre of mass and inertia

**Symptoms:** the body leans, a leg is overloaded, swing timing is off, a manipulator misses
targets under gravity.

- Weigh the whole robot and, during assembly, every link with its motors, screws and cables. CAD
  masses leave out cables, glue and fasteners; scale the CAD values to the weighed totals.
- Find the base centre of mass by balancing it on an edge in two directions, or by hanging it from
  two points.
- Inertia: CAD of the full link assembly, scaled to the weighed mass; or fit it
  ([system-identification.md](system-identification.md)). Formulas and validity checks are in
  [ros2-robot-description inertials](../../ros2-robot-description/references/inertials.md).
- Payloads (battery, computer, gripper load) change between runs: randomise added base mass.

## 6. The robot description is wrong

**Symptoms:** a joint moves the wrong way, poses look right in RViz but not on the robot, the
policy pushes a joint into its stop, the robot falls on start.

Run these before any policy:

1. **Sign test.** Command +0.1 rad (small, slow) on one joint at a time, in sim and on the robot.
   Both must move the same way. Fix flipped axes in the URDF or the driver, never in the policy.
2. **Zero test.** Put the robot in its zero pose (calibration jig or marks) and compare the
   measured joint positions with zero. Offsets go in the driver's calibration.
3. **Pose test.** Command three or four known poses and measure link positions with a ruler or
   protractor; compare with forward kinematics of the URDF.
4. **Limits.** Move each joint slowly to its physical stops (by hand, motors off) and compare with
   the URDF limits; the sim limits should be inside the real stops.
5. **Order and units.** Print the joint order used in training next to the driver's order; check
   radians versus degrees or ticks, and gear ratios.
6. **IMU frame.** Check the IMU's mounting rotation against the URDF (section 3).

Tools for the URDF itself (check_urdf, RViz, `tf2_echo`) are in
[ros2-robot-description](../../ros2-robot-description/SKILL.md).

## Sources

- Tan et al., "Sim-to-Real: Learning Agile Locomotion For Quadruped Robots", RSS 2018
  (arXiv:1804.10332): latency spike measurement, DC motor model, randomised parameters.
- MuJoCo docs, XML reference (sensor `noise`, `delay`, `nsample`; joint `armature`,
  `frictionloss`, `damping`; `dcmotor`), and the modeling guide on contact parameters (4.0.1).
- Isaac Lab 3.0 source: `isaaclab/actuators`, `isaaclab/utils/noise`, `isaaclab/managers`.
- IEEE Std 952, single-axis interferometric fibre optic gyro test procedure (Allan variance).
