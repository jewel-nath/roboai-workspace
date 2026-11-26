---
type: source
name: Awesome Robotics
registry: awesome-robotics
url: https://github.com/kiloreux/awesome-robotics
commit: "067f76e"
read_on: 2026-11-18
counts: {entries: 147, pages: 7, waiting: 0, index_only: 107, deferred: 0, rejected: 33}
---

# Awesome Robotics: what it gives RoboAI

A general starter list from 2015: courses, books, a short software list, conferences, journals,
competitions, companies and community links. Most of it is reading and orientation, not things a
builder runs, and much has aged: 13 of its 28 courses are gone or duplicated. Its value to
RoboAI is a handful of core tools (ROS 2, Gazebo, Webots, CoppeliaSim, Drake), two builder
resources (Linorobot and PythonRobotics), and a reading list worth keeping as index rows.

## How it was read

- Read at commit `067f76e` (2024-09-22) on 2026-11-18: the whole README (147 entries in ten
  sections), `CONTRIBUTING.md` and `LICENSE.md` (a permissive "do what you want" notice).
- Every link was requested once on 2026-11-18, following redirects, and failures were tried a
  second time with a longer timeout. Amazon, IEEE Xplore and publisher pages were only checked to
  load.
- Page candidates were checked by a shallow clone of their repo: `gazebosim/gz-sim`
  (2026-11-18, Apache-2.0), `ros2/ros2` (2026-10-20) and `ros2/rclcpp` (2026-11-17, Apache-2.0),
  `CoppeliaRobotics/CoppeliaSimLib` (2026-11-18, GPL-3.0-or-later; the binaries ship under
  Coppelia's free education or paid commercial licence), `cyberbotics/webots` (2026-11-16,
  Apache-2.0), `RobotLocomotion/drake` (2026-11-17, BSD-3-Clause), `linorobot/linorobot2`
  (2026-09-29, Apache-2.0) and `AtsushiSakai/PythonRobotics` (2026-11-10, MIT).
- To decide B or C, MRPT, ViSP, RBDL, YARP, the Robotics Library and Unity Robotics Hub were also
  cloned: all have commits in 2025 or 2026 but serve a niche, so they are index only. Morse,
  Roboschool, ROS-Behavior-Tree and ur5controller were cloned to confirm they are abandoned
  (last commits 2022, 2019, 2018 and 2020).
- **Papers:** the Papers section holds one paper, so it is one index row.
- **Duplicates:** four course rows repeat another course's page or an older run of it.
- **Dead or moved on 2026-11-18:** nine courses return 404 or redirect to a catalogue; ROS 2 docs
  moved from index.ros.org to docs.ros.org; the Webots overview page is 404 (cyberbotics.com
  loads); Correll's book moved to the `Introduction-to-Autonomous-Robots` organisation; Robotics
  for Software Engineers is now Robotics for Programmers; Robotex moved to robotex.international;
  aldebaran.com redirects to Maxtronics; the ISRR and ISER pages on ifrr.org, the RoManSy 2016
  site, rethinkrobotics.com, the ABB link and the Neobotix home page no longer load.
- **Suspicious:** `ijrr.org`, the list's link for IJRR, now redirects to a gambling site, and
  `journalfieldrobotics.org` redirects to an unrelated foundation's site; both journals still
  publish elsewhere. `fetchrobotics.com` redirects to Skild AI, which bought Fetch's assets in
  2026 (see the [Fetch](../wiki/robots/fetch.md) page). The README holds no prompt-like text.
  MRPT's repo carries an `agents.md` with coding rules for its own contributors; it was read as
  data and not followed. Unity Robotics Hub's README now advertises Unity's paid Simulation Pro.
- **Left for Phase 5 (triaged 2026-11-26):** g2core (motion-control firmware).
- **Phase 5 re-triage (2026-11-26):** g2core was partial-cloned from `synthetos/g2` (default
  branch `edge-preview`; 679 stars). Its last commit, 2026-11-15, only links synthetos.com in the
  README; the code is unchanged since 2023-07-20, and the `edge` branch since 2021-11-05. The
  licence is GPL-2.0 with the BeRTOS exception for component files. It is 9-axis motion-control
  firmware for the Arduino Due, aimed first at CNC machines, 3D printers and lasers (its README
  also names robotics); with its code quiet for three years, it is index only.

## Pages made

| Entry | Page | Tier |
|---|---|---|
| ROS2 | [ROS 2](../wiki/tools/ros2.md) | A |
| Gazebo | [Gazebo](../wiki/tools/gazebo.md) | A |
| V-REP | [CoppeliaSim](../wiki/tools/coppeliasim.md) | B |
| Webots | [Webots](../wiki/tools/webots.md) | B |
| Linorobot | [linorobot2](../wiki/software/linorobot2.md) | B |
| PythonRobotics | [PythonRobotics](../wiki/software/pythonrobotics.md) | B |
| Drake | [Drake](../wiki/software/drake.md) | A |

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| Robotics Nanodegree (Udacity) | Paid Udacity robotics software engineer programme | — | — |
| Autonomous Mobile Robots (edX, 2019 run) | ETH Zurich mobile-robotics MOOC | — | — |
| Underactuated Robotics (MIT CSAIL) | MIT course and online text on nonlinear robot control | — | — |
| QUT Robot Academy | Peter Corke's free video lessons on robotics and vision | — | — |
| Robotic vision (QUT) | QUT robotic vision short course, now run on FutureLearn | — | — |
| Introduction to robotics (MIT) | MIT OpenCourseWare robotics course from 2005 | — | — |
| Robotics: Vision Intelligence and Machine Learning (edX) | Penn course on robot perception and learning | — | — |
| Applied robot design (Stanford University) | Stanford CS235 robot design lecture videos | — | — |
| Introduction to Robotics (Stanford University) | Khatib's CS223A lectures on manipulator kinematics and dynamics | — | — |
| Introduction to Mobile Robotics (University of Freiburg) | Freiburg course on localisation, mapping and SLAM (2016) | — | — |
| Columbia Robotics (edX) | Columbia introductory robotics MOOC | — | — |
| Modern Robotics: Mechanics, Planning, and Control (Coursera) | Lynch and Park's Northwestern specialization on mechanics, planning, control | — | — |
| Hello (Real) World with ROS (edX) | TU Delft introduction to ROS | — | — |
| Advanced Robotics (UC Berkeley, 2019) | Abbeel's CS287 course on planning, control and estimation | — | — |
| Self-Driving Cars with Duckietown (edX) | ETH autonomy course built on Duckietown robots | — | — |
| Probabilistic Robotics | Thrun, Burgard and Fox's text on probabilistic localisation and SLAM | — | — |
| Introduction to Autonomous Mobile Robots | Siegwart and Nourbakhsh's mobile-robotics textbook | — | — |
| Springer Handbook of Robotics | Large reference handbook covering all of robotics | — | — |
| Planning Algorithms | LaValle's free motion-planning textbook | — | — |
| A Mathematical Introduction to Robotic Manipulation | Murray, Li and Sastry's screw-theory manipulation text | — | — |
| Robotics, Vision and Control | Corke's robotics and vision text; later editions use Python | — | — |
| Introduction to Autonomous Robots | Correll's open textbook, released as free PDFs | — | — |
| Principles of Robot Motion | Choset et al.'s motion-planning textbook | — | — |
| Introduction to Modern Robotics | Lynch and Park's free textbook behind the Modern Robotics course | — | — |
| Programming Robots with ROS | O'Reilly ROS 1 book from 2015; dated | — | — |
| Learning ROS for Robotics Programming | Packt ROS 1 book from 2015; dated | — | — |
| Mastering ROS for Robotics Programming | Packt ROS book; the linked first edition covers ROS 1 | — | — |
| Behavior Trees in Robotics and AI | Colledanchise and Ögren's free behaviour-tree book | — | — |
| Automated Planning and Acting | Ghallab, Nau and Traverso's AI planning text | — | — |
| Robotics for Software Engineers | Manning book on robot software, renamed Robotics for Programmers | — | — |
| ROS | ROS 1; its last release, Noetic, reached end of life May 2025 | — | — |
| RobWork | SDU's C++ libraries for robot simulation and control | — | — |
| MRPT | C++ mobile-robot library for SLAM, localisation and sensor data | — | — |
| Robotics Library | Self-contained C++ library for kinematics, planning and control | — | — |
| Carmen | CMU mobile-robot navigation toolkit; dormant since 2013 | — | — |
| YARP | Robot middleware used mainly around [iCub](../wiki/robots/icub.md) | — | — |
| The Player Project | Pre-ROS robot device server and Stage 2D simulator; historical | — | — |
| ViSP | Inria's visual-servoing and model-based tracking library | — | — |
| RBDL | C++ rigid-body dynamics library; Pinocchio covers the same ground | — | — |
| Unity Robotics Hub | Unity's ROS integration tutorials, now pointing to paid Simulation Pro | — | — |
| Section: Papers (1 paper) | CMU's optimisation-based Atlas controller for the DRC finals | — | — |
| ACM/IEEE International Conference on Human Robot Interaction (HRI) | Main human-robot interaction conference | — | — |
| CISM IFToMM Symposium on Robot Design, Dynamics and Control (RoManSy) | IFToMM symposium on robot design, dynamics and control | — | — |
| IEEE Conference on Decision and Controls (CDC) | IEEE control conference; robotics is a small part | — | — |
| IEEE International Conference on Rehabilitation Robotics (ICORR) | IEEE rehabilitation robotics conference | — | — |
| IEEE International Conference on Robotics and Automation (ICRA) | IEEE's flagship robotics conference | — | — |
| IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) | Major IEEE/RSJ robotics conference | — | — |
| IEEE-RAS International Conference on Humanoid Robots (Humanoids) | IEEE-RAS humanoid robots conference | — | — |
| International Symposium of Robotic Research (ISRR) | Biennial robotics research symposium run by IFRR | — | — |
| International Symposium of Experimental Robotics (ISER) | Experimental robotics symposium run by IFRR | — | — |
| Robotics: Science and Systems Conference (RSS) | Selective single-track robotics conference | — | — |
| The International Workshop on the Algorithmic Foundations of Robotics (WAFR) | Workshop on the theory of robot algorithms | — | — |
| Autonomous Robots | Springer robotics journal | — | — |
| Bioinspiration & Biomimetics | IOP journal on bio-inspired engineering | — | — |
| Frontiers in Robotics and AI | Open-access robotics and AI journal | — | — |
| IEEE Robotics & Automation Magazine | IEEE Robotics and Automation Society's magazine | — | — |
| IEEE Transactions on Haptics | IEEE journal on haptics | — | — |
| IEEE Transactions on Robotics | IEEE's main robotics journal | — | — |
| IEEE/ASME Transactions on Mechatronics | IEEE/ASME mechatronics journal | — | — |
| International Journal of Social Robotics | Springer social robotics journal | — | — |
| Journal of Field Robotics | Wiley field robotics journal; the list's domain now goes elsewhere | — | — |
| Journal of Intelligent & Robotic Systems | Springer journal on intelligent and robotic systems | — | — |
| Mechatronics | Elsevier mechatronics journal | — | — |
| Robotics and Computer-Integrated Manufacturing | Elsevier journal on industrial and manufacturing robotics | — | — |
| Robotics and Autonomous Systems | Elsevier robotics journal | — | — |
| The International Journal of Robotics Research | SAGE's leading robotics journal; the list's domain is hijacked | — | — |
| DARPA Robotics Challenge | 2012–2015 disaster-response humanoid challenge; ended, site gone | — | — |
| European Robotics Challenges | Finished EU-funded industrial and drone robotics challenge | — | — |
| First Robotics Competition | FIRST high-school robot competition | — | — |
| VEX Robotics Competition | School robot competition on VEX kits | — | — |
| RoboCup | International robot soccer, rescue and home-robot competitions | — | — |
| RoboCupJunior | RoboCup's school-level leagues | — | — |
| Eurobot | European student robot contest | — | — |
| RoboMasters | DJI's university robot combat competition | — | — |
| Intelligent Ground Vehicle Competition | Student autonomous ground-vehicle competition | — | — |
| Robotex | Estonian robotics festival and contest, now at robotex.international | — | — |
| First Lego League | FIRST LEGO robotics league for school children | — | — |
| Boston Dynamics | Company; maker of [Spot](../wiki/robots/boston-dynamics-spot.md) and [Atlas](../wiki/robots/boston-dynamics-atlas.md) | — | — |
| iRobot | Company; maker of the Roomba, which is not in the Atlas | — | — |
| PAL Robotics | Company; maker of [TIAGo](../wiki/robots/tiago.md) and [TALOS](../wiki/robots/pal-talos.md) | — | — |
| Aldebaran Robotics | Company; maker of [NAO](../wiki/robots/nao.md) and [Pepper](../wiki/robots/pepper.md), assets sold in 2025 | — | — |
| ABB Robotics | Company; large industrial-arm maker | — | — |
| KUKA Robotics | Company; industrial-arm maker of the [LBR iiwa](../wiki/robots/kuka-lbr-iiwa.md) | — | — |
| FANUC | Company; industrial-arm maker with a very large installed base | — | — |
| Rethink Robotics | Company, site gone; maker of [Baxter](../wiki/robots/baxter.md) and [Sawyer](../wiki/robots/sawyer.md) | — | — |
| DJI | Company; drone maker, also behind RoboMaster | — | — |
| The construct sim | Company; online ROS courses and cloud simulation, now The Construct | — | — |
| Fetch Robotics | Company; maker of [Fetch](../wiki/robots/fetch.md), its domain now redirects to Skild AI | — | — |
| Festo Robotics | Company; automation maker known for animal-inspired demonstration robots | — | — |
| Neobotix | Company; German maker of industrial and research mobile robots | — | — |
| IEEE Spectrum Robotics | Robotics news section of IEEE Spectrum | — | — |
| MIT Technology Review Robotics | Robotics news section of MIT Technology Review | — | — |
| reddit robotics subreddit | General robotics forum on Reddit | — | — |
| RosCON conference (video talks included) | Yearly ROS developer conference, talk videos online | — | — |
| Carnegie Mellon Robotics Academy | CMU's school robotics curricula for VEX and LEGO | — | — |
| StackExchange Robotics community | Robotics Q&A site; ROS Answers moved here in 2023 | — | — |
| Hexapod Robot Simulator | Browser tool for hexapod inverse kinematics and gaits | — | — |
| Awesome Artificial Intelligence | General AI resource list, not robotics | — | — |
| Awesome Computer Vision | Computer vision resource list | — | — |
| Awesome Machine Learning | Machine learning libraries by language | — | — |
| Awesome Deep Learning | Deep learning resource list | — | — |
| Awesome Deep Vision | Deep-learning computer vision paper list | — | — |
| Awesome Reinforcement Learning | Reinforcement learning resource list | — | — |
| Awesome Robotics (ahundt) | Another general robotics list, research-leaning | — | — |
| Awesome Robotics Libraries | A Phase 4 source with its own triage note | — | — |
| Awesome RoboCupJunior Soccer | Resources for RoboCupJunior Soccer teams | — | — |
| g2core | Motion-control firmware for CNC machines, 3D printers, lasers and robots on the Arduino Due; code quiet since July 2023 | 2026-11-15 | GPL-2.0 with BeRTOS exception |

## Deferred

| Entry | What it is | Phase |
|---|---|---|

## Rejected

| Entry | Why | Date |
|---|---|---|
| Artificial Intelligence for Robotics (Udacity) | Dead link: the course page now redirects to Udacity's catalogue | 2026-11-18 |
| Autonomous Mobile Robots (edX, 2014 run) | Duplicate of the 2019 run above; this page returns 404 | 2026-11-18 |
| Robot Mechanics and Control, Part I (edX) | Dead link: the edX course returns 404 | 2026-11-18 |
| Robot Mechanics and Control, Part II (edX) | Dead link: the edX course returns 404 | 2026-11-18 |
| Autonomous Navigation for Flying Robots (edX) | Dead link: the edX course returns 404 | 2026-11-18 |
| Robotics Specialization by GRASP Lab (Coursera) | Dead link: the Coursera specialization returns 404 | 2026-11-18 |
| Control of Mobile Robots (Coursera) | Dead link: the course page now redirects to Coursera's catalogue | 2026-11-18 |
| Robotics (edX MicroMasters) | Dead link: the MicroMasters programme returns 404 | 2026-11-18 |
| Building Arduino robots and devices (Coursera) | Dead link: the Coursera course returns 404 | 2026-11-18 |
| Introduction to The Robot Operating System (ROS2) (Coursera) | Dead link: the Coursera project returns 404 | 2026-11-18 |
| Modern Robotics: Mechanics, Planning, and Control Specialization (Coursera) | Duplicate of Modern Robotics above: the same page | 2026-11-18 |
| Become a Robotics Software Engineer (Udacity) | Duplicate of Robotics Nanodegree above: the same page | 2026-11-18 |
| Advanced Robotics (UC Berkeley, 2013) | Duplicate: the 2013 run of CS287, listed above for 2019 | 2026-11-18 |
| A gentle introduction to ROS | Dead link (404), and the book covers ROS 1 only | 2026-11-18 |
| Learning Computing With Robots | Dead link: the wiki returns HTTP 500 | 2026-11-18 |
| INTECH Books | Dead link: IntechOpen's robotics subject page returns 404 | 2026-11-18 |
| Simbad | Abandoned: a Java simulator last updated on SourceForge in 2013 | 2026-11-18 |
| Morse | Dead link; its authors stopped maintaining MORSE in 2020 and it needs Blender 2.79b | 2026-11-18 |
| Peekabot | Dead link: peekabot.org no longer resolves, and the tool is abandoned | 2026-11-18 |
| Neurorobotics Platform (NRP) | Dead link: neurorobotics.net does not answer; it was a Human Brain Project service | 2026-11-18 |
| Open AI's Roboschool | Archived by OpenAI in 2019 and deprecated in favour of PyBullet | 2026-11-18 |
| ROS Behavior Trees | Abandoned in 2018; superseded by BehaviorTree.CPP | 2026-11-18 |
| ur5controller | Abandoned in 2020: an OpenRAVE controller for one arm model | 2026-11-18 |
| Robotica | Dead link: the IEEE RAS page is gone and the list does not say which event it means | 2026-11-18 |
| ICRA Robot Challenges | Dead link: the ICRA 2017 site no longer resolves | 2026-11-18 |
| RobotChallenge | Dead link: robotchallenge.org does not answer, and no current edition was found | 2026-11-18 |
| RoboSoft, Grand Challenge | Dead link: robosoftca.eu does not answer; a past one-off contest | 2026-11-18 |
| Let's Make Robots | The community is gone; its domain redirects to a RobotShop forum page | 2026-11-18 |
| How do I learn Robotics? | A Quora thread; too thin to help a builder | 2026-11-18 |
| Free NXT Lego MindStorms NXT-G code tutorials | Obsolete: tutorials for LEGO's retired NXT-G software | 2026-11-18 |
| 47 Programmable robotic kits | A dated listicle of kits; too thin to help a builder | 2026-11-18 |
| Awesome Gazebo | Dead link: the repo returns 404 | 2026-11-18 |
| Awesome ROS2 | Dead link: the repo returns 404, as the plan's 2026-11-18 decision notes | 2026-11-18 |
