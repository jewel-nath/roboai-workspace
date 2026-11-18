---
type: source
name: Awesome Robotics Projects
registry: awesome-robotics-projects
url: https://github.com/mjyc/awesome-robotics-projects
commit: "9943f0e"
read_on: 2026-11-17
counts: {entries: 63, pages: 9, waiting: 8, index_only: 26, deferred: 17, rejected: 3}
---

# Awesome Robotics Projects: what it gives RoboAI

A personal list of open-source, affordable and unusual robot projects, followed by robotics
software, tools, datasets, communities and companies. Its robot list is a good mix of landmark
open builds (Stanford Doggo, Poppy, TurtleBot, the JPL rover) and newer ones (Berkeley Humanoid
Lite, Open Duck Mini, RUKA), but about half its robots are small one-off builds or dormant. Its
software sections belong to Phase 4.

## How it was read

- Read at commit `9943f0e` on 2026-11-17. Phase 3 covers the robot list at the top and the
  `Library, Framework, SDK > Robots` subsection: 63 entries, with Dobb-E's duplicate merged.
- **Left for Phase 4:** Autonomous Driving, ML & Vision, Command Line Tools, Data Visualization &
  UI, Simulators, Dataset, Deployment, Hardware Communities, Conferences & Events, Newsletter,
  Bloggers, Robotics Tooling Companies, Deployment & DevEnv and Related Awesome Lists.
- Each robot's own repo was checked with a shallow git clone (last commit, licence files, CAD and
  BOM); pages without a repo were checked to still load. Software in the robot list (LeRobot,
  PyRobot, PythonRobotics and others) is deferred to Phase 4.
- A page needs files a builder can use under a stated licence, so DUMMY (popular, but with no
  licence) is index only.
- Dead or moved on 2026-11-17: LHF connect's domain now serves spam; poppy-project.org and the
  K-Scale sites no longer resolve; `osrf/rmf_demos` moved to `open-rmf/rmf_demos`. K-Scale Labs
  shut down in November 2025, so K-Bot can no longer be bought.

## Pages made

| Entry | Page | Tier |
|---|---|---|
| Berkeley Humanoid Lite | [Berkeley Humanoid Lite](../wiki/robots/berkeley-humanoid-lite.md) | A |
| JPL Open Source Rover | [JPL Open Source Rover](../wiki/robots/jpl-open-source-rover.md) | A |
| NanoSaur | [NanoSaur](../wiki/robots/nanosaur.md) | A |
| Open Duck Mini v2 | [Open Duck Mini v2](../wiki/robots/open-duck-mini.md) | A |
| OpenBot | [OpenBot](../wiki/robots/openbot.md) | A |
| BCN3D Moveo | [BCN3D Moveo](../wiki/robots/bcn3d-moveo.md) | B |
| Openmanipulator (ROBOTIS) | [OpenManipulator-X](../wiki/robots/openmanipulator-x.md) | B |
| RUKA (NYU) | [RUKA](../wiki/robots/ruka.md) | B |
| TriFinger | [TriFinger](../wiki/robots/trifinger.md) | B |

## Waiting for a page

| Entry | Page | Tier | Why it matters |
|---|---|---|---|
| ANYmal C (ANYbotics) | `anymal` | B | Common research quadruped and legged-RL baseline |
| Nybble (Petoi) | `petoi-nybble-bittle` | B | Popular servo robot-cat kit on open OpenCat firmware; a first step into legged gaits |
| Open Dynamic Robot Initiative | `odri-solo` | B | Open torque-controlled actuator and the Solo quadrupeds |
| Poppy Project | `poppy-humanoid` | B | Historically important open printed humanoid and teaching platform; dormant |
| Reachy 2 (Pollen Robotics) | `reachy` | B | Research humanoid with an open ROS 2 stack, supported in LeRobot |
| Stanford Doggo | `stanford-doggo` | B | Landmark open jumping quadruped with Fusion 360 CAD and BOM; its team later made Pupper |
| Thor (AngelLM) | `angellm-thor` | B | Well-known printable 6-DoF arm designed in FreeCAD |
| TurtleBot | `turtlebot` | B | The standard ROS teaching and Nav2 reference robot line |

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| Animatronic Eye Mechanism | Print-in-place eye mechanism for props; a mechanism, not a robot | — | unknown |
| AWS DeepRacer | 1/18 RL race car; service retired and devices off sale since December 2025 | — | — |
| BetaBot | Printable arm in Inventor files; inactive | 2016-02-04 | GPL-3.0 |
| BiDexHand | 16-DoF open hand with STL, STEP and BOM; one developer, no known builds yet | 2025-11-23 | MIT |
| Bobble-Bot | Balancing robot for teaching real-time control, mostly in simulation | 2021-12-05 | BSD-3-Clause |
| DG-5F (Tesollo) | Commercial five-finger robot hand | — | — |
| DUMMY (Peng Zhihui) | Popular desktop 6-axis arm with STEP, PCB and firmware, but no licence | 2022-10-21 | none found |
| ExoMy (ESA) | Printed six-wheel Mars rover; inactive, the JPL rover covers the niche | 2021-02-10 | GPL-3.0 |
| Forte | Capstan-drive low-cost arm; paper only, no files released | — | unknown |
| GoodBoy | Small Arduino servo robot dog, a 2020 one-off | — | unknown |
| Just1 | Personal ROS 2 robot build with a good write-up | 2025-11-09 | MIT |
| K-Bot (K-Scale Labs) | Full-size open humanoid; its maker shut down in November 2025 | 2025-11-07 | MIT, CERN-OHL-S-2.0 (hardware) |
| MABEL | Raspberry Pi wheel-legged balancing robot, a 2020 one-off | 2020-08-18 | GPL-3.0 |
| Magni (Ubiquity Robotics) | Commercial ROS mobile base | — | — |
| Maker's Pet (Loki) | Printed ESP32 home robot; STLs hosted elsewhere | 2025-01-05 | Apache-2.0 |
| MuSHR | University of Washington research race car; inactive, F1TENTH covers it | 2022-02-10 | BSD-3-Clause |
| Niryo One | Printed 6-axis ROS arm; discontinued, non-commercial licence | 2020-10-08 | CC-BY-NC-SA-4.0 |
| Open-Source Robotic Arm (Abot) | Student arm with STM32 CAN-bus joints, thin docs | 2019-03-15 | none found |
| OpenPodcar | Autonomous mobility-scooter conversion; inactive | 2022-05-09 | GPL-2.0 |
| OpenBionics | Academic low-cost robot and prosthetic hands; inactive | 2018-02-09 | CC-BY-SA-4.0 |
| ROBEL (Google) | D'Claw and D'Kitty RL benchmark robots; dormant | 2020-02-12 | Apache-2.0 |
| RoboPrime | 21-servo printed humanoid on an ATmega328P, a 2017 one-off | 2017-10-19 | GPL-3.0 |
| ROSbot 2.0 (Husarion) | Commercial four-wheel ROS 2 robot | 2026-11-09 | Apache-2.0 (software) |
| UMIRobot | Small printed teaching arm; inactive | 2022-06-29 | GPL-3.0 (code) |
| Vine Robots | Build guides for tip-growing soft robots; a robot type, better as a concept page | — | unknown |
| Walter | Vintage-styled 6-DoF arm, a 2017 one-person build | 2017-04-30 | none found |

## Deferred

| Entry | What it is | Phase |
|---|---|---|
| CHAMP | ROS quadruped controller | 4 |
| CyPhyHouse | Toolchain for distributed robot fleets | 4 |
| Dobb-E (listed twice) | Imitation-learning framework for household tasks on Stretch | 4 |
| LeRobot | Hugging Face robot-learning library | 4 |
| Linorobot | ROS 2 stack and firmware for DIY wheeled bases | 4 |
| NVIDIA Isaac Platform | Simulation and robot AI platform | 4 |
| PyRobot | Meta's Python interface for robot-learning experiments | 4 |
| PythonRobotics | Python samples of robotics algorithms | 4 |
| Robotics Middleware Framework | Fleet task and traffic management | 4 |
| boston-dynamics/spot-sdk | Spot SDK, proprietary licence | 4 |
| copper-project/copper-rs | Deterministic robot runtime in Rust | 4 |
| facebookresearch/home-robot | Mobile-manipulation stack for Stretch | 4 |
| facebookresearch/pyrobot | Same project as PyRobot | 4 |
| resibots/minitaur_sdk | Minitaur SDK extension, proprietary licence | 4 |
| robotemi/sdk | Android SDK for the temi robot | 4 |
| Anki Cozmo Python SDK, C# SDK, PyCozmo | Official and community Cozmo SDKs | 4 |
| unitreerobotics/unitree_sdk2 | SDK for current Unitree robots | 4 |

## Rejected

| Entry | Why | Date |
|---|---|---|
| LHF connect | Dead link: the domain now serves a spam page | 2026-11-17 |
| Nguyen Vincent's omnidirectional ROS2 robot | A build video and code, with no CAD, BOM or licence | 2026-11-17 |
| RoboArm | Too thin to build from: a small repo with parts on Thingiverse, dated 2019 | 2026-11-17 |
