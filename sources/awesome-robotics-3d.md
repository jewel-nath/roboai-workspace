---
type: source
name: Awesome Robotics 3D
registry: awesome-robotics-3d
url: https://github.com/zubair-irshad/Awesome-Robotics-3D
commit: "6a8573c"
read_on: 2026-11-18
counts: {entries: 32, pages: 0, waiting: 5, index_only: 25, deferred: 0, rejected: 2}
---

# Awesome Robotics 3D: what it gives RoboAI

A list of about 100 papers on 3D vision for robots in the era of LLMs and VLMs: point-cloud and
multi-view manipulation policies, 3D pretraining, spatial-reasoning VLMs, feature fields and
Gaussian splats, and a mixed section of simulators, datasets and benchmarks. For a builder its
value is narrow: 3D Diffusion Policy as a point-cloud alternative to image policies, and the DROID,
RoboCasa, ManiSkill and Habitat entries. The rest is research to read, not tools to install, and
many entries carry copy-paste errors in their titles and links.

## How it was read

- Read at commit `6a8573c` (last commit 2025-12-17) on 2026-11-18: the README, `how-to-PR.md` and
  `CITATION.cff`, which still names the author's older Awesome-Implicit-NeRF-Robotics list.
- **Paper sections:** the survey bullets at the top and the Policy Learning, Pretraining, VLM and
  LLM, and Representation sections hold only papers, so each is one index row with its count as
  listed (87 papers). Policy Learning lists PolarNet twice.
- Papers whose code builders use have their own rows as well: 3D Diffusion Policy waits for a page;
  3D Diffuser Actor, RVT, PerAct, CLIPort, VLMaps and ConceptGraphs are index only.
- Simulations, Datasets and Benchmarks (20 entries) is triaged entry by entry. Its first two
  entries, RoboTracer and RoboRefer, repeat papers from VLM and LLM.
- Page candidates were checked with a blobless shallow clone (last commit, licence file):
  3D Diffusion Policy (2025-10-16, MIT); RoboCasa (2026-11-12, MIT); habitat-lab (2026-05-07,
  MIT). ManiSkill2's repo now only points to `haosulab/ManiSkill` (ManiSkill3; 2026-08-01,
  Apache-2.0). DROID's platform repo (2025-09-15) has no licence file and the dataset's licence was
  not found on its site; LeRobot's converted copy is tagged Apache-2.0. Confirm it before the page
  is written.
- Index rows were not checked; their Last commit and Licence are `—`.
- **Errors in the list:** RVT carries 3D Diffusion Policy's subtitle, Gen2Sim carries RH20T's and
  3D-LLM carries MOKA's; CLIPort's links go to PolarNet and PerAct's webpage to CLIPort; PolarNet's
  and RoboPoint's paper links point to other papers (Act3D, RL3D). Broken links: 3D Diffusion
  Policy's webpage, RoboUniView's and VLMaps' code, JCR's paper. Open6DOR's "Code" link is a
  temporary gradio.live demo URL.
- The README loads a third-party visitor-counter image (`visitor-badge.laobi.icu`). No prompt-like
  text.

## Pages made

| Entry | Page | Tier |
|---|---|---|

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|
| 3D Diffusion Policy | `learning/3d-diffusion-policy` | B | learning | Diffusion Policy on sparse point clouds; learns from few demonstrations and is the common 3D imitation baseline |
| DROID | `learning/droid` | A | learning | Large in-the-wild Franka manipulation dataset with a reproducible collection platform; used to train and test VLAs |
| RoboCasa | `learning/robocasa` | B | learning | Large robosuite-based kitchen simulation with tasks and assets for training generalist policies; active |
| ManiSkill2 | `learning/maniskill` | A | learning | Earlier ManiSkill; its repo now points to ManiSkill3, a GPU-parallel manipulation simulator and benchmark |
| Habitat 2.0 | `tools/habitat` | B | sim | Meta's fast embodied-AI simulator for navigation and rearrangement; the standard in indoor-navigation research |

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| Section: Other relevant survey papers (4 papers) | Surveys on neural fields, 3D LLMs, splatting and 3D manipulation | — | — |
| Section: Policy Learning (22 papers) | 3D-input manipulation policies, mostly tested on RLBench | — | — |
| 3D Diffuser Actor | Diffusion policy over 3D scene tokens; strong RLBench and CALVIN baseline | — | — |
| RVT | NVIDIA's multi-view transformer policy; RVT-2 shares its repo | — | — |
| Perceiver-Actor | Voxel transformer policy; the usual RLBench multi-task baseline | — | — |
| CLIPort | Language-conditioned pick-and-place policy; a common Ravens baseline | — | — |
| Section: Pretraining (8 papers) | 3D and multi-view visual pretraining for manipulation | — | — |
| Section: VLM and LLM (31 papers) | VLMs and LLMs for spatial reasoning, grasping and affordances | — | — |
| VLMaps | Open-vocabulary navigation maps built from visual-language features | — | — |
| Section: Representation (22 papers) | Feature fields, Gaussian splats and scene graphs for manipulation | — | — |
| ConceptGraphs | Open-vocabulary 3D scene graphs from RGB-D for planning | — | — |
| The Colosseum | RLBench-based benchmark testing policies under scene perturbations | — | — |
| OpenEQA | Meta's embodied question-answering benchmark for foundation models | — | — |
| RH20T | Multi-robot manipulation dataset with paired human demonstrations | — | — |
| Gen2Sim | Generates simulation assets and tasks with generative models | — | — |
| BEHAVIOR Vision Suite | Synthetic vision-data generator built on OmniGibson | — | — |
| ARNOLD | Language-grounded manipulation benchmark on Isaac Sim | — | — |
| VIMA | Multimodal-prompt manipulation policy with its VIMA-Bench suite | — | — |
| Robo360 | Multi-view, multi-material manipulation dataset; no code linked | — | — |
| AR2-D2 | Collects robot demonstrations through a phone AR app | — | — |
| VL-Grasp | Language-conditioned 6-DoF grasping dataset and policy | — | — |
| OCID-Ref | Referring-expression dataset over cluttered OCID tabletop scenes | — | — |
| ManipulaTHOR | AI2-THOR's arm-manipulation extension | — | — |
| RoboTHOR | AI2-THOR's sim-to-real navigation platform | — | — |
| HabiCrowd | Crowd-aware navigation simulator built on Habitat | — | — |

## Deferred

| Entry | What it is | Phase |
|---|---|---|

## Rejected

| Entry | Why | Date |
|---|---|---|
| RoboTracer (second listing) | Duplicate: already listed under VLM and LLM | 2026-11-18 |
| RoboRefer (second listing) | Duplicate: already listed under VLM and LLM | 2026-11-18 |
