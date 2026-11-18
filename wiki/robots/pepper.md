---
type: robot
name: Pepper
summary: SoftBank Robotics' 1.2 m wheeled humanoid with a chest tablet, a common human-robot interaction platform since 2014; production paused in 2021, Aldebaran's assets passed to Maxvision in 2025, Maxtronics does not support it, and ROS 2 support is community-maintained.
tags: [humanoid, wheeled, hri, service-robot, naoqi, ros2, aldebaran, softbank-robotics, tablet, discontinued]
category: social
tier: B
openness: software-only
maker: Aldebaran for SoftBank Robotics (assets sold to Maxvision in 2025)
year: 2014
license: {hardware: , software: Apache-2.0, docs: }
links: {repo: "https://github.com/ros-naoqi/naoqi_driver2", docs: "http://doc.aldebaran.com/2-5/family/pepper_technical/index_dev_pepper.html", cad: , paper: , site: "https://maxtronics.com/en/pepper"}
specs: {dof: 20, payload_kg: , reach_mm: , mass_kg: 28, size_mm: "1200 x 485 x 425", speed_mps: 0.83, runtime_h: 12}
stack: {actuators: "20 DC motors of six types (brushed coreless and brushless): 17 joints and 3 wheels", mcu: , compute: "Intel Atom E3845 quad-core 1.91 GHz, 4 GB DDR3 in the head; NAOqi OS", sensors: ["four microphones", "two RGB cameras", "3D depth sensor", "gyroscope", "touch sensors", "two sonars", "six lasers", "three bumpers"], sim_models: ["URDF/Xacro (ros-naoqi/pepper_robot pepper_description, ROS 1)", "URDF (robot_descriptions: pepper_description from jrl-umi3218)", "meshes (ros-naoqi/pepper_meshes2, CC-BY-NC-ND-4.0)"], ros2: community}
cost: {type: retail, usd: 32000, as_of: 2026-11-18, source: "https://www.robotlab.com/store/pepper-robot-for-research"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2026-06-22, stars: 21, active: true}
use_cases: [hri, research, education]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://en.wikipedia.org/wiki/Pepper_(robot)", title: "Wikipedia: Pepper (robot)", accessed: 2026-11-18}
  - {url: "https://www.pcworld.com/article/428175/1000-pepper-robots-sell-out-in-a-minute-on-launch-day.html", title: "PCWorld: 1000 Pepper robots sell out in a minute on launch day (2015-06-20)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/maxvision-buys-core-robot-assets-including-nao-pepper-aldebaran/", title: "The Robot Report: Maxvision buys core robot assets, including NAO and Pepper, from Aldebaran (2025-07-19)", accessed: 2026-11-18}
  - {url: "https://maxtronics.com/en/pepper", title: "Maxtronics: Pepper support page", accessed: 2026-11-18}
  - {url: "http://doc.aldebaran.com/2-5/family/pepper_technical/motors_pep.html", title: "Aldebaran Pepper developer guide: motors", accessed: 2026-11-18}
  - {url: "http://doc.aldebaran.com/2-5/family/pepper_technical/motherboard_pep.html", title: "Aldebaran Pepper developer guide: motherboard", accessed: 2026-11-18}
  - {url: "https://github.com/ros-naoqi/naoqi_driver2", title: naoqi_driver2 README and changelog, accessed: 2026-11-18}
  - {url: "https://github.com/ros-naoqi/pepper_robot", title: ros-naoqi pepper_robot repository, accessed: 2026-11-18}
  - {url: "https://github.com/robot-descriptions/robot_descriptions.py", title: robot_descriptions model list, accessed: 2026-11-18}
  - {url: "https://www.robotlab.com/store/pepper-robot-for-research", title: "RobotLAB: Softbank Pepper Robot", accessed: 2026-11-18}
---

# Pepper

A 1.2 m wheeled humanoid with a tablet on its chest, made by Aldebaran for SoftBank and shown in
June 2014; consumer sales began in Japan in June 2015 [1][2]. Builders meet it in human-robot
interaction studies and service pilots. **Discontinued:** production paused in June 2021 [1],
Maxvision bought Aldebaran's assets in 2025 [3], and Maxtronics neither sells nor supports
Pepper [4]. [NAO](nao.md) tells the same maker's story.

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Pepper 1.8 and 1.8A, the last versions; 1.6 and 1.7 came before | [4][5] |
| Degrees of freedom | 20 motors: head 2; per side 4 arm joints, wrist yaw and hand; hip roll, hip pitch, knee pitch; 3 wheels | [5] |
| Height, width, depth, mass | 1.20 m x 485 mm x 425 mm; 28 kg | [1] |
| Battery | Li-ion, 30.0 Ah, 795 Wh; about 12 h in shop use | [1] |
| Speed | up to 3 km/h (0.83 m/s); climbs steps up to 1.5 cm | [1] |
| Computer | Intel Atom E3845, 4 cores, 1.91 GHz, 4 GB DDR3; older units: Atom Z530, 1 GB (maker's figures) | [6] |
| Sensors | 4 microphones, 2 RGB cameras, 3D depth sensor, gyroscope, touch sensors, 2 sonars, 6 lasers, 3 bumpers | [1] |
| Display, network | 10.1 in touch tablet; Wi-Fi a/b/g/n and Ethernet | [1] |
| Software | NAOqi OS. NAOqi 2.5 (Python, Choregraphe) on every version; 2.9 (Android SDK) only on 1.8 and 1.8A | [4] |

## How it works

Brushed coreless and brushless DC motors of six types drive 17 joints and 3 wheels, with stall
torques from 14.7 mNm at the wrist and hand to 1.46 N·m at the hip and knee; a hip and knee chain
stands in for legs [5]. The head computer runs NAOqi: Choregraphe and the Python SDK on 2.5, the
Android SDK on 2.9 [4]. Maxtronics warns against changing the NAOqi version yourself, and said
Pepper's cloud services and the Aldebaran app store would end on 2026-10-01 [4].

ROS 2 support comes from the ros-naoqi project: naoqi_driver2 bridges NAOqi to ROS 2 through
libqi, has setup notes for NAOqi 2.8 and lower and for 2.9 and higher, and release 2.1.2
(2026-06-22) added Jazzy fixes [7]. Its LICENSE file is Apache-2.0, while package.xml says BSD [7].
The Pepper URDF and xacro files live in pepper_robot, a ROS 1 catkin package last changed on
2023-10-13 [8]; the meshes are CC BY-NC-ND 4.0 and must be accepted at build time [7].
robot_descriptions loads a separate Pepper URDF from jrl-umi3218 [9]. No MJCF model was found.

## What it is used for

- **HRI research and teaching:** offered to schools and universities for programming and
  human-robot interaction work; CARESSES, an eldercare research project, started in 2017 [1].
- **Customer service:** receptionist in UK offices, in banks and clinics in Japan, in phone shops
  and restaurants, and as a greeter at North American airports [1].

## Cost and BOM

| Item | Price | Type | Date | Source |
|---|---|---|---|---|
| Pepper at RobotLAB: robot, charger, 2 batteries, English speech; lease offered; new or refurbished not stated | from USD 32,000 | retail | 2026-11-18 | [10] |
| Consumer launch in Japan, first 1,000 units | JPY 198,000 plus JPY 24,600 a month for data and insurance | retail | 2015-06-20 | [2] |

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Hardware, NAOqi OS | — | Not published | Proprietary |
| ROS 2 driver | ROS 2 package | [naoqi_driver2](https://github.com/ros-naoqi/naoqi_driver2) [7] | Apache-2.0 (package.xml says BSD) |
| Descriptions | URDF/Xacro | [pepper_robot](https://github.com/ros-naoqi/pepper_robot) (ROS 1) [8]; jrl-umi3218/pepper_description via robot_descriptions [9] | Apache-2.0; BSD-2-Clause |
| Meshes | mesh files | [pepper_meshes2](https://github.com/ros-naoqi/pepper_meshes2) [7] | CC BY-NC-ND 4.0: non-commercial, no derivatives |

## Strengths and limits

- **Strengths:** a complete, approachable interaction robot: human height, tablet, cameras, depth
  sensor, four microphones, all-day battery [1]; about 27,000 built, so studies compare well [1];
  a ROS 2 driver updated in 2026 [7].
- **Limits:** out of production since 2021 and unsupported by the current owner, whose cloud
  services were set to end in October 2026 [1][4]; USD 32,000 at RobotLAB [10]; no stated payload;
  a ROS 1 description and non-commercial meshes [7][8].

## Related robots

- [NAO](nao.md): Aldebaran's small walking humanoid, on the same NAOqi software.
- [TIAGo](tiago.md) and [Reachy](reachy.md): service and interaction robots with open ROS 2 stacks.
- [Jibo](jibo.md) and [Vector](anki-vector.md): consumer social robots that outlived their makers.

## Sources

1. [Wikipedia: Pepper (robot)](https://en.wikipedia.org/wiki/Pepper_(robot)), accessed 2026-11-18
2. [PCWorld: 1000 Pepper robots sell out in a minute on launch day (2015-06-20)](https://www.pcworld.com/article/428175/1000-pepper-robots-sell-out-in-a-minute-on-launch-day.html), accessed 2026-11-18
3. [The Robot Report: Maxvision buys core robot assets, including NAO and Pepper, from Aldebaran (2025-07-19)](https://www.therobotreport.com/maxvision-buys-core-robot-assets-including-nao-pepper-aldebaran/), accessed 2026-11-18
4. [Maxtronics: Pepper support page](https://maxtronics.com/en/pepper), accessed 2026-11-18
5. [Aldebaran Pepper developer guide: motors](http://doc.aldebaran.com/2-5/family/pepper_technical/motors_pep.html), accessed 2026-11-18
6. [Aldebaran Pepper developer guide: motherboard](http://doc.aldebaran.com/2-5/family/pepper_technical/motherboard_pep.html), accessed 2026-11-18
7. [naoqi_driver2 README and changelog](https://github.com/ros-naoqi/naoqi_driver2), accessed 2026-11-18
8. [ros-naoqi pepper_robot repository](https://github.com/ros-naoqi/pepper_robot), accessed 2026-11-18
9. [robot_descriptions model list](https://github.com/robot-descriptions/robot_descriptions.py), accessed 2026-11-18
10. [RobotLAB: Softbank Pepper Robot](https://www.robotlab.com/store/pepper-robot-for-research), accessed 2026-11-18
