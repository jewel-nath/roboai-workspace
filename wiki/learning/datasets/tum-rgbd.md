---
type: tool
name: TUM RGB-D
summary: The standard indoor RGB-D SLAM benchmark from TU Munich, Kinect colour and depth at 30 Hz with motion-capture ground truth, 47 sequences with public ground truth; data under CC BY 4.0, and its TUM trajectory format is what evo and most SLAM tools read.
tags: [tum-rgbd, dataset, benchmark, rgbd, slam, visual-odometry, kinect, ground-truth, ate, rpe, evo, tum-format]
kind: dataset
area: perception
support:
license: CC-BY-4.0
links: {repo: , docs: "https://cvg.cit.tum.de/data/datasets/rgbd-dataset/file_formats", site: "https://cvg.cit.tum.de/data/datasets/rgbd-dataset"}
version: {tested: , latest: , as_of: 2026-11-23}
platforms: []
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://cvg.cit.tum.de/data/datasets/rgbd-dataset", title: "TUM RGB-D SLAM Dataset and Benchmark: overview and licence", accessed: 2026-11-23}
  - {url: "https://cvg.cit.tum.de/data/datasets/rgbd-dataset/file_formats", title: "TUM RGB-D: file formats and intrinsic calibration", accessed: 2026-11-23}
  - {url: "https://cvg.cit.tum.de/data/datasets/rgbd-dataset/download", title: "TUM RGB-D: dataset download (sequence list and sizes)", accessed: 2026-11-23}
  - {url: "https://cvg.cit.tum.de/data/datasets/rgbd-dataset/tools", title: "TUM RGB-D: useful tools (associate, ATE, RPE, point clouds)", accessed: 2026-11-23}
  - {url: "https://github.com/MichaelGrupp/evo", title: "evo repository: README, LICENSE and APE/RPE options", accessed: 2026-11-23}
  - {url: "https://pypi.org/project/rosbags/", title: "PyPI: rosbags (rosbag1 to rosbag2 converter)", accessed: 2026-11-23}
---

# TUM RGB-D

TU Munich's RGB-D SLAM benchmark: colour and depth from a Microsoft Kinect at 30 Hz and 640 x 480,
the Kinect's accelerometer, and camera poses from an eight-camera motion-capture system at 100 Hz
[1]. Builders use it to check an RGB-D or visual SLAM setup against ground truth before trusting
it indoors. Data is CC BY 4.0 and the benchmark code BSD-2-Clause, so commercial use is allowed
with attribution; it came with Sturm et al.'s IROS 2012 paper [1].

## When to use it

- Indoor RGB-D or monocular SLAM and visual odometry: hand-held, robot-mounted, and scenes with
  people moving [3].
- Outdoor driving: [KITTI](kitti.md). Visual-inertial work needs a full IMU; this has only the
  Kinect's accelerometer [1].

## How an agent works with it

- **Sequences** [3]: 47 with public ground truth, in six groups: Testing and Debugging (4,
  `freiburg1_xyz`, ...), Handheld SLAM (11), Robot SLAM (4), Structure vs. Texture (8), Dynamic
  Objects (9, `freiburg3_walking_*`) and 3D Object Reconstruction (11). 33 `*_validation`
  sequences have no public ground truth and are scored online; 9 are calibration sets. Archives
  are about 0.2 to 2.8 GB.
- **Files** [2]: a TGZ (and a ROS 1 bag) per sequence, with 8-bit colour PNGs and 16-bit depth
  PNGs registered pixel for pixel, and ground truth as `timestamp tx ty tz qx qy qz qw` lines
  (Unix seconds; the colour camera's optical centre in the motion-capture frame). The site
  advises ROS default intrinsics (fx = fy = 525, cx = 319.5, cy = 239.5) or its per-camera values.

```bash
B=https://cvg.cit.tum.de/rgbd/dataset/freiburg1/rgbd_dataset_freiburg1_xyz
wget $B.tgz $B-groundtruth.txt && tar xzf rgbd_dataset_freiburg1_xyz.tgz   # 0.45 GB
# run your SLAM on it and save its path in TUM format as est.txt, then:
pipx install evo
evo_ape tum rgbd_dataset_freiburg1_xyz-groundtruth.txt est.txt -va --align --plot
evo_rpe tum rgbd_dataset_freiburg1_xyz-groundtruth.txt est.txt -va --align -d 1 -u m
```

ATE, after alignment, measures global accuracy; RPE per metre or second measures drift [4].
Monocular SLAM also needs `--correct_scale`; evo is GPL-3.0 and needs Python 3.11+ [5].

## Traps

- **Depth scale is 5000, not 1000.** 5000 is 1 m and 0 means no data [2]; a reader set for
  millimetre cameras puts the world five times too far away.
- **Colour and depth are not synchronised.** Pair frames by timestamp: the TUM tools allow
  0.02 s [4], evo's default `--t_max_diff` is 0.01 s [5]; too tight drops pairs.
- **w comes last.** Quaternions are `qx qy qz qw`, for the colour camera, not a robot base [2].
- **The bags are ROS 1** (ROS Diamondback) [2]: `rosbags-convert file.bag` (Apache-2.0,
  0.11.10) writes a ROS 2 bag [6], or use the TGZ files.
- **The original scripts' links are dead.** `associate.py` and `evaluate_ate.py` sit on an SVN
  server that returned 404 on 2026-11-19 and 2026-11-23 [4]; evo computes both metrics [5].

## Alternatives

[KITTI](kitti.md); to test: [ORB-SLAM3](../../software/orb-slam3.md),
[RTAB-Map](../../software/rtab-map.md); plots: [Rerun](../../tools/rerun.md), fed by evo [5].
See [Choose a SLAM system](../../guides/choose-a-slam-system.md).

## Sources

1. [TUM RGB-D SLAM Dataset and Benchmark: overview and licence](https://cvg.cit.tum.de/data/datasets/rgbd-dataset), accessed 2026-11-23
2. [TUM RGB-D: file formats and intrinsic calibration](https://cvg.cit.tum.de/data/datasets/rgbd-dataset/file_formats), accessed 2026-11-23
3. [TUM RGB-D: dataset download (sequence list and sizes)](https://cvg.cit.tum.de/data/datasets/rgbd-dataset/download), accessed 2026-11-23
4. [TUM RGB-D: useful tools (associate, ATE, RPE, point clouds)](https://cvg.cit.tum.de/data/datasets/rgbd-dataset/tools), accessed 2026-11-23
5. [evo repository: README, LICENSE and APE/RPE options](https://github.com/MichaelGrupp/evo), accessed 2026-11-23
6. [PyPI: rosbags (rosbag1 to rosbag2 converter)](https://pypi.org/project/rosbags/), accessed 2026-11-23
