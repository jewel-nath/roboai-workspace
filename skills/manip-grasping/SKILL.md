---
name: manip-grasping
description: Pick and place with a ROS 2 Jazzy arm - parallel_gripper_action_controller and GripperActionController (ParallelGripperCommand,
  GripperCommand), MoveIt gripper controllers, hand-eye calibration (easy_handeye2, MoveIt Calibration, cv2.calibrateHandEye), grasp poses
  (top-down, FoundationPose, Contact-GraspNet), approach-grasp-lift, force_torque_sensor_broadcaster, admittance_controller, grasp checks, safety limits.
license: Apache-2.0
metadata:
  sources: []
  evidence: researched
  last_verified: 2026-11-25
---

# Grasping

Lets an agent make an arm pick an object and put it down safely: drive the gripper through
ros2_control, place the camera in the arm's frame, choose a grasp, run approach-close-lift with
checks, and use a wrist force-torque sensor. Written for Jazzy against ros2_controllers 4.43.1,
control_msgs 5.11.0, control_toolbox 4.11.1, MoveIt 2.12.4 and MoveIt Task Constructor 0.1.8 (the
Jazzy binaries), easy_handeye2 0.5.0 and MoveIt Calibration `ros2` (source); the recipes were not
run. Lyrical and Humble differences are at the end.

## When to use

- Adding a gripper to an arm: URDF joints and `tcp`, `<ros2_control>` tag, gripper controller,
  the MoveIt gripper controller entry; testing open and close from the command line.
- Calibrating a wrist or fixed camera to the arm (eye-in-hand, eye-to-hand).
- Turning a detection, an object pose or a point cloud into a grasp pose the arm can reach.
- Writing the pick: pre-grasp, straight approach, close, check, attach, lift, place, release.
- Reading a wrist F/T sensor, zeroing it, compensating the tool's weight; compliant placing.
- Debugging: gripper goal aborts, closes on nothing, object slips, camera and arm disagree.

Elsewhere: MoveIt setup, SRDF, planners, MTC basics and Servo in
[manip-moveit2](../manip-moveit2/SKILL.md); controllers and hardware plugins in general in
[ros2-control](../ros2-control/SKILL.md); URDF and frames in
[ros2-robot-description](../ros2-robot-description/SKILL.md); cameras, intrinsics and AprilTags in
[perception-camera](../perception-camera/SKILL.md). Force and impedance control, insertion and
assembly belong to the later `control-` skills (Phase 5); learned picking policies to
[learn-robot-learning](../learn-robot-learning/SKILL.md); system safety to [arch-safety](../arch-safety/SKILL.md).

## Quick start

On mock hardware, no robot needed:

```bash
sudo apt install ros-jazzy-ros2-controllers   # includes parallel_gripper_controller
```

1. Give the gripper one driven finger joint, a mimic finger, a fixed `tcp` link between the
   fingertips, and a `<ros2_control>` entry exporting position and velocity states.
2. Add `gripper_controller` of type `parallel_gripper_action_controller/GripperActionController`
   with `joint`, `allow_stalling: true` and a `goal_tolerance` in the joint's units.
3. Spawn it with the arm controller and send goals:

```bash
ros2 action send_goal /gripper_controller/gripper_cmd control_msgs/action/ParallelGripperCommand \
  "{command: {name: [gripper_left_finger_joint], position: [0.0]}}"
ros2 topic echo --once /joint_states     # both finger joints moved
```

Files to adapt: [references/gripper.md](references/gripper.md).

## Workflow

### 1. Model the gripper and its TCP

- One actuated finger joint with real limits; other fingers as URDF `<mimic>` joints (state
  interfaces only in the `<ros2_control>` tag).
- A fixed `tcp` link midway between the fingertips: z out of the palm toward the object, x from
  finger to finger. Plan for `tcp`, never for `tool0` plus a hand-made offset.
- With a wrist F/T sensor, keep one serial chain: `tool0` -> `ft_sensor_link` -> gripper -> `tcp`.

Check: `check_urdf` passes; in RViz the `tcp` axes sit between the fingertips, z pointing out.

### 2. Run the gripper controller

- Default: `parallel_gripper_action_controller` (action `ParallelGripperCommand`). The older
  `position_controllers/GripperActionController` (`GripperCommand`) is deprecated on Jazzy.
- In MoveIt, the gripper entry is `type: ParallelGripperCommand`, `action_ns: gripper_cmd`.
- Force: use the gripper's force limit if the hardware has one (`max_effort_interface`);
  position-only servos get a close target slightly under the object width.

Check: open and close goals succeed; a close on a real object returns `stalled: true` with the
position at the object's width. Details: [references/gripper.md](references/gripper.md).

### 3. Calibrate the camera to the arm

- Intrinsics first; a tag or ChArUco target publishing TF; no camera mount joint in the URDF while
  calibrating.
- easy_handeye2 (LGPL-3.0, rqt) with `apriltag_ros`, MoveIt Calibration (BSD, RViz, ChArUco), or
  `cv2.calibrateHandEye` directly. All build or run from source; none is in rosdistro.
- Sample many still poses with large rotations about every axis.

Check: the target's position computed through each sample agrees within your grasp tolerance;
the `tcp` driven to a seen tag corner lands on it. [references/hand-eye.md](references/hand-eye.md)

### 4. Get grasp poses

- Box-like objects on a table: top-down heuristic from the segmented points (centroid, narrow
  axis, top height).
- Known objects with a mesh: pose from [FoundationPose](../../wiki/learning/models/foundationpose.md)
  (non-commercial research code; Isaac ROS for NVIDIA GPUs) or a tag on a jig, plus a grasp library
  in the object frame.
- Clutter or unknown objects: [Contact-GraspNet](../../wiki/learning/models/contact-graspnet.md),
  **research-and-evaluation-only licence**, Python 3.7 and TensorFlow 2.2, so it runs in its own
  environment; shift its Panda-hand frame 0.1034 m along z to the contact centre.
- Filter by width, approach direction, and IK plus collisions (`/compute_ik`) for grasp and
  pre-grasp.

Check: candidates drawn in RViz over the point cloud have the fingers on both sides of the object.
[references/grasp-poses.md](references/grasp-poses.md)

### 5. Pick: approach, close, check, lift

- Open; plan to the pre-grasp (grasp moved back along tcp z); remove the target from the planning
  scene; Cartesian approach at low scaling; close; judge the grasp; attach the object to `tcp`
  with the gripper links as touch links; Cartesian lift; check for slip.
- MoveIt Task Constructor plans the same stages as one task; split it where you need a check.
- Place is the mirror: down slowly, open, detach, retreat along tcp z before planning.

Check: each stage's condition in the table of [references/pick-place.md](references/pick-place.md)
holds before the next starts; grasp checks in [references/grasp-checks.md](references/grasp-checks.md).

### 6. Sense force at the wrist

- `<sensor>` with `force.x` ... `torque.z` in the URDF; `force_torque_sensor_broadcaster` with
  `sensor_name`, `frame_id`, and a filter chain: `control_filters/GravityCompensationWrench`
  (tool mass and CoG) then `control_filters/LowPassFilterWrench`.
- Zero at the start of each session (sensor tare, or the broadcaster's `offset`, which is added).
- `wrench_transformer_node` republishes the wrench in `base_link` or `tcp`.

Check: at rest the compensated force stays near zero in several tool orientations; a known mass
reads its weight. [references/force-torque.md](references/force-torque.md)

### 7. Add compliance where contact is expected (optional)

- `admittance_controller` chained under the trajectory controller (`command_joints`), with
  `kinematics_interface_kdl` installed and `--activate-as-group` spawning.
- Start with all axes off, then z only, stiff, softened step by step.

Check: with axes off, motion is unchanged; with z on, a push along tcp z is yielded to and the arm
returns without oscillating. [references/admittance.md](references/admittance.md)

### 8. Set the safety limits

Layers, from the one that must never fail to the convenient ones:

1. Hardware: an emergency stop the operator can reach; the arm controller's own force, speed and
   zone limits (cobots have them); a gripper force setting the object survives.
2. ros2_control: real URDF joint limits with `enforce_command_limits: true` (default `false` on
   Jazzy); `constraints.<joint>.trajectory` tolerances on the arm controller (0 disables the check)
   so a blocked arm aborts its goal.
3. MoveIt: low velocity and acceleration scaling (`default_velocity_scaling_factor` in
   `joint_limits.yaml`, 0.1 if unset), table and fixtures as collision objects, slower approach.
4. Software monitor: the force guard (wrench change above a limit sends `stop` to MoveIt) and the
   grasp checks. Not real-time; it protects the work, not people.

Check: test each layer once on purpose (press the e-stop, block a slow move by hand, exceed a
force) and record that it stopped the arm.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| Gripper goal aborts whenever it closes on an object | `allow_stalling` is `false` (default): a stall aborts | `allow_stalling: true`; judge the grasp from position |
| Parallel gripper controller will not activate: "Expected 1 velocity state interface" | Hardware exports no gripper velocity | Export velocity (difference positions in the plugin) |
| Gripper "reaches" the goal half closed | `goal_tolerance` default 0.01 is large for a joint in metres | Set it to a few percent of travel |
| `max_effort` has no effect | Position-only controller, or no `max_effort_interface` | Effort interface in the plugin, or limit by close target |
| Deprecation warning names `parallel_gripper_controllers/GripperActionController` | The message has a typo | The type is `parallel_gripper_action_controller/GripperActionController` |
| Approach fails at the last centimetres | Fingers collide with the target in the planning scene | Remove or allow-collide the target before the final approach |
| TF warns of a frame with two parents after hand-eye | URDF mount joint and calibration both publish the camera frame | One source: calibration result into the URDF, or the URDF mount removed |
| Grasps land a few cm off, always the same way | Hand-eye result or tag size wrong; an optical-frame pose stamped as `camera_link` | Re-check tag size and frame ids; repeat the touch test |
| Contact-GraspNet grasps sit 10 cm short | Panda hand frame used as the contact point | Multiply by the 0.1034 m z shift |
| F/T reading swings as the wrist turns | Tool mass or CoG wrong in the gravity filter | Weigh the tool; fix CoG; repeat the tilt test |
| No `~/wrench_filtered` after adding gravity compensation | No TF between `world_frame` and `sensor_frame` | Fix TF; read the throttled "GravityCompensation update failed" log |
| Admittance controller fails to configure | `kinematics_interface_kdl` not installed, or a frame off the base-to-tip chain | Install it; make `tip` the deepest frame used |
| Arm drifts after a push with admittance on | Stiffness 0 on a selected axis gives zero damping | Keep some stiffness; raise the damping ratio |
| Hobby gripper servo hot or buzzing while holding | Position target far inside the object: constant stall | Target just under the width; torque limit in the servo |

## Checks

- `ros2 control list_controllers`: `gripper_controller`, `arm_controller`, broadcasters active;
  with compliance, `arm_controller` chained to `admittance_controller`.
- Open and close succeed from the CLI; a real close on a test object reports `stalled: true` and
  the position of its width.
- Hand-eye: sample spread and touch test within the grasp tolerance, recorded with the date.
- Ten picks of the target object in a row with the grasp checks logging success, and every failure
  ending with the gripper open and the arm retreated.
- F/T: near zero at rest in several orientations; a known mass reads its weight.
- Each safety layer tested once on purpose; the force guard stops a slow move pressed by hand.

## Distro differences

- **Humble:** no `parallel_gripper_controller` (ros2_controllers 2.54.1) and MoveIt 2.5 has no
  `ParallelGripperCommand` type: use `position_controllers/GripperActionController` and
  `type: GripperCommand`. The F/T broadcaster has no `sensor_filter_chain`. MoveIt headers end in
  `.h` and `computeCartesianPath` takes a `jump_threshold` argument.
- **Lyrical:** `gripper_controllers` is no longer released (ros2_controllers 6.10.1): only the
  parallel gripper controller. `enforce_command_limits` defaults to `true`; the trajectory
  controller's `constraints.goal_time` defaults to 10 s and 0 now disables the grace period.
  MoveIt 2.15.2, MTC 0.2.0. Isaac ROS (FoundationPose) 5.x targets Lyrical, 4.6 Jazzy.
- easy_handeye2 and MoveIt Calibration are source-only on every distro.

## Related

- Wiki: [ros2_control](../../wiki/software/ros2-control.md), [tf2](../../wiki/software/tf2.md),
  [AprilTag](../../wiki/software/apriltag.md), [Open3D](../../wiki/software/open3d.md),
  [MoveIt 2](../../wiki/software/moveit2.md), [Contact-GraspNet](../../wiki/learning/models/contact-graspnet.md),
  [GraspNet-1Billion](../../wiki/learning/datasets/graspnet-1billion.md),
  [FoundationPose](../../wiki/learning/models/foundationpose.md),
  [Segment Anything](../../wiki/learning/models/segment-anything.md),
  [PlotJuggler](../../wiki/tools/plotjuggler.md), [Robotiq 2F-85](../../wiki/robots/robotiq-2f-85.md).
- Skills: [manip-moveit2](../manip-moveit2/SKILL.md), [ros2-control](../ros2-control/SKILL.md),
  [ros2-robot-description](../ros2-robot-description/SKILL.md),
  [perception-camera](../perception-camera/SKILL.md), [perception-lidar](../perception-lidar/SKILL.md),
  [sim-gazebo](../sim-gazebo/SKILL.md), [sim-to-real](../sim-to-real/SKILL.md). Later: `control-`
  skills (force and impedance control). Also [arch-safety](../arch-safety/SKILL.md),
  [ops-bringup](../ops-bringup/SKILL.md), [learn-robot-learning](../learn-robot-learning/SKILL.md).
- Upstream: control.ros.org Jazzy (parallel gripper, gripper, F/T broadcaster and admittance
  controller user docs), moveit.picknik.ai (MTC pick and place), easy_handeye2 and
  moveit_calibration READMEs.
