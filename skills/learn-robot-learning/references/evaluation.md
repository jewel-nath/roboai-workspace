# Evaluating a policy: offline, in simulation, on the robot

Part of [learn-robot-learning](../SKILL.md). Checked against LeRobot 0.7.0 and `main` (b07adcc, 2026-11-24):
`docs/source/libero.mdx`, `inference.mdx`, `hil_data_collection.mdx`, `hilserl.mdx`, `simulation.mdx`,
`src/lerobot/utils/eval_stats.py`, `src/lerobot/robots/so_follower/`; SimplerEnv `main` (eddb569, 2026-09-30);
ManiSkill 3.0.1 docs; Isaac-GR00T N1.7 `getting_started/finetune_new_embodiment.md`. Nothing here was run.

Only closed-loop success on the task decides whether a policy works. Loss and open-loop error find setup mistakes
cheaply; simulation benchmarks compare methods; the robot gives the answer.

## 1. Offline checks

- **Held-out loss:** train with `--dataset.eval_split=0.1 --eval_steps=2000`. A held-out loss that rises while
  the training loss falls is overfitting; pick checkpoints from before that point to test on the robot.
- **Open-loop replay:** feed recorded observations of a held-out episode to the policy and plot predicted against
  recorded actions. GR00T ships this as `gr00t/eval/open_loop_eval.py`
  ([openpi-groot.md](openpi-groot.md#fine-tune-and-check-offline)). Flat predictions mean a key or
  normalisation mismatch, not an under-trained model.
- Neither predicts closed-loop success: small per-step errors compound once the policy drives the robot into
  states the demonstrations never visited.

## 2. Simulation benchmarks

### LIBERO through LeRobot

LIBERO (130 Franka Panda tasks in five suites; MIT code) via LeRobot's `hf-libero` package, Linux only, MuJoCo
rendering. The upstream LIBERO repo pins Python 3.8 and PyTorch 1.11, so use LeRobot's packaging instead.

```bash
pip install 'lerobot[libero]'
export MUJOCO_GL=egl                                  # headless rendering
lerobot-eval --policy.path=${HF_USER}/pi05_libero --env.type=libero \
  --env.task=libero_spatial,libero_object,libero_goal,libero_10 \
  --eval.n_episodes=10 --eval.batch_size=1 --env.max_parallel_tasks=1
```

- Standard protocol (LeRobot docs): 10 episodes per task over the four suites, 400 episodes, ideally averaged
  over 3 seeds; use hard resets when reproducing published numbers.
- `--env.control_mode=relative` (default) or `absolute` must match how the checkpoint was trained.
- Observations: `observation.images.image` (agent view), `observation.images.image2` (wrist), 8-dim state;
  actions: 7-dim end-effector delta plus gripper in [-1, 1]. Use `--rename_map` for policies with other keys.
- `lerobot-env-server --config_path=docker/sim/configs/libero.yaml --sim.task=<suite> --docker=true` runs the
  simulator in a container, and `--env.server.endpoint=tcp/127.0.0.1:7448` points `lerobot-eval` at it, keeping
  simulator dependencies apart from the policy's.
- LIBERO results say how a method does on LIBERO's robot and tasks. They are useful to check a training pipeline
  (reproduce a published checkpoint first) and to compare methods, not to predict success on your robot.

### SimplerEnv

Real-to-sim evaluation for two robots only: Google Robot (Fractal/RT-1 data) and WidowX (BridgeData V2), built
on SAPIEN and ManiSkill2. Two setups: visual matching (real background overlaid) and variant aggregation
(backgrounds, lighting and distractors averaged). Default control rates: 3 Hz Google Robot, 5 Hz WidowX.

```bash
conda create -n simpler_env python=3.10 && conda activate simpler_env
git clone https://github.com/simpler-env/SimplerEnv --recurse-submodules && cd SimplerEnv
pip install numpy==1.24.4                    # newer numpy breaks IK in pinocchio (SimplerEnv README)
pip install -e ManiSkill2_real2sim && pip install -e .
```

```python
import simpler_env
from simpler_env.utils.env.observation_utils import get_image_from_maniskill2_obs_dict

env = simpler_env.make("widowx_carrot_on_plate")
obs, _ = env.reset()
instruction = env.get_language_instruction()
done = truncated = False
while not (done or truncated):
    image = get_image_from_maniskill2_obs_dict(env, obs)
    action = my_policy(image, instruction)     # xyz delta, axis-angle delta, gripper
    obs, reward, done, truncated, info = env.step(action)
```

Use it for generalist policies trained on Open X-Embodiment, Bridge or Fractal data (Octo, OpenVLA, RT-1,
GR00T's SimplerEnv checkpoints). It needs an NVIDIA GPU (RTX for the ray-traced scenes). A GPU-parallel version
lives on the repository's `maniskill3` branch.

### Your own robot in simulation

For a policy on your robot, build a matching scene: ManiSkill ships an SO-100 model and `SO100GraspCube-v1`
(with the `lerobot-sim2real` tutorial); LeRobot's EnvHub can serve simulators to `lerobot-eval`. A sim twin must
reproduce the cameras, control mode and rate of the real setup, and still only screens policies before robot
time ([sim-to-real](../../sim-to-real/SKILL.md)).

## 3. Report numbers with an interval

```python
from lerobot.utils.eval_stats import wilson_interval

low, high = wilson_interval(15, 20)        # 15 successes in 20 trials
print(f"75% success, 95% interval {low:.0%}-{high:.0%}")   # about 53%-89%
```

- `lerobot-eval` prints the same interval as `pc_success_ci95`.
- 20 trials cannot separate 75% from 60%. Decide how many trials you need before comparing policies, and run
  both on the same start conditions (and in simulation the same `--seed`).
- The interval covers which episodes were drawn, not training-seed variation; that needs several training runs.

## 4. On the real robot

### Limits for policy runs

The policy has no idea of safety. Before the first autonomous run:

- **E-stop:** a switch that cuts motor power, within reach of the operator, tested that session
  ([arch-safety](../../arch-safety/SKILL.md)). On an SO-101 that is the motor power supply, not the USB cable.
- **Step limit:** `--robot.max_relative_target=10.0` caps each command to 10 units from the present position
  (degrees for SO-101 body joints, 0-100 range for the gripper; a dict sets it per motor). Start small; widen it
  only when motion is visibly too slow.
- **Joint and workspace limits:** keep calibration ranges sane; outside LeRobot (openpi, GR00T or ROS clients),
  clamp every action to joint limits and a per-step change in your own loop before sending it.
- **Speed and force:** start with slow motions and light objects; for ros2_control arms, use the controller's
  limits ([ros2-control](../../ros2-control/SKILL.md)).
- **Clear area:** nothing fragile or human inside the reach of the arm; an operator watching every run.
- **Stop on the unexpected:** collisions, oscillation, the arm pressing on the table, or a policy that stalls.

Commands in this reference that move a robot were not run. They rely on the limits above.

### Protocol

1. Write the start conditions (for example 5 object positions x 4 trials = 20), the success rule and the time
   limit before the session; randomise the order.
2. Use the recording's cameras, `--robot.id`, task text and `--fps`.
3. Record every trial:

```bash
lerobot-rollout --strategy.type=episodic --policy.path=outputs/train/act_pick_cube/checkpoints/last/pretrained_model \
  --robot.type=so101_follower --robot.port=/dev/ttyACM0 --robot.id=robot-01 --robot.cameras="$CAMS" \
  --robot.max_relative_target=10.0 \
  --teleop.type=so101_leader --teleop.port=/dev/ttyACM1 --teleop.id=robot-01-leader \
  --dataset.repo_id=${HF_USER}/rollout_eval_act_pick_cube --dataset.push_to_hub=false \
  --dataset.num_episodes=20 --dataset.episode_time_s=30 --dataset.reset_time_s=15 \
  --dataset.single_task="Pick the cube and put it in the bin"
```

   Rollout dataset names must start with `rollout_`. The teleoperator drives the robot during resets; without
   one the robot holds its position. Right arrow ends an episode, left arrow discards it, `Esc` stops.
4. Log per trial: start condition, success or failure, failure type (missed grasp, dropped, wrong place,
   timeout, collision, stopped by operator).
5. Report k/N with the Wilson interval, per start condition as well as overall, with the checkpoint, dataset
   revision and limits used.

### Strategies and inference options

| Option | Use |
|---|---|
| `--strategy.type=base` | Quick runs, nothing recorded (`--duration` seconds) |
| `--strategy.type=episodic` | Scored evaluation episodes with resets |
| `--strategy.type=sentry` / `highlight` | Long unattended runs; keep only interesting moments |
| `--strategy.type=dagger` | Human corrections recorded as new training data |
| `--inference.type=rtc` | Smooth motion when a VLA's inference takes a noticeable part of each chunk |
| `--inference.type=remote` | Policy on a GPU host, robot loop keeps running ([remote inference docs](https://huggingface.co/docs/lerobot/remote_inference)) |
| `--interpolation_multiplier=N` | Robot commands at `fps x N` between policy actions |

## 5. Learn from failures

- **More demonstrations** for the start conditions that fail, recorded the same way.
- **Human corrections:** `--strategy.type=dagger` runs the policy; `Space` pauses it, `Tab` hands control to the
  teleoperator and back. Only correction windows are recorded by default (`--strategy.record_autonomous=true`
  records everything, with intervention frames marked). Merge them with the original data and retrain.
- **Online RL on the robot:** LeRobot's HIL-SERL (`pip install 'lerobot[hilserl]'`) trains a SAC actor on the
  real robot from a few demonstrations, a learned success classifier and human interventions, for short tasks
  of about 5-10 s (LeRobot docs). It needs joint or end-effector bounds and an NVIDIA GPU.
