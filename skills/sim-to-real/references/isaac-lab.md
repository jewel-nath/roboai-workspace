# Isaac Lab: randomisation, noise, delay, actuators and export

Part of [sim-to-real](../SKILL.md). Isaac Lab has no wiki page yet; it runs on
[Isaac Sim](../../../wiki/tools/isaac-sim.md). Checked against the
`isaac-sim/IsaacLab` source at tag v3.0.0 (2026-10-19) and `main` (892354c, 2026-11-18), manager-
based workflow. Isaac Lab 2.x differences are at the end.

## Timing

```python
self.sim.dt = 0.005      # physics step, s
self.decimation = 4      # physics steps per policy step -> policy at 50 Hz
```

These are the values of the built-in quadruped velocity task. The robot must run the policy at
`1 / (sim.dt * decimation)`. Explicit actuator models (below) run every physics step.

## Events: domain randomisation

Event terms run in one of four modes: `prestartup` (before the simulation starts), `startup`
(once), `reset` (each episode reset), `interval` (every `interval_range_s` seconds of sim time).

```python
import isaaclab.envs.mdp as mdp
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.utils import configclass


@configclass
class EventsCfg:
    # ranges are starting points (references/ranges.md); centre them on identified values
    foot_friction = EventTerm(
        func=mdp.randomize_rigid_body_material,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg("robot", body_names=".*_foot"),
            "static_friction_range": (0.5, 1.25),
            "dynamic_friction_range": (0.5, 1.25),
            "restitution_range": (0.0, 0.0),
            "num_buckets": 64,
            "make_consistent": True,  # dynamic <= static
        },
    )
    link_mass = EventTerm(
        func=mdp.randomize_rigid_body_mass,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg("robot", body_names=".*"),
            "mass_distribution_params": (0.9, 1.1),
            "operation": "scale",  # recompute_inertia defaults to True
        },
    )
    base_com = EventTerm(
        func=mdp.randomize_rigid_body_com,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg("robot", body_names="base"),
            "com_range": {"x": (-0.02, 0.02), "y": (-0.02, 0.02), "z": (-0.01, 0.01)},
        },
    )
    pd_gains = EventTerm(
        func=mdp.randomize_actuator_gains,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg("robot", joint_names=".*"),
            "stiffness_distribution_params": (0.9, 1.1),
            "damping_distribution_params": (0.9, 1.1),
            "operation": "scale",
        },
    )
    joint_friction = EventTerm(
        func=mdp.randomize_joint_parameters,
        mode="startup",
        params={
            "asset_cfg": SceneEntityCfg("robot", joint_names=".*"),
            "friction_distribution_params": (0.8, 1.2),
            "armature_distribution_params": (0.9, 1.1),
            "operation": "scale",
        },
    )
    push = EventTerm(
        func=mdp.push_by_setting_velocity,
        mode="interval",
        interval_range_s=(10.0, 15.0),
        params={"velocity_range": {"x": (-0.5, 0.5), "y": (-0.5, 0.5)}},
    )
```

- Material, mass, joint-parameter and implicit-actuator-gain terms write through CPU tensors; their
  docstrings recommend `startup` only. With thousands of environments, one sample per environment
  at startup already gives the spread.
- On PhysX, materials are sampled once into `num_buckets` buckets (PhysX allows 64,000 unique
  materials) and then assigned. On the Newton backend there is one friction coefficient per shape,
  so `dynamic_friction_range` and `num_buckets` are ignored.
- `operation`: `"scale"` multiplies the default, `"add"` offsets it, `"abs"` sets it.
  `distribution`: `"uniform"`, `"log_uniform"` or `"gaussian"`. Scaling a joint friction or
  armature whose default is zero leaves it at zero; use `"abs"` or set a nominal value first.
- Other terms: `randomize_rigid_body_inertia`, `randomize_physics_scene_gravity`,
  `apply_external_force_torque` (`force_range`, `torque_range`), `reset_root_state_uniform`,
  `reset_joints_by_scale`. A curriculum on ranges (as in automatic domain randomisation, OpenAI et
  al. 2019, arXiv:1910.07113) goes in a `CurriculumTermCfg`.

## Observations: noise, bias, delay, history

```python
from isaaclab.managers import ObservationGroupCfg as ObsGroup
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.utils.noise import GaussianNoiseCfg, NoiseModelWithAdditiveBiasCfg
from isaaclab.utils.noise import UniformNoiseCfg as Unoise


@configclass
class PolicyCfg(ObsGroup):
    # order here is the order of the observation vector on the robot
    projected_gravity = ObsTerm(func=mdp.projected_gravity, noise=Unoise(n_min=-0.05, n_max=0.05))
    base_ang_vel = ObsTerm(
        func=mdp.base_ang_vel,
        noise=NoiseModelWithAdditiveBiasCfg(
            noise_cfg=GaussianNoiseCfg(std=0.05),                    # white noise every step
            bias_noise_cfg=Unoise(n_min=-0.02, n_max=0.02),          # bias drawn at each reset
        ),
        delay_min_lag=0,
        delay_max_lag=1,  # in policy steps
    )
    joint_pos = ObsTerm(func=mdp.joint_pos_rel, noise=Unoise(n_min=-0.01, n_max=0.01),
                        history_length=3)
    joint_vel = ObsTerm(func=mdp.joint_vel_rel, noise=Unoise(n_min=-1.5, n_max=1.5),
                        history_length=3)
    actions = ObsTerm(func=mdp.last_action)

    def __post_init__(self):
        self.enable_corruption = True  # without this, no noise is added
        self.concatenate_terms = True
```

- Noise is added, then clipped, then scaled; delay is applied after that and before history.
- History is oldest first by default (`history_newest_first=False`) and flattened per term.
- For an asymmetric actor-critic (Pinto et al. 2018, arXiv:1710.06542), add a second group, for
  example `critic`, without noise and with privileged terms, and map it in the RSL-RL runner config:
  `obs_groups = {"actor": ["policy"], "critic": ["critic"]}`. Only the actor group must exist on
  the robot.

## Actuators

Implicit actuators (`ImplicitActuatorCfg`) put the PD inside the physics solver. Explicit ones
compute torque in Python every physics step and can model the drive:

```python
from isaaclab.actuators import DelayedPDActuatorCfg

actuators = {
    "legs": DelayedPDActuatorCfg(
        joint_names_expr=[".*_hip", ".*_knee"],
        stiffness=20.0, damping=0.5,     # identified drive gains (placeholders)
        armature=0.01, friction=0.05,    # identified values (placeholders)
        actuator_effort_limit=10.0,      # actuator-model clip, N·m
        actuator_velocity_limit=8.0,     # rad/s
        min_delay=0, max_delay=4,        # physics steps, resampled at each reset
    ),
}
```

- `DCMotorCfg` adds the torque-speed curve (`saturation_effort` is the stall torque at the joint;
  `actuator_velocity_limit` the no-load speed). There is no delayed DC motor class in 3.0; pick the
  effect that matters more, or write a custom actuator.
- `ActuatorNetMLPCfg` and `ActuatorNetLSTMCfg` load a TorchScript actuator network
  ([system-identification.md](system-identification.md#method-3-actuator-network)).
- `RemotizedPDActuatorCfg` takes angle-dependent torque limits for linkage-driven joints.
- `joint_effort_limit` and `joint_velocity_limit` are solver limits; the `actuator_*` limits are
  what the model clips to. Set both from the datasheet.
- `main` after v3.0.0 adds `BamActuatorCfg` (BAM servo friction models, Newton MJWarp backend
  only); it is not in the v3.0.0 release.

## Actions

```python
joint_pos = mdp.JointPositionActionCfg(
    asset_name="robot", joint_names=[".*"], scale=0.5, use_default_offset=True,
    preserve_order=True,  # keep the order of joint_names instead of the articulation order
)
```

The robot computes the same thing: `target = default_joint_pos + scale * action`. For a smoothed
action, `EMAJointPositionToLimitsActionCfg` maps actions onto the joint limits and applies an
exponential moving average (`alpha`); the robot must run the same mapping and filter.

## Joint order and quaternions

- Joint order is the backend's articulation order: both PhysX backends list links breadth-first,
  and Newton can differ. `ArticulationCfg.joint_ordering` (3.0) can fix a public order. Either
  way, read `robot.joint_names` from the trained environment and write it into the deploy spec;
  never assume the URDF or driver order.
- Isaac Lab 3.0 quaternions are `x, y, z, w` (2.x used `w, x, y, z`).

## Export

Isaac Lab 3.0 exports a policy with its observation and action processing through LEAPP: a YAML
pipeline description, ONNX models and initial values. Run the export in simulation with
`LeappDeploymentEnv` first, then on the robot with Isaac ROS Deploy or your own runtime that reads
the YAML (Isaac Lab docs, "Policy Deployment" section). If you export only the network, write the
deploy spec by hand ([deployment.md](deployment.md#the-deploy-spec)).

## Isaac Lab 2.x differences

- Tasks live under `isaaclab_tasks/manager_based/...`; the quadruped velocity task was
  `manager_based/locomotion/velocity`, now `core/velocity`.
- Actuator limits were `effort_limit`, `velocity_limit`, `effort_limit_sim`,
  `velocity_limit_sim`. 3.0 keeps them as deprecated aliases; `main` has removed them.
- No observation delay fields (`delay_min_lag`, `delay_max_lag`, `delay_hold_prob`) before 3.0.
- `modifiers` on an observation term is renamed `tensor_processors` on `main`.
- Quaternions were `w, x, y, z`.

## Sources

- IsaacLab `source/isaaclab/isaaclab/envs/mdp/events.py`, `managers/manager_term_cfg.py`,
  `managers/event_manager.py`, `utils/noise/noise_cfg.py`, `actuators/*.py`,
  `envs/mdp/actions/actions_cfg.py`; `isaaclab_tasks/core/velocity/velocity_env_cfg.py`;
  `isaaclab_rl/rsl_rl/rl_cfg.py`.
- Isaac Lab docs: `isaaclab/migrating.rst`, `how-to/transfer_policies_between_physx_and_newton.rst`,
  `policy_deployment/05_leapp/`, release notes (v3.0.0-beta notes for the multi-backend change).
- Tag v2.3.2 for the 2.x names.
