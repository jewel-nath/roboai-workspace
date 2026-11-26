---
type: source
name: Awesome Mobile Robotics
registry: awesome-mobile-robotics
url: https://github.com/mathiasmantelli/awesome-mobile-robotics
commit: "03a0871"
read_on: 2026-11-18
counts: {entries: 533, pages: 23, waiting: 0, index_only: 441, deferred: 0, rejected: 69}
---

# Awesome Mobile Robotics: what it gives RoboAI

A personal list of mobile-robotics material: courses, books, datasets, software, podcasts,
conferences, journals, companies, labs and a Misc section. Its value for a builder sits in the
software section, which names most of the core open stack (ROS 2, Nav2, SLAM Toolbox, MoveIt,
Gazebo, Webots, Isaac Sim, GTSAM, Docker) next to a long tail of research SLAM, mapping and
planning code, and in the classic SLAM benchmarks among its datasets. The courses, books,
companies and labs are index material, and the end of Misc is off-topic writing, slide and AI
tools. 23 of 533 entries earn a page.

## How it was read

- Read at commit `03a0871` (2026-08-03) on 2026-11-18: the README in full, 533 linked entries in
  ten sections (Courses 113, Books 24, Datasets 54, Softwares and Libraries 179, Podcasts 7,
  Conferences 11, Journals 10, Companies and Jobs 73, Laboratories and Research Groups 21, Misc
  41). The repo has no other list files and no licence file. No section holds only papers; the one
  paper link (Augmented LiDAR Simulator) and the paper lists have their own rows.
- Each page candidate's own repo was shallow-cloned for its last commit and licence file:
  ros2/ros2 2026-10-20 (rclcpp Apache-2.0); gz-sim 2026-11-18, Apache-2.0; CoppeliaSimLib
  2026-11-18, GPL-3.0-or-later (the CoppeliaSim app has its own edu and paid licences); Webots
  2026-11-16, Apache-2.0; Drake 2026-11-17, BSD-3-Clause; moby 2026-11-18, Apache-2.0;
  navigation2 2026-11-17, Apache-2.0, BSD-3-Clause and LGPL-2.1-or-later by package;
  rosbridge_suite 2026-11-04, BSD-3-Clause; IsaacSim 2026-11-16, Apache-2.0; GTSAM 2026-11-18,
  BSD-3-Clause; robosuite 2026-07-11, MIT; moveit2 2026-11-17, BSD-3-Clause; slam_toolbox
  2026-11-02, LGPL-2.1; PythonRobotics 2026-11-10, MIT; OctoMap 2026-09-26, BSD-3-Clause
  (octovis GPL-2.0); LIO-SAM 2023-04-17, BSD-3-Clause; open_vins 2025-11-30, GPL-3.0;
  BehaviorTree.CPP 2026-11-13, MIT; robotics-toolbox-python 2026-11-18, MIT; ORB_SLAM2
  2017-10-10 and ORB_SLAM3 2022-02-10, both GPL-3.0; segment-anything 2024-09-18 and sam2
  2024-12-15 under Apache-2.0, sam3 2026-11-17 under Meta's own SAM License. KITTI (CC
  BY-NC-SA 3.0) and TUM RGB-D (CC BY 4.0) were checked on their websites.
- Some entries link a predecessor or a companion of the project that earns the page: ROS goes to
  ROS 2, the ROS 1 MoveIt repo to MoveIt 2, V-REP to CoppeliaSim, ORB-SLAM2 to ORB-SLAM3,
  RobotWebTools to rosbridge, and Groot 2 (a closed-source editor with a free tier) to
  BehaviorTree.CPP. OpenCV appears only as two install guides for Ubuntu 16.04 and 18.04, which
  are rejected; OpenCV itself comes from other lists.
- Courses, books, podcasts, conferences, journals, companies and labs are index only. Parts and
  sensor vendors and one trajectory-optimisation repo are deferred to Phase 5 (triaged
  2026-11-26). Twenty entries are duplicates within the list.
- Dead or moved on 2026-11-18: cpp.bw.org, peekabot.org, the MORSE site and the Neurorobotics
  Platform's bare IP address no longer load; paperswithcode.com redirects to Hugging Face Papers;
  the "Robótica Educacional" entry links donkeycar.com, which now redirects to diyrobocars.com;
  the TUM dataset moved to cvg.cit.tum.de. Several company links point to new owners (Vicarious
  to Intrinsic, Lyft Level 5 to Woven by Toyota).
- Suspicious content: no prompt-like text. The TutorialSearch entry in Courses and the run of
  generic AI, video, website and SEO tools at the end of Misc read like advertisements. Eleven
  links carry a `__s=` tracking parameter and two Amazon links carry affiliate tags. The README
  gives the author's email address; it is not copied here.
- **Phase 5 re-triage (2026-11-26):** the four rows deferred to Phase 5 were checked at their
  links; the entries read the same at the list's newer head, `2c4381c` (2026-11-24).
  `mayataka/mini_pupper_trajopt` was partial-cloned: last commit 2022-01-02, Apache-2.0, about 40
  stars. The three company sites were read by HTTP request: Soft Robotics says it sold its mGrip
  gripper business to the Schmalz Group in August 2024 and now presents itself as Oxipital AI
  (vision inspection); AutonomouStuff still lists drive-by-wire and sensor products; Zivid sells
  the Zivid 2+ and Zivid 3 cameras and keeps `zivid-ros` (2026-09-16, BSD-3-Clause). No Atlas
  robot uses any of them, so the three companies are index only and the Mini Pupper repo is
  rejected.

## Pages made

| Entry | Page | Tier |
|---|---|---|
| Robot Operating System (ROS) | [ROS 2](../wiki/tools/ros2.md) | A |
| RobotWebTools | [rosbridge_suite](../wiki/software/rosbridge-suite.md) | B |
| Gazebo | [Gazebo](../wiki/tools/gazebo.md) | A |
| V-REP | [CoppeliaSim](../wiki/tools/coppeliasim.md) | B |
| Webots | [Webots](../wiki/tools/webots.md) | B |
| NVidia Isaac Sim | [Isaac Sim](../wiki/tools/isaac-sim.md) | A |
| KITTI Vision Benchmark Suite | [KITTI and KITTI-360](../wiki/learning/datasets/kitti.md) | B |
| TUM Dataset | [TUM RGB-D](../wiki/learning/datasets/tum-rgbd.md) | B |
| ORB-SLAM2 | [ORB-SLAM3](../wiki/software/orb-slam3.md) | B |
| GTSAM | [GTSAM](../wiki/software/gtsam.md) | A |
| SLAM Toolbox | [SLAM Toolbox](../wiki/software/slam-toolbox.md) | A |
| OctoMap | [OctoMap](../wiki/software/octomap.md) | B |
| LIO-SAM | [LIO-SAM](../wiki/software/lio-sam.md) | B |
| OpenVINS | [OpenVINS](../wiki/software/openvins.md) | B |
| Segment Anything | [Segment Anything (SAM, SAM 2, SAM 3)](../wiki/learning/models/segment-anything.md) | B |
| ROS 2 Navigation | [Nav2](../wiki/software/nav2.md) | A |
| PythonRobotics | [PythonRobotics](../wiki/software/pythonrobotics.md) | B |
| Groot 2 | [BehaviorTree.CPP](../wiki/software/behaviortree-cpp.md) | A |
| Drake | [Drake](../wiki/software/drake.md) | A |
| MoveIt | [MoveIt 2](../wiki/software/moveit2.md) | A |
| Robotics Toolbox for Python | [Robotics Toolbox for Python](../wiki/software/robotics-toolbox-python.md) | B |
| Docker | [Docker](../wiki/tools/docker.md) | B |
| robosuite | [robosuite](../wiki/learning/frameworks/robosuite.md) | A |

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| Mobile Sensing and Robotics | Cyrill Stachniss's video course on mobile sensing and robotics | — | — |
| Mobile Sensing and Robotics - 2 | Second part of Stachniss's mobile sensing video course | — | — |
| Photogrametry | Stachniss's photogrammetry video lectures | — | — |
| SLAM | Stachniss's SLAM video lectures | — | — |
| Modern C++ | Stachniss's modern C++ course for robotics students | — | — |
| Become a Robotics Software Engineer | Udacity robotics software engineer video playlist | — | — |
| Different playlists about ROS | The Construct's ROS video playlists | — | — |
| A platform to learn/teach robotics from zero | The Construct's paid online ROS learning platform | — | — |
| Autonomous Systems | Udacity's paid autonomous systems programmes | — | — |
| Artificial Intelligence for Robotics | Thrun's Udacity course on localisation, filters and planning | — | — |
| Slides of Computer Vision | Cornell computer vision lecture slides from 2013 | — | — |
| Computer Vision: Foundations and Applications | Stanford CS131 computer vision course, 2014 | — | — |
| Interval Analysis | MOOC on interval methods, applied to robot localisation | — | — |
| Robot Mapping | Freiburg robot mapping course, 2013 | — | — |
| JAI: Robótica e Simulação com o V-REP | Portuguese 2015 short course on V-REP simulation | — | — |
| Digital Image Processing | University of Tartu image processing course | — | — |
| Tutorial on Visual Odometry | Scaramuzza's visual odometry tutorial and slides | — | — |
| Visual SLAM Tutorial | CVPR 2014 visual SLAM tutorial by Dellaert and Kaess | — | — |
| Visual Odometry from scratch - A tutorial for beginners | Blog tutorial on monocular visual odometry | — | — |
| Aerial Robot Courses | Kostas Alexis's aerial robotics course pages | — | — |
| Stereo Vision Tutorial | Blog tutorial on stereo vision, 2014 | — | — |
| Introduction to Mobile Robotics | Burgard's Freiburg mobile robotics course | — | — |
| GaiTech EDU | ROS tutorial website by Gaitech | — | — |
| Robocademy | Lentin Joseph's paid ROS courses | — | — |
| Hello (Real) World with ROS | TU Delft ROS course on edX | — | — |
| Self-Driving Cars with ROS and Autoware | Autoware Foundation course on ROS 2 and Autoware.Auto | — | — |
| Programming for Robotics - ROS | ETH Zurich ROS course slides and exercises | — | — |
| Think Autonomous | Paid self-driving and computer vision courses | — | — |
| PyImageSearch | Computer vision and deep learning tutorial blog | — | — |
| DuckieTown | Robot; not in the Atlas: Duckietown teaching robots and course | — | — |
| Machine Learning | Andrew Ng's Coursera machine learning course | — | — |
| Deep Learning Specialization | Andrew Ng's Coursera deep learning courses | — | — |
| OpenCV: C++ and Python | Code for the LearnOpenCV computer vision tutorials | — | — |
| Awesome Self-Driving | Awesome list on self-driving cars | — | — |
| Principles of Computer Vision | Shree Nayar's computer vision lecture series | — | — |
| Awesome Computer Vision | Awesome list on computer vision | — | — |
| Introduction to ROS: The Robot Operating System | Paid introductory ROS course | — | — |
| ROS Tutorials | ROS 1 tutorials from Erle Robotics' drone docs | — | — |
| ROS Industrial Training | ROS-Industrial training exercises, ROS 1 Melodic edition | — | — |
| ROS C++ Hello World | Short roscpp hello-world article | — | — |
| ROS2 C++ Hello World | Short rclcpp hello-world article | — | — |
| Programming for Robotics | Michigan ROB 599 robot programming course, 2019 | — | — |
| Mathematics for Robotics | Michigan ROB 501 mathematics for robotics course | — | — |
| Introduction to the A* Algorithm | Interactive A* pathfinding explainer | — | — |
| Computer Science courses with video lectures | Index of computer science video courses | — | — |
| Common Path Planning Algorithms | Small repo of path planning algorithm samples | — | — |
| PyVisualOdometry | Python visual odometry sample code | — | — |
| KITTI Odometry in Python and OpenCV | Notebook doing visual odometry on KITTI | — | — |
| Awesome 3D Reconstruction List | Awesome list on 3D reconstruction | — | — |
| ROS Autonomous Driving and Path Planning SLAM with TurtleBot3 | Course code for TurtleBot3 driving, SLAM and planning | — | — |
| ROS2 Ultimate learners Repository with Supporting Documentation | ROS 2 course code and notes | — | — |
| ROS2 C++ learning | ROS 2 C++ example nodes | — | — |
| F1TENTH | Robot; on the [F1TENTH (RoboRacer)](../wiki/robots/f1tenth.md) page | — | — |
| ROS Book Sample Code | Code for the book Programming Robots with ROS | — | — |
| CPP Best Practices | Collaborative C++ best-practice guide | — | — |
| C++ Cheatsheet | Modern C++ cheatsheet | — | — |
| Computer Vision | York University computer vision course | — | — |
| Machine Learning Course Notes | DAIR.AI notes on machine learning lectures | — | — |
| Data Structure & Algorithms 101 | Illustrated notes on data structures and algorithms | — | — |
| Trending in 3D Vision | Paper list on 3D vision | — | — |
| Udacity's autonomous car | Archived code of Udacity's open self-driving car project | — | — |
| Muhammad Luqman | YouTube channel with ROS tutorials | — | — |
| Hummingbird | YouTube channel about working in robotics | — | — |
| ROS Tutorials by CLEARPATH | Clearpath's ROS 1 Melodic tutorials | — | — |
| Roboflow Notebooks | Computer vision model training notebooks | — | — |
| Autonomous Driving Lecture | Autonomous driving lecture materials | — | — |
| C++ Optimizations Diary | Davide Faconti's C++ performance tips | — | — |
| Visual SLAM Roadmap | Study roadmap for visual SLAM developers | — | — |
| Official Repository RVSS | Robotic Vision Summer School Colab notebooks | — | — |
| KF in Python | Kalman filter examples in Python | — | — |
| Self Driving Cars | Notes and code for Toronto's self-driving car courses | — | — |
| Coding Notes and Tutorials | methylDragon's notes on languages and frameworks | — | — |
| Introduction to Robotics | Princeton introductory robotics course | — | — |
| Michigan Robotics | Michigan Robotics free online courses | — | — |
| Sensor Fusion Tutorial | Tutorial on fusing sensors with robot_localization | — | — |
| Rosetta Launch | Side-by-side guide to ROS 1 and ROS 2 launch files | — | — |
| Open-Source ROS Projects | Blog list of open-source ROS projects | — | — |
| Autonomous Vehicle Control Beginners Guide | Python samples of vehicle control and planning | — | — |
| Awesome Robotic Tooling | Awesome list; triaged separately in Phase 4 | — | — |
| Awesome Robotics | Awesome list; triaged separately in Phase 4 | — | — |
| Awesome Papers of Autonomous Driving | Paper list on autonomous driving | — | — |
| Pigeon ROS Tutorial | Small ROS tutorial code repo | — | — |
| Introduction to Robotics and Perception | Online robotics and perception textbook with runnable notebooks | — | — |
| Start Machine Learning | Guide to learning machine learning | — | — |
| Python course | Code for a beginner Python and ML course | — | — |
| C++ for Beginners | Code for a beginner C++ course | — | — |
| Advanced C++ | Code for an advanced C++ course | — | — |
| JPL Open Source Rover Project | Robot; on the [JPL Open Source Rover](../wiki/robots/jpl-open-source-rover.md) page | — | — |
| F1TENTH - Course Documentation | Robot; on the [F1TENTH (RoboRacer)](../wiki/robots/f1tenth.md) page; this is its course kit | — | — |
| Modern C++ Programming | Free modern C++ course slides, C++11 to C++20 | — | — |
| Modern Robotics Course | Course lessons following the Modern Robotics textbook | — | — |
| ROS 2 Best Practices | Personal notes on ROS 2 coding practice | — | — |
| Advanced Robotics at UC Berkeley | Pieter Abbeel's advanced robotics lectures | — | — |
| Robotics 2 at Sapienza University of Rome | Alessandro De Luca's robot control lectures | — | — |
| Awesome Weekly Robotics | Links collected by the Weekly Robotics newsletter | — | — |
| Mobile Sensing and Robotics - 2020/21 | A student's exercise solutions for Stachniss's course | — | — |
| Machine Learning Engineering | Open book on training large ML models | — | — |
| SLAM Resources for Beginners | Curated SLAM learning resources | — | — |
| Computer Vision: Algorithms and Applications | Szeliski's computer vision textbook, free online | — | — |
| Probabilistic Robotics | Classic textbook on probabilistic localisation, mapping and filtering | — | — |
| Handbook of Robotics | Springer Handbook of Robotics reference work | — | — |
| Introduction to Autonomous Mobile Robots (Intelligent Robotics and Autonomous Agents series) | Siegwart, Nourbakhsh and Scaramuzza's mobile robotics textbook | — | — |
| Planning Algorithm | LaValle's motion planning textbook, free online | — | — |
| A Gentle Introduction to ROS | Free introductory ROS 1 book | — | — |
| Robotics, Vision and Control: Fundamental Algorithms in MATLAB | Corke's robotics textbook, MATLAB edition | — | — |
| Introduction to Autonomous Robots | Correll's open textbook on autonomous robots | — | — |
| Principles of Robot Motion: Theory, Algorithms, and Implementations | Textbook on motion planning algorithms | — | — |
| Modern Robotics: Mechanics, Planning, and Control | Lynch and Park's textbook on kinematics, dynamics and control | — | — |
| Learning ROS for Robotics Programming | ROS 1 programming book | — | — |
| Mastering ROS for Robotics Programming | Lentin Joseph's ROS book | — | — |
| Robótica Móvel | Portuguese mobile robotics textbook | — | — |
| Computational Principles of Mobile Robotics | Dudek and Jenkin's mobile robotics textbook | — | — |
| Visual Navigation for Autonomous Vehicles | MIT VNAV course notes on visual navigation | — | — |
| Think C++ | Free beginner C++ book from 1999 | — | — |
| A Concise Introduction to Robot Programming with ROS2 | Book and code on ROS 2 programming | — | — |
| Robotics, Vision & Control: 3rd edition in Python | Code for Corke's textbook, Python edition | — | — |
| SLAM Book | Gao Xiang's visual SLAM book, English translation | — | — |
| Modern C++ for Absolute Beginners: A Friendly Introduction to the C++ Programming Language and C++11 to C++23 Standards | Beginner book on modern C++ | — | — |
| Modern Software Engineering: Doing What Works to Build Better Software Faster | Book on software engineering practice | — | — |
| Clean Code: A Handbook of Agile Software Craftsmanship | Book on writing readable code | — | — |
| Robotics for Programmers | Manning book on robotics for software developers | — | — |
| Stereo Dataset with ground truth | Middlebury 2006 stereo images with ground truth | — | — |
| Databases or Datasets for Computer Vision Applications and Testing | Large index of computer vision datasets | — | — |
| Robot@Home | Indoor RGB-D and laser dataset from a mobile robot | — | — |
| UAV Dataset - AdM | Small UAV image dataset from UFRGS | — | — |
| UAV Dataset - POA | Small UAV image dataset from UFRGS | — | — |
| SemanticKITTI | Semantic labels for KITTI lidar scans | — | — |
| CLEARPATH Simulation Environments | Clearpath's Gazebo Classic worlds for ROS 1 | — | — |
| FinnForest | Forest dataset for visual SLAM | — | — |
| Ford Autonomous Vehicles Dataset | Multi-season driving dataset from Ford | — | — |
| ENAV planetary Dataset | Planetary-analogue rover navigation dataset | — | — |
| Udacity Self-Driving Car | Driving data from Udacity's archived car project | — | — |
| Long-term Visual Localization | Benchmark for 6-DoF visual localisation across conditions | — | — |
| Waymo Open Dataset | Large driving perception and motion dataset | — | — |
| ASTYX HiReS2019 | Small automotive radar dataset | — | — |
| Berkeley DeepDrive (BDD) | BDD100K driving video dataset | — | — |
| nuScenes | Driving dataset with a full sensor suite | — | — |
| BARN Dataset | Benchmark worlds for navigation in cluttered spaces | — | — |
| RELLIS-3D | Off-road lidar and camera dataset with labels | — | — |
| Gazebo Models and Worlds collection | Collected Gazebo Classic models and worlds | — | — |
| Gazebo models | Legacy Gazebo Classic model database | — | — |
| NASA 3D models | NASA 3D models and textures | — | — |
| Audi Autonomous Driving Dataset (A2D2) | Audi driving dataset with lidar and labels | — | — |
| Oxford Road Boundaries Dataset | Road-boundary detection dataset | — | — |
| SLAM Datasets | Awesome list of SLAM datasets | — | — |
| The Hilti SLAM-Challenge | SLAM challenge rosbags from construction sites | — | — |
| Omnidata | Pipeline for vision datasets made from 3D scans | — | — |
| Mix3D | Data augmentation method for 3D scene segmentation | — | — |
| Large Scale dataset for indoor localization | Indoor visual localisation dataset with ground truth | — | — |
| nuReality | VR scenes for pedestrian and vehicle interaction studies | — | — |
| Blend Swap | Community Blender models | — | — |
| ARKitScenes | Apple's indoor RGB-D scene dataset | — | — |
| SEMFIRE | Forest dataset with multispectral, lidar and thermal data | — | — |
| MOTSynth | Synthetic pedestrian detection and tracking dataset | — | — |
| NeBula | Subterranean odometry dataset from JPL's NeBula team | — | — |
| ALITA | Long-term place recognition dataset | — | — |
| Argoverse 2 | Driving dataset and API | — | — |
| Habitat Matterport 3D Semantics Dataset | Semantically labelled 3D indoor scans for embodied AI | — | — |
| 3D Object Detection for Autonomous Driving | Paper list on 3D object detection for driving | — | — |
| Laser Line Extraction | ROS 1 package that fits lines to laser scans | — | — |
| Ground-Challenge | Ground-robot SLAM dataset with sensor failures | — | — |
| LIDAR-CS | Cross-sensor lidar perception dataset | — | — |
| Awesome LIDAR | Awesome list on lidar sensors, datasets and tools | — | — |
| Awesome RGB-D Datasets | Survey list of RGB-D datasets | — | — |
| LINS -- LiDAR-inertial-SLAM | Lidar-inertial odometry with an iterated Kalman filter | — | — |
| OpenScene | 3D occupancy prediction benchmark for driving | — | — |
| Awesome 3D LiDAR Datasets | List of public 3D lidar datasets | — | — |
| CritrusFarm Dataset | Multimodal citrus-farm dataset for localisation and mapping | — | — |
| Terrasentia Dataset | Agricultural dataset for visual localisation and mapping | — | — |
| Awesome Robotics Dataset | Awesome list; triaged separately in Phase 4 | — | — |
| ORB-SLAM | First, monocular ORB-SLAM; superseded by ORB-SLAM2 and 3 | — | — |
| ORB-SLAM2 Point Cloud | ORB-SLAM2 fork that builds a point-cloud map | — | — |
| ORB-SLAM2 Save/Load Map | ORB-SLAM2 fork that saves and loads maps | — | — |
| DS-SLAM | Semantic SLAM for dynamic scenes, research code | — | — |
| RobWork | C++ libraries for robot simulation and control from SDU | — | — |
| MRPT | C++ mobile-robotics library for SLAM, localisation and planning | — | — |
| Robotics Library | C++ library for kinematics, planning and control | — | — |
| Carmen | CMU mobile-robot toolkit; historical, inactive | — | — |
| FusionCore | Small new ROS 2 UKF for GPS, IMU and odometry fusion | — | — |
| YARP | IIT robot middleware, used mainly on iCub | — | — |
| The Player Project | Player/Stage robot server and 2D simulator; historical | — | — |
| AirSim | Microsoft's Unreal-based drone and car simulator; development ended | — | — |
| Bonnet | Semantic segmentation training and deployment framework, 2019 | — | — |
| Summit | CARLA-based simulator for dense urban traffic | — | — |
| CyPhyHouse | Research toolchain for programming distributed mobile robots | — | — |
| Assistive Gym | Simulation for physical human-robot assistance tasks | — | — |
| Augmented LiDAR Simulator for Autonomous Driving | Paper: augments real lidar scans with synthetic objects | — | — |
| LIRS World Construction Tool (LIRS-WCT) | Builds Gazebo worlds from 2D images or laser scans | — | — |
| Segments.ai | Commercial 2D and 3D data labelling platform | — | — |
| GBPlanner | Graph-based exploration planner from DARPA SubT work | — | — |
| MBPlanner | Motion-primitive exploration planner for aerial robots | — | — |
| SalsaNext | Lidar point-cloud semantic segmentation network | — | — |
| ROS Navigation Stack | ROS 1 navigation stack (move_base); Nav2 replaces it | — | — |
| Deep Drone Acrobatics | Learned control policies for drone acrobatics, research code | — | — |
| atlatec | Company making HD maps for driving | — | — |
| EGO-Planner | Lightweight quadrotor local planner, research code | — | — |
| Event-based Asynchronous Sparse CNNs | Converts event-camera CNNs to sparse asynchronous models | — | — |
| OpenBot | Robot; on the [OpenBot](../wiki/robots/openbot.md) page | — | — |
| SkiROS | Skill-based behaviour-tree framework for ROS | — | — |
| OpenStreetMap | Open world map data, used for outdoor route planning | — | — |
| Flightmare | Quadrotor simulator from UZH RPG | — | — |
| Hierarchical Localization toolbox - HLOC | Toolbox for 6-DoF visual localisation with learned features | — | — |
| ICP | Notebook explaining ICP variants | — | — |
| iSAM | Older incremental SLAM solver; GTSAM's iSAM2 supersedes it | — | — |
| Bag of Visual Words | Notebook explaining bag of visual words | — | — |
| Small projects to clarify big concepts | Notebooks explaining vision and robotics concepts | — | — |
| 3DWarehouse | SketchUp 3D model library | — | — |
| 3DGEMS | Gazebo model collection from York University | — | — |
| GMMLoc | Visual localisation in dense maps, research code | — | — |
| ROS Robots | Showcase site of robots that run ROS | — | — |
| Apollo | Baidu's autonomous-driving software platform | — | — |
| hdcp_planning | Hex-decomposed coverage planning, research code | — | — |
| BALM | Bundle adjustment for lidar mapping | — | — |
| STDyn-SLAM | Stereo semantic SLAM for dynamic outdoor scenes | — | — |
| Learning to drive smoothly | SAC and VAE driving demo in the Donkey Car simulator | — | — |
| Fast-Planner | Quadrotor fast-flight planner, research code | — | — |
| GradSLAM | Differentiable dense SLAM framework, research code | — | — |
| MATLABRobotics | MATLAB samples of navigation algorithms | — | — |
| Data Science & Machine Learning | Personal notes on data science and ML | — | — |
| SSL_SLAM2 | Lidar SLAM for solid-state lidar, research code | — | — |
| Lane Detection | Awesome list on lane detection | — | — |
| Crowd-SLAM | Visual SLAM for crowded scenes, research code | — | — |
| Awesome Robotics Libraries | Awesome list; triaged separately in Phase 4 | — | — |
| EVO: Event-based Visual Odometry | Event-camera visual odometry, research code | — | — |
| ROSshow | Shows ROS topics as terminal graphics | — | — |
| ROSboard | Web dashboard node for viewing ROS topics | — | — |
| ViMantic | Unity-based semantic mapping architecture for robots | — | — |
| openpilot | comma.ai's driver-assistance software for cars | — | — |
| SLAM Research | List of SLAM papers since 2018 | — | — |
| SC-LeGO-LOAM | LeGO-LOAM with Scan Context loop closure | — | — |
| LidarView | Kitware's lidar recording and visualisation app | — | — |
| UFOMap | Octree 3D mapping with explicit unknown space | — | — |
| Treexy | Compact sparse voxel grid library, later renamed Bonxai | — | — |
| SVO Pro | Semi-direct visual(-inertial) odometry from UZH RPG | — | — |
| OpenDR Project | EU-funded deep-learning toolkit for robot perception and control | — | — |
| DiSCo-SLAM | Distributed multi-robot lidar SLAM, research code | — | — |
| Extended-Object-Detection-ROS | ROS object detection package with classic methods | — | — |
| YoloV4-For-Darknet-ROS | YOLOv4 port of darknet_ros for ROS 1 | — | — |
| Face Recognition | Python face recognition library built on dlib | — | — |
| Urban Road Filter | Lidar road and sidewalk detection for ROS | — | — |
| Darknet ROS 3D | Adds 3D boxes to darknet_ros detections using depth | — | — |
| Pedestrian Simulator | ROS social-force pedestrian simulator (pedsim_ros) | — | — |
| SPENCER | ROS 1 people detection and tracking framework | — | — |
| Fiducials | ROS 1 SLAM with ceiling fiducial markers | — | — |
| Mini Pupper | Robot; not in the Atlas | — | — |
| E2ES | End-to-end UAV simulation for SLAM and navigation | — | — |
| SLAM Dynamic | Semantic visual SLAM for dynamic scenes, on Gitee | — | — |
| ABot | Robot; not in the Atlas | — | — |
| KR Autonomous Flight | Kumar Lab's GPS-denied quadrotor autonomy stack | — | — |
| Clober | Robot; not in the Atlas | — | — |
| Robot-Centric Elevation Mapping | ANYbotics elevation mapping for rough terrain, ROS 1 | — | — |
| Terrain Mapping | Neural network fills occlusions in terrain maps | — | — |
| GPS Waypoint Based Autonomous Navigation in ROS | ROS 1 GPS waypoint navigation example | — | — |
| NICE-SLAM | Neural implicit dense SLAM, research code | — | — |
| SOLD2 | Learned line detection and description | — | — |
| FAR Planner | Visibility-graph route planner for known and unknown spaces | — | — |
| Track, Check, Repeat: An EM Approach to Unsupervised Tracking | Unsupervised tracking method, research code | — | — |
| Maps with Semantic and Contextual Object Information | Code for a 2020 semantic object mapping paper | — | — |
| LIO SAM 6AXIS | LIO-SAM fork for 6-axis IMUs and GNSS | — | — |
| Awesome YOLO Ojbect Detection | Awesome list of YOLO projects | — | — |
| Prometheus | Open autonomous drone software platform from Amov Lab | — | — |
| Virtual Costmap Layer | ROS 1 costmap layer for virtual obstacles and zones | — | — |
| ROS2 Path Planning and Maze Solving | ROS 2 maze-solving course project | — | — |
| ROS Best Practices | ETH legged robotics ROS 1 conventions | — | — |
| ROS Noetic Tutorials | Official ROS 1 roscpp tutorials | — | — |
| MSCKF_VIO | Stereo MSCKF visual-inertial odometry, ROS 1 | — | — |
| OSSDC-SIM | Autonomous vehicle simulator based on LGSVL | — | — |
| POLYSCOPE | C++ and Python viewer for meshes and point clouds | — | — |
| Planar Recon | Plane detection and reconstruction from monocular video | — | — |
| LOCUS | Multi-sensor lidar odometry from JPL's NeBula team | — | — |
| MMS_SLAM | Multi-modal semantic SLAM, research code | — | — |
| Fast LOAM | Fast lidar odometry and mapping, research code | — | — |
| Webviz | Cruise's archived web bag viewer; Foxglove grew from it | — | — |
| CarlaSC | Semantic scene completion dataset and network on CARLA | — | — |
| Acorn precision farming rover | Robot; not in the Atlas | — | — |
| Awesome Robot Descriptions | Awesome list; triaged in Phase 3 | — | — |
| hdl_graph_slam | 3D lidar graph SLAM for ROS 1 | — | — |
| PL-SLAM | Point and line monocular SLAM, research code | — | — |
| Rosbag Editor | Small GUI to cut and filter rosbags | — | — |
| DCL-SLAM | Distributed lidar SLAM for robot swarms | — | — |
| READ | Neural scene rendering for driving, research code | — | — |
| 3D Detection & Tracking Viewer | Viewer for 3D detection and tracking results | — | — |
| maplab | ETH multi-session visual-inertial mapping framework | — | — |
| Kimera | MIT metric-semantic SLAM library | — | — |
| ORB-SLAM3-RGBL | ORB-SLAM3 fork adding RGB plus lidar input | — | — |
| LiDAR Ground Mapping | High-density lidar ground maps for vehicles | — | — |
| LiDAR to Image | Converts lidar point clouds to images | — | — |
| Awesome Visual SLAM | Awesome list on visual SLAM | — | — |
| Fields2Cover | Coverage path planning library for farm vehicles | — | — |
| Dense Fusion | 6D object pose estimation from RGB-D, research code | — | — |
| Monocular Quasi-Dense 3D Object Tracking | Monocular 3D object tracking, research code | — | — |
| LSD (LiDAR SLAM & Detection | Lidar SLAM and detection stack for vehicles | — | — |
| Dynablox | Detects moving objects from volumetric maps | — | — |
| FTXUI | C++ terminal user interface library | — | — |
| All about ROS 2 and the new Gazebo | ICRA 2023 tutorial on ROS 2 with the new Gazebo | — | — |
| Vizanti - Web Visualizer & Mission Planner for ROS | Web visualiser and mission planner for outdoor ROS robots | — | — |
| Frontier Exploration | ROS 1 frontier exploration node and costmap layer | — | — |
| DockerSLAM | Docker images for running SLAM systems | — | — |
| Motion planners implementations | Python samples of vehicle motion planners | — | — |
| Awesome point cloud place recognition | Paper list on lidar place recognition | — | — |
| Dear ROS Node Viewer | Viewer for ROS 2 node graphs | — | — |
| Robo3D | Benchmark of 3D perception under corruptions | — | — |
| 3DMR | Multi-robot 3D exploration and patrolling, ROS 1 | — | — |
| ROS 2 Planning System | PDDL task planning framework for ROS 2 (PlanSys2) | — | — |
| ROS SAM | ROS wrapper for Segment Anything | — | — |
| Small GICP | Fast point-cloud registration library (ICP, GICP, VGICP) | — | — |
| OK-Robot | Open-vocabulary pick-and-drop system on Stretch, research code | — | — |
| ROS2 Laser scan merger | Merges several laser scans into one virtual scan | — | — |
| Dubins Path Planning | Hybrid A* and RRT with Dubins paths, sample code | — | — |
| The Robot Report | Robotics industry news podcast | — | — |
| ROS Developers Podcast | The Construct's ROS interview podcast | — | — |
| Audrow Nash Podcast | Interviews with robotics builders and founders | — | — |
| Learn Robotics and AI | Podcast on robotics careers and learning | — | — |
| Lex Fridman Podcast | General AI and science interview podcast | — | — |
| Sense Think Act Podcast (Inactive) | Inactive robotics interview podcast; the archive remains | — | — |
| Robothub Podcast (Inactive) | Inactive Robohub robotics podcast; the archive remains | — | — |
| ACM/IEEE International Conference on Human Robot Interaction (HRI) | Conference on human-robot interaction | — | — |
| IEEE Conference on Decision and Controls (CDC) | Control systems conference | — | — |
| IEEE International Conference on Rehabilitation Robotics (ICORR) | Rehabilitation robotics conference | — | — |
| IEEE International Conference on Robotics and Automation (ICRA) | The main IEEE robotics conference | — | — |
| IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) | Major IEEE/RSJ robotics conference | — | — |
| IEEE-RAS International Conference on Humanoid Robots (Humanoids) | Humanoid robotics conference | — | — |
| International Symposium of Robotic Research (ISRR) | Robotics research symposium | — | — |
| International Symposium of Experimental Robotics (ISER) | Experimental robotics symposium | — | — |
| Robotics: Science and Systems Conference (RSS) | Robotics: Science and Systems conference | — | — |
| The International Workshop on the Algorithmic Foundations of Robotics (WAFR) | Workshop on algorithmic foundations of robotics | — | — |
| Conference on Computer Vision and Pattern Recognition (CVPF) | The main computer vision conference (CVPR) | — | — |
| Robotics and Autonomous Systems | Elsevier robotics journal | — | — |
| Journal of Intelligent & Robotic Systems (JINT) | Springer intelligent and robotic systems journal | — | — |
| Transactions on Robotics (T-RO) | IEEE flagship robotics journal | — | — |
| International Journal of Robotics Research (IJRR) | SAGE robotics research journal | — | — |
| Autonomous Robots | Springer autonomous robots journal | — | — |
| Robotics and Computer-Integrated Manufacturing | Elsevier manufacturing robotics journal | — | — |
| Journal of Field Robotics (JFR) | Wiley field robotics journal | — | — |
| Robotics & Automation Magazine (RAM) | IEEE robotics magazine | — | — |
| Robotica | Cambridge robotics journal | — | — |
| Robotics and Automation Letters (RA-L) | IEEE robotics letters journal | — | — |
| NAVER LABS Europe | Industrial research lab in vision and robotics | — | — |
| PAL Robotics | Maker of humanoid and mobile robots (TIAGo, TALOS) | — | — |
| X | Alphabet's moonshot lab | — | — |
| Waymo | Self-driving car company | — | — |
| ZOOX | Robotaxi company owned by Amazon | — | — |
| Robotec AI | Simulation and software company for vehicles and robots | — | — |
| Fraunhofer IPA | Applied robotics and automation research institute | — | — |
| ihmc Robotics | Research institute known for humanoid walking control | — | — |
| GUSS | Autonomous orchard sprayer maker | — | — |
| AgroIntelli | Autonomous field robot maker | — | — |
| Rowbot | Row-crop agriculture robot company | — | — |
| Bear Flag Robotics | Autonomous tractor startup, bought by John Deere in 2021 | — | — |
| Agrobot | Fruit-harvesting robot company | — | — |
| Rabbit | Farm utility robot company | — | — |
| Civil Maps | HD mapping and localisation company | — | — |
| Small Robot | UK farming robot company | — | — |
| Aptiv | Automotive supplier | — | — |
| nuTonomy | Self-driving startup, now part of Motional | — | — |
| Agreenculture | Autonomous farming robot company | — | — |
| robust.ai | Warehouse robot and AI company | — | — |
| Vicarious | AI robotics company, now part of Intrinsic | — | — |
| Kopernikus Automotive | Automated valet parking company | — | — |
| Korechi | Agricultural and turf robot company | — | — |
| Toyota Research Instute | Toyota's research institute for robotics and AI | — | — |
| AGXEED | Autonomous tractor maker | — | — |
| Halodi Robotics | Humanoid maker, now 1X Technologies | — | — |
| SelfDriving.fyi | Database of self-driving companies | — | — |
| Swarm Farm | Autonomous farm robot company | — | — |
| Lyft Level 5 | Lyft's self-driving unit, now part of Toyota's Woven | — | — |
| Wayve | Learned end-to-end driving company | — | — |
| Catalog - Self-driving cars | Catalogue of self-driving companies and products | — | — |
| BoxBot | Parcel-sorting robot company | — | — |
| NVIDIA DRIVE Constellation | NVIDIA's driving simulation platform | — | — |
| Aeolus | Service robot company | — | — |
| Burro | Collaborative farm robot maker | — | — |
| Intermodalics | Robotics software consultancy | — | — |
| Gestalt | Industrial automation service company | — | — |
| Volvo Autonomous Solutions | Volvo's autonomous transport unit | — | — |
| DeepMap | HD mapping company, bought by NVIDIA in 2021 | — | — |
| ABB | Industrial robot maker | — | — |
| exyn | Autonomous mapping drone company | — | — |
| FarmDroid | Solar field robot for sowing and weeding | — | — |
| naïo technologies | Farm robot maker | — | — |
| Thorvald | Saga Robotics' modular farm robot | — | — |
| nLink | Norwegian mobile robot company | — | — |
| intek | Norwegian robotics company | — | — |
| nuro | Autonomous delivery vehicle company | — | — |
| Blue River | Precision spraying company, part of John Deere | — | — |
| ecorobotix | Precision spraying robot company | — | — |
| ZTractor | Autonomous electric tractor maker | — | — |
| FarmWise | Weeding robot company | — | — |
| mobileye | Driver-assistance and autonomy supplier | — | — |
| Optimus Ride | Self-driving shuttle startup | — | — |
| comma | Maker of the openpilot driver-assistance device | — | — |
| emesent | Lidar mapping drones and payloads | — | — |
| Apptronik | Humanoid robot maker | — | — |
| Automata | Lab automation company | — | — |
| Sevensense | Visual navigation company for mobile robots | — | — |
| Kingdom | Robot lawnmower maker for large terrain | — | — |
| Tangram Vision Platform | Sensor calibration and fusion software company | — | — |
| Brisa Robotics | Warehouse inventory robot company | — | — |
| AutoAgri | Autonomous implement-carrier maker | — | — |
| Istituto Italiano di Tecnologia (iit) | Italian research institute, home of iCub | — | — |
| ForwardX | Warehouse mobile robot company | — | — |
| AutoStore | Warehouse storage robot system | — | — |
| TORC | Self-driving truck company | — | — |
| NavVis | Mobile mapping and digital twin company | — | — |
| ROS Robotics Companies | List of companies using ROS | — | — |
| Sereact GmbH | AI warehouse robotics company | — | — |
| Autonomous Vision Group (AVG) | Andreas Geiger's vision group (KITTI) | — | — |
| Robot Vision Group | Andrew Davison's group at Imperial College | — | — |
| Computer Vision Group | Computer vision group, University Jaume I | — | — |
| Robotics and Perception Group | Scaramuzza's group at the University of Zurich | — | — |
| Laboratrio de Robótica Móvel | Mobile robotics lab at USP São Carlos | — | — |
| StachnissLab | Stachniss's photogrammetry and robotics lab, Bonn | — | — |
| Autonomous Intelligent Systems | Freiburg autonomous intelligent systems lab | — | — |
| Multi-Robt Systems Group | CTU Prague multi-robot systems group | — | — |
| Robotics and Intelligent Systems (ROBIN) | Robotics and intelligent systems group, University of Oslo | — | — |
| Machine Perception and Intelligent Robotics (MAPIR) | Machine perception and robotics group, Málaga | — | — |
| Robotics, Perception and Real Time Group | Zaragoza robotics group behind ORB-SLAM | — | — |
| Team CoSTAR | JPL-led DARPA SubT team (NeBula) | — | — |
| Autonomous Navigation and Perception Lab (ANPL) | Technion autonomous navigation and perception lab | — | — |
| Institute for Robotics and Intelligent Machines (IRIM) | Georgia Tech robotics institute | — | — |
| Vijay Kumar Lab | UPenn aerial and multi-robot lab | — | — |
| Phi Robotics | UFRGS robotics group | — | — |
| Computer Science and Artificial Intelligence Laboratory (CSAIL) | MIT computer science and AI lab | — | — |
| Goal-Oriented Long-Lived Systems (GOALS) | Nick Hawes's group at the Oxford Robotics Institute | — | — |
| Skoltech Mobile Robotics | Mobile robotics group at Skoltech | — | — |
| Compuver Vision and Intelligent Systems Laboratory | Computer vision lab at Ryerson University | — | — |
| The Computer Vision Industry | David Lowe's old list of vision companies | — | — |
| Google's driverless car | Thrun's TED talk on Google's self-driving car | — | — |
| Women in US Academic Research in Robotics | Directory of women researchers in US robotics | — | — |
| Talking Robotics | Virtual robotics seminar series | — | — |
| Robotics Diversity Reading List | Reading list for a more diverse robotics community | — | — |
| Stanford Cheatsheet on CNNs, RNNs | Stanford CS 230 deep learning cheatsheets | — | — |
| Google Dataset Search | Search engine for public datasets | — | — |
| Wevolver | Engineering news and knowledge platform | — | — |
| Awesome Robotics Brazil | List of Brazilian robotics groups and initiatives | — | — |
| Robot Hacking Manual | Notes and papers on robot cybersecurity | — | — |
| Black in Robotics | Community organisation for Black roboticists | — | — |
| Awesome Robotic Deliberation | Awesome list on ROS 2 deliberation, such as behaviour trees | — | — |
| Soft Robotics | Soft gripper maker; sold its mGrip gripper line to the Schmalz Group in 2024 and became Oxipital AI | — | — |
| AutonomousStuff | Vendor of drive-by-wire kits, autonomy sensors and integration for vehicles | — | — |
| ZiVID | Industrial 3D colour cameras for bin picking, with a ROS driver (zivid-ros) | — | — |

## Deferred

| Entry | What it is | Phase |
|---|---|---|

## Rejected

| Entry | Why | Date |
|---|---|---|
| C++ Essential Training | Dead link: cpp.bw.org no longer loads | 2026-11-18 |
| TutorialSearch | An advertisement for a tutorial search engine, not a course | 2026-11-18 |
| Different ROS courses | A Udemy search results page, not a course | 2026-11-18 |
| LearnOpencv | Duplicate of OpenCV: C++ and Python (the same LearnOpenCV tutorials) | 2026-11-18 |
| ROS Industrial Training | Duplicate of ROS Industrial Training above (its source repo) | 2026-11-18 |
| Master Git list | Too thin: a single tweet about Git | 2026-11-18 |
| Algorithms / Data Structures | Duplicate of Data Structure & Algorithms 101 (a folder of it) | 2026-11-18 |
| Robótica Educacional | Mislabelled: the link goes to Donkey Car's site, not the named group | 2026-11-18 |
| C++ Best Practices | Duplicate of CPP Best Practices | 2026-11-18 |
| Coding Notes | Duplicate of Coding Notes and Tutorials | 2026-11-18 |
| Google Interview Preparation | Off topic: coding interview puzzles | 2026-11-18 |
| Programming for Robotics | Duplicate of Programming for Robotics (the same Michigan course) | 2026-11-18 |
| List of Computer Science courses | Duplicate of Computer Science courses with video lectures | 2026-11-18 |
| CPP Optimizations Diary | Duplicate of C++ Optimizations Diary | 2026-11-18 |
| Machine Learning Stash | Too thin: a personal bookmark folder | 2026-11-18 |
| Writing for Computer Science | Off topic: an academic writing guide | 2026-11-18 |
| RGB-D SLAM Dataset | Duplicate of TUM Dataset | 2026-11-18 |
| RELLIS-3D | Duplicate of RELLIS-3D above | 2026-11-18 |
| Awesome SLAM Datasets | Duplicate of SLAM Datasets | 2026-11-18 |
| OpenCV 3.2.0 + Contrib | Outdated install guide (Ubuntu 16.04); OpenCV itself is triaged from other lists | 2026-11-18 |
| OpenCV 3.4.0 + Contrib | Outdated install guide (Ubuntu 18.04); OpenCV itself is triaged from other lists | 2026-11-18 |
| Simbad | Abandoned Java 3D simulator, unimportant today | 2026-11-18 |
| Morse | Dead link: the MORSE site no longer loads | 2026-11-18 |
| Peekabot | Dead link: the Peekabot site no longer loads | 2026-11-18 |
| Neurorobotics Platform (NRP) | Dead link: a bare IP address that no longer answers | 2026-11-18 |
| CoppeliaSim | Duplicate of V-REP (renamed CoppeliaSim) | 2026-11-18 |
| Ignition | Duplicate of Gazebo (Ignition was the new Gazebo's name) | 2026-11-18 |
| PyImageSearch on GitHub | Duplicate of PyImageSearch (the blog's code) | 2026-11-18 |
| DiSCo-SLAM | Duplicate of DiSCo-SLAM above | 2026-11-18 |
| LIO-SAM | Duplicate of LIO-SAM above | 2026-11-18 |
| My Global Planner Plugin | Too thin: a student's move_base planner plugin | 2026-11-18 |
| F110-MPC | Too thin: a student MPC demo in the F1TENTH simulator | 2026-11-18 |
| MRPT Project | Duplicate of MRPT | 2026-11-18 |
| Engineering Manager Resources | Off topic: engineering-management links | 2026-11-18 |
| GPS Waypoint-based Autonomous Navigation in ROS | Duplicate of GPS Waypoint Based Autonomous Navigation in ROS | 2026-11-18 |
| Awesome ChatGPT Prompts | Off topic: a ChatGPT prompt collection | 2026-11-18 |
| Fields2Cover | Duplicate of Fields2Cover above | 2026-11-18 |
| Segments.ai | Duplicate of Segments.ai in Softwares and Libraries | 2026-11-18 |
| Michael R. Bock | Not a lab: a personal homepage | 2026-11-18 |
| LaTeX Templates for documents of Inf/UFRGS | Off topic: university thesis templates | 2026-11-18 |
| Como usar o modelo LaTeX do Inf/UFRGS | Off topic: guide to a university LaTeX template | 2026-11-18 |
| Deckez | Advertisement: a pitch-deck design agency | 2026-11-18 |
| SlideEgg | Off topic: presentation templates | 2026-11-18 |
| Slidone | Off topic: presentation software | 2026-11-18 |
| SlidesCarnival | Off topic: presentation templates | 2026-11-18 |
| SlidesGO | Off topic: presentation templates | 2026-11-18 |
| Linguee | Off topic: dictionary and translator | 2026-11-18 |
| Academic Phrasebank | Off topic: academic writing phrases | 2026-11-18 |
| SkELL | Off topic: language corpus tool | 2026-11-18 |
| collocaid | Off topic: writing collocation tool | 2026-11-18 |
| Sketch Engine | Off topic: language corpus tool | 2026-11-18 |
| Thesaurus | Off topic: thesaurus | 2026-11-18 |
| LeetCode | Off topic: coding interview practice | 2026-11-18 |
| Autonomous Vehicle people | Too thin: a Twitter follower graph | 2026-11-18 |
| Jobs UK | Off topic: general academic job board | 2026-11-18 |
| Papers with Code | Shut down: the address now redirects to Hugging Face Papers | 2026-11-18 |
| Código aberto em 12 passos | Off topic: a general open-source contribution guide, in Portuguese | 2026-11-18 |
| Matcha | Off topic: online maths editor | 2026-11-18 |
| Quillbot | Off topic: paraphrasing tool | 2026-11-18 |
| OtterAI | Off topic: speech transcription tool | 2026-11-18 |
| Hemingway | Off topic: readability checker | 2026-11-18 |
| MakeReal TLDraw | Off topic: sketch-to-website demo | 2026-11-18 |
| Musicfly | Off topic: AI voice-to-instrument app | 2026-11-18 |
| Krea | Off topic: AI image tool | 2026-11-18 |
| Vidnoz | Off topic: AI video tool; reads like an advertisement | 2026-11-18 |
| Pixverse | Off topic: AI video tool | 2026-11-18 |
| Durable | Off topic: AI website builder; reads like an advertisement | 2026-11-18 |
| Seona | Advertisement: an AI SEO assistant | 2026-11-18 |
| Mini Pupper Trajectory Optimization | Small research demo (about 40 stars) for a robot not in the Atlas, inactive since January 2022 | 2026-11-26 |
