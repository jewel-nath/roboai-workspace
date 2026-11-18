---
type: robot
name: UMI gripper (Universal Manipulation Interface)
summary: Hand-held, 3D-printed parallel-jaw gripper with a GoPro as its only sensor, for collecting robot-free demonstrations that train policies for real arms; about $371 in parts, MIT-licensed code, CAD published without a licence.
tags: [data-collection, hand-held, gopro, diffusion-policy, orb-slam3, imitation-learning, 3d-printed, umi]
category: gripper
tier: B
openness: partial
maker: Stanford University, Columbia University and Toyota Research Institute (Chi et al.)
year: 2024
license: {hardware: , software: MIT, docs: }
links: {repo: "https://github.com/real-stanford/universal_manipulation_interface", docs: "https://docs.google.com/document/d/1TPYwV9sNVPAi0ZlAupDMkXZ4CA1hsZx7YDMSmcEy6EU/edit", cad: "https://cad.onshape.com/documents/a8a98201374f5cc9c6538790", paper: "https://arxiv.org/abs/2402.10329", site: "https://umi-gripper.github.io/"}
specs: {dof: 1, payload_kg: , reach_mm: , mass_kg: 0.78, size_mm: "310 x 175 x 210", speed_mps: , runtime_h: }
stack: {actuators: "none; a hand trigger drives both fingers through printed gears and linkages on two MGN9C linear rails", mcu: "none", compute: "offline workstation for SLAM and training; RTX 3090 24 GB tested for training", sensors: ["GoPro Hero 9 with Max Lens Mod 1.0 (155° fisheye)", "GoPro built-in IMU", "two side mirrors for implicit stereo", "printed ArUco tags for gripper width"], sim_models: ["MJCF (MuJoCo Menagerie, umi_gripper)"], ros2: none}
cost: {type: bom, usd: 371, as_of: 2024-03-06, source: "https://arxiv.org/abs/2402.10329"}
build: {difficulty: 2, hours: , print_hours: }
maturity: {last_commit: 2026-05-26, stars: 1645, active: true}
use_cases: [data-collection, imitation-learning, manipulation, research]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://arxiv.org/abs/2402.10329", title: "Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots (arXiv v3, 2024-03-06)", accessed: 2026-11-18}
  - {url: "https://umi-gripper.github.io/", title: UMI project page, accessed: 2026-11-18}
  - {url: "https://docs.google.com/document/d/1TPYwV9sNVPAi0ZlAupDMkXZ4CA1hsZx7YDMSmcEy6EU/edit", title: UMI hardware building guide, accessed: 2026-11-18}
  - {url: "https://github.com/real-stanford/universal_manipulation_interface", title: UMI repository README, accessed: 2026-11-18}
  - {url: "https://github.com/real-stanford/universal_manipulation_interface/blob/main/franka_instruction.md", title: UMI Franka deployment instructions, accessed: 2026-11-18}
  - {url: "https://github.com/cheng-chi/ORB_SLAM3", title: UMI fork of ORB-SLAM3, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/umi_gripper", title: MuJoCo Menagerie umi_gripper, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2407.10353", title: "UMI on Legs: Making Manipulation Policies Mobile with Manipulation-Centric Whole-body Controllers", accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2410.18647", title: Data Scaling Laws in Imitation Learning for Robotic Manipulation, accessed: 2026-11-18}
---

# UMI gripper (Universal Manipulation Interface)

A hand-held, trigger-operated parallel-jaw gripper, printed in PLA and TPU, that carries a GoPro
as its only sensor. You record demonstrations by hand anywhere, without a robot, and the UMI
pipeline turns the video into training data for a policy that runs on a real arm. Cheng Chi and
colleagues at Stanford, Columbia and Toyota Research Institute published it in 2024 [1][2]. It is
the reference design for robot-free data collection and is cheap to build.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | The hand-held data-collection gripper; the robot-side kit is under "How it works" | — |
| Degrees of freedom | 1 jaw axis, moved by the user's trigger; there are no motors | [1] |
| Finger stroke | 80 mm | [1] |
| Mass | 780 g | [1] |
| Size (L x W x H) | 310 x 175 x 210 mm | [1] |
| Camera | GoPro Hero 9 with Max Lens Mod 1.0, 155° fisheye | [1][3] |
| Other sensing | GoPro IMU logged into the video file; two side mirrors give stereo views in the same image | [1] |
| Gripper-width sensing | Printed ArUco tags, detected in the video | [3][4] |
| Fingers | Soft, ribbed TPU 95A fingers, the same on the hand-held and the robot gripper | [1] |
| Collection speed | About 30 s per demonstration; 111 cup demos per hour against 35 with SpaceMouse teleoperation | [2] |
| Robot-side requirement | Any arm with a parallel-jaw gripper of more than 85 mm stroke and a matching camera mount | [1][2] |

## How it works

The body is a printed parallel-jaw gripper: a trigger and handle drive two finger holders through
printed gears and linkages, riding on two MGN9C linear rails, with a compression spring in the
BOM [1][3]. A GoPro on the wrist records everything: fisheye video for wide context, the two
mirrors for implicit stereo depth, and IMU data in the same MP4 file, so all streams share one
clock [1].

Software rebuilds the actions after the fact. The pipeline processes the videos, extracts the IMU
track, builds a map, runs inertial-monocular SLAM with the team's ORB-SLAM3 fork, detects the
ArUco tags to measure gripper width and tell the grippers apart, calibrates, and writes a Zarr
dataset [4][6]. The README calls SLAM the most fragile step [4]. Policies are Diffusion Policy
models; they output relative end-effector trajectories plus gripper width, and the system
compensates for each robot's measured camera and actuation latency at run time [1].

To deploy, the robot gets the same GoPro and soft fingers. The reference kit is a UR5e or UR5
CB3 with a Weiss WSG-50 gripper, a printed mount, and a GoPro Media Mod and Elgato capture card
to stream video [3][4]. A Franka arm works through Polymetis, with a mount that turns the
WSG-50 by 90° [1][5]. Bimanual setups use two grippers [1].

MuJoCo Menagerie has an MJCF model converted from the published CAD, with free-floating base
joints so it can be moved like a hand-held tool [7].

## What it is used for

- Demonstrations collected in the wild: the paper trains cup arrangement, dynamic tossing,
  bimanual cloth folding and dish washing from UMI data alone [1][2].
- The cup policy was trained on demonstrations from 30 locations; the processed dataset and a
  pretrained checkpoint are public [4].
- UMI on Legs feeds UMI demonstrations to a quadruped with an arm [8].
- A 2024 study of data scaling in imitation learning collected its demonstrations with UMI grippers [9].

## Cost and BOM

| Item | Price (USD) | Type | Date | Source |
|---|---|---|---|---|
| Gripper body: PLA+, two MGN9C rails, screws, spring, mirror, grease, tape | about 62 | BOM | guide undated | [3] |
| Soft fingers: TPU 95A and grip tape | about 11 | BOM | guide undated | [3] |
| GoPro Hero 9, Max Lens Mod 1.0, microSD card | about 298 | BOM | guide undated | [3] |
| Whole hand-held gripper ($73 printed gripper plus $298 camera) | 371 | BOM | 2024-03-06 | [1] |
| Robot-side camera system, per arm | about 546.58 | BOM | guide undated | [3] |

The robot side also needs a WSG-50 gripper, listed at €3,875, and the arm itself ("By Quote" for
the UR5e) [3]. Parts are linked to Amazon.

## Building it

**Difficulty 2:** printed parts, off-the-shelf rails and screws, a GoPro; no soldering. The
hard part is the SLAM pipeline, not the build.

- **Printing:** PLA+ with a 0.6 mm nozzle, 0.3 mm layers, 1.2 mm walls, 20% gyroid; TPU 95A
  fingers at 100% infill, 255 °C, fan off; Cura 3MF examples are shared [3]. Print time is not
  stated.
- **Guides:** video tutorials for printing and assembly, and a data-collection tutorial [2][3].
- **Calibration:** left and right grippers carry different ArUco tags; the robot GoPro needs GoPro
  Labs firmware and a QR code setting for clean HDMI output [3][4].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Gripper, soft finger and robot-mount CAD | Onshape | [Hardware guide](https://docs.google.com/document/d/1TPYwV9sNVPAi0ZlAupDMkXZ4CA1hsZx7YDMSmcEy6EU/edit) [3] | No licence stated |
| Print profiles, ArUco tag sheets | Cura 3MF, PDF | Google Drive, linked from the guide [3] | No licence stated |
| BOM and build guide | Google Doc | [3] | No licence stated |
| Pipeline, training and deployment code | Python | [real-stanford/universal_manipulation_interface](https://github.com/real-stanford/universal_manipulation_interface) | MIT |
| SLAM | C++ | [cheng-chi/ORB_SLAM3](https://github.com/cheng-chi/ORB_SLAM3) | GPL-3.0 |
| Example data and checkpoints | Zarr, checkpoint | real.stanford.edu, linked from the README [4] | No licence stated |
| Model | MJCF | [Menagerie umi_gripper](https://github.com/google-deepmind/mujoco_menagerie/tree/main/umi_gripper) | MIT |
| Electronics and firmware | GoPro | — | Proprietary |

The triage note was right: no hardware licence is stated in the guide, on the project page or in
the repo, which holds no CAD [2][3][4]. The CAD is linked publicly from the guide, but reuse
rights are unclear: ask the authors before redistributing it. The paper says the hardware is
open-sourced, without naming a licence [1].

## Strengths and limits

- **Strengths:** about $371 per gripper [1]; no robot needed while collecting, so data comes from
  many places fast [2]; policies move between robots [1]; full pipeline code, data and a
  checkpoint are public [4]; a MuJoCo model exists [7].
- **Limits:** visual SLAM needs a textured scene [1]; slower than a bare human hand, partly
  because of its weight and bulk [1]; the robot side needs an expensive gripper with more than
  85 mm of stroke [2][3]; tested only on Ubuntu 22.04 with Docker [4]; no hardware licence.

## What to reuse

- Put the same camera and soft fingers on the hand-held tool and on the robot, so observations
  match at training and run time [1].
- Mirrors in the camera's field of view for cheap stereo from one camera [1].
- Log IMU and video in one file so the streams never need syncing [1].
- Measure and compensate each robot's latencies at inference [1].

## Related robots

- [Universal Robots](universal-robots.md) and [Franka Panda](franka-panda.md): the reference
  deployment arms [3][5].
- [Robotiq 2F-85](robotiq-2f-85.md): a common research gripper; UMI's robot side asks for more
  than 85 mm of stroke [2].

## Sources

1. [Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots (arXiv v3, 2024-03-06)](https://arxiv.org/abs/2402.10329), accessed 2026-11-18
2. [UMI project page](https://umi-gripper.github.io/), accessed 2026-11-18
3. [UMI hardware building guide](https://docs.google.com/document/d/1TPYwV9sNVPAi0ZlAupDMkXZ4CA1hsZx7YDMSmcEy6EU/edit), accessed 2026-11-18
4. [UMI repository README](https://github.com/real-stanford/universal_manipulation_interface), accessed 2026-11-18
5. [UMI Franka deployment instructions](https://github.com/real-stanford/universal_manipulation_interface/blob/main/franka_instruction.md), accessed 2026-11-18
6. [UMI fork of ORB-SLAM3](https://github.com/cheng-chi/ORB_SLAM3), accessed 2026-11-18
7. [MuJoCo Menagerie umi_gripper](https://github.com/google-deepmind/mujoco_menagerie/tree/main/umi_gripper), accessed 2026-11-18
8. [UMI on Legs: Making Manipulation Policies Mobile with Manipulation-Centric Whole-body Controllers](https://arxiv.org/abs/2407.10353), accessed 2026-11-18
9. [Data Scaling Laws in Imitation Learning for Robotic Manipulation](https://arxiv.org/abs/2410.18647), accessed 2026-11-18
