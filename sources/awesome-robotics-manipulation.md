---
type: source
name: Awesome-Robotics-Manipulation
registry: awesome-robotics-manipulation
url: https://github.com/BaiShuanghao/Awesome-Robotics-Manipulation
commit: "14f72df"
read_on: 2026-11-18
counts: {entries: 109, pages: 28, waiting: 0, index_only: 77, deferred: 0, rejected: 4}
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
| Contact-GraspNet | [Contact-GraspNet](../wiki/learning/models/contact-graspnet.md) | B |
| GraspNet-1Billion | [GraspNet-1Billion](../wiki/learning/datasets/graspnet-1billion.md) | B |
| GR00T N1 | [Isaac GR00T](../wiki/learning/models/gr00t.md) | A |
| Octo | [Octo](../wiki/learning/models/octo.md) | B |
| RT-1 | [RT-1 (Robotics Transformer 1)](../wiki/learning/models/rt-1.md) | B |
| π0 | [π0 family (openpi - π0, π0-FAST, π0.5)](../wiki/learning/models/pi0.md) | A |
| OpenVLA | [OpenVLA (and OpenVLA-OFT)](../wiki/learning/models/openvla.md) | B |
| RT-2 | [RT-2 (Robotics Transformer 2)](../wiki/learning/models/rt-2.md) | B |
| SmolVLA | [SmolVLA](../wiki/learning/models/smolvla.md) | B |
| ACT | [ACT (Action Chunking with Transformers)](../wiki/learning/policies/act.md) | A |
| RDT-1B | [RDT (RDT-1B and RDT2)](../wiki/learning/models/rdt.md) | B |
| Diffusion Policy | [Diffusion Policy](../wiki/learning/policies/diffusion-policy.md) | A |
| ManiSkill | [ManiSkill](../wiki/learning/frameworks/maniskill.md) | A |
| SIMPLER | [SimplerEnv (SIMPLER)](../wiki/learning/benchmarks/simpler-env.md) | B |
| LIBERO | [LIBERO](../wiki/learning/benchmarks/libero.md) | B |
| Robomimic | [robomimic](../wiki/learning/frameworks/robomimic.md) | B |
| RLBench | [RLBench](../wiki/learning/benchmarks/rlbench.md) | B |
| Isaac Lab | [Isaac Lab](../wiki/learning/frameworks/isaac-lab.md) | A |
| RoboCasa | [RoboCasa (RoboCasa365)](../wiki/learning/benchmarks/robocasa.md) | B |
| robosuite | [robosuite](../wiki/learning/frameworks/robosuite.md) | A |
| DROID | [DROID](../wiki/learning/datasets/droid.md) | A |
| Open X-Embodiment | [Open X-Embodiment](../wiki/learning/datasets/open-x-embodiment.md) | A |
| BridgeData V2 | [BridgeData V2](../wiki/learning/datasets/bridgedata-v2.md) | B |
| Robot Learning: A Tutorial (code: LeRobot) | [LeRobot](../wiki/learning/frameworks/lerobot.md) | A |
| ManiSkill2 | [ManiSkill](../wiki/learning/frameworks/maniskill.md) | A |
| CALVIN | [CALVIN](../wiki/learning/benchmarks/calvin.md) | B |
| BEHAVIOR-1K | [BEHAVIOR-1K (with OmniGibson)](../wiki/learning/benchmarks/behavior-1k.md) | B |

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|

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
