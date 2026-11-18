---
type: robot
name: Robotiq 2F-85
summary: Electric two-finger adaptive gripper with 85 mm stroke, the default end effector on many research arms and datasets, now with an official BSD-licensed ROS 2 driver, C++ SDK and sim assets.
tags: [gripper, parallel-jaw, adaptive, underactuated, modbus-rtu, rs-485, 2f-140, droid, robotiq]
category: gripper
tier: B
openness: software-only
maker: Robotiq
year: 2012
license: {hardware: , software: BSD-3-Clause, docs: }
links: {repo: "https://github.com/robotiq/robotiq-ros", docs: "https://github.com/robotiq/robotiq-sdk/tree/main/grippers", cad: "https://blog.robotiq.com/hubfs/support-files/2F85_Opened_20190924-Sep-06-2024-02-25-46-4707-PM.step", paper: , site: "https://robotiq.com/products/adaptive-grippers"}
specs: {dof: 1, payload_kg: 5, reach_mm: , mass_kg: 0.9, size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "one electric drive; both fingers coupled through linkages", mcu: "built-in gripper controller, Modbus RTU over RS-485", compute: "host PC or robot controller", sensors: ["finger position", "motor current", "object-detection status", "optional TSF-85 tactile fingertips"], sim_models: ["URDF/Xacro (robotiq/robotiq-ros robotiq_description, 2F-85 and 2F-140)", "MJCF (MuJoCo Menagerie, robotiq_2f85)", "MJCF (MuJoCo Menagerie, robotiq_2f85_v4)", "USD (robotiq/isaacsim_assets, PhysX and Newton variants)", "MJCF (robosuite Robotiq85Gripper and Robotiq140Gripper)"], ros2: official}
cost: {type: retail, usd: 9271.41, as_of: 2026-11-18, source: "https://automationdistribution.com/robotiq-agc-grp-2f85-2f-85"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-11-17, stars: 13, active: true}
use_cases: [manipulation, research, imitation-learning, data-collection]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://robotiq.com/products/adaptive-grippers", title: Robotiq Adaptive Grippers product page, accessed: 2026-11-18}
  - {url: "https://blog.robotiq.com/hubfs/Product-sheets/Adaptive%20Grippers/Product-sheet-Adaptive-Grippers-EN.pdf", title: "Robotiq Adaptive Grippers product sheet (May 2025)", accessed: 2026-11-18}
  - {url: "https://blog.robotiq.com/hubfs/press%20releases/2F-85%20&%202F-140_Press_Release.docx.pdf", title: "Robotiq press release: next-generation 2F-85 and 2F-140 (2018-11-07)", accessed: 2026-11-18}
  - {url: "https://github.com/robotiq/robotiq-ros", title: robotiq-ros repository README, accessed: 2026-11-18}
  - {url: "https://blog.robotiq.com/robotiq-releases-ros-2-packages-for-adaptive-grippers/", title: "Robotiq blog: Robotiq releases ROS 2 packages for adaptive grippers (2026-08-26)", accessed: 2026-11-18}
  - {url: "https://github.com/robotiq/robotiq-sdk/tree/main/grippers", title: Robotiq grippers C++ SDK and docs, accessed: 2026-11-18}
  - {url: "https://github.com/PickNikRobotics/ros2_robotiq_gripper", title: PickNik ros2_robotiq_gripper README, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/robotiq_2f85", title: MuJoCo Menagerie robotiq_2f85, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/robotiq_2f85_v4", title: MuJoCo Menagerie robotiq_2f85_v4, accessed: 2026-11-18}
  - {url: "https://github.com/robotiq/isaacsim_assets", title: Robotiq Isaac Sim assets README, accessed: 2026-11-18}
  - {url: "https://robosuite.ai/docs/modules/robots.html", title: robosuite robots and grippers, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2403.12945", title: "DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset", accessed: 2026-11-18}
  - {url: "https://www.robotics247.com/article/robotiq-launches-tsf-85-tactile-sensor-fingertips-for-2f-85-adaptive-gripper", title: "Robotics 24/7: Robotiq launches TSF-85 tactile sensor fingertips (2026-02-02)", accessed: 2026-11-18}
  - {url: "https://automationdistribution.com/robotiq-agc-grp-2f85-2f-85", title: "Automation Distribution: Robotiq 2F-85 basic adaptive gripper unit", accessed: 2026-11-18}
  - {url: "https://automationdistribution.com/robotiq-2-finger-85-gripper-universal-robots-installation-kit-agc-ur-kit-002", title: "Automation Distribution: Robotiq 2F-85 Universal Robots installation kit", accessed: 2026-11-18}
  - {url: "https://umi-gripper.github.io/", title: UMI project page, accessed: 2026-11-18}
  - {url: "https://github.com/Kinovarobotics/ros2_kortex", title: Kinova ros2_kortex README, accessed: 2026-11-18}
---

# Robotiq 2F-85

An electric two-finger gripper from Robotiq (Quebec, Canada) with an 85 mm stroke and fingers that
either pinch in parallel or wrap around an object. It is the gripper on the DROID data-collection
setup and ships as a model in MuJoCo Menagerie, robosuite and Isaac Sim [8][10][11][12]. Since
2026 Robotiq maintains an open ROS 2 driver and C++ SDK for it [4][5][6]. The hardware is closed
and sold through distributors.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | 2F-85 | — |
| Degrees of freedom | 1: a single position command moves both fingers, coupled through linkages | [4][6] |
| Stroke | 85 mm, adjustable (maker's claim) | [2] |
| Grip force | 20 to 235 N, adjustable (maker's claim) | [2] |
| Payload, form-fit and friction grip | 5 kg each (maker's claim) | [2] |
| Closing speed | 20 to 150 mm/s, adjustable (maker's claim) | [2] |
| Mass | 0.9 kg (maker's claim) | [2] |
| Position resolution at the fingertip | 0.4 mm (maker's claim) | [2] |
| Ingress protection | IP40 | [2] |
| Interface | Modbus RTU over RS-485; factory default 115200 baud, 8N1, slave ID 0x09 | [2][6] |
| Status and command rate | Up to about 250 Hz at 115200 baud through the SDK | [6] |
| Supply | 24 V | [6][14] |

Robotiq states the sheet values are "for reference only" and points to the manual [2]. The
manual host (assets.robotiq.com) had no DNS record on 2026-11-18, so the manual was not read.

## How it works

One electric drive closes both fingers through a linkage. Robotiq describes a patented finger
design that grips in parallel, inside or outside a part, and also wraps around an object in an
encompassing mode [3]. Fingertips are swappable [3]. The current generation came out in November
2018; Robotiq's release dates the line's launch six years earlier, which gives the 2012 in the
frontmatter [3]. The ROS description models one actuated
knuckle joint and drives the other links as mimic joints [4].

The gripper has its own controller. A host writes three byte-sized requests (position, speed and
force, each 0 to 255) over Modbus RTU and reads back position, motor current and an object-status
flag that says whether the fingers stopped on contact while opening or closing [6]. The force
register is not a value in newtons: the real grip force also depends on speed, so it cannot be
converted [6]. It connects through a USB to RS-485 adapter or the tool connector of a Universal
Robots arm, at 24 V [6].

Robotiq released its own ROS 2 packages in August 2026: a `ros2_control` hardware interface built
on its C++ SDK, controllers and descriptions, on Humble, Jazzy and Lyrical from one branch, BSD-3-Clause
[4][5]. They support the 2F-85, 2F-140, Hand-E and Hand-E C10, but release 1.1.0 was validated on
hardware only with a 2F-85 [4][5]. They are a drop-in replacement for PickNik's community package,
which started the code in 2022 and is still maintained [5][7]. The same repo holds an MCP server
that lets an LLM agent open, close and query the gripper [4]. The C++ SDK builds on Linux,
Windows, macOS and RTOS targets [6]. The old ROS 1 packages from ROS-Industrial are archived [4].

Models: URDF/Xacro for the 2F-85 and 2F-140, with a UR mounting adapter, in `robotiq_description`
[4]; MuJoCo Menagerie's `robotiq_2f85` (converted from the ROS-Industrial URDF) and
`robotiq_2f85_v4` (rebuilt from Robotiq's STEP files), both BSD-2-Clause [8][9]; Robotiq's own Isaac
Sim USD assets with PhysX and Newton variants [10]; and robosuite's Robotiq 85 and 140 grippers [11].

| Variant | Stroke | Grip force | Payload | Mass | Closing speed | Source |
|---|---|---|---|---|---|---|
| 2F-85 | 85 mm | 20 to 235 N | 5 kg | 0.9 kg | 20 to 150 mm/s | [2] |
| 2F-140 | 140 mm | 10 to 125 N | 2.5 kg | 1 kg | 30 to 250 mm/s | [2] |

## What it is used for

- Research arms: DROID, a dataset of 76k trajectories (350 hours) over 564 scenes, was collected
  on Franka Panda arms fitted with the 2F-85 [12].
- Simulation benchmarks: robosuite offers the Robotiq 85 and 140 grippers for its arms [11].
- Tactile learning: the TSF-85 fingertips (launched early 2026) add a 4 x 7 taxel grid, slip
  sensing at 1000 Hz and an IMU, aimed at imitation and reinforcement learning (maker's claims) [13].
- Industrial pick-and-place and machine tending on cobots, its original market [2][3].

## Cost and BOM

Robotiq lists no price; its page asks you to request pricing [1].

| Item | Price (USD) | Type | Date | Source |
|---|---|---|---|---|
| 2F-85 basic gripper unit, distributor | 9,271.41 | retail | 2026-11-18 | [14] |
| 2F-85 UR installation kit: gripper, coupling, 10 m cable, USB to RS-485 adapter, fingertips | 10,482.66 | retail | 2026-11-18 | [15] |

The basic-unit page does not say whether a coupling or cable is included [14].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Mechanical and electronic design | — | Not published | Proprietary |
| CAD | STEP | [Robotiq support file](https://blog.robotiq.com/hubfs/support-files/2F85_Opened_20190924-Sep-06-2024-02-25-46-4707-PM.step) [9] | No licence stated |
| ROS 2 driver, controllers, description, MCP server | C++, Python, Xacro | [robotiq/robotiq-ros](https://github.com/robotiq/robotiq-ros) | BSD-3-Clause |
| C++ SDK | C++ | [robotiq/robotiq-sdk](https://github.com/robotiq/robotiq-sdk) | BSD-3-Clause |
| Isaac Sim assets | USD | [robotiq/isaacsim_assets](https://github.com/robotiq/isaacsim_assets) | BSD-3-Clause |
| MuJoCo models | MJCF | [Menagerie](https://github.com/google-deepmind/mujoco_menagerie) | BSD-2-Clause |
| Community ROS 2 driver | C++, Xacro | [PickNikRobotics/ros2_robotiq_gripper](https://github.com/PickNikRobotics/ros2_robotiq_gripper) | BSD-3-Clause |
| Firmware | — | Not published | Proprietary |

## Strengths and limits

- **Strengths:** a common research default, so data, policies and sim models carry over [8][11][12];
  a maker-maintained open driver and SDK on current ROS 2 LTS releases [4][5]; models in MuJoCo,
  Isaac Sim, robosuite and URDF [4][8][9][10][11]; parallel and wrapping grips from one drive [3];
  5 kg rated payload [2].
- **Limits:** about $9,300 at a distributor and no public list price [1][14]; IP40 only [2];
  commands are 8-bit and force has no unit in newtons [6]; the ROS 2 driver reports no holding
  effort [4]; the 2026 driver was hardware-tested only on the 2F-85 [5]; hardware and firmware
  are closed.

## What to reuse

- One drive plus a finger linkage that switches between parallel pinch and wrapping grasp [3].
- Contact detection from the drive stopping before its target, reported as a status flag, with
  no extra sensor [6].

## Related robots

- [Franka Panda](franka-panda.md): DROID pairs it with the 2F-85 [12].
- [Universal Robots](universal-robots.md): the description ships a UR adapter and distributors
  sell a UR kit [4][15].
- [Kinova Gen3](kinova-gen3.md): Kinova's ROS 2 driver takes the 2F-85 or 2F-140 as its
  gripper option [17].
- [UMI gripper](umi-gripper.md): its robot side needs a parallel gripper with more than 85 mm of
  stroke [16].
- Robotiq Hand-E and Hand-E C10 use the same driver and SDK [4][6].

## Sources

1. [Robotiq Adaptive Grippers product page](https://robotiq.com/products/adaptive-grippers), accessed 2026-11-18
2. [Robotiq Adaptive Grippers product sheet (May 2025)](https://blog.robotiq.com/hubfs/Product-sheets/Adaptive%20Grippers/Product-sheet-Adaptive-Grippers-EN.pdf), accessed 2026-11-18
3. [Robotiq press release: next-generation 2F-85 and 2F-140 (2018-11-07)](https://blog.robotiq.com/hubfs/press%20releases/2F-85%20&%202F-140_Press_Release.docx.pdf), accessed 2026-11-18
4. [robotiq-ros repository README](https://github.com/robotiq/robotiq-ros), accessed 2026-11-18
5. [Robotiq blog: Robotiq releases ROS 2 packages for adaptive grippers (2026-08-26)](https://blog.robotiq.com/robotiq-releases-ros-2-packages-for-adaptive-grippers/), accessed 2026-11-18
6. [Robotiq grippers C++ SDK and docs](https://github.com/robotiq/robotiq-sdk/tree/main/grippers), accessed 2026-11-18
7. [PickNik ros2_robotiq_gripper README](https://github.com/PickNikRobotics/ros2_robotiq_gripper), accessed 2026-11-18
8. [MuJoCo Menagerie robotiq_2f85](https://github.com/google-deepmind/mujoco_menagerie/tree/main/robotiq_2f85), accessed 2026-11-18
9. [MuJoCo Menagerie robotiq_2f85_v4](https://github.com/google-deepmind/mujoco_menagerie/tree/main/robotiq_2f85_v4), accessed 2026-11-18
10. [Robotiq Isaac Sim assets README](https://github.com/robotiq/isaacsim_assets), accessed 2026-11-18
11. [robosuite robots and grippers](https://robosuite.ai/docs/modules/robots.html), accessed 2026-11-18
12. [DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset](https://arxiv.org/abs/2403.12945), accessed 2026-11-18
13. [Robotics 24/7: Robotiq launches TSF-85 tactile sensor fingertips (2026-02-02)](https://www.robotics247.com/article/robotiq-launches-tsf-85-tactile-sensor-fingertips-for-2f-85-adaptive-gripper), accessed 2026-11-18
14. [Automation Distribution: Robotiq 2F-85 basic adaptive gripper unit](https://automationdistribution.com/robotiq-agc-grp-2f85-2f-85), accessed 2026-11-18
15. [Automation Distribution: Robotiq 2F-85 Universal Robots installation kit](https://automationdistribution.com/robotiq-2-finger-85-gripper-universal-robots-installation-kit-agc-ur-kit-002), accessed 2026-11-18
16. [UMI project page](https://umi-gripper.github.io/), accessed 2026-11-18
17. [Kinova ros2_kortex README](https://github.com/Kinovarobotics/ros2_kortex), accessed 2026-11-18
