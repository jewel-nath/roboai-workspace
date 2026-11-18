---
type: robot
name: Willow Garage PR2
summary: Willow Garage's two-armed research mobile manipulator, sold from 2010 at $400,000 and written entirely in ROS; discontinued, with support passed to Clearpath in 2014, BSD ROS 1 packages and full design files that Clearpath published in 2023 without a licence.
tags: [dual-arm, ros1, ethercat, willow-garage, clearpath, discontinued, gazebo, moveit]
category: mobile-manipulator
tier: B
openness: partial
maker: Willow Garage
year: 2010
license: {hardware: , software: BSD-3-Clause, docs: }
links: {repo: "https://github.com/PR2/pr2_common", docs: "https://www.clearpathrobotics.com/assets/downloads/pr2/pr2_manual_r321.pdf", cad: "https://docs.clearpathrobotics.com/docs_robots/legacy/pr2", paper: , site: }
specs: {dof: 19, payload_kg: , reach_mm: , mass_kg: 220, size_mm: , speed_mps: 1.0, runtime_h: 2}
stack: {actuators: "Maxon motors on every joint; spring-counterbalanced 7-DoF arms; prismatic torso; four steered casters with two driven wheels each", mcu: "one motor controller board per joint, on EtherCAT", compute: "two computers, each with two quad-core Nehalem processors and 24 GB RAM", sensors: ["Hokuyo UTM-30LX base laser", "Hokuyo UTM-30LX tilting laser", "wide and narrow stereo cameras", "Prosilica GC2450C 5 MP camera", "texture projector", "Microsoft Kinect in the head", "IMU", "gripper accelerometers", "fingertip pressure sensors"], sim_models: ["URDF/Xacro with Gazebo extensions (PR2/pr2_common pr2_description, ROS 1)", "URDF for ROS 2 (moveit/moveit_resources pr2_description, MoveIt test model)", "URDF (robot_descriptions pr2_description)"], ros2: none}
cost: {type: retail, usd: 400000, as_of: 2010-09-08, source: "https://www.engadget.com/2010-09-08-willow-garage-now-selling-the-pr2-for-400k-a-pop.html"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2025-01-14, stars: 45, active: false}
use_cases: [research, manipulation, navigation]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://www.clearpathrobotics.com/assets/downloads/pr2/pr2_manual_r321.pdf", title: "Willow Garage: PR2 User Manual (2012-10-05)", accessed: 2026-11-18}
  - {url: "https://robotsguide.com/robots/pr2", title: "IEEE Robots guide: PR2", accessed: 2026-11-18}
  - {url: "https://www.engadget.com/2010-09-08-willow-garage-now-selling-the-pr2-for-400k-a-pop.html", title: "Engadget: Willow Garage now selling the PR2 for $400k a pop (2010-09-08)", accessed: 2026-11-18}
  - {url: "https://spectrum.ieee.org/clearpath-robotics-to-provide-pr2-support-through-2016", title: "IEEE Spectrum: Clearpath Robotics to provide PR2 support through 2016 (2014-01-15)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/full-set-design-files-released-pr2-robot/", title: "The Robot Report: Full set of design files released for PR2 robot (2023-03-14)", accessed: 2026-11-18}
  - {url: "https://docs.clearpathrobotics.com/docs_robots/legacy/pr2", title: "Clearpath Robotics docs: PR2 design files", accessed: 2026-11-18}
  - {url: "https://github.com/PR2/pr2_common", title: "PR2/pr2_common (melodic-devel)", accessed: 2026-11-18}
  - {url: "https://github.com/moveit/moveit_resources/tree/ros2/pr2_description", title: "moveit_resources: pr2_description (ros2 branch)", accessed: 2026-11-18}
  - {url: "https://github.com/robot-descriptions/robot_descriptions.py", title: robot_descriptions model list, accessed: 2026-11-18}
  - {url: "https://people.eecs.berkeley.edu/~pabbeel/papers/Maitin-ShepardCusumano-TownerLeiAbbeel_ICRA2010.pdf", title: "Maitin-Shepard et al.: Cloth grasp point detection with application to robotic towel folding (ICRA 2010)", accessed: 2026-11-18}
---

# Willow Garage PR2

A two-armed mobile manipulator from Willow Garage, sold from September 2010 at $400,000 after 11
beta units went to labs [3]; its software was written entirely in ROS [5]. It is discontinued:
Willow Garage passed support to Clearpath Robotics in January 2014 [4] and shut down that year [5].
Clearpath published its CAD, schematics and cable drawings in 2023, so the design can be studied [6].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | PR2 with two arms; the one-armed PR2 SE is in the variant table | [2] |
| Degrees of freedom | 19 counted: torso lift, head pan and tilt, two 7-DoF arms, two 1-DoF grippers. Not counted: 4 steered casters with 8 driven wheels and the laser tilt joint. The IEEE Robots guide gives 20 | [1][2] |
| Mass, height | about 220 kg (manual); 226.8 kg in the Robots guide; up to 165 cm with the spine raised | [1][2] |
| Speed, battery | 3.6 km/h, about 1.0 m/s; 1.3 kWh lithium-ion, about 2 h | [1][2] |
| Arm effort limits | 30 Nm at shoulder, upper arm, elbow and forearm; 10 Nm at the wrist (URDF limits) | [1] |
| Payload, reach | not found in the sources read | — |
| Control | single hard real-time loop at 1 kHz on RT PREEMPT Linux, talking EtherCAT to the motor boards | [1] |
| Computers | two, each with two quad-core Nehalem processors and 24 GB RAM | [1] |
| Sensors | two Hokuyo UTM-30LX (base and tilting), wide and narrow stereo, 5 MP camera, texture projector, IMU, gripper accelerometers and fingertip pressure sensors | [1][2] |

## How it works

Four casters, each steered and driven by two wheels, carry the base; a prismatic torso lifts the arms
and head [1]. A spring counterbalance holds each arm's weight, so small motors only carry the
payload and the arms "simply cannot push very hard" [1]. Every joint's Maxon motor has its own
controller board on EtherCAT, run by one 1 ms real-time loop [1].

`pr2_common` holds `pr2_description` (URDF/Xacro with Gazebo extensions), messages and configs under
BSD; its default branch, `melodic-devel`, last changed on 2025-01-14 [7]. No official ROS 2 driver
exists; MoveIt 2 keeps a PR2 model for its tests [8] and robot_descriptions loads a PR2 URDF [9].

| Variant | Arms | Price | Source |
|---|---|---|---|
| PR2 | two 7-DoF | $400,000 list; $280,000 for proven open-source contributors (2010) | [3] |
| PR2 SE | one | $285,000 | [2] |

## What it is used for

- Research labs: 11 beta units in 2010 [3] and about 40 PR2s in use in January 2014 [4].
- Manipulation: Berkeley folded unseen towels on a prototype PR2, 50 of 50 trials [10].
- ROS development: Clearpath cites over 1,000 software libraries for the platform [5].
- Planning tests: MoveIt 2 still uses the PR2 model in its test resources [8].

## Cost and BOM

Retail $400,000 at launch on 2010-09-08, or $280,000 with the open-source discount [3]; the PR2 SE
cost $285,000 [2]. It is no longer made; in 2014 Willow Garage sold its remaining stock [4].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Description, messages, configs | ROS 1 packages, URDF/Xacro | [pr2_common](https://github.com/PR2/pr2_common) [7] | BSD-3-Clause |
| ROS 2 test model | URDF | [moveit_resources](https://github.com/moveit/moveit_resources/tree/ros2/pr2_description) [8] | BSD |
| CAD, schematics, cable drawings, electrical manufacturing files | ZIP archives; CAD 11 GB | [Clearpath docs](https://docs.clearpathrobotics.com/docs_robots/legacy/pr2) [6] | None stated; site footer says all rights reserved |

## Strengths and limits

- **Strengths:** two 7-DoF arms on a lifting torso, a dense head sensor suite and 1 kHz EtherCAT
  control [1]; its full design files are public [6]; long-used BSD ROS packages [7].
- **Limits:** discontinued; Clearpath's first support pledge ran to the end of 2016 [4]; ROS 1 only [7];
  about 220 kg and 2 h per charge [1]; design files carry no licence [6]; $400,000 new [3].

## What to reuse

- Spring counterbalance on the arms, so small motors suffice and the arm is weak by design [1].
- One hard real-time loop driving per-joint motor boards over EtherCAT [1].

## Related robots

- [Fetch](fetch.md), [TIAGo](tiago.md), [Hello Robot Stretch](hello-robot-stretch.md): later, smaller research mobile manipulators.
- [Baxter](baxter.md): another discontinued research robot with an open ROS 1 SDK.
- [Clearpath Robotics](clearpath-robots.md): the company that took over PR2 support [4].

## Sources

1. [Willow Garage: PR2 User Manual (2012-10-05)](https://www.clearpathrobotics.com/assets/downloads/pr2/pr2_manual_r321.pdf), accessed 2026-11-18
2. [IEEE Robots guide: PR2](https://robotsguide.com/robots/pr2), accessed 2026-11-18
3. [Engadget: Willow Garage now selling the PR2 for $400k a pop (2010-09-08)](https://www.engadget.com/2010-09-08-willow-garage-now-selling-the-pr2-for-400k-a-pop.html), accessed 2026-11-18
4. [IEEE Spectrum: Clearpath Robotics to provide PR2 support through 2016 (2014-01-15)](https://spectrum.ieee.org/clearpath-robotics-to-provide-pr2-support-through-2016), accessed 2026-11-18
5. [The Robot Report: Full set of design files released for PR2 robot (2023-03-14)](https://www.therobotreport.com/full-set-design-files-released-pr2-robot/), accessed 2026-11-18
6. [Clearpath Robotics docs: PR2 design files](https://docs.clearpathrobotics.com/docs_robots/legacy/pr2), accessed 2026-11-18
7. [PR2/pr2_common (melodic-devel)](https://github.com/PR2/pr2_common), accessed 2026-11-18
8. [moveit_resources: pr2_description (ros2 branch)](https://github.com/moveit/moveit_resources/tree/ros2/pr2_description), accessed 2026-11-18
9. [robot_descriptions model list](https://github.com/robot-descriptions/robot_descriptions.py), accessed 2026-11-18
10. [Maitin-Shepard et al.: Cloth grasp point detection with application to robotic towel folding (ICRA 2010)](https://people.eecs.berkeley.edu/~pabbeel/papers/Maitin-ShepardCusumano-TownerLeiAbbeel_ICRA2010.pdf), accessed 2026-11-18
