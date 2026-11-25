# Fine-tuning with openpi and Isaac-GR00T

Part of [learn-robot-learning](../SKILL.md). Checked against openpi `main` (215abfb, 2026-08-24): `README.md`,
`docs/remote_inference.md`, `docs/norm_stats.md`, `src/openpi/training/config.py`,
`src/openpi/policies/libero_policy.py`, `pyproject.toml`; and Isaac-GR00T `main` (708617f, 2026-11-17, N1.7):
`README.md`, `getting_started/finetune_new_embodiment.md`, `examples/SO100/`,
`scripts/lerobot_conversion/convert_v3_to_v2.py`. Nothing here was run.

Use these upstream trainers instead of LeRobot's ports ([training.md](training.md)) when you need what only they
offer: openpi's JAX LoRA configs, reloadable pretraining statistics and expert checkpoints (DROID, ALOHA,
LIBERO); GR00T's modality configs, open-loop evaluation, TensorRT path and whole-body (SONIC) workflow.

## The dataset format gap

| Tool | Reads | Note |
|---|---|---|
| LeRobot 0.7 | LeRobotDataset v3.0 | What `lerobot-record` writes |
| openpi | v2.1 | Pins a LeRobot commit from 2025-05-28 (`codebase_version` v2.1) |
| Isaac-GR00T N1.7 | v2.1 plus `meta/modality.json` | Ships a v3.0 to v2.1 converter |

Convert a v3.0 dataset back to v2.1 with GR00T's helper, in its own environment:

```bash
git clone --recurse-submodules https://github.com/NVIDIA/Isaac-GR00T && cd Isaac-GR00T
V21=~/datasets/lerobot_v21                    # a home for v2.1 copies, apart from LeRobot's cache
mkdir -p $V21/my-user && cp -r ~/.cache/huggingface/lerobot/my-user/pick_cube $V21/my-user/
uv run --project scripts/lerobot_conversion python scripts/lerobot_conversion/convert_v3_to_v2.py \
  --repo-id my-user/pick_cube --root $V21
# result: $V21/my-user/pick_cube is v2.1; the v3.0 original moves to $V21/my-user/pick_cube_v30
```

The converter works on `<root>/<repo-id>`, downloading it from the Hub if absent, and converts in place. Without
`--root` that is `$HF_LEROBOT_HOME/<repo-id>`: your LeRobot copy becomes v2.1, which LeRobot 0.7 no longer
reads. Always pass a separate `--root`. openpi finds the copy by repo id when run with `HF_LEROBOT_HOME=$V21`;
GR00T takes the folder path.

## openpi (pi0, pi0-FAST, pi0.5)

Requirements from the README: NVIDIA GPU with more than 8 GB to run, 22.5 GB for LoRA, 70 GB for full
fine-tuning (FSDP across GPUs via `fsdp_devices`); tested on Ubuntu 22.04 only; Python 3.11 managed by uv.
Checkpoints download from `gs://openpi-assets` into `~/.cache/openpi` (`OPENPI_DATA_HOME` to move it).

```bash
git clone --recurse-submodules https://github.com/Physical-Intelligence/openpi && cd openpi
GIT_LFS_SKIP_SMUDGE=1 uv sync
GIT_LFS_SKIP_SMUDGE=1 uv pip install -e .
```

### Add your robot

Three pieces, all modelled on the LIBERO example:

1. **Policy transforms** (`src/openpi/policies/my_robot_policy.py`, copied from `libero_policy.py`):
   `MyRobotInputs` maps your observation to the model's `image` dict (`base_0_rgb`, `left_wrist_0_rgb`,
   `right_wrist_0_rgb`, missing views as zeros with `image_mask` false), `state` and `prompt`;
   `MyRobotOutputs` slices the model's 32-dim action back to your action size (6 for an SO-101).
2. **Data config** (in `src/openpi/training/config.py`, copied from `LeRobotLiberoDataConfig`): the
   `RepackTransform` maps your dataset keys to the names your inputs read, for example
   `"observation/image": "observation.images.top"`, `"observation/wrist_image": "observation.images.wrist"`,
   `"observation/state": "observation.state"`, `"actions": "action"`, `"prompt": "prompt"`.
   pi0 models are trained on delta actions: for absolute joint targets (leader-arm data) add
   `DeltaActions` and `AbsoluteActions` with `_transforms.make_bool_mask(5, -1)` (five joints delta, gripper
   absolute).
3. **Train config**:

```python
TrainConfig(
    name="pi05_my_robot",
    model=pi0_config.Pi0Config(pi05=True, action_horizon=50),
    data=LeRobotMyRobotDataConfig(
        repo_id="my-user/pick_cube",               # the v2.1 copy under $V21
        base_config=DataConfig(prompt_from_task=True),
    ),
    weight_loader=weight_loaders.CheckpointWeightLoader("gs://openpi-assets/checkpoints/pi05_base/params"),
    num_train_steps=30_000,
),
```

LoRA configs upstream exist for pi0 (`pi0_libero_low_mem_finetune`: `paligemma_variant="gemma_2b_lora"`,
`action_expert_variant="gemma_300m_lora"`, the matching `freeze_filter`, `ema_decay=None`) and pi0-FAST. For
pi0-FAST also set `action_dim`, `action_horizon` and `max_token_len` (about 180 for one arm, 250 for two, per the
config comments).

### Statistics, training, serving

```bash
export HF_LEROBOT_HOME=~/datasets/lerobot_v21      # where the v2.1 copies are
uv run scripts/compute_norm_stats.py --config-name pi05_my_robot
XLA_PYTHON_CLIENT_MEM_FRACTION=0.9 uv run scripts/train.py pi05_my_robot --exp-name=run1 --overwrite
uv run scripts/serve_policy.py policy:checkpoint --policy.config=pi05_my_robot \
  --policy.dir=checkpoints/pi05_my_robot/run1/29999       # websocket server on port 8000
```

- Robots in the pretraining mix (ALOHA `trossen`, DROID, Franka, UR5e) can reload pretraining statistics with an
  `AssetsConfig` instead of computing new ones; openpi recommends trying both.
- Loss diverging: look at `q01`, `q99` and `std` in `norm_stats.json`; a rarely used dimension with tiny spread
  blows up after normalisation (openpi troubleshooting).
- PyTorch path: `scripts/train_pytorch.py` after converting the JAX base checkpoint
  (`examples/convert_jax_model_to_pytorch.py`); no pi0-FAST, LoRA, FSDP, EMA or mixed precision there yet, and it
  patches the `transformers` install in the uv cache (undo with `uv cache clean transformers`).

### The robot side

```bash
pip install -e packages/openpi-client      # in the robot's environment: few dependencies
```

```python
from openpi_client import image_tools, websocket_client_policy

client = websocket_client_policy.WebsocketClientPolicy(host="gpu-host.local", port=8000)
obs = {
    "observation/image": image_tools.convert_to_uint8(image_tools.resize_with_pad(top, 224, 224)),
    "observation/wrist_image": image_tools.convert_to_uint8(image_tools.resize_with_pad(wrist, 224, 224)),
    "observation/state": state,              # raw; the server normalises
    "prompt": "pick the cube and put it in the bin",
}
chunk = client.infer(obs)["actions"]         # (action_horizon, action_dim); execute part, then query again
```

Clamp every action to the joint limits and a per-step change before sending it
([evaluation.md](evaluation.md#limits-for-policy-runs)). The websocket has no authentication: keep it on a
trusted network.

## Isaac-GR00T N1.7

Requirements from the README: 16 GB+ GPU to run, 40 GB+ recommended to fine-tune (H100 or L40 suggested);
CUDA 12.8 with Python 3.12 on x86_64; JetPack 7.2 on Jetson Thor and Orin. FFmpeg 4-7 only for its
`torchcodec` 0.8. The backbone `nvidia/Cosmos-Reason2-2B` is gated: request access and log in before the first
run.

```bash
git clone --recurse-submodules https://github.com/NVIDIA/Isaac-GR00T && cd Isaac-GR00T
sudo apt install ffmpeg git-lfs && uv sync --python 3.12
uv run huggingface-cli login
```

### Data and modality config

1. Convert to v2.1 (above), then add `meta/modality.json`: index ranges of each state and action part in the
   concatenated vectors, and the video keys. For an SO-101 recorded by LeRobot (5 joints then the gripper):

```json
{
  "state":  {"single_arm": {"start": 0, "end": 5}, "gripper": {"start": 5, "end": 6}},
  "action": {"single_arm": {"start": 0, "end": 5}, "gripper": {"start": 5, "end": 6}},
  "video":  {"top": {"original_key": "observation.images.top"},
             "wrist": {"original_key": "observation.images.wrist"}},
  "annotation": {"human.task_description": {"original_key": "task_index"}}
}
```

2. A modality config in Python, registered under `EmbodimentTag.NEW_EMBODIMENT`, names the video, state,
   action and language keys and how many future steps to predict, with one `ActionConfig` per action key
   (relative joint actions for the arm, absolute for the gripper in the upstream SO-100 example). Start from
   `examples/SO100/so100_config.py` and change the keys.

### Fine-tune and check offline

```bash
CUDA_VISIBLE_DEVICES=0 uv run python gr00t/experiment/launch_finetune.py \
  --base-model-path nvidia/GR00T-N1.7-3B --dataset-path $V21/my-user/pick_cube \
  --embodiment-tag NEW_EMBODIMENT --modality-config-path my_robot_config.py \
  --num-gpus 1 --output-dir checkpoints/groot_pick_cube --max-steps 10000 \
  --global-batch-size 32 --dataloader-num-workers 4
uv run python gr00t/eval/open_loop_eval.py --dataset-path $V21/my-user/pick_cube \
  --embodiment-tag NEW_EMBODIMENT --model-path checkpoints/groot_pick_cube/checkpoint-10000 \
  --traj-ids 0 --execution-horizon 16 --steps 400
```

- Open-loop evaluation plots predicted against recorded actions. GR00T's guide: predictions should track a
  training episode closely and the error should fall across checkpoints; flat predictions mean the modality keys
  do not match; NaN or huge error points at normalisation.
- `--state_dropout_prob` (fine-tune default 0.2) drops state inputs during training; lower it if the task leans
  on proprioception. Runs vary by 5-6% from non-deterministic augmentation (GR00T README).

### Serve to the robot

```bash
uv run python gr00t/eval/run_gr00t_server.py --model-path checkpoints/groot_pick_cube/checkpoint-10000 \
  --embodiment-tag NEW_EMBODIMENT          # ZMQ on port 5555
```

The SO-100/SO-101 client is `gr00t/eval/real_robot/SO100/eval_so100.py` (its own uv environment, LeRobot robot
flags, `--policy_host`, `--policy_port`, `--lang_instruction`). TensorRT export and Jetson Thor or Orin
deployment are in [learn-edge-deployment](../../learn-edge-deployment/SKILL.md).

## Licences

- openpi code: Apache-2.0. The repository also ships the Gemma Terms of Use (`LICENSE_GEMMA.txt`), and the
  LeRobot copies of the base weights declare the `gemma` licence: the models build on PaliGemma.
- Isaac-GR00T code: Apache-2.0; GR00T N1.7 weights and the Cosmos-Reason2-2B backbone: NVIDIA Open Model License.
- Datasets you fine-tune on carry their own licences (the LIBERO code is MIT; check the LIBERO data, DROID, Open X-Embodiment parts and
  anything from the Hub before shipping a model trained on them).
