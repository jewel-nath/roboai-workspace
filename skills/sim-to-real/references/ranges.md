# Randomisation ranges: published starting points

Part of [sim-to-real](../SKILL.md). These are the ranges that published, transferred setups used,
for their robots. **They are starting points, not answers.** Centre every range on your identified
value ([system-identification.md](system-identification.md)), make it about as wide as your
measurement uncertainty, and widen only what you could not measure. A range much wider than the
real spread makes the policy conservative; Tan et al. chose theirs from measurements plus small
safety margins for that reason.

How to set them: [mujoco.md](mujoco.md), [isaac-lab.md](isaac-lab.md), [gazebo.md](gazebo.md).

## Dynamics

| Parameter | Range used | Robot | Source |
|---|---|---|---|
| Link mass | 80 to 120 % | Minitaur | [T] |
| Link mass | x 0.9 to 1.1, all links | Go1 | [P] |
| Base mass | x 1/1.25 to 1.25, log-uniform | quadruped velocity task | [L] |
| Added base mass | -1 to +1 kg (off by default) | ANYmal and others | [G] |
| Added torso mass | -1 to +1 kg | Go1 | [P] |
| Base centre of mass | +-0.05 m in x and y, +-0.01 m in z | quadruped velocity task | [L] |
| Torso centre of mass | +-0.05 m per axis | Go1 | [P] |
| Inertia | 50 to 150 % | Minitaur | [T] |
| Motor strength | 80 to 120 % | Minitaur | [T] |
| Motor (joint) friction | 0 to 0.05 N·m | Minitaur | [T] |
| Joint friction loss | x 0.9 to 1.1 | Go1 | [P] |
| Armature | x 1.0 to 1.05 | Go1 | [P] |
| Default joint pose | +-0.05 rad | Go1 | [P] |
| Battery voltage | 14.0 to 16.8 V | Minitaur | [T] |

## Contact

| Parameter | Range used | Robot | Source |
|---|---|---|---|
| Foot-floor friction | 0.5 to 1.25 | Minitaur (rubber feet on carpets) | [T] |
| Ground friction | 0.5 to 1.25 | ANYmal and others | [G] |
| Floor friction | 0.4 to 1.0 | Go1 | [P] |
| Static / dynamic friction | fixed 0.8 / 0.6 (not randomised in the base task) | quadruped velocity task | [L] |

## Timing

| Parameter | Range used | Robot | Source |
|---|---|---|---|
| Control step | 3 to 20 ms | Minitaur | [T] |
| Latency | 0 to 40 ms | Minitaur | [T] |
| Measured latency | 3 ms (PD on the microcontroller), 15 to 19 ms (policy on the Jetson TX2) | Minitaur | [T] |

## Observation noise

Uniform noise, added to the raw value before scaling:

| Observation | Half-width | Source |
|---|---|---|
| Joint position | 0.01 rad | [G], [L] |
| Joint velocity | 1.5 rad/s | [G], [L] |
| Base linear velocity | 0.1 m/s | [G], [L] |
| Base angular velocity | 0.2 rad/s | [G], [L] |
| Projected gravity | 0.05 | [G], [L] |
| Height scan | 0.1 m | [G], [L] |

Tan et al. used Gaussian IMU noise with a standard deviation of 0 to 0.05 rad and an IMU bias of
-0.05 to 0.05 rad [T].

## Disturbances

| Disturbance | Setting | Source |
|---|---|---|
| Push by setting base velocity | every 15 s, up to 1 m/s in x and y | [G] |
| Push by adding to base velocity | every 10 to 15 s, +-0.5 m/s in x and y | [L] |
| Push force on the base | every 1.2 s, lasting 0.06 s, 130 to 220 N, random direction | [T] (Minitaur) |
| Reset joint positions | x 0.5 to 1.5 of the default pose | [L] |

Push sizes scale with the robot: compare the velocity change or impulse to your robot's mass and
speed, not the raw number.

## Sources

- **[T]** Tan et al., "Sim-to-Real: Learning Agile Locomotion For Quadruped Robots", RSS 2018
  (arXiv:1804.10332), Table I and section on robust controllers.
- **[G]** legged_gym, `legged_gym/envs/base/legged_robot_config.py` (`domain_rand`, `noise`),
  commit 8fa29ac (2025-05-29). The repository now points users to Isaac Lab.
- **[L]** Isaac Lab 3.0, `source/isaaclab_tasks/isaaclab_tasks/core/velocity/velocity_env_cfg.py`
  (`EventsCfg`, `ObservationsCfg`), tag v3.0.0 and main at 892354c (2026-11-18).
- **[P]** MuJoCo Playground, `rss2025/mujoco_playground/_src/locomotion/go1/randomize.py`,
  commit 3ff05b5 (2026-11-18).
