# Recording bags on robots and collecting them

Part of [ops-fleet](../SKILL.md). Robots record what is needed to explain a failure, keep the disk
from filling, and send finished files home. Checked against `rosbag2` 0.26.11 (`jazzy` branch:
`ros2bag/verb/record.py`, `sequential_writer.cpp`, the MCAP storage README) on 2026-11-25.

## What to record

On Jazzy the default storage is MCAP. Record the robot's state and decisions, not raw sensor
floods:

| Keep | Usually skip or throttle |
|---|---|
| `/tf`, `/tf_static`, `/odom`, `/joint_states`, `/cmd_vel` | raw images and point clouds at full rate |
| `/scan` (small), `/diagnostics_agg`, `/rosout` | depth images; use compressed topics at a low rate |
| goals, plans and states of your task logic | anything you would not open when debugging |

`/rosout` carries every node's log lines, so a bag can be read without the journal.

## Always-on recording, split into files

```bash
ros2 bag record \
  --topics /tf /tf_static /odom /joint_states /cmd_vel /scan /diagnostics_agg /rosout \
  -o /var/lib/my_robot/bags/$(date +%Y%m%d-%H%M%S) \
  --max-bag-duration 600 \
  --storage-preset-profile zstd_fast \
  --custom-data robot=robot-01 release=1.4.0 \
  --disable-keyboard-controls
```

- `--max-bag-duration` (seconds) or `--max-bag-size` (bytes) start a new file inside the bag folder;
  600 s is an example. The output folder must not exist yet, hence the timestamp.
- `--storage-preset-profile`: `zstd_fast` compresses chunks cheaply; `fastwrite` uses the least
  CPU but writes no message index, so convert those files afterwards before keeping them.
- `--custom-data` stores key=value pairs in the bag's metadata; put the robot and the release
  there, so a file found later still says where it came from.
- Run it as its own service, modelled on the robot unit in
  [ops-bringup](../../ops-bringup/SKILL.md), with `--disable-keyboard-controls`, since there is no
  terminal.
- Positional topics (`ros2 bag record /odom /scan`) are deprecated in Jazzy and removed in Lyrical;
  use `--topics`.

## Snapshot mode: keep the last minutes, write on demand

```bash
ros2 bag record --topics /tf /tf_static /odom /scan /cmd_vel /rosout \
  -o /var/lib/my_robot/bags/snapshots-$(date +%Y%m%d-%H%M%S) \
  --snapshot-mode --max-cache-size 268435456 --disable-keyboard-controls
# when something goes wrong (a diagnostics ERROR, an operator button, a failed goal):
ros2 service call /rosbag2_recorder/snapshot rosbag2_interfaces/srv/Snapshot
```

Messages stay in a circular buffer in memory (`--max-cache-size` bytes; 256 MiB here is an
example, and up to twice that is used) and reach disk only when the service is called; each call
writes the buffer and starts a new file. A node that calls the service when
`/diagnostics_toplevel_state` turns ERROR gives a recording of every incident with almost no disk
use.

## Finished files, quota and upload

- **A bag folder gets its `metadata.yaml` only when recording stops.** After a power cut the
  folder has none; `ros2 bag reindex <folder>` rebuilds it. The split `.mcap` files themselves
  are complete once closed and open in any MCAP tool.
- **Split files are closed when the next one starts**: everything but the newest file in the
  active folder is safe to move.
- **`/tf_static` is written once**, into the first file. A later split file opened alone has no
  static transforms; Lyrical adds `--repeat-transient-local` for this. On Jazzy, always keep and
  upload the first file of a bag together with the later ones.
- **Quota.** Jazzy has no file-count limit (Lyrical adds `--max-bag-files`). Delete the oldest
  bags while the bag disk is too full, never the newest:

  ```bash
  #!/usr/bin/env bash
  # /usr/local/bin/my-robot-bag-quota - run from a systemd timer, e.g. every 10 minutes
  set -euo pipefail
  dir=/var/lib/my_robot/bags
  limit_pct=80                                   # example; leave room for the OS and logs
  while [ "$(df --output=pcent "$dir" | tail -1 | tr -dc '0-9')" -gt "$limit_pct" ]; do
    oldest=$(ls -1dt "$dir"/*/ 2>/dev/null | tail -n +2 | tail -1)   # skip the newest folder
    [ -n "$oldest" ] || break
    rm -rf -- "$oldest"
  done
  ```

  Put bags on their own partition or disk so a full bag disk cannot stop the OS, and point
  `hd_monitor` at it ([health.md](health.md)).
- **Upload** closed files over the VPN to storage you own, for example with rclone (MIT) to an
  S3-compatible bucket, moving only files untouched for a few minutes:

  ```bash
  rclone move /var/lib/my_robot/bags fleet:bags/robot-01 \
    --min-age 5m --include "*.mcap" --include "metadata.yaml" --delete-empty-src-dirs
  ```

  Upload on a timer and when docked or on a cheap network; limit bandwidth (`--bwlimit`) on LTE.

## Foxglove's device agent

Foxglove's agent (Foxlet, formerly Foxglove Agent; `.deb`, binary or Docker image, amd64 and
arm64) watches a folder (`STORAGE_ROOT`; set `WATCH_INCLUDE_SUFFIXES=.mcap`) and imports
recordings into Foxglove's cloud, by hand or by pattern. Terms to know before using it:

- Each robot is a Foxglove device with its own token, and devices count against the plan: the
  Free plan allows 5 devices; Pro charges per device beyond 5
  ([Foxglove](../../../wiki/tools/foxglove.md) has the plan table). The app is closed source.
- Recordings go to Foxglove's hosted storage unless you have a self-hosted (Enterprise) site.
- It needs outbound HTTPS to `api.foxglove.dev`.

To stay on open tools, upload with rclone and open MCAP files in Lichtblick (MPL-2.0) or
PlotJuggler; [Rerun](../../../wiki/tools/rerun.md) is another open viewer.

## Checks

- `ros2 bag info <folder>` on a finished bag lists the topics with message counts, and the custom
  data shows the robot and release.
- A forced snapshot (`ros2 service call .../snapshot`) produces a new file with the last minutes.
- Filling a test partition triggers the quota script before `hd_monitor` reports ERROR.
- Uploaded files appear in the bucket under the robot's name and are gone from the robot.
