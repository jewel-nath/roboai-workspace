---
type: robot
name: RUKA
summary: Human-sized five-finger tendon hand from NYU, 11 Dynamixel servos in the forearm and learned controllers instead of joint encoders, about $1,300 in parts; code is MIT, but the CAD states no licence.
tags: [dexterous-hand, five-finger, tendon-driven, dynamixel, 3d-printed, learned-control, manus-glove, mujoco]
category: gripper
tier: B
openness: partial
maker: New York University
year: 2025
license: {hardware: , software: MIT, docs: }
links: {repo: "https://github.com/ruka-hand/RUKA", docs: "https://ruka.gitbook.io/instructions", cad: "https://cad.onshape.com/documents/6be13b87a3aad01bd61ef6ab/w/86f8cbb4c7b89f36daabaded/e/5b18eb8a388f7b1857d3fdb3", paper: "https://arxiv.org/abs/2504.13165", site: "https://ruka-hand.github.io"}
specs: {dof: 11, payload_kg: 6, reach_mm: , mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "11 Dynamixel servos in the forearm pulling tendons: 8 x XL330-M288-T for the fingers, 3 x XM430 for the thumb", mcu: "none; a Dynamixel U2D2 USB adapter", compute: "host PC over USB; a MANUS glove to collect controller training data", sensors: ["servo encoders (11)"], sim_models: ["MJCF (RUKA repo, assets/xml)"], ros2: none}
cost: {type: bom, usd: 1307.11, as_of: 2025-02-19, source: "https://docs.google.com/spreadsheets/d/1bi4XM1knMoRTz975P-abTXNx2L5BT7-KNwVOGFRxrvw/edit?gid=1155455594"}
build: {difficulty: 3, hours: 7, print_hours: 24}
maturity: {last_commit: 2025-08-11, stars: 202, active: false}
use_cases: [research, teleop, reinforcement-learning, manipulation]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/ruka-hand/RUKA", title: RUKA repository README, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2504.13165", title: "RUKA: Rethinking the Design of Humanoid Hands with Learning", accessed: 2026-11-18}
  - {url: "https://ruka-hand.github.io", title: RUKA project page, accessed: 2026-11-18}
  - {url: "https://ruka.gitbook.io/instructions", title: RUKA hardware instructions, introduction, accessed: 2026-11-18}
  - {url: "https://docs.google.com/spreadsheets/d/1bi4XM1knMoRTz975P-abTXNx2L5BT7-KNwVOGFRxrvw/edit?gid=1155455594", title: RUKA single-hand bill of materials (sheet), accessed: 2026-11-18}
  - {url: "https://ruka.gitbook.io/instructions/hardware/bill-of-materials", title: RUKA bill of materials and tools page, accessed: 2026-11-18}
  - {url: "https://ruka.gitbook.io/instructions/hardware/3d-print-parts", title: RUKA 3D print parts, accessed: 2026-11-18}
  - {url: "https://ruka.gitbook.io/instructions/hardware/power-supply-and-wiring-harness-assembly", title: RUKA power supply and wiring harness assembly, accessed: 2026-11-18}
  - {url: "https://ruka.gitbook.io/instructions/hardware/robot-arm-mounts", title: RUKA robot arm mounts, accessed: 2026-11-18}
  - {url: "https://cad.onshape.com/documents/6be13b87a3aad01bd61ef6ab/w/86f8cbb4c7b89f36daabaded/e/5b18eb8a388f7b1857d3fdb3", title: RUKA Onshape CAD, accessed: 2026-11-18}
  - {url: "https://github.com/ruka-hand/RUKA/blob/main/LICENSE", title: RUKA licence file, accessed: 2026-11-18}
  - {url: "https://osf.io/hwajz/", title: RUKA controller checkpoints and data (OSF), accessed: 2026-11-18}
---

# RUKA

A human-sized, five-finger robot hand in which eleven servos in the forearm pull tendons to move
fifteen joints, published by New York University at RSS 2025 [2][3]. It has no joint encoders:
per-finger neural networks, trained on data from a motion-capture glove, turn fingertip targets
into motor commands [2][4]. Parts cost about $1,300, the CAD and build guide are public, but the
hardware files carry no licence, and the repository has had no commit since August 2025 [1][3][5].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | the current BOM: 8 XL330 finger servos and 3 XM430 thumb servos | [5] |
| Digits and DoF | 5 digits; 15 joints, 11 actuated, so the hand is underactuated | [2] |
| Coupling | on each finger one tendon flexes both outer joints (PIP and DIP); side-to-side knuckle motion is passive; springs open the fingers | [2] |
| Actuators | 11 Dynamixel servos in the forearm: 2 per finger, 3 for the thumb | [2] |
| Tendons | braided fishing line rated 200 lb, run through PTFE tubes | [2][5] |
| Joint ranges | DIP 120°, PIP 120°, finger MCP 140°, thumb MCP 90°, thumb CMC 190° | [2] |
| Size and mass | sized to an average adult hand from NASA anthropometric data; mass not given | [2] |
| Strength (authors' tests) | pinch 2.74 N; payload 6.0 kg; outer-joint slip force 33.02 N; MCP slip force 16.15 N | [2] |
| Endurance | 20 h of continuous running without a significant loss of motor precision | [2][3] |
| Grasps | 10/10 on the Kapandji thumb test; 29 of the 33 GRASP taxonomy grasps | [2] |
| Power | 5 V for the XL330 servos, 12 V for the XM430 servos | [8] |
| Control rate | 25 Hz teleoperation with the learned controller, 40 Hz with direct motor commands | [2] |

The authors measured LEAP Hand and Allegro Hand in the same strength tests: LEAP held 4.0 kg and
the Allegro 3.6 kg [2].

## How it works

Each finger has two tendons from two forearm servos: the paper's figure shows one for the knuckle
(MCP) and one shared by both outer joints, and springs pull the finger straight again [2]. The thumb
has three servos, one for each of its joints (CMC, MCP and IP) [2]. Printed PLA parts form the hand,
TPU pads and 3M friction tape give grip, and dowel pins, torsion springs and extension springs make
the joints [2][5].

Because the joints have no encoders, the authors put a MANUS glove on the robot hand, drive the
servos through random walks and record where the fingertips go [2][4]. A small network per finger
(an LSTM over the last ten states and an MLP head) then maps targets to servo positions: fingertip
positions for the thumb, joint angles for the other fingers [1][2]. Pretrained controllers and the
training data are on OSF; the download script asks for an OSF account token [1][12]. Each build
needs its own calibration, because tendon tension varies: a script finds the fully curled and
just-tensioned servo limits [1]. Teleoperation works with MANUS gloves or a Meta Quest headset
through OpenTeach [1]. The software is Python only, with no ROS packages [1].

The repository also holds a MuJoCo model of the hand with a cube-reorientation scene [1][2].

## What it is used for

- **Teleoperation** of household tasks with a glove or a VR headset [1][3].
- **Policy learning:** the authors trained residual motor policies with their HuDOR method, which
  converged in 45 minutes over 40 episodes [3].
- **Research on learned control** of tendon hands that lack joint sensing [2].

## Cost and BOM

| Item | Price (USD) | Type | Date | Source |
|---|---|---|---|---|
| One hand, current BOM, without tools | 1,307.11 | BOM | sheet dated 2025-02-19 | [5] |
| The same with tools and a $199 printer | 1,549.93 | BOM | sheet dated 2025-02-19 | [5] |
| Older all-XL330 build, without tools | 519.94 | BOM | sheet tab dated 2024-12-19 | [5][6] |

The three XM430 thumb servos are $842.70 of the current total [5]. The sheet labels both of its
totals "without tools"; the figures above are its row sums. The GitBook BOM page links the older
tab [6]. The paper gives the same price ladder: under $1,300, with $500 and $900 builds possible
using other servos [2]. The paper names the XM430-W210-T for the thumb, but the BOM lists the
XM430-W350-R [2][5]. A MANUS glove, needed to collect your own controller data, is not in the BOM
[1][5].

## Building it

**Difficulty 3:** printing, soldering two wiring harnesses, setting servo IDs, routing tendons and
calibrating.

- **Printing:** about 24 h on a Bambu Lab X1C; finger parts at 100% infill and 0.12 mm layers, tree
  supports on the build plate [2][7]. Check that dowels fit; drill tight holes to 2.5 mm [7].
- **Wiring:** a 5 V harness for the XL330 servos and a 12 V harness for the XM430s, soldered by hand
  [8].
- **Time:** about 7 hours to assemble; most repairs take under 20 minutes [2][3].
- **Tools:** printer, soldering iron, Allen keys (4, 2.5 and 1.5 mm), small Phillips screwdriver,
  tweezers and a razor blade [6].
- **Mounting:** the base plate fits Franka and xArm arms directly; a printed adapter fits Kinova
  arms [9].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| CAD | Onshape; STL print plates | Onshape [10], GitBook [7] | none stated |
| BOM and assembly guide | Google Sheet, GitBook | [ruka.gitbook.io](https://ruka.gitbook.io/instructions) | none stated |
| Control and teleoperation code | Python | [ruka-hand/RUKA](https://github.com/ruka-hand/RUKA) | MIT |
| MuJoCo model | MJCF, meshes | `assets/xml` in the repo | MIT (repository licence) |
| Controller weights and data | checkpoints, recordings | OSF [12] | not stated in the repo; the OSF page was not readable |

**No hardware licence.** The MIT licence file covers the repository's software [11]. The CAD,
print files, BOM and build guide state no licence, and the CC BY-SA 4.0 notice on the project page
covers that website's own source code [3]. Without a licence there is no clear right to copy, modify
or sell the design; ask the authors first. The MANUS teleoperation code comes in as a submodule
with MANUS's SDK, under MANUS's own terms [1].

## Strengths and limits

- **Strengths:** five human-sized digits with servos kept out of the fingers [2]; stronger than
  LEAP and Allegro in the authors' tests, at a lower parts cost than LEAP [2]; fast repairs [2];
  controllers and data shared [12]; mounts for three common arms [9].
- **Limits:** no hardware licence [11]; no joint sensing, so control depends on a learned model
  and, for new data, an expensive glove [2][4]; tendon tension varies by build [1]; no ROS support
  [1]; no commit since 2025-08-11; the BOM and paper disagree on the thumb servo [2][5].

## What to reuse

- Replace joint encoders with a model learned from a motion-capture glove worn on the robot hand
  [2].
- Keep servos in the forearm and run tendons through PTFE tubes to keep fingers slim [2][5].
- Couple the two outer finger joints on one tendon with spring return to save a motor per finger
  [2].
- Calibrate each build's curled and tensioned servo limits instead of trusting fixed offsets [1].

## Related robots

- [Aero Hand Open](aero-hand-open.md): another printed tendon hand, with seven servos and a tuned
  MuJoCo model.
- [LEAP Hand](leap-hand.md) and [Allegro Hand](allegro-hand.md): the direct-drive hands RUKA tests
  against.
- [Shadow Dexterous Hand](shadow-dexterous-hand.md): the commercial tendon hand.
- Arm mounts exist for the [Franka Panda](franka-panda.md), [UFACTORY xArm](ufactory-xarm.md) and
  [Kinova Gen3](kinova-gen3.md) [9].

## Sources

1. [RUKA repository README](https://github.com/ruka-hand/RUKA), accessed 2026-11-18
2. [RUKA: Rethinking the Design of Humanoid Hands with Learning](https://arxiv.org/abs/2504.13165), accessed 2026-11-18
3. [RUKA project page](https://ruka-hand.github.io), accessed 2026-11-18
4. [RUKA hardware instructions, introduction](https://ruka.gitbook.io/instructions), accessed 2026-11-18
5. [RUKA single-hand bill of materials (sheet)](https://docs.google.com/spreadsheets/d/1bi4XM1knMoRTz975P-abTXNx2L5BT7-KNwVOGFRxrvw/edit?gid=1155455594), accessed 2026-11-18
6. [RUKA bill of materials and tools page](https://ruka.gitbook.io/instructions/hardware/bill-of-materials), accessed 2026-11-18
7. [RUKA 3D print parts](https://ruka.gitbook.io/instructions/hardware/3d-print-parts), accessed 2026-11-18
8. [RUKA power supply and wiring harness assembly](https://ruka.gitbook.io/instructions/hardware/power-supply-and-wiring-harness-assembly), accessed 2026-11-18
9. [RUKA robot arm mounts](https://ruka.gitbook.io/instructions/hardware/robot-arm-mounts), accessed 2026-11-18
10. [RUKA Onshape CAD](https://cad.onshape.com/documents/6be13b87a3aad01bd61ef6ab/w/86f8cbb4c7b89f36daabaded/e/5b18eb8a388f7b1857d3fdb3), accessed 2026-11-18
11. [RUKA licence file](https://github.com/ruka-hand/RUKA/blob/main/LICENSE), accessed 2026-11-18
12. [RUKA controller checkpoints and data (OSF)](https://osf.io/hwajz/), accessed 2026-11-18
