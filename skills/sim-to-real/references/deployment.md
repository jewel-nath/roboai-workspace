# Deployment: deploy spec, policy runner, safety layers and logging

Part of [sim-to-real](../SKILL.md). Written for ROS 2 Jazzy with `rclpy` and ONNX Runtime; the
stage gates themselves are in the skill's workflow.

## The deploy spec

One file, written when the policy is exported, read by every runner: the sim-to-sim runner
([mujoco.md](mujoco.md#sim-to-sim-runner-a-policy-trained-elsewhere-run-in-mujoco)) and the robot
node below. Anything the policy depends on goes here, so nobody re-types it.

```yaml
# deploy_spec.yaml - example values for a four-joint robot; every number is a placeholder
policy: policy.onnx
physics_dt: 0.005                 # training physics step, s
control_rate_hz: 50               # 1 / (physics_dt * decimation)
joint_names: [left_hip, left_knee, right_hip, right_knee]   # training order, from the sim
default_joint_pos: [0.0, 0.6, 0.0, 0.6]                     # rad, same order
action_scale: 0.5                 # target = default + action_scale * action
action_clip: 1.0                  # the clip used in training
observation: [projected_gravity, base_ang_vel, joint_pos_rel, joint_vel_rel, last_action]
obs_scale: {joint_vel_rel: 0.05}  # per-term scales used in training; missing means 1.0
pd_gains: {kp: [20, 20, 20, 20], kd: [0.5, 0.5, 0.5, 0.5]}  # the drives must match these
effort_limit: [10, 10, 10, 10]    # N·m, as trained
soft_limits: {lower: [-0.5, -0.1, -0.5, -0.1], upper: [0.5, 1.4, 0.5, 1.4]}  # inside the stops
command_topic: joint_group_position_controller/commands
state_timeout_s: 0.05             # stop if joint states are older than this
max_tilt_rad: 0.8                 # stop beyond this tilt
ramp_s: 3.0                       # soft start duration
```

Generate `joint_names` and `default_joint_pos` from the training environment (in Isaac Lab,
`robot.joint_names` and the articulation's default joint positions), not by hand. Isaac Lab 3.0's
LEAPP export writes an equivalent YAML ([isaac-lab.md](isaac-lab.md#export)).

## Policy runner node

Commands a `position_controllers/JointGroupPositionController` (ros2_controllers), whose
`~/commands` topic takes `std_msgs/msg/Float64MultiArray` in the controller's joint order; list the
controller's joints in the deploy-spec order. Controller setup is in
[ros2-control](../../ros2-control/SKILL.md).

```python
"""Run an exported policy at a fixed rate with soft start, watchdog, tilt stop and limits."""
import numpy as np
import onnxruntime as ort
import rclpy
import yaml
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Imu, JointState
from std_msgs.msg import Float32MultiArray, Float64MultiArray


def projected_gravity(x, y, z, w):
    """World -z axis in the body frame, from a unit quaternion in ROS x, y, z, w order."""
    return -np.array([2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)])


class PolicyRunner(Node):
    def __init__(self):
        super().__init__("policy_runner")
        with open(self.declare_parameter("deploy_spec", "deploy_spec.yaml").value) as f:
            self.spec = s = yaml.safe_load(f)
        self.names = s["joint_names"]
        self.default = np.array(s["default_joint_pos"])
        self.lower = np.array(s["soft_limits"]["lower"])
        self.upper = np.array(s["soft_limits"]["upper"])
        self.session = ort.InferenceSession(s["policy"], providers=["CPUExecutionProvider"])
        self.input_name = self.session.get_inputs()[0].name
        self.q = self.dq = self.gyro = self.gravity = self.stamp = self.start_pose = None
        self.action = np.zeros(len(self.names))
        self.ramp, self.stopped = 0.0, False
        self.create_subscription(JointState, "joint_states", self.on_joints, qos_profile_sensor_data)
        self.create_subscription(Imu, "imu/data", self.on_imu, qos_profile_sensor_data)
        self.cmd_pub = self.create_publisher(Float64MultiArray, s["command_topic"], 10)
        self.obs_pub = self.create_publisher(Float32MultiArray, "policy/observation", 10)
        self.act_pub = self.create_publisher(Float32MultiArray, "policy/action", 10)
        self.timer = self.create_timer(1.0 / s["control_rate_hz"], self.step)

    def on_joints(self, msg):
        index = {name: i for i, name in enumerate(msg.name)}
        missing = [n for n in self.names if n not in index]
        if missing:
            return self.stop(f"joints missing from joint_states: {missing}")
        order = [index[n] for n in self.names]  # map by name, never by position
        self.q = np.array(msg.position)[order]
        self.dq = np.array(msg.velocity)[order]
        self.stamp = self.get_clock().now()

    def on_imu(self, msg):
        o, w = msg.orientation, msg.angular_velocity
        self.gravity = projected_gravity(o.x, o.y, o.z, o.w)
        self.gyro = np.array([w.x, w.y, w.z])

    def observation(self):
        terms = {
            "projected_gravity": self.gravity,
            "base_ang_vel": self.gyro,
            "joint_pos_rel": self.q - self.default,
            "joint_vel_rel": self.dq,
            "last_action": self.action,
        }
        scale = self.spec["obs_scale"]
        obs = [terms[t] * scale.get(t, 1.0) for t in self.spec["observation"]]
        return np.concatenate(obs).astype(np.float32)

    def step(self):
        s = self.spec
        if self.stopped or self.q is None or self.gravity is None:
            return
        age = (self.get_clock().now() - self.stamp).nanoseconds * 1e-9
        if age > s["state_timeout_s"]:
            return self.stop(f"joint states are {age:.3f} s old")
        if self.gravity[2] > -np.cos(s["max_tilt_rad"]):
            return self.stop("tilt limit exceeded")
        if self.ramp < 1.0:  # soft start: reach the default pose before the policy acts
            if self.start_pose is None:
                self.start_pose = self.q.copy()
            self.ramp = min(1.0, self.ramp + 1.0 / (s["ramp_s"] * s["control_rate_hz"]))
            target = (1.0 - self.ramp) * self.start_pose + self.ramp * self.default
        else:
            obs = self.observation()
            raw = self.session.run(None, {self.input_name: obs[None]})[0][0]
            self.action = np.clip(raw, -s["action_clip"], s["action_clip"])
            target = self.default + s["action_scale"] * self.action
            self.obs_pub.publish(Float32MultiArray(data=obs.tolist()))
            self.act_pub.publish(Float32MultiArray(data=self.action.astype(np.float32).tolist()))
        self.cmd_pub.publish(Float64MultiArray(data=np.clip(target, self.lower, self.upper).tolist()))

    def stop(self, reason):
        if self.stopped:
            return
        self.stopped = True
        self.timer.cancel()
        self.get_logger().error(f"stopping: {reason}")
        # hold the last measured pose; replace with the driver's damping or torque-off mode
        if self.q is not None:
            self.cmd_pub.publish(Float64MultiArray(data=self.q.tolist()))


def main():
    rclpy.init()
    rclpy.spin(PolicyRunner())


if __name__ == "__main__":
    main()
```

- The observation and action code must be the same functions the sim-to-sim runner uses; put them
  in one module and import it in both.
- `sensor_msgs/Imu` orientation must be relative to a gravity-aligned frame, and the IMU frame
  aligned with the base (or rotate it first). Check the sign with the tilt test in
  [reality-gap.md](reality-gap.md#6-the-robot-description-is-wrong).
- An `rclpy` timer jitters under load. Log `policy/action` and check the period histogram; if it is
  far wider than in sim, move the policy into C++ or into a ros2_control controller.
- The stop path is a convenience. The real stop is the hardware e-stop.

## Safety layers

From the outside in; each layer must work when the ones inside it fail.

1. **Hardware e-stop** that removes motor power without software in the loop, within reach of the
   person watching. Test it at the start of every session. ISO 13850 covers the design of
   emergency stop functions.
2. **Drive limits** in the motor drivers: current or torque, velocity, position, and a command
   timeout that stops or damps the motor when commands stop arriving.
3. **ros2_control limits**: joint limits enforced on commands (`enforce_command_limits`, see
   [ros2-control](../../ros2-control/SKILL.md)).
4. **Policy node**: soft joint limits inside the physical stops, stale-state watchdog, tilt stop,
   soft start, action clip.
5. **Setup**: a stand, gantry or harness for the early stages, a clear area, and one person whose
   only job is the e-stop.

## Logging

Record everything the policy saw and did, with the commands and the raw sensors, at every stage
(sim-to-sim runs too, if they publish ROS topics):

```bash
ros2 bag record -s mcap -o stand_$(date +%Y%m%d_%H%M%S) \
  --topics /joint_states /imu/data /policy/observation /policy/action \
    /joint_group_position_controller/commands /diagnostics /tf /tf_static \
  --custom-data stage=stand policy=policy.onnx
```

- MCAP is the default storage on Jazzy; `-s mcap` makes it explicit. Topics go after `--topics`:
  positional topics are deprecated in Jazzy and removed in Lyrical.
- Add drive currents, temperatures and battery voltage if the driver publishes them.
- A black box for long sessions: `--snapshot-mode` with `--max-cache-size <bytes>` keeps a ring
  buffer in memory; `ros2 service call /rosbag2_recorder/snapshot rosbag2_interfaces/srv/Snapshot`
  writes it to disk after something goes wrong.

## Review

Open the bag in [Foxglove](../../../wiki/tools/foxglove.md) or
[PlotJuggler](../../../wiki/tools/plotjuggler.md), next to the same plots from simulation:

- Commanded target against measured position, per joint: the lag and overshoot should look like
  the sim's. More lag means more latency or a weaker drive PD than modelled.
- Period between `policy/action` messages: mean at the trained rate, narrow spread.
- Actions near the clip, and torque or current near the limit: the policy is asking for more than
  the robot has.
- Projected gravity and gyro: noise level and bias as measured, signs right.
- Replay the logged commands in the simulator from the logged start state
  ([system-identification.md](system-identification.md#method-1-replay-fit-in-the-simulator-grey-box));
  where the replay and the robot part ways is where the model is wrong.

## Sources

- ros2_controllers (`jazzy`): `position_controllers/JointGroupPositionController`, `~/commands`
  as `std_msgs/msg/Float64MultiArray`.
- rosbag2 (`jazzy` and `lyrical`): `ros2bag/verb/record.py` options; README on the default MCAP
  storage and snapshot mode.
- unitree_rl_gym `deploy/deploy_real` (commit 276801e): zero-torque start, move to the default pose,
  hold, run the policy, damping mode on exit, with the robot hoisted at first.
