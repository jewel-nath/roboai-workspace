# Checking a dataset before training

Part of [learn-robot-learning](../SKILL.md). Checked against LeRobot 0.7.0 and `main` (b07adcc, 2026-11-24):
`docs/source/using_dataset_tools.mdx`, `rename_map.mdx`, `pi05.mdx`, `src/lerobot/scripts/lerobot_edit_dataset.py`,
`lerobot_dataset_viz.py` and `src/lerobot/datasets/dataset_metadata.py`. The script below was not run.

A bad dataset costs a training run and a robot session. Check it in this order and write the results down.

## 1. Watch episodes

```bash
# local dataset: --root is the dataset folder itself
lerobot-dataset-viz --repo-id local/pick_cube --root ~/.cache/huggingface/lerobot/local/pick_cube \
  --mode local --episode-index 0
# Hub dataset: no --root; private ones need `hf auth login`
lerobot-dataset-viz --repo-id ${HF_USER}/pick_cube --episode-index 12
```

It opens Rerun with every camera, `observation.state` and `action` on one timeline (`--display-mode foxglove`
serves it to Foxglove on `ws://127.0.0.1:8765` instead). Hub datasets also open in the browser visualizer at
`https://huggingface.co/spaces/lerobot/visualize_dataset?path=/<repo_id>/episode_0`.

Look at the first, a middle and the last episode, plus any the script below flags:

- Each camera shows the task, in focus, not frozen, not dropping frames.
- The action curves lead the state curves slightly and have the same shape (follower tracking the leader).
- The gripper closes on the object and opens at the end; no episode ends before success.
- Nothing in view that should not be published (people, screens) if the dataset goes to the Hub.

## 2. Run the check script

```python
"""check_dataset.py - sanity checks for a LeRobot v3.0 dataset before training.

python check_dataset.py --repo-id local/pick_cube --expect-cameras top wrist
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from lerobot.datasets import LeRobotDatasetMetadata


def names_of(feature: dict, size: int) -> list[str]:
    names = feature.get("names")
    if isinstance(names, dict):  # some older datasets nest the list
        names = next(iter(names.values()))
    return list(names) if names else [f"dim{i}" for i in range(size)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-id", required=True)
    parser.add_argument("--root", default=None, help="dataset folder (default $HF_LEROBOT_HOME/<repo-id>)")
    parser.add_argument("--expect-cameras", nargs="*", default=[])
    args = parser.parse_args()

    meta = LeRobotDatasetMetadata(args.repo_id, root=args.root)
    print(f"format {meta.info['codebase_version']}  fps {meta.fps}  robot {meta.robot_type}")
    print(f"episodes {meta.total_episodes}  frames {meta.total_frames}  tasks {meta.total_tasks}")

    for key in meta.camera_keys:
        print(f"camera {key}: {meta.features[key]['shape']}")
    for cam in args.expect_cameras:
        if f"observation.images.{cam}" not in meta.camera_keys:
            print(f"ERROR camera '{cam}' missing")

    lengths = np.array(list(meta.episodes["length"]))
    median = float(np.median(lengths))
    print(f"episode length s: min {lengths.min() / meta.fps:.1f}  median {median / meta.fps:.1f}  "
          f"max {lengths.max() / meta.fps:.1f}")
    for ep in np.where((lengths < 0.5 * median) | (lengths > 1.5 * median))[0]:
        print(f"WARN episode {ep}: {lengths[ep]} frames (median {median:.0f})")

    data = pd.read_parquet(Path(meta.root) / "data", columns=["episode_index", "observation.state", "action"])
    for key in ("observation.state", "action"):
        arr = np.stack(data[key].to_numpy()).astype(np.float64)
        span = arr.max(0) - arr.min(0)
        for i, name in enumerate(names_of(meta.features[key], arr.shape[1])):
            at_edge = np.mean(np.isclose(arr[:, i], arr[:, i].min()) | np.isclose(arr[:, i], arr[:, i].max()))
            note = ""
            if span[i] < 1e-3:
                note = "  <- constant: breaks normalisation"
            elif at_edge > 0.2:
                note = f"  <- {at_edge:.0%} of frames at an extreme: clipped or saturated?"
            print(f"{key:18s} {name:20s} min {arr[:, i].min():9.3f} max {arr[:, i].max():9.3f} "
                  f"std {arr[:, i].std():8.3f}{note}")

    # largest step between consecutive actions per episode: teleop glitches, dropped frames
    actions = np.stack(data["action"].to_numpy())
    jumps = []
    for ep, rows in data.groupby("episode_index").indices.items():
        if len(rows) > 1:
            jumps.append((float(np.abs(np.diff(actions[rows], axis=0)).max()), int(ep)))
    for jump, ep in sorted(jumps, reverse=True)[:3]:
        print(f"largest action step: episode {ep}: {jump:.2f}")

    stats = meta.stats.get("action", {})
    print("quantile stats (needed by pi0.5):", "yes" if "q01" in stats else "no")


if __name__ == "__main__":
    main()
```

What to do with the output:

| Finding | Likely cause | Action |
|---|---|---|
| A camera missing or a different shape than deployment | Camera config changed | Re-record, or retrain with the deployment config |
| `fps` not what you meant | Wrong `--dataset.fps` | Record again; never relabel the rate |
| Episode far shorter or longer than the median | Aborted, hesitant or failed demonstration | Watch it; delete if bad |
| Constant dimension | Unused joint, disconnected sensor | Fix the hardware or remove the dimension consistently in training and deployment |
| Many frames at an extreme | Joint at its limit, gripper squeezing an object, calibration offset | Usually fine for the gripper; for other joints, check calibration and limits |
| Large action step in one episode | Teleop glitch, bus error, dropped frames | Watch it; delete if the robot jumped |
| Gripper range far smaller than the motor range | Leader gripper calibrated differently | Recalibrate the leader; re-record |

## 3. Edit the dataset

`lerobot-edit-dataset` reads `$HF_LEROBOT_HOME/<repo_id>` unless `--root` says otherwise, and writes to
`$HF_LEROBOT_HOME/<new_repo_id>` (or `--new_root`). Without `--new_repo_id` it edits in place and moves the
original to `<name>_old`; a second in-place edit deletes that backup first, so use a new repo id for anything you
may want back. `--push_to_hub=true` uploads the result.

```bash
# remove bad episodes into a new dataset (indices are renumbered afterwards)
lerobot-edit-dataset --repo_id local/pick_cube --new_repo_id local/pick_cube_clean \
  --operation.type delete_episodes --operation.episode_indices "[3, 17, 41]"
# summary, with feature details
lerobot-edit-dataset --repo_id local/pick_cube_clean --operation.type info --operation.show_features true
# held-out split by episode (or train with --dataset.eval_split instead)
lerobot-edit-dataset --repo_id local/pick_cube_clean --operation.type split \
  --operation.splits '{"train": 0.9, "val": 0.1}'
# merge sessions recorded separately (identical features required)
lerobot-edit-dataset --new_repo_id local/pick_cube_all --operation.type merge \
  --operation.repo_ids "['local/pick_cube_day1', 'local/pick_cube_day2']"
# fix the task text
lerobot-edit-dataset --repo_id local/pick_cube_clean --operation.type modify_tasks \
  --operation.new_task "Pick the red cube and put it in the bin"
# drop a camera you will not have at deployment
lerobot-edit-dataset --repo_id local/pick_cube_clean --new_repo_id local/pick_cube_top \
  --operation.type remove_feature --operation.feature_names "['observation.images.wrist']"
# statistics again (pi0.5 quantiles, or relative actions for pi0/pi0.5/GR00T)
lerobot-edit-dataset --repo_id local/pick_cube_clean --new_repo_id local/pick_cube_clean \
  --operation.type recompute_stats --operation.overwrite true
```

- After `delete_episodes`, episode indices change: re-run the check script before quoting any index.
- `recompute_stats` writes to `$HF_LEROBOT_HOME/<new_repo_id>`, not to the Hub cache a downloaded dataset is read
  from; train with `--dataset.root` pointing there, or push the result (LeRobot pi0.5 docs).
- Statistics merged during recording or `merge` hold a conservative envelope of per-episode quantiles, not
  whole-dataset quantiles; `src/lerobot/scripts/augment_dataset_quantile_stats.py` estimates the latter.
- Relative actions: `--operation.relative_action true --operation.chunk_size 50
  --operation.relative_exclude_joints "['gripper']"`, with `chunk_size` equal to the policy's.

## 4. Match keys to the policy

- ACT and Diffusion Policy build their inputs from the dataset's own keys: any camera names work, but deployment
  must use the same ones.
- Pretrained VLAs have fixed input names. `--rename_map='{"observation.images.top": "observation.images.camera1"}'`
  renames observation keys (not actions) inside the preprocessor; LeRobot supports it for pi0, pi0.5,
  pi0-FAST, SmolVLA and X-VLA. Pass the same map at training and at rollout.
- A policy expecting more cameras than you have: `--policy.empty_cameras=N` (pi0, pi0.5) adds blank inputs.

## 5. Replay before training

`lerobot-replay --dataset.episode=<n>` on the robot ([lerobot-recording.md](lerobot-recording.md#replay-an-episode-on-the-robot))
proves the actions still mean the same thing on today's robot and calibration.
