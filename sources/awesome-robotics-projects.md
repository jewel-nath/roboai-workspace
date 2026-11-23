---
type: source
name: Awesome Robotics Projects
registry: awesome-robotics-projects
url: https://github.com/mjyc/awesome-robotics-projects
commit: "9943f0e"
read_on: 2026-11-17
counts: {entries: 195, pages: 29, waiting: 5, index_only: 127, deferred: 1, rejected: 33}
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
- **Phase 4** read, on 2026-11-18 at the same commit, Autonomous Driving, ML & Vision, Command
  Line Tools, Data Visualization & UI, Simulators, Dataset, Deployment, Hardware Communities,
  Conferences & Events, Newsletter, Bloggers, Robotics Tooling Companies, Deployment & DevEnv,
  Related Awesome Lists and Shameless Self-Advertisement (which Phase 3 did not name), and decided
  the 17 software rows Phase 3 deferred. Page candidates were checked with shallow git clones
  (last commit, licence) and every link with an HTTP request; the eleven bloggers are one row. No
  section holds only papers. CRISP links this list itself (its repo is
  `utiasDSL/crisp_controllers`), and the ROSBoard link is a deleted fork of `dheera/rosboard`.
  Renamed sites: formant.ai, mirurobotics.com, getvinci.ai, synpse.com. Dead links and domains
  that now serve unrelated sites are in Rejected. Nothing in the README addresses agents.
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
| ANYmal C (ANYbotics) | [ANYmal B, C, D and X](../wiki/robots/anymal.md) | B |
| Nybble (Petoi) | [Petoi Nybble and Bittle](../wiki/robots/petoi-nybble-bittle.md) | B |
| Open Dynamic Robot Initiative | [ODRI Solo-8, Solo-12 and Bolt](../wiki/robots/odri-solo.md) | B |
| Poppy Project | [Poppy Humanoid](../wiki/robots/poppy-humanoid.md) | B |
| Stanford Doggo | [Stanford Doggo](../wiki/robots/stanford-doggo.md) | B |
| Thor (AngelLM) | [Thor (AngelLM)](../wiki/robots/angellm-thor.md) | B |
| Reachy 2 (Pollen Robotics) | [Reachy and Reachy 2](../wiki/robots/reachy.md) | B |
| TurtleBot | [TurtleBot (1, 2 and 4)](../wiki/robots/turtlebot.md) | B |
| Pixi: Modern package management for Robotics | [Pixi (with RoboStack)](../wiki/tools/pixi.md) | B |
| rerun.io | [Rerun](../wiki/tools/rerun.md) | B |
| Gazebo | [Gazebo](../wiki/tools/gazebo.md) | A |
| MuJoCo | [MuJoCo](../wiki/tools/mujoco.md) | A |
| NVIDIA Isaac Sim | [Isaac Sim](../wiki/tools/isaac-sim.md) | A |
| Webots | [Webots](../wiki/tools/webots.md) | B |
| AI Habitat | [Habitat](../wiki/tools/habitat.md) | B |
| CARLA | [CARLA](../wiki/tools/carla.md) | B |
| borglab/gtsam | [GTSAM](../wiki/software/gtsam.md) | A |
| Linorobot | [linorobot2](../wiki/software/linorobot2.md) | B |
| PythonRobotics | [PythonRobotics](../wiki/software/pythonrobotics.md) | B |
| autowarefoundation/autoware.universe | [Autoware](../wiki/software/autoware.md) | B |

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|
| LeRobot | `learning/lerobot` | A | learning | Hugging Face's library of datasets, policies and low-cost arm support; the centre of hobby robot learning |
| Robotics Middleware Framework | `software/open-rmf` | B | ops | Open-RMF, the ROS 2 framework for multi-vendor fleets sharing lifts, doors and corridors |
| LIBERO | `learning/libero` | B | learning | Simulated manipulation benchmark that most recent VLA and imitation-learning papers report on |
| OmniGibson | `learning/behavior-1k` | B | learning | Same project as BEHAVIOR-1K: its repo now holds both the OmniGibson simulator and the benchmark |
| SimplerEnv | `learning/simpler-env` | B | learning | Simulated evaluation matched to real Google Robot and WidowX setups; widely reported for VLAs |

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| Animatronic Eye Mechanism | Print-in-place eye mechanism for props; a mechanism, not a robot | — | unknown |
| AWS DeepRacer | 1/18 RL race car; service retired and devices off sale since December 2025 | — | — |
| BetaBot | Printable arm in Inventor files; inactive | 2016-02-04 | GPL-3.0 |
| BiDexHand | 16-DoF open hand with STL, STEP and BOM; one developer, no known builds yet | 2025-11-23 | MIT |
| Bobble-Bot | Balancing robot for teaching real-time control, mostly in simulation | 2021-12-05 | BSD-3-Clause |
| CHAMP | ROS quadruped gait controller used by many hobby robot dogs | 2024-07-04 | BSD-3-Clause |
| CyPhyHouse | Academic toolchain for programming distributed robot fleets | — | — |
| DG-5F (Tesollo) | Commercial five-finger robot hand | — | — |
| Dobb-E (listed twice) | NYU imitation-learning framework and Stick data collector for Stretch | 2024-10-15 | MIT |
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
| NVIDIA Isaac Platform | NVIDIA's umbrella for Isaac Sim, Isaac Lab, Isaac ROS and GR00T | — | — |
| Open-Source Robotic Arm (Abot) | Student arm with STM32 CAN-bus joints, thin docs | 2019-03-15 | none found |
| OpenPodcar | Autonomous mobility-scooter conversion; inactive | 2022-05-09 | GPL-2.0 |
| OpenBionics | Academic low-cost robot and prosthetic hands; inactive | 2018-02-09 | CC-BY-SA-4.0 |
| PyRobot | Meta's Python interface for robot-learning experiments; pyrobot.org no longer resolves | 2026-07-30 | MIT |
| ROBEL (Google) | D'Claw and D'Kitty RL benchmark robots; dormant | 2020-02-12 | Apache-2.0 |
| RoboPrime | 21-servo printed humanoid on an ATmega328P, a 2017 one-off | 2017-10-19 | GPL-3.0 |
| ROSbot 2.0 (Husarion) | Commercial four-wheel ROS 2 robot | 2026-11-09 | Apache-2.0 (software) |
| UMIRobot | Small printed teaching arm; inactive | 2022-06-29 | GPL-3.0 (code) |
| Vine Robots | Build guides for tip-growing soft robots; a robot type, better as a concept page | — | unknown |
| Walter | Vintage-styled 6-DoF arm, a 2017 one-person build | 2017-04-30 | none found |
| boston-dynamics/spot-sdk | Spot's Python SDK, proprietary; for the [Boston Dynamics Spot](../wiki/robots/boston-dynamics-spot.md) page | — | — |
| copper-project/copper-rs | Deterministic Rust runtime for robot software; young project | — | — |
| facebookresearch/home-robot | Meta's mobile-manipulation stack for Stretch; inactive | 2024-05-24 | MIT |
| robotemi/sdk | Android SDK for the temi telepresence robot, not in the Atlas | — | — |
| Anki Cozmo Python SDK, C# SDK, PyCozmo | Anki's Cozmo SDKs and the community PyCozmo library | — | — |
| unitreerobotics/unitree_sdk2 | SDK for Go2, B2, H1 and G1; for the Unitree robot pages | — | — |
| ApolloAuto/apollo | Baidu's full self-driving software stack | — | — |
| commaai/openpilot | Driver-assistance software for production cars | — | — |
| any4lerobot | Dataset conversion and utilities for LeRobot | — | — |
| facebookresearch/theseus | Meta's differentiable nonlinear optimisation library for PyTorch | — | — |
| KFCore | Small Kalman filter library in C, C++ and MATLAB | — | — |
| nano-pgo | Single-file Python pose-graph optimisation for teaching | — | — |
| openMVG/openMVG | Multiple-view geometry and structure-from-motion library | — | — |
| CRISP | Compliant ROS 2 controllers for learned policies; the list mislinks it | 2026-08-16 | MIT |
| ros command | Shortcuts unifying ROS 1 and ROS 2 command-line tools | — | — |
| ROSA | NASA JPL's LLM agent for inspecting and operating ROS robots | — | — |
| ROSBoard | Web dashboard node for ROS; the listed fork is gone, use dheera/rosboard | 2026-08-21 | BSD-3-Clause |
| TermViz - ROS visualization on the terminal | Terminal ROS visualiser for headless robots | — | — |
| A-FRAME | Web framework for 3D, AR and VR scenes | — | — |
| AR.js | Augmented reality in the web browser | — | — |
| CloudPeek | Single-header C++ point-cloud viewer | — | — |
| Lanelet2 | C++ lane-map library for automated driving | — | — |
| mujoco-scene-editor | Small interactive editor for MuJoCo scenes | — | — |
| phntm_bridge_client | WebRTC bridge for ROS 2 streaming, teleoperation and monitoring | — | — |
| ROS Reality | Unity bridge to view and teleoperate ROS robots in VR | — | — |
| ros2_bag_exporter | Exports rosbag2 files to common file formats | — | — |
| rosetta — ROS 2 ⇄ LeRobot bridge | YAML-defined bridge between ROS 2 topics and LeRobot policies | — | — |
| URDF-Architect | Web-based visual URDF editor with MuJoCo export | — | — |
| URDFormer | Research code that builds URDF scenes from images | — | — |
| web-based visualization libraries (Webviz) | Cruise's browser visualiser, inactive since 2022; Foxglove began as its fork | 2022-03-10 | Apache-2.0 |
| Flightmare | UZH quadrotor simulator with a Unity renderer | — | — |
| MetaDrive | Lightweight procedurally generated driving simulator for RL | — | — |
| Open 3D Engine (O3DE) | Open game engine with a ROS 2 Gem for simulation | — | — |
| Project dave | Gazebo-based underwater robot simulation | — | — |
| Unity Robotics Hub | Unity's ROS integration packages and tutorials | 2026-09-22 | Apache-2.0 |
| ZeroSimROSUnity | Unity-based robot simulation with ROS integration | — | — |
| nvidia/PhysicalAI-Autonomous-Vehicles | NVIDIA's multi-sensor driving dataset on Hugging Face | — | — |
| YCB Benchmarks – Object and Model Set | Standard object set and 3D models for manipulation benchmarks | — | — |
| ROS Kubernetes / KubeEdge | Sample setups for running ROS and ROS 2 on Kubernetes | — | — |
| hackaday and hackaday.io | Hardware news blog and project-hosting community | — | — |
| hackster.io | Community of hardware project tutorials | — | — |
| instructables | Step-by-step maker project guides | — | — |
| BARS | Bay Area Robotics Symposium; the link is the 2021 edition | — | — |
| MODEX | Supply-chain and warehouse automation trade show | — | — |
| Robotics Summit & Expo | Robotics industry conference and expo | — | — |
| ROSCon | Yearly ROS developer conference; the link is the 2023 edition | — | — |
| TEROS | Texas regional robotics symposium | — | — |
| Evan Ackerman's Twitter feed | Posts by IEEE Spectrum's robotics editor, now on X | — | — |
| IEEE SPECTRUM - Robotics | Robotics news and features | — | — |
| The Robot Report | Robotics industry news | — | — |
| The Verge - Robot | Consumer tech news about robots | — | — |
| Weekly Robotics | Weekly newsletter of robotics news and open-source projects | — | — |
| TechCrunch: Robotics category, robotics tag | Startup and funding news about robotics | — | — |
| Bloggers (11 blogs) | Personal robotics blogs, among them Rodney Brooks, Sergey Levine, Matt Mason | — | — |
| Applied Intuition | Simulation and software tools for vehicles and physical AI | — | — |
| cogniteam | Cloud robotics platform and software services | — | — |
| Ekumen | Robotics software consultancy | — | — |
| FogROS2 | Berkeley framework that offloads ROS 2 nodes to cloud machines | — | — |
| Formant | Fleet operations platform for robots; now formant.ai | — | — |
| Generalist | Company building robot foundation models | — | — |
| Honu Robotics | Robotics engineering services company | — | — |
| InOrbit | Robot operations and fleet management platform | — | — |
| Lightwheel-Platform Enterprise | Simulation assets and synthetic data for robot learning | — | — |
| micropsi industries | AI control for industrial robot arms (MIRAI) | — | — |
| miru | Configuration and deployment tooling for robots; now mirurobotics.com | — | — |
| Nema | Tools for safety-critical autonomous systems; its focus has changed | — | — |
| Open Navigation LLC | The Nav2 maintainers' company: support and services | — | — |
| PHANTOM AI | Driver-assistance software company | — | — |
| Physical Intelligence (π) | Robot foundation-model company behind the π0 policies | — | — |
| Rapyuta Robotics | Warehouse robots and automation | — | — |
| Roboto | Analytics and search for robot log data | — | — |
| ROS Development Studio | The Construct's online ROS development environment | — | — |
| ROSbloX | Docker building blocks for robot software stacks | — | — |
| scale | Data labelling and AI data platform | — | — |
| SEMIO | Software platform for social and service robots | — | — |
| SLAMCore | Commercial visual SLAM and positioning | — | — |
| TANGRAM | Multi-sensor calibration software | — | — |
| Transitive Robotics | Open-core web capabilities for robot fleets | — | — |
| Vinci | AI simulation for hardware design; now getvinci.ai | — | — |
| Windows 10 IoT + ROS | Microsoft's ROS on Windows landing page | — | — |
| balena | Fleet deployment and OTA updates for Linux devices | — | — |
| MENDER | Open-source OTA updates for embedded Linux | — | — |
| Synpse | Device fleet deployment platform; now synpse.com | — | — |
| Awesome HRI Datasets and Human Simulators | List of HRI datasets and human simulators, same author | — | — |
| Awesome Human Robot Interaction | List of HRI libraries and resources | — | — |
| Awesome Projects | jslee02's personal list of software projects | — | — |
| Awesome Robotic Tooling | A Phase 4 source with its own triage note | — | — |
| Awesome Robotics Conferences and Schools | List of robotics conferences and summer schools | — | — |
| Awesome Robotics Libraries | A Phase 4 source with its own triage note | — | — |
| Awesome Robotics (ahundt) | General robotics awesome list | — | — |
| Awesome Robotics (Kiloreux) | A Phase 4 source with its own triage note | — | — |
| Awesome Weekly Robotics | Projects collected through the Weekly Robotics newsletter | — | — |
| awesome-cloud-robotics | List of cloud robotics tools and platforms | — | — |
| (Wannabe) Awesome (Remote) Robot DevEnvs | List of remote and container robot dev environments | — | — |
| Awesome Robotics System Design (and more) | Reading list on robotics system and software design | — | — |
| My curated list of robotics companies (Google Sheet) | The author's spreadsheet of robotics companies | — | — |

## Deferred

| Entry | What it is | Phase |
|---|---|---|
| adafruit | Electronics vendor with tutorials | 5 |

## Rejected

| Entry | Why | Date |
|---|---|---|
| LHF connect | Dead link: the domain now serves a spam page | 2026-11-17 |
| Nguyen Vincent's omnidirectional ROS2 robot | A build video and code, with no CAD, BOM or licence | 2026-11-17 |
| RoboArm | Too thin to build from: a small repo with parts on Thingiverse, dated 2019 | 2026-11-17 |
| facebookresearch/pyrobot | Duplicate of PyRobot | 2026-11-18 |
| resibots/minitaur_sdk | SDK extension for the discontinued Minitaur; proprietary, no commit since 2019 | 2026-11-18 |
| linux_isolate_process | A small script listed with no description; too thin to help a builder | 2026-11-18 |
| Realtime robot data visualization in the browser (Zethus) | Abandoned: no commit since 2020; Foxglove covers browser visualisation | 2026-11-18 |
| Gibson | Superseded by OmniGibson, listed below; its site no longer answers | 2026-11-18 |
| MORSE | Abandoned: no commit since 2022; Gazebo and Webots cover academic simulation | 2026-11-18 |
| Amazon re:MARS | Discontinued: the link redirects to a generic AWS events page | 2026-11-18 |
| BazelCon | A build-tool conference, not robotics | 2026-11-18 |
| COMMA_CON | One company's event about its driver-assistance product | 2026-11-18 |
| CppCon | A general C++ conference, not robotics | 2026-11-18 |
| Airbotics | Dead link: airbotics.io no longer resolves | 2026-11-18 |
| Artificial | Dead link: the server does not respond (Cloudflare 522) | 2026-11-18 |
| Autoware.AI | Duplicate of Autoware above; the link redirects to autoware.org | 2026-11-18 |
| AWS RoboMaker | Discontinued; the link redirects to a generic AWS page | 2026-11-18 |
| FogROS | Deprecated ROS 1 predecessor of FogROS2, as the list says | 2026-11-18 |
| Freedom robotics | Dead link: the site is no longer served | 2026-11-18 |
| KABAM Robotics | Dead link: no response | 2026-11-18 |
| rethink robotics | Dead link: the domain no longer resolves; see [Baxter](../wiki/robots/baxter.md) and [Sawyer](../wiki/robots/sawyer.md) | 2026-11-18 |
| RosHub | The domain now serves an unrelated sneaker shop | 2026-11-18 |
| SOUTHIE AUTONOMY | The domain now redirects to an unrelated site | 2026-11-18 |
| YOU ONLY NEED ONE HUB | Dead link: server error (500) | 2026-11-18 |
| aviator | A Git merge-queue tool, not robotics | 2026-11-18 |
| DevZero | A Kubernetes cost tool, not robotics | 2026-11-18 |
| Miru (Deployment & DevEnv) | Duplicate of miru above | 2026-11-18 |
| Awesome Robot Operating System 2 (ROS 2) | Dead link (404); dropped as a source on 2026-11-18 | 2026-11-18 |
| Awesome HRI Datasets and Human Simulators (self-advertisement) | Duplicate of the same list above | 2026-11-18 |
| Awesome HRI Papers for Industry | Mislinked: points to Awesome Robotics System Design, the next entry | 2026-11-18 |
| awesome-behavioral-change | Not robotics: persuasive-technology papers | 2026-11-18 |
| awesome-end-user-programming | Not robotics: end-user programming links | 2026-11-18 |
| awesome-tech-education | Mostly general coding education, not robotics | 2026-11-18 |
