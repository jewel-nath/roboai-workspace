---
type: source
name: Awesome-Robotics-Manipulation
registry: awesome-robotics-manipulation
url: https://github.com/BaiShuanghao/Awesome-Robotics-Manipulation
commit: "14f72df"
read_on: 2026-11-18
counts: {entries: 109, pages: 1, waiting: 27, index_only: 77, deferred: 0, rejected: 4}
---

# Awesome-Robotics-Manipulation: what it gives RoboAI

The paper list behind a large survey of robot manipulation: about 4,050 papers, up to October
2026, sorted by task, high-level planning, low-level action modelling, bottlenecks and
applications, plus tables of simulators, benchmarks and datasets. Almost every entry is a paper, so
for RoboAI it is a map of the research rather than a source of tools. What it gives a builder is
the few dozen entries whose code, weights or data people actually run: the VLAs (π0, GR00T,
OpenVLA, SmolVLA), the standard policies (ACT, Diffusion Policy), the big datasets (Open
X-Embodiment, DROID) and the simulators and benchmarks (robosuite, ManiSkill, Isaac Lab, LIBERO).

## How it was read

- Read at commit `14f72df` (last commit 2026-10-29) on 2026-11-18: the README and the five
  section files it links (`contents/manipulation_tasks.md`, `high-level_structured_planning.md`,
  `low-level_learning-based_action_modeling.md`, `bottlenecks.md`, `applications.md`), plus the
  survey's v2 update log. Every table row was parsed with a script and every title read.
- **Size.** The plan's ~340 counted the README alone. The list holds 4,129 paper rows (about
  4,050 distinct titles, as some papers sit in several sections), 2,616 of them with a GitHub link.
- **Paper sections** are one index row per entry of the README's table of contents, 46 in all;
  their subsections are folded in (the VLA row alone covers 17 subsections and 1,065 papers).
  Counts are table rows, repeats included. Only Tutorial and GitHub Repo are not paper sections, so
  each of their entries has its own row.
- **Own rows** went to papers whose code, model, dataset or benchmark builders use, plus robots a
  builder would look up. Their repos were shallow-cloned on 2026-11-18 for the last commit and the
  licence (27 repos). Quiet repos: Diffusion Policy (2024-12-24), ACT (`tonyzhaozh/act`,
  2024-01-28; the list links the `aloha` hardware repo), Octo (2024-07-30), OpenVLA (2025-03-23),
  LIBERO (2025-03-15), BridgeData V2 (2024-03-16) and RT-1 (2023-02-10). ACT and Diffusion Policy
  stay tier A because LeRobot maintains both.
- **Licences of note:** Contact-GraspNet is under the NVIDIA Source Code License (non-commercial
  use only); `graspnet-baseline` is academic non-commercial, while `graspnetAPI` is MIT; RLBench
  allows non-commercial research only. openpi is Apache-2.0, with Gemma terms for the weights.
  GR00T's code is Apache-2.0 and its weights use the NVIDIA Open Model License, which allows
  commercial use. Open X-Embodiment code is Apache-2.0 and its data CC-BY-4.0. The DROID platform
  repo has no licence file; its policy-learning repo is MIT. RT-2 has no public code or weights.
- **LeRobot** is not a list entry by name. It is the code link of "Robot Learning: A Tutorial",
  SmolVLA and FineART, so it is triaged on the tutorial's row.
- **Variants** (OpenVLA-OFT, π0.5, FAST, RDT2, DP3) are index rows that belong on their parent's
  page.
- **Robots.** Hardware papers (new hands, grippers, exoskeletons, teleoperation rigs) stay in their
  section rows. Mobile ALOHA, TidyBot++, UMI, GELLO, Ruka-v2 and TriFinger have their own rows. The
  2023 TidyBot paper is counted under Mobile Manipulation and is on the same Atlas page as TidyBot++.
- **Nothing deferred:** the MPC and control work is papers, already in section rows, and the list
  names no Phase 5 tools or parts.
- **Nothing dead** among the checked repos, and nothing suspicious: no agent instruction files and
  no prompt-like text, only an invitation to send papers by pull request or email.

## Pages made

| Entry | Page | Tier |
|---|---|---|
| GENESIS | [Genesis](../wiki/tools/genesis.md) | B |

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|
| Contact-GraspNet | `learning/contact-graspnet` | B | manip | Common 6-DoF grasp generator from depth point clouds; NVIDIA non-commercial licence, quiet since 2024 |
| GraspNet-1Billion | `learning/graspnet-1billion` | B | manip | Standard 6-DoF grasp benchmark and dataset; MIT API, non-commercial baseline code |
| GR00T N1 | `learning/gr00t` | A | learning | NVIDIA's open foundation model for humanoids and other robots; Apache-2.0 code, commercially usable weights, very active |
| Octo | `learning/octo` | B | learning | Open generalist policy trained on Open X-Embodiment; a frequent baseline, repo quiet since 2024 |
| RT-1 | `learning/rt-1` | B | learning | Google's landmark Robotics Transformer and dataset; still a baseline and part of Open X-Embodiment |
| π0 | `learning/pi0` | A | learning | Physical Intelligence's flow-matching VLA; openpi ships π0, π0-FAST and π0.5 weights with fine-tuning code |
| OpenVLA | `learning/openvla` | B | learning | Reference open-source VLA, widely fine-tuned and compared; MIT, repo quiet since March 2025 |
| RT-2 | `learning/rt-2` | B | learning | Introduced the VLA: a web-trained vision-language model that outputs actions; closed, no code |
| SmolVLA | `learning/smolvla` | B | learning | Hugging Face's small VLA in LeRobot, aimed at affordable arms and modest GPUs |
| ACT | `learning/act` | A | learning | Action-chunking transformer from ALOHA; a common first policy for low-cost arms through LeRobot |
| RDT-1B | `learning/rdt` | B | learning | Open diffusion foundation model for bimanual arms; MIT, maintained, with RDT2 as its successor |
| Diffusion Policy | `learning/diffusion-policy` | A | learning | The standard visuomotor diffusion policy; reference repo quiet since 2024, maintained in LeRobot |
| ManiSkill | `learning/maniskill` | A | learning | GPU-parallel manipulation simulator and benchmark, now ManiSkill3; Apache-2.0, active |
| SIMPLER | `learning/simpler-env` | B | learning | Simulated evaluation matched to real Google Robot and WidowX setups; widely reported for VLAs |
| LIBERO | `learning/libero` | B | learning | Standard VLA fine-tuning benchmark with many LIBERO-* offshoots; repo quiet since March 2025 |
| Robomimic | `learning/robomimic` | B | learning | Imitation-learning framework and datasets on robosuite; MIT, maintained |
| RLBench | `learning/rlbench` | B | learning | Historic CoppeliaSim benchmark used by PerAct and RVT; non-commercial research licence |
| Isaac Lab | `learning/isaac-lab` | A | learning | NVIDIA's GPU-parallel RL and imitation framework on Isaac Sim; BSD-3-Clause, very active |
| RoboCasa | `learning/robocasa` | B | learning | Large household-kitchen simulation on robosuite for generalist policies; MIT, active |
| robosuite | `learning/robosuite` | A | learning | MuJoCo manipulation framework under robomimic, RoboCasa and many benchmarks; MIT, maintained |
| DROID | `learning/droid` | A | learning | Large in-the-wild Franka teleoperation dataset with a reproducible robot platform; openpi trains on it |
| Open X-Embodiment | `learning/open-x-embodiment` | A | learning | Pooled multi-robot dataset, CC-BY-4.0, behind RT-X, Octo and OpenVLA |
| BridgeData V2 | `learning/bridgedata-v2` | B | learning | WidowX dataset across many toy-kitchen scenes, part of Open X-Embodiment; basis of SIMPLER's WidowX tasks |
| Robot Learning: A Tutorial (code: LeRobot) | `learning/lerobot` | A | learning | Hugging Face's robot-learning library: datasets, ACT, Diffusion Policy, SmolVLA, SO-101 support |
| ManiSkill2 | `learning/maniskill` | A | learning | GPU-parallel SAPIEN simulator and benchmark for manipulation learning; fast, active and Apache-2.0 |
| CALVIN | `learning/calvin` | B | learning | Long-horizon, language-conditioned manipulation benchmark in PyBullet; a standard test for language policies and VLAs |
| BEHAVIOR-1K | `learning/behavior-1k` | B | learning | Same project as BEHAVIOR-1K: its repo now holds both the OmniGibson simulator and the benchmark |

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| Section: Survey (54 papers) | Surveys of VLAs, world models, dexterity, deformables and humanoids | — | — |
| Section: Grasp (194 papers) | Grasp detection: rectangle, 6-DoF, language-driven, dexterous, bimanual, transparent | — | — |
| AnyGrasp | Closed grasp-detection SDK from the GraspNet team, licence on request | — | — |
| Section: Basic Manipulation (29 papers) | Arm motion planning, MPC and compliance-control papers | — | — |
| Section: Dexterous Manipulation (102 papers) | Dexterous hand designs, teleoperation and dexterous policy learning | — | — |
| Ruka-v2 | Robot; not in the Atlas ([RUKA](../wiki/robots/ruka.md) covers version 1) | — | — |
| Section: Soft Robotic Manipulation (41 papers) | Soft and continuum manipulator design, modelling and control | — | — |
| Section: Deformable Object Manipulation (51 papers) | Cloth, cable, dough and garment manipulation | — | — |
| Section: Mobile Manipulation (55 papers) | Mobile manipulators: whole-body control, planning, mobile VLAs | — | — |
| Mobile ALOHA | Robot; not in the Atlas | — | — |
| TidyBot++ | Robot; on the [Stanford TidyBot and TidyBot++](../wiki/robots/tidybot.md) page | — | — |
| Section: Quadrupedal Manipulation (44 papers) | Legged robots manipulating with arms, legs or body | — | — |
| Section: Humanoid Manipulation (103 papers) | Humanoid loco-manipulation, teleoperation, retargeting and humanoid VLAs | — | — |
| Section: Aerial Manipulation (17 papers) | Drones with arms or grippers | — | — |
| Section: Underwater Manipulation (11 papers) | Underwater manipulators and their control | — | — |
| Section: Task Planning (36 papers) | LLM and symbolic task planners, e.g. SayCan, PaLM-E | — | — |
| Section: Programmatic Planning (38 papers) | LLMs writing robot code as plans, e.g. Code as Policies | — | — |
| Section: Multimodal Reasoning (102 papers) | Embodied VLMs for rewards, spatial reasoning, affordances, failure detection | — | — |
| Section: Geometric Constraint-based Planning (21 papers) | VLM-made constraints and value maps, e.g. VoxPoser, ReKep | — | — |
| Section: 3D Representation-based Planning (32 papers) | Neural fields, Gaussian splats and part models for planning | — | — |
| Section: Video-based Planning (81 papers) | Video generation and world models used as planners | — | — |
| Section: Imitation Learning (IL) (170 papers) | Imitation from actions and observations; interactive and robust IL | — | — |
| Section: Reinforcement Learning (RL) (91 papers) | Model-free and model-based RL, e.g. HIL-SERL, TD-MPC2, DreamerV3 | — | — |
| Section: RL and IL (49 papers) | Methods mixing demonstrations with reinforcement learning | — | — |
| Section: Learning with Auxiliary Tasks (205 papers) | World models, video prediction, pretraining and goal extraction aiding policies | — | — |
| Cosmos World Foundation Model Platform for Physical AI | NVIDIA's open world foundation models for physical-AI video | — | — |
| Section: Vision Action Models (18 papers) | Visuomotor policies without language input | — | — |
| Section: Vision Language Action Models (1,065 papers) | VLAs: architectures, RL tuning, efficiency, robustness, memory, 3D | — | — |
| RDT2 | Successor to RDT-1B; belongs on its page | — | — |
| OpenVLA-Oft | Fast fine-tuning recipe for OpenVLA; belongs on its page | — | — |
| π0.5 | Successor to π0, released in openpi; belongs on its page | — | — |
| Section: Tactile-based Action Models (99 papers) | Visuo-tactile sensing, tactile policies and tactile VLAs | — | — |
| Section: Other Modalities (64 papers) | Audio, force, thermal and event sensing in action models | — | — |
| Section: Pretrained Latent Learning (41 papers) | Pretrained visual representations, e.g. R3M, VC-1, Voltron | — | — |
| Section: Latent Action Learning (29 papers) | Latent actions learned from video and demonstrations | — | — |
| Section: Other Policies (89 papers) | Transformer, Mamba, spiking, frequency, spline and tokenised policies | — | — |
| Section: Diffusion Policy (107 papers) | 2D and 3D diffusion policies and faster variants | — | — |
| DP3 | Point-cloud variant of Diffusion Policy; belongs on its page | — | — |
| Section: Flow Matching Policy (57 papers) | Flow-matching and one-step generative policies | — | — |
| FAST | Action tokenizer for autoregressive VLAs; belongs on the π0 page | — | — |
| Section: Data Collection (155 papers) | Teleoperation rigs, UMI-style grippers, demo generation, crowdsourcing | — | — |
| Universal Manipulation Interface | Robot; on the [UMI gripper](../wiki/robots/umi-gripper.md) page | — | — |
| GELLO | Low-cost printed leader arms for teleoperation; not in the Atlas | — | — |
| MimicGen | Turns a few human demos into many simulated ones (NVIDIA) | — | — |
| Section: Data Utilization (139 papers) | Augmentation, selection, retrieval and reweighting of training data | — | — |
| Section: Task Generalization (107 papers) | Long-horizon, few-shot, meta and continual learning | — | — |
| Section: Environment Generalization (84 papers) | Sim-to-real, viewpoint, lighting and distractor robustness | — | — |
| Section: Cross-Embodiment Generalization (53 papers) | Human-to-robot and cross-robot transfer, e.g. HPT, CrossFormer | — | — |
| Section: Agent (49 papers) | LLM agent harnesses and orchestration for robots | — | — |
| Section: Human-Robot Interaction and Collaboration (25 papers) | Shared autonomy, language feedback and human-robot collaboration | — | — |
| Section: Safety (12 papers) | Safe trajectories, safe control and safe policy learning | — | — |
| Section: Applications (108 papers) | Household, industrial, farm, art, lab, surgical and sports uses | — | — |
| Section: Grasp Datasets (22 papers) | Grasp datasets, e.g. Cornell, Jacquard, ACRONYM, DexGraspNet | — | — |
| Section: Single-Embodiment Manipulation Simulators and Benchmarks (148 papers) | Benchmarks by task: arm, bimanual, long-horizon, robustness, dexterous, humanoid | — | — |
| SO-101 Bench | Simulated spatial-manipulation benchmark for the SO-101 arm; very new | — | — |
| Meta-World | Multi-task and meta-RL benchmark of simulated Sawyer tasks | — | — |
| RoboTwin 2.0 | Bimanual sim benchmark and data generator with domain randomisation | — | — |
| Panda-gym | Simple Franka Gymnasium tasks on PyBullet, good for RL practice | — | — |
| TriFinger | Robot; on the [TriFinger](../wiki/robots/trifinger.md) page | — | — |
| HomeRobot | Meta's open-vocabulary mobile-manipulation benchmark and stack | — | — |
| Section: Cross-Embodiment Simulators and Benchmarks (17 papers) | Multi-robot simulators and learning frameworks | — | — |
| Section: Other Simulators and Benchmarks (17 papers) | Niche sims: chemistry, surgery, orchards, bricks, space, magnetic robots | — | — |
| Section: Trajectory Datasets (35 papers) | Real and synthetic robot demonstration datasets | — | — |
| AgiBot World Colosseo | Large real-robot dataset and GO-1 model from AgiBot | — | — |
| Section: Embodied QA and Affordance Datasets (23 papers) | Spatial reasoning, pointing and affordance benchmarks for VLMs | — | — |
| Section: Human and Robotic Video Benchmarks and Datasets (28 papers) | World-model benchmarks and egocentric human video, e.g. Ego4D, EgoDex | — | — |
| so101-nexus | Personal repo with full-stack robot-learning code for the SO-101 | — | — |
| Awesome-Dual-System-VLA | Paper list on dual-system (fast and slow) VLAs | — | — |
| awesome-embodied-vla-va-vln | Paper list on VLA, vision-action and navigation models | — | — |
| Awesome-Implicit-NeRF-Robotics | Paper list on neural fields in robotics | — | — |
| awesome-humanoid-robot-learning | Paper list on humanoid robot learning | — | — |
| Awesome-Robotics-3D | Paper list on 3D vision; triaged as its own Phase 4 list | — | — |
| Awesome-Video-Robotic-Papers | Paper list on video for robot learning | — | — |
| awesome-humanoid-learning | Paper list on humanoid learning | — | — |
| Awesome-Robotics-Foundation-Models | Paper list on foundation models; triaged as its own Phase 4 list | — | — |
| Awesome-Generalist-Robots-via-Foundation-Models | Paper list from a survey on generalist robots | — | — |
| Awesome-LLM-Robotics | Paper list on LLMs in robotics | — | — |

## Deferred

| Entry | What it is | Phase |
|---|---|---|

## Rejected

| Entry | Why | Date |
|---|---|---|
| GraspNet-1Billion (Grasp Datasets) | Duplicate of the GraspNet-1Billion entry under Grasp | 2026-11-18 |
| ManiSkill3 | Duplicate: same repo as ManiSkill, which now holds ManiSkill3 | 2026-11-18 |
| Isaac Lab (Orbit) | Duplicate: Orbit is Isaac Lab's earlier name, same repo | 2026-11-18 |
| RT-1 (Trajectory Datasets) | Duplicate of the RT-1 entry; its dataset belongs on that page | 2026-11-18 |
