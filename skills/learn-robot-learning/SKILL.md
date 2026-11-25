---
name: learn-robot-learning
description: Teach a robot a task from data - imitation or RL; LeRobot recording (SO-101 leader arm, lerobot-record, LeRobotDataset v3),
  dataset checks, ACT, Diffusion Policy, SmolVLA, pi0/pi0.5 (LeRobot, openpi), GR00T N1.7 fine-tuning; evaluation in LIBERO, SimplerEnv
  and on the real robot with limits; RL in Isaac Lab, ManiSkill, Stable-Baselines3 on Gymnasium; ROS 2 bags to LeRobot datasets.
license: Apache-2.0
metadata:
  sources: []
  evidence: researched
  last_verified: 2026-11-25
---

# Robot learning: imitation and reinforcement learning

Lets an agent teach a robot a task from data: choose imitation or reinforcement learning, record and check
demonstrations, train or fine-tune a policy, and evaluate it in simulation and on the robot within limits.
Written against LeRobot 0.7.0 (checked against `main` b07adcc, 2026-11-24), openpi `main` (215abfb, 2026-08-24),
Isaac-GR00T N1.7 (`main` 708617f, 2026-11-17), Isaac Lab 3.0.0, ManiSkill 3.0.1, Stable-Baselines3 2.9.2 and
Gymnasium 1.4.0, from their sources and docs; the recipes were not run.

## When to use

- Deciding between imitation learning and reinforcement learning for a task.
- Recording teleoperated demonstrations with LeRobot (leader arm, cameras, episodes), locally or to the Hub.
- Checking a dataset before training: episodes, cameras, action and state ranges, recording rate.
- Training ACT or Diffusion Policy, or fine-tuning SmolVLA, pi0/pi0.5 or GR00T, on your robot's data.
- Evaluating a policy in LIBERO or SimplerEnv, or on the real robot with limits and an e-stop.
- Training locomotion or contact-rich skills with RL in Isaac Lab, ManiSkill or Stable-Baselines3 (SB3).

Elsewhere: running a trained policy fast on a Jetson (export, TensorRT, ONNX Runtime, the on-robot node) in
[learn-edge-deployment](../learn-edge-deployment/SKILL.md); domain randomisation, system identification and the
staged transfer of a sim-trained policy in [sim-to-real](../sim-to-real/SKILL.md); cameras and `camera_info` in
[perception-camera](../perception-camera/SKILL.md); planned (not learned) arm motion in
[manip-moveit2](../manip-moveit2/SKILL.md); stops and limits in [arch-safety](../arch-safety/SKILL.md).

## Imitation or reinforcement learning

| Situation | Choose | Start with |
|---|---|---|
| A person can do the task by teleoperation; reward hard to write; manipulation | Imitation learning | ACT in LeRobot, about 50 episodes |
| Several tasks, objects or language instructions; you have a large GPU | Fine-tune a vision-language-action model (VLA) | SmolVLA, then pi0.5 or GR00T N1.7 |
| Locomotion, balance or contact-rich control a person cannot teleoperate well; a good simulator model | RL in simulation, then [sim-to-real](../sim-to-real/SKILL.md) | Isaac Lab with RSL-RL PPO |
| A small task with a fast state-based simulator you wrote | RL on a Gymnasium environment | SB3 PPO or SAC |
| Imitation gets close but fails on states the demos never reached | Human corrections on the robot | `lerobot-rollout --strategy.type=dagger`; LeRobot HIL-SERL |

Compute (upstream claims): ACT is about 80M parameters and trains in a few hours on one GPU (LeRobot ACT docs);
SmolVLA is 450M, about 4 h for 20k steps on one A100 (LeRobot SmolVLA docs); openpi needs more than 8 GB to run,
22.5 GB for LoRA and 70 GB for full fine-tuning (openpi README); GR00T N1.7 needs 16 GB+ to run and recommends
40 GB+ to fine-tune (Isaac-GR00T README). Policy comparison:
[choose a robot learning policy](../../wiki/guides/choose-a-robot-learning-policy.md).

## Quick start

SO-101 follower and leader arm, two cameras, LeRobot 0.7.0 on Python 3.12, a CUDA GPU. Details in
[lerobot-recording.md](references/lerobot-recording.md).

```bash
pip install 'lerobot[core_scripts,feetech,training]'
lerobot-find-port                                  # once per arm; unplug when asked
lerobot-calibrate --robot.type=so101_follower --robot.port=/dev/ttyACM0 --robot.id=robot-01
lerobot-calibrate --teleop.type=so101_leader --teleop.port=/dev/ttyACM1 --teleop.id=robot-01-leader
lerobot-find-cameras opencv
CAMS='{ top: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}, wrist: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}}'
lerobot-record --robot.type=so101_follower --robot.port=/dev/ttyACM0 --robot.id=robot-01 --robot.cameras="$CAMS" \
  --teleop.type=so101_leader --teleop.port=/dev/ttyACM1 --teleop.id=robot-01-leader --display_data=true \
  --dataset.repo_id=local/pick_cube --dataset.no_stamp=true --dataset.push_to_hub=false \
  --dataset.single_task="Pick the cube and put it in the bin" --dataset.num_episodes=50 \
  --dataset.episode_time_s=30 --dataset.reset_time_s=15 --dataset.streaming_encoding=true
lerobot-dataset-viz --repo-id local/pick_cube --root ~/.cache/huggingface/lerobot/local/pick_cube \
  --mode local --episode-index 0
lerobot-train --dataset.repo_id=local/pick_cube --policy.type=act --policy.device=cuda --policy.push_to_hub=false \
  --dataset.eval_split=0.1 --eval_steps=2000 --steps=40000 --output_dir=outputs/train/act_pick_cube --job_name=act_pick_cube
# arm clear, e-stop (power switch) in reach, then:
lerobot-rollout --strategy.type=base --policy.path=outputs/train/act_pick_cube/checkpoints/last/pretrained_model \
  --robot.type=so101_follower --robot.port=/dev/ttyACM0 --robot.id=robot-01 --robot.cameras="$CAMS" \
  --robot.max_relative_target=10.0 --task="Pick the cube and put it in the bin" --duration=30
```

## Workflow

1. **Define the task and its success test.** Write down the start conditions (object positions, lighting),
   what counts as success, and the time limit, before recording anything. Choose the method from the table above.
   *Check:* a written task card with at least five distinct start conditions and a pass or fail rule a second
   person would apply the same way.

2. **Prepare the robot.** Calibrate with fixed ids, mount cameras rigidly, find joint limits, and set a step
   limit (`max_relative_target`) for policy runs. A ROS 2 robot records through rosbag2 instead
   ([ros2.md](references/ros2.md)). *Check:* `lerobot-teleoperate` with `--display_data=true` shows both camera
   streams and the follower tracks the leader over the whole workspace with no motor errors.

3. **Record demonstrations.** About 50 episodes to start, spread evenly over the start conditions (LeRobot
   suggests 10 per object position), one consistent strategy, task visible in the cameras
   ([lerobot-recording.md](references/lerobot-recording.md)). *Check:* the cadence report after recording shows
   the effective rate within a few percent of `--dataset.fps`; re-record otherwise.

4. **Check the dataset.** Watch several episodes, confirm camera keys and resolution, look at per-joint ranges and
   episode lengths, drop failed or odd episodes ([dataset-checks.md](references/dataset-checks.md)).
   *Check:* the check script reports no constant or clipped dimension, no episode far shorter or longer than the
   rest, and the camera keys you will use at deployment.

5. **Train a baseline.** ACT first; Diffusion Policy when demonstrations are multimodal (several valid ways to do
   the task). Size `--steps` from epochs: LeRobot notes imitation learning usually converges within 5-10 epochs,
   and steps = epochs x frames / batch size ([training.md](references/training.md)).
   *Check:* training loss falls, held-out loss (`--dataset.eval_split`) stops falling before the last checkpoint,
   and `train_config.json` is saved with the checkpoint.

6. **Fine-tune a VLA when the baseline is not enough.** SmolVLA (`lerobot/smolvla_base`), pi0.5 in LeRobot or
   openpi, or GR00T N1.7 in LeRobot or Isaac-GR00T. Accept the gated licences first; openpi and Isaac-GR00T read
   LeRobot v2.1 datasets ([training.md](references/training.md),
   [openpi-groot.md](references/openpi-groot.md)). *Check:* the first training batch passes without feature or
   normalisation errors, and an open-loop replay of a held-out episode tracks the recorded actions.

7. **Evaluate in simulation when it applies.** LIBERO and SimplerEnv measure policies for their own robots and
   tasks; use them to compare methods or check a pipeline, not to predict your robot's success
   ([evaluation.md](references/evaluation.md)). *Check:* results are reported with episode count and a 95%
   interval, on the suite's standard protocol.

8. **Evaluate on the real robot, within limits.** Fixed list of start conditions, same cameras and task text as
   recording, step limit on, e-stop in reach, low speed first; record evaluation episodes
   (`--strategy.type=episodic`) and note each failure ([evaluation.md](references/evaluation.md)).
   *Check:* success k/N with its interval over at least 20 trials, compared with the baseline on the same starts.

9. **Improve from failures.** Add demonstrations for the failing start conditions, or record human corrections
   with `--strategy.type=dagger`, then retrain. *Check:* the failure that triggered the change is fixed and
   success on the other starts did not drop.

10. **Train with RL when the task needs it.** Smoke-test the environment, train in Isaac Lab, ManiSkill or SB3,
    evaluate deterministically over many seeds, then follow [sim-to-real](../sim-to-real/SKILL.md)
    ([reinforcement-learning.md](references/reinforcement-learning.md)). *Check:* the trained policy meets the
    task's success rule in simulation with randomisation on, across seeds.

11. **Hand over for deployment.** Fast on-robot inference, export and the robot node are in
    [learn-edge-deployment](../learn-edge-deployment/SKILL.md). *Check:* the handed-over checkpoint, its
    normalisation statistics, camera names, joint order, control rate and evaluation results travel together.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| Policy moves strangely or fails on load at deployment | Camera names, order or resolution differ from recording | Reuse the recording `--robot.cameras`; `--rename_map` (pi0, pi0.5, SmolVLA, X-VLA only) |
| Joints offset after a restart | Different `--robot.id`, so another calibration file | Same id in calibrate, record, train and rollout |
| Replayed motion runs faster than it was recorded | Loop below `--dataset.fps`; timestamps come from frame index | Read the cadence report; lower camera load; `--dataset.streaming_encoding=true` |
| Training cannot find the dataset | `lerobot-record` appended `_YYYYMMDD_HHMMSS` to the repo id | Use the stamped name, or record with `--dataset.no_stamp=true` |
| openpi or Isaac-GR00T rejects the dataset | They read LeRobot v2.1; LeRobot records v3.0 | Convert v3.0 to v2.1 ([openpi-groot.md](references/openpi-groot.md)) |
| `QUANTILES normalization mode requires q01 and q99 stats` | pi0.5 normalises with quantiles; old stats | `lerobot-edit-dataset --operation.type recompute_stats` |
| Fine-tune ignores the checkpoint's `n_action_steps` or cameras | `--policy.pretrained_path` loads weights only | Use `--policy.path`, or set those flags again |
| `GatedRepoError` or 401 on first batch | PaliGemma tokenizer (pi0, pi0.5) or Cosmos-Reason2-2B (GR00T) is gated | Accept the licence on the Hub; `hf auth login` |
| SmolVLA stops with a feature mismatch | `smolvla_base` expects `camera1`..`camera3` | `--rename_map` from your camera keys |
| GR00T N1.5 checkpoint rejected by LeRobot | LeRobot supports GR00T N1.7 only now | Migrate to N1.7, or pin `lerobot==0.5.1` |
| Robot pauses or jerks between action chunks | Slow VLA inference blocks the loop | `--inference.type=rtc`, or remote inference on a GPU host |
| Low training loss, robot fails | Too few variations, memorised trajectories | Judge checkpoints on the robot; add demos where it fails |
| Loss diverges in openpi | Near-constant dimension gives tiny `std`/quantile spread | Inspect `norm_stats.json`; drop or fix that dimension |
| Old commands fail | `control_robot.py`, `--control.type=record`, `lerobot-record --policy.path`, `--wandb.enable` | `lerobot-record`, `lerobot-rollout`, `--trackio.enable` |
| SB3 policy fails outside training | `VecNormalize` statistics not saved or still updating | Save them; load with `training=False`, `norm_reward=False` |
| ROS 2 message import fails next to LeRobot | Jazzy message modules use numpy 1.26's C API; LeRobot needs numpy 2 | Separate processes ([ros2.md](references/ros2.md)) |
| Isaac Lab script paths not found | Isaac Lab 2.x `./isaaclab.sh -p scripts/.../rsl_rl/train.py` | 3.0: `uv run isaaclab train --rl_library rsl_rl --task ...` |

## Checks

Before reporting a learned skill done:

- The task card, dataset name and revision, recording rate, episode count and camera keys are written down.
- The dataset check script output is saved; dropped episodes are listed with the reason.
- The checkpoint directory holds weights, `config.json`, `train_config.json` and processor or norm-stat files.
- Real-robot evaluation: success k/N with a 95% interval over a fixed list of start conditions, the limits used
  (`max_relative_target`, speed, workspace), the e-stop tested that session, and a note per failure.
- RL: deterministic evaluation over many seeds with randomisation on; sim-to-real stages recorded.
- Licences of every model, dataset and asset used are noted (gated, non-commercial or NVIDIA terms).

## Version and distro differences

- **LeRobot before 0.4:** dataset v2.x (convert with `python -m lerobot.scripts.convert_dataset_v21_to_v30`).
  Before `lerobot-rollout`, policies ran through `lerobot-record --policy.path`; even older releases used
  `python lerobot/scripts/control_robot.py`. W&B logging became Trackio (old `wandb` sections are migrated).
- **GR00T:** N1.7 replaced N1.6 (`n1d6` branch) and N1.5 (`n1d5`); N1.7 moved to a Cosmos-Reason2-2B backbone,
  132-dim state and action, 40-step horizon, and renamed `--action-horizon` to `--execution-horizon`.
- **Jazzy** (Ubuntu 24.04, Python 3.12): matches LeRobot (3.12-3.13) and GR00T (3.12 only), but keep them in
  their own virtual environment because of the numpy split above.
- **Lyrical** (Ubuntu 26.04, Python 3.14): no learning stack here supports 3.14; run it in its own Python 3.12
  environment or container and bridge to ROS. System FFmpeg 8 breaks GR00T's `torchcodec` 0.8 (install
  FFmpeg < 8 from conda); LeRobot's `torchcodec` range supports FFmpeg 8 from 0.8.1.

## Related

- References: [lerobot-recording.md](references/lerobot-recording.md),
  [dataset-checks.md](references/dataset-checks.md), [training.md](references/training.md),
  [openpi-groot.md](references/openpi-groot.md), [evaluation.md](references/evaluation.md),
  [reinforcement-learning.md](references/reinforcement-learning.md), [ros2.md](references/ros2.md).
- Wiki: [LeRobot](../../wiki/learning/frameworks/lerobot.md), [ACT](../../wiki/learning/policies/act.md),
  [Diffusion Policy](../../wiki/learning/policies/diffusion-policy.md),
  [SmolVLA](../../wiki/learning/models/smolvla.md), [pi0](../../wiki/learning/models/pi0.md),
  [GR00T](../../wiki/learning/models/gr00t.md), [Isaac Lab](../../wiki/learning/frameworks/isaac-lab.md),
  [ManiSkill](../../wiki/learning/frameworks/maniskill.md),
  [Stable-Baselines3](../../wiki/learning/frameworks/stable-baselines3.md),
  [Gymnasium](../../wiki/learning/frameworks/gymnasium.md), [LIBERO](../../wiki/learning/benchmarks/libero.md),
  [SimplerEnv](../../wiki/learning/benchmarks/simpler-env.md),
  [Open X-Embodiment](../../wiki/learning/datasets/open-x-embodiment.md),
  [DROID](../../wiki/learning/datasets/droid.md), [Rerun](../../wiki/tools/rerun.md),
  [Isaac Sim](../../wiki/tools/isaac-sim.md), [MuJoCo](../../wiki/tools/mujoco.md),
  [choose a robot learning policy](../../wiki/guides/choose-a-robot-learning-policy.md),
  [choose a simulator](../../wiki/guides/choose-a-simulator.md), robots [SO-101](../../wiki/robots/so-101.md)
  and [Koch v1.1](../../wiki/robots/koch-v1-1.md).
- Skills: [learn-edge-deployment](../learn-edge-deployment/SKILL.md), [sim-to-real](../sim-to-real/SKILL.md),
  [perception-camera](../perception-camera/SKILL.md), [arch-safety](../arch-safety/SKILL.md),
  [ros2-control](../ros2-control/SKILL.md), [ros2-core](../ros2-core/SKILL.md),
  [manip-moveit2](../manip-moveit2/SKILL.md), [manip-grasping](../manip-grasping/SKILL.md),
  [ops-docker-ci](../ops-docker-ci/SKILL.md) (GPU containers), [ops-fleet](../ops-fleet/SKILL.md); later
  `sim-mujoco` and the firmware and motor-control skills.
- Upstream: huggingface/lerobot (`docs/source`), Physical-Intelligence/openpi, NVIDIA/Isaac-GR00T,
  isaac-sim/IsaacLab, haosulab/ManiSkill, DLR-RM/stable-baselines3, Farama-Foundation/Gymnasium,
  simpler-env/SimplerEnv, Lifelong-Robot-Learning/LIBERO.
