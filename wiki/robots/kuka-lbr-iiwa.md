---
type: robot
name: KUKA LBR iiwa and LBR Med
summary: KUKA's seven-axis lightweight arm with a torque sensor in every joint, descended from DLR's LWR and sold since 2013 in 7 kg and 14 kg versions plus the medical LBR Med; closed controller, driven from ROS 2 by community FRI stacks and modelled in Drake.
tags: [cobot, iiwa, lbr-med, torque-sensing, 7-dof, fri, sunrise, drake, ros2, commercial]
category: arm
tier: B
openness: closed-reference
maker: KUKA
year: 2013
license: {hardware: , software: Apache-2.0, docs: }
links: {repo: "https://github.com/lbr-stack/lbr_fri_ros2_stack", docs: "https://lbr-stack.readthedocs.io/en/latest", cad: , paper: , site: "https://www.kuka.com/en-de/products/robot-systems/industrial-robots/lbr-iiwa"}
specs: {dof: 7, payload_kg: 14, reach_mm: 820, mass_kg: 29.9, size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "7 joints, each with an integrated joint torque sensor", mcu: , compute: "KUKA Sunrise Cabinet (quad-core, Sunrise.OS, Java); external PC over FRI for real-time control", sensors: ["joint position sensing", "joint torque sensors in all 7 axes"], sim_models: ["URDF/Xacro and Gazebo (lbr_fri_ros2_stack: iiwa7, iiwa14, med7, med14)", "URDF and SDF (Drake models repository, iiwa_description: iiwa 14 and dual iiwa 14)", "MJCF (MuJoCo Menagerie, kuka_iiwa_14, from Drake)", "URDF and MJCF (robot_descriptions: iiwa7, iiwa14)"], ros2: community}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-11-06, stars: 277, active: true}
use_cases: [research, manipulation, education, hri]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://www.kuka.com/en-de/products/robot-systems/industrial-robots/lbr-iiwa", title: KUKA LBR iiwa product page, accessed: 2026-11-18}
  - {url: "https://git.phschoen.de/phschoen/lwr_server/raw/commit/1debece1117ae5d940d2f15c0647304bf45473c6/lwrserv/doc/LBRiiwa_en.pdf", title: "KUKA LBR iiwa brochure with technical data (undated KUKA PDF, copy in a third-party repository)", accessed: 2026-11-18}
  - {url: "https://www.kuka.com/en-de/industries/health-care/kuka-medical-robotics/lbr-med", title: KUKA LBR Med product page, accessed: 2026-11-18}
  - {url: "https://www.dlr.de/en/rm/research/robotic-systems/arms/lwr-iii/history-of-the-dlr-lwr", title: "DLR: History of the DLR LWR", accessed: 2026-11-18}
  - {url: "https://github.com/lbr-stack/lbr_fri_ros2_stack", title: lbr_fri_ros2_stack README, accessed: 2026-11-18}
  - {url: "https://doi.org/10.21105/joss.06138", title: "LBR-Stack: ROS 2 and Python Integration of KUKA FRI for Med and IIWA Robots (JOSS, 2024)", accessed: 2026-11-18}
  - {url: "https://github.com/lbr-stack/lbr_fri_ros2_stack/blob/jazzy/lbr_ros2_control/doc/lbr_ros2_control.rst", title: lbr_ros2_control documentation, accessed: 2026-11-18}
  - {url: "https://github.com/lbr-stack/lbr_fri_ros2_stack/blob/jazzy/lbr_fri_ros2_stack/doc/hardware_setup.rst", title: LBR-Stack hardware setup guide, accessed: 2026-11-18}
  - {url: "https://github.com/lbr-stack/fri", title: "lbr-stack/fri: CMake support for KUKA's FRI client SDK", accessed: 2026-11-18}
  - {url: "https://github.com/kroshu/kuka_drivers", title: kroshu/kuka_drivers README, accessed: 2026-11-18}
  - {url: "https://github.com/kroshu/kuka_drivers/blob/master/doc/wiki/3_Sunrise_FRI.md", title: kuka_drivers Sunrise FRI driver guide, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/kuka_iiwa_14", title: "MuJoCo Menagerie: kuka_iiwa_14", accessed: 2026-11-18}
  - {url: "https://github.com/RobotLocomotion/models/tree/master/iiwa_description", title: Drake models repository, iiwa_description, accessed: 2026-11-18}
  - {url: "https://github.com/robot-descriptions/robot_descriptions.py", title: robot_descriptions model list, accessed: 2026-11-18}
  - {url: "https://manipulation.csail.mit.edu/robot.html", title: "Robotic Manipulation (MIT course notes), chapter 2: Let's get you a robot", accessed: 2026-11-18}
---

# KUKA LBR iiwa and LBR Med

A seven-axis lightweight arm from KUKA with a torque sensor in every joint. It grew out of the DLR
Light-Weight Robot III, which KUKA licensed in 2004, and reached its current form as the LBR iiwa
in 2013 [4]. KUKA calls it the first series-produced sensitive robot [1]. For a builder it matters
as the arm modelled in Drake and taught in MIT's Robotic Manipulation course, a reference for
contact-rich manipulation [13][15]. It is still sold, at a price on request [1].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | LBR iiwa 14 R820 | [1][2] |
| Degrees of freedom | 7 revolute joints; no gripper included, so `dof: 7` | [1][2] |
| Rated payload | 14 kg (maker's claim) | [1][2] |
| Reach | 820 mm (maker's claim) | [1] |
| Mass | 29.9 kg (maker's claim) | [2] |
| Repeatability | ±0.15 mm, ISO 9283 (maker's claim) | [2] |
| Joint torque sensing | in all 7 axes; accuracy ±2% of maximum torque (maker's claim) | [1][2] |
| Axis ranges | A1, A3, A5 ±170°; A2, A4, A6 ±120°; A7 ±175° | [2] |
| Maximum torque | A1, A2 320 Nm; A3, A4 176 Nm; A5 110 Nm; A6, A7 40 Nm | [2] |
| Maximum joint speed | A1, A2 85°/s; A3 100°/s; A4 75°/s; A5 130°/s; A6, A7 135°/s | [2] |
| Programmable Cartesian stiffness | 0.01–5,000 N/m; 0.01–300 Nm/rad | [2] |
| Protection, mounting | IP54; any orientation; DIN ISO 9409-1-A50 flange | [1][2] |
| Controller | KUKA Sunrise Cabinet: quad-core, 500 x 483 x 190 mm, 23 kg, IP20 | [1][2] |

The technical data come from an undated KUKA brochure found as a copy in a third-party repository
[2]; KUKA's download centre listed no documents without an account. The brochure gives no TCP
speed, so `speed_mps` stays empty.

## How it works

Each joint has a torque sensor, so the controller can run joint and Cartesian impedance control
with programmable stiffness [2][7]. The arm runs from the KUKA Sunrise Cabinet, which is
programmed in Java with Sunrise Workbench [3][8]. For real-time control from outside, KUKA's Fast
Robot Interface (FRI) streams commands and state between the cabinet and an external PC; a Java
application on the cabinet opens the FRI session [8]. KUKA's FRI client SDK ships inside Sunrise
Workbench; lbr-stack/fri repackages it with CMake under Apache-2.0 and does not state a licence for
KUKA's own code [9].

KUKA has no maker-supported ROS 2 driver for the iiwa. kroshu/kuka_drivers pairs KUKA's officially
supported RSI drivers with community-supported code for legacy systems, and its Sunrise FRI driver
is in the community part; it supports only Sunrise 1.x, only the KLI network port, and no Cartesian
modes [10][11]. The better-maintained choice is lbr_fri_ros2_stack from King's College London: it
covers the iiwa 7, iiwa 14, Med 7 and Med 14 with FRI 1.11 to 2.7 on ROS 2 Jazzy, with ros2_control
controllers for joint position, torque and wrench commands, MoveIt configs, Gazebo simulation,
Python support and a JOSS paper [5][6][7].

For simulation, Drake's model repository has iiwa 14 URDFs, including a dual-arm setup, plus joint
limit and rotor parameters for the iiwa 7 and 14 [13]. Menagerie's `kuka_iiwa_14` is derived from
Drake's model, with force limits taken from KUKA's spec sheet [12]. robot_descriptions loads URDFs
of both arms [14].

| Variant | Payload | Reach | Mass | Repeatability | Note | Source |
|---|---|---|---|---|---|---|
| LBR iiwa 7 R800 | 7 kg | 800 mm | 23.9 kg | ±0.1 mm | Faster wrist (A6, A7 180°/s) | [1][2] |
| LBR iiwa 14 R820 | 14 kg | 820 mm | 29.9 kg | ±0.15 mm | Frontmatter variant | [1][2] |
| LBR iiwa 7 R800 CR, 14 R820 CR | 7 kg, 14 kg | 800, 820 mm | — | — | Cleanroom versions, floor mount only | [1] |
| LBR Med 7 R800 | 7 kg | 800 mm | ~25.5 kg | ±0.1 mm | Medical; Sunrise Cabinet Med, Sunrise.OS Med | [3] |
| LBR Med 14 R820 | 14 kg | 820 mm | ~32.3 kg | ±0.15 mm | Medical; IEC 60601-1 and IEC 62304 tested | [3] |

KUKA also sells the LBR iisy, a smaller sibling on its iiQKA.OS software, which this card does not
cover [1].

## What it is used for

- Contact-rich manipulation and force control research: the MIT Robotic Manipulation course uses
  the seven-joint iiwa as its main example, choosing it for its joint-torque sensing and control [15].
- Simulation-first work in Drake and MuJoCo with the community models [12][13].
- Medical robotics: the LBR Med is tested to medical standards to speed approval of devices built on
  it [3]; LBR-Stack was built at King's College London with medical-engineering funding [5].

## Cost and BOM

Price on request. KUKA's page offers a quote form and its my.KUKA marketplace, with no listed
price [1], so the frontmatter `cost` stays empty.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| ROS 2 stack (FRI, ros2_control, MoveIt, Gazebo, Python) | ROS 2 packages | [lbr_fri_ros2_stack](https://github.com/lbr-stack/lbr_fri_ros2_stack) [5] | Apache-2.0 |
| FRI client build support | CMake around KUKA's SDK | [lbr-stack/fri](https://github.com/lbr-stack/fri) [9] | Apache-2.0 for the CMake support; KUKA's SDK licence not stated |
| Alternative ROS 2 driver | ROS 2 packages | [kroshu/kuka_drivers](https://github.com/kroshu/kuka_drivers) [10] | Apache-2.0 |
| Models | URDF, SDF | Drake models repository, `iiwa_description` [13] | Licence files present, not read; Menagerie cites Drake's BSD-3-Clause [12] |
| MuJoCo model | MJCF | Menagerie `kuka_iiwa_14` [12] | BSD-3-Clause |
| Arm hardware, Sunrise.OS, cabinet firmware | — | Not published | Closed |

## Strengths and limits

- **Strengths:** torque sensors in all seven joints with programmable Cartesian stiffness [2]; up to
  14 kg payload, far more than other torque-sensing research arms [1]; IP54 and any mounting angle
  [2]; a certified medical variant [3]; strong academic tooling in Drake, LBR-Stack and the MIT
  course [5][13][15].
- **Limits:** closed Java controller; no maker-supported ROS 2 driver [10]; FRI setup needs Sunrise
  Workbench to deploy a Java app to the cabinet [8]; heavy, at 29.9 kg plus a 23 kg cabinet [2];
  price on request; KUKA's public pages give little technical data [1][2]; Menagerie models only the
  iiwa 14 [12].

## Related robots

- [Franka Panda](franka-panda.md): the lighter, cheaper seven-axis torque-sensing research arm.
- [Kinova Gen3](kinova-gen3.md): a much lighter seven-axis arm with joint torque sensors.
- [Universal Robots](universal-robots.md): six-axis industrial cobots without joint torque sensors.
- DLR LWR III and KUKA LBR 4 and LBR 4+: the iiwa's predecessors [4].

## Sources

1. [KUKA LBR iiwa product page](https://www.kuka.com/en-de/products/robot-systems/industrial-robots/lbr-iiwa), accessed 2026-11-18
2. [KUKA LBR iiwa brochure with technical data (undated KUKA PDF, copy in a third-party repository)](https://git.phschoen.de/phschoen/lwr_server/raw/commit/1debece1117ae5d940d2f15c0647304bf45473c6/lwrserv/doc/LBRiiwa_en.pdf), accessed 2026-11-18
3. [KUKA LBR Med product page](https://www.kuka.com/en-de/industries/health-care/kuka-medical-robotics/lbr-med), accessed 2026-11-18
4. [DLR: History of the DLR LWR](https://www.dlr.de/en/rm/research/robotic-systems/arms/lwr-iii/history-of-the-dlr-lwr), accessed 2026-11-18
5. [lbr_fri_ros2_stack README](https://github.com/lbr-stack/lbr_fri_ros2_stack), accessed 2026-11-18
6. [LBR-Stack: ROS 2 and Python Integration of KUKA FRI for Med and IIWA Robots (JOSS, 2024)](https://doi.org/10.21105/joss.06138), accessed 2026-11-18
7. [lbr_ros2_control documentation](https://github.com/lbr-stack/lbr_fri_ros2_stack/blob/jazzy/lbr_ros2_control/doc/lbr_ros2_control.rst), accessed 2026-11-18
8. [LBR-Stack hardware setup guide](https://github.com/lbr-stack/lbr_fri_ros2_stack/blob/jazzy/lbr_fri_ros2_stack/doc/hardware_setup.rst), accessed 2026-11-18
9. [lbr-stack/fri: CMake support for KUKA's FRI client SDK](https://github.com/lbr-stack/fri), accessed 2026-11-18
10. [kroshu/kuka_drivers README](https://github.com/kroshu/kuka_drivers), accessed 2026-11-18
11. [kuka_drivers Sunrise FRI driver guide](https://github.com/kroshu/kuka_drivers/blob/master/doc/wiki/3_Sunrise_FRI.md), accessed 2026-11-18
12. [MuJoCo Menagerie: kuka_iiwa_14](https://github.com/google-deepmind/mujoco_menagerie/tree/main/kuka_iiwa_14), accessed 2026-11-18
13. [Drake models repository, iiwa_description](https://github.com/RobotLocomotion/models/tree/master/iiwa_description), accessed 2026-11-18
14. [robot_descriptions model list](https://github.com/robot-descriptions/robot_descriptions.py), accessed 2026-11-18
15. [Robotic Manipulation (MIT course notes), chapter 2: Let's get you a robot](https://manipulation.csail.mit.edu/robot.html), accessed 2026-11-18
