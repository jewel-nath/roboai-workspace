---
type: robot
name: Koch v1.1
summary: Printable leader-follower arm on Dynamixel XL430 and XL330 servos, Alexander Koch's Low-Cost Robot Arm reworked with Hugging Face; LeRobot's first real-robot arm, about $477 in parts for a pair at 2024 prices.
tags: [leader-follower, dynamixel, xl430, xl330, lerobot, 3d-printed, low-cost, imitation-learning, low-cost-robot-arm]
category: arm
tier: B
openness: full
maker: Alexander Koch; v1.1 by Jess Moss with Hugging Face
year: 2024
license: {hardware: Apache-2.0, software: Apache-2.0, docs: Apache-2.0}
links: {repo: "https://github.com/jess-moss/koch-v1-1", docs: "https://huggingface.co/docs/lerobot/koch", cad: "https://github.com/jess-moss/koch-v1-1/tree/main/hardware", paper: , site: }
specs: {dof: 6, payload_kg: , reach_mm: , mass_kg: , size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "Dynamixel servos: follower 2 x XL430-W250-T and 4 x XL330-M288-T; leader 6 x XL330-M077-T", mcu: "none on the arm; one Waveshare serial bus servo driver board per arm", compute: "host PC over USB-C", sensors: ["servo encoders"], sim_models: ["MJCF (MuJoCo Menagerie, low_cost_robot_arm, from a community Koch v1.1 URDF)", "URDF and MJCF (original low_cost_robot repo, v1.0)"], ros2: none}
cost: {type: bom, usd: 477, as_of: 2024-09-17, source: "https://github.com/jess-moss/koch-v1-1#sourcing-parts"}
build: {difficulty: 2, hours: , print_hours: }
maturity: {last_commit: 2024-09-17, stars: 737, active: false}
use_cases: [teleop, imitation-learning, data-collection, education, hobby]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/jess-moss/koch-v1-1", title: Koch v1.1 repository README, accessed: 2026-11-18}
  - {url: "https://github.com/AlexanderKoch-Koch/low_cost_robot", title: Low-Cost Robot Arm (original) repository README, accessed: 2026-11-18}
  - {url: "https://huggingface.co/docs/lerobot/koch", title: LeRobot Koch v1.1 guide, accessed: 2026-11-18}
  - {url: "https://github.com/huggingface/lerobot/blob/e64fad2224ba01e21ed698b1a07a8ead81252177/examples/7_get_started_with_real_robot.md", title: "LeRobot real-robot tutorial, February 2025 version", accessed: 2026-11-18}
  - {url: "https://github.com/huggingface/lerobot", title: LeRobot repository README and robot drivers, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/low_cost_robot_arm", title: "MuJoCo Menagerie: Low-Cost Robot Arm model", accessed: 2026-11-18}
  - {url: "https://github.com/robot-descriptions/robot_descriptions.py", title: robot_descriptions model list, accessed: 2026-11-18}
---

# Koch v1.1

A 3D-printed leader-follower arm on Dynamixel servos: you move the small leader by hand and the
follower copies it. Alexander Koch published the original Low-Cost Robot Arm in 2024 [2]; Jess Moss
and Hugging Face reworked it as v1.1 to ease assembly [1]. LeRobot's original getting-started
tutorial for real robots was written for it [4]. The repository has had no commit since September
2024, and LeRobot's default arm is now the [SO-101](so-101.md) [5].

## Specs

| Item | Value | Source |
|---|---|---|
| Degrees of freedom | 6 per arm: shoulder pan, shoulder lift, elbow flex, wrist flex, wrist roll, gripper | [5] |
| Follower servos | 2 x XL430-W250-T (shoulder pan and lift), 4 x XL330-M288-T | [1][5] |
| Leader servos | 6 x XL330-M077-T; the gripper is a handle and trigger | [1][5] |
| Power | Follower 12 V with a step-down converter for the 5 V XL330s; leader 5 V | [1] |
| Bus adapter | Waveshare serial bus servo driver board, one per arm, USB-C | [1] |
| Reach, payload, mass | Not published | — |

## How it works

The follower uses the stronger XL430 servos on the first two joints and the light XL330 servos
(18 g each) elsewhere, so the arm is light and quick [2]. The leader uses the low-geared XL330-M077
on every joint so it moves easily by hand; its gripper becomes a trigger [1][2]. Koch credits the
GELLO project for the leader idea [2]. Both arms skip ROBOTIS's U2D2 adapter, which Koch found
costly and slow, for a cheap Waveshare board [2].

Version 1.1 fixed screw clashes, standardised holes, stopped screws going into plastic, added a
platform that lets the follower pick objects off the ground, replaced the step-down converter so no
soldering is needed, and added SolidWorks and STEP files and a wiring diagram [1].

LeRobot drives both arms (`koch_follower`, `koch_leader`) through its Dynamixel extra: find ports,
set motor IDs, calibrate, teleoperate, record and train [3][5]. There is no ROS 2 driver.

MuJoCo Menagerie's `low_cost_robot_arm` (Apache-2.0) is a simplified MJCF of the v1.1 follower,
converted from a community URDF, with approximate joint limits [6]; robot_descriptions loads it
[7]. The original repository has its own URDF and MuJoCo scene for v1.0 [2].

| Variant | Follower BOM | Leader BOM | CAD | Licence | Source |
|---|---|---|---|---|---|
| Low-Cost Robot Arm (v1.0), Alexander Koch | $258 | $183 | Fusion 360, STEP, STL | MIT | [2] |
| Koch v1.1, Jess Moss with Hugging Face | $278 | $199 | SolidWorks, STEP, STL | Apache-2.0 | [1] |

## What it is used for

- Teleoperation and demonstration recording for imitation learning with LeRobot; the tutorial
  trains a policy to put a Lego block in a bin [4].
- A cheap Dynamixel-based learning arm for teaching; LeRobot still supports it natively [3][5].

## Cost and BOM

| Item | Price (USD) | Type | Date | Source |
|---|---|---|---|---|
| Leader and follower, US links | 477 | BOM | 2024-09-17 | [1] |
| Follower only, US links | 278 | BOM | 2024-09-17 | [1] |
| Leader only, US links | 199 | BOM | 2024-09-17 | [1] |

The pair total adds the README's two US totals; both lists include a screwdriver set and a USB
cable set that serve both arms, so the pair costs $461 if those are bought once [1]. Servos are
most of the cost: $50 per XL430 and $24 per XL330 [1]. Prices date from the README's last change
(last commit 2024-09-17) and have not been updated since; filament is not included. The README also
gives EU, UK, China and Japan prices [1].

## Building it

**Difficulty 2:** print the parts and screw in off-the-shelf servos and boards; v1.1 needs no
soldering [1].

- **Printing:** PLA+, ABS or PETG; at most 0.2 mm layers and a 0.4 mm nozzle; about 30% infill;
  a glue stick on the bed [1]. Print time is not stated.
- **Assembly:** follow the v1.1 assembly video; LeRobot asks you not to plug in all motor cables or
  screw down the board until the motor setup step [1][3].
- **Pitfalls:** the leader platform now bolts on with M2 screws and nuts because the snap fit was
  loose on some printers; the Waveshare board is run at 5 V on the leader, below its rated input,
  on purpose [1].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| CAD | SolidWorks, STEP, per part and assembly | [hardware/](https://github.com/jess-moss/koch-v1-1/tree/main/hardware) | Apache-2.0 |
| Print files | STL | [hardware/](https://github.com/jess-moss/koch-v1-1/tree/main/hardware) | Apache-2.0 |
| Wiring diagram | PDF | [electrical/](https://github.com/jess-moss/koch-v1-1/tree/main/electrical) | Apache-2.0 |
| BOM | Markdown table with buy links | [README](https://github.com/jess-moss/koch-v1-1#sourcing-parts) | Apache-2.0 |
| Software | LeRobot, Python | [huggingface/lerobot](https://github.com/huggingface/lerobot) [5] | Apache-2.0 |
| Original v1.0 files and scripts | Fusion 360, STEP, STL, Python, URDF, MJCF | [low_cost_robot](https://github.com/AlexanderKoch-Koch/low_cost_robot) [2] | MIT |
| Sim model | MJCF | MuJoCo Menagerie [6] | Apache-2.0 |
| Servo firmware | Dynamixel, closed | ROBOTIS | Not open |

## Strengths and limits

- **Strengths:** Dynamixel servos that ROBOTIS's own SDK can drive [2]; full CAD in SolidWorks
  and STEP [1]; native LeRobot support [3]; a Menagerie model [6]; no soldering [1].
- **Limits:** about twice the parts cost of an SO-101 pair (see its page); no commit since
  September 2024, and 2024 prices [1]; no published reach, payload or mass; LeRobot's README and
  examples now lead with the SO-101 [5]; the Menagerie model is simplified [6].

## What to reuse

- Strong servos on the two shoulder joints, light ones elsewhere [2].
- A leader built from low-geared versions of the same servo family, with a trigger for the
  gripper [1][2].
- A cheap USB serial bus board instead of the maker's adapter [2].

## Related robots

- [SO-101](so-101.md): its successor as LeRobot's default arm, on cheaper Feetech servos.
- [SO-ARM 102](so-arm-102.md): a stiffer SO-101 derivative.
- [OpenManipulator-X](openmanipulator-x.md): ROBOTIS's OMX successor line is a factory-made
  Dynamixel leader-follower pair on similar XL430 and XL330 servos.
- [Interbotix X-Series arms](interbotix-x-series-arms.md): the ALOHA arms; Koch and SO-101 do the
  same leader-follower job for a few hundred dollars.
- GELLO: the low-cost teleoperation project that inspired the leader [2].

## Sources

1. [Koch v1.1 repository README](https://github.com/jess-moss/koch-v1-1), accessed 2026-11-18
2. [Low-Cost Robot Arm (original) repository README](https://github.com/AlexanderKoch-Koch/low_cost_robot), accessed 2026-11-18
3. [LeRobot Koch v1.1 guide](https://huggingface.co/docs/lerobot/koch), accessed 2026-11-18
4. [LeRobot real-robot tutorial, February 2025 version](https://github.com/huggingface/lerobot/blob/e64fad2224ba01e21ed698b1a07a8ead81252177/examples/7_get_started_with_real_robot.md), accessed 2026-11-18
5. [LeRobot repository README and robot drivers](https://github.com/huggingface/lerobot), accessed 2026-11-18
6. [MuJoCo Menagerie: Low-Cost Robot Arm model](https://github.com/google-deepmind/mujoco_menagerie/tree/main/low_cost_robot_arm), accessed 2026-11-18
7. [robot_descriptions model list](https://github.com/robot-descriptions/robot_descriptions.py), accessed 2026-11-18
