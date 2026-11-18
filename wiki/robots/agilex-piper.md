---
type: robot
name: AgileX PiPER
summary: Low-cost commercial 6-axis arm on a CAN bus with a 1.5 kg payload, an MIT-licensed Python SDK and ROS drivers, and an official MuJoCo model; a common follower arm for imitation-learning labs.
tags: [can-bus, 6-axis, lightweight, leader-follower, mujoco, ros2, moveit, commercial]
category: arm
tier: B
openness: software-only
maker: AgileX Robotics
year: 2024
license: {hardware: , software: MIT, docs: }
links: {repo: "https://github.com/agilexrobotics/agx_arm_ros", docs: "https://github.com/agilexrobotics/piper_sdk", cad: , paper: , site: "https://global.agilex.ai/products/piper"}
specs: {dof: 7, payload_kg: 1.5, reach_mm: 626, mass_kg: 4.2, size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "six joint actuators plus a gripper; motor and gearbox models not published", mcu: "integrated controller in the arm", compute: "host PC over a USB-to-CAN adapter", sensors: ["joint encoders"], sim_models: ["URDF and MJCF (piper_ros, piper_description)", "Gazebo and MuJoCo setups (piper_ros, piper_sim)", "MJCF (MuJoCo Menagerie, agilex_piper)", "URDF and MJCF (robot_descriptions, piper_description and piper_mj_description)"], ros2: official}
cost: {type: retail, usd: 3500, as_of: 2026-11-18, source: "https://www.roboticscenter.ai/store/product/agilex-agilex-piper"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-11-14, stars: 72, active: true}
use_cases: [imitation-learning, teleop, data-collection, research, manipulation, education]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://global.agilex.ai/products/piper", title: AgileX PiPER product page, accessed: 2026-11-18}
  - {url: "https://www.generationrobots.com/en/404258-6-axis-robotic-arm-piper.html", title: Generation Robots PiPER product page, accessed: 2026-11-18}
  - {url: "https://github.com/agilexrobotics/piper_sdk", title: piper_sdk repository README, accessed: 2026-11-18}
  - {url: "https://github.com/agilexrobotics/piper_sdk/blob/master/assets/double_piper.MD", title: piper_sdk master-slave (leader-follower) guide, accessed: 2026-11-18}
  - {url: "https://github.com/agilexrobotics/piper_ros/tree/humble", title: "piper_ros repository, humble branch README", accessed: 2026-11-18}
  - {url: "https://github.com/agilexrobotics/agx_arm_ros", title: agx_arm_ros repository README, accessed: 2026-11-18}
  - {url: "https://github.com/agilexrobotics/pyAgxArm", title: pyAgxArm repository README and licence, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie", title: MuJoCo Menagerie model list, accessed: 2026-11-18}
  - {url: "https://github.com/robot-descriptions/robot_descriptions.py", title: robot_descriptions model list, accessed: 2026-11-18}
  - {url: "https://github.com/huggingface/lerobot", title: LeRobot repository README, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2605.28231", title: "ProgVLA: Progress-Aware Robot Manipulation Skill Learning", accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2607.25731", title: Tri-Manual Visuomotor Imitation Learning of Robot Policies, accessed: 2026-11-18}
  - {url: "https://www.roboticscenter.ai/store/product/agilex-agilex-piper", title: Robotics Center store PiPER page, accessed: 2026-11-18}
---

# AgileX PiPER

A light six-axis arm from AgileX Robotics, driven over a CAN bus, with a 1.5 kg payload and 626 mm
reach (maker's claims) [1]. The hardware is closed, but the Python SDK and ROS drivers are MIT, and
MuJoCo Menagerie has a model of it [3][5][8]. For a builder it is a cheap step up from
printed servo arms: a real six-axis follower arm that recent learning papers use.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | PiPER (standard) | [1] |
| Degrees of freedom | 6 arm joints plus a gripper (sold separately by some resellers); `dof: 7` counts the gripper as one | [1][5][13] |
| Payload | 1.5 kg (maker's claim) | [1] |
| Reach | 626 mm (maker's claim) | [1] |
| Mass | 4.2 kg (maker's claim) | [1] |
| Repeatability | ±0.1 mm (maker's claim) | [1] |
| Supply and interface | 24 V DC; CAN at 1 Mbit/s through a USB-to-CAN adapter | [1][5] |
| Joint 5 | ±75° range, 225°/s (maker's claim); other joint speeds not published | [1] |
| Joint limits in the URDF | J1 ±150°, J2 0 to 180°, J3 −170 to 0°, J4 ±100°, J5 ±70°, J6 ±120° | [5] |
| Gripper travel | 80 mm | [5] |
| Operating temperature | −20 to 50 °C (maker's claim) | [1] |
| Mounting | 70 x 70 mm hole pattern | [1] |
| Brake | None | [2] |

## How it works

The controller is built into the arm, which has only two external ports, power and CAN [2].
AgileX does not publish the motor or gearbox models, so torque and backlash figures are not
available. The body is aluminium alloy with a polymer shell [2].

The host talks to the arm through a USB-to-CAN adapter set up with a shell script; the bus speed is
fixed at 1 Mbit/s [5]. `piper_sdk` reads and writes CAN frames from Python [3]. Two arms on one CAN
bus can be set as leader and follower: the leader sends joint targets straight to the follower, and
the PC reads both arms' data for recording [4]. The arm also supports drag teaching [2].

`piper_ros` holds the ROS 1 Noetic driver on its default branch and ROS 2 Foxy and Humble drivers
on other branches, with MoveIt configs, Gazebo and MuJoCo setups, and two URDFs for firmware before
and after S-V1.6-3 [5]. AgileX now points new users to `pyAgxArm`, a newer SDK for its PiPER and
Nero arms, and `agx_arm_ros`, a ROS 2 Humble and Jazzy driver built on it [3][6][7].

MuJoCo Menagerie carries `agilex_piper` (MIT) [8], and robot_descriptions loads both the URDF and
the MJCF [9].

| Variant | Reach | Payload | Mass | Note | Source |
|---|---|---|---|---|---|
| PiPER | 626 mm | 1.5 kg | 4.2 kg | Standard arm | [1] |
| PiPER-X | 669 mm | 1.5 kg | 4.5 kg | J5 range ±90° | [1] |
| PiPER-L | 750 mm | 1.5 kg | 4.5 kg | Longer reach | [1] |
| PiPER-H | 636 mm | 2 kg | 4.5 kg | Higher payload | [1] |

## What it is used for

- Imitation learning with leader-follower teleoperation. ProgVLA used a pair of PiPERs, one as
  leader and one as follower [11]; a 2026 tri-manual study used three PiPER-X arms with
  grippers [12].
- LeRobot: the PiPER is driven through a community plugin, not a native driver [10].
- Simulation-first work in MuJoCo with the Menagerie model [8].

## Cost and BOM

| Item | Price | Type | Date | Source |
|---|---|---|---|---|
| PiPER arm, no gripper, with USB-to-CAN module and power adapter (Robotics Center, US) | USD 3,500 | retail | 2026-11-18 | [13] |
| PiPER arm (Generation Robots, France) | EUR 2,000 excl. VAT | retail | 2026-11-18 | [2] |

AgileX's own site has no online checkout; it sells on inquiry [1]. Resale prices differ widely.
The gripper and the teach pendant are sold separately [13].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Python SDK | Python | [piper_sdk](https://github.com/agilexrobotics/piper_sdk) [3] | MIT |
| ROS drivers, MoveIt, Gazebo and MuJoCo setups | ROS 1 and ROS 2 packages | [piper_ros](https://github.com/agilexrobotics/piper_ros) [5] | MIT, copyright held by an individual developer |
| Newer SDK | Python | [pyAgxArm](https://github.com/agilexrobotics/pyAgxArm) [7] | LGPL-3.0 |
| Newer ROS 2 driver | ROS 2 packages | [agx_arm_ros](https://github.com/agilexrobotics/agx_arm_ros) [6] | MIT |
| Robot models | URDF, MJCF | piper_ros; MuJoCo Menagerie `agilex_piper` [5][8] | MIT |
| Mechanical CAD, firmware, electronics | — | Not published | Closed |

## Strengths and limits

- **Strengths:** a real six-axis arm at a few thousand dollars [13]; 1.5 kg payload (maker's
  claim) [1]; built-in leader-follower mode over CAN [4]; MIT SDK and ROS drivers; a MuJoCo
  Menagerie model [8]; several longer-reach and higher-payload variants [1].
- **Limits:** closed hardware with no published motor or torque data; no brakes [2]; a dedicated
  CAN adapter and Linux CAN setup [5]; two SDKs and two ROS repos at once, and the newer SDK is
  LGPL-3.0, not MIT [3][7]; only a community LeRobot plugin [10]; prices vary widely between
  resellers.

## Related robots

- [SO-101](so-101.md): the printed alternative for LeRobot; far cheaper, far weaker.
- [Interbotix X-Series arms](interbotix-x-series-arms.md): the Dynamixel arms behind ALOHA and
  BridgeData V2, now discontinued.
- [UFACTORY xArm](ufactory-xarm.md): another commercial research arm in this batch.
- AgileX Nero: a second AgileX arm that shares the newer SDK and ROS 2 driver [6][7].

## Sources

1. [AgileX PiPER product page](https://global.agilex.ai/products/piper), accessed 2026-11-18
2. [Generation Robots PiPER product page](https://www.generationrobots.com/en/404258-6-axis-robotic-arm-piper.html), accessed 2026-11-18
3. [piper_sdk repository README](https://github.com/agilexrobotics/piper_sdk), accessed 2026-11-18
4. [piper_sdk master-slave (leader-follower) guide](https://github.com/agilexrobotics/piper_sdk/blob/master/assets/double_piper.MD), accessed 2026-11-18
5. [piper_ros repository, humble branch README](https://github.com/agilexrobotics/piper_ros/tree/humble), accessed 2026-11-18
6. [agx_arm_ros repository README](https://github.com/agilexrobotics/agx_arm_ros), accessed 2026-11-18
7. [pyAgxArm repository README and licence](https://github.com/agilexrobotics/pyAgxArm), accessed 2026-11-18
8. [MuJoCo Menagerie model list](https://github.com/google-deepmind/mujoco_menagerie), accessed 2026-11-18
9. [robot_descriptions model list](https://github.com/robot-descriptions/robot_descriptions.py), accessed 2026-11-18
10. [LeRobot repository README](https://github.com/huggingface/lerobot), accessed 2026-11-18
11. [ProgVLA: Progress-Aware Robot Manipulation Skill Learning](https://arxiv.org/abs/2605.28231), accessed 2026-11-18
12. [Tri-Manual Visuomotor Imitation Learning of Robot Policies](https://arxiv.org/abs/2607.25731), accessed 2026-11-18
13. [Robotics Center store PiPER page](https://www.roboticscenter.ai/store/product/agilex-agilex-piper), accessed 2026-11-18
