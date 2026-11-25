# Training and fine-tuning policies in LeRobot

Part of [learn-robot-learning](../SKILL.md). Checked against LeRobot 0.7.0 and `main` (b07adcc, 2026-11-24):
`src/lerobot/configs/train.py`, `configs/default.py`, the policy configs under `src/lerobot/policies/`, and
`docs/source/il_robots.mdx`, `act.mdx`, `policy_diffusion_README.md`, `smolvla.mdx`, `pi0.mdx`, `pi05.mdx`,
`groot.mdx`, `peft_training.mdx`. Model licences read from the Hugging Face model cards on 2026-11-25. Nothing
here was run. openpi and Isaac-GR00T's own trainers are in [openpi-groot.md](openpi-groot.md).

## Common flags

| Flag | Default | Notes |
|---|---|---|
| `--dataset.repo_id` | required | Local datasets are found in `$HF_LEROBOT_HOME/<repo_id>`; `--dataset.root` to point elsewhere |
| `--policy.type` | — | Train from scratch (or with `--policy.pretrained_path` for weights only) |
| `--policy.path` | — | Start from a checkpoint: weights and its `config.json`; omit `--policy.type` |
| `--policy.device` | auto | `cuda`, `mps`, `cpu` |
| `--policy.push_to_hub` | `true` | Needs `--policy.repo_id`; set `false` to keep the model local |
| `--batch_size` | 8 | Raise until GPU memory is nearly full |
| `--steps` | 100000 | See below |
| `--save_freq` | 20000 | Checkpoint interval; the last step is always saved |
| `--num_workers` | 4 | Data loader processes; video decoding is often the bottleneck |
| `--seed` | 1000 | Fix it when comparing runs |
| `--dataset.eval_split` | 0.0 | Fraction of episodes per task held out for an offline loss |
| `--eval_steps` | 0 | Compute the held-out loss every N steps (needs `eval_split` > 0) |
| `--dataset.image_transforms.enable` | `false` | Colour, sharpness and affine augmentation at training time only |
| `--trackio.enable` | `false` | Local Trackio dashboard: `trackio show --project lerobot` |
| `--output_dir`, `--job_name` | — | Checkpoints in `<output_dir>/checkpoints/<step>/pretrained_model`, `last` links to the newest |

Resume: `lerobot-train --config_path=<output_dir>/checkpoints/last/pretrained_model/train_config.json --resume=true`.

### How many steps

steps = epochs x total frames / batch size. LeRobot's guide notes imitation learning usually converges within
5-10 epochs. Example: 50 episodes x 30 s x 30 fps = 45,000 frames; at batch 8, one epoch is about 5,600 steps,
so 30k-60k steps rather than the 100k default. Save often enough to compare several checkpoints on the robot:
the lowest loss is not always the best policy.

### Checkpoint contents

`pretrained_model/` holds `config.json`, `model.safetensors`, `train_config.json` and the processor pipelines
(`policy_preprocessor*`, `policy_postprocessor*`) with the normalisation statistics. Ship the whole folder;
the statistics are part of the policy. `training_state/` (optimizer, scheduler, step) is only for resuming.

## ACT

```bash
lerobot-train --dataset.repo_id=local/pick_cube --policy.type=act --policy.device=cuda \
  --policy.push_to_hub=false --batch_size=8 --steps=40000 --save_freq=5000 \
  --dataset.eval_split=0.1 --eval_steps=2000 --output_dir=outputs/train/act_pick_cube --job_name=act_pick_cube
```

- Defaults: `chunk_size=100`, `n_action_steps=100` (predicts and executes 100 actions per inference, about 3.3 s
  at 30 Hz), ResNet-18 backbone with ImageNet weights, `use_vae=true`, `kl_weight=10`, learning rate 1e-5.
- `--policy.temporal_ensemble_coeff=0.01` with `--policy.n_action_steps=1` runs inference every step and blends
  overlapping chunks (smoother, more compute). The ACT paper used 0.01 (Zhao et al. 2023).
- A smaller `n_action_steps` reacts faster to disturbances; keep `chunk_size` as trained.
- No extra install. LeRobot's docs: a few hours for 100k steps on a single GPU, often good with about 50 demos.

## Diffusion Policy

```bash
pip install 'lerobot[diffusion]'
lerobot-train --dataset.repo_id=local/pick_cube --policy.type=diffusion --ema.type=warmup \
  --policy.device=cuda --policy.push_to_hub=false --batch_size=32 --steps=100000 \
  --output_dir=outputs/train/dp_pick_cube --job_name=dp_pick_cube
```

- Defaults in 0.7: `n_obs_steps=2`, `horizon=64`, `n_action_steps=32`, DDPM with 100 training timesteps, U-Net
  `down_dims=(512, 1024, 2048)`, random crop at training when `crop_shape` (or `resize_shape` with
  `crop_ratio` < 1) is set.
- `--ema.type=warmup` keeps an exponential moving average like the reference implementation; evaluate
  `pretrained_model_ema` in the checkpoint folder.
- Choose it over ACT when the demonstrations contain several valid ways to do the task.
- `--policy.num_inference_steps` lower than the training timesteps speeds inference (DDIM via
  `--policy.noise_scheduler_type=DDIM`); measure success again after changing it.

## SmolVLA

```bash
pip install 'lerobot[smolvla]'
lerobot-train --policy.path=lerobot/smolvla_base --dataset.repo_id=${HF_USER}/pick_cube \
  --rename_map='{"observation.images.top": "observation.images.camera1", "observation.images.wrist": "observation.images.camera2"}' \
  --policy.repo_id=${HF_USER}/smolvla_pick_cube --batch_size=64 --steps=20000 \
  --output_dir=outputs/train/smolvla_pick_cube --job_name=smolvla_pick_cube --policy.device=cuda
```

- 450M parameters on SmolVLM2-500M; both Apache-2.0 on their model cards.
- The base model expects `camera1`..`camera3`; without the rename map training stops with a feature mismatch.
- LeRobot reports about 4 h for 20k steps on one A100. Language-conditioned: keep `--dataset.single_task`
  texts meaningful and pass the same text at rollout.

## pi0 and pi0.5 in LeRobot

```bash
pip install 'lerobot[pi]'
hf auth login        # after accepting google/paligemma-3b-pt-224 on the Hub (gated)
lerobot-train --dataset.repo_id=${HF_USER}/pick_cube --policy.type=pi05 \
  --policy.pretrained_path=lerobot/pi05_base --policy.repo_id=${HF_USER}/pi05_pick_cube \
  --policy.dtype=bfloat16 --policy.gradient_checkpointing=true --policy.compile_model=true \
  --policy.freeze_vision_encoder=true --policy.train_expert_only=true \
  --batch_size=32 --steps=20000 --save_freq=5000 --policy.device=cuda \
  --output_dir=outputs/train/pi05_pick_cube --job_name=pi05_pick_cube
```

- `--policy.type=pi0` with `lerobot/pi0_base` works the same way. Both predict 50-step chunks by default.
- pi0.5 normalises state and action with quantiles (`q01`, `q99`): recompute statistics first
  ([dataset-checks.md](dataset-checks.md#3-edit-the-dataset)) or pass
  `--policy.normalization_mapping='{"ACTION": "MEAN_STD", "STATE": "MEAN_STD", "VISUAL": "IDENTITY"}'`.
- `--policy.pretrained_path` loads weights only: settings stored in the checkpoint (`n_action_steps`,
  `empty_cameras`) fall back to defaults unless you pass them. `--policy.path` loads both, without `--policy.type`.
- `train_expert_only=true` and a frozen vision encoder cut memory at some cost in success (LeRobot pi0.5 docs);
  the full fine-tune example in those docs is sized for one 80 GB GPU.
- Relative actions (`--policy.use_relative_actions=true --policy.relative_exclude_joints='["gripper"]'`) need
  statistics recomputed in relative space with the same chunk size.

## GR00T N1.7 in LeRobot

```bash
pip install 'lerobot[groot,training]'
hf auth login        # nvidia/Cosmos-Reason2-2B backbone is gated
lerobot-train --dataset.repo_id=${HF_USER}/pick_cube --dataset.image_transforms.enable=true \
  --policy.type=groot --policy.base_model_path=nvidia/GR00T-N1.7-3B --policy.embodiment_tag=new_embodiment \
  --policy.chunk_size=16 --policy.n_action_steps=16 --policy.use_relative_actions=true \
  --policy.relative_exclude_joints='["gripper"]' --policy.use_bf16=true --policy.device=cuda \
  --policy.repo_id=${HF_USER}/groot_pick_cube --batch_size=64 --steps=20000 --save_freq=5000 \
  --env_eval_freq=0 --output_dir=outputs/train/groot_pick_cube --job_name=groot_pick_cube
```

- LeRobot supports N1.7 only; N1.5 checkpoints are rejected (pin `lerobot==0.5.1` for them).
- `new_embodiment` is the tag for a robot outside GR00T's pretraining set, such as an SO-101.
- NVIDIA states 16 GB+ for inference and recommends 40 GB+ for fine-tuning.

## LoRA and other PEFT methods

```bash
pip install 'lerobot[peft]'
lerobot-train --policy.path=lerobot/smolvla_base ... --peft.method_type=LORA --peft.r=64 --peft.lora_alpha=64 \
  --policy.optimizer_lr=1e-3 --policy.scheduler_decay_lr=1e-4
```

SmolVLA, pi0, pi0.5 and MolmoAct2 ship default target modules; others need `--peft.target_modules`. LeRobot
suggests a learning rate about 10x the full fine-tune's.

## Training in the cloud

`--job.target=a10g-small` (any flavour from `hf jobs hardware`) runs `lerobot-train` on Hugging Face Jobs, a paid
per-second service. A local-only dataset is pushed to a private Hub repo first. Jobs stop at 48 h unless
`--job.timeout` says otherwise; failed runs leave their model repo behind. Alternatively run in a GPU container
([ops-docker-ci](../../ops-docker-ci/SKILL.md)).

## Licences

| Model | Code | Weights (model card, 2026-11-25) | Gate |
|---|---|---|---|
| ACT, Diffusion Policy | Apache-2.0 (LeRobot) | Your own; ResNet-18 ImageNet weights from torchvision | — |
| SmolVLA | Apache-2.0 | `lerobot/smolvla_base`: Apache-2.0 | — |
| pi0, pi0.5 | Apache-2.0 (LeRobot, openpi) | `lerobot/pi0_base`, `lerobot/pi05_base`: `gemma` (Gemma Terms of Use) | Tokenizer `google/paligemma-3b-pt-224` (manual approval) |
| GR00T N1.7 | Apache-2.0 | NVIDIA Open Model License | Backbone `nvidia/Cosmos-Reason2-2B` (automatic approval) |

LeRobot's pi0 and pi0.5 pages say the model follows Apache 2.0, but the weights' cards declare the Gemma
licence and openpi ships the Gemma terms: read them before redistributing a fine-tune. pi0, pi0.5 and pi0-FAST
all load the gated PaliGemma tokenizer.
