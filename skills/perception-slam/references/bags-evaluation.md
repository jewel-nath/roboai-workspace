# Bags for SLAM, and judging the result with evo

Part of [perception-slam](../SKILL.md). Checked against rosbag2 0.26 (`jazzy` branch: README and the
`ros2 bag record` / `play` verbs), the Jazzy QoS-override guide, and evo `master` (CLI parsers and file
readers). Datasets with ground truth: [KITTI](../../../wiki/learning/datasets/kitti.md) and
[TUM RGB-D](../../../wiki/learning/datasets/tum-rgbd.md).

## Record

Record the inputs, not the outputs you want to tune. Run only the drivers, `robot_state_publisher` and the
odometry source while recording; no SLAM, no global filter.

```bash
ros2 bag record -o run1 --topics \
  /scan /points /imu/data_raw /imu/data /diff_drive_controller/odom /joint_states \
  /camera/color/image_raw /camera/color/camera_info /camera/aligned_depth_to_color/image_raw \
  /gps/fix /tf /tf_static /robot_description
ros2 bag info run1                       # message counts and rates per topic
```

- Always include `/tf_static`. rosbag2 records and replays the publishers' QoS, so the transient-local
  static transforms reach nodes that start after playback begins.
- Jazzy writes MCAP by default (`-s sqlite3` for the old format). Split long runs with `-b <bytes>` or
  `-d <seconds>`; MCAP compression is set in a `--storage-config-file`.
- Images dominate size. Record compressed image topics if the SLAM node can decompress them (RTAB-Map:
  `compressed:=true` in `rtabmap.launch.py`); the transport setup is in
  [perception-camera](../../perception-camera/SKILL.md).
- In simulation add `/clock` and record with `--use-sim-time`.
- A topic missing from `ros2 bag info` was not published, or its QoS did not match; check with
  `ros2 topic info -v`.

## Replay

```bash
ros2 bag play run1 --clock               # publishes /clock from the bag's time (40 Hz by default)
```

- Every node in the replay runs with `use_sim_time: true`, RViz included. Start them first, or play with
  `--start-paused` and press space in the player's terminal (in a script:
  `ros2 service call /rosbag2_player/resume rosbag2_interfaces/srv/Resume`).
- Re-tuning SLAM on top of recorded odometry: play everything; the bag's `/tf` holds `odom` → `base_link`.
- Re-tuning the EKF as well: keep the recorded TF out with `--remap /tf:=/tf_recorded`, and run
  `robot_state_publisher` (from `/robot_description` and `/joint_states`) and the EKF live. `/tf_static`
  still plays.
- Leave out topics with `--exclude-topics /map /odometry/filtered`; slow down with `--rate 0.5` when the
  SLAM node falls behind (or use slam_toolbox's synchronous mode).
- robot_localization: `reset_on_time_jump: true` resets the filter when a bag loops (`--loop`).
- Same bag, same parameters, same result: change one thing per replay and keep a note of it.

## evo

evo (GPL-3.0, a developer tool) computes trajectory errors. Ubuntu 24.04 blocks system-wide `pip`, so use a
virtual environment:

```bash
python3 -m venv ~/.venvs/evo && ~/.venvs/evo/bin/pip install evo
export PATH="$HOME/.venvs/evo/bin:$PATH"
```

It reads ROS 1 and ROS 2 bags (including MCAP) without ROS through the `rosbags` library, except `/tf`,
which needs a sourced ROS install. Supported message types: `nav_msgs/Odometry`,
`geometry_msgs/PoseStamped`, `PoseWithCovarianceStamped`, `TransformStamped`, `PointStamped`.

### Formats

| Format | Line | Notes |
|---|---|---|
| TUM | `timestamp tx ty tz qx qy qz qw` (8 values, space-separated) | Timestamps let evo associate poses by time |
| KITTI | 12 values: the first three rows of the 4x4 pose, row-major | No timestamps: line *i* of both files must be the same instant |
| EuRoC | ground-truth CSV `state_groundtruth_estimate0/data.csv` | Estimate in TUM format |
| bag2 | topics in a ROS 2 bag | `evo_* bag2 <bag> <ref_topic> <est_topic>` |

```bash
# Extract trajectories from a replay bag that recorded the outputs
evo_traj bag2 run1_out /odometry/filtered /rtabmap/localization_pose --save_as_tum
evo_traj bag2 run1_out /tf:map.base_link --save_as_tum            # needs ROS sourced
evo_traj tum est.tum --ref gt.tum -p --plot_mode xy -a
```

### APE (ATE) and RPE

- **APE** (absolute pose error; ATE when it is the translation part): the estimate is aligned to the
  reference once, then compared pose by pose. It measures global consistency: did loop closure work?
- **RPE** (relative pose error): the error of the motion over a fixed step (frames, metres or degrees).
  It measures local drift, independent of where the run started.

```bash
evo_ape tum gt.tum est.tum -a -p --save_results results/est_ape.zip            # -r trans_part by default
evo_ape tum gt.tum est.tum -a -r rot_part                                      # rotation only
evo_rpe tum gt.tum est.tum -a -d 1 -u m -p --save_results results/est_rpe.zip  # per metre travelled
evo_res results/*_ape.zip -p                                                   # compare runs
evo_ape kitti gt_kitti.txt est_kitti.txt -a                                    # KITTI files
```

| Option | Use |
|---|---|
| `-a` / `--align` | Umeyama SE(3) alignment, needed when the estimate's origin differs from the reference |
| `-s` / `--correct_scale` | Also fit scale: monocular VO and VIO before scale converges |
| `--align_origin` | Align only the first pose (instead of `-a`) |
| `--n_to_align N` | Align on the first N poses only, to show drift after alignment |
| `--t_max_diff`, `--t_offset` | Association tolerance (default 0.01 s) and a constant clock offset |
| `--project_to_plane xy` | Planar robots |
| `-d`, `-u f/m/d/r`, `--all_pairs` | RPE step and its unit |

- Without ground truth: compare against a reference run (motion capture, RTK GNSS, or a well-closed
  slam_toolbox map), or report the end-point error of a run that returns to its start.
- KITTI's leaderboard uses its own segment-based metric from its devkit; evo's RPE is a different number.
  Name the metric and its options whenever you report one.
- Save the evo command, the bag name and the parameter files with every reported number.
