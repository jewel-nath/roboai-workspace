---
type: robot
name: Stanford TidyBot and TidyBot++
summary: Holonomic mobile manipulator from Princeton and Stanford; TidyBot (2023) used LLMs to learn where a person puts things away, and TidyBot++ (2024) is an open powered-caster base with CAD, a BOM of about $5,400 without the arm, MIT code and a phone-teleoperation imitation-learning pipeline.
tags: [mobile-manipulator, holonomic, powered-casters, swerve, kinova-gen3, imitation-learning, diffusion-policy, llm, mujoco, stanford, princeton]
category: mobile-manipulator
tier: B
openness: partial
maker: Jimmy Wu and colleagues, Princeton University and Stanford University
year: 2023
license: {hardware: , software: MIT, docs: CC-BY-4.0}
links: {repo: "https://github.com/jimmyyhwu/tidybot2", docs: "https://tidybot2.github.io/docs/", cad: "https://github.com/jimmyyhwu/tidybot2-resources", paper: "https://arxiv.org/abs/2412.10447", site: "https://tidybot2.github.io/"}
specs: {dof: 16, payload_kg: , reach_mm: , mass_kg: 34, size_mm: "540 x 500 x 375", speed_mps: , runtime_h: 8}
stack: {actuators: "8 CTRE Kraken X60 motors in 4 SDS MK4 swerve modules used as powered casters (steer and drive per caster); Kinova Gen3 arm in the reference design", mcu: , compute: "onboard mini PC for real-time control (Intel NUC 7 or Beelink Mini S12 Pro used); CTRE CANivore USB-to-CAN adapter; GPU laptop for policy training and inference", sensors: ["CTRE CANcoder steering encoder per caster", "Logitech USB base camera", "Kinova Gen3 wrist camera"], sim_models: ["MJCF, base with Kinova Gen3 and Robotiq 2F-85 (tidybot2 models/)", "MJCF (MuJoCo Menagerie, stanford_tidybot)"], ros2: none}
cost: {type: bom, usd: 5379.63, as_of: 2024-10-01, source: "https://tidybot2.github.io/docs/bom/"}
build: {difficulty: 3, hours: 10, print_hours: }
maturity: {last_commit: 2025-03-27, stars: 626, active: false}
use_cases: [imitation-learning, teleop, manipulation, navigation, data-collection, research]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://tidybot.cs.princeton.edu/", title: TidyBot project page, accessed: 2026-11-18}
  - {url: "https://github.com/jimmyyhwu/tidybot", title: tidybot repository (2023 code release), accessed: 2026-11-18}
  - {url: "https://tidybot2.github.io/", title: TidyBot++ project page, accessed: 2026-11-18}
  - {url: "https://tidybot2.github.io/docs/", title: TidyBot++ assembly guide, accessed: 2026-11-18}
  - {url: "https://tidybot2.github.io/docs/bom/", title: TidyBot++ bill of materials, accessed: 2026-11-18}
  - {url: "https://tidybot2.github.io/docs/can-system/", title: TidyBot++ assembly guide, CAN system, accessed: 2026-11-18}
  - {url: "https://github.com/jimmyyhwu/tidybot2", title: tidybot2 repository README, accessed: 2026-11-18}
  - {url: "https://github.com/jimmyyhwu/tidybot2-resources", title: tidybot2-resources (STEP, print, laser-cut and machining files), accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2412.10447", title: "TidyBot++: An Open-Source Holonomic Mobile Manipulator for Robot Learning", accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/stanford_tidybot", title: "MuJoCo Menagerie: stanford_tidybot", accessed: 2026-11-18}
---

# Stanford TidyBot and TidyBot++

TidyBot (2023), from Princeton and Stanford, tidies rooms with an LLM that infers each person's
storage preferences from a few examples [1]. TidyBot++ (2024) is its holonomic powered-caster base
as an open design for imitation learning, carrying the arm of your choice [3][9]. Its code is idle since March 2025 [7].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | TidyBot++, Kinova reference design, with a Kinova Gen3 arm and Robotiq 2F-85 gripper; size, mass and runtime in the variant table | [4][7] |
| Degrees of freedom | 16 counted: 8 caster motors (steer and drive on 4 casters) giving 3 planar DoF, 7 arm joints, gripper as one | [5][7] |
| Payload, odometry | Built for one arm of about 10 kg; tested with 120 kg of plates. Drift under 1 cm per metre, under 1° per turn | [3][4] |
| Control rates | Base 250 Hz; policy 10 Hz; default base limits 0.5 m/s and 1.57 rad/s (top speed not published) | [7] |
| TidyBot results | 91.2% accuracy on unseen objects in the benchmark; 85.0% of objects put away in real tests | [1] |

## How it works

Each TidyBot++ caster is an FRC swerve module with steer and drive motors and an absolute encoder,
all on one CAN bus behind a USB adapter [5][6]. Driving all four together moves the base in x, y
and yaw at once, avoiding the slow manoeuvres of non-holonomic bases [9]. The frame is extrusion with
laser-cut acrylic plates, printed mounts and four machined shafts, on one battery [4][5].

The Python code runs base and arm controllers as real-time processes on the mini PC behind RPC
servers; a GPU laptop runs Diffusion Policy; a phone interface does teleoperation [7]. Only a Kinova
Gen3 arm controller ships [7]. A MuJoCo environment covers the pipeline without hardware [7], and
Menagerie has `stanford_tidybot` [10]. There is no ROS. The 2023 TidyBot ran three Kinova Gen3 robots
on holonomic bases driven by Stanford lab code, located by ceiling cameras and fiducials [2].

| Base design | Intended arms | Size (W x L x H) | Mass | Battery, runtime | BOM | Source |
|---|---|---|---|---|---|---|
| Kinova | about 10 kg: Kinova, xArm | 500 x 540 x 375 mm | 34 kg | 768 Wh, 8 h | $5,379.63 | [4][5] |
| Franka | about 20 kg: Franka, UR5 | 500 x 540 x 445 mm | 45 kg | 2160 Wh, 8 h | $6,272.77 | [4][5] |
| ARX5 | about 5 kg: ARX5, ViperX | 400 x 440 x 375 mm | 26 kg | 288 Wh, 4.5 h | $5,205.71 | [4][5] |

## What it is used for

- Imitation learning for household mobile manipulation from phone-teleoperated demos [9].
- LLM-based personalised tidying, the 2023 work (IROS 2023, Autonomous Robots) [1].

## Cost and BOM

**$5,379.63** for the Kinova base, arm excluded; 8 Kraken X60 motors ($199.99 each) and 4 MK4 modules
($300 each) dominate [5]. Arm, mini PC, GPU laptop and tools are unpriced. The BOM is undated (Amazon
links "current as of October 2024"), so `as_of` uses 2024-10-01 [5].

## Building it

**Difficulty 3:** order four machined shafts, laser-cut plates, print PLA mounts, wire CAN with WAGO
connectors, set up firmware and IDs in Phoenix Tuner X on Windows ($100 Phoenix Pro licence in the BOM);
no soldering [5][6]. Assembly takes about 10 hours [4].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| CAD and fabrication files | STEP; STL, 3MF, G-code; DXF; PDF drawings; CSV BOMs | [tidybot2-resources](https://github.com/jimmyyhwu/tidybot2-resources) [8]; Onshape links in the guide [4] | None stated in the repo |
| Code, sim models | Python, MJCF | [tidybot2](https://github.com/jimmyyhwu/tidybot2) [7]; 2023 code in [tidybot](https://github.com/jimmyyhwu/tidybot) [2] | MIT |
| Assembly and usage guide | Website | [tidybot2.github.io/docs](https://tidybot2.github.io/docs/) [4] | CC-BY-4.0 |
| Menagerie model | MJCF | `stanford_tidybot` [10] | MIT; Kinova and Robotiq parts keep their own |

## Strengths and limits

- **Strengths:** a true holonomic base from off-the-shelf FRC parts for about $5,400 that takes the arm
  a lab already owns, with BOM, CAD, sim and a tested teleoperation-to-policy pipeline [3][5][7].
- **Limits:** the arm, the costly part, is extra; no hardware licence; Kinova-only arm code; no ROS;
  Windows for motor setup; code idle since March 2025 [5][6][7][8].

## Related robots

- Arms the base is sized for: [Kinova Gen3](kinova-gen3.md), [Franka Panda](franka-panda.md),
  [UFACTORY xArm](ufactory-xarm.md), [Universal Robots](universal-robots.md), [Interbotix X-series](interbotix-x-series-arms.md).
- Other mobile manipulators: [Hello Robot Stretch](hello-robot-stretch.md), [Fetch](fetch.md),
  [TIAGo](tiago.md), [Google Robot](google-robot.md).

## Sources

1. [TidyBot project page](https://tidybot.cs.princeton.edu/), accessed 2026-11-18
2. [tidybot repository (2023 code release)](https://github.com/jimmyyhwu/tidybot), accessed 2026-11-18
3. [TidyBot++ project page](https://tidybot2.github.io/), accessed 2026-11-18
4. [TidyBot++ assembly guide](https://tidybot2.github.io/docs/), accessed 2026-11-18
5. [TidyBot++ bill of materials](https://tidybot2.github.io/docs/bom/), accessed 2026-11-18
6. [TidyBot++ assembly guide, CAN system](https://tidybot2.github.io/docs/can-system/), accessed 2026-11-18
7. [tidybot2 repository README](https://github.com/jimmyyhwu/tidybot2), accessed 2026-11-18
8. [tidybot2-resources (STEP, print, laser-cut and machining files)](https://github.com/jimmyyhwu/tidybot2-resources), accessed 2026-11-18
9. [TidyBot++: An Open-Source Holonomic Mobile Manipulator for Robot Learning](https://arxiv.org/abs/2412.10447), accessed 2026-11-18
10. [MuJoCo Menagerie: stanford_tidybot](https://github.com/google-deepmind/mujoco_menagerie/tree/main/stanford_tidybot), accessed 2026-11-18
