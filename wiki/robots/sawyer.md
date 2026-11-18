---
type: robot
name: Sawyer
summary: Rethink Robotics' single-arm 7-DoF collaborative robot (2015, $29,000) with series elastic actuators; discontinued, but still the simulated arm in Meta-World and a stock robot in robosuite and MuJoCo Menagerie.
tags: [cobot, 7-dof, series-elastic-actuator, intera, ros1, rethink-robotics, discontinued, meta-world, robosuite]
category: arm
tier: B
openness: software-only
maker: Rethink Robotics
year: 2015
license: {hardware: , software: Apache-2.0, docs: }
links: {repo: "https://github.com/RethinkRobotics/intera_sdk", docs: "https://rethinkrobotics.github.io/intera_sdk_docs/", cad: , paper: , site: }
specs: {dof: 8, payload_kg: 4, reach_mm: 1260, mass_kg: 19, size_mm: , speed_mps: 1.5, runtime_h: }
stack: {actuators: "series elastic actuators, 7 arm joints", mcu: , compute: "separate robot controller with I/O and fieldbus ports", sensors: ["head camera", "Cognex wrist camera with built-in light", "torque sensing in every joint"], sim_models: ["URDF (RethinkRobotics/sawyer_robot sawyer_description)", "Gazebo (RethinkRobotics/sawyer_simulator, ROS 1 Noetic)", "MJCF (MuJoCo Menagerie, rethink_robotics_sawyer)", "MJCF (robosuite Sawyer)", "MJCF (Meta-World Sawyer)"], ros2: none}
cost: {type: retail, usd: 29000, as_of: 2015-03-19, source: "https://www.roboticstomorrow.com/news/2015/03/19/automate-2015--rethink-robotics-unveils-its-newest-smart-collaborative-robot-/5757/"}
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2021-08-09, stars: 44, active: false}
use_cases: [research, manipulation, reinforcement-learning, data-collection]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://www.roboticstomorrow.com/news/2015/03/19/automate-2015--rethink-robotics-unveils-its-newest-smart-collaborative-robot-/5757/", title: "Robotics Tomorrow: Rethink Robotics unveils its newest smart, collaborative robot (2015-03-19)", accessed: 2026-11-18}
  - {url: "https://web.archive.org/web/20190307192142/https://www.rethinkrobotics.com/sawyer/tech-specs/", title: "Rethink Robotics: Sawyer tech specs (archived 2019-03-07)", accessed: 2026-11-18}
  - {url: "https://web.archive.org/web/20240614185427/https://www.rethinkrobotics.com/sawyer/", title: "Rethink Robotics: Sawyer BLACK Edition page (archived 2024-06-14)", accessed: 2026-11-18}
  - {url: "https://robotsguide.com/robots/sawyer", title: "IEEE Robots guide: Sawyer", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/sawyer-black-edition-debut-rethink-robotics-new-ceo/", title: "The Robot Report: Sawyer BLACK Edition debuts (2019-10-16)", accessed: 2026-11-18}
  - {url: "https://spectrum.ieee.org/rethink-robotics-pioneer-of-collaborative-robots-shuts-down", title: "IEEE Spectrum: Rethink Robotics, Pioneer of Collaborative Robots, Shuts Down (2018-10-04)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/rethink-robotics-cobots-get-continuing-support/", title: "The Robot Report: Rethink Robotics cobots get continuing support (2018-10-25)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/rethink-robotics-relaunches-with-cobots-amrs-mobile-manipulation/", title: "The Robot Report: Rethink Robotics relaunches with cobots, AMRs, mobile manipulation (2024-09-09)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/rethink-robotics-shuts-down-again/", title: "The Robot Report: Rethink Robotics shuts down, again (2025-09-16)", accessed: 2026-11-18}
  - {url: "https://github.com/RethinkRobotics/intera_sdk", title: RethinkRobotics Intera SDK repository and changelog, accessed: 2026-11-18}
  - {url: "https://github.com/RethinkRobotics/intera_sdk/issues/160", title: "Intera SDK issue 160: Support for ROS2?", accessed: 2026-11-18}
  - {url: "https://github.com/RethinkRobotics/sawyer_robot", title: RethinkRobotics sawyer_robot repository, accessed: 2026-11-18}
  - {url: "https://github.com/RethinkRobotics/sawyer_simulator", title: RethinkRobotics sawyer_simulator repository, accessed: 2026-11-18}
  - {url: "https://github.com/google-deepmind/mujoco_menagerie/tree/main/rethink_robotics_sawyer", title: MuJoCo Menagerie rethink_robotics_sawyer, accessed: 2026-11-18}
  - {url: "https://robosuite.ai/docs/modules/robots.html", title: robosuite robots and grippers, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/1910.10897", title: "Meta-World: A Benchmark and Evaluation for Multi-Task and Meta Reinforcement Learning", accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/1910.11215", title: "RoboNet: Large-Scale Multi-Robot Learning", accessed: 2026-11-18}
  - {url: "https://web.archive.org/web/20260315180906/https://rethinkrobotics.com/", title: "rethinkrobotics.com (archived 2026-03-15, parked domain)", accessed: 2026-11-18}
  - {url: "https://github.com/RethinkRobotics/intera_common", title: RethinkRobotics intera_common repository, accessed: 2026-11-18}
---

# Sawyer

A single-arm, seven-joint collaborative robot with a screen for a face, launched by Rethink
Robotics in March 2015 at a $29,000 base price as a smaller, more precise follow-up to Baxter
[1][6]. Few builders will buy one now, but many will simulate it: Meta-World runs all 50 tasks on a
simulated Sawyer, and robosuite and MuJoCo Menagerie ship models [14][15][16].

**Status: discontinued.** Rethink closed in October 2018; HAHN Group bought its patents,
trademarks and Intera software and promised continuing Sawyer support [6][7]. Its Rethink
Robotics GmbH released the Sawyer BLACK Edition in 2019 [5]. Under HAHN's United Robotics Group,
Rethink relaunched in the US in September 2024 with new arms and mobile robots, then shut down in
2025 when the group's investors withdrew; the fate of the IP has not been announced [8][9]. The
rethinkrobotics.com domain is parked, and the SDK and support hosts no longer resolve (checked
2026-11-18) [18].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Sawyer (2015); the BLACK Edition keeps the reach, payload and joints | [1][5] |
| Degrees of freedom | 8 counted: 7 arm joints and a head pan joint; grippers are add-ons and not counted | [1][12] |
| Reach | 1260 mm maximum; 900 mm when gantry-mounted (maker's claim) | [2] |
| Payload | 4 kg (maker's claim) | [1][2] |
| Repeatability | ±0.1 mm (maker's claim) | [2] |
| Typical tool speed | 1.5 m/s (maker's claim) | [2] |
| Joint ranges | J0 to J3 350°, J4 and J5 340°, J6 540° | [2] |
| Mass | 19 kg | [1] |
| Vision | Camera in the head; Cognex camera with built-in light in the wrist | [1][3] |
| Force sensing | Torque sensing in every joint | [1][3] |
| I/O | Controller 8 digital in, 8 out; end of arm 4 digital in, 2 out, 2 analog in, 24 V DC 2 A | [2] |
| Fieldbus | Modbus TCP, TCP/IP, PROFINET, EtherNet/IP | [2] |
| Power | 100 to 240 V AC, 4 A maximum | [2] |
| Protection and safety | IP54; ISO 10218-1:2011; PLd Cat. 3 certified by TÜV Rheinland | [2][3] |

## How it works

The arm's seven joints use series elastic actuators, and torque sensing in every joint lets it
control force for tasks such as part insertion [3][4][9]. The head is a display that pans [12].
Grippers attach through Rethink's ClickSmart plate on the wrist [2][3]. A separate controller
holds the I/O and fieldbus ports [2].

On the factory side, the closed Intera software lets a worker teach a task by moving the arm by
hand [3]. Researchers use the Intera SDK instead: Python interfaces and examples on ROS 1, from
Indigo to Noetic, under Apache-2.0 [10]. Its last release, 5.3.0, came in August 2018; the
default branch last changed in 2021 and a `main` branch updated documentation links in 2023 [10].
There is no ROS 2 driver: asked in 2021, a contributor replied that the SDK did not support ROS 2,
and no community port was found [11].

Models: the URDF and meshes in `sawyer_description` [12]; a Gazebo simulator whose Noetic branch
was merged in September 2023 [13]; MuJoCo Menagerie's MJCF, built from that URDF with hand-made
collision shapes and position actuators, Apache-2.0 [14]; and MJCF models in robosuite and
Meta-World, both MIT [15][16].

| Variant | Year | Notes | Source |
|---|---|---|---|
| Sawyer | 2015 | Original Rethink Robotics model, $29,000 base | [1] |
| Sawyer BLACK Edition | 2019 | HAHN's Rethink Robotics GmbH; quieter and more durable, same 1260 mm reach, 4 kg payload, 7 joints | [3][5] |

## What it is used for

- Reinforcement-learning benchmarks: every Meta-World task uses a simulated Sawyer [16].
- Simulation research: robosuite offers Sawyer with the Rethink gripper as a stock arm [15].
- Multi-robot data: RoboNet includes Sawyer data, and pretraining on it helped transfer to a
  Baxter [17].
- Industry: machine tending, packaging, circuit-board assembly and inspection [3].

## Cost and BOM

| Item | Price (USD) | Type | Date | Source |
|---|---|---|---|---|
| Sawyer base price at launch | 29,000 | retail | 2015-03-19 | [1] |
| Sawyer, IEEE Robots guide listing | 34,900 | retail | undated | [4] |

No new units are sold; used units are the only route, and no current listing was checked.

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| Hardware design | — | Not published | Proprietary |
| Intera SDK | Python, ROS 1 | [RethinkRobotics/intera_sdk](https://github.com/RethinkRobotics/intera_sdk) | Apache-2.0 |
| Messages and end-effector models | ROS 1 msgs, URDF | [RethinkRobotics/intera_common](https://github.com/RethinkRobotics/intera_common) [19] | Apache-2.0 |
| Description | URDF, meshes | [RethinkRobotics/sawyer_robot](https://github.com/RethinkRobotics/sawyer_robot) | Apache-2.0 |
| Simulator | Gazebo, ROS 1 | [RethinkRobotics/sawyer_simulator](https://github.com/RethinkRobotics/sawyer_simulator) | Apache-2.0 |
| MuJoCo model | MJCF | [Menagerie](https://github.com/google-deepmind/mujoco_menagerie/tree/main/rethink_robotics_sawyer) | Apache-2.0 |
| Benchmark models | MJCF | robosuite, Meta-World | MIT |
| Intera robot software | — | On the robot | Proprietary [7] |
| Docs | HTML | [Python API docs](https://rethinkrobotics.github.io/intera_sdk_docs/); the wiki survives only in web archives | — |

## Strengths and limits

- **Strengths:** a 7-joint arm with joint torque sensing [3]; 4 kg payload and 1260 mm reach
  [2]; open Apache-2.0 SDK and URDF [10][12]; one of the most-simulated arms, so benchmark
  results refer to it [14][15][16].
- **Limits:** discontinued, with the maker gone twice and its sites offline [9][18]; ROS 1 only
  [10][11]; Julia Astrid Riemenschneider of the relaunched Rethink said in 2024 "For industrial
  applications, Sawyer had issues with repeatability and accuracy," despite the ±0.1 mm claim
  [2][8]; The Robot Report ties these problems to the series elastic actuators [9].

## Related robots

- [Baxter](baxter.md): Rethink's two-armed predecessor from 2012 [6].
- [Franka Panda](franka-panda.md), [KUKA LBR iiwa](kuka-lbr-iiwa.md),
  [Universal Robots](universal-robots.md) and [Kinova Gen3](kinova-gen3.md): the other stock arms
  in robosuite [15].

## Sources

1. [Robotics Tomorrow: Rethink Robotics unveils its newest smart, collaborative robot (2015-03-19)](https://www.roboticstomorrow.com/news/2015/03/19/automate-2015--rethink-robotics-unveils-its-newest-smart-collaborative-robot-/5757/), accessed 2026-11-18
2. [Rethink Robotics: Sawyer tech specs (archived 2019-03-07)](https://web.archive.org/web/20190307192142/https://www.rethinkrobotics.com/sawyer/tech-specs/), accessed 2026-11-18
3. [Rethink Robotics: Sawyer BLACK Edition page (archived 2024-06-14)](https://web.archive.org/web/20240614185427/https://www.rethinkrobotics.com/sawyer/), accessed 2026-11-18
4. [IEEE Robots guide: Sawyer](https://robotsguide.com/robots/sawyer), accessed 2026-11-18
5. [The Robot Report: Sawyer BLACK Edition debuts (2019-10-16)](https://www.therobotreport.com/sawyer-black-edition-debut-rethink-robotics-new-ceo/), accessed 2026-11-18
6. [IEEE Spectrum: Rethink Robotics, Pioneer of Collaborative Robots, Shuts Down (2018-10-04)](https://spectrum.ieee.org/rethink-robotics-pioneer-of-collaborative-robots-shuts-down), accessed 2026-11-18
7. [The Robot Report: Rethink Robotics cobots get continuing support (2018-10-25)](https://www.therobotreport.com/rethink-robotics-cobots-get-continuing-support/), accessed 2026-11-18
8. [The Robot Report: Rethink Robotics relaunches with cobots, AMRs, mobile manipulation (2024-09-09)](https://www.therobotreport.com/rethink-robotics-relaunches-with-cobots-amrs-mobile-manipulation/), accessed 2026-11-18
9. [The Robot Report: Rethink Robotics shuts down, again (2025-09-16)](https://www.therobotreport.com/rethink-robotics-shuts-down-again/), accessed 2026-11-18
10. [RethinkRobotics Intera SDK repository and changelog](https://github.com/RethinkRobotics/intera_sdk), accessed 2026-11-18
11. [Intera SDK issue 160: Support for ROS2?](https://github.com/RethinkRobotics/intera_sdk/issues/160), accessed 2026-11-18
12. [RethinkRobotics sawyer_robot repository](https://github.com/RethinkRobotics/sawyer_robot), accessed 2026-11-18
13. [RethinkRobotics sawyer_simulator repository](https://github.com/RethinkRobotics/sawyer_simulator), accessed 2026-11-18
14. [MuJoCo Menagerie rethink_robotics_sawyer](https://github.com/google-deepmind/mujoco_menagerie/tree/main/rethink_robotics_sawyer), accessed 2026-11-18
15. [robosuite robots and grippers](https://robosuite.ai/docs/modules/robots.html), accessed 2026-11-18
16. [Meta-World: A Benchmark and Evaluation for Multi-Task and Meta Reinforcement Learning](https://arxiv.org/abs/1910.10897), accessed 2026-11-18
17. [RoboNet: Large-Scale Multi-Robot Learning](https://arxiv.org/abs/1910.11215), accessed 2026-11-18
18. [rethinkrobotics.com (archived 2026-03-15, parked domain)](https://web.archive.org/web/20260315180906/https://rethinkrobotics.com/), accessed 2026-11-18
19. [RethinkRobotics intera_common repository](https://github.com/RethinkRobotics/intera_common), accessed 2026-11-18
