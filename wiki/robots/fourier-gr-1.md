---
type: robot
name: Fourier GR-1 and GR-2
summary: Full-size 1.65 m humanoid from Fourier with 32 FSA joints of up to 230 N·m and optional dexterous hands; the reference body for NVIDIA's GR00T N1, with GPL-3.0 URDFs and an MIT client SDK, but no public price.
tags: [humanoid, fourier, gr-1, gr-2, fsa, dexterous-hand, gr00t, robosuite, urdf, commercial]
category: humanoid
tier: B
openness: software-only
maker: Fourier (Fourier Intelligence)
year: 2023
license: {hardware: , software: GPL-3.0-only AND MIT, docs: }
links: {repo: "https://github.com/FFTAI/Wiki-GRx-Models", docs: "https://support-old.fftai.com/en/docs/GR-X-Humanoid-Robot/GR1/GR-1_Introduction/", cad: , paper: , site: "https://www.fftai.com/products-gr1"}
specs: {dof: 44, payload_kg: 3, reach_mm: , mass_kg: 52, size_mm: "1650 x 524 x 325", speed_mps: 1.39, runtime_h: 0.75}
stack: {actuators: "32 Fourier Smart Actuators (FSA), up to 230 N·m (maker's claim); Fourier 6-DoF dexterous hands or jaw grippers", mcu: , compute: "Intel i7-13700H mini PC (ASUS), Ubuntu 20.04 with ROS 2", sensors: ["Intel RealSense depth camera", "IMU"], sim_models: ["URDF (Wiki-GRx-Models: GR1T1 and GR1T2, with or without Fourier hands; GR-2; GR-3)", "MJCF (robosuite GR1 with Fourier hands)"], ros2: }
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2025-11-13, stars: 44, active: false}
use_cases: [research, imitation-learning, manipulation, locomotion]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://support-old.fftai.com/en/docs/GR-X-Humanoid-Robot/GR1/GR-1_Introduction/", title: "Fourier support docs: About GR-1", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/fourier-intelligence-launches-production-version-of-gr-1-humanoid-robot/", title: "The Robot Report: Fourier Intelligence launches production version of GR-1 humanoid robot (2023-12-29)", accessed: 2026-11-18}
  - {url: "https://github.com/FFTAI/Wiki-GRx-Models", title: Wiki-GRx-Models README, accessed: 2026-11-18}
  - {url: "https://github.com/FFTAI/fourier-grx-client", title: fourier-grx-client README, accessed: 2026-11-18}
  - {url: "https://github.com/ARISE-Initiative/robosuite", title: "robosuite repository (GR1 robot model)", accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2503.14734", title: "NVIDIA, GR00T N1: An Open Foundation Model for Generalist Humanoid Robots (2025)", accessed: 2026-11-18}
  - {url: "https://technode.global/prnasia/fourier-unveils-the-next-generation-humanoid-robot-gr-2", title: "Fourier unveils the next-generation humanoid robot GR-2 (press release, 2024-09-30)", accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/fourier_n1", title: "MuJoCo Menagerie: fourier_n1", accessed: 2026-11-18}
---

# Fourier GR-1 and GR-2

A full-size humanoid from Fourier of Shanghai, which also makes rehabilitation robots; the
production GR-1 launched at the end of 2023 [2]. It is the robot NVIDIA used to deploy its GR00T N1
foundation model [6], and simulators ship it for bimanual manipulation work [5]. Fourier publishes
URDFs and a client SDK, not the hardware. The GR-2 followed in 2024 [7].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | GR-1 (code name GR1T1) with Fourier dexterous hands | [3] |
| Degrees of freedom | 32 FSA body joints; "44/34" actuators, which matches two 6-DoF hands or two jaws; `dof: 44` | [1][3] |
| Size, mass | 1650 x 524 x 325 mm, arm span 1764 mm; about 52 kg (maker's claims) | [1] |
| Peak joint torque | 230 N·m (maker's claim); the 2023 launch report says 300 N·m at the hip | [1][2] |
| Speed, payload | walking 5 km/h; about 3 kg per hand (maker's claims) | [1] |
| Battery, runtime | 483 Wh lithium, 40 V nominal; about 60 min standing, 45 min walking; 315 min to charge | [1] |
| Power | 46.2 V supply, about 550 W maximum | [1] |
| Compute | Intel i7-13700H mini PC (ASUS), Ubuntu 20.04 with ROS 2 | [1] |
| Sensors | Intel RealSense depth camera, IMU | [1] |

## How it works

The body joints are Fourier Smart Actuators (FSA), the integrated actuator line Fourier released
with the production GR-1 [2]: 32 of them, rated at 46 V [1]. The URDF gives 6 joints per leg, 3 at
the waist, 7 per arm and 3 in the head [3]. The hands are Fourier's 6-DoF hand or an Inspire hand;
the "L" versions carry Fourier jaw grippers instead [3].

The robot PC runs Ubuntu 20.04 with ROS 2 [1], but this card found no published ROS 2 driver.
Fourier's control server installs on the robot as the `fourier-grx` package from PyPI, and the MIT
fourier-grx-client controls it from another machine; its README calls the software highly unstable
and says the older Wiki-GRx-Deploy repo is deprecated [4].

Wiki-GRx-Models holds URDFs for the GR1T1 and GR1T2, each with or without Fourier hands, plus the
GR-2 and GR-3, under GPL-3.0 [3]. robosuite (MIT) ships a GR1 MJCF with Fourier hands [5]. MuJoCo
Menagerie has no GR-1 model; it has one for Fourier's newer N1 [8].

| Variant | Notes | Source |
|---|---|---|
| GR-1 | GR1T1 with dexterous hands; 32 + 2 x 6 = 44 actuators | [1][3] |
| GR-1L | GR1T1 with Fourier jaw grippers; 32 + 2 = 34 actuators | [1][3] |
| GR-1 Pro, GR-1L Pro | GR1T2, with hands or jaws | [3] |
| GR-2 (2024) | 175 cm, 63 kg, 53 DoF with 12-DoF hands, FSA 2.0 over 380 N·m (maker's claims) | [7] |

## What it is used for

- Humanoid foundation models: NVIDIA deployed GR00T N1 on a GR-1 for language-conditioned
  bimanual manipulation [6].
- Simulated manipulation: robosuite's GR1 models, with fixed-lower-body and floating-body controller
  configurations [5].

## Cost and BOM

Price on request. The 2023 launch report says the production price was not announced [2], and none
of Fourier's pages read for this card give one [1], so the frontmatter `cost` stays empty.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Robot descriptions | URDF and meshes | [Wiki-GRx-Models](https://github.com/FFTAI/Wiki-GRx-Models) [3] | GPL-3.0 (LICENSE file) |
| Client SDK | Python | [fourier-grx-client](https://github.com/FFTAI/fourier-grx-client) [4] | MIT |
| Robot-side server | Python package on PyPI | `fourier-grx` [4] | Not stated in the sources read |
| MJCF model (third party) | MJCF | robosuite [5] | MIT |
| Hardware, FSA firmware | — | Not published | Closed |

## Strengths and limits

- **Strengths:** a full-size body with 230 N·m joints and dexterous hands [1][3]; the deployment
  robot for GR00T N1 [6]; maker URDFs for several versions [3] and an MJCF in robosuite [5].
- **Limits:** about 45 min of walking per charge [1]; no public price [2]; GPL-3.0 models [3]; an
  unstable, changing SDK [4]; no Menagerie model [8]; spec figures differ between sources [1][2].

## Related robots

- [Unitree H1](unitree-h1.md): the other common full-size research humanoid.
- [Unitree G1](unitree-g1.md), [Booster T1](booster-t1.md) and [AgiBot X1](agibot-x1.md): smaller
  research humanoids.

## Sources

1. [Fourier support docs: About GR-1](https://support-old.fftai.com/en/docs/GR-X-Humanoid-Robot/GR1/GR-1_Introduction/), accessed 2026-11-18
2. [The Robot Report: Fourier Intelligence launches production version of GR-1 humanoid robot (2023-12-29)](https://www.therobotreport.com/fourier-intelligence-launches-production-version-of-gr-1-humanoid-robot/), accessed 2026-11-18
3. [Wiki-GRx-Models README](https://github.com/FFTAI/Wiki-GRx-Models), accessed 2026-11-18
4. [fourier-grx-client README](https://github.com/FFTAI/fourier-grx-client), accessed 2026-11-18
5. [robosuite repository (GR1 robot model)](https://github.com/ARISE-Initiative/robosuite), accessed 2026-11-18
6. [NVIDIA, GR00T N1: An Open Foundation Model for Generalist Humanoid Robots (2025)](https://arxiv.org/abs/2503.14734), accessed 2026-11-18
7. [Fourier unveils the next-generation humanoid robot GR-2 (press release, 2024-09-30)](https://technode.global/prnasia/fourier-unveils-the-next-generation-humanoid-robot-gr-2), accessed 2026-11-18
8. [MuJoCo Menagerie: fourier_n1](https://github.com/google-deepmind/mujoco_menagerie/tree/main/fourier_n1), accessed 2026-11-18
