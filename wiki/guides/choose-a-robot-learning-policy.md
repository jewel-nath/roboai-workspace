---
type: guide
name: Choose a robot learning policy
summary: Which policy to train or fine-tune first so a robot learns a task - ACT, Diffusion Policy or DP3 from your own demonstrations, a pretrained VLA (SmolVLA, pi0.5, GR00T N1.7, OpenVLA, Octo, RDT) fine-tuned on them, or RL in simulation with Isaac Lab, ManiSkill or Stable-Baselines3 - decided by the robot, demonstrations, cameras, training GPU, robot computer, control rate and the licences of code, weights and data.
tags: [robot-learning, imitation-learning, reinforcement-learning, vla, vision-language-action, act, diffusion-policy, dp3, smolvla, pi0, pi05, openpi, gr00t, openvla, octo, rdt, rt-1, rt-2, lerobot, isaac-lab, maniskill, stable-baselines3, libero, simplerenv, robocasa, so-101, humanoid, jetson, remote-inference]
question: Which policy should I train or fine-tune first for my robot?
options: [act, diffusion-policy, 3d-diffusion-policy, smolvla, pi0, gr00t, openvla, octo, rdt, isaac-lab, maniskill, stable-baselines3]
recommendation: "ACT in LeRobot from about 50 demonstrations for one task on one arm; SmolVLA when one policy must follow language across tasks on a consumer GPU; pi0.5 or GR00T N1.7 only with a 40 GB-class training GPU and their weight terms read; Isaac Lab with RSL-RL PPO for locomotion, balance and in-hand skills nobody can teleoperate."
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://github.com/huggingface/lerobot/tree/main/docs/source", title: "LeRobot main (b07adcc): docs hardware_guide, act, smolvla, pi0, pi05, groot, inference, libero; pi0, pi05 and pi0_fast configs; pyproject.toml", accessed: 2026-11-25}
  - {url: "https://github.com/huggingface/lerobot/blob/main/src/lerobot/remote_inference/README.md", title: "LeRobot remote inference: design reference and policy support table", accessed: 2026-11-25}
  - {url: "https://github.com/Physical-Intelligence/openpi", title: "openpi main (215abfb): README, LICENSE, LICENSE_GEMMA.txt, pyproject.toml", accessed: 2026-11-25}
  - {url: "https://huggingface.co/lerobot/pi05_base", title: "Hugging Face licence tags: lerobot/pi0_base, lerobot/pi05_base, lerobot/smolvla_base, google/paligemma-3b-pt-224, LIBERO and DROID dataset copies", accessed: 2026-11-25}
  - {url: "https://github.com/NVIDIA/Isaac-GR00T", title: "Isaac-GR00T main (708617f): README, FAQ, hardware recommendation, real-world deployment guide, deployment README", accessed: 2026-11-25}
  - {url: "https://huggingface.co/nvidia/GR00T-N1.7-3B", title: "Hugging Face nvidia/GR00T-N1.7-3B: model card, LICENSE and commit history; N1.5 and N1.6 LICENSE files", accessed: 2026-11-25}
  - {url: "https://developer.nvidia.com/isaac/gr00t/llm-info.md", title: "NVIDIA: LLM Info - NVIDIA Isaac GR00T (last updated August 2026)", accessed: 2026-11-25}
  - {url: "https://isaac-sim.github.io/IsaacLab/main/source/isaaclab/environments.html", title: "Isaac Lab docs (main): available environments", accessed: 2026-11-25}
  - {url: "https://github.com/mani-skill/ManiSkill", title: "ManiSkill repository: README licence section", accessed: 2026-11-25}
  - {url: "https://nvidia-isaac-ros.github.io/releases/index.html", title: "Isaac ROS release notes (4.0.0 to 5.1.0)", accessed: 2026-11-25}
  - {url: "https://nvidia-isaac-ros.github.io/v/release-4.6/repositories_and_packages/isaac_ros_deploy/index.html", title: "Isaac ROS docs: Isaac ROS Deploy (release 4.6, and latest)", accessed: 2026-11-25}
  - {url: "https://docs.nvidia.com/deeplearning/tensorrt/latest/api/migration/tensorrt-10x-to-11x-jetson.html", title: "TensorRT: migrating from 10.x to 11.x on Jetson/JetPack", accessed: 2026-11-25}
  - {url: "https://github.com/Lifelong-Robot-Learning/LIBERO", title: "LIBERO repository: README licence table", accessed: 2026-11-25}
---

# Choose a robot learning policy

Which policy should you train or fine-tune first so your robot learns a task? For builders who
can teleoperate demonstrations on a low-cost arm such as [SO-101](../robots/so-101.md), a cobot,
a bimanual rig or a humanoid, and for legged skills learned by RL in simulation. Steps:
[learn-robot-learning](../../skills/learn-robot-learning/SKILL.md); on the robot's computer:
[learn-edge-deployment](../../skills/learn-edge-deployment/SKILL.md).

## Short answer

- **One task, your own demonstrations:** [ACT](../learning/policies/act.md) in
  [LeRobot](../learning/frameworks/lerobot.md), about 50 episodes, 2 to 6 GB of VRAM; for demos
  that solve it in several ways, [Diffusion Policy](../learning/policies/diffusion-policy.md),
  8 to 14 GB [1].
- **Several tasks named in language, one consumer GPU:** [SmolVLA](../learning/models/smolvla.md)
  (450M, code and weights Apache-2.0), fine-tuned on about 50 episodes in 10 to 16 GB [1][4].
- **Harder tasks, a 40 GB-class training GPU, a cobot, bimanual arm or humanoid:** pi0.5
  ([π0 family](../learning/models/pi0.md)) in LeRobot or openpi, or
  [GR00T N1.7](../learning/models/gr00t.md); read their weight terms first [3][4][6].
- **Locomotion, balance, in-hand reorientation:** RL in
  [Isaac Lab](../learning/frameworks/isaac-lab.md) with RSL-RL PPO, then
  [sim-to-real](../../skills/sim-to-real/SKILL.md) [8].
- **History, not options:** [RT-1](../learning/models/rt-1.md) is archived,
  [RT-2](../learning/models/rt-2.md) never released, [Octo](../learning/models/octo.md)
  unmaintained; [OpenVLA](../learning/models/openvla.md) and [RDT](../learning/models/rdt.md) are
  quiet research code, for reproducing papers.

## What decides it

- **One task or many, imitation or RL.** ACT, Diffusion Policy and
  [DP3](../learning/policies/3d-diffusion-policy.md) learn one task and take no text; a VLA
  follows instructions across tasks, for a bigger GPU. Imitate what a person can teleoperate. Use
  RL, given a good simulator model, for what nobody can demonstrate: Isaac Lab ships velocity
  tasks for G1, H1, Go2, ANYmal-D and Cassie, and cube reorientation with Allegro and Shadow
  hands [8]. For contact-rich arm tasks, imitate first, then add human corrections
  (`--strategy.type=dagger`) or HIL-SERL ([skill](../../skills/learn-robot-learning/SKILL.md)).
- **The robot.** LeRobot drives the SO-101, Koch, LeKiwi, OMX, Reachy 2 and Unitree G1 itself
  ([LeRobot](../learning/frameworks/lerobot.md)). openpi's base models know PI's mix (ALOHA,
  Franka, UR5e, ARX); its DROID and ALOHA checkpoints run only on those rigs
  ([π0](../learning/models/pi0.md)). GR00T N1.7 runs zero-shot only on its pretraining robots,
  such as the DROID Franka and G1 ([GR00T](../learning/models/gr00t.md)). RDT targets dual arms.
- **Demonstrations.** ACT and SmolVLA: about 50, about 10 per object position or variation [1].
  GR00T: 100 or more (about 30 for narrow tasks), 500+ for multi-step and 2,000+ for humanoid
  tasks, by NVIDIA's guidance [5]. DP3's authors learned most of 72 simulated tasks from 10.
- **Cameras.** RGB serves all but DP3, which needs a good depth camera (its authors warn a
  RealSense D435 may fall short). Names, count and size at rollout must match training; SmolVLA
  expects `camera1` to `camera3`, openpi up to three 224 x 224 views.
- **Training GPU.** LeRobot's indicative peaks at batch 8: ACT 2 to 6 GB, Diffusion 8 to 14,
  SmolVLA 10 to 16, the pi0 family and GR00T 24 to 40 GB; no CPU training [1]. openpi asks for
  more than 22.5 GB for LoRA and 70 GB for full fine-tuning [3], Isaac-GR00T 40 GB+ [5].
- **The robot's computer.** On an RTX 4090 LeRobot measured ACT at about 5 ms per pass and
  Diffusion Policy at about 370 ms ([page](../learning/policies/diffusion-policy.md)). VLAs often
  run off-board: `lerobot-policy-server` on a GPU host, `lerobot-rollout --inference.type=remote`
  on the robot; ACT and SmolVLA have run so on hardware, pi0 and pi0.5 not yet, Diffusion Policy
  cannot [2]. GR00T N1.7 has a TensorRT path for Jetson: 12.4 replans per second on AGX Thor and
  6.6 on Orin, NVIDIA's figures [5]. No upstream Jetson figures exist for ACT, Diffusion Policy or
  SmolVLA; measure ([learn-edge-deployment](../../skills/learn-edge-deployment/SKILL.md)).
- **Control rate.** Chunks count dataset steps: ACT's default 100-step chunk lasts 3.3 s at
  30 fps, where its authors aim for about 1 s ([ACT](../learning/policies/act.md)). GR00T replans
  near 10 Hz to feed a 30 Hz robot [5]; `--inference.type=rtc` overlaps inference and motion for
  pi0, pi0.5 and SmolVLA [1].
- **Licences of code, weights and data.** pi0 and pi0.5: LeRobot's docs say Apache-2.0, but the
  Hub cards tag the weights `gemma` and openpi ships the Gemma Terms of Use beside its Apache-2.0
  code: treat weights and fine-tunes as Gemma derivatives; LeRobot's pi0, pi0-FAST and pi0.5 load
  the gated PaliGemma tokenizer [1][3][4]. GR00T N1.7's LICENSE file is the NVIDIA Open Model
  License (commercial use allowed) since 2026-11-10, though NVIDIA's info page still says
  non-commercial; N1.5 and N1.6 are non-commercial [6][7]. Data: ManiSkill assets CC BY-NC 4.0 [9];
  LIBERO data CC BY 4.0 by its README, Apache-2.0 on `lerobot/libero` [4][13].

## Options compared

| Option | Cost (licence, GPU, data) | Strengths | Limits | Best when |
|---|---|---|---|---|
| ACT | MIT (original), Apache-2.0 (LeRobot); 2-6 GB; ~50 demos [1] | Light and fast; LeRobot's first pick; copes with imprecise low-cost arms | One task; tune chunk length to the rate; original repo frozen | One task on an SO-101, Koch or ALOHA |
| Diffusion Policy | MIT, Apache-2.0 (LeRobot); 8-14 GB [1]; 90-284 demos in the paper | Demos with several valid strategies; strong single-task baseline | ~370 ms per chunk on an RTX 4090 (LeRobot); not on the remote server [2]; LeRobot 0.6 changed horizons | Multimodal demos, a desktop GPU near the robot |
| 3D Diffusion Policy | MIT; ~10 GB on an A40 (authors); 10-40 demos | Point clouds, few demos, dexterous hands | Idle research code, Python 3.8 stack; no LeRobot port; depth quality decides | A fixed workspace with a good depth camera |
| SmolVLA | Apache-2.0 code and weights; 10-16 GB [1][4]; ~50 demos | Language and several tasks on one consumer GPU; remote and RTC tested on hardware [2] | Smaller than pi0.5 and GR00T; pretrained mostly on SO-100 data | A hobby arm with several tasks |
| pi0 / pi0.5 (openpi or LeRobot) | Code Apache-2.0, weights Gemma terms; >22.5 GB LoRA, >70 GB full [3] | Strong generalist; DROID and ALOHA checkpoints; 96.85% on LIBERO (PI) [1] | Gated tokenizer; openpi pins Python 3.11 and reads v2.1 data; PI calls it an experiment [3] | Cobots and bimanual arms, a large GPU |
| GR00T N1.7 | Code Apache-2.0, weights NVIDIA Open Model License; 40 GB+ to fine-tune, 16 GB+ to run [5][6] | Humanoids and arms; TensorRT on Thor and Orin; Isaac ROS G1 workflow [10] | Gated backbone; Linux and NVIDIA only; v2.1 data plus `modality.json`; 100+ demos | A humanoid, or an NVIDIA edge stack |
| OpenVLA (and OFT) | MIT code, Llama 2 terms on weights; ~15 GB bf16 to run, ~27 GB LoRA | The common open VLA baseline; RLDS and OXE data | Quiet since 2025; ignores the image on transformers 4.50+ | Reproducing published VLA comparisons |
| Octo | MIT code and weights; ~5 h on a 24 GB GPU to fine-tune | Small; language or goal images | Unmaintained since 2024-07; install fails on import | Reproducing papers only |
| RDT-1B, RDT2 | MIT; Apache-2.0; RDT2 ~16 GB | Dual-arm pretraining; RDT2 zero-shot on UMI hardware | Research code, no LeRobot port; RDT-1B used 6,000+ episodes, 150K+ steps | A dual-arm research rig |
| Isaac Lab | BSD-3-Clause, Isaac Sim parts NVIDIA terms; NVIDIA GPU; no demos | Thousands of GPU environments; locomotion and in-hand tasks [8]; ONNX export | NVIDIA only; 3.0 breaks 2.x code; actuator and latency gaps to close | Legged, humanoid and dexterous RL |
| ManiSkill | Apache-2.0 code, CC BY-NC 4.0 assets [9]; NVIDIA GPU on Linux for GPU sim | GPU-parallel manipulation RL; demos; SO100 sim-to-real example | Non-commercial assets; slowing upkeep; no Jetson wheel | Manipulation RL research |
| Stable-Baselines3 | MIT; CPU is fine | Tested PPO, SAC, TD3 on any Gymnasium environment | Slow with thousands of GPU environments | A small environment you wrote |

## Check a policy before you trust it

- **Offline checks find setup mistakes.** Loss and open-loop replay do not predict closed-loop
  success ([evaluation](../../skills/learn-robot-learning/references/evaluation.md)).
- **Simulated benchmarks compare methods.** [LIBERO](../learning/benchmarks/libero.md) is
  saturated: pi0.5 scores 96.85% (PI) and 97.5% (LeRobot's re-run), and at 10 episodes a 9/10
  task spans about 60 to 98% at 95% confidence [1].
  [SimplerEnv](../learning/benchmarks/simpler-env.md) fits Google Robot and WidowX policies only;
  on the [RoboCasa](../learning/benchmarks/robocasa.md) leaderboard pi0 scores 14.8, pi0.5 16.9
  and GR00T N1.5 23.9. None of these predicts your robot.
- **The real robot decides.** Rehearse in simulation ([choose a simulator](choose-a-simulator.md)),
  then fixed start conditions, 20 trials or more, k/N with a Wilson interval,
  `--robot.max_relative_target` set, low speed first, an e-stop in reach.
- **Paper numbers rarely transfer.** ACT's 84 to 96% on four tasks came from ALOHA with four
  cameras at 50 Hz; PI says pi0 "may or may not work for you" [3]; GR00T runs vary 5 to 6% from
  augmentation alone. Your robot's cameras, rate, action conventions and normalisation differ.

## When the answer changes

- **openpi rather than LeRobot for pi0.5:** for JAX LoRA, PI's statistics and the DROID and
  ALOHA checkpoints. openpi reads LeRobot v2.1 data while LeRobot 0.7 records v3.0; convert with
  GR00T's helper into a separate root
  ([openpi and GR00T](../../skills/learn-robot-learning/references/openpi-groot.md)).
- **GR00T N2** was previewed at GTC 2026 but is not released; LeRobot supports N1.7 only [7].
- **A Jetson on the robot.** GR00T's Jetson path needs JetPack 7.2 [5]. TensorRT 11 reaches
  Jetson only as 11.4.1 on JetPack 7.2.2; the 11.5 that pip installs does not support JetPack
  [12]. Isaac ROS 4.6 is the Jazzy line on JetPack 7.2, 5.x is Lyrical; the G1 GR00T workflow
  came in 4.5 and 5.1 restored it on Lyrical [10]. Isaac ROS Deploy runs Isaac Lab policies
  exported with LEAPP through Triton, on Jazzy (4.6) and Lyrical [11].
- **No NVIDIA GPU.** ACT trains slowly on Apple Silicon (6 to 14 h for 5 epochs on an M-series
  Max) [1]; SB3 runs RL on the CPU, and ManiSkill simulates on the CPU on Windows and macOS.
- **A commercial product.** Avoid ManiSkill assets, GR00T N1.5 and N1.6,
  [BEHAVIOR-1K](../learning/benchmarks/behavior-1k.md) scenes and
  [RLBench](../learning/benchmarks/rlbench.md); credit CC BY data; ship the Gemma or NVIDIA notices.

## Sources

1. [LeRobot main (b07adcc): docs hardware_guide, act, smolvla, pi0, pi05, groot, inference, libero; pi0, pi05 and pi0_fast configs; pyproject.toml](https://github.com/huggingface/lerobot/tree/main/docs/source), accessed 2026-11-25
2. [LeRobot remote inference: design reference and policy support table](https://github.com/huggingface/lerobot/blob/main/src/lerobot/remote_inference/README.md), accessed 2026-11-25
3. [openpi main (215abfb): README, LICENSE, LICENSE_GEMMA.txt, pyproject.toml](https://github.com/Physical-Intelligence/openpi), accessed 2026-11-25
4. [Hugging Face licence tags: lerobot/pi0_base, lerobot/pi05_base, lerobot/smolvla_base, google/paligemma-3b-pt-224, LIBERO and DROID dataset copies](https://huggingface.co/lerobot/pi05_base), accessed 2026-11-25
5. [Isaac-GR00T main (708617f): README, FAQ, hardware recommendation, real-world deployment guide, deployment README](https://github.com/NVIDIA/Isaac-GR00T), accessed 2026-11-25
6. [Hugging Face nvidia/GR00T-N1.7-3B: model card, LICENSE and commit history; N1.5 and N1.6 LICENSE files](https://huggingface.co/nvidia/GR00T-N1.7-3B), accessed 2026-11-25
7. [NVIDIA: LLM Info - NVIDIA Isaac GR00T (last updated August 2026)](https://developer.nvidia.com/isaac/gr00t/llm-info.md), accessed 2026-11-25
8. [Isaac Lab docs (main): available environments](https://isaac-sim.github.io/IsaacLab/main/source/isaaclab/environments.html), accessed 2026-11-25
9. [ManiSkill repository: README licence section](https://github.com/mani-skill/ManiSkill), accessed 2026-11-25
10. [Isaac ROS release notes (4.0.0 to 5.1.0)](https://nvidia-isaac-ros.github.io/releases/index.html), accessed 2026-11-25
11. [Isaac ROS docs: Isaac ROS Deploy (release 4.6, and latest)](https://nvidia-isaac-ros.github.io/v/release-4.6/repositories_and_packages/isaac_ros_deploy/index.html), accessed 2026-11-25
12. [TensorRT: migrating from 10.x to 11.x on Jetson/JetPack](https://docs.nvidia.com/deeplearning/tensorrt/latest/api/migration/tensorrt-10x-to-11x-jetson.html), accessed 2026-11-25
13. [LIBERO repository: README licence table](https://github.com/Lifelong-Robot-Learning/LIBERO), accessed 2026-11-25
