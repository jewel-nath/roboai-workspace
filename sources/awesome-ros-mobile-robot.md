---
type: source
name: awesome-ros-mobile-robot
registry: awesome-ros-mobile-robot
url: https://github.com/shannon112/awesome-ros-mobile-robot
commit: "a405fbf"
read_on: 2026-11-17
counts: {entries: 185, pages: 13, waiting: 17, index_only: 119, deferred: 11, rejected: 25}
---

# awesome-ros-mobile-robot: what it gives RoboAI

A list of resources for building ROS mobile robots: theory, ROS, platforms, sensors,
calibration, odometry, SLAM, localization, mapping, navigation and manipulation. For the Atlas it
gives a short platform section naming the classic ROS research robots and the small race-car
projects; its real weight is the software sections, which Phase 4 reads.

## How it was read

- Read at commit `a405fbf` on 2026-11-17 (its last commit is 2025-10-31). Phase 3 covers only
  the `2_Robotic_Platform` section: 23 entries.
- **Phase 4** read the header links and sections 0, 1 and 3 to 11 on 2026-11-18, at the same
  commit, and decided the robots.ros.org row Phase 3 deferred. Page candidates were checked with
  shallow git clones (last commit, licence) and every link with an HTTP request. The sensors in
  section 3 and the Razor IMU guides in section 4 are parts, deferred to Phase 5. Paper-only
  groups (surveys, tutorials, the mapping backbones, the navigation research) and bullets that
  only name methods are one row each. Moved on 2026-11-18: the Gazebo releases page, the
  torchvision models page, `ydlidar_ros`, the MultiSense S7 docs and the TUM RGB-D site (now
  cvg.cit.tum.de); ceres-solver.org did not resolve, though its repo is active. Dead links are in
  Rejected. Nothing in the README addresses agents.
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
| "Franka Emika panda" | [Franka Emika Panda and Franka Research 3](../wiki/robots/franka-panda.md) | B |
| "Universal Robot 3/5/10/e" | [Universal Robots UR3, UR5, UR10 and e-Series](../wiki/robots/universal-robots.md) | B |
| "Georgia Tech" race car (AutoRally) | [AutoRally](../wiki/robots/autorally.md) | B |
| "turtlebot" (GitHub org) | [TurtleBot (1, 2 and 4)](../wiki/robots/turtlebot.md) | B |
| "clearpath husky", "clearpath jackel" | [Clearpath research bases (Husky, Jackal, Dingo, Ridgeback, Boxer)](../wiki/robots/clearpath-robots.md) | B |
| "Personal Robot 2 (PR2)" | [Willow Garage PR2](../wiki/robots/pr2.md) | B |
| "kuka youbot" | [KUKA youBot](../wiki/robots/kuka-youbot.md) | B |
| "fetch robotics" | [Fetch Robotics Fetch and Freight](../wiki/robots/fetch.md) | B |
| ROS2 (release list) | [ROS 2](../wiki/tools/ros2.md) | A |
| "Bridge for Non-ROS Programs(JSON API)" (rosbridge_suite) | [rosbridge_suite](../wiki/software/rosbridge-suite.md) | B |
| "ros_control" | [ros2_control](../wiki/software/ros2-control.md) | A |

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|
| Gazebo (release list) | `tools/gazebo` | A | sim | The default open simulator for ROS 2 robots, with sensors and the ros_gz bridge |
| "AprilTag" | `software/apriltag` | B | perception | The standard fiducial markers for pose, calibration and docking; maintained C library with ROS 2 nodes |
| "YOLOv3" | `learning/yolo` | B | perception | The YOLO family is the usual real-time detector on robots; the linked darknet_ros is ROS 1 and stale |
| Feature Matching (OpenCV feature2d tutorials) | `software/opencv` | A | perception | The base computer-vision library under most robot perception code, from calibration to features |
| "VINS-Fusion" | `software/vins-fusion` | B | perception | A widely used visual-inertial odometry baseline for mono, stereo and GPS fusion; inactive since 2021 |
| "robot_localization" | `software/robot-localization` | A | perception | The standard EKF/UKF package for fusing wheel odometry, IMU and GPS in ROS 2 |
| GTSAM | `software/gtsam` | A | perception | Factor-graph library behind LIO-SAM and many sensor-fusion stacks; iSAM2 is part of it |
| "Cartographer" | `software/cartographer` | B | perception | Google's 2D and 3D lidar SLAM, still common on ROS 2 robots; inactive since January 2024 |
| "ORB-SLAM3" | `software/orb-slam3` | B | perception | The reference feature-based visual and visual-inertial SLAM; GPL-3.0, inactive since 2022 |
| "RTAB-Map" | `software/rtab-map` | A | perception | Maintained RGB-D, stereo and lidar SLAM with ROS 2 support; a common default for 3D mapping |
| "LIO-SAM" | `software/lio-sam` | B | perception | Widely used tightly coupled lidar-inertial SLAM built on GTSAM; inactive since 2023 |
| "Octomap" | `software/octomap` | B | perception | Probabilistic octree 3D occupancy maps; MoveIt and many planners use them for collision checking |
| ROS Navigation Stack (move_base architecture) | `software/nav2` | A | nav | This is the ROS 1 stack; its successor Nav2 is the standard ROS 2 navigation framework |
| ROS Moveit (move_group architecture) | `software/moveit2` | A | manip | The standard ROS motion-planning framework; MoveIt 2 is its ROS 2 version |
| "Open Motion Planning Library (OMPL)" | `software/ompl` | A | manip | The sampling-based planner library behind MoveIt; maintained |
| "KITTI" | `learning/kitti` | B | perception | The classic driving benchmark for odometry, SLAM and 3D detection; still cited everywhere |
| "TUM RGB-D SLAM Benchmark & Dataset" | `learning/tum-rgbd` | B | perception | The standard RGB-D benchmark with ground truth for visual odometry and SLAM |

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| ROS1 (release list) | ROS 1 releases; the last, Noetic, ended in May 2025 | — | — |
| Open Robotics Resources (7 links) | Official ROS sites: Open Robotics, ROS Index, docs, forums, Q&A | — | — |
| Books, robotics section (7) | Textbooks on probabilistic robotics, vision geometry, SLAM, ML and maths | — | — |
| Courses (17) | Video lectures and courses on robotics, control, SLAM and ML | — | — |
| Paper Libraries (7) | Paper search sites: IEEE Xplore, arXiv, OpenReview, Google Scholar and more | — | — |
| ROS Official Website (5 links) | ros.org, wiki, docs, status page, and ROS Answers (read-only since 2023) | — | — |
| ROS Related Blogs & Channels & Forums (5) | The Construct and JetsonHacks videos; Chinese Linux and SLAM blogs | — | — |
| Books, ROS section (10) | C++, design-pattern and ROS 1 programming books | — | — |
| Multiple Machines with Multi-Master | ROS 1 multi-master discovery across machines (multimaster_fkie) | — | — |
| Multiple Machines with One Master | ROS 1 network setup guide | — | — |
| Multiple Tasks with Smach | Python state-machine library for ROS tasks | — | — |
| Bridge communication between ROS 1 and ROS 2 | ros1_bridge: relays topics between ROS 1 and ROS 2 | — | — |
| "Aerial, Ground, Marine, Manipulator, Component" (robots.ros.org) | Directory of robots with ROS support | — | — |
| "MIT" race car (MIT RACECAR) | 1/10 teaching race car, predecessor of F1TENTH; on its page | 2022-02-23 | BSD-3-Clause (software) |
| "UCB" race car (BARC) | 1/10 Berkeley control-research car; inactive | 2021-06-09 | MIT |
| "Taiwan Hypharos" race car | Low-cost 1/10 car with RPLidar and Odroid; inactive | 2018-05-09 | LGPL-3.0 |
| "Robotnik XL-GEN" | Summit-XL base, the same robot as RB-SUMMIT | — | — |
| "Robotnik RB-KAIROS" | Omnidirectional base with a cobot arm | — | — |
| "Robotnik RB-1" | One-arm torso mobile manipulator | — | — |
| "Techman Robot" | Cobot with a wrist camera; the link is an unofficial driver | — | — |
| "usb camera", "gstream-based camera", "opencv camera" | Generic ROS camera drivers: usb_cam, gscam, cv_camera | — | — |
| "gTTS" | Python text-to-speech through Google Translate | — | — |
| "sound_play" | ROS package that plays sounds and speech | — | — |
| "SpeechRecognition" | Python wrapper for several speech-to-text engines | — | — |
| "ARTag" | ROS 1 AR-marker tracker (ar_track_alvar) | — | — |
| "CALTag" | Self-identifying checkerboard calibration target, academic code | — | — |
| "comparison" (1 paper) | Paper comparing ARTag, AprilTag and CALTag under occlusion | — | — |
| Learning-Based Feature Extractor | Pretrained CNN backbones in torchvision; the link has moved | — | — |
| "Faster R-CNN", "SSD" (2 papers) | Object-detector papers, no code linked | — | — |
| "OpenPose" | Classic multi-person pose estimator; non-commercial research licence | 2024-08-02 | custom, non-commercial |
| "camera_calibration" | ROS checkerboard calibration for camera intrinsics (image_pipeline) | — | — |
| "format converter" (camera_calibration_parsers) | Reads and writes ROS camera calibration files | — | — |
| "easy_handeye" | Hand-eye calibration for ROS 1 arms; easy_handeye2 targets ROS 2 | — | — |
| Visual Based Ego-Motion Backbone | Visual odometry building blocks: features, matching, optical flow, PnP, ICP | — | — |
| Odometry Survey Paper (2 papers) | Visual-inertial odometry benchmark and review | — | — |
| "rf2o" | Planar odometry from 2D laser scans (range flow) | — | — |
| "VINS-Mono" | Monocular visual-inertial estimator; VINS-Fusion extends it | 2024-05-23 | GPL-3.0 |
| "SVO" | Semi-direct monocular visual odometry from UZH | — | — |
| "DSO" | Direct sparse monocular odometry from TUM | — | — |
| "VISO2" | Stereo and monocular visual odometry library from KIT | — | — |
| "OKVIS" | Keyframe-based visual-inertial odometry from ETH | — | — |
| "ROVIO" | EKF visual-inertial odometry from ETH using photometric error | — | — |
| "RotRocc+, RotRocc, ROCC, MonoROCC" (4 papers) | Visual odometry outlier-rejection papers, no code linked | — | — |
| "DVO" | Dense RGB-D odometry from TUM, old ROS 1 code | — | — |
| "SOFT" | Student MATLAB implementation of SOFT stereo odometry | — | — |
| "LOAM & V-LOAM" | Unofficial copy of the original LOAM lidar odometry code | — | — |
| "LIMO" | Lidar-monocular visual odometry from KIT | — | — |
| "DeepVO" | Unofficial PyTorch reimplementation of learned DeepVO; second link dead | — | — |
| "robot_pose_ekf" | ROS 1 EKF odometry fusion, replaced by robot_localization | — | — |
| SLAM Theorem & Tutorial (4 papers) | Classic SLAM tutorials and a filter-versus-graph comparison | — | — |
| SLAM Survey Paper (3 papers) | Surveys of SLAM, RGB-D SLAM and RGB-D reconstruction | — | — |
| SLAM Backbone (Back-End) | Back-end methods, named only: Kalman, particle filters, graph optimisation | — | — |
| g2o Library | Graph-optimisation library used by ORB-SLAM | 2026-09-26 | BSD-2-Clause (core) |
| iSAM | Incremental smoothing and mapping; iSAM2 now ships in GTSAM | — | — |
| SLAM++ | Incremental SLAM optimisation library from Brno University | — | — |
| "MIT Stata Center Dataset" | Long-term indoor SLAM dataset recorded on a PR2 | — | — |
| "Radish Dataset" | Old repository of 2D laser SLAM logs | — | — |
| "ICL-NUIM RGB-D Benchmark & Dataset" | Synthetic RGB-D benchmark with ground truth | — | — |
| "EuRoC MAV Dataset" | Standard visual-inertial benchmark recorded on drones | — | — |
| "Benchmark", "Survey Paper" (2 papers) | SLAM accuracy metrics and an RGB-D dataset survey | — | — |
| "Gmapping" | Particle-filter 2D SLAM, the ROS 1 default | — | — |
| "Hector" | 2D scan-matching SLAM that needs no odometry, ROS 1 | — | — |
| "Karto" | Graph-based 2D SLAM; SLAM Toolbox builds on Open Karto | — | — |
| "FastSLAM" (2 papers) | Particle-filter SLAM papers, no code linked | — | — |
| "MonoSLAM" | Early real-time monocular EKF SLAM; SceneLib2 port | — | — |
| "PTAM" | Parallel tracking and mapping, keyframe SLAM for small AR spaces | — | — |
| "ORB-SLAM" | Feature-based monocular SLAM, superseded by ORB-SLAM3; links ORB-SLAM2's repo | — | — |
| "LSD-SLAM" | Semi-dense direct monocular SLAM; paper only here | — | — |
| "DTAM" | Dense monocular tracking and mapping (OpenDTAM port) | — | — |
| "DVO-SLAM" | Dense visual SLAM for RGB-D cameras from TUM | — | — |
| "RGBDSLAMv2" | RGB-D SLAM for ROS 1 | — | — |
| "KinectFusion" | Dense depth-camera reconstruction research; no code linked | — | — |
| "ElasticFusion" | Surfel-based dense RGB-D SLAM; non-commercial licence | — | — |
| "BundleFusion" | Globally consistent RGB-D reconstruction from Stanford | — | — |
| "KO-Fusion" | Dense SLAM for a mobile manipulator; video and paper only | — | — |
| "arm-slam" | SLAM from arm kinematics; video and paper only | — | — |
| "Zebedee" | CSIRO's handheld spring-mounted lidar mapper | — | — |
| "hdl_graph_slam" | 3D lidar graph SLAM with GPS and IMU constraints, ROS 1 | — | — |
| "Lego-LOAM" | Ground-optimised lidar odometry for UGVs; LIO-SAM succeeded it | 2020-07-02 | BSD-3-Clause |
| "IMLS-SLAM" (1 paper) | Scan-to-model lidar SLAM; paper only | — | — |
| "ViTa-SLAM" | Bio-inspired visuo-tactile SLAM research code | — | — |
| "Kimera" | Metric-semantic VIO and mesh mapping from MIT SPARK | 2021-01-30 | BSD-2-Clause |
| "AMCL" | Particle-filter localisation on 2D maps; ships in Nav2 | — | — |
| "mrpt_localization" | Particle-filter localisation from the MRPT library | — | — |
| "2D Occupancy Grid Map", "3D Occupancy Grid Map" | Occupancy grid maps, named as concepts | — | — |
| "map_server" | ROS map loading and saving; Nav2 has its own map server | — | — |
| "octomap_server" | ROS node that builds and serves OctoMaps | — | — |
| Advanced 3D Mapping Backbones (4 papers) | Surfel, SDF, TSDF and ESDF map papers | — | — |
| "voxblox" | TSDF and ESDF mapping for drone planning from ETH | — | — |
| "OpenChisel" | Spatially hashed TSDF reconstruction for mobile devices | — | — |
| "DenseSurfelMapping" | Real-time dense surfel mapping from HKUST | — | — |
| "move_base" | Central node of the ROS 1 navigation stack | — | — |
| "move_base_flex" | ROS 1 navigation framework with pluggable planners and controllers | — | — |
| global_planner, carrot_planner, navfn, sbpl_lattice_planner, srl_global_planner, voronoi_planner | ROS 1 global planner plugins, named only | — | — |
| "A* (A Star)", "Dijkstra's" (2 papers) | Classic shortest-path search papers | — | — |
| dwa_local_planner, teb_local_planner and 5 more | ROS 1 local planner plugins, named only | — | — |
| "Timed Elastic Band (TEB)" | Trajectory-optimising local planner, also for car-like robots | — | — |
| "Dynamic Window Approach (DWA)" | Sampling local planner; Nav2's DWB controller descends from it | — | — |
| Velocity Obstacle (VO), Reciprocal Velocity Obstacle (RVO), ORCA | Multi-agent collision avoidance papers, with the RVO2 library and collvoid | — | — |
| rotate_recovery, move_slow_and_clear, stepback_and_steerturn_recovery | ROS 1 recovery behaviour plugins, named only | — | — |
| Novel Navigation Strategy (9 papers) | Learned and socially aware navigation research from MIT, Google, ETH | — | — |
| Coverage Navigation (1 paper) | Survey of coverage path planning | — | — |
| "Search Based Planning Library (SBPL)" | Search-based lattice planners (ARA*, Anytime D*) from CMU | — | — |
| "Covariant Hamiltonian Optimiza-tion for Motion Planning (CHOMP)" | Trajectory-optimisation motion planner; available in MoveIt | — | — |
| Orocos Kinematics and Dynamics Library (KDL) | Kinematics library behind ROS's default IK plugin | — | — |
| Robotic Companies (table, about 60 names) | Robotics companies in 15 categories, names only | — | — |
| Top conferences: ICRA, IROS | The two main robotics conferences | — | — |
| Related Societies (6) | IEEE RAS, IES, CSS, SMC, Science Robotics and CoRL | — | — |
| "Google Scholar Rank", "Journal Citation Reports (JCR)" | Venue ranking sites | — | — |
| "DARPA Robotics Challenge" | 2012–2015 disaster-response humanoid challenge (Wikipedia) | — | — |
| "RoboCup" | Robot soccer, rescue and home competitions (Wikipedia) | — | — |
| "ICRA Robot Competitions", "IROS Robot Competitions" | Yearly conference competitions; no links | — | — |
| "SKS 新光保全智慧型保全機器人競賽" | Taiwanese security-robot contest (Facebook page) | — | — |
| "ROS-industrial" | Consortium extending ROS to industrial robots and drivers | — | — |
| "ROS2.0" (design.ros2.org) | ROS 2 design articles | — | — |
| "Open Source Robotics Foundation (OSRF)" | Open Robotics, the non-profit behind ROS and Gazebo | — | — |
| "ROS.Taiwan", "ROS.Taipei" | Taiwanese ROS user groups on Facebook | — | — |
| "ROScon" | Yearly ROS developer conference | — | — |
| "ROS Summer School(CN)" | Chinese ROS summer school | — | — |

## Deferred

| Entry | What it is | Phase |
|---|---|---|
| Processing Unit (SBC/IPC): Raspberry Pi, BeagleBone Black, Odroid, Tinker Board, Jetson, ADLINK Neuron | Robot computers | 5 |
| Motor & Controller & Encoder: Elmo, RLS, Faulhaber, Maxon, Dexmart | Motor and encoder vendors | 5 |
| RGB-D Camera: Kinect v1 and v2, Asus Xtion, Intel RealSense D400, Occipital Structure | RGB-D cameras and their ROS drivers | 5 |
| Stereo Camera: Stereolabs ZED, Carnegie Robotics MultiSense S7, e-Con Tara, Nerian SP1 | Stereo cameras and their ROS drivers | 5 |
| Laser Rangefinder: Hokuyo URG and UTM, YDLIDAR, RPLIDAR, SICK | 2D lidars and their ROS drivers | 5 |
| LIDAR: Velodyne, Livox | 3D lidars; the Livox link is the loam_livox SLAM package | 5 |
| IMU: Xsens, MicroStrain 3DM-GX2, SparkFun 9DOF Razor IMU M0 | IMUs and their ROS drivers | 5 |
| 3D Scanning & Novel Sensing Device: Kaarta, Matterport, Azure Kinect DK, RealSense T265 and L515 | Scanners and depth or tracking cameras, several discontinued | 5 |
| Microphone Array: ReSpeaker Mic Array v2.0 | USB microphone array | 5 |
| IMU (Sparkfun Razer 9dof-razor-imu-m0) Calibration (4 guides) | Calibration guides for the Razor IMU | 5 |
| Ceres Solver Library | Non-linear least-squares solver, with the other optimisation libraries | 5 |

## Rejected

| Entry | Why | Date |
|---|---|---|
| "Robotics" {UPenn} (course) | Dead link: the Coursera specialisation returns 404 | 2026-11-18 |
| "Sci-Hub" | Shadow library of unlicensed papers; the sci-hub.tw domain is parked | 2026-11-18 |
| "泡泡機器人論壇" (PaoPao Robot forum) | Dead link: paopaorobot.org no longer resolves | 2026-11-18 |
| "機器人作業系統ROS 史話36篇" | Dead link: the PDF returns 404 | 2026-11-18 |
| "clearpath husky+UR5" | Dead link (404); the configuration belongs on `clearpath-robots` | 2026-11-17 |
| "clearpath husky+dualUR5" | Dead link (404); the configuration belongs on `clearpath-robots` | 2026-11-17 |
| "Amazon Alexa", "Google Nest", "Apple Homepod", "Mi AI Speaker", "ASUS Smart Speaker" | Shop pages for consumer smart speakers; nothing to build with | 2026-11-18 |
| "PyAIML -- The Python AIML Interpreter" | Dead link (404); AIML chatbots are long obsolete | 2026-11-18 |
| "OpenPose-plugin" | Dead link: tf-pose-estimation returns 404 | 2026-11-18 |
| "VISO2" (stereo) | Duplicate of VISO2 above | 2026-11-18 |
| "VINET" | Unofficial reimplementation with no licence, inactive since 2018 | 2026-11-18 |
| "The KITTI Vision Benchmark & Dataset" | Duplicate of KITTI above | 2026-11-18 |
| "ORB-SLAM2" | Duplicate: the same repo as ORB-SLAM above | 2026-11-18 |
| "Kaarta" (3D LiDAR SLAM) | Duplicate of Kaarta in the sensing section, deferred to Phase 5 | 2026-11-18 |
| "BLAM" | Abandoned: no commit since 2016, and newer lidar SLAM covers it | 2026-11-18 |
| "Cartographer" (3D LiDAR SLAM) | Duplicate of Cartographer above | 2026-11-18 |
| "Compress PDF Online" | A generic PDF tool, not robotics | 2026-11-18 |
| "Amazon Robotics/Picking Challenge" | Dead link: the domain no longer resolves; the challenge ended in 2017 | 2026-11-18 |
| "PMC 全國智慧機器人競賽 Robot competition" | The domain now serves a sports-streaming spam page | 2026-11-18 |
| "HIWIN 上銀智慧機械手實作競賽" | Dead link (404) | 2026-11-18 |
| "SiliconAwards 旺宏金矽獎" | Dead link: the server sends an empty reply | 2026-11-18 |
| "ROS-H" | Dead: the Acutronic Robotics domain now redirects to an unrelated site | 2026-11-18 |
| "Open Source Robotics Corporation (OSRC)" | Duplicate: the same link as OSRF | 2026-11-18 |
| "ROSDevCon" | A one-off 2019 online event; the domain redirects to its old page | 2026-11-18 |
| "ROS Summer School(TW)" | Dead link: taoyuan-ros.com.tw no longer resolves | 2026-11-18 |
