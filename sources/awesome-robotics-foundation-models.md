---
type: source
name: Awesome Robotics Foundation Models
registry: awesome-robotics-foundation-models
url: https://github.com/robotics-survey/Awesome-Robotics-Foundation-Models
commit: "58ebfc2"
read_on: 2026-11-18
counts: {entries: 42, pages: 4, waiting: 4, index_only: 33, deferred: 0, rejected: 1}
---

# Awesome Robotics Foundation Models: what it gives RoboAI

The companion list to the survey "Foundation Models in Robotics" (IJRR 2024): about 110 papers on
LLMs, VLMs and robot transformers used for planning, rewards and control, plus open-vocabulary
perception models and embodied-AI simulators. It stopped in October 2024 and misses Octo, OpenVLA
and pi0, so it is a map of the 2022–2024 research rather than a tool list. What a builder can still
use from it: RT-1 and RT-2 as the start of vision-language-action models, Segment Anything,
Grounding DINO and FoundationPose for perception, and the LIBERO, BEHAVIOR-1K and Habitat
benchmarks.

## How it was read

- Read at commit `58ebfc2` (last commit 2024-10-07) on 2026-11-18. The repo holds only the README,
  a licence and the survey's figure; the README was read in full.
- **Paper sections:** every section except Simulators holds only papers, so each is one index row
  with its paper count as listed (subsections folded into their `###` section). They list 123
  papers with 12 repeats: NLMap and MineDreamer appear three times each, and CLIP-Fields, Voyager,
  DEPS, JARVIS-1, LEO, GROOT, MP5 and the zero-shot planners paper twice each.
- Papers whose code, model or benchmark builders still use have their own rows as well: RT-1,
  RT-2, Grounding DINO, Segment Anything and FoundationPose wait for pages; CLIPort, PerAct, R3M,
  VIMA, OWL-ViT, DINO, FastSAM, MobileSAM and RoboNet are index only.
- The Simulators section lists platforms and benchmarks, so its 11 entries are triaged one by one.
- Page candidates were checked with a blobless shallow clone (last commit, licence file):
  RT-1 (2023-02-10, Apache-2.0); Grounding DINO (2024-08-12, Apache-2.0); FoundationPose
  (2026-04-29, NVIDIA Source Code License, non-commercial); BEHAVIOR-1K (2026-11-18, MIT);
  habitat-sim and habitat-lab (2026-05-07, MIT); LIBERO (2025-03-15, MIT). The list links only
  Segment Anything's project site, so its three repos were checked and the page covers the family:
  segment-anything (2024-09-18, Apache-2.0), sam2 (2024-12-15, Apache-2.0) and sam3 (2026-11-17,
  Meta's own SAM License). RT-2 has no public code or weights; its row rests on the paper.
- LIBERO is widely used to compare VLAs, but its repo has had no commit for 20 months, so it is
  tier B.
- Index rows were not checked; their Last commit and Licence are `—`.
- Empty or wrong links: the survey's own title link is empty, CoWs on PASTURE's code link and
  LSC's paper link are empty, and L3MVN's "Project" link is its arXiv page. Nothing suspicious and
  no prompt-like text.

## Pages made

| Entry | Page | Tier |
|---|---|---|
| Habitat | [Habitat](../wiki/tools/habitat.md) | B |
| Grounding DINO | [Grounding DINO](../wiki/learning/models/grounding-dino.md) | B |
| Segment Anything | [Segment Anything (SAM, SAM 2, SAM 3)](../wiki/learning/models/segment-anything.md) | B |
| FoundationPose | [FoundationPose](../wiki/learning/models/foundationpose.md) | B |

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|
| RT-1 | `learning/rt-1` | B | learning | Google's robot transformer that set the large-scale imitation baseline; RT-1-X ships with Open X-Embodiment. Code frozen since 2023 |
| Rt-2 | `learning/rt-2` | B | learning | The first vision-language-action model, the idea OpenVLA and pi0 build on; its weights were never released |
| BEHAVIOR-1k | `learning/behavior-1k` | B | learning | Stanford's 1,000-activity household benchmark on its own OmniGibson simulator; active and MIT-licensed |
| LIBERO | `learning/libero` | B | learning | The usual simulated benchmark for fine-tuning and comparing VLAs such as OpenVLA and pi0 |

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| Section: Survey (1 paper) | The IJRR survey this list accompanies | — | — |
| Section: Neural Scaling Laws (1 paper) | A scaling-law study for embodied AI | — | — |
| Section: Robot Policy Learning for Decision-Making and Controls (9 papers) | Language-conditioned imitation learning and language-assisted RL | — | — |
| CLIPort | Language-conditioned pick-and-place policy; a common Ravens baseline | — | — |
| Perceiver-Actor | Voxel transformer policy; the usual RLBench multi-task baseline | — | — |
| Section: Language-Image Goal-Conditioned Value Learning (8 papers) | Language and image rewards and value maps, such as SayCan | — | — |
| Section: Robot Task Planning Using Large Language Models (11 papers) | LLM task planners, several tested in Minecraft | — | — |
| Section: LLM-Based Code Generation (6 papers) | LLMs writing robot programs, such as Code as Policies | — | — |
| Section: Robot Transformers (12 papers) | Transformer policies and visual pretraining for control | — | — |
| R3M | Pretrained visual encoder for manipulation; since overtaken by newer encoders | — | — |
| Section: In-context Learning for Decision-Making (5 papers) | In-context learning and reasoning for decisions | — | — |
| Section: Open-Vocabulary Robot Navigation and Manipulation (12 papers) | Zero-shot object navigation and open-vocabulary manipulation | — | — |
| VIMA | Multimodal-prompt manipulation policy with its VIMA-Bench suite | — | — |
| Section: Open-Vocabulary Object Detection and 3D Classification (8 papers) | Open-set 2D detectors and language-aligned point-cloud models | — | — |
| Simple Open-Vocabulary Object Detection with Vision Transformers | OWL-ViT detector; its successor OWLv2 is in Hugging Face Transformers | — | — |
| Section: Open-Vocabulary Semantic Segmentation (6 papers) | Language-driven and promptable segmentation models | — | — |
| Emerging Properties in Self-Supervised Vision Transformers | DINO; its successors DINOv2 and DINOv3 are common policy encoders | — | — |
| Fast segment anything | FastSAM, a faster CNN stand-in for SAM | — | — |
| Faster Segment Anything | MobileSAM, a lightweight SAM encoder for edge devices | — | — |
| Section: Open-Vocabulary 3D Scene Representations (5 papers) | Language-embedded NeRFs and semantic feature fields | — | — |
| Section: Object Representations (8 papers) | Object pose estimation, object fields and object-centric policies | — | — |
| Section: Affordance Information (2 papers) | Affordances learned from human videos and image generation | — | — |
| Section: Predictive Models (10 papers) | Video prediction, world models and diffusion planning | — | — |
| Robonet | 2019 multi-robot video dataset; superseded by Open X-Embodiment | — | — |
| Section: Relevant to Robotics (Embodied AI) (15 papers) | Embodied LLM agents, mostly in Minecraft and household simulators | — | — |
| Section: Generalist AI (4 papers) | Generalist agents such as Gato | — | — |
| Gibson Env | Indoor simulator from real scans; superseded by iGibson and OmniGibson | — | — |
| iGibson 2.0 | Household-task simulator; superseded by OmniGibson | — | — |
| RoboTHOR | AI2-THOR's sim-to-real navigation platform | — | — |
| VirtualHome | Program-driven household-activity simulator for agents | — | — |
| ARNOLD | Language-grounded manipulation benchmark on Isaac Sim | — | — |
| ALFRED | Instruction-following benchmark in AI2-THOR homes | — | — |
| ProcTHOR | Procedurally generated AI2-THOR houses for embodied AI | — | — |

## Deferred

| Entry | What it is | Phase |
|---|---|---|

## Rejected

| Entry | Why | Date |
|---|---|---|
| Habitat 2.0 | Duplicate: the same platform as Habitat, listed above it | 2026-11-18 |
