---
type: robot
name: Google Robot (Everyday Robots mobile manipulator)
summary: One-armed wheeled mobile manipulator from Alphabet's Everyday Robots that collected the RT-1 data behind RT-1, RT-2 and SayCan; never sold and retired with the unit in 2023, it lives on as a MuJoCo Menagerie model, a SimplerEnv benchmark robot and the fractal dataset in Open X-Embodiment.
tags: [mobile-manipulator, everyday-robots, google, rt-1, rt-2, saycan, vla, simplerenv, open-x-embodiment, mujoco, discontinued]
category: mobile-manipulator
tier: B
openness: closed-reference
maker: Everyday Robots (Alphabet X), with Google Research
year: 2019
license: {hardware: , software: Apache-2.0, docs: }
links: {repo: , docs: , cad: , paper: "https://arxiv.org/abs/2212.06817", site: }
specs: {dof: 8, payload_kg: , reach_mm: , mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: , mcu: , compute: , sensors: ["RGB camera (256 x 320 images in the RT-1 dataset)"], sim_models: ["MJCF (MuJoCo Menagerie, google_robot)", "SAPIEN / ManiSkill2 (SimplerEnv Google Robot environments)"], ros2: none}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: , stars: , active: }
use_cases: [research, manipulation, imitation-learning, reinforcement-learning, data-collection]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://x.company/blog/posts/introducing-the-everyday-robot-project/", title: "X blog: Introducing the Everyday Robot Project (2019-11-21)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/alphabet-closes-everyday-robots-among-layoffs/", title: "The Robot Report: Alphabet closes Everyday Robots among layoffs (2023-02-24)", accessed: 2026-11-18}
  - {url: "https://ar5iv.labs.arxiv.org/html/2212.06817", title: "RT-1: Robotics Transformer for Real-World Control at Scale (paper, ar5iv)", accessed: 2026-11-18}
  - {url: "https://robotics-transformer1.github.io/", title: RT-1 project page, accessed: 2026-11-18}
  - {url: "https://say-can.github.io/", title: "SayCan: Do As I Can, Not As I Say project page", accessed: 2026-11-18}
  - {url: "https://ar5iv.labs.arxiv.org/html/2307.15818", title: "RT-2: Vision-Language-Action Models (paper, ar5iv)", accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/google_robot", title: "MuJoCo Menagerie: google_robot", accessed: 2026-11-18}
  - {url: "https://github.com/simpler-env/SimplerEnv", title: SimplerEnv README, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/open_x_embodiment", title: Open X-Embodiment repository README, accessed: 2026-11-18}
  - {url: "https://www.tensorflow.org/datasets/catalog/fractal20220817_data", title: "TensorFlow Datasets: fractal20220817_data", accessed: 2026-11-18}
---

# Google Robot (Everyday Robots mobile manipulator)

The wheeled, one-armed robot from Alphabet's Everyday Robots, which X announced in 2019 [1]. Google
Research used its fleet for RT-1, SayCan and RT-2 [3][5][6]; it is the "Google Robot" of SimplerEnv
[8], and its data is part of Open X-Embodiment [9][10]. It was **never sold**, and Alphabet
**shut Everyday Robots down in February 2023** [2]. Builders meet it only as models and data.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | The one robot used in RT-1; no variants or public datasheet | [3] |
| Degrees of freedom | 7-DoF arm, two-finger gripper, mobile base; `dof: 8` counts the arm and the gripper as one, as base and head actuators were not published | [3] |
| Menagerie model | 9 joints: torso, shoulder, bicep, elbow, forearm, wrist, gripper and two fingers; head and wheels fixed | [7] |
| Action space (RT-1) | Arm x, y, z, roll, pitch, yaw and gripper opening; base x, y and yaw; 3 Hz | [4] |
| Camera data | 256 x 320 RGB images in the RT-1 dataset | [10] |
| Fleet | Over a hundred robots built; 13 collected the RT-1 data over 17 months | [2][3] |
| Mass, size, payload, reach, speed | Not published | — |

## How it works

Google never released a datasheet, CAD or driver. What is public is the outline: a wheeled base, a
7-DoF arm with a two-finger gripper [3], and a head, fixed in the Menagerie model [7]. X framed the
project around robots that learn from practice and simulation rather than hand-coding; an office
trial cut waste-sorting contamination from 20% to under 5% [1].

Control in the papers is learned end to end. RT-1 maps camera images and a text instruction to
end-effector and base motions at 3 Hz [4]. RT-2 fine-tuned vision-language models (PaLI-X at 5B and
55B, PaLM-E at 12B) to output the 7-DoF mobile manipulator's actions as text tokens [6].
SayCan used a language model to chain the robot's learned skills [5].

For simulation, Menagerie's `google_robot` is a simplified MJCF of the arm and gripper on a fixed
base, under Apache-2.0 [7]. SimplerEnv rebuilt six Google Robot tasks (pick coke can, pick object, move
near, open and close drawer, place in closed drawer) in SAPIEN at 3 Hz, with visual-matching and
variant-aggregation setups, and ships RT-1, RT-1-X and Octo evaluations [8].

## What it is used for

- The RT-1 dataset: about 130k episodes, more than 700 instructions, two real office kitchens [3][4];
  released as `fractal20220817_data` (87,212 episodes, 111 GiB) in TFDS and Open X-Embodiment [9][10].
- SayCan: 101 kitchen instructions; 84% correct plans and 74% execution with PaLM [5].
- Real-to-sim benchmarking of generalist robot policies in SimplerEnv [8].
- Fleet reinforcement learning: Menagerie asks users to cite a 2023 RSS paper on waste sorting [7].

## Cost and BOM

Never sold, so `cost` is empty. No price or BOM was ever published.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Simulation model | MJCF | Menagerie [`google_robot`](https://github.com/google-deepmind/mujoco_menagerie/tree/main/google_robot) [7] | Apache-2.0 |
| Benchmark | SAPIEN / ManiSkill2 environments | [SimplerEnv](https://github.com/simpler-env/SimplerEnv) [8] | MIT |
| RT-1 data | RLDS / TFDS | `fractal20220817_data` [10]; Open X-Embodiment [9] | OXE repo: CC-BY-4.0 for non-software materials |
| RT-1 code, RT-1-X checkpoints | TensorFlow, JAX | [robotics_transformer](https://github.com/google-research/robotics_transformer) via [4]; OXE repo [9] | Apache-2.0 |
| Hardware, firmware, driver | — | Not published | Closed |

## Strengths and limits

- **Strengths:** about 130k real episodes from one robot type, free to download, plus a free model
  and a sim benchmark with reference RT-1, RT-1-X and Octo results [3][8][10].
- **Limits:** you cannot buy, build or run the real robot; no published specs; the Menagerie model
  has no mobile base or head joints [2][7].

## Related robots

- [Hello Robot Stretch](hello-robot-stretch.md), [Fetch](fetch.md), [TIAGo](tiago.md),
  [PR2](pr2.md) and [TidyBot](tidybot.md): other mobile manipulators, sold or open.
- [Interbotix X-series arms](interbotix-x-series-arms.md): the WidowX, the other SimplerEnv robot.
- [KUKA LBR iiwa](kuka-lbr-iiwa.md): RT-1 also mixed in data from a KUKA arm [4].

## Sources

1. [X blog: Introducing the Everyday Robot Project (2019-11-21)](https://x.company/blog/posts/introducing-the-everyday-robot-project/), accessed 2026-11-18
2. [The Robot Report: Alphabet closes Everyday Robots among layoffs (2023-02-24)](https://www.therobotreport.com/alphabet-closes-everyday-robots-among-layoffs/), accessed 2026-11-18
3. [RT-1: Robotics Transformer for Real-World Control at Scale (paper, ar5iv)](https://ar5iv.labs.arxiv.org/html/2212.06817), accessed 2026-11-18
4. [RT-1 project page](https://robotics-transformer1.github.io/), accessed 2026-11-18
5. [SayCan: Do As I Can, Not As I Say project page](https://say-can.github.io/), accessed 2026-11-18
6. [RT-2: Vision-Language-Action Models (paper, ar5iv)](https://ar5iv.labs.arxiv.org/html/2307.15818), accessed 2026-11-18
7. [MuJoCo Menagerie: google_robot](https://github.com/google-deepmind/mujoco_menagerie/tree/main/google_robot), accessed 2026-11-18
8. [SimplerEnv README](https://github.com/simpler-env/SimplerEnv), accessed 2026-11-18
9. [Open X-Embodiment repository README](https://github.com/google-deepmind/open_x_embodiment), accessed 2026-11-18
10. [TensorFlow Datasets: fractal20220817_data](https://www.tensorflow.org/datasets/catalog/fractal20220817_data), accessed 2026-11-18
