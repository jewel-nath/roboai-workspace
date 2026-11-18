---
type: robot
name: Fetch Robotics Fetch and Freight
summary: Fetch Robotics' single-arm research mobile manipulator (2015) and its Freight base, long a standard ROS 1 platform and the robot of Habitat 2.0; no longer sold or supported by Zebra Technologies since 2024, with BSD and Apache ROS 1 packages and a non-commercial description.
tags: [single-arm, ros1, differential-drive, fetch-robotics, zebra, discontinued, gazebo, moveit, habitat]
category: mobile-manipulator
tier: B
openness: software-only
maker: Fetch Robotics
year: 2015
license: {hardware: , software: BSD-3-Clause AND Apache-2.0 AND CC-BY-NC-SA-4.0, docs: }
links: {repo: "https://github.com/fetchrobotics/fetch_ros", docs: "https://fetchrobotics.github.io/docs/", cad: , paper: , site: }
specs: {dof: 11, payload_kg: 6, reach_mm: , mass_kg: 113.3, size_mm: , speed_mps: 1.0, runtime_h: 9}
stack: {actuators: "back-drivable 7-DoF arm; prismatic torso with 400 mm travel; pan-tilt head; parallel gripper; two-wheel differential drive", mcu: , compute: "Intel i5, 8 GB RAM, 120 GB SSD; last docs target Ubuntu 20.04 and ROS Noetic", sensors: ["SICK TiM571 base laser, 25 m, 220°", "Primesense Carmine 1.09 RGB-D camera in the head", "6-axis IMU in the base", "IMU in the gripper"], sim_models: ["URDF (fetchrobotics/fetch_ros fetch_description, CC BY-NC-SA 4.0)", "Gazebo Classic (fetchrobotics/fetch_gazebo, ROS 1)", "URDF (robot_descriptions fetch_description, copy from OpenAI roboschool)", "Habitat 2.0 (Fetch is its benchmark robot)"], ros2: none}
cost: {type: , usd: , as_of: , source: }
build: {difficulty: , hours: , print_hours: }
maturity: {last_commit: 2024-06-07, stars: 205, active: false}
use_cases: [research, manipulation, navigation, reinforcement-learning, education]
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://fetchrobotics.github.io/docs/introduction.html", title: "Fetch & Freight Research Edition manual: Introduction", accessed: 2026-11-18}
  - {url: "https://fetchrobotics.github.io/docs/robot_hardware.html", title: "Fetch & Freight Research Edition manual: Robot Hardware Overview", accessed: 2026-11-18}
  - {url: "https://spectrum.ieee.org/fetch-robotics-introduces-fetch-and-freight-your-warehouse-is-now-automated", title: "IEEE Spectrum: Fetch Robotics introduces Fetch and Freight (2015-04-29)", accessed: 2026-11-18}
  - {url: "https://robotsguide.com/robots/fetch", title: "IEEE Robots guide: Fetch", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/zebra-technologies-winding-down-fetch-based-mobile-robot-group/", title: "The Robot Report: Zebra Technologies winding down Fetch-based mobile robot group (2025-12-12)", accessed: 2026-11-18}
  - {url: "https://www.therobotreport.com/skild-acquires-fetch-robotics-assets-from-zebra-automation/", title: "The Robot Report: Skild acquires Fetch Robotics assets from Zebra (2026-04-16)", accessed: 2026-11-18}
  - {url: "https://github.com/fetchrobotics/fetch_ros", title: "fetchrobotics/fetch_ros (ros1)", accessed: 2026-11-18}
  - {url: "https://github.com/fetchrobotics/fetch_gazebo", title: "fetchrobotics/fetch_gazebo", accessed: 2026-11-18}
  - {url: "https://github.com/robot-descriptions/robot_descriptions.py", title: robot_descriptions model list, accessed: 2026-11-18}
  - {url: "https://arxiv.org/abs/2106.14405", title: "Szot et al.: Habitat 2.0, training home assistants to rearrange their habitat (2021)", accessed: 2026-11-18}
---

# Fetch Robotics Fetch and Freight

A single-arm mobile manipulator from Fetch Robotics, introduced in 2015 with the Freight base for
warehouses and later sold as a research platform [1][3]. Zebra Technologies bought Fetch Robotics in
2021 [5]. It is discontinued: the manual says the research robots have not been sold or supported by
Zebra since 2024 [1]. Builders still meet it in papers and in simulators such as Habitat 2.0 [10].

## Specs

| Item | Value | Source |
|---|---|---|
| Variant in frontmatter | Fetch; Freight is the same base without torso, arm or head | [3][7] |
| Degrees of freedom | 11 counted: torso lift, 7-DoF arm, gripper, head pan and tilt; the two drive wheels are not counted. The Robots guide also gives 11, counting the base instead of the head | [2][4] |
| Arm payload, reach | 6 kg (maker's claim); no reach figure found, but the maker said it grasps from the floor to just under 2 m | [3][4] |
| Mass, height | about 113.3 kg; 109.6 cm, or 149.1 cm with the torso raised | [2][4] |
| Torso, gripper | torso 0 to 400 mm at up to 0.1 m/s; each finger 0 to 50 mm, 60 N limit | [2] |
| Speed | 3.6 km/h, about 1.0 m/s | [4] |
| Battery | two 12 V sealed lead-acid batteries for a 24 V rail; 9 h | [2][4] |
| Computer | Intel i5, 8 GB RAM, 120 GB SSD | [4] |
| Sensors | SICK TiM571 laser (25 m, 220°, 15 Hz); Primesense Carmine 1.09 RGB-D in the head; IMUs in base and gripper | [2][4] |

## How it works

A two-wheel differential base carries a prismatic torso, which lifts a back-drivable 7-DoF arm and a
pan-tilt RGB-D head [2][3]. The gripper sits on an ISO-standard mechanical interface that also
carries Ethernet and 24 V power, so cameras or other tools can replace it [2][3].

The software is ROS 1; the last manual targets ROS Noetic on Ubuntu 20.04 [1]. `fetch_ros` holds the
description, MoveIt config, navigation, calibration, teleop and an IKFast plugin; its default branch,
`ros1`, last changed on 2024-06-07, and its README lists ROS 2 only as "in planning" [7].

`fetch_gazebo` simulates Fetch and Freight in Gazebo Classic; its `gazebo11` branch last changed in
June 2024 [8]. robot_descriptions loads a Fetch URDF copied in OpenAI's roboschool and lists it as
MIT [9], though the original is CC BY-NC-SA 4.0 [7]. Habitat 2.0 uses Fetch as its robot [10].

| Variant | What it is | Source |
|---|---|---|
| Fetch | base, torso, 7-DoF arm, gripper and head | [2][3] |
| Freight | base only; at launch the maker claimed 70 kg payload and 2 m/s, up to 3 m/s | [3][7] |

## What it is used for

- Mobile manipulation research; OpenAI used Fetch to explore machine learning for it [5].
- Embodied AI in simulation: Habitat 2.0 trains Fetch to pick, open drawers and rearrange [10].
- Teaching and contests: `fetch_gazebo` ships pick-and-place demos and a `fetchit_challenge` package [8].
- Warehouse picking, its launch pitch: the maker said 6 kg covers 90 to 95% of warehouse items [3].

## Cost and BOM

No list price was found, so `cost` stays empty. At launch the CEO said Fetch would cost under
$100,000 [3]; the Robots guide lists a base price of 100000 with no currency or date [4]. Skild AI bought Zebra's
robotics unit in April 2026 and plans to sell new Fetch robots, naming only warehouse models [6].

## What is open

| Item | Format | Where | Licence |
|---|---|---|---|
| ROS 1 packages: MoveIt, navigation, calibration, teleop | ROS 1 (catkin) | [fetch_ros](https://github.com/fetchrobotics/fetch_ros) [7] | BSD-3-Clause; calibration and IKFast plugin Apache-2.0 |
| Description of Fetch and Freight | URDF, meshes | `fetch_ros/fetch_description` [7] | CC BY-NC-SA 4.0, non-commercial |
| Gazebo simulation and demos | ROS 1 packages | [fetch_gazebo](https://github.com/fetchrobotics/fetch_gazebo) [8] | BSD |
| Hardware, firmware | — | Not published | Closed |

## Strengths and limits

- **Strengths:** a 6 kg arm on a lifting torso, from the floor to about 2 m [3]; 9 h runtime [4];
  mature ROS 1 MoveIt and navigation configs [7]; a tool flange with Ethernet and 24 V [2].
- **Limits:** not sold or supported by Zebra since 2024 [1]; ROS 1 only [7]; the description is
  non-commercial [7]; 113 kg on lead-acid batteries [2]; no published list price [3].

## Related robots

- [PR2](pr2.md): the larger two-armed ROS research robot before it.
- [TIAGo](tiago.md), [Hello Robot Stretch](hello-robot-stretch.md): research mobile manipulators on sale.
- [Clearpath Robotics](clearpath-robots.md): ROS research bases.

## Sources

1. [Fetch & Freight Research Edition manual: Introduction](https://fetchrobotics.github.io/docs/introduction.html), accessed 2026-11-18
2. [Fetch & Freight Research Edition manual: Robot Hardware Overview](https://fetchrobotics.github.io/docs/robot_hardware.html), accessed 2026-11-18
3. [IEEE Spectrum: Fetch Robotics introduces Fetch and Freight (2015-04-29)](https://spectrum.ieee.org/fetch-robotics-introduces-fetch-and-freight-your-warehouse-is-now-automated), accessed 2026-11-18
4. [IEEE Robots guide: Fetch](https://robotsguide.com/robots/fetch), accessed 2026-11-18
5. [The Robot Report: Zebra Technologies winding down Fetch-based mobile robot group (2025-12-12)](https://www.therobotreport.com/zebra-technologies-winding-down-fetch-based-mobile-robot-group/), accessed 2026-11-18
6. [The Robot Report: Skild acquires Fetch Robotics assets from Zebra (2026-04-16)](https://www.therobotreport.com/skild-acquires-fetch-robotics-assets-from-zebra-automation/), accessed 2026-11-18
7. [fetchrobotics/fetch_ros (ros1)](https://github.com/fetchrobotics/fetch_ros), accessed 2026-11-18
8. [fetchrobotics/fetch_gazebo](https://github.com/fetchrobotics/fetch_gazebo), accessed 2026-11-18
9. [robot_descriptions model list](https://github.com/robot-descriptions/robot_descriptions.py), accessed 2026-11-18
10. [Szot et al.: Habitat 2.0, training home assistants to rearrange their habitat (2021)](https://arxiv.org/abs/2106.14405), accessed 2026-11-18
