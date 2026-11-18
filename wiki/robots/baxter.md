---
type: robot
name: Baxter
summary: Rethink Robotics' two-armed collaborative robot (2012, $22,000) with series elastic actuators and a face screen; a long-running ROS 1 research platform, discontinued since Rethink closed in 2018, with BSD-licensed SDK, URDF and Gazebo models.
tags: [cobot, dual-arm, series-elastic-actuator, ros1, rethink-robotics, discontinued, gazebo]
category: arm
tier: B
openness: software-only
maker: Rethink Robotics
year: 2012
license: {hardware: , software: BSD-3-Clause, docs: }
links: {repo: "https://github.com/RethinkRobotics/baxter_common", docs: "https://web.archive.org/web/20230610211612/https://sdk.rethinkrobotics.com/wiki/Main_Page", cad: , paper: , site: }
specs: {dof: 15, payload_kg: 2.2, reach_mm: 1210, mass_kg: 75, size_mm: , speed_mps: , runtime_h: }
stack: {actuators: "series elastic actuators with brushless DC motors, 7 per arm", mcu: "ARM-based motor controller boards in the arms", compute: "Intel Core i7-3770 PC in the torso, 4 GB RAM, 128 GB SSD", sensors: ["head camera", "camera in each hand", "IR range sensor in each hand", "sonar ring in the head", "14-bit joint position sensors", "joint torque from spring deflection"], sim_models: ["URDF (RethinkRobotics/baxter_common)", "Gazebo (RethinkRobotics/baxter_simulator, ROS 1)", "URDF, ROS 2 port (CentraleNantesRobotics/baxter_common_ros2)", "MJCF (robosuite Baxter)"], ros2: community}
cost: {type: retail, usd: 22000, as_of: 2012-09-18, source: "https://spectrum.ieee.org/rethink-robotics-baxter-robot-factory-worker"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2015-12-30, stars: 60, active: false}
use_cases: [research, manipulation, education, data-collection]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://spectrum.ieee.org/rethink-robotics-baxter-robot-factory-worker", title: "IEEE Spectrum: How Rethink Robotics Built Its New Baxter Robot Worker (2012-09-18)", accessed: 2026-11-18}
  - {url: "https://spectrum.ieee.org/rethink-robotics-baxter-research-robot", title: "IEEE Spectrum: Rethink Robotics Opens Up Baxter Robot for Researchers (2013-05-06)", accessed: 2026-11-18}
  - {url: "https://web.archive.org/web/20181219111522/https://www.rethinkrobotics.com/baxter/tech-specs/", title: "Rethink Robotics: Baxter tech specs (archived 2018-12-19)", accessed: 2026-11-18}
  - {url: "https://web.archive.org/web/20221126215159/https://sdk.rethinkrobotics.com/wiki/Hardware_Specifications", title: "Baxter SDK wiki: Hardware Specifications (archived 2022-11-26)", accessed: 2026-11-18}
  - {url: "https://robotsguide.com/robots/baxter", title: "IEEE Robots guide: Baxter", accessed: 2026-11-18}
  - {url: "https://spectrum.ieee.org/rethink-robotics-pioneer-of-collaborative-robots-shuts-down", title: "IEEE Spectrum: Rethink Robotics, Pioneer of Collaborative Robots, Shuts Down (2018-10-04)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/rethink-robotics-cobots-get-continuing-support/", title: "The Robot Report: Rethink Robotics cobots get continuing support (2018-10-25)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/rethink-robotics-shuts-down-again/", title: "The Robot Report: Rethink Robotics shuts down, again (2025-09-16)", accessed: 2026-11-18}
  - {url: "https://github.com/RethinkRobotics/baxter_common", title: RethinkRobotics baxter_common repository, accessed: 2026-11-18}
  - {url: "https://github.com/RethinkRobotics/baxter", title: RethinkRobotics Baxter SDK repository and changelog, accessed: 2026-11-18}
  - {url: "https://github.com/RethinkRobotics/baxter_simulator", title: RethinkRobotics baxter_simulator repository, accessed: 2026-11-18}
  - {url: "https://github.com/CentraleNantesRobotics/baxter_common_ros2", title: CentraleNantesRobotics baxter_common_ros2 README, accessed: 2026-11-18}
  - {url: "https://discourse.openrobotics.org/t/using-baxter-after-2025/25272", title: "ROS Discourse: Using Baxter after 2025", accessed: 2026-11-18}
  - {url: "https://robosuite.ai/docs/modules/robots.html", title: robosuite robots and grippers, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/1509.06825", title: "Supersizing Self-supervision: Learning to Grasp from 50K Tries and 700 Robot Hours", accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/1910.11215", title: "RoboNet: Large-Scale Multi-Robot Learning", accessed: 2026-11-18}
  - {url: "https://web.archive.org/web/20260315180906/https://rethinkrobotics.com/", title: "rethinkrobotics.com (archived 2026-03-15, parked domain)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/rethink-robotics-relaunches-with-cobots-amrs-mobile-manipulation/", title: "The Robot Report: Rethink Robotics relaunches with cobots, AMRs, mobile manipulation (2024-09-09)", accessed: 2026-11-18}
---

# Baxter

A two-armed collaborative robot with a screen for a face, launched by Rethink Robotics (Boston)
in September 2012 at $22,000 [1]. Its series elastic actuators let it work next to people, and a
research edition with an open ROS SDK followed in 2013, so it became a common university platform
[2]. Builders now meet it in older papers, datasets and simulators.

**Status: discontinued.** Rethink closed on 3 October 2018 after sales fell short and a buyer
backed out [6]. HAHN Group bought its patents, trademarks and Intera software on 25 October 2018
and promised continuing support for Sawyer; the report names no such plan for Baxter [7]. Under
HAHN's United Robotics Group, Rethink relaunched in September 2024 with new products and shut
down again in 2025; the fate of its IP has not been announced [8][18]. The rethinkrobotics.com
domain is parked, and its SDK and support hosts no longer resolve (checked 2026-11-18) [17].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Baxter (the research and manufacturing editions share the hardware) | [2] |
| Degrees of freedom | 15 counted: 2 arms x 7 joints and a head pan joint; the head can also nod; grippers are swappable end effectors (electric, pneumatic or none) and not counted | [3][5][9] |
| Reach | 1210 mm maximum (maker's claim) | [3] |
| Payload | 2.2 kg per arm, including the end effector (maker's claim) | [3][4] |
| Positional accuracy | ±5 mm (maker's claim) | [4] |
| Joint speed | 2.0 rad/s at shoulder and elbow, 4.0 rad/s at the wrist | [4] |
| Peak joint torque | 50 N·m shoulder and elbow, 15 N·m wrist | [4] |
| Joint sensors | 14-bit position; about ±0.10° typical accuracy | [4] |
| Mass | 75 kg without pedestal; one arm 21.3 kg, torso 31.8 kg, pedestal 60.8 kg | [1][4] |
| Height | 3 ft 1 in without pedestal; 5 ft 10 in to 6 ft 3 in on the adjustable pedestal | [3] |
| Cameras | 1280 x 800 maximum, 30 fps; in the head and each hand | [3][9] |
| Computer | Intel Core i7-3770, 4 GB RAM, 128 GB SSD | [3][4] |
| Gripping force | 35 N maximum (maker's claim) | [4] |
| Power | 120 V AC, 6 A; internal supplies accept 90 to 264 V AC | [3][4] |

The tech-spec page gives 306 lb with the pedestal, while the SDK wiki gives 135.2 kg (298 lb) [3][4].

## How it works

Each arm has seven joints driven by series elastic actuators: a brushless motor and gearbox turn
a spring, which turns the joint, so the spring's deflection measures joint torque and softens
impacts [1][5]. The joints are compliant by design: the large flexures deflect 3.4° at 50 N·m
[4]. A PC in the torso runs Linux and ROS; ARM-based boards in the arms run the motors [1][5]. A
sonar ring in the head senses people moving close by, and IR range sensors in the hands read
distances from 4 to 40 cm [3][5][9].

Users taught tasks by moving the arms by hand, and the face screen doubled as the interface [1].
The research edition dropped the factory software for an SDK whose ROS layer is open source,
while the core system stayed proprietary [2]. The SDK is Python on ROS 1; its last release, 1.2.0,
came in December 2015 and targets ROS Indigo [10]. The `kinetic-devel` branches of the
description and simulator last changed in June 2018 [9][11].

There is no official ROS 2 support. Centrale Nantes ported the messages and description to ROS 2
and ships a prebuilt ROS 1 to ROS 2 bridge that lets several students share one robot; its last
commit was 2026-09-23 [12]. The robot itself still speaks ROS 1, so labs keep a minimal ROS 1
install or run the SDK in Docker [13].

Models: the URDF and meshes in `baxter_common`, the Gazebo simulator in `baxter_simulator`, both
BSD-3-Clause and ROS 1, and a Baxter with Rethink grippers in robosuite [9][11][14]. MuJoCo
Menagerie has no Baxter model.

## What it is used for

- University research: Rethink sold the research edition from 2013 at the same base price [2].
- Self-supervised grasping: Pinto and Gupta collected 50,000 grasp attempts over 700 robot hours
  on a Baxter [15].
- Multi-robot datasets: RoboNet includes Baxter data alongside Sawyer, Franka, Kuka and WidowX
  arms [16].
- Teaching: Centrale Nantes has run ROS 2 labs on Baxter through its bridge since 2020 [13].

## Cost and BOM

| Item | Price (USD) | Type | Date | Source |
|---|---|---|---|---|
| Baxter at launch, with a year of software updates and warranty | 22,000 | retail | 2012-09-18 | [1] |
| Baxter Research Robot base price | 22,000 | retail | 2013-05-06 | [2] |

No new units are sold. After the 2018 closure, Hunan CoThink, Rethink's former Baxter maker and
distributor in China, said it held about 100 robots and had rights to make more [7]. Used units
are the only route; no current listing was checked.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Hardware design | — | Not published | Proprietary |
| SDK (interface, tools, examples) | Python, ROS 1 | [RethinkRobotics/baxter](https://github.com/RethinkRobotics/baxter) and linked repos | BSD-3-Clause |
| Description and messages | URDF, meshes, ROS 1 msgs | [RethinkRobotics/baxter_common](https://github.com/RethinkRobotics/baxter_common) | BSD-3-Clause |
| Simulator | Gazebo, ROS 1 | [RethinkRobotics/baxter_simulator](https://github.com/RethinkRobotics/baxter_simulator) | BSD-3-Clause |
| ROS 2 port and bridge | ROS 2 packages | [CentraleNantesRobotics/baxter_common_ros2](https://github.com/CentraleNantesRobotics/baxter_common_ros2) | BSD-3-Clause (Rethink's notice) |
| Robot core software | — | On the robot | Proprietary [2] |
| Docs | Wiki | [SDK wiki, archived](https://web.archive.org/web/20230610211612/https://sdk.rethinkrobotics.com/wiki/Main_Page) | All rights reserved |

## Strengths and limits

- **Strengths:** two 7-DoF arms with joint torque sensing at a 2012 price of $22,000 [1]; safe,
  compliant joints [1][4]; open SDK, URDF and Gazebo models [9][10][11]; many past papers and
  datasets [15][16].
- **Limits:** discontinued with no maker support, and the SDK wiki host no longer resolves
  (checked 2026-11-18) [17]; ROS 1 software last released in 2015 [10]; ±5 mm accuracy and
  2.2 kg payload [4]; the springy actuators hurt precision and repeatability [8]; heavy, at
  75 kg plus pedestal [1][4].

## What to reuse

- Series elastic actuation: a spring between gearbox and joint gives torque sensing and safer
  contact without a separate torque sensor [1].
- A face screen as the robot's status display and user interface [1].

## Related robots

- [Sawyer](sawyer.md): Rethink's one-armed successor from 2015 [6].
- [Universal Robots](universal-robots.md): IEEE Spectrum names it as the rival that came to
  dominate the cobot market Rethink opened [6].
- [Franka Panda](franka-panda.md) and [KUKA LBR iiwa](kuka-lbr-iiwa.md): share the RoboNet
  dataset with Baxter [16].

## Sources

1. [IEEE Spectrum: How Rethink Robotics Built Its New Baxter Robot Worker (2012-09-18)](https://spectrum.ieee.org/rethink-robotics-baxter-robot-factory-worker), accessed 2026-11-18
2. [IEEE Spectrum: Rethink Robotics Opens Up Baxter Robot for Researchers (2013-05-06)](https://spectrum.ieee.org/rethink-robotics-baxter-research-robot), accessed 2026-11-18
3. [Rethink Robotics: Baxter tech specs (archived 2018-12-19)](https://web.archive.org/web/20181219111522/https://www.rethinkrobotics.com/baxter/tech-specs/), accessed 2026-11-18
4. [Baxter SDK wiki: Hardware Specifications (archived 2022-11-26)](https://web.archive.org/web/20221126215159/https://sdk.rethinkrobotics.com/wiki/Hardware_Specifications), accessed 2026-11-18
5. [IEEE Robots guide: Baxter](https://robotsguide.com/robots/baxter), accessed 2026-11-18
6. [IEEE Spectrum: Rethink Robotics, Pioneer of Collaborative Robots, Shuts Down (2018-10-04)](https://spectrum.ieee.org/rethink-robotics-pioneer-of-collaborative-robots-shuts-down), accessed 2026-11-18
7. [The Robot Report: Rethink Robotics cobots get continuing support (2018-10-25)](https://www.therobotreport.com/rethink-robotics-cobots-get-continuing-support/), accessed 2026-11-18
8. [The Robot Report: Rethink Robotics shuts down, again (2025-09-16)](https://www.therobotreport.com/rethink-robotics-shuts-down-again/), accessed 2026-11-18
9. [RethinkRobotics baxter_common repository](https://github.com/RethinkRobotics/baxter_common), accessed 2026-11-18
10. [RethinkRobotics Baxter SDK repository and changelog](https://github.com/RethinkRobotics/baxter), accessed 2026-11-18
11. [RethinkRobotics baxter_simulator repository](https://github.com/RethinkRobotics/baxter_simulator), accessed 2026-11-18
12. [CentraleNantesRobotics baxter_common_ros2 README](https://github.com/CentraleNantesRobotics/baxter_common_ros2), accessed 2026-11-18
13. [ROS Discourse: Using Baxter after 2025](https://discourse.openrobotics.org/t/using-baxter-after-2025/25272), accessed 2026-11-18
14. [robosuite robots and grippers](https://robosuite.ai/docs/modules/robots.html), accessed 2026-11-18
15. [Supersizing Self-supervision: Learning to Grasp from 50K Tries and 700 Robot Hours](https://arxiv.org/abs/1509.06825), accessed 2026-11-18
16. [RoboNet: Large-Scale Multi-Robot Learning](https://arxiv.org/abs/1910.11215), accessed 2026-11-18
17. [rethinkrobotics.com (archived 2026-03-15, parked domain)](https://web.archive.org/web/20260315180906/https://rethinkrobotics.com/), accessed 2026-11-18
18. [The Robot Report: Rethink Robotics relaunches with cobots, AMRs, mobile manipulation (2024-09-09)](https://www.therobotreport.com/rethink-robotics-relaunches-with-cobots-amrs-mobile-manipulation/), accessed 2026-11-18
