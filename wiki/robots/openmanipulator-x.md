---
type: robot
name: OpenManipulator-X
summary: ROBOTIS's small 4-joint arm with a gripper on five Dynamixel XM430 servos, with Onshape CAD and Apache-2.0 ROS 2 packages; the standard arm for TurtleBot3 mobile manipulation, now joined by the OMX and OMY lines.
tags: [dynamixel, xm430, robotis, turtlebot3, ros2, moveit, onshape, education, omx, omy]
category: arm
tier: B
openness: partial
maker: ROBOTIS
year: 2017
license: {hardware: , software: Apache-2.0, docs: CC-BY-4.0}
links: {repo: "https://github.com/ROBOTIS-GIT/open_manipulator", docs: "https://emanual.robotis.com/docs/en/platform/openmanipulator_x/overview/", cad: "https://cad.onshape.com/documents/9442f03bd8ccac084fda9dd3/w/039e8dbd53e0782540ea5b0d/e/6f08aa8ac3d3e5b3054f7782", paper: , site: "https://robotis.us/openmanipulator-x-rm-x52-tnm"}
specs: {dof: 5, payload_kg: 0.5, reach_mm: 380, mass_kg: 0.7, size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "Dynamixel XM430-W350-T smart servos (5)", mcu: "none on the arm; OpenCR board or a U2D2 adapter with power hub, sold separately", compute: "host PC, or OpenCR alone for simple control", sensors: ["servo encoders"], sim_models: ["URDF and Gazebo (open_manipulator_description)", "MJCF (open_manipulator_description, since 2026-09)", "URDF and SRDF (robot_descriptions, open_manipulator_x_description)"], ros2: official}
cost: {type: retail, usd: 1629.09, as_of: 2026-11-18, source: "https://robotis.us/openmanipulator-x-rm-x52-tnm"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-11-18, stars: 679, active: true}
use_cases: [education, research, manipulation, teleop]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://emanual.robotis.com/docs/en/platform/openmanipulator_x/specification/", title: "ROBOTIS e-Manual: OpenMANIPULATOR-X specification", accessed: 2026-11-18}
  - {url: "https://emanual.robotis.com/docs/en/platform/openmanipulator_x/overview/", title: "ROBOTIS e-Manual: OpenMANIPULATOR-X overview", accessed: 2026-11-18}
  - {url: "https://emanual.robotis.com/docs/en/platform/openmanipulator_x/assembly/", title: "ROBOTIS e-Manual: OpenMANIPULATOR-X assembly and part list", accessed: 2026-11-18}
  - {url: "https://robotis.us/openmanipulator-x-rm-x52-tnm", title: "ROBOTIS US store: OpenManipulator-X (RM-X52-TNM)", accessed: 2026-11-18}
  - {url: "https://github.com/ROBOTIS-GIT/open_manipulator", title: open_manipulator repository README and changelog, accessed: 2026-11-18}
  - {url: "https://emanual.robotis.com/docs/en/platform/turtlebot3/opensource/", title: "ROBOTIS e-Manual: TurtleBot3 open source and licences", accessed: 2026-11-18}
  - {url: "https://discourse.openrobotics.org/t/introducing-the-openmanipulator/2595", title: "Open Robotics Discourse: Introducing the OpenManipulator", accessed: 2026-11-18}
  - {url: "https://ai.robotis.com/omx/introduction_omx.html", title: "ROBOTIS AI docs: OMX introduction", accessed: 2026-11-18}
  - {url: "https://ai.robotis.com/omx/hardware_omx.html", title: "ROBOTIS AI docs: OMX hardware", accessed: 2026-11-18}
  - {url: "https://ai.robotis.com/omy/hardware_omy.html", title: "ROBOTIS AI docs: OMY hardware", accessed: 2026-11-18}
  - {url: "https://huggingface.co/docs/lerobot/omx", title: LeRobot OMX guide, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie", title: MuJoCo Menagerie model list, accessed: 2026-11-18}
  - {url: "https://github.com/robot-descriptions/robot_descriptions.py", title: robot_descriptions model list, accessed: 2026-11-18}
---

# OpenManipulator-X

A small arm from ROBOTIS: four joints and a gripper, each driven by a Dynamixel XM430 servo, with
printable parts on Onshape and Apache-2.0 ROS 2 packages [1][2][5]. ROBOTIS announced the
OpenManipulator in 2017 as a TurtleBot3 companion [7], and its manuals pair it with a TurtleBot3
for mobile manipulation [2][6]. ROBOTIS now also sells the OMX and OMY arms for learning work;
LeRobot supports the OMX [8][11].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | OpenMANIPULATOR-X (RM-X52-TNM) | [1] |
| Degrees of freedom | 4 arm joints plus a gripper (5 servos) | [1] |
| Servos | 5 x Dynamixel XM430-W350-T, 12 V | [1][4] |
| Payload | 500 g (maker's claim) | [1] |
| Reach | 380 mm (maker's claim) | [1] |
| Mass | 0.70 kg (maker's claim) | [1] |
| Repeatability | < 0.2 mm (maker's claim) | [1] |
| Joint speed | 46 RPM (maker's claim) | [1] |
| Joint limits in the URDF | J1 ±180°, J2 ±86°, J3 −86 to 80°, J4 −97 to 113° | [5] |
| Gripper stroke | 20 to 75 mm | [1] |
| Bus | TTL multidrop (Dynamixel protocol) | [1] |

## How it works

The servos chain from the base to the gripper through ROBOTIS FR12 metal brackets and plastic
links [3][4]. The gripper turns one servo's rotation into parallel jaw travel through a crank, link
rods and small rail blocks [3]. ROBOTIS calls the design modular: the same joints can be rearranged
into SCARA, planar, delta, Stewart or linear layouts [2].

There is no board on the arm. A PC drives the bus through a U2D2 adapter and power hub, or an
OpenCR board runs the arm alone with on-board kinematics examples; both are sold separately [2][3].
The `open_manipulator` repository holds the ROS 2 packages: bringup, ros2_control hardware
interfaces, MoveIt config, a GUI, teleop and Docker images [5]. Releases target ROS 2
Jazzy and Kilted; a Humble branch was last updated in July 2025 [5]. The same repository now also
serves the OMX and OMY arms [5].

The description package has URDF, Gazebo and, since September 2026, MuJoCo models of the
OpenManipulator-X [5]. robot_descriptions loads it as `open_manipulator_x_description` [13].
MuJoCo Menagerie has no OpenManipulator-X model; it carries the OMY-3M [12].

| Variant | DoF | Reach | Payload | Actuators | Note | Source |
|---|---|---|---|---|---|---|
| OpenMANIPULATOR-X | 4 + gripper | 380 mm | 500 g | 5 x XM430-W350-T | This page | [1] |
| OMX-F (follower) | 5 + gripper | 400 mm | 100 g at full reach, 250 g nearer | XL430-W250-T and XL330-M288-T | 560 g, 12 V; LeRobot `omx_follower` | [9][11] |
| OMX-L (leader) | 5 + gripper | 335 mm | — | XL330-M288-T and XL330-M077-T | 360 g, 5 V; sold only as a pair with OMX-F | [8][9] |
| OMY-F3M (follower) | 6 | 580 mm | 3 kg | Dynamixel-Y (YM080, YM070) | 13.5 kg, 24 V, Ethernet | [10] |
| OMY-L100 (leader) | 6 | 560 mm | — | XH540 and XC330 | 1.46 kg | [10] |

## What it is used for

- Teaching ROS 2 manipulation: MoveIt, Gazebo and the GUI on a small desktop arm [2][5].
- Mobile manipulation on a TurtleBot3, which ROBOTIS documents as a combined platform [2][6].
- For imitation learning, ROBOTIS points to the OMX instead: it ships pre-configured and runs
  LeRobot's record, train and evaluate workflow out of the box [8][11].

## Cost and BOM

| Item | Price (USD) | Type | Date | Source |
|---|---|---|---|---|
| OpenManipulator-X kit, unassembled (ROBOTIS US) | 1,629.09 | retail | 2026-11-18 | [4] |

The kit holds the five servos, the plastic frame set, brackets, cables, fasteners and tools. It
leaves out the 12 V 5 A supply, the U2D2 and power hub or OpenCR, and the base plate [4]. On
2026-11-18 it was sold out, with stock expected in mid-January [4]. `build` stays empty: ROBOTIS's
part list gives quantities but no prices and does not mark which parts are printed, and no licence
is named for the hardware files [3][6].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Arm CAD | Onshape (exports STL, STEP) | [Onshape document](https://cad.onshape.com/documents/9442f03bd8ccac084fda9dd3/w/039e8dbd53e0782540ea5b0d/e/6f08aa8ac3d3e5b3054f7782) via the e-Manual [3] | None named; ROBOTIS lists it as open hardware [6] |
| Printable parts | STL | ROBOTIS Thingiverse page linked from the e-Manual [3] | None named |
| ROS 2 packages and models | ROS 2, URDF, MJCF | [open_manipulator](https://github.com/ROBOTIS-GIT/open_manipulator) [5] | Apache-2.0 |
| OMX CAD | STEP, PDF drawings, Printables | ROBOTIS AI docs [9] | The docs footer says its "AI Manipulator" line is Apache-2.0; the files name no licence |
| Docs | Web | e-Manual, moving to ROBOTIS Docs [2] | CC-BY-4.0 per the e-Manual [6] |
| Servos and firmware | Closed commercial parts | ROBOTIS | Not open |

## Strengths and limits

- **Strengths:** official, actively maintained ROS 2 packages (last commit 2026-11-18) [5];
  MoveIt, Gazebo and MuJoCo models in one repository [5]; fits TurtleBot3 [2]; light, at 0.7 kg
  [1]; a clear upgrade path to the OMX and OMY in the same software [5].
- **Limits:** only four arm joints, so the gripper cannot take an arbitrary orientation; 500 g
  payload and 380 mm reach (maker's claims) [1]; USD 1,629 before a controller and power supply
  [4]; no licence named for the hardware files [6]; sold out on the day checked [4].

## What to reuse

- A parallel gripper from one servo, a crank and two rail blocks [3].
- Metal servo brackets plus printed links: the links can change length without new brackets [2].

## Related robots

- [TurtleBot3](turtlebot3.md): ROBOTIS's mobile base; the Waffle Pi carries this arm.
- [Interbotix X-Series arms](interbotix-x-series-arms.md): larger research arms on the same
  Dynamixel servos.
- [Koch v1.1](koch-v1-1.md): a printed Dynamixel leader-follower arm, close to the OMX in idea.
- [SO-101](so-101.md): the cheaper Feetech-based LeRobot arm.

## Sources

1. [ROBOTIS e-Manual: OpenMANIPULATOR-X specification](https://emanual.robotis.com/docs/en/platform/openmanipulator_x/specification/), accessed 2026-11-18
2. [ROBOTIS e-Manual: OpenMANIPULATOR-X overview](https://emanual.robotis.com/docs/en/platform/openmanipulator_x/overview/), accessed 2026-11-18
3. [ROBOTIS e-Manual: OpenMANIPULATOR-X assembly and part list](https://emanual.robotis.com/docs/en/platform/openmanipulator_x/assembly/), accessed 2026-11-18
4. [ROBOTIS US store: OpenManipulator-X (RM-X52-TNM)](https://robotis.us/openmanipulator-x-rm-x52-tnm), accessed 2026-11-18
5. [open_manipulator repository README and changelog](https://github.com/ROBOTIS-GIT/open_manipulator), accessed 2026-11-18
6. [ROBOTIS e-Manual: TurtleBot3 open source and licences](https://emanual.robotis.com/docs/en/platform/turtlebot3/opensource/), accessed 2026-11-18
7. [Open Robotics Discourse: Introducing the OpenManipulator](https://discourse.openrobotics.org/t/introducing-the-openmanipulator/2595), accessed 2026-11-18
8. [ROBOTIS AI docs: OMX introduction](https://ai.robotis.com/omx/introduction_omx.html), accessed 2026-11-18
9. [ROBOTIS AI docs: OMX hardware](https://ai.robotis.com/omx/hardware_omx.html), accessed 2026-11-18
10. [ROBOTIS AI docs: OMY hardware](https://ai.robotis.com/omy/hardware_omy.html), accessed 2026-11-18
11. [LeRobot OMX guide](https://huggingface.co/docs/lerobot/omx), accessed 2026-11-18
12. [MuJoCo Menagerie model list](https://github.com/google-deepmind/mujoco_menagerie), accessed 2026-11-18
13. [robot_descriptions model list](https://github.com/robot-descriptions/robot_descriptions.py), accessed 2026-11-18
