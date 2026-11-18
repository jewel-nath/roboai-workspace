---
type: robot
name: Shadow Dexterous Hand
summary: Commercial five-finger tendon-driven hand with 24 joints and 20 motors, the benchmark hand of OpenAI's Dactyl work; official ROS 1 software and maker-supplied MuJoCo models, price on request.
tags: [dexterous-hand, five-finger, tendon-driven, ethercat, ros1, mujoco, dactyl, commercial]
category: gripper
tier: B
openness: software-only
maker: The Shadow Robot Company
year:
license: {hardware: , software: BSD-3-Clause, docs: }
links: {repo: "https://github.com/shadow-robot/sr_common", docs: "https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/", cad: , paper: , site: "https://shadowrobot.com/dexterous-hand-series/"}
specs: {dof: 20, payload_kg: , reach_mm: , mass_kg: 4.3, size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "20 DC motors in the forearm, each pulling a pair of tendons (16 small Maxon motors with 131:1 gearheads, 4 large)", mcu: "PIC32 with an ET1200 EtherCAT chip in the palm", compute: "host PC over EtherCAT (Shadow supplies a NUC and a laptop)", sensors: ["Hall-effect joint angle sensors", "tendon load sensors (40)", "tactile fingertips", "IMU"], sim_models: ["MJCF (MuJoCo Menagerie, shadow_hand, E3M5)", "MJCF (MuJoCo Menagerie, shadow_dexee)", "URDF/Xacro (sr_common, sr_description)", "MJCF of the hand on a UR10 (sr_description, mujoco_models)", "Gazebo (official ROS 1 stack)", "Gymnasium Robotics hand tasks", "Isaac Gym task (IsaacGymEnvs, ShadowHand)"], ros2: none}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2025-01-09, stars: 36, active: false}
use_cases: [research, reinforcement-learning, manipulation]
evidence: vendor-claim
last_verified: 2026-11-18
sources:
  - {url: "https://shadowrobot.com/dexterous-hand-series/", title: Shadow Dexterous Hand series page, accessed: 2026-11-18}
  - {url: "https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/", title: Shadow Dexterous Hand documentation, accessed: 2026-11-18}
  - {url: "https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/md_motor_unit.html", title: "Shadow Dexterous Hand documentation: motor unit", accessed: 2026-11-18}
  - {url: "https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/md_position_sensors.html", title: "Shadow Dexterous Hand documentation: position sensors", accessed: 2026-11-18}
  - {url: "https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/ed_chipset.html", title: "Shadow Dexterous Hand documentation: chipset", accessed: 2026-11-18}
  - {url: "https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/sd_fingertips.html", title: "Shadow Dexterous Hand documentation: fingertips", accessed: 2026-11-18}
  - {url: "https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/fc_changelog.html", title: "Shadow Dexterous Hand documentation: changelog", accessed: 2026-11-18}
  - {url: "https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/sd_robot_description.html", title: "Shadow Dexterous Hand documentation: robot descriptions", accessed: 2026-11-18}
  - {url: "https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/mh_re_installing_the_software.html", title: "Shadow Dexterous Hand documentation: reinstalling the software", accessed: 2026-11-18}
  - {url: "https://github.com/shadow-robot/sr_common", title: sr_common repository README and licence, accessed: 2026-11-18}
  - {url: "https://github.com/shadow-robot/sr_core", title: sr_core repository, accessed: 2026-11-18}
  - {url: "https://github.com/shadow-robot/sr_interface", title: sr_interface repository, accessed: 2026-11-18}
  - {url: "https://github.com/shadow-robot", title: Shadow Robot GitHub organisation, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/shadow_hand", title: "MuJoCo Menagerie: Shadow Hand E3M5 description", accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/shadow_dexee", title: "MuJoCo Menagerie: Shadow DEX-EE description", accessed: 2026-11-18}
  - {url: "https://shadowrobot.com/DEX-EE/", title: Shadow DEX-EE product page, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/1808.00177", title: Learning Dexterous In-Hand Manipulation, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/1910.07113", title: "Solving Rubik's Cube with a Robot Hand", accessed: 2026-11-18}
  - {url: "https://robotics.farama.org/envs/shadow_dexterous_hand/", title: "Gymnasium Robotics: Shadow Dexterous Hand environments", accessed: 2026-11-18}
  - {url: "https://github.com/isaac-sim/IsaacGymEnvs/blob/main/isaacgymenvs/tasks/shadow_hand.py", title: IsaacGymEnvs ShadowHand task, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2309.06440", title: "LEAP Hand: Low-Cost, Efficient, and Anthropomorphic Hand for Robot Learning", accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2504.13165", title: "RUKA: Rethinking the Design of Humanoid Hands with Learning", accessed: 2026-11-18}
  - {url: "https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/md_finger.html", title: "Shadow Dexterous Hand documentation: finger", accessed: 2026-11-18}
  - {url: "https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/sd_repositories.html", title: "Shadow Dexterous Hand documentation: repositories", accessed: 2026-11-18}
---

# Shadow Dexterous Hand

A five-finger robot hand with a two-joint wrist, driven by twenty motors in the forearm that pull
tendons [1][3]. The Shadow Robot Company makes it. It is the hand OpenAI used to learn
in-hand cube reorientation and to solve a Rubik's Cube, and it remains the high-end reference
that open hands compare their cost and joint count with [17][18][21][22].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Dexterous Hand, the full five-digit model; MuJoCo Menagerie models its E3M5 version | [1][8][14] |
| Digits and joints | 4 fingers + thumb; 24 joints: 20 with their own motor, 4 coupled | [1] |
| Wrist | 2 joints, included | [1] |
| Actuators | 20 DC motors in the forearm, each pulling a pair of tendons to drive one joint or one coupled pair | [1][3][23] |
| Small motors | 16 x Maxon 118608 with 131:1 gearheads; 65 N continuous safe tendon load, 110 N at full power | [3] |
| Joint sensing | Hall-effect sensor on every joint | [4][5] |
| Force sensing | 40 tendon load sensors | [1] |
| Touch | 2 Shadow tactile fingertips as standard, up to 5; the docs also describe air-pressure (PST) tips | [1][6] |
| Other sensors | IMU; over 100 sensors in all, sampled at up to 1 kHz | [1] |
| Mass | 4.3 kg, a self-contained unit with the motors in the forearm (maker's claim) | [1][2][3] |
| Host link | EtherCAT, 1 kHz control loop | [1] |
| Payload and force | not published | [1] |

## How it works

Each motor sits in the forearm and drives one joint through two tendons, one per direction, with a
force sensor on each tendon at the motor; the controller uses these for compliant motion [3]. On
each finger the two outer joints share one motor, and the outer joint can never bend further than
the middle one; this is how 20 motors move 24 joints [1][23]. Hall-effect sensors measure every
joint angle, and a PIC32 processor in the palm samples the sensors and passes data to the host
through an ET1200 EtherCAT chip [4][5].

The hand ships with a NUC and a laptop with the software installed; Shadow gives customers a
one-line installer to reinstall or upgrade [9]. The official stack is ROS 1 Noetic: the current
release is 1.0.31, installed by Shadow's Aurora tool 2.2.5 [7][13]. Its code is split across
repositories: `sr_common` (URDF models and messages), `sr_core` (hardware and simulation),
`sr_interface` (high-level control) and `sr_hand_config` (customer-specific configuration), with
more tools in `sr_tools` and `sr_visualization` [10][11][12][24]. `sr_common` has branches for ROS 1
distributions up to Noetic and none for ROS 2 [10]. The URDF builder covers hand types E, G and C;
the E type comes in E3M5 and E2M3 versions [8].

For simulation, the ROS stack runs the hand in Gazebo [2]. Shadow supplied the E3M5 model in MuJoCo
Menagerie, and a DEX-EE model, both Apache-2.0 [14][15]; `sr_description` also has MuJoCo models of
the hand on a UR10 arm [10]. Gymnasium Robotics has Shadow hand reach and manipulation tasks, and
IsaacGymEnvs has a ShadowHand task [19][20].

| Variant | Digits | Motors, joints | Mass | Notes | Source |
|---|---|---|---|---|---|
| Dexterous Hand | 4 + thumb | 20, 24 with wrist | 4.3 kg | 40 tendon load sensors | [1] |
| Dexterous Hand Lite | 3 + thumb | 13, 16 | 2.4 kg | no wrist | [1] |
| Extra Lite | 2 + thumb | 10, 12 | 2.1 kg | no wrist | [1] |
| Super Lite | 1 + thumb | 7, 8 | 1.8 kg | no wrist | [1] |
| DEX-EE | 3 fingers | 12 DoF | 4.1 kg | made with Google DeepMind; dense tactile sensing; Chiral version with an offset third finger | [16] |

## What it is used for

- **Reinforcement learning in simulation, transferred to hardware:** OpenAI trained vision-based
  block reorientation on a Shadow Dexterous Hand in simulation, then solved a Rubik's Cube with
  it [17][18].
- **Benchmark tasks:** the Gymnasium Robotics hand tasks and the IsaacGymEnvs ShadowHand task use
  its model [19][20].
- **Reference point for open hands:** the LEAP Hand and RUKA papers list it as the costly,
  fully actuated comparison [21][22].

## Cost and BOM

Price on request: Shadow lists no prices and asks buyers to contact or book a call [1][16]. The
LEAP Hand paper gives about $100,000 for the Shadow Hand (2023), and the RUKA paper gives the same
figure (2025) [21][22]; these are the papers' figures, not quotes.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Hand description and messages | URDF/Xacro, meshes, ROS msgs | [sr_common](https://github.com/shadow-robot/sr_common) | BSD-3-Clause licence file; package.xml says GPL |
| Hardware and simulation drivers | ROS 1 packages | [sr_core](https://github.com/shadow-robot/sr_core) | GPL-2.0 |
| High-level control | ROS 1 packages | [sr_interface](https://github.com/shadow-robot/sr_interface) | BSD-3-Clause |
| Hand configuration, installer | ROS 1 packages, scripts | `sr_hand_config`, `aurora` | GPL-2.0 [13] |
| DEX-EE system files | config, CMake | `dx_system`, `dx_common` | BSD-3-Clause [13] |
| MuJoCo models | MJCF | MuJoCo Menagerie | Apache-2.0 [14][15] |
| Docs | web manual | readthedocs | not stated |
| CAD, electronics, firmware | not published | — | closed |

## Strengths and limits

- **Strengths:** the most human-like joint layout here, with five digits, a wrist and 24 joints
  [1]; joint, tendon-force and tactile sensing at 1 kHz [1]; maker-supplied MuJoCo models [14][15];
  a long record in learning research [17][18].
- **Limits:** price on request, about fifty times LEAP Hand's cost by that paper's count [21]; 4.3
  kg [1]; official software is ROS 1 only [7][10]; licences differ between
  repositories, and `sr_common` contradicts itself [10]; payload and fingertip force are not
  published [1].

## Related robots

- [Allegro Hand](allegro-hand.md): the cheaper commercial four-finger reference.
- [LEAP Hand](leap-hand.md), [RUKA](ruka.md) and [Aero Hand Open](aero-hand-open.md): open hands
  that compare themselves with it.
- [TriFinger](trifinger.md): another three-finger dexterity platform, like DEX-EE.
- [Universal Robots](universal-robots.md): Shadow's MuJoCo models mount the hand on a UR10 [10].

## Sources

1. [Shadow Dexterous Hand series page](https://shadowrobot.com/dexterous-hand-series/), accessed 2026-11-18
2. [Shadow Dexterous Hand documentation](https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/), accessed 2026-11-18
3. [Shadow Dexterous Hand documentation: motor unit](https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/md_motor_unit.html), accessed 2026-11-18
4. [Shadow Dexterous Hand documentation: position sensors](https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/md_position_sensors.html), accessed 2026-11-18
5. [Shadow Dexterous Hand documentation: chipset](https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/ed_chipset.html), accessed 2026-11-18
6. [Shadow Dexterous Hand documentation: fingertips](https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/sd_fingertips.html), accessed 2026-11-18
7. [Shadow Dexterous Hand documentation: changelog](https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/fc_changelog.html), accessed 2026-11-18
8. [Shadow Dexterous Hand documentation: robot descriptions](https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/sd_robot_description.html), accessed 2026-11-18
9. [Shadow Dexterous Hand documentation: reinstalling the software](https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/mh_re_installing_the_software.html), accessed 2026-11-18
10. [sr_common repository README and licence](https://github.com/shadow-robot/sr_common), accessed 2026-11-18
11. [sr_core repository](https://github.com/shadow-robot/sr_core), accessed 2026-11-18
12. [sr_interface repository](https://github.com/shadow-robot/sr_interface), accessed 2026-11-18
13. [Shadow Robot GitHub organisation](https://github.com/shadow-robot), accessed 2026-11-18
14. [MuJoCo Menagerie: Shadow Hand E3M5 description](https://github.com/google-deepmind/mujoco_menagerie/tree/main/shadow_hand), accessed 2026-11-18
15. [MuJoCo Menagerie: Shadow DEX-EE description](https://github.com/google-deepmind/mujoco_menagerie/tree/main/shadow_dexee), accessed 2026-11-18
16. [Shadow DEX-EE product page](https://shadowrobot.com/DEX-EE/), accessed 2026-11-18
17. [Learning Dexterous In-Hand Manipulation](https://arxiv.org/abs/1808.00177), accessed 2026-11-18
18. [Solving Rubik's Cube with a Robot Hand](https://arxiv.org/abs/1910.07113), accessed 2026-11-18
19. [Gymnasium Robotics: Shadow Dexterous Hand environments](https://robotics.farama.org/envs/shadow_dexterous_hand/), accessed 2026-11-18
20. [IsaacGymEnvs ShadowHand task](https://github.com/isaac-sim/IsaacGymEnvs/blob/main/isaacgymenvs/tasks/shadow_hand.py), accessed 2026-11-18
21. [LEAP Hand: Low-Cost, Efficient, and Anthropomorphic Hand for Robot Learning](https://arxiv.org/abs/2309.06440), accessed 2026-11-18
22. [RUKA: Rethinking the Design of Humanoid Hands with Learning](https://arxiv.org/abs/2504.13165), accessed 2026-11-18
23. [Shadow Dexterous Hand documentation: finger](https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/md_finger.html), accessed 2026-11-18
24. [Shadow Dexterous Hand documentation: repositories](https://shadow-robot-company-dexterous-hand.readthedocs-hosted.com/en/latest/user_guide/sd_repositories.html), accessed 2026-11-18
