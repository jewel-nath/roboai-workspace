---
type: robot
name: NAO
summary: Aldebaran's 58 cm, 25-DoF humanoid (NAO V6 since 2018), for years the RoboCup Standard Platform League robot and a common education and HRI platform; Aldebaran's assets passed to Maxvision (Maxtronics) in 2025, resellers still list NAO V6, and ROS 2 support is community-maintained.
tags: [humanoid, small-humanoid, robocup, spl, education, hri, naoqi, ros2, aldebaran, softbank-robotics]
category: humanoid
tier: B
openness: software-only
maker: Aldebaran (SoftBank Robotics 2015–2022; Maxtronics since 2025)
year: 2008
license: {hardware: , software: Apache-2.0, docs: }
links: {repo: "https://github.com/ros-naoqi/naoqi_driver2", docs: "http://doc.aldebaran.com/2-8/family/nao_technical/index_dev_naov6.html", cad: , paper: , site: "https://maxtronics.com/en/nao"}
specs: {dof: 25, payload_kg: , reach_mm: , mass_kg: 5.48, size_mm: , speed_mps: , runtime_h: 1.5}
stack: {actuators: "DC motors with reduction gears (five motor types)", mcu: , compute: "Intel Atom E3845 quad-core 1.91 GHz, 4 GB DDR3, 32 GB eMMC; NAOqi OS (Gentoo-based Linux)", sensors: ["two 5 MP cameras", "four microphones", "sonar", "IMU (gyroscope and accelerometer)", "force sensors in each foot", "tactile sensors on head, hands and feet"], sim_models: ["URDF/Xacro (ros-naoqi/nao_robot nao_description, ROS 1)", "meshes (ros-naoqi/nao_meshes2, CC-BY-NC-ND-4.0)"], ros2: community}
cost: {type: retail, usd: 16990, as_of: 2026-11-18, source: "https://www.robotlab.com/store/nao-v6-standard-edition/"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-06-22, stars: 21, active: true}
use_cases: [education, research, competition]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://www.robotlab.com/store/nao-v6-standard-edition/", title: "RobotLAB: NAO V6 Standard Edition", accessed: 2026-11-18}
  - {url: "http://doc.aldebaran.com/2-8/family/nao_technical/motors_naov6.html", title: "Aldebaran NAO V6 developer guide: motors", accessed: 2026-11-18}
  - {url: "https://en.wikipedia.org/wiki/Nao_(robot)", title: "Wikipedia: Nao (robot)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/maxvision-buys-core-robot-assets-including-nao-pepper-aldebaran/", title: "The Robot Report: Maxvision buys core robot assets, including NAO and Pepper, from Aldebaran (2025-07-19)", accessed: 2026-11-18}
  - {url: "https://maxtronics.com/en/nao", title: "Maxtronics: NAO6 support center", accessed: 2026-11-18}
  - {url: "https://github.com/ros-naoqi/naoqi_driver2", title: naoqi_driver2 README and changelog, accessed: 2026-11-18}
  - {url: "https://github.com/ros-sports/nao_lola", title: nao_lola README, accessed: 2026-11-18}
  - {url: "https://github.com/ros-naoqi/nao_robot", title: ros-naoqi nao_robot repository, accessed: 2026-11-18}
  - {url: "https://lists.robocup.org/archives/list/robocup-nao@lists.robocup.org/thread/UKXU72T3LDRS256SOYCASVTVHTGWBNSC/", title: "RoboCup-nao mailing list: Newsletter 1, new RoboCup soccer league (2025-10-07)", accessed: 2026-11-18}
  - {url: "https://spl.robocup.org/?p=3962", title: "RoboCup SPL: Robot Pricing 2024", accessed: 2026-11-18}
---

# NAO

A 58 cm humanoid first made by Aldebaran in France. It replaced Sony's AIBO in the RoboCup Standard
Platform League in 2007 [3], and Aldebaran reported about 20,000 sold [4]. Aldebaran entered
receivership in June 2025 and Maxvision bought its core assets in July 2025 [4]; its French arm
Maxtronics runs the NAO6 support site [3][5], and resellers such as RobotLAB still list NAO V6 [1].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | NAO V6 (NAO6, 2018), the current version | [1][3] |
| Degrees of freedom | 25 (the maker's figure); RobotLAB's tech-sheet breakdown counts 26 | [1] |
| Height, mass | 574 mm; 5.48 kg (RobotLAB's comparison table says 5.6 kg) | [1] |
| Battery | lithium-ion, 21.6 V, 2.9 Ah (62.5 Wh); about 60 min of active use, 90 min of normal use | [1] |
| Computer, OS | Intel Atom E3845, quad core, 1.91 GHz; 4 GB DDR3; 32 GB eMMC; NAOqi OS, a Gentoo-based Linux | [1] |
| Motors | five DC motor types with reduction gears; stall torque 9.4 to 65 mNm | [2] |
| Sensors | two 5 MP cameras, four microphones, sonar, IMU, foot force sensors, tactile sensors on head, hands and feet | [1] |

## How it works

NAOqi OS runs on the robot, and users program it with Choregraphe or the SDK, both included [1].
Maxtronics' site links a "NAO7 project" but gives no details [5].

ROS 2 support comes from the ros-naoqi project, not the current maker; its naoqi_driver2 bridges
NAOqi to ROS 2 through libqi, lists SoftBank Robotics staff among its maintainers, and its release
2.1.2 (2026-06-22) added Jazzy fixes [6]. Its LICENSE file is Apache-2.0 but package.xml says BSD [6].
RoboCup teams use nao_lola, ROS 2 packages for NAO's RoboCup-specific Lola layer, built for Humble,
Iron and Rolling [7]. The URDF is in nao_robot's nao_description (BSD, ROS 1, last commit 2018) [8];
the meshes are CC BY-NC-ND 4.0, accepted at build time [6].

| Version | Year | Changes | Source |
|---|---|---|---|
| NAO V3+ | 2008 | first production version, released to RoboCup teams | [3] |
| NAO Next Gen (V4) | 2011 | better cameras and robustness, anti-collision, faster walking | [3] |
| NAO Evolution (V5) | 2014 | stronger metal joints, better grip, four directional microphones | [3] |
| NAO6 (V6) | 2018 | current version; Atom E3845 and 4 GB RAM | [1][3] |

## What it is used for

- RoboCup soccer: the SPL robot since 2008 [3]. From RoboCup 2026 the SPL and Humanoid League merge;
  NAO V5 and V6 stay eligible next to Booster T1 and K1, Unitree G1 and H1 and others [9].
- Education: RobotLAB sells NAO with a curriculum and Choregraphe licence [1].

## Cost and BOM

| Item | Price (USD) | Type | Date | Source |
|---|---|---|---|---|
| NAO V6 Standard Edition: robot, charger, battery, Choregraphe, SDK, curriculum, 1-year warranty | 16,990 (starting at) | retail | 2026-11-18 | [1] |
| NAO V6 for RoboCup teams, North and Latin America; 2-year warranty, no shipping or tax | 7,970 | retail | 2024 | [10] |

RobotLAB also offers leasing [1]; the 2024 RoboCup price for Europe, Asia-Pacific and Japan was €5,784 [10].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Hardware, NAOqi OS | — | Not published | Proprietary |
| ROS 2 driver | ROS 2 package | [naoqi_driver2](https://github.com/ros-naoqi/naoqi_driver2) [6] | Apache-2.0 (package.xml says BSD) |
| RoboCup low-level ROS 2 interface | ROS 2 packages | [nao_lola](https://github.com/ros-sports/nao_lola) [7] | Apache-2.0 |
| Description | URDF/Xacro, ROS 1 | [nao_robot](https://github.com/ros-naoqi/nao_robot) [8] | BSD |
| Meshes | mesh files | [nao_meshes2](https://github.com/ros-naoqi/nao_meshes2) [6] | CC BY-NC-ND 4.0: non-commercial, no derivatives |

## Strengths and limits

- **Strengths:** a small, complete humanoid with cameras, microphones, speech and touch sensors [1];
  a large RoboCup and classroom base, about 20,000 sold [4]; a ROS 2 driver updated in 2026 [6].
- **Limits:** the maker went through receivership in 2025 [4]; about 60 min of active battery [1];
  $16,990 for a 5.5 kg robot [1]; community ROS 2 support and non-commercial meshes [6].

## Related robots

- [ROBOTIS OP3](robotis-op3.md) and [Poppy Humanoid](poppy-humanoid.md): other small humanoids.
- [Booster T1](booster-t1.md) and [Unitree G1](unitree-g1.md): eligible in the merged RoboCup league [9].

## Sources

1. [RobotLAB: NAO V6 Standard Edition](https://www.robotlab.com/store/nao-v6-standard-edition/), accessed 2026-11-18
2. [Aldebaran NAO V6 developer guide: motors](http://doc.aldebaran.com/2-8/family/nao_technical/motors_naov6.html), accessed 2026-11-18
3. [Wikipedia: Nao (robot)](https://en.wikipedia.org/wiki/Nao_(robot)), accessed 2026-11-18
4. [The Robot Report: Maxvision buys core robot assets, including NAO and Pepper, from Aldebaran (2025-07-19)](https://www.therobotreport.com/maxvision-buys-core-robot-assets-including-nao-pepper-aldebaran/), accessed 2026-11-18
5. [Maxtronics: NAO6 support center](https://maxtronics.com/en/nao), accessed 2026-11-18
6. [naoqi_driver2 README and changelog](https://github.com/ros-naoqi/naoqi_driver2), accessed 2026-11-18
7. [nao_lola README](https://github.com/ros-sports/nao_lola), accessed 2026-11-18
8. [ros-naoqi nao_robot repository](https://github.com/ros-naoqi/nao_robot), accessed 2026-11-18
9. [RoboCup-nao mailing list: Newsletter 1, new RoboCup soccer league (2025-10-07)](https://lists.robocup.org/archives/list/robocup-nao@lists.robocup.org/thread/UKXU72T3LDRS256SOYCASVTVHTGWBNSC/), accessed 2026-11-18
10. [RoboCup SPL: Robot Pricing 2024](https://spl.robocup.org/?p=3962), accessed 2026-11-18
