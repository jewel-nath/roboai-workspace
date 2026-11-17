---
type: source
name: awesome-ros-mobile-robot
registry: awesome-ros-mobile-robot
url: https://github.com/shannon112/awesome-ros-mobile-robot
commit: "a405fbf"
read_on: 2026-11-17
counts: {entries: 23, pages: 2, waiting: 8, index_only: 7, deferred: 3, rejected: 2}
---

# awesome-ros-mobile-robot: what it gives RoboAI

A list of resources for building ROS mobile robots: theory, ROS, platforms, sensors,
calibration, odometry, SLAM, localization, mapping, navigation and manipulation. For the Atlas it
gives a short platform section naming the classic ROS research robots and the small race-car
projects; its real weight is the software sections, which Phase 4 reads.

## How it was read

- Read at commit `a405fbf` on 2026-11-17 (its last commit is 2025-10-31). Phase 3 covers only
  the `2_Robotic_Platform` section: 23 entries.
- **Left for Phase 4:** sections 0, 1 and 3 to 11 (robotics theory, ROS, sensing, calibration,
  odometry, SLAM, localization, mapping, navigation, manipulation, and the companies,
  publications, competitions and organisations).
- The processing-unit and motor-vendor bullets are parts, deferred to Phase 5. The wheel
  configuration images were skipped.
- Open designs were checked with shallow git clones; commercial robots were judged by how often
  builders meet them. Robots also listed in awesome-robot-descriptions share its page slugs.
- Dead on 2026-11-17: both Clearpath Husky manipulation guides. f1tenth.org now redirects to
  roboracer.ai (the project's new name; its docs and GitHub still say F1TENTH). The Techman link is
  an unofficial ROS 1 driver.

## Pages made

| Entry | Page | Tier |
|---|---|---|
| "Penn" race car (F1TENTH, now RoboRacer) | [F1TENTH (RoboRacer)](../wiki/robots/f1tenth.md) | A |
| "turtlebot3" (ROBOTIS) | [TurtleBot3](../wiki/robots/turtlebot3.md) | A |

## Waiting for a page

| Entry | Page | Tier | Why it matters |
|---|---|---|---|
| "Georgia Tech" race car (AutoRally) | `autorally` | B | 1:5 off-road autonomous rally car with an open build guide; platform of the MPPI driving papers |
| "turtlebot" (GitHub org) | `turtlebot` | B | TurtleBot 2 and 4, the ROS reference robot line |
| "clearpath husky", "clearpath jackel" | `clearpath-robots` | B | The best-known commercial ROS research bases |
| "Personal Robot 2 (PR2)" | `pr2` | B | The robot ROS grew up on |
| "kuka youbot" | `kuka-youbot` | B | Classic teaching mobile manipulator, standard in Webots and CoppeliaSim; discontinued |
| "fetch robotics" | `fetch` | B | Long a standard ROS research mobile manipulator |
| "Franka Emika panda" | `franka-panda` | B | Among the most common arms in manipulation research |
| "Universal Robot 3/5/10/e" | `universal-robots` | B | The most widespread cobots, with standard ROS drivers |

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| "MIT" race car (MIT RACECAR) | 1/10 teaching race car, predecessor of F1TENTH; on its page | 2022-02-23 | BSD-3-Clause (software) |
| "UCB" race car (BARC) | 1/10 Berkeley control-research car; inactive | 2021-06-09 | MIT |
| "Taiwan Hypharos" race car | Low-cost 1/10 car with RPLidar and Odroid; inactive | 2018-05-09 | LGPL-3.0 |
| "Robotnik XL-GEN" | Summit-XL base, the same robot as RB-SUMMIT | — | — |
| "Robotnik RB-KAIROS" | Omnidirectional base with a cobot arm | — | — |
| "Robotnik RB-1" | One-arm torso mobile manipulator | — | — |
| "Techman Robot" | Cobot with a wrist camera; the link is an unofficial driver | — | — |

## Deferred

| Entry | What it is | Phase |
|---|---|---|
| "Aerial, Ground, Marine, Manipulator, Component" (robots.ros.org) | Directory of robots with ROS support | 4 |
| Processing Unit (SBC/IPC): Raspberry Pi, BeagleBone Black, Odroid, Tinker Board, Jetson, ADLINK Neuron | Robot computers | 5 |
| Motor & Controller & Encoder: Elmo, RLS, Faulhaber, Maxon, Dexmart | Motor and encoder vendors | 5 |

## Rejected

| Entry | Why | Date |
|---|---|---|
| "clearpath husky+UR5" | Dead link (404); the configuration belongs on `clearpath-robots` | 2026-11-17 |
| "clearpath husky+dualUR5" | Dead link (404); the configuration belongs on `clearpath-robots` | 2026-11-17 |
