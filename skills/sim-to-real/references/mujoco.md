# MuJoCo: actuator models, randomisation and a sim-to-sim runner

Part of [sim-to-real](../SKILL.md). Checked against the MuJoCo 4.0.1 docs and changelog
(November 2026). Getting a URDF into MJCF is in
[ros2-robot-description simulators](../../ros2-robot-description/references/simulators.md); running
and tuning MuJoCo itself is for the `sim-mujoco` skill.

## Model the actuator in MJCF

```xml
<mujoco model="my_robot">
  <option timestep="0.005"/>                 <!-- the physics dt the policy was trained with -->
  <default>
    <!-- identified values go here; these numbers are placeholders -->
    <joint armature="0.01" frictionloss="0.1" damping="0.1"/>
    <!-- drive PD with torque limit; nsample sizes the delay buffer: 4 x 5 ms = 20 ms max -->
    <position kp="20" kv="0.5" forcerange="-10 10" nsample="4" delay="0.01"/>
  </default>
  <worldbody>
    <!-- ... bodies; set simple="false" on any body whose centre of mass you randomise -->
  </worldbody>
  <actuator>
    <position name="left_knee" joint="left_knee"/>   <!-- one per joint, named after the joint -->
  </actuator>
  <sensor>
    <jointpos name="left_knee_pos" joint="left_knee"/>
    <jointvel name="left_knee_vel" joint="left_knee"/>
    <gyro name="imu_gyro" site="imu"/>
    <framequat name="imu_quat" objtype="site" objname="imu"/>
  </sensor>
</mujoco>
```

- `armature` is the reflected rotor inertia (rotor inertia times gear ratio squared),
  `frictionloss` the Coulomb friction, `damping` the viscous term.
- A `<position>` actuator is `kp * (target - q) - kv * dq`, clipped to `forcerange`. It has no
  torque-speed curve. For that, use `<dcmotor>` (since 3.7.0): resistance and motor constants (or a
  `nominal` voltage, stall torque and no-load speed), saturation, optional inductance, thermal
  model, cogging and LuGre friction, and an on-board PID. Read its technical note for the units
  before filling it in. A `<pid>` actuator exists since 3.12.0.
- Delays (since 3.5.0): with `nsample > 0` and `delay > 0` the actuator reads its control from a
  history buffer at `time - delay`. The smallest real delay is one timestep. Keep
  `delay <= nsample * timestep`; at run time you may change `model.actuator_delay` within that
  bound. Sensors take the same `nsample` and `delay` attributes, plus `interval` for sensors slower
  than the physics step.
- A sensor's `noise` attribute is only a stored number; MuJoCo does not add noise. Add it in the
  observation code (below).
- Contact friction between two geoms is the element-wise maximum of their `friction` values
  unless one geom has a higher `priority`. Set the floor and foot values with that rule in mind.

## Per-episode randomisation (CPU)

Always sample from saved nominal values. Writing `model.body_mass *= scale` every reset compounds
the changes into a random walk.

```python
"""Per-episode domain randomisation for one MuJoCo model."""
import mujoco
import numpy as np

FIELDS = ("geom_friction", "body_mass", "body_inertia", "body_ipos", "dof_damping",
          "dof_armature", "dof_frictionloss", "actuator_gainprm", "actuator_biasprm",
          "actuator_delay")


class Randomiser:
    def __init__(self, model, cfg, foot_geoms, base_body, seed=0):
        self.m, self.cfg = model, cfg
        self.rng = np.random.default_rng(seed)
        self.nominal = {f: getattr(model, f).copy() for f in FIELDS}
        self.feet = [model.geom(name).id for name in foot_geoms]
        self.base = model.body(base_body).id

    def apply(self, data):
        m, c, r = self.m, self.cfg, self.rng
        for f, value in self.nominal.items():
            getattr(m, f)[:] = value
        m.geom_friction[self.feet, 0] = r.uniform(*c["foot_friction"], len(self.feet))
        scale = r.uniform(*c["mass_scale"], m.nbody)
        m.body_mass[:] *= scale
        m.body_inertia[:] *= scale[:, None]  # keep density uniform
        m.body_mass[self.base] += r.uniform(*c["added_base_mass"])
        m.body_ipos[self.base] += r.uniform(*c["base_com_offset"], 3)
        m.dof_armature[:] *= r.uniform(*c["armature_scale"], m.nv)
        m.dof_frictionloss[:] *= r.uniform(*c["friction_scale"], m.nv)
        kp = r.uniform(*c["kp_scale"], m.nu)
        m.actuator_gainprm[:, 0] *= kp  # position actuator: gain kp,
        m.actuator_biasprm[:, 1] *= kp  # bias -kp ...
        m.actuator_biasprm[:, 2] *= r.uniform(*c["kv_scale"], m.nu)  # ... and -kv
        m.actuator_delay[:] = r.uniform(*c["actuator_delay"], m.nu)  # must stay <= nsample * dt
        mujoco.mj_setConst(m, data)  # recompute constants derived from mass and frames
        mujoco.mj_resetData(m, data)
        # one IMU bias per episode, plus white noise every step (see observe)
        self.gyro_bias = r.uniform(*c["gyro_bias"], 3)


def observe_gyro(data, rnd, noise_std):
    gyro = data.sensor("imu_gyro").data.copy()
    return gyro + rnd.gyro_bias + rnd.rng.normal(0.0, noise_std, 3)
```

- `cfg` holds `(low, high)` tuples; take them from [ranges.md](ranges.md), centred on your
  identified values.
- Floor friction: randomise the floor geom instead of (or as well as) the feet, keeping the
  maximum rule in mind.
- Changing `body_ipos` (or joint offsets) at run time needs `simple="false"` on that body in the
  MJCF; a change that breaks the "simple body" conditions otherwise triggers a validation error
  (the `simple` attribute exists since 3.11.0).
- Pushes: write a force into `data.xfrc_applied[base_id, :3]` (world frame, at the body's centre
  of mass) for a few steps, then zero it.

**Batched training.** For GPU training on MJX or MuJoCo Warp, randomise per environment by mapping
a sampling function over the model fields: MuJoCo Playground's Go1 task does this with
`jax.vmap` and `model.tree_replace` (`rss2025/mujoco_playground/_src/locomotion/go1/randomize.py`).
MuJoCo 4.0's C batch API gives per-simulation fields through `mjb_expand`, with `mjb_setConst` for
the derived constants.

## Sim-to-sim runner: a policy trained elsewhere, run in MuJoCo

Run the exported policy through the same observation and action code the robot will use. Joint
order, default pose, gains and rates come from the deploy spec
([deployment.md](deployment.md#the-deploy-spec)).

```python
import mujoco
import numpy as np
import onnxruntime as ort
import yaml

spec = yaml.safe_load(open("deploy_spec.yaml"))
m = mujoco.MjModel.from_xml_path("my_robot_scene.xml")
d = mujoco.MjData(m)
m.opt.timestep = spec["physics_dt"]
decimation = round(1.0 / (spec["control_rate_hz"] * spec["physics_dt"]))
names = spec["joint_names"]
qadr = [m.joint(n).qposadr[0] for n in names]
vadr = [m.joint(n).dofadr[0] for n in names]
act = [m.actuator(n).id for n in names]
default = np.array(spec["default_joint_pos"])
session = ort.InferenceSession(spec["policy"], providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name


def projected_gravity(quat_wxyz):
    inverse = np.zeros(4)
    mujoco.mju_negQuat(inverse, quat_wxyz)
    g = np.zeros(3)
    mujoco.mju_rotVecQuat(g, np.array([0.0, 0.0, -1.0]), inverse)
    return g


last_action = np.zeros(len(names))
mujoco.mj_resetData(m, d)
d.qpos[qadr] = default
for _ in range(int(20.0 * spec["control_rate_hz"])):  # 20 s
    terms = {
        "projected_gravity": projected_gravity(d.sensor("imu_quat").data),
        "base_ang_vel": d.sensor("imu_gyro").data,
        "joint_pos_rel": d.qpos[qadr] - default,
        "joint_vel_rel": d.qvel[vadr],
        "last_action": last_action,
    }
    obs = np.concatenate([terms[t] * spec["obs_scale"].get(t, 1.0) for t in spec["observation"]])
    last_action = session.run(None, {input_name: obs[None].astype(np.float32)})[0][0]
    d.ctrl[act] = default + spec["action_scale"] * last_action
    for _ in range(decimation):
        mujoco.mj_step(m, d)
```

- MuJoCo quaternions are `w, x, y, z`; ROS messages and Isaac Lab 3.0 use `x, y, z, w`.
- Isaac Lab's implicit PD runs inside the physics solver; MuJoCo's `<position>` with `kv` is close
  but not identical. Use the training stiffness and damping, the training `armature`, and the
  training effort limit as `forcerange`.
- Contact solver differences are the point of the test: a policy that only works with one solver's
  contacts will not survive the real floor.

## Sources

- MuJoCo docs (4.0.1): XML reference (`position`, `dcmotor`, joint `armature`, `frictionloss`,
  `damping`, sensor `noise`, `nsample`, `delay`, `interval`, `body/simple`), modeling guide
  ("Delays", contact parameters), API reference (`mj_setConst`, `mju_negQuat`, `mju_rotVecQuat`),
  programming guide (batch API), Python named access; changelog 3.5.0, 3.7.0, 3.11.0, 3.12.0.
- MuJoCo Playground, `rss2025/.../go1/randomize.py`, commit 3ff05b5.
- Isaac Lab 3.0 migration guide (quaternion order changed from WXYZ to XYZW).
