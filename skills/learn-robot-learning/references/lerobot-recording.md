# Recording demonstrations with LeRobot

Part of [learn-robot-learning](../SKILL.md). Checked against LeRobot 0.7.0 and `main` (b07adcc, 2026-11-24):
`docs/source/il_robots.mdx`, `so101.mdx`, `cameras.mdx`, `lerobot-dataset-v3.mdx`, `src/lerobot/configs/dataset.py`
and `src/lerobot/robots/so_follower/`. Nothing here was run on hardware.

LeRobot is not a ROS package. It drives the motors and cameras itself (Feetech and Dynamixel buses, OpenCV and
RealSense cameras) through `Robot` and `Teleoperator` classes. For a robot that only speaks ROS 2, see
[ros2.md](ros2.md).

## Install

```bash
python3.12 -m venv ~/venvs/lerobot && source ~/venvs/lerobot/bin/activate
pip install 'lerobot[core_scripts,feetech,training]'    # core_scripts = dataset + hardware + viz
# Dynamixel arms (Koch): 'lerobot[dynamixel]'; RealSense: 'lerobot[intelrealsense]'
```

LeRobot 0.7 needs Python 3.12 or 3.13 and numpy 2. Keep it out of the ROS 2 interpreter
([ros2.md](ros2.md#why-separate-processes)). On Linux, add your user to `dialout` for the serial ports (the
docs' `chmod 666 /dev/ttyACM0` is lost at every replug).

## Set up an SO-101 pair

| Step | Command | Notes |
|---|---|---|
| Find each arm's port | `lerobot-find-port` | Unplug the arm when asked; it prints the port that vanished |
| Set motor ids and baud rate (new motors only) | `lerobot-setup-motors --robot.type=so101_follower --robot.port=/dev/ttyACM0` | One motor connected at a time, as prompted; repeat with `--teleop.type=so101_leader` |
| Calibrate | `lerobot-calibrate --robot.type=so101_follower --robot.port=/dev/ttyACM0 --robot.id=robot-01` | Joints near mid-range first; repeat for the leader with `--teleop.*` |
| Find cameras | `lerobot-find-cameras opencv` (or `realsense`) | Saves test frames to `outputs/captured_images` |
| Teleoperate | `lerobot-teleoperate ... --display_data=true` | Same ids as calibration |

- Calibration files live under `$HF_LEROBOT_CALIBRATION` (default `~/.cache/huggingface/lerobot/calibration`),
  keyed by robot type and `id`. Every later command must use the same `--robot.id` and `--teleop.id`.
- `use_degrees: true` (default) reports body joints in degrees; the gripper is a 0-100 range. Joint names:
  `shoulder_pan`, `shoulder_lift`, `elbow_flex`, `wrist_flex`, `wrist_roll`, `gripper` (each with `.pos`).
- `max_relative_target` (float, or a dict per motor) clips each command to that distance from the present
  position. It reads the motors every step, so the loop runs a little slower. Leave it off for teleoperation
  (the leader already limits you), set it for policy runs.
- `disable_torque_on_disconnect: true` (default): the arm goes limp when the script ends. Support the arm or
  park it before stopping.
- Other teleoperators: `keyboard`, `gamepad`, `phone`, Koch and OpenArm leaders, bimanual `bi_so_leader`.

## Cameras

```bash
CAMS='{ top: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}, wrist: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}}'
```

- The names become dataset keys `observation.images.top` and `observation.images.wrist`; a policy expects the
  same names and resolution at deployment.
- Use `/dev/v4l/by-id/...` paths for `index_or_path`, or udev rules, so indices do not swap after a reboot
  ([perception-camera](../../perception-camera/SKILL.md)). Add `fourcc: "MJPG"` when two USB cameras at
  640x480 30 fps exceed the USB bandwidth.
- Fix the cameras rigidly. Moving a camera between recording and deployment is a distribution shift.
- Depth: RealSense with `use_depth: true` records a separate depth video stream (LeRobot cheat sheet).

## Record

```bash
lerobot-record \
  --robot.type=so101_follower --robot.port=/dev/ttyACM0 --robot.id=robot-01 --robot.cameras="$CAMS" \
  --teleop.type=so101_leader --teleop.port=/dev/ttyACM1 --teleop.id=robot-01-leader \
  --display_data=true \
  --dataset.repo_id=${HF_USER}/pick_cube --dataset.single_task="Pick the cube and put it in the bin" \
  --dataset.fps=30 --dataset.num_episodes=50 --dataset.episode_time_s=30 --dataset.reset_time_s=15 \
  --dataset.streaming_encoding=true --dataset.encoder_threads=2 \
  --dataset.push_to_hub=false --dataset.private=true
```

| Flag | Default | Meaning |
|---|---|---|
| `--dataset.repo_id` | required | `user/name`; also the folder under `$HF_LEROBOT_HOME` (default `~/.cache/huggingface/lerobot`) |
| `--dataset.no_stamp` | `false` | Without it, `_YYYYMMDD_HHMMSS` is appended to the repo id |
| `--dataset.root` | `$HF_LEROBOT_HOME/repo_id` | Store elsewhere (needed when resuming) |
| `--dataset.single_task` | required | The task text; language-conditioned policies read it |
| `--dataset.fps` | 30 | Loop rate and the rate written to the dataset |
| `--dataset.episode_time_s` / `reset_time_s` | 60 / 60 | Episode and reset durations |
| `--dataset.num_episodes` | 50 | On resume: the number of *additional* episodes |
| `--dataset.video` | `true` | Encode cameras to MP4 (otherwise PNG images) |
| `--dataset.streaming_encoding` | `false` | Encode while recording; `save_episode()` returns at once |
| `--dataset.push_to_hub` | `true` | Upload at the end; `--dataset.private=true` for a private repo |
| `--resume` | `false` | Continue a dataset; pass the full stamped repo id and `--dataset.root` |
| `--display_mode` | `rerun` | Or `foxglove` (WebSocket on port 8765) |

Keys while recording (terminal focused; X11, Wayland or SSH): right arrow or `n` ends the episode or reset early;
left arrow or `r` discards and re-records the episode; `Esc` or `q` stops, encodes and (if enabled) uploads.

### Local only, or the Hub

- Local: `--dataset.push_to_hub=false`. Everything is in `~/.cache/huggingface/lerobot/<repo_id>`; training finds
  it there by repo id. Back it up: the cache is easy to wipe.
- Hub: `hf auth login` with a write token first. Upload later with
  `hf upload <repo_id> ~/.cache/huggingface/lerobot/<repo_id> --repo-type dataset`. Datasets are public unless
  `--dataset.private=true`; check what the cameras saw (faces, screens, documents) before pushing.

## Read the cadence report

After each episode and at the end, `lerobot-record` prints the achieved rate, the ticks over budget and which loop
step (observe, teleop, send, record) took the time. A frame's timestamp is its index divided by `fps`, so a session
that really ran at 25 Hz still claims 30 Hz and the motion replays fast. If the effective rate is more than a few
percent low: reduce camera resolution or count, use MJPG, turn on streaming encoding, close the Rerun viewer
(`--display_data=false`), or lower `--dataset.fps` for every later step too.

## Dataset layout (v3.0)

```
<root>/
  meta/info.json          # features, shapes, dtypes, fps, codebase_version "v3.0", path templates
  meta/stats.json         # per-feature min/max/mean/std (and quantiles when computed)
  meta/tasks.parquet      # task strings and their indices
  meta/episodes/chunk-000/file-000.parquet   # per-episode length, task, offsets into shared files
  data/chunk-000/file-000.parquet            # frames of many episodes: observation.state, action, indices
  videos/observation.images.top/chunk-000/file-000.mp4
```

- `observation.state` is the follower's measured joint positions; `action` is the command sent (the leader's
  positions in leader-follower teleoperation). Both are ordered by the feature's `names`.
- v3.0 packs many episodes per file; episode boundaries live in `meta/episodes`. Do not edit files by hand: use
  `lerobot-edit-dataset` ([dataset-checks.md](dataset-checks.md)).
- Older v2.1 datasets: `python -m lerobot.scripts.convert_dataset_v21_to_v30 --repo-id=<user/name>`.

## How to collect useful demonstrations

Mostly from the LeRobot recording guide and the SmolVLA docs:

- Start with one task and about 50 episodes; LeRobot suggests 10 episodes per object position. The SmolVLA team
  reports 25 episodes over 5 positions was not enough for their cube task, while 50 worked.
- Keep one strategy (the same grasp, the same approach side). Mixed strategies need a multimodal policy
  (Diffusion Policy, a VLA) and more data.
- The object must be visible to the cameras; a rule of thumb from LeRobot: you should be able to do the task
  watching only the camera images.
- Move smoothly at a speed the robot can hold; pauses and hesitations are learned too.
- Add variation step by step (positions, then lighting and distractors, then new objects) once the simple version
  works.
- Discard failed attempts with left arrow at once, rather than cleaning up later.
- Record a few recovery demonstrations: start from slightly wrong poses and complete the task.

## Replay an episode on the robot

```bash
lerobot-replay --robot.type=so101_follower --robot.port=/dev/ttyACM0 --robot.id=robot-01 \
  --dataset.repo_id=${HF_USER}/pick_cube --dataset.episode=0
```

It sends the recorded actions open loop. If the replay misses the object, the robot or calibration changed since
recording, or the cadence was off; fix that before training.

## Your own hardware in LeRobot

Write a `Robot` (and if needed a `Teleoperator`) subclass with its config, as `docs/source/integrate_hardware.mdx`
describes, or install a third-party plugin from `docs/source/third_party_robots.mdx`. Then all `lerobot-*`
commands work with `--robot.type=<yours>`.
