---
type: robot
name: iCub
summary: Child-size open research humanoid from IIT with 53 DoF, dexterous hands, force/torque sensors and tactile skin on the YARP middleware; GPL and BSD software, CC-BY-SA models and a public subset of its CAD under CERN-OHL-W-2.0. iCub3 and ergoCub are larger successors.
tags: [research-humanoid, yarp, tactile-skin, force-torque, cognitive-robotics, iit, robotcub, icub3, ergocub, gazebo]
category: humanoid
tier: B
openness: partial
maker: Istituto Italiano di Tecnologia (IIT), from the EU RobotCub project
year: 2008
license: {hardware: CERN-OHL-W-2.0, software: GPL-2.0-or-later AND BSD-3-Clause, docs: }
links: {repo: "https://github.com/robotology/icub-main", docs: "https://icub-tech-iit.github.io/documentation/", cad: "https://github.com/mesh-iit/cad-mechanics-public", paper: "https://www.robotcub.org/misc/papers/08_Metta_Sandini_Vernon_etal.pdf", site: "https://icub.iit.it"}
specs: {dof: 53, payload_kg: , reach_mm: , mass_kg: 30, size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "electric motors; zero-backlash main joints and elastic actuators in the legs (maker's spec)", mcu: , compute: "onboard Intel i7 PC, 4 GB RAM, 32 GB SSD, Ubuntu (Rev 2.5 spec)", sensors: ["2 Point Grey Dragonfly 2 cameras (640 x 480) in the eyes", "2 microphones", "BNO055 IMU in the head", "six-axis force/torque sensors in arms and legs", "over 3000 capacitive tactile sensors", "absolute magnetic joint encoders"], sim_models: ["URDF and SDF (icub-models: iCub v1 to v2.7, Gazebo-tuned versions)", "URDF and a MuJoCo generator script (ergocub-software, ergoCub only)"], ros2: official}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-11-03, stars: 121, active: true}
use_cases: [research, hri, manipulation, locomotion, teleop]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://www.iit.it/documents/175012/528824/Technical-specs_iCub_robot_Rev_2.3_05082019+%282%29.pdf/56ccea3f-af0d-8ecf-f1f5-a387d2223a45", title: "IIT: Technical specifications of the iCub platform, Rev 2.5 (2019)", accessed: 2026-11-18}
  - {url: "https://icub.iit.it/products/product-catalog", title: iCub product catalogue (IIT), accessed: 2026-11-18}
  - {url: "https://www.robotcub.org/misc/papers/08_Metta_Sandini_Vernon_etal.pdf", title: "Metta et al. (2008): The iCub humanoid robot, an open platform for research in embodied cognition", accessed: 2026-11-18}
  - {url: "https://github.com/robotology/icub-main", title: icub-main repository, accessed: 2026-11-18}
  - {url: "https://github.com/robotology/yarp", title: YARP repository, accessed: 2026-11-18}
  - {url: "https://github.com/robotology/yarp-devices-ros2", title: yarp-devices-ros2 repository, accessed: 2026-11-18}
  - {url: "https://github.com/robotology/icub-models", title: icub-models repository, accessed: 2026-11-18}
  - {url: "https://github.com/mesh-iit/cad-mechanics-public", title: cad-mechanics-public (IIT public CAD subset), accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2203.06972", title: "Dafarra et al.: iCub3 Avatar System", accessed: 2026-11-18}
  - {url: "https://github.com/icub-tech-iit/ergocub-software", title: ergocub-software repository, accessed: 2026-11-18}
---

# iCub

A child-size humanoid from the Istituto Italiano di Tecnologia (IIT) in Genoa, built in the EU
RobotCub project and described in 2008 to study how a robot learns through its body [3]. It has 53
joints, coupled dexterous hands, force/torque sensors and a tactile skin [1]. IIT still sells and
develops it [2][4]. For a builder it is a reference design and a source of models and software.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | iCub 2.x, as in the Rev 2.5 spec (2019) | [1] |
| Degrees of freedom | 53 motors: eyes 3, neck 3, torso 3, arms 7 each, hands 9 each, legs 6 each; each hand has 19 joints | [1] |
| Height, width | about 105 cm, 36.5 cm (maker's claim) | [1] |
| Mass | 30 kg; 33 kg with the battery backpack (maker's claim) | [1] |
| Vision, audio | 2 Dragonfly 2 cameras (640 x 480) in the eyes; 2 microphones | [1] |
| Force and touch | six-axis F/T sensors in the upper arms and legs, plus 2 near the ankles; over 3000 capacitive tactile sensors | [1] |
| Joint sensing | 12-bit absolute magnetic encoders at the joints, incremental encoders at the motors | [1] |
| Power | 36 V 9 Ah battery listed as "not available yet": a dummy pack connects to a supply | [1] |
| Repeatability | palm 1 mm, foot 3 mm, static (maker's claim) | [1] |

## How it works

Electric motors drive every joint, with zero-backlash main joints and elastic actuators in the legs.
Each hand moves 19 joints with 9 motors; the ring and little fingers are coupled [1]. Encoders, an
IMU, the F/T sensors and the skin feed IIT's libraries for force and impedance control, reaching and
grasping. IIT says all source code, down to the microcontroller code, is on GitHub [1].

An onboard PC runs Ubuntu and YARP, IIT's library for communication and device interfaces [1][5].
icub-main holds the device drivers and the kinematics, dynamics, gaze, Cartesian control and skin
modules [4]; yarp-devices-ros2 gives ROS 2 access [6]. icub-models has URDF and SDF files for iCub
versions 1 to 2.7, some tuned for Gazebo Classic [7]. iCub itself has no MuJoCo model;
ergocub-software ships ergoCub URDFs and a script that builds a MuJoCo model [10].

| Variant | Height | Mass | DoF | Notes | Source |
|---|---|---|---|---|---|
| iCub 2.x | about 105 cm | 30 kg | 53 | sold by IIT, also as a head or upper body; versions v1.0 to v2.9 | [1][2][9] |
| iCub3 | 125 cm | 52 kg | 54 | battery in the torso, 18-bit joint encoders, 4K eye cameras, depth camera | [9] |
| ergoCub | — | — | — | larger successor; not in IIT's catalogue; models BSD-3-Clause | [2][10] |

## What it is used for

- Research on embodied cognition and development, RobotCub's aim; the project gave six iCubs to
  labs through an open call [3].
- Robot avatars: IIT's iCub3 system let an operator in Genoa visit an exhibition in Venice, about
  290 km away, and was built for the ANA Avatar XPrize [9].
- Force control, reaching and grasping with the libraries that ship with the robot [1][4].

## Cost and BOM

IIT's catalogue gives undated indicative prices: €250,000 for a full iCub, €200,000 for an upper body
and €40,000 for a head [2]. No USD price or date is stated, so `cost` stays empty. There is no BOM.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Robot software | C++ | [icub-main](https://github.com/robotology/icub-main) [4] | GPL-2.0-or-later (COPYING); some files BSD-3-Clause |
| Middleware and ROS 2 bridge | C++, bindings | [YARP](https://github.com/robotology/yarp) [5], [yarp-devices-ros2](https://github.com/robotology/yarp-devices-ros2) [6] | BSD-3-Clause; some optional YARP parts LGPL, GPL or Apache |
| Models | URDF, SDF | [icub-models](https://github.com/robotology/icub-models) [7]; [ergocub-software](https://github.com/icub-tech-iit/ergocub-software) [10] | CC-BY-SA-4.0; ergoCub BSD-3-Clause |
| CAD, a subset | PTC Creo 9 parts, assemblies, drawings | [cad-mechanics-public](https://github.com/mesh-iit/cad-mechanics-public) [8] | CERN-OHL-W-2.0 |

## Strengths and limits

- **Strengths:** 53 DoF, dexterous hands, F/T sensors and skin in one child-size body [1]; long-lived
  open software with models for ROS and Gazebo [4][6][7]; about 6000 CAD files public [8].
- **Limits:** about €250,000 [2]; the public CAD is a subset of IIT's private repo and needs PTC Creo
  and IIT's cad-libraries [8]; YARP is one more middleware to learn [5]; no MuJoCo model for iCub [7].

## Related robots

- [PAL TALOS](pal-talos.md): an adult-size torque-controlled research humanoid.
- [NAO](nao.md) and [ROBOTIS OP3](robotis-op3.md): smaller, cheaper humanoids for research and teaching.
- [Poppy Humanoid](poppy-humanoid.md): an open printed research humanoid from Inria.

## Sources

1. [IIT: Technical specifications of the iCub platform, Rev 2.5 (2019)](https://www.iit.it/documents/175012/528824/Technical-specs_iCub_robot_Rev_2.3_05082019+%282%29.pdf/56ccea3f-af0d-8ecf-f1f5-a387d2223a45), accessed 2026-11-18
2. [iCub product catalogue (IIT)](https://icub.iit.it/products/product-catalog), accessed 2026-11-18
3. [Metta et al. (2008): The iCub humanoid robot, an open platform for research in embodied cognition](https://www.robotcub.org/misc/papers/08_Metta_Sandini_Vernon_etal.pdf), accessed 2026-11-18
4. [icub-main repository](https://github.com/robotology/icub-main), accessed 2026-11-18
5. [YARP repository](https://github.com/robotology/yarp), accessed 2026-11-18
6. [yarp-devices-ros2 repository](https://github.com/robotology/yarp-devices-ros2), accessed 2026-11-18
7. [icub-models repository](https://github.com/robotology/icub-models), accessed 2026-11-18
8. [cad-mechanics-public (IIT public CAD subset)](https://github.com/mesh-iit/cad-mechanics-public), accessed 2026-11-18
9. [Dafarra et al.: iCub3 Avatar System](https://arxiv.org/abs/2203.06972), accessed 2026-11-18
10. [ergocub-software repository](https://github.com/icub-tech-iit/ergocub-software), accessed 2026-11-18
