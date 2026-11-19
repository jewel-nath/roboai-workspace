# System identification

Part of [sim-to-real](../SKILL.md): fit the simulator's parameters to logs from the robot, so that
randomisation only has to cover what is still uncertain. What to measure first is in
[reality-gap.md](reality-gap.md).

## Order of work

1. **One actuator on a bench**, or one limb lifted clear of the ground: delay, drive PD gains,
   friction, armature, torque saturation.
2. **The whole robot in the air** (on a stand or hanging): link masses and inertias, if CAD and the
   scale are not good enough.
3. **Contact:** friction tests on each floor ([reality-gap.md](reality-gap.md#4-contact-and-friction)).

Fit each stage with the earlier stages' results frozen. Hwangbo et al. (Science Robotics 2019)
follow the same split: identify the rigid-body parameters with their uncertainty, then learn the
actuator, then train the policy.

## What to log

- Commanded target (what the drive was asked to do), measured position and velocity, motor current
  or torque if available, supply voltage, and timestamps from one clock.
- The highest rate the bus allows. Log on the robot, not over Wi-Fi.
- Each test as its own bag, named after the test and date, with a note of the load and setup.

## Excitation

- Use chirps (swept sines) and multi-sines inside safe limits, at several amplitudes, both
  directions, unloaded and loaded. Add slow constant-velocity sweeps for friction.
- Cover at least the frequency band the controller will use. Hwangbo et al. found that an actuator
  model trained on narrow-band data made the simulated robot oscillate; they varied the amplitude and
  frequency of sine foot trajectories and pushed the robot by hand while logging.
- For inertial parameters on an arm, optimised excitation trajectories (Swevers et al., IEEE
  Transactions on Robotics and Automation, 1997) make the regressor well conditioned.
- Keep one test out of the fit for validation.

## Method 1: replay fit in the simulator (grey box)

Replay the logged commands in the simulator from the logged initial state and adjust parameters
until the simulated trajectory matches the measured one (nonlinear least squares). It works for any
parameter the simulator exposes, including delays.

**MuJoCo** ships this as `mujoco.sysid` (since 3.5.0; `pip install "mujoco[sysid]"`): box-
constrained least squares over batched rollouts, helpers for mass, centre of mass, physically
consistent inertia and PD gains, and an HTML report. A bench model of one knee joint with a
`<position name="knee">` actuator (with `nsample` set for the largest delay you will try) and
`jointpos`/`jointvel` sensors named `knee_pos` and `knee_vel`:

```python
import mujoco
import numpy as np
from mujoco import sysid

spec = mujoco.MjSpec.from_file("knee_bench.xml")
model = spec.compile()


def set_damping(s, p):
    s.joint("knee").damping[0] = p.value[0]  # damping holds [linear, quadratic, cubic] terms


params = sysid.ParameterDict()
params.add(sysid.Parameter("armature", nominal=0.01, min_value=0.0, max_value=0.2,
                           modifier=lambda s, p: setattr(s.joint("knee"), "armature", p.value[0])))
params.add(sysid.Parameter("frictionloss", nominal=0.1, min_value=0.0, max_value=2.0,
                           modifier=lambda s, p: setattr(s.joint("knee"), "frictionloss", p.value[0])))
params.add(sysid.Parameter("damping", nominal=0.1, min_value=0.0, max_value=5.0,
                           modifier=set_damping))
params.add(sysid.Parameter("pd", nominal=np.array([20.0, 0.5]), min_value=np.array([1.0, 0.0]),
                           max_value=np.array([100.0, 5.0]),
                           modifier=lambda s, p: sysid.apply_pdgain(s, "knee", p.value)))
params.add(sysid.Parameter("delay", nominal=0.01, min_value=0.0, max_value=0.04,
                           modifier=lambda s, p: setattr(s.actuator("knee"), "delay", p.value[0])))

log = np.load("knee_chirp_01.npz")  # exported from the bag: time, target, position, velocity
t = log["time"] - log["time"][0]
control = sysid.TimeSeries.from_control_names(t, log["target"][:, None], model)
measured = sysid.TimeSeries.from_names(t, np.c_[log["position"], log["velocity"]], model,
                                       names=["knee_pos", "knee_vel"])
x0 = sysid.create_initial_state(model, log["position"][:1], log["velocity"][:1])
seq = sysid.ModelSequences("knee", spec, "chirp_01", x0, control, measured)

residual_fn = sysid.build_residual_fn(models_sequences=[seq])
fitted, result = sysid.optimize(initial_params=params, residual_fn=residual_fn)
sysid.save_results("sysid_knee/", [seq], params, fitted, result, residual_fn)
```

- The parameter values and bounds above are placeholders; set the nominal values from datasheets
  and the bounds wide enough to contain the truth.
- The `delay` bound must stay below `nsample * timestep` of that actuator, or MuJoCo reads before
  the buffer starts (see "Delays" in the MuJoCo modeling guide).
- Fit position and velocity together; position alone leaves damping and armature poorly
  separated.

**Other simulators:** wrap one rollout as `simulate(params, commands, x0) -> trajectory` and hand
the residual to `scipy.optimize.least_squares` with bounds. With Isaac Lab, run the rollouts in
parallel environments, one parameter set per environment.

## Method 2: inertial parameters from the dynamics regressor

Rigid-body joint torques are linear in the inertial parameters: `tau = Y(q, dq, ddq) @ pi`.
Pinocchio builds `Y`:

```python
import numpy as np
import pinocchio as pin

model = pin.buildModelFromUrdf("my_robot.urdf")
data = model.createData()
rows = [pin.computeJointTorqueRegressor(model, data, q, v, a) for q, v, a in samples]
Y = np.vstack(rows)          # stacked regressors
tau = np.concatenate(taus)   # measured joint torques (or current x torque constant x gear ratio)
pi, *_ = np.linalg.lstsq(Y, tau, rcond=None)
```

- Each link's 10 parameters follow `pin.Inertia.toDynamicParameters()`;
  `pin.Inertia.FromDynamicParameters()` converts back.
- Accelerations come from differentiating encoder positions: filter with a zero-phase filter
  (`scipy.signal.filtfilt`) first, and apply the same filter to the torques.
- Add Coulomb and viscous friction columns per joint, or the friction ends up in the inertias.
- Only some combinations of parameters are identifiable (the base parameters). Plain least squares
  can return physically impossible inertias; constrain them with linear matrix inequalities
  (Wensing, Kim and Slotine, IEEE RA-L 2018, arXiv:1701.04395) or the pseudo-inertia
  parameterisation (Rucker and Wensing, IEEE RA-L 2022), which `mujoco.sysid` uses for
  `InertiaType.Pseudo`.

## Method 3: actuator network

When the drive is too complex to model, learn the map from commands to torque. Hwangbo et al. 2019:

- Inputs: the joint position error (target minus measured) and joint velocity at the current step
  and two past steps (t - 0.01 s and t - 0.02 s); output: joint torque.
- An MLP with three hidden layers of 32 units and softsign activations, one model shared by
  identical actuators.
- Data from sine trajectories of varied amplitude and frequency with manual pushes, logged at
  400 Hz with measured torque; a few minutes were enough because all 12 actuators logged at once.
- The history must be longer than the sum of all communication delays and the mechanical response
  time.

Isaac Lab runs such networks as explicit actuators: `ActuatorNetMLPCfg` (TorchScript file,
`pos_scale`, `vel_scale`, `torque_scale`, `input_order`, `input_idx` counted in physics steps) and
`ActuatorNetLSTMCfg`. Without a torque sensor, label the data with motor current times torque
constant times gear ratio, and check it against a static load test before trusting it.

## Method 4: friction models for hobby servos

BAM ("Better Actuator Models", Duclusaud et al., ICRA 2025, github.com/Rhoban/bam, Apache-2.0)
identifies extended friction models (Stribeck, load-dependent, quadratic terms) from pendulum
recordings and ships fitted models for common Dynamixel, Feetech and eRob actuators, with an API for
MuJoCo and MuJoCo Warp.

## Validate the fit

- Replay the held-out test with the fitted parameters; plot measured against simulated position,
  velocity and torque. The fit is done when the held-out error is close to the fit error.
- Check that fitted values are physical (positive friction and armature, plausible gains, delay near
  the measured latency). A parameter that runs to its bound means the model is missing something.
- Use the parameter uncertainty (`mujoco.sysid` reports confidence intervals) to set the width of
  the randomisation around each value.

## Sources

- MuJoCo 4.0.1 docs: Python `sysid` section, modeling guide "System identification" and "Delays";
  `python/mujoco/sysid/README.md` and source (commit ab8b9f8, 2026-11-18).
- Hwangbo et al., "Learning agile and dynamic motor skills for legged robots", Science Robotics
  4(26), 2019 (arXiv:1901.08652).
- Pinocchio `computeJointTorqueRegressor` and `Inertia.toDynamicParameters` (stack-of-tasks/pinocchio).
- Duclusaud, Passault, Padois and Ly, "Extended Friction Models for the Physics Simulation of
  Servo Actuators", ICRA 2025 (arXiv:2410.08650).
- Isaac Lab 3.0 `isaaclab/actuators/actuator_net_cfg.py`.
