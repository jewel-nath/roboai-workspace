---
type: robot
name: Kinova Gen3, Gen3 lite and Gen2
summary: Light seven- or six-axis research arm from Kinova with a torque sensor in every actuator, 1 kHz low-level control, an optional wrist depth camera and an official BSD-3 ROS 2 driver; the Gen3 lite is a smaller teaching arm and Gen2 (JACO, MICO) the older line.
tags: [cobot, gen3, gen3-lite, jaco, torque-sensing, 7-dof, kortex, ros2, mujoco, commercial]
category: arm
tier: B
openness: software-only
maker: Kinova
year: 2019
license: {hardware: , software: BSD-3-Clause, docs: }
links: {repo: "https://github.com/Kinovarobotics/ros2_kortex", docs: "https://github.com/Kinovarobotics/kortex", cad: , paper: , site: "https://www.kinovarobotics.com/product/gen3-robots"}
specs: {dof: 7, payload_kg: 2, reach_mm: 902, mass_kg: 8.2, size_mm: , speed_mps: 0.5, runtime_h: }
stack: {actuators: "7 Kinova actuators with integrated torque sensors and infinite rotation", mcu: , compute: "controller inside the arm base; external PC over Ethernet with the Kortex API", sensors: ["joint position", "joint torque", "current, voltage and temperature", "accelerometer and gyroscope", "optional wrist vision module: colour camera and Intel RealSense depth sensor"], sim_models: ["URDF/Xacro (ros2_kortex kortex_description: Gen3 6 and 7 DoF, Gen3 lite)", "Gazebo Harmonic (ros2_kortex simulation packages)", "MJCF (MuJoCo Menagerie, kinova_gen3)", "URDF and MJCF (robot_descriptions: Gen3, Gen3 lite, Gen2 and JACO2 variants)"], ros2: official}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-09-18, stars: 135, active: true}
use_cases: [research, manipulation, imitation-learning, teleop, education, hri]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://www.kinovarobotics.com/uploads/Kinova_Onepager_Gen3_2026_EN.pdf", title: Kinova Gen3 technical specifications one-pager (2026), accessed: 2026-11-18}
  - {url: "https://store.clearpathrobotics.com/products/kinova-gen-3", title: Clearpath Robotics store, Kinova Gen3 page, accessed: 2026-11-18}
  - {url: "https://store.clearpathrobotics.com/products/gen3-lite", title: Clearpath Robotics store, Kinova Gen3 lite page, accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/rbr50-company/kinovas-gen3-family-of-robotic-arms-supports-research-efforts-and-spurs-commercial-development/", title: "The Robot Report (RBR50): Kinova's Gen3 family of robotic arms", accessed: 2026-11-18}
  - {url: "https://en.wikipedia.org/wiki/Kinova", title: "Wikipedia: Kinova", accessed: 2026-11-18}
  - {url: "https://github.com/Kinovarobotics/ros2_kortex", title: ros2_kortex README, accessed: 2026-11-18}
  - {url: "https://github.com/Kinovarobotics/kortex", title: Kinova Kortex API repository, accessed: 2026-11-18}
  - {url: "https://github.com/Kinovarobotics/kinova-ros", title: "kinova-ros (Gen2: JACO, JACO2, MICO) README", accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/kinova_gen3", title: "MuJoCo Menagerie: kinova_gen3", accessed: 2026-11-18}
  - {url: "https://github.com/robot-descriptions/robot_descriptions.py", title: robot_descriptions model list, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2502.13142", title: Pre-training Auto-regressive Robotic Models with 4D Representations, accessed: 2026-11-18}
  - {url: "https://www.kinovarobotics.com/product/gen3-lite-robots", title: "Kinova Gen3 lite product page (title only readable)", accessed: 2026-11-18}
---

# Kinova Gen3, Gen3 lite and Gen2

A light research arm from Kinova of Quebec, Canada, sold in six- and seven-axis versions, with a
torque sensor in every actuator, 1 kHz low-level control and an optional depth camera in the wrist
[1][5]. Kinova launched it commercially in January 2019 [4]. At 8.2 kg for the seven-axis arm it is
much lighter than the Panda or the iiwa, and Kinova pitches it for mobile manipulation as well as
lab work [1]. The Gen3 lite is a smaller six-axis arm for teaching and research [3][12]; Kinova's
ROS driver for the older Gen2 line (JACO, JACO2, MICO) is ROS 1 only [8].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Gen3, 7 DoF | [1] |
| Degrees of freedom | 7 actuators, each with infinite rotation; gripper optional, so `dof: 7` | [1] |
| Payload | 2.0 kg full-range continuous; 4.0 kg mid-range continuous; both without a gripper (maker's claims). The frontmatter uses 2.0 kg | [1] |
| Reach | 902 mm (maker's claim) | [1] |
| Mass | 8.2 kg (maker's claim) | [1] |
| Maximum Cartesian speed | 50 cm/s (maker's claim) | [1] |
| Power | 18–30 VDC, 24 VDC nominal; 36 W average (maker's claim) | [1] |
| Protection, temperature | IP33; −30 to 35 °C | [1] |
| Sensors per actuator | torque, position, current, voltage, temperature, accelerometer, gyroscope | [1] |
| Control | 1 kHz control loop; low level: position, velocity, motor current, torque; high level: Cartesian pose and velocity, joint pose and velocity, wrench | [1] |
| Interfaces | 2 x 100 Mbit/s Ethernet inside the arm; end-effector port with Ethernet, I2C, UART, GPIO and 1 A at 24 V | [1] |
| Optional vision module | colour camera up to 1280 x 720 at 30 fps; Intel RealSense depth sensor up to 480 x 270 at 30 fps, minimum range 18 cm | [1] |

## How it works

Each joint is a Kinova actuator with its own torque sensor, inertial sensors and infinite
rotation [1]. The controller sits in the base [2], and the arm runs from 24 V DC [1]. Software
goes through Kinova's Kortex API: the C++ API ships as prebuilt packages from Kinova's server and
the Python API installs with pip, with BSD-3 examples and docs on GitHub [7]. Kortex covers both
the Gen3 and the Gen3 lite [6][7].

ros2_kortex is Kinova's official ROS 2 driver, built on ros2_control: it supports the Gen3 with 6
or 7 DoF and the Gen3 lite, Robotiq 2F-85 and 2F-140 grippers or the Gen3 lite gripper, a joint
trajectory controller and a twist controller, mock hardware, MoveIt configs and Gazebo Harmonic
simulation [6]. Its README marks Humble as stable with binaries, Jazzy as stable from source, and
Rolling as unstable [6]. The build downloads the Kortex API 2.8.0 binary for Linux x86-64 [6].

For simulation, ros2_kortex holds the URDFs and Gazebo setup [6], MuJoCo Menagerie carries a
`kinova_gen3` model converted from Kinova's URDF [9], and robot_descriptions loads the Gen3,
Gen3 lite, Gen2 and seven JACO2 variants [10].

| Variant | DoF | Payload | Reach | Mass | ROS support | Source |
|---|---|---|---|---|---|---|
| Gen3, 7 DoF | 7 | 2.0 kg full range, 4.0 kg mid range | 902 mm | 8.2 kg | ros2_kortex | [1][6] |
| Gen3, 6 DoF | 6 | 2.0 kg full range, 4.0 kg mid range | 891 mm | 7.2 kg | ros2_kortex | [1][6] |
| Gen3 lite | 6 | 0.5 kg | 760 mm | 5.4 kg; 20 W | ros2_kortex | [3][6] |
| Gen2 (JACO, JACO2, MICO) | 4 to 7 by model | — | — | — | kinova-ros, ROS 1 (Noetic on master) | [8][10] |

Gen2 specs were not found in the sources read, and its current sales status was not confirmed.
By 2009 Kinova had introduced a wheelchair-mounted assistive arm, and the JACO assistive arm is
still listed among its products [5].

## What it is used for

- Manipulation and learning research: for example, a 2025 Berkeley paper on pre-training robot
  models with 4D representations ran its real-world tests on a seven-axis Gen3 with a Robotiq
  2F-85 gripper [11].
- Mobile manipulation, which Kinova lists among the Gen3's target uses [1].
- Teaching with the Gen3 lite, which Kinova sells for teaching and research [12].
- Assistive robotics with the JACO arm [5].

## Cost and BOM

Price on request. Both the Gen3 and Gen3 lite pages on Clearpath's store, a Kinova reseller, offer
only a quote form [2][3], so the frontmatter `cost` stays empty.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| ROS 2 driver, descriptions, MoveIt, Gazebo | ROS 2 packages, URDF/Xacro | [ros2_kortex](https://github.com/Kinovarobotics/ros2_kortex) [6] | BSD-3-Clause |
| Kortex API docs and examples | C++, Python | [kortex](https://github.com/Kinovarobotics/kortex) [7] | BSD-3-Clause; the C++ API library itself is a prebuilt download |
| Gen2 ROS 1 driver | ROS 1 packages | [kinova-ros](https://github.com/Kinovarobotics/kinova-ros) [8] | BSD-3-Clause |
| MuJoCo model | MJCF | Menagerie `kinova_gen3` [9] | BSD-3-Clause |
| Arm hardware, actuator firmware | — | Not published | Closed |

## Strengths and limits

- **Strengths:** joint torque sensing and 1 kHz torque control in an 8.2 kg arm [1]; 24 V DC supply
  and the controller in the base, with no separate control box [1][2]; an optional wrist RGB-D
  camera [1];
  infinite rotation on every joint [1]; an official ROS 2 driver with MoveIt and Gazebo [6];
  a Menagerie model [9].
- **Limits:** only 2 kg payload across the full workspace, 4 kg only mid-range [1]; 50 cm/s top
  Cartesian speed [1]; IP33 [1]; the Kortex C++ library comes only as a prebuilt binary, Linux
  x86-64 in the ros2_kortex build [6][7];
  Jazzy only from source [6]; price on request [2]; Gen2 arms have no ROS 2 driver from Kinova [8].

## Related robots

- [Franka Panda](franka-panda.md) and [KUKA LBR iiwa](kuka-lbr-iiwa.md): heavier seven-axis arms
  with joint torque sensors and more payload.
- [Universal Robots](universal-robots.md): six-axis industrial cobots.
- [Robotiq 2F-85](robotiq-2f-85.md): the gripper ros2_kortex supports on the Gen3 [6].
- [UFACTORY xArm](ufactory-xarm.md): a cheaper arm with a published shop price but no joint torque
  sensors.

## Sources

1. [Kinova Gen3 technical specifications one-pager (2026)](https://www.kinovarobotics.com/uploads/Kinova_Onepager_Gen3_2026_EN.pdf), accessed 2026-11-18
2. [Clearpath Robotics store, Kinova Gen3 page](https://store.clearpathrobotics.com/products/kinova-gen-3), accessed 2026-11-18
3. [Clearpath Robotics store, Kinova Gen3 lite page](https://store.clearpathrobotics.com/products/gen3-lite), accessed 2026-11-18
4. [The Robot Report (RBR50): Kinova's Gen3 family of robotic arms](https://www.therobotreport.com/rbr50-company/kinovas-gen3-family-of-robotic-arms-supports-research-efforts-and-spurs-commercial-development/), accessed 2026-11-18
5. [Wikipedia: Kinova](https://en.wikipedia.org/wiki/Kinova), accessed 2026-11-18
6. [ros2_kortex README](https://github.com/Kinovarobotics/ros2_kortex), accessed 2026-11-18
7. [Kinova Kortex API repository](https://github.com/Kinovarobotics/kortex), accessed 2026-11-18
8. [kinova-ros (Gen2: JACO, JACO2, MICO) README](https://github.com/Kinovarobotics/kinova-ros), accessed 2026-11-18
9. [MuJoCo Menagerie: kinova_gen3](https://github.com/google-deepmind/mujoco_menagerie/tree/main/kinova_gen3), accessed 2026-11-18
10. [robot_descriptions model list](https://github.com/robot-descriptions/robot_descriptions.py), accessed 2026-11-18
11. [Pre-training Auto-regressive Robotic Models with 4D Representations](https://arxiv.org/abs/2502.13142), accessed 2026-11-18
12. [Kinova Gen3 lite product page (title only readable)](https://www.kinovarobotics.com/product/gen3-lite-robots), accessed 2026-11-18
