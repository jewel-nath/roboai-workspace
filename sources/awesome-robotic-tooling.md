---
type: source
name: awesome-robotic-tooling
registry: awesome-robotic-tooling
url: https://github.com/Ly0n/awesome-robotic-tooling
commit: "dc73ead"
read_on: 2026-11-18
counts: {entries: 938, pages: 49, waiting: 8, index_only: 624, deferred: 0, rejected: 257}
---

# awesome-robotic-tooling: what it gives RoboAI

A broad list of tooling for professional robot development in C++ and Python: ROS, simulation,
sensor processing, SLAM, planning, visualisation, middleware, operations and security. For RoboAI
it confirms the core ROS 2 toolset (ROS 2, tf2, URDF, colcon, the DDS implementations,
PlotJuggler), the planning libraries (MoveIt 2, OMPL, Pinocchio) and the standard perception and
SLAM libraries (robot_localization, slam_toolbox, Open3D). It has had no commit since April 2023
and much of it is general software with no robot angle, so most entries are index rows or
rejected.

## How it was read

- Read at commit `dc73ead` (2023-04-30) on 2026-11-18. The repository moved from protontypes to
  Ly0n; the old URL redirects. The list was split between two agents at the section "Localization
  and State Estimation"; each part's notes follow.
- **Phase 5 re-triage (2026-11-26):** the 71 rows deferred to Phase 5 were decided; the list was
  not re-read, so `commit` and `read_on` stay. Each entry's link was loaded on github.com (to
  follow renames and look for the archived banner) and its repo fetched as a blobless shallow
  clone for the last commit and the licence file; ROS repos without one were read from
  `package.xml`. Index rows show the newest commit of the entry's repo, or of its ROS 2 branch
  where that is newer (ublox). **Moved:** PX4/Firmware to PX4/PX4-Autopilot, madcowswe/ODrive to
  odriverobotics/ODrive, xesscorp/kicad-3rd-party-tools to devbisme, formatc1702/WireViz to
  wireviz/WireViz, UAVCAN/libuavcan to OpenCyphal-Garage/libcyphal, eerimoq/cantools to
  cantools/cantools, christiansandberg/canopen to canopen-python/canopen,
  mayataka/autogenu-jupyter to ohtsukalab, JWhitleyAStuff/decanstructor to JWhitleyWork,
  ouster_example to ouster-sdk, and ngspice.sourceforge.net to ngspice.sourceforge.io.
  **Archived:** intel/ros2_intel_realsense. **Page candidates** (last commit, licence): PX4
  2026-11-25, BSD-3-Clause; ArduPilot 2026-11-25, GPL-3.0; phobos 2026-07-14, BSD-3-Clause;
  solidworks_urdf_exporter 2026-09-25, MIT (its newest release, 1.6.1, targets SolidWorks 2021);
  FreeCAD 2026-11-25, LGPL-2.1; KiCad 2026-11-25 (GitLab and the GitHub mirror at the same
  commit), GPL-3.0; OpenSCAD 2026-11-25, GPL-2.0; WireViz 2026-10-25, GPL-3.0; CasADi
  2026-11-25, LGPL-3.0; python-can 2026-11-23, LGPL-3.0; can-utils 2026-10-14, GPL-2.0-only or
  BSD-3-Clause per file; CANopenNode 2026-07-10, Apache-2.0; micro_ros_arduino 2025-09-30
  (release 2.0.8, Kilted), Apache-2.0. ros_canopen is ROS 1 (its default branch targets Melodic),
  so its row carries the `software/ros2-canopen` page, checked at ros-industrial/ros2_canopen
  (2026-11-06; Apache-2.0 and LGPL-3.0 packages, with a CiA 402 driver and a ros2_control
  interface). **Parts:** OpenCR's repo last changed on 2023-08-01 (Apache-2.0), but ROBOTIS's
  shop still lists the OpenCR1.0 board and three Atlas robots use it. ODrive's open firmware
  (2026-01-20, MIT) covers only the ODrive v3.x, which its README marks not recommended for new
  designs; the S1, Pro and Micro on sale run closed firmware, so the page must say which models
  it covers. **Index only although the plan names them:** PcbDraw and ngspice, helpers the KiCad
  page can cover; SOES, an EtherCAT slave stack, where builders mostly need a master. **Vendor
  drivers:** RealSense earns a part page, so the archived ROS 2 wrapper names it; the BNO055 is
  in three Atlas stacks (iCub, Kayra, Open Duck Mini), so bosch_imu_driver names
  `parts/sensors/bosch-bno055`. No other sensor line in these rows is in two Atlas robots (the
  two SICK robots use TiM571 scanners, not safety scanners). ROS 1-only drivers and tools with no
  commit since 2022 or earlier are rejected, except rosserial (the standard ROS 1 link to MCUs,
  used by the BCN3D Moveo) and bosch_imu_driver (kept for the BNO055 page). **Outcome:** 17
  waiting, 47 index only, 7 rejected; "awesome CAN" is iDoka/awesome-canbus, ingested as its own
  source. PX4, ArduPilot, FreeCAD, KiCad, LibrePCB, F Prime and vxworks7-ros2-build ship
  `AGENTS.md` or `CLAUDE.md` files for their own contributors; they were not read or followed.
  Nothing else in the fetched files was addressed to agents.

### Communication and Coordination to Sensor Processing

- Read the README in full from a shallow clone at `dc73ead`; CONTRIBUTING.md too. No section in
  this part holds only papers; the one paper, "Guidelines" (ICSE 2020, architecting ROS systems),
  has its own index row.
- Every repository link in this part (436 on GitHub, GitLab and Gerrit) was fetched as a
  commit-only shallow clone to read its last commit date, and each GitHub page was checked for the
  archived banner; the other 57 links were loaded with curl. These dates only separated index rows
  from rejected ones; index rows keep `—` in Last commit and Licence, as the brief asks.
- Page candidates were checked in the live upstream repo (last commit, licence file): ROS via
  ros2/rclcpp (2026-11-17, Apache-2.0); Autoware via autowarefoundation/autoware (2026-11-09,
  Apache-2.0); colcon-core (2026-09-17, Apache-2.0); Drake (2026-11-17, BSD-3-Clause); Webots
  (2026-11-16, Apache-2.0); CARLA (2026-11-18, MIT); Gazebo via gazebosim/gz-sim (2026-11-18,
  Apache-2.0); URDF via ros2/urdf (2026-11-02, BSD-3-Clause), since the listed ros/urdf is the
  ROS 1 repo and was archived on 2025-05-31; tf2 via ros2/geometry2 (2026-11-03, BSD-3-Clause);
  kalibr (2024-03-08, BSD-3-Clause); gym is archived (2026-04-08) and points to
  Farama-Foundation/Gymnasium (2026-11-12, MIT); TensorRT OSS (2026-11-16, Apache-2.0; the
  runtime itself is under NVIDIA's licence); image_pipeline (2026-11-04, BSD-3-Clause with
  Apache-2.0 parts); apriltag_ros (2023-03-27, BSD-2-Clause), with AprilRobotics/apriltag
  (2026-08-07, BSD-2-Clause) and the ROS 2 port christianrauch/apriltag_ros (2026-11-01, MIT);
  Open3D (2026-11-13, MIT); grid_map (2026-11-13, BSD-3-Clause); OctoMap (2026-09-26,
  BSD-3-Clause, octovis GPL-2.0); KISS-ICP (2026-05-04, MIT).
- 141 entries are general software with no robot angle (project management, office and
  document tools, git clients, diagram editors, aircraft, energy and satellite tools); they are
  rejected as off topic. General C++ and Python build, test, lint, debug and profiling tools stay
  as index rows for the operations batch. CAD, EDA, firmware (PX4, ArduPilot, F Prime), motor and
  battery electronics and FPGA boards are deferred to Phase 5 (triaged 2026-11-26).
- Robots: astrobee (not in the Atlas) and open-source-rover (the JPL Open Source Rover page).
  CHAMP, deferred here by the Phase 3 notes, is index only: no commit since July 2024.
- Dead on 2026-11-18: fkromer/awesome-ros2, emmjaykay/stanford_self_driving_car_code,
  kubos/kubos, fritzlabs/Awesome-Mobile-Machine-Learning and ildoonet/tf-pose-estimation (GitHub
  404); the AUTOSAR C++14 PDF and a Read the Docs page (404); the Vector W-Model PDF,
  gitlab.apex.ai and gpu-voxels.org (no response; GPU-Voxels' code is still on GitHub);
  robmosys.eu (HTTP 500).
- Moved or renamed: PCDet is now OpenPCDet (the list has both; same repository); Ignition is now
  Gazebo; ros2_tracing moved from GitLab to github.com/ros2/ros2_tracing; llvm-mirror/clang is an
  archived mirror of llvm-project; Thrust and libcudacxx were archived into NVIDIA CCCL.
  ANYbotics archived elevation_mapping and point_cloud_io on 2026-11-16, and Microsoft archived
  vscode-ros on 2025-09-02.
- List errors: CameraRadarFusionNet's description repeats the TUM Roborace stack text; "ROS" and
  "URDF" each name two different links (marked "package template" and "examples" below); two
  different repos are both called lidar_camera_calibration (author in What it is).
- Nothing suspicious: no prompt-like or agent-directed text in the README or CONTRIBUTING.md.

### Localization and State Estimation to Datasets

- Read at commit `dc73ead` (2023-04-30) on 2026-11-18. The task's URL,
  `protontypes/awesome-robotic-tooling`, now redirects to `Ly0n/awesome-robotic-tooling`, the URL
  the registry already holds. This part covers the README from "Localization and State Estimation"
  to "Datasets": 445 entries. No section in it holds only papers.
- Every GitHub and GitLab link (402 repos) was checked with `git ls-remote`, the others with curl.
  **Dead:** orb_slam_2_ros, Labelbox, HybridAStarTrailer, sick_scan, rdbox and AUTOSAR-Adaptive
  return 404; openvslam's code was withdrawn in 2021 and only a notice remains; Papers With Code
  redirects to Hugging Face; the Lyft Level 5 page and the ASTYX blog post do not answer; the
  Atlatec sample-data page redirects to the company site. The Ford AV dataset site now asks for a
  login.
- **Moved:** Scan Context to `gisbi-kim/scancontext`; sick_scan's successor is `sick_scan_xd`;
  gLAB to a new page on the gAGE site; OpenDRIVE to ASAM; `micro-ros.github.io` redirects to
  `micro.vulcanexus.org`; the eCAL link is the Continental org, eCAL now lives at
  `eclipse-ecal/ecal`; Fast-RTPS is now `eProsima/Fast-DDS`; Cartographer is under
  `cartographer-project`; PlotJuggler under the `PlotJuggler` org; the listed
  `sunglok/awesome-robotics-datasets` is the `mint-lab` list triaged on its own.
- Page candidates were checked by shallow clone (last commit, licence file) and, where dormant,
  for a GitHub archive banner. Maintained (commit in 2025-26): robot_localization (BSD-3-Clause),
  slam_toolbox (LGPL-2.1), BehaviorTree.CPP (MIT), MoveIt 2 (BSD-3-Clause), OMPL (BSD-3-Clause),
  Pinocchio (BSD-2-Clause), PlotJuggler (MPL-2.0), micro-ROS (Apache-2.0), Fast DDS (Apache-2.0),
  Cyclone DDS (EPL-2.0 OR BSD-3-Clause), OpenVINS (GPL-3.0, 2025-11-30), MAVROS (BSD-3-Clause OR
  GPL-3.0 OR LGPL-3.0), CloudCompare (GPL-2.0-or-later), jetson-containers (MIT),
  rosbridge_suite (BSD-3-Clause), SROS2 (Apache-2.0) and Open-RMF's `rmf_ros2` (Apache-2.0).
- **Dormant, kept at tier B as historical standards:** VINS-Fusion (2021-07-26, GPL-3.0),
  ORB_SLAM3 (2022-02-10, GPL-3.0), LIO-SAM (2023-04-17, BSD-3-Clause), Cartographer (2024-01-05;
  the `ros2/cartographer_ros` fork 2025-05-24, Apache-2.0). **Archived:** `osrf/rmf_core`
  (2021-07-22; Open-RMF continues it) and `foxglove/studio` (2024-03-11; Foxglove is closed
  source since, and BMW's Lichtblick fork of the last MPL-2.0 code is active).
- **Deferred to Phase 5 (triaged 2026-11-26):** CAN tools, microcontroller and RTOS entries
  (rosserial, micro-ROS for Arduino, ros2arduino, VxWorks), EtherCAT, FPGA, MPC and optimisation
  solvers, and vendor-specific sensor drivers, which belong with their parts. micro-ROS itself
  stays a ROS 2 page, since the brief names its slug.
- **Rejected as off-topic:** consumer car diagnostics and hacking (OBD, UDS, Tesla, opendbc),
  EV charging, satellites and orbits, GIS editing and publishing, music audio, personal dotfiles.
  Generic Linux, container, network and security tools are index only; so are the driving
  datasets, which are benchmarks for cars, not robot-learning data.
- **Suspicious content:** none in the list. BehaviorTree.CPP, PlotJuggler, MoveIt 2, MAVROS,
  jetson-containers and Lichtblick ship `CLAUDE.md`, `AGENTS.md` or `.claude/` files for their own
  contributors; they were not read or followed.

## Pages made

| Entry | Page | Tier |
|---|---|---|
| ROS | [ROS 2](../wiki/tools/ros2.md) | A |
| colcon-core | [colcon](../wiki/tools/colcon.md) | A |
| URDF | [URDF and xacro](../wiki/software/urdf.md) | A |
| tf2 | [tf2](../wiki/software/tf2.md) | A |
| PlotJuggler | [PlotJuggler](../wiki/tools/plotjuggler.md) | A |
| marvros | [MAVROS](../wiki/software/mavros.md) | B |
| Foxglove Studio | [Foxglove](../wiki/tools/foxglove.md) | B |
| Fast-RTPS | [Fast DDS](../wiki/software/fast-dds.md) | B |
| cyclonedds | [Cyclone DDS](../wiki/software/cyclone-dds.md) | B |
| rosbridge_suite | [rosbridge_suite](../wiki/software/rosbridge-suite.md) | B |
| Webots | [Webots](../wiki/tools/webots.md) | B |
| carla | [CARLA](../wiki/tools/carla.md) | B |
| Ignition Robotics | [Gazebo](../wiki/tools/gazebo.md) | A |
| kalibr | [Kalibr](../wiki/software/kalibr.md) | B |
| image_pipeline | [image_pipeline](../wiki/software/image-pipeline.md) | A |
| apriltag_ros | [AprilTag](../wiki/software/apriltag.md) | B |
| open3d | [Open3D](../wiki/software/open3d.md) | A |
| octomap | [OctoMap](../wiki/software/octomap.md) | B |
| KISS-ICP | [KISS-ICP](../wiki/software/kiss-icp.md) | B |
| robot_localization | [robot_localization](../wiki/software/robot-localization.md) | A |
| LIO_SAM | [LIO-SAM](../wiki/software/lio-sam.md) | B |
| cartographer_ros | [Cartographer](../wiki/software/cartographer.md) | B |
| slam_toolbox | [SLAM Toolbox](../wiki/software/slam-toolbox.md) | A |
| VINS-Fusion | [VINS-Fusion](../wiki/software/vins-fusion.md) | B |
| open_vins | [OpenVINS](../wiki/software/openvins.md) | B |
| ORB_SLAM3 | [ORB-SLAM3](../wiki/software/orb-slam3.md) | B |
| CloudCompare | [CloudCompare](../wiki/tools/cloudcompare.md) | B |
| Autoware.Auto | [Autoware](../wiki/software/autoware.md) | B |
| grid_map | [grid_map](../wiki/software/grid-map.md) | B |
| BehaviorTree.CPP | [BehaviorTree.CPP](../wiki/software/behaviortree-cpp.md) | A |
| PythonRobotics | [PythonRobotics](../wiki/software/pythonrobotics.md) | B |
| Drake | [Drake](../wiki/software/drake.md) | A |
| moveit | [MoveIt 2](../wiki/software/moveit2.md) | A |
| ompl | [OMPL](../wiki/software/ompl.md) | A |
| pinocchio | [Pinocchio](../wiki/software/pinocchio.md) | A |
| rmf_core | [Open-RMF](../wiki/software/open-rmf.md) | B |
| jetson-containers | [jetson-containers](../wiki/tools/jetson-containers.md) | B |
| ros2_dds_security | [SROS2](../wiki/software/sros2.md) | B |
| gym | [Gymnasium](../wiki/learning/frameworks/gymnasium.md) | B |
| TensorRT | [TensorRT](../wiki/software/tensorrt.md) | B |
| PX4 | [PX4](../wiki/software/px4.md) | B |
| ArduPilot | [ArduPilot](../wiki/software/ardupilot.md) | B |
| OpenCR | [ROBOTIS OpenCR 1.0](../wiki/parts/mcu/robotis-opencr.md) | B |
| micro-ROS for Arduino | [micro-ROS](../wiki/software/micro-ros.md) | A |
| python-can | [python-can](../wiki/software/python-can.md) | B |
| CANopenNode | [CANopenNode](../wiki/software/canopennode.md) | B |
| can-utils | [can-utils and SocketCAN](../wiki/tools/can-utils.md) | B |
| ros_canopen | [ros2_canopen](../wiki/software/ros2-canopen.md) | B |
| micro-ros | [micro-ROS](../wiki/software/micro-ros.md) | A |

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|
| phobos | `tools/phobos` | B | cad-to-sim | Blender add-on that builds URDF and SDF models from meshes; one of the open CAD-to-sim routes |
| solidworks_urdf_exporter | `tools/solidworks-urdf-exporter` | B | cad-to-sim | SolidWorks add-in, kept under the ROS org, that exports assemblies to URDF; seven Atlas robots publish SolidWorks CAD |
| FreeCAD | `tools/freecad` | A | cad | Open parametric CAD and this workspace's first-class CAD tool, scriptable headless with `freecadcmd` |
| kicad | `tools/kicad` | A | pcb | Open schematic and PCB suite, first-class here; seven Atlas robot pages name KiCad files |
| openscad | `tools/openscad` | B | cad | The classic script-based solid CAD tool, documented here; common for parametric printed parts |
| WireViz | `tools/wireviz` | B | pcb | Draws cable and harness diagrams with a cable BOM from YAML, so a robot's wiring lives in git |
| ODrive | `parts/drivers/odrive-robotics-odrive` | B | actuators | Open BLDC motor controller behind Stanford Doggo; the actuator guide compares it with other BLDC drives |
| casADi | `software/casadi` | A | control | Symbolic modelling and automatic differentiation for MPC and trajectory optimisation, with Ipopt and other solvers |

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| Doxygen | C++ API documentation generator; ROS 2 package docs use it | — | — |
| Sphinx | Python documentation generator; ROS 2 docs are built with it | — | — |
| tesseract | OCR engine; robots use it to read labels and signs | — | — |
| awesome-safety-critical | Awesome list on safety-critical software practice | — | — |
| open-autonomous-safety | Voyage's self-driving safety processes and tests; dormant since 2018 | — | — |
| Automated Valet Parking Safety Documents | Published safety case for an automated-parking trial vehicle | — | — |
| safe_numerics | Boost library of overflow-checked numeric types | — | — |
| Air Vehicle C++ development coding standards | JSF air-vehicle C++ coding rules for safety-critical code | — | — |
| doorstop | Requirements management kept as files in version control | — | — |
| capella | Eclipse model-based systems engineering (MBSE) tool | — | — |
| Papyrus for Robotics | Eclipse model-driven design tool for RobMoSys-style robot software | — | — |
| fossology | Licence and copyright scanner for software releases | — | — |
| Guidelines | ICSE 2020 paper: guidelines for architecting ROS systems | — | — |
| rqt_graph | rqt plugin that draws the ROS node and topic graph | — | — |
| cpp-dependencies | Draws and checks C++ include dependencies | — | — |
| pydeps | Draws Python module dependency graphs | — | — |
| aztarna | Alias Robotics network scanner for exposed ROS hosts; archived 2026 | — | — |
| Architecture_Decision_Record | Templates and examples for architecture decision records | — | — |
| Autoware.ai | ROS 1 Autoware; succeeded by Autoware Core and Universe | — | — |
| OpenPilot | comma.ai driver-assistance software for production cars | — | — |
| Apollo | Baidu's full autonomous-driving software stack | — | — |
| astrobee | Robot; not in the Atlas (NASA's ISS free-flyer software) | — | — |
| CARMAPlatform | US DOT cooperative driving automation platform on ROS | — | — |
| mod_vehicle_dynamics_control | TUM Roborace vehicle control and state estimation; inactive since 2022 | — | — |
| open-source-rover | Robot; on the [JPL Open Source Rover](../wiki/robots/jpl-open-source-rover.md) page | — | — |
| mir_robot | ROS driver and simulation for MiR mobile robots | — | — |
| COMPAS | COMPAS FAB: robotic fabrication tools for architecture | — | — |
| JdeRobot Academy | Course: browser-based robotics exercises with ROS | — | — |
| clover | ROS framework and Raspberry Pi image for PX4 drones | — | — |
| Vim-ros | Vim plugin for ROS 1 development | — | — |
| Visual Studio Code | Code editor most ROS developers use, with ROS extensions | — | — |
| ade-cli | Apex.AI Docker-based development environment manager | — | — |
| Jupyter ROS | Jupyter widgets for ROS and ROS 2 | — | — |
| ros_rqt_plugin | ROS plug-in for the Qt Creator IDE | — | — |
| ROS IDEs | ROS wiki advice on IDE setup (ROS 1) | — | — |
| roslibpy | Python client for rosbridge, no ROS install needed | — | — |
| pybind11 | C++ and Python bindings, used across ROS 2 and robot libraries | — | — |
| vscode-ros | VS Code extension for ROS; Microsoft archived it in 2025 | — | — |
| ROS (package template) | ROS 1 C++ package template from ETH's ROS best practices | — | — |
| Launch | ROS 1 wiki tips for launch files in large projects | — | — |
| URDF (examples) | ROS wiki URDF examples for several kinds of robot | — | — |
| Python | ROS 1 Python style guide | — | — |
| Docker | ADE guide to building a custom base Docker image | — | — |
| VS Code ROS2 Workspace Template | VS Code workspace template for ROS 2 development | — | — |
| qemu-user-static | Runs other-architecture containers, such as ARM images on x86 | — | — |
| bloom | Release tool that sends ROS packages to the build farm | — | — |
| superflore | Generates ROS package recipes for Gentoo and Yocto | — | — |
| catkin_tools | ROS 1 catkin build tool; colcon replaces it in ROS 2 | — | — |
| industrial_ci | CI scripts for ROS and ROS 2 repositories | — | — |
| clang | C and C++ compiler; the linked mirror is archived, see llvm-project | — | — |
| catkin_virtualenv | Bundles Python dependencies into a ROS package via virtualenv | — | — |
| pyenv | Python version manager | — | — |
| aptly | Debian package repository manager for shipping robot software | — | — |
| docker_images | Official ROS, ROS 2 and Gazebo Docker images | — | — |
| robot_upstart | Installs ROS launch files as systemd services | — | — |
| ryo-iso | Builds robot OS install images from a YAML config | — | — |
| rosbuild | ROSCon 2016 talk on the ROS build farm | — | — |
| setup-ros | GitHub Action that installs ROS or ROS 2 for CI | — | — |
| UnitTesting | ROS wiki policy and practice for unit tests (ROS 1) | — | — |
| googletest | C++ test framework that ROS 2 uses through ament | — | — |
| pytest | Python test framework that ROS 2 uses | — | — |
| doctest | Single-header C++ test framework | — | — |
| osrf_testing_tools_cpp | OSRF C++ testing helpers, such as memory tools | — | — |
| code_coverage | ROS package for coverage reports; inactive since 2023 | — | — |
| action-ros-ci | GitHub Action that builds and tests ROS 2 packages | — | — |
| action-ros-lint | GitHub Action that runs ament linters on ROS 2 packages | — | — |
| cppcheck | Static analyser for C and C++ | — | — |
| hadolint | Dockerfile linter | — | — |
| shellcheck | Static analyser for shell scripts | — | — |
| catkin_lint | Checks ROS 1 catkin package configuration | — | — |
| pylint | Python static analyser | — | — |
| black | Python code formatter | — | — |
| haros | Static analysis framework for ROS 1 code | — | — |
| heaptrack | Heap memory profiler for Linux | — | — |
| ros2_tracing | LTTng tracing for ROS 2; moved to github.com/ros2/ros2_tracing | — | — |
| Linuxperf | Brendan Gregg's Linux performance analysis guide | — | — |
| FlameGraph | Flame-graph visualiser for profiler output | — | — |
| gpuvis | GPU trace visualiser | — | — |
| sanitizer | Address, thread and memory sanitizers for C and C++ | — | — |
| Roslaunch Nodes in Valgrind or GDB | ROS 1 tutorial: run nodes under gdb or valgrind | — | — |
| gdb-frontend | Browser-based GUI for gdb | — | — |
| lttng | Linux kernel and user-space tracer; ros2_tracing builds on it | — | — |
| ros2-performance | iRobot framework to benchmark ROS 2 systems | — | — |
| bcc | eBPF tools for Linux performance and IO analysis | — | — |
| tracy | Real-time frame profiler with nanosecond timing | — | — |
| bpftrace | High-level eBPF tracing language | — | — |
| pudb | Console debugger for Python | — | — |
| backward-cpp | Readable C++ stack traces on crash | — | — |
| gdb-dashboard | Modular dashboard for gdb | — | — |
| hotspot | GUI for Linux perf profiles | — | — |
| memory_profiler | Line-by-line Python memory profiler | — | — |
| libstatistics_collector | ROS 2 library for topic and message statistics | — | — |
| dive | Explores Docker image layers, to shrink robot images | — | — |
| dvc | Version control for datasets and models | — | — |
| AI2-THOR | Unity household simulator for embodied-AI research | — | — |
| lgsv | Unity driving simulator; LG ended it in 2022 | — | — |
| awesome-CARLA | Awesome list of CARLA tutorials and projects | — | — |
| ros-bridge | ROS bridge for CARLA; no commit since 2022 | — | — |
| scenario_runner | CARLA traffic-scenario engine | — | — |
| uuv_simulator | Gazebo underwater robot simulation (ROS 1); archived 2023 | — | — |
| AirSim | Microsoft's Unreal-based drone and car simulator | — | — |
| ROSIntegration | Unreal Engine plugin for ROS communication | — | — |
| gym-pybullet-drones | PyBullet Gym environments for quadrotor RL | — | — |
| safe-control-gym | PyBullet benchmark for safe learning-based control | — | — |
| highway-env | Gym environments for driving decision-making | — | — |
| VREP Interface | ROS interface of CoppeliaSim (formerly V-REP) | — | — |
| sumo | Eclipse SUMO road-traffic simulator, often paired with CARLA | — | — |
| open-simulation-interface | ASAM interface standard for driving-simulation sensor data | — | — |
| ESIM | Event-camera simulator; inactive since 2021 | — | — |
| pedsim_ros | Pedestrian crowd simulation for ROS 1 and Gazebo | — | — |
| opencrg | ASAM road-surface description format and tools | — | — |
| esmini | Lightweight OpenSCENARIO player | — | — |
| OpenSceneGraph | 3D graphics toolkit for visual simulation | — | — |
| ROSIntegrationVision | RGB-D data capture from Unreal Engine for ROS | — | — |
| fetch_gazebo | Gazebo models of the [Fetch](../wiki/robots/fetch.md) robot; inactive since 2021 | — | — |
| rotors_simulator | ETH Gazebo multirotor simulator for ROS 1; inactive since 2021 | — | — |
| gnss-ins-sim | GNSS and inertial sensor simulator for navigation testing | — | — |
| simulation assets for the SubT | DARPA SubT Gazebo models; the link now opens the site root | — | — |
| sim_vehicle_dynamics | TUM Roborace vehicle-dynamics simulation; inactive since 2022 | — | — |
| simbody | C++ multibody dynamics library behind OpenSim | — | — |
| gazebo_models | Gazebo Classic model database; Gazebo Fuel replaced it | — | — |
| pylot | Autonomous-driving research platform on CARLA; inactive since 2023 | — | — |
| flightmare | Unity-based quadrotor simulator from UZH; inactive since 2023 | — | — |
| champ | ROS quadruped gait controller; no commit since July 2024 | — | — |
| rex-gym | Gym environments for the SpotMicro quadruped; inactive since 2021 | — | — |
| usv_sim_lsa | Gazebo surface-vessel simulation with wind and currents | — | — |
| Unity-Robotics-Hub | Unity tools and tutorials for robot simulation with ROS | — | — |
| Cloe | Eclipse closed-loop simulation middleware for driving software | — | — |
| OpenCDA | Cooperative driving automation framework on CARLA and SUMO | — | — |
| urdf-viz | Standalone URDF and xacro viewer | — | — |
| urdfpy | Python URDF library; inactive since 2022 | — | — |
| FMPy | Runs FMI co-simulation units in Python | — | — |
| lidar_align | Lidar to pose-sensor extrinsic calibration (ETH) | — | — |
| Calibnet | Learned lidar-camera extrinsic calibration; research code | — | — |
| lidar_camera_calibration | ROS lidar-camera extrinsic calibration (ankitdhall) | — | — |
| ILCC | Lidar-camera calibration using reflectance intensity | — | — |
| easy_handeye | Hand-eye calibration for ROS 1 arms and cameras | — | — |
| imu_utils | IMU noise analysis with Allan variance (ROS 1) | — | — |
| kalibr_allan | Allan-variance tools for Kalibr IMU noise; archived 2022 | — | — |
| pyquaternion | Python quaternion class; inactive since 2020 | — | — |
| robot_calibration | Calibrates camera, joint and frame offsets on ROS robots | — | — |
| multi_sensor_calibration | Calibration of lidar, radar and camera rigs; inactive since 2021 | — | — |
| LiDARTag | Fiducial tag detection in lidar point clouds | — | — |
| multicam_calibration | Multi-camera intrinsic and extrinsic calibration | — | — |
| ikpy | Pure-Python inverse kinematics from URDF | — | — |
| livox_camera_lidar_calibration | Livox lidar to camera extrinsic calibration | — | — |
| lidar_camera_calibration | Lidar-camera calibration with ROS, OpenCV and PCL (heethesh) | — | — |
| e2calib | Event-camera calibration through image reconstruction | — | — |
| SARosPerceptionKitti | ROS perception pipeline evaluated on KITTI; inactive since 2022 | — | — |
| multiple-object-tracking-lidar | Lidar multi-object detection and tracking for ROS | — | — |
| cadrl_ros | Learned dynamic-obstacle avoidance for ROS ground robots | — | — |
| AugmentedAutoencoder | RGB object detection and 6D pose estimation (DLR) | — | — |
| jsk_recognition | JSK lab ROS perception packages | — | — |
| GibsonEnv | Embodied-AI simulator from real scans; succeeded by iGibson and OmniGibson | — | — |
| morefusion | 6D pose estimation by volumetric fusion; archived 2023 | — | — |
| se(3)-TrackNet | 6D object pose tracking from a CAD model | — | — |
| DLIB | C++ toolkit for machine learning and vision, such as face landmarks | — | — |
| finn | Quantised neural-network inference on FPGAs (AMD/Xilinx) | — | — |
| mlflow | Experiment tracking and model registry for ML | — | — |
| Netron | Viewer for neural-network model files such as ONNX | — | — |
| MNN | Alibaba's lightweight on-device inference engine | — | — |
| Dopamine | Google research framework for RL prototyping | — | — |
| ray | Distributed compute framework; RLlib is its RL library | — | — |
| tf-agents | TensorFlow reinforcement-learning library | — | — |
| modelzoo | Autoware's trained models for driving; inactive since 2023 | — | — |
| dask | Parallel task scheduling for Python | — | — |
| cupy | NumPy-compatible arrays on CUDA GPUs | — | — |
| Thrust | C++ GPU parallel algorithms; archived, now part of NVIDIA CCCL | — | — |
| ArrayFire | General-purpose GPU computing library | — | — |
| OpenMP | Shared-memory parallelism API for C and C++ | — | — |
| VexCL | C++ vector expressions for OpenCL and CUDA | — | — |
| numba | JIT compiler for numeric Python on CPU and GPU | — | — |
| gstreamer | Media pipeline framework, used for camera streaming | — | — |
| ros2_openvino_toolkit | Intel OpenVINO inference nodes for ROS 2 | — | — |
| vision_visp | ROS wrapper of ViSP visual tracking and servoing | — | — |
| deep_object_pose | NVIDIA DOPE: 6D pose of known objects from RGB | — | — |
| DetectAndTrack | Video human-pose tracking research code; archived 2021 | — | — |
| SfMLearner | Self-supervised depth and ego-motion research code | — | — |
| imgaug | Image augmentation library; inactive since 2020 | — | — |
| vision_opencv | cv_bridge and image_geometry: the ROS bridge to OpenCV | — | — |
| darknet_ros | YOLO v3 detection for ROS 1; inactive since 2021 | — | — |
| find-object | Qt tool to try feature detectors and find objects (ROS) | — | — |
| yolact | Real-time instance segmentation research code | — | — |
| Kimera-Semantics | 3D semantic reconstruction from MIT SPARK; inactive since 2021 | — | — |
| detectron2 | Meta's detection and segmentation library | — | — |
| OpenVX | Khronos API for accelerated embedded vision | — | — |
| 3d-vehicle-tracking | Monocular 3D vehicle detection and tracking research code | — | — |
| pysot | Visual object tracking research codebase | — | — |
| kitti_scan_unfolding | Lidar semantic segmentation study code on KITTI scans | — | — |
| packnet-sfm | TRI self-supervised monocular depth research code | — | — |
| AB3DMOT | Simple 3D multi-object tracking baseline | — | — |
| monoloco | Monocular 3D pedestrian localisation research code | — | — |
| Poly-YOLO | YOLOv3 variant with polygon segmentation; inactive since 2021 | — | — |
| LEDNet | Lightweight real-time semantic segmentation research code | — | — |
| TorchSeg | PyTorch semantic segmentation models; inactive since 2020 | — | — |
| simpledet | Object detection framework; inactive since 2021 | — | — |
| meshroom | Photogrammetry app that builds 3D models from photos | — | — |
| EasyOCR | Deep-learning OCR library for many languages | — | — |
| pytracking | PyTorch visual object tracking framework | — | — |
| ros_deep_learning | Jetson inference nodes for ROS and ROS 2 | — | — |
| hyperpose | Real-time human pose estimation library; inactive since 2021 | — | — |
| Cam2BEV | Bird's-eye-view segmentation from vehicle cameras | — | — |
| flownet2-pytorch | PyTorch FlowNet 2 optical flow | — | — |
| Simd | SIMD-optimised C++ image processing library | — | — |
| AliceVision | Photogrammetry framework behind Meshroom | — | — |
| CameraRadarFusionNet | TUM camera-radar fusion network for object detection | — | — |
| cilantro | Lean C++ point-cloud library | — | — |
| SqueezeSeg | Early CNN lidar segmentation research code; inactive since 2019 | — | — |
| libpointmatcher | Modular ICP library for 2D and 3D mapping | — | — |
| depth_clustering | Fast range-image clustering of Velodyne point clouds | — | — |
| lidar-bonnetal | RangeNet++ lidar semantic segmentation; archived 2024 | — | — |
| CSF | Cloth-simulation ground filter for lidar | — | — |
| robot_body_filter | Removes the robot's own body from laser and point-cloud data | — | — |
| elevation_mapping | ANYbotics robot-centric elevation mapping; archived 2026 | — | — |
| rangenet_lib | TensorRT C++ inference for RangeNet++ | — | — |
| pointcloud_to_laserscan | Converts 3D point clouds to 2D laser scans | — | — |
| gpu-voxels | CUDA voxel collision checking (FZI); website down, code on GitHub | — | — |
| spatio_temporal_voxel_layer | Nav2 costmap layer for 3D sensor data with decay | — | — |
| LAStools | Tools for airborne lidar LAS and LAZ files | — | — |
| PCDet | Lidar 3D object detection toolbox, now named OpenPCDet | — | — |
| PDAL | Point-cloud data translation library, mainly geospatial | — | — |
| PotreeConverter | Converts point clouds for web viewing in Potree | — | — |
| fast_gicp | Fast GICP and VGICP point-cloud registration | — | — |
| ndt_omp | Multi-threaded NDT registration | — | — |
| laser_line_extraction | Line extraction from 2D laser scans; inactive since 2021 | — | — |
| Go-ICP | Globally optimal ICP registration research code | — | — |
| PointCNN | Point-cloud feature-learning research code | — | — |
| MotionNet | BEV perception and motion prediction research code | — | — |
| PolarSeg | Polar-grid lidar segmentation research code | — | — |
| traversability_mapping | Lidar traversability map for navigation; inactive since 2020 | — | — |
| lidar_super_resolution | Lidar super-resolution trained in simulation; inactive since 2021 | — | — |
| Cupoch | CUDA point-cloud and robotics library, similar to Open3D | — | — |
| linefit_ground_segmentation | Line-fit ground segmentation for lidar | — | — |
| Draco | Google mesh and point-cloud compression | — | — |
| Votenet | 3D detection by Hough voting, research code; archived 2023 | — | — |
| lidar_undistortion | Lidar motion undistortion from an external pose estimate | — | — |
| superpoint_graph | Large-scale point-cloud segmentation research code | — | — |
| RandLA-Net | Efficient large-scale point-cloud segmentation research code | — | — |
| Det3D | 3D object detection toolbox; inactive since 2023 | — | — |
| OverlapNet | Lidar loop-closure detection network (PRBonn) | — | — |
| mp2p_icp | Multi-primitive ICP library used by MOLA | — | — |
| torch-points3d | PyTorch point-cloud deep learning; inactive since 2021 | — | — |
| PolyFit | Polygonal surface reconstruction from point clouds | — | — |
| mmdetection3d | OpenMMLab 3D detection toolbox | — | — |
| gpd | Grasp pose detection from point clouds; inactive since 2021 | — | — |
| SalsaNext | Uncertainty-aware lidar semantic segmentation | — | — |
| Super-Fast-Accurate-3D-Object-Detection | Fast lidar 3D object detection research code | — | — |
| kaolin | NVIDIA PyTorch library for 3D deep learning | — | — |
| CamVox | Low-cost SLAM with a camera and a Livox lidar | — | — |
| SA-SSD | Structure-aware single-stage 3D detection research code | — | — |
| cuda-pcl | NVIDIA CUDA-accelerated PCL functions for Jetson | — | — |
| urban_road_filter | Lidar road and sidewalk detection | — | — |
| Removert | Removes dynamic points to build static lidar maps | — | — |
| evo | Python tool to evaluate odometry and SLAM trajectories | — | — |
| fuse | Factor-graph sensor-fusion framework for ROS from Locus Robotics | — | — |
| GeographicLib | Geodesy and map-projection library; the link is an unofficial mirror | — | — |
| ntripbrowser | Python API to browse NTRIP casters for RTK corrections | — | — |
| imu_tools | ROS IMU filters (Madgwick, complementary) and an RViz plugin | — | — |
| RTKLIB | RTK GNSS processing; a fork tuned for low-cost u-blox receivers | — | — |
| gLAB | UPC's GNSS positioning and analysis suite; its page moved | — | — |
| ai-imu-dr | Research code: IMU-only dead reckoning for cars | — | — |
| Kalman-and-Bayesian-Filters-in-Python | Free Jupyter book on Kalman and Bayesian filters | — | — |
| mcl_3dl | ROS Monte Carlo localisation with 3D lidar | — | — |
| se2lam | Research code: odometry-plus-vision SLAM for ground vehicles | — | — |
| dynamic_robot_localization | ROS point-cloud localisation with map updates through OctoMap | — | — |
| eagleye | GNSS and IMU vehicle localisation from MAP IV, used with Autoware | — | — |
| PROJ | Standard library for map projections and coordinate transforms | — | — |
| rpg_trajectory_evaluation | UZH tools to evaluate visual-inertial odometry trajectories | — | — |
| pymap3d | Pure-Python geodetic coordinate conversions (ECEF, ENU, geodetic) | — | — |
| libRSF | Robust factor-graph sensor-fusion library for online localisation | — | — |
| loam_velodyne | Community copy of the original LOAM lidar odometry; ROS 1 | — | — |
| lio-mapping | Research code: tightly coupled lidar-inertial odometry and mapping | — | — |
| A-LOAM | Clean LOAM reimplementation with Ceres; a common teaching baseline | — | — |
| Fast LOAM | Faster LOAM variant for lidar odometry and mapping | — | — |
| loam_livox | LOAM adapted to Livox solid-state lidars | — | — |
| StaticMapping | Lidar mapping that removes dynamic objects; one developer | — | — |
| semantic_suma | Research code: surfel mapping with semantic segmentation | — | — |
| maplab | ETH visual-inertial mapping and map-merging framework | — | — |
| hdl_graph_slam | Popular ROS 1 graph SLAM for 3D lidars | — | — |
| interactive_slam | GUI to correct lidar pose graphs by hand | — | — |
| LeGO-LOAM | Ground-optimised LOAM for ground vehicles; LIO-SAM succeeds it | — | — |
| pyslam | Python visual odometry and SLAM framework for learning | — | — |
| Kitware SLAM | Kitware's lidar SLAM with ROS and LidarView integration | — | — |
| horizon_highway_slam | Livox highway SLAM for the Horizon lidar | — | — |
| mola | Modular localisation and mapping framework with ROS 2 lidar odometry | — | — |
| DH3D | Research code: learned 3D descriptors for relocalisation | — | — |
| LaMa | Lightweight C++ 2D localisation and mapping library | — | — |
| Scan Context | Lidar place-recognition descriptor for loop closure; repo moved | — | — |
| M-LOAM | Research code: multi-lidar odometry with online extrinsic calibration | — | — |
| orbslam-map-saving-extension | Map saving for ORB-SLAM2; ORB-SLAM3 saves maps itself | — | — |
| dso | Direct Sparse Odometry, a landmark monocular method from TUM | — | — |
| viso2 | ROS wrapper for the libviso2 stereo visual odometry | — | — |
| xivo | Research visual-inertial odometry from UCLA | — | — |
| rovio | ETH filter-based visual-inertial odometry; a classic baseline | — | — |
| LSD-SLAM | Landmark direct monocular SLAM from TUM; ROS 1 era | — | — |
| CubeSLAM and ORB SLAM | Research code: monocular 3D object detection with SLAM | — | — |
| basalt | TUM visual-inertial odometry and mapping | — | — |
| Kimera | MIT metric-semantic SLAM that builds labelled 3D meshes | — | — |
| tagslam | ROS SLAM with AprilTag fiducials | — | — |
| LARVIO | Lightweight MSCKF monocular visual-inertial odometry | — | — |
| fiducials | Ubiquity Robotics ROS SLAM with fiducial markers | — | — |
| Atlas | Research code: 3D scene reconstruction from posed images | — | — |
| vilib | CUDA front end for visual-inertial pipelines | — | — |
| hloc | Toolbox for 6-DoF visual localisation with retrieval and matching | — | — |
| ESVO | Research code: stereo event-camera visual odometry | — | — |
| gradslam | Differentiable dense SLAM in PyTorch | — | — |
| OpenDRIVE | ASAM file format for road networks; the link redirects to ASAM | — | — |
| Lanelet2 | Lane-level map framework for automated driving, used by Autoware | — | — |
| barefoot | BMW's matching of GPS traces to road maps | — | — |
| segmap | ETH research map representation built from 3D segments | — | — |
| Mapbox | Web vector-map library; proprietary since v2, MapLibre is the open fork | — | — |
| osrm-backend | Open Source Routing Machine: road routing on OpenStreetMap data | — | — |
| assuremapingtools | Desktop editor for Autoware road-network maps | — | — |
| geopandas | Geographic data support for pandas | — | — |
| MapToolbox | Unity plugins to build Autoware vector maps | — | — |
| gdal | Standard library for raster and vector geodata formats | — | — |
| 3d-tiles | Open spec for streaming large 3D geospatial datasets | — | — |
| osmnx | Python tool to fetch and analyse OpenStreetMap street networks | — | — |
| Awesome-Interaction-aware-Trajectory-Prediction | Awesome list of trajectory-prediction papers and datasets | — | — |
| sgan | Research code: Social GAN pedestrian trajectory prediction | — | — |
| Groot | BehaviorTree.CPP editor; superseded by Groot2, which is not open source | — | — |
| RAFCON | DLR hierarchical state-machine tool with a graphical editor | — | — |
| ROSPlan | ROS 1 PDDL task planning; PlanSys2 covers ROS 2 | — | — |
| ad-rss-lib | Intel's Responsibility-Sensitive Safety model for automated vehicles | — | — |
| FlexBE | Hierarchical state-machine behaviour engine with a GUI for ROS | — | — |
| sts_bt_library | Small behaviour-tree library from an autonomous-logistics project | — | — |
| SMACC | ROS 1 event-driven state-machine library; SMACC2 is the ROS 2 one | — | — |
| py_trees_ros | ROS bindings for py_trees, the Python behaviour-tree library | — | — |
| pacmod | ROS 1 driver for PACMod drive-by-wire cars; pacmod3 replaces it | — | — |
| rrt | Small C++ RRT implementation | — | — |
| path_planner | Hybrid A* path planner for car-like vehicles; ROS 1 | — | — |
| open_street_map | ROS 1 packages for OpenStreetMap data | — | — |
| Open Source Car Control | PolySync's open drive-by-wire hardware and firmware for cars | — | — |
| fastrack | ROS implementation of FaSTrack safe trajectory tracking | — | — |
| commonroad | TUM benchmarks and tools for on-road motion planning | — | — |
| traffic-editor | Open-RMF traffic-lane editor; now rmf_traffic_editor | — | — |
| steering_functions | Steering functions (Dubins, Reeds-Shepp) for car-like robots | — | — |
| flexible-collision-library | FCL, the collision and distance library under MoveIt | — | — |
| aikido | Personal Robotics Lab planning and control library | — | — |
| CrowdNav | Research code: crowd-aware navigation with deep RL | — | — |
| openrave | Historic planning environment, still known for its IKFast solver generator | — | — |
| teb_local_planner | Timed-elastic-band local planner from ROS 1 navigation | — | — |
| global_racetrajectory_optimization | TUM global race-line optimisation methods | — | — |
| toppra | Time-optimal path parametrisation under kinematic and dynamic limits | — | — |
| tinyspline | Small library for B-splines and NURBS | — | — |
| dual quaternions ros | Small ROS Python package for dual-quaternion interpolation | — | — |
| mb planner | Motion-primitive aerial planner from the DARPA SubT challenge | — | — |
| EGO-Planner | ZJU gradient-based local planner for quadrotors | — | — |
| am_traj | Research code: aggressive quadrotor trajectory generation | — | — |
| GraphBasedLocalTrajectoryPlanner | TUM graph-based local planner for race cars | — | — |
| se2_navigation | ETH pure-pursuit and Reeds-Shepp planning in SE(2) | — | — |
| Ruckig | Jerk-limited online trajectory generation, used inside MoveIt 2 | — | — |
| imgui | Immediate-mode C++ GUI library for tools and debug views | — | — |
| qtpy | Shim to write Python Qt code once for all bindings | — | — |
| rqt | Qt GUI plugin framework of ROS; covered by the ROS 2 pages | — | — |
| cage | Wayland kiosk compositor that runs one full-screen app | — | — |
| chilipie | Raspberry Pi image that boots into a Chrome kiosk | — | — |
| dynamic_reconfigure | ROS 1 runtime parameter changes; ROS 2 parameters replace it | — | — |
| ddynamic_reconfigure | ROS 1 dynamic_reconfigure without .cfg files | — | — |
| elements | Lightweight modular C++ GUI library | — | — |
| NanoGUI | Minimal OpenGL widget library | — | — |
| pyo | Python audio signal-processing module | — | — |
| rhasspy | Offline voice-assistant toolkit | — | — |
| mycroft-core | Open voice assistant; discontinued, OpenVoiceOS continues it | — | — |
| DeepSpeech | Mozilla's speech-to-text engine; discontinued | — | — |
| waveglow | NVIDIA flow-based speech-synthesis model from 2018 | — | — |
| TTS | Coqui text-to-speech toolkit; Coqui closed, Idiap keeps a fork | — | — |
| the-art-of-command-line | One-page guide to the command line | — | — |
| dotbot | Tool to bootstrap dotfiles | — | — |
| ag | Fast code search; ripgrep has largely replaced it | — | — |
| fzf | Command-line fuzzy finder | — | — |
| pkgtop | Terminal package manager and resource monitor | — | — |
| asciimatics | Python library for text UIs and ASCII animations | — | — |
| gocui | Go library for console user interfaces | — | — |
| TerminalImageViewer | Shows images in a terminal | — | — |
| rosshow | Shows ROS 1 topics as terminal graphics | — | — |
| python-prompt-toolkit | Python library for interactive command-line apps | — | — |
| guake | Drop-down terminal for GNOME | — | — |
| wemux | Multi-user tmux sessions | — | — |
| tmuxp | tmux session manager driven by YAML configs | — | — |
| terminator | Terminal emulator that tiles terminals | — | — |
| bat | cat clone with syntax highlighting | — | — |
| fx | Terminal JSON viewer | — | — |
| tmate | Instant terminal sharing over SSH | — | — |
| xdot | Interactive viewer for Graphviz dot graphs | — | — |
| guacamole | Browser-based remote desktop gateway (VNC, RDP, SSH) | — | — |
| ros3djs | JavaScript 3D visualisation for ROS over rosbridge | — | — |
| webviz | Cruise's web ROS visualiser; Foxglove Studio forked and replaced it | — | — |
| plotly.py | Interactive plotting library for Python | — | — |
| bokeh | Browser-based interactive plotting from Python | — | — |
| voila | Turns Jupyter notebooks into web dashboards | — | — |
| Pangolin | Lightweight OpenGL viewer library, used by ORB-SLAM | — | — |
| rqt_bag | rqt plugin to view and replay bag files | — | — |
| kepler.gl | Web tool to visualise large geospatial datasets | — | — |
| qgis_ros | Shows ROS bag and live data in QGIS; ROS 1 | — | — |
| openmct | NASA's web mission-control framework | — | — |
| web_video_server | Streams ROS image topics over HTTP | — | — |
| RVizWeb | Early OSRF web app with RViz-like features | — | — |
| octave | GNU numerical computing language, largely MATLAB-compatible | — | — |
| streetscape.gl | Uber's toolkit to visualise autonomy data in XVIZ | — | — |
| urdf-loaders | Loads URDF robots into three.js and Unity | — | — |
| obs-studio | Screen recording and live streaming | — | — |
| K3D-tools | Jupyter extension for 3D visualisation | — | — |
| PyQtGraph | Fast plotting and GUI widgets for Python Qt | — | — |
| ipygany | 3D scientific visualisation in Jupyter | — | — |
| ROS-Mobile | Android app to view and drive ROS robots | — | — |
| PixelAnnotationTool | Quick pixel-level image annotation tool | — | — |
| LabelImg | Bounding-box image labeller; moved into Label Studio | — | — |
| cvat | Widely used open annotation tool for images and video | — | — |
| point_labeler | Labelling tool for point clouds and point-cloud sequences | — | — |
| label-studio | Multi-type data labelling tool | — | — |
| napari | Fast multi-dimensional image viewer for Python | — | — |
| semantic-segmentation-editor | Web labelling tool for 2D and 3D segmentation | — | — |
| 3d-bat | 3D bounding-box annotation for point clouds and images | — | — |
| labelme | Polygon image annotation in Python | — | — |
| universal-data-tool | Web or desktop tool to label many data types | — | — |
| BMW-Labeltool-Lite | Simple bounding-box labelling tool from BMW | — | — |
| 3d-annotation-tool | Point-cloud annotation with boxes and keypoints, from Stray Robots | — | — |
| Potree | WebGL viewer for very large point clouds | — | — |
| point_cloud_viewer | Google's viewer for massive point clouds | — | — |
| LidarView | Kitware real-time viewer and processor for live lidar data | — | — |
| VeloView | Velodyne-only predecessor of LidarView | — | — |
| entwine | Organises massive point clouds for streaming | — | — |
| polyscope | C++ and Python viewer for meshes and point clouds | — | — |
| Pcx | Point-cloud importer and renderer for Unity | — | — |
| ImmersivePoints | Web VR viewer for 3D point data | — | — |
| mapviz | Modular 2D map visualisation for ROS, suited to outdoor robots | — | — |
| rviz_cinematographer | Tools to script RViz camera paths for videos | — | — |
| rviz_satellite | Satellite imagery tiles in RViz | — | — |
| rviz_visual_tools | C++ helpers to draw markers in RViz | — | — |
| xpp | Visualises legged-robot motion plans in RViz | — | — |
| rviz stereo | ROS 1 tutorial for stereo 3D rendering in RViz | — | — |
| jsk_visualization | JSK RViz and rqt plugins; ROS 1 | — | — |
| moveit_visual_tools | Helpers to show MoveIt data in RViz | — | — |
| rosmon | ROS 1 launcher and monitoring daemon | — | — |
| multimaster_fkie | FKIE GUI to manage ROS launch configurations and nodes | — | — |
| collectd | System metrics collection daemon | — | — |
| lnav | Log file viewer that understands timestamps and levels | — | — |
| htop | Interactive process viewer | — | — |
| atop | Linux system monitor with logging and replay | — | — |
| psutil | Python process and system monitoring library | — | — |
| gputil | Python GPU status through nvidia-smi | — | — |
| gpustat | Command-line GPU status | — | — |
| nvtop | htop-like GPU monitor | — | — |
| ShellHub | Central SSH access to remote Linux devices | — | — |
| Sshwifty | Web SSH and Telnet client | — | — |
| spdlog | Fast C++ logging library | — | — |
| ctop | top-like view of container metrics | — | — |
| ntop | Web network-traffic monitor (ntopng) | — | — |
| jupyterlab-nvdashboard | JupyterLab dashboards of GPU use | — | — |
| ncdu | Disk usage analyser with an ncurses UI | — | — |
| borg | Deduplicating, encrypted backup tool | — | — |
| bag-database | Web catalogue for ROS bag files | — | — |
| marv-robotics | Robot data management platform | — | — |
| kitti2bag | Converts KITTI data to ROS 1 bags | — | — |
| pykitti | Python tools for KITTI data | — | — |
| rosbag_editor | GUI to make a filtered copy of a rosbag | — | — |
| nextcloud | Self-hosted file hosting and sync server | — | — |
| ros_type_introspection | Deserialises unknown ROS 1 messages at runtime | — | — |
| syncthing | Continuous peer-to-peer file sync | — | — |
| rqt_bag_exporter | Exports ROS bag topics to CSV or video | — | — |
| xviz | Uber's protocol to stream and visualise autonomy data | — | — |
| kitti_to_rosbag | ETH tool to convert KITTI raw data to ROS bags | — | — |
| ros_numpy | Converts ROS messages to and from NumPy arrays | — | — |
| kitti_ros | ROS player that replays KITTI | — | — |
| DuckDB | Embedded analytical SQL database | — | — |
| sshfs | Mounts remote folders over SSH; the linked repo is the macOS fork | — | — |
| moosefs | Scalable distributed file system | — | — |
| ceph | Distributed object, block and file storage | — | — |
| nfs | NFS client library (libnfs) | — | — |
| ansible-role-nfs | Ansible role that installs NFS | — | — |
| mass | Canonical MAAS: bare-metal server provisioning | — | — |
| polyaxon | Platform to manage machine-learning experiments | — | — |
| localstack | Local emulator of AWS cloud services | — | — |
| nvidia-docker | GPU Docker containers; replaced by the NVIDIA Container Toolkit | — | — |
| kubeflow | Machine-learning toolkit for Kubernetes | — | — |
| log-pilot | Log collector for Docker containers | — | — |
| traefik | Reverse proxy and load balancer for containers | — | — |
| graylog2-server | Log management server | — | — |
| ansible | Agentless configuration and deployment automation | — | — |
| pyinfra | Python infrastructure automation and deployment | — | — |
| docker-py | Python client for the Docker Engine API | — | — |
| noVNC | VNC client in the browser | — | — |
| Slurm | Cluster workload manager | — | — |
| jupyterhub | Multi-user Jupyter notebook server | — | — |
| Portainer | Web UI to manage Docker | — | — |
| enroot | NVIDIA tool to run container images as unprivileged sandboxes | — | — |
| docker-firefox | Firefox in Docker with noVNC access | — | — |
| luigi | Python pipeline manager for batch jobs | — | — |
| triton-inference-server | NVIDIA server for GPU model inference | — | — |
| cudf | GPU DataFrame library with a pandas-like API | — | — |
| Yocto | Build system for custom embedded Linux distributions | — | — |
| bitbake | Task engine behind Yocto and OpenEmbedded | — | — |
| Jailhouse | Partitioning hypervisor for Linux, for isolated real-time cells | — | — |
| Xen | Type-1 hypervisor | — | — |
| QEMU | Machine emulator and virtualiser | — | — |
| meta-ros | OpenEmbedded layer that builds ROS into Yocto images | — | — |
| meta-balena | balenaOS layer to run containers on embedded devices | — | — |
| nvidia-container-runtime | GPU-aware OCI runtime; folded into the NVIDIA Container Toolkit | — | — |
| jetson_easy | Script to set up NVIDIA Jetson boards | — | — |
| docker-jetpack-sdk | Runs the NVIDIA JetPack SDK in Docker | — | — |
| Pressed | Debian preseeding for unattended installs | — | — |
| jetson_stats | jtop: monitor and control NVIDIA Jetson boards | — | — |
| ros_jetson_stats | Publishes jetson_stats as ROS diagnostics | — | — |
| acrn-hypervisor | Embedded hypervisor for mixed-criticality systems | — | — |
| ELISA | Linux Foundation project for safety-critical Linux | — | — |
| PREEMPT_RT kernel patch | Real-time Linux patch set; in mainline since Linux 6.12 | — | — |
| performance_test | Apex.AI benchmark for pub/sub middleware | — | — |
| realtime_support | ROS 2 utilities to measure real-time jitter and latency | — | — |
| ros1_bridge | Bridges ROS 1 and ROS 2; ROS 1 reached end of life | — | — |
| protobuf | Google's data serialisation format | — | — |
| opensplice | ADLINK's community DDS edition; no longer a ROS 2 middleware | — | — |
| iceoryx | Eclipse zero-copy shared-memory IPC middleware | — | — |
| eCAL | Continental's pub/sub middleware, now Eclipse eCAL | — | — |
| mqtt_bridge | Bridges ROS 1 and MQTT | — | — |
| netplan | YAML network configuration for Ubuntu | — | — |
| wavemon | ncurses Wi-Fi monitor | — | — |
| wireless | Clearpath ROS package that publishes Wi-Fi status | — | — |
| ptpd | PTP (IEEE 1588) clock-sync daemon | — | — |
| iperf | Network bandwidth measurement | — | — |
| tcpreplay | Edits and replays pcap captures | — | — |
| nethogs | Bandwidth use per process | — | — |
| pyshark | Python wrapper for tshark packet parsing | — | — |
| pingtop | Pings many hosts in a top-like view | — | — |
| termshark | Terminal UI for tshark | — | — |
| udpreplay | Replays UDP packets from pcap files | — | — |
| pacmod3 | ROS driver for PACMod 3 drive-by-wire in cars | — | — |
| crazyflie_ros | ROS 1 driver for the [Crazyflie](../wiki/robots/crazyflie.md); Crazyswarm2 replaces it | — | — |
| spot_ros | ROS 1 driver for [Spot](../wiki/robots/boston-dynamics-spot.md); spot_ros2 serves ROS 2 | — | — |
| owasp-threat-dragon-desktop | OWASP threat-modelling tool; now in OWASP/threat-dragon | — | — |
| launch_ros_sandbox | ROS 2 launch of nodes in sandboxes such as Docker | — | — |
| wolfssl | Small TLS library for embedded devices | — | — |
| RSF | Alias Robotics robot security assessment methodology | — | — |
| How-to-Secure-A-Linux-Server | Guide to hardening a Linux server | — | — |
| lynis | Security auditing and hardening checks for Unix systems | — | — |
| OpenVPN | VPN daemon | — | — |
| openfortivpn | Client for Fortinet SSL VPNs | — | — |
| WireGuard | Modern in-kernel VPN | — | — |
| ssh-auditor | Scans a network for weak SSH passwords | — | — |
| vulscan | Nmap vulnerability scanning script | — | — |
| nmap-vulners | Nmap script for Vulners.com vulnerability lookup | — | — |
| brutespray | Tries default credentials on discovered services | — | — |
| fail2ban | Bans hosts after repeated authentication failures | — | — |
| DependencyCheck | OWASP scanner for known-vulnerable dependencies | — | — |
| Firejail | Linux namespace sandbox for untrusted programs | — | — |
| RVD | Alias Robotics robot vulnerability database | — | — |
| Security-Enhanced Linux | SELinux mandatory access control | — | — |
| bandit | Security linter for Python code | — | — |
| hardening | Ubuntu server hardening script | — | — |
| Passbolt | Team password manager (Docker image) | — | — |
| gopass | Command-line team password manager | — | — |
| pass | Standard Unix password manager | — | — |
| Vault | HashiCorp secrets manager; source-available (BSL) since 2023 | — | — |
| legion | Semi-automated network penetration-testing framework | — | — |
| openscap | SCAP compliance scanning tool | — | — |
| KITTI-360 | Driving dataset with 360-degree images and lidar; its scripts repo | — | — |
| waymo_ros | ROS package to replay the Waymo Open Dataset | — | — |
| waymo-open-dataset | Waymo's large driving dataset and tools | — | — |
| Ford Autonomous Vehicle Dataset | Ford multi-season driving dataset; the site now asks for a login | — | — |
| awesome-robotics-datasets | Awesome list of robotics datasets; triaged as `awesome-robotics-datasets` | — | — |
| nuscenes-devkit | Devkit for the nuScenes driving dataset | — | — |
| dataset-api | Toolkit for the ApolloScape driving dataset | — | — |
| utbm_robocar_dataset | Long-term multi-sensor driving dataset from UTBM | — | — |
| DBNet | Driving-behaviour learning dataset | — | — |
| argoverse-api | Argoverse 1 API; av2-api serves Argoverse 2 | — | — |
| DDAD | TRI long-range dense-depth driving benchmark | — | — |
| pandaset-devkit | Devkit for the PandaSet driving dataset from Hesai and Scale | — | — |
| a2d2_to_ros | Converts Audi's A2D2 dataset to ROS bags | — | — |
| adas-dataset-form | FLIR thermal driving dataset (sign-up form) | — | — |
| h3d | Honda 3D multi-object detection and tracking driving dataset | — | — |
| Mapillary Vistas Dataset | Street-level images with pixel-accurate semantic labels | — | — |
| TensorFlow Datasets | Catalogue of ready-to-use datasets for TensorFlow | — | — |
| racetrack-database | Centre lines, widths and race lines for 20+ race tracks | — | — |
| BlenderProc | Blender pipeline for photorealistic synthetic training images | — | — |
| holicity | City-scale 3D structure dataset | — | — |
| Objectron | Google object-centric videos with 3D boxes and AR poses | — | — |
| ONCE dataset | Large driving dataset with 2D and 3D annotations | — | — |
| F Prime | NASA JPL component framework for embedded flight software | 2026-11-24 | Apache-2.0 |
| PcbDraw | Renders KiCad boards as 2D drawings for pinout diagrams; a KiCad helper | 2026-10-09 | MIT |
| kicad-3rd-party-tools | List of tools that extend KiCad; moved from xesscorp to devbisme | 2026-05-15 | — |
| LibrePCB | Open schematic and PCB editor; KiCad is the first-class EDA tool here | 2026-11-25 | GPL-3.0 |
| ngspice | Open SPICE circuit simulator; KiCad's schematic editor runs it, so the KiCad page covers it | 2026-11-22 | BSD-3-Clause, some files other |
| riscv | RISC-V open instruction set, found in MCUs such as the ESP32-C series; the link is riscv.org | — | — |
| Horizon | Open PCB design suite with integrated part management | 2026-11-17 | GPL-3.0 |
| foxBMS | Fraunhofer IISB open battery-management platform; foxBMS 1 is unsupported, foxbms-2 continues it | 2024-04-05 | — |
| PYNQ | Python framework for AMD/Xilinx Zynq FPGA boards | 2026-09-29 | BSD-3-Clause |
| mpcc | Model predictive contouring control for autonomous racing; research code in C++ and MATLAB | 2021-11-11 | Apache-2.0 |
| ACADO Toolkit | Automatic control and dynamic optimisation with C code generation for MPC; inactive since 2023 | 2023-12-06 | LGPL-3.0 |
| control-toolbox | ETH ADRL C++ library for optimal control, estimation and MPC; inactive since 2021 | 2021-07-05 | BSD-2-Clause |
| OpEn | Embedded nonconvex optimisation solver in Rust with code generation | 2026-03-31 | MIT OR Apache-2.0 |
| autogenu-jupyter | C/GMRES nonlinear MPC solvers with a code generator; moved to ohtsukalab | 2026-09-09 | MIT |
| vxworks7-ros2-build | Builds ROS 2 for Wind River's commercial VxWorks 7 RTOS | 2026-11-21 | Apache-2.0 |
| qemu-xilinx | AMD/Xilinx fork of QEMU that models its SoC and FPGA platforms | 2026-10-20 | GPL-2.0 |
| rosserial | ROS 1 serial link for MCUs such as Arduino; micro-ROS (`software/micro-ros`) replaces it | 2021-06-16 | BSD |
| fusesoc | Package manager and build tool for FPGA and ASIC cores | 2026-11-25 | BSD-2-Clause |
| SOES | EtherCAT slave stack in C, for building EtherCAT devices; SOEM is its master-side sibling | 2026-11-19 | GPL-2.0 with linking exception |
| ros_ethercat | Shadow Robot's ROS 1 EtherCAT main loop; ROS 2 users have ICube's ethercat_driver_ros2 | 2024-05-02 | BSD-2-Clause |
| awesome CAN | Awesome list of CAN tools and hardware; ingested as its own source, `sources/awesome-canbus.md` | 2026-11-17 | CC0-1.0 |
| libuavcan | UAVCAN (now Cyphal) C++ stack, now libcyphal, which its README calls a work in progress | 2025-12-17 | MIT |
| cantools | Python CAN tools: DBC parsing, message encoding and a bus monitor | 2026-11-20 | MIT |
| CANdevStudio | Qt GUI to simulate and analyse CAN traffic | 2024-05-01 | MPL-2.0 |
| kvaser_interface | AutonomouStuff ROS and ROS 2 driver for Kvaser CAN adapters; inactive since 2022 | 2022-08-23 | MIT |
| canmatrix | Converts between CAN database formats (DBC, ARXML, KCD and more) | 2026-11-24 | BSD-2-Clause |
| canopen | Python CANopen library for talking to CANopen drives and nodes; moved to canopen-python | 2026-06-28 | MIT |
| SavvyCAN | Qt GUI to capture, analyse and replay CAN frames | 2026-11-16 | MIT |
| flirpy | Python library for FLIR thermal cameras such as the Boson and Tau 2 | 2026-11-24 | MIT |
| nerian_stereo | ROS 1 driver for Nerian SceneScan and Scarlet stereo sensors; its ros2 branch dates from 2018 | 2024-01-23 | MIT |
| pymmw | Python scripts for the TI IWR1443 mmWave radar board; inactive since 2021 | 2021-11-11 | MIT |
| ros2_intel_realsense | Archived ROS 2 RealSense wrapper; realsense-ros replaces it, for `parts/sensors/intel-realsense-d400` | 2023-01-06 | Apache-2.0 |
| ouster_example | Ouster lidar SDK in C++ and Python, renamed ouster-sdk | 2026-11-20 | BSD-3-Clause |
| ros2_ouster_drivers | Community ROS 2 driver for Ouster lidars; its README sends new users to ouster-ros | 2024-06-18 | Apache-2.0 |
| livox_ros_driver | ROS 1 driver for older Livox lidars; livox_ros_driver2 serves the Mid-360 and HAP | 2023-02-28 | MIT |
| velodyne | ROS and ROS 2 driver for Velodyne lidars | 2026-10-23 | BSD-3-Clause |
| ublox | ROS driver for u-blox GNSS receivers, with a ROS 2 branch | 2025-09-26 | BSD-3-Clause |
| novatel_gps_driver | SwRI ROS 2 driver for NovAtel GNSS receivers | 2026-10-30 | BSD-3-Clause |
| pylon-ros-camera | Basler's official ROS 2 driver for its GigE and USB3 cameras | 2026-10-22 | BSD-3-Clause |
| ethz_piksi_ros | ETH ROS 1 drivers and tools for the Swift Navigation Piksi RTK GNSS | 2023-04-18 | BSD-3-Clause |
| sick_safetyscanners | SICK's ROS 1 driver for microScan3 and nanoScan3 safety scanners; sick_safetyscanners2 serves ROS 2 | 2024-06-19 | Apache-2.0 |
| bosch_imu_driver | ROS 1 UART driver for the Bosch BNO055 IMU; for `parts/sensors/bosch-bno055` (to be written) | 2021-02-06 | BSD-3-Clause |
| ifm3d | ifm library and tools for its O3R, O3D and O3X 3D time-of-flight cameras | 2026-11-23 | Apache-2.0 |
| cepton_sdk_redist | Cepton lidar SDK with ROS 1 support; inactive since 2023 | 2023-07-20 | BSD-3-Clause |
| ros_astra_camera | Orbbec's ROS 1 driver for its Astra 3D cameras; OrbbecSDK_ROS2 serves ROS 2 | 2025-06-05 | Apache-2.0 |
| blickfeld-scanner-lib | Library for Blickfeld Cube lidars; inactive since 2023 | 2023-01-17 | BSD-3-Clause |
| TauLidarCamera | Host API for the Onion Tau time-of-flight camera; inactive since 2023 | 2023-08-23 | MIT |

## Deferred

| Entry | What it is | Phase |
|---|---|---|

## Rejected

| Entry | Why | Date |
|---|---|---|
| Agile Development | Off topic: the Agile Manifesto, a general software-process text | 2026-11-18 |
| Gitflow | Off topic: a git branching extension; archived on 2025-10-14 | 2026-11-18 |
| DeepL | Off topic: a third-party DeepL translator wrapper; archived 2024 | 2026-11-18 |
| Taiga | Off topic: Docker setup for a project-management tool; archived 2024 | 2026-11-18 |
| Kanboard | Off topic: a general Kanban board | 2026-11-18 |
| kanban | Off topic: a GitLab Kanban board, no commit since 2019 | 2026-11-18 |
| Gitlab | Off topic: a Docker image for self-hosting GitLab | 2026-11-18 |
| Gogs | Off topic: a self-hosted git service | 2026-11-18 |
| Wekan | Off topic: a general Kanban board | 2026-11-18 |
| JIRA API | Off topic: a Python client for Jira | 2026-11-18 |
| Taiga API | Off topic: a Python client for Taiga | 2026-11-18 |
| Chronos-Timetracker | Off topic: a Jira time tracker, no commit since 2019 | 2026-11-18 |
| Grge | Off topic: a GitLab helper daemon, no commit since 2020 | 2026-11-18 |
| gitlab-triage | Off topic: a GitLab issue-triage bot | 2026-11-18 |
| Helpy | Off topic: a helpdesk app, no commit since 2021 | 2026-11-18 |
| ONLYOFFICE | Off topic: an office and groupware suite | 2026-11-18 |
| discourse | Off topic: forum software | 2026-11-18 |
| Gerrit | Off topic: a general code-review server | 2026-11-18 |
| jitsi-meet | Off topic: video conferencing | 2026-11-18 |
| mattermost | Off topic: team chat | 2026-11-18 |
| openproject | Off topic: project-management software | 2026-11-18 |
| leantime | Off topic: project-management software | 2026-11-18 |
| gitter | Off topic: a community chat platform | 2026-11-18 |
| Typora | Off topic: a commercial Markdown editor | 2026-11-18 |
| Markor | Off topic: an Android Markdown editor | 2026-11-18 |
| Pandoc | Off topic: a general document converter | 2026-11-18 |
| Yaspeller | Off topic: a spell checker; archived 2024 | 2026-11-18 |
| ReadtheDocs | Off topic, and the link returns 404: Read the Docs build environments | 2026-11-18 |
| Word-to-Markdown | Off topic: converts Word documents to Markdown | 2026-11-18 |
| paperless | Off topic: a scanned-document archive; archived 2021 | 2026-11-18 |
| carbon | Off topic: images of source code for sharing | 2026-11-18 |
| undraw | Off topic: stock illustrations | 2026-11-18 |
| asciinema | Off topic: terminal session recorder | 2026-11-18 |
| inkscape | Off topic: a vector graphics editor | 2026-11-18 |
| Reveal-Hugo | Off topic: a presentation theme | 2026-11-18 |
| Hugo-Webslides | Off topic: a presentation theme, no commit since 2022 | 2026-11-18 |
| jupyter2slides | Off topic: notebook slides, no commit since 2018 | 2026-11-18 |
| patat | Off topic: terminal presentations | 2026-11-18 |
| github-changelog-generator | Off topic: a changelog generator | 2026-11-18 |
| GitLab-Release-Note-Generator | Off topic: a release-note generator, no commit since 2022 | 2026-11-18 |
| OCRmyPDF | Off topic: OCR for scanned PDFs | 2026-11-18 |
| papermill | Off topic: runs parameterised Jupyter notebooks | 2026-11-18 |
| docsy | Off topic: a documentation site theme | 2026-11-18 |
| actions-hugo | Off topic, and the link opens a user page, not the action | 2026-11-18 |
| overleaf | Off topic: a LaTeX editor | 2026-11-18 |
| landslide | Off topic: a slideshow generator | 2026-11-18 |
| libreoffice-impress-templates | Off topic: slide templates, no commit since 2020 | 2026-11-18 |
| opensourcedesign | Off topic: design resources | 2026-11-18 |
| olive | Off topic: a video editor | 2026-11-18 |
| buku | Off topic: a bookmark manager | 2026-11-18 |
| swiftlatex | Off topic: a browser LaTeX editor | 2026-11-18 |
| ReLaXed | Off topic: a PDF layout tool | 2026-11-18 |
| foam | Off topic: personal knowledge management | 2026-11-18 |
| CodiMD | Off topic: collaborative Markdown notes | 2026-11-18 |
| jupyter-book | Off topic: books from Jupyter notebooks | 2026-11-18 |
| InvoiceNet | Off topic: invoice data extraction | 2026-11-18 |
| mkdocs | Off topic: a general static documentation site generator | 2026-11-18 |
| PlotNeuralNet | Off topic: LaTeX drawings of neural networks, no commit since 2020 | 2026-11-18 |
| Excalidraw | Off topic: a general sketching and diagram tool | 2026-11-18 |
| SVGrepo | Off topic: stock SVG images | 2026-11-18 |
| gollum | Off topic: a git-backed wiki | 2026-11-18 |
| GanttLab | Off topic: Gantt charts for GitLab, no commit since 2021 | 2026-11-18 |
| Zotero | Off topic: a reference manager | 2026-11-18 |
| CarND-Functional-Safety-Project | Too thin: a Udacity course exercise, no commit since 2021 | 2026-11-18 |
| AUTOSAR Coding Standard | Dead link: the AUTOSAR C++14 guideline PDF returns 404 | 2026-11-18 |
| The W-Model and Lean Scaled Agility for Engineering | Dead link: the Vector PDF does not load | 2026-11-18 |
| robmosys | Dead link: robmosys.eu returns a server error | 2026-11-18 |
| ScenarioArchitect | Too thin: a small driving-scenario tool, no commit since 2021 | 2026-11-18 |
| yEd | Off topic: a general diagram editor | 2026-11-18 |
| yed_py | Off topic: generates yEd diagram files | 2026-11-18 |
| Plantuml | Off topic: a general UML diagram server | 2026-11-18 |
| rqt_launchtree | Abandoned: ROS 1 rqt plugin, no commit since 2017 | 2026-11-18 |
| draw.io | Off topic: a general diagram editor | 2026-11-18 |
| vscode-drawio | Off topic: a draw.io plugin for VS Code | 2026-11-18 |
| awesome-ros2 | Dead link: fkromer/awesome-ros2 returns 404 | 2026-11-18 |
| Stanford Self Driving Car Code | Dead link: the repository returns 404 | 2026-11-18 |
| Automotive Grade Linux | Off topic: a Linux distribution for car infotainment | 2026-11-18 |
| KubOS | Dead link: the repository returns 404 | 2026-11-18 |
| Aslan | Abandoned: a small low-speed self-driving stack, no commit since 2021 | 2026-11-18 |
| pybotics | Archived 2024: a small Python kinematics toolbox | 2026-11-18 |
| makani | Archived 2022: flight software of Google's Makani energy kite, off topic | 2026-11-18 |
| atom | Archived: the Atom editor was sunset in December 2022 | 2026-11-18 |
| Teletype | Archived with Atom in December 2022 | 2026-11-18 |
| Sublime | Off topic: a general commercial text editor | 2026-11-18 |
| recipe-wizard | Abandoned: a Dockerfile generator, no commit since 2020 | 2026-11-18 |
| xeus-cling | Off topic: a general C++ Jupyter kernel | 2026-11-18 |
| TabNine | Off topic: commercial AI code completion; archived 2026 | 2026-11-18 |
| kite | Discontinued in 2022: AI code completion for Python | 2026-11-18 |
| jedi | Off topic: a general Python autocompletion library | 2026-11-18 |
| Sourcetrail | Archived 2021: a source code explorer | 2026-11-18 |
| rebound | Off topic: Stack Overflow lookups on errors, no commit since 2022 | 2026-11-18 |
| mybinder | Off topic: hosted Jupyter notebooks | 2026-11-18 |
| ROSOnWindows | Outdated: experimental ROS 1 on Windows; ROS 2 supports Windows itself | 2026-11-18 |
| live-share | Off topic: collaborative editing for VS Code | 2026-11-18 |
| cocalc | Off topic: cloud notebooks; archived 2026 | 2026-11-18 |
| EasyClangComplete | Off topic: a Sublime Text C++ completion plugin | 2026-11-18 |
| awesome-hpp | Off topic: a general list of header-only C++ libraries | 2026-11-18 |
| Gitpod | Off topic: cloud development environments | 2026-11-18 |
| Bash | Off topic: a general Bash script template | 2026-11-18 |
| Cross compile ROS 2 on QNX | Dead link: gitlab.apex.ai does not respond | 2026-11-18 |
| ros_gitlab_ci | Abandoned: GitLab CI helpers for ROS 1, no commit since 2021 | 2026-11-18 |
| gitlab-runner | Off topic: GitLab's general CI runner | 2026-11-18 |
| gitlab-release | Too thin: a small release-upload script, no commit since 2022 | 2026-11-18 |
| cross_compile | Archived 2022: ROS 2 cross-compilation tool | 2026-11-18 |
| robot_systemd | Abandoned: ROS Kinetic systemd units | 2026-11-18 |
| network_autoconfig | Abandoned: ROS Kinetic network auto-configuration | 2026-11-18 |
| cros | Abandoned: a pure-C ROS 1 client, no commit since 2020 | 2026-11-18 |
| pydocstyle | Archived 2023: a Python docstring checker | 2026-11-18 |
| pydantic | Off topic: a Python data-validation library, not a linter | 2026-11-18 |
| lptrace | Abandoned: a Python call tracer, no commit since 2017 | 2026-11-18 |
| pyre-check | Off topic: a Python type checker; archived 2026 | 2026-11-18 |
| cppinsights | Off topic: a C++ language learning tool | 2026-11-18 |
| inspect | Off topic: Python 2 docs page for the inspect module | 2026-11-18 |
| pyperformance | Off topic: a benchmark suite for Python interpreters | 2026-11-18 |
| qira | Abandoned: a timeless debugger, no commit since 2022 | 2026-11-18 |
| ros1_fuzzer | Archived 2020: a ROS 1 topic fuzzer | 2026-11-18 |
| vscode-debug-visualizer | Off topic: a VS Code data visualiser for debugging | 2026-11-18 |
| action-tmate | Off topic: SSH access to GitHub Actions runners | 2026-11-18 |
| system_metrics_collector | Archived 2021: ROS 2 system metrics collector | 2026-11-18 |
| git-fuzzy | Off topic: a general git tool | 2026-11-18 |
| meld | Off topic: a general diff and merge tool | 2026-11-18 |
| tig | Off topic: a general git tool | 2026-11-18 |
| gitg | Off topic: a general git tool | 2026-11-18 |
| git-cola | Off topic: a general git tool | 2026-11-18 |
| python-gitlab | Off topic: a Python client for GitLab | 2026-11-18 |
| bfg-repo-cleaner | Off topic: a general git history cleaner | 2026-11-18 |
| nbdime | Off topic: diffs for Jupyter notebooks | 2026-11-18 |
| semantic-release | Off topic: general release automation | 2026-11-18 |
| go-semrel-gitab | Off topic: GitLab release automation, no commit since 2019 | 2026-11-18 |
| Git-repo | Off topic: Android's multi-repository git tool | 2026-11-18 |
| learnGitBranching | Off topic: a git teaching game | 2026-11-18 |
| gitfs | Off topic: a git-backed file system, no commit since 2021 | 2026-11-18 |
| git-secret | Off topic: a general secret-encryption tool for git | 2026-11-18 |
| git-sweep | Off topic: a git branch cleaner, no commit since 2016 | 2026-11-18 |
| lazygit | Off topic: a general git tool | 2026-11-18 |
| glab | Off topic: a GitLab CLI; archived 2022 | 2026-11-18 |
| deepdive | Abandoned: a driving simulator, no commit since 2020 | 2026-11-18 |
| self-driving-car-sim | Archived 2022: a Udacity course simulator | 2026-11-18 |
| gym-gazebo | Archived 2019: a Gym wrapper for Gazebo | 2026-11-18 |
| car_demo | Archived 2025: a Prius demo for Gazebo 9 and ROS Kinetic | 2026-11-18 |
| Menge | Abandoned: a crowd simulator, no commit since 2019 | 2026-11-18 |
| morse | Abandoned: built on Blender's game engine, which Blender 2.80 removed | 2026-11-18 |
| flow | Abandoned: a traffic RL framework, no commit since 2020 | 2026-11-18 |
| gazebo_ros_motors | Abandoned: Gazebo DC-motor plugins for ROS 1, no commit since 2021 | 2026-11-18 |
| map2gazebo | Abandoned: makes Gazebo worlds from 2D maps, no commit since 2020 | 2026-11-18 |
| gym-carla | Abandoned: a Gym wrapper for CARLA, no commit since 2020 | 2026-11-18 |
| Trick | Off topic: NASA's space-vehicle simulation framework | 2026-11-18 |
| 42 | Off topic: a spacecraft attitude-control simulator | 2026-11-18 |
| Complete_Street_Rule | Off topic: street-design rules for ArcGIS CityEngine | 2026-11-18 |
| AutoCore simulation | Too thin: the link opens the Autoware Foundation org, not a project | 2026-11-18 |
| fields-ignition | Archived 2026: crop-field world generator for Ignition Gazebo | 2026-11-18 |
| BlueSky | Off topic: an air-traffic simulator | 2026-11-18 |
| Dynamic_logistics_Warehouse | Abandoned: a small Gazebo warehouse world, no commit since 2021 | 2026-11-18 |
| HRIM | Archived 2019: an abandoned robot hardware information model | 2026-11-18 |
| PandaPower | Off topic: power-grid modelling | 2026-11-18 |
| GNSS-SDR | Off topic: a software-defined GNSS receiver | 2026-11-18 |
| FMIKit-Simulink | Archived 2025: FMU import and export for Simulink | 2026-11-18 |
| oemof-solph | Off topic: energy-system modelling | 2026-11-18 |
| NASA-3D-Resources | Off topic: NASA 3D models and images | 2026-11-18 |
| SUAVE | Off topic: aircraft design, no commit since 2022 | 2026-11-18 |
| opem | Off topic: fuel-cell simulation | 2026-11-18 |
| pvlib-python | Off topic: solar power simulation | 2026-11-18 |
| tigl | Off topic: aircraft geometry | 2026-11-18 |
| cadCAD | Off topic: system simulation for token-economy design | 2026-11-18 |
| OpenMDAO | Off topic: multidisciplinary design optimisation, mainly aircraft | 2026-11-18 |
| OpenTirePython | Off topic: tyre models, no commit since 2020 | 2026-11-18 |
| Inkscape Ray Optics | Off topic: optics diagrams in Inkscape | 2026-11-18 |
| OpenAeroStruct | Off topic: aircraft aerostructural optimisation | 2026-11-18 |
| TriP | Abandoned: a small IK library, no commit since 2022 | 2026-11-18 |
| fastai | Off topic: a general deep-learning training library | 2026-11-18 |
| tpot | Off topic: AutoML for tabular data | 2026-11-18 |
| deap | Off topic: general evolutionary algorithms | 2026-11-18 |
| tensorflow_ros_cpp | Abandoned: TensorFlow inference for ROS 1, no commit since 2022 | 2026-11-18 |
| Tensorflow Federated | Off topic: federated learning on decentralised data | 2026-11-18 |
| neuropod | Abandoned: Uber's model-runtime wrapper, no commit since 2022 | 2026-11-18 |
| leela-zero | Off topic: a Go-playing engine | 2026-11-18 |
| Trax | Off topic: a deep-learning library; archived 2025 | 2026-11-18 |
| Tensorforce | Abandoned: its README says it is no longer maintained | 2026-11-18 |
| catalyst | Off topic: a PyTorch training framework, no commit since 2022 | 2026-11-18 |
| ReAgent | Off topic: Meta's RL platform for recommendation systems | 2026-11-18 |
| Awesome-Mobile-Machine-Learning | Dead link: the repository returns 404 | 2026-11-18 |
| cnn-explainer | Off topic: an interactive CNN teaching demo | 2026-11-18 |
| nnstreamer-ros | Abandoned: GStreamer neural-network nodes for ROS, no commit since 2020 | 2026-11-18 |
| libcudacxx | Archived 2024: merged into NVIDIA CCCL | 2026-11-18 |
| CV-pretrained-model | Too thin: a link list of pretrained models, no commit since 2021 | 2026-11-18 |
| ros_ncnn | Abandoned: YOLO on ncnn for ROS 1, no commit since 2021 | 2026-11-18 |
| tf-pose-estimation | Dead link: the repository returns 404 | 2026-11-18 |
| semantic_slam | Abandoned: a semantic SLAM demo for ROS 1, no commit since 2019 | 2026-11-18 |
| satellite-image-deep-learning | Off topic: satellite and aerial imagery resources | 2026-11-18 |
| robosat | Off topic: segmentation of satellite imagery | 2026-11-18 |
| big_transfer | Off topic: image-classification pretraining; archived 2025 | 2026-11-18 |
| fawkes | Off topic: a tool against facial recognition | 2026-11-18 |
| anonymizer | Archived 2022: face and licence-plate blurring | 2026-11-18 |
| opendatacam | Off topic: a traffic-counting camera app | 2026-11-18 |
| satpy | Off topic: meteorological satellite data | 2026-11-18 |
| eo-learn | Off topic: satellite image processing | 2026-11-18 |
| libvips | Off topic: an image library for web-scale processing | 2026-11-18 |
| pyroSAR | Off topic: satellite radar (SAR) data processing | 2026-11-18 |
| point_cloud_io | Archived 2026: ROS 1 point-cloud file reader and writer | 2026-11-18 |
| python-pcl | Archived 2023: abandoned Python bindings for PCL | 2026-11-18 |
| pptk | Abandoned: a point-cloud viewer, no commit since 2018 | 2026-11-18 |
| segmenters_lib | Abandoned: a lidar segmentation library, no commit since 2020 | 2026-11-18 |
| OpenPCDet | Duplicate of PCDet: the same repository after a rename | 2026-11-18 |
| mmWave-localization-learning | Positioning from cellular mmWave signals; research code with no use to a robot builder | 2026-11-18 |
| python-sgp4 | Satellite orbit propagation; off-topic for robot builders | 2026-11-18 |
| KISS-ICP | Duplicate of KISS-ICP under Lidar and Point Cloud Processing | 2026-11-18 |
| orb_slam_2_ros | Dead link (404) | 2026-11-18 |
| openvslam | Code withdrawn in 2021, only a notice remains; the stella_vslam fork continues it | 2026-11-18 |
| MapsModelsImporter | Imports Google Maps captures into Blender; not a robot tool | 2026-11-18 |
| iD | OpenStreetMap web editor; off-topic for robot builders | 2026-11-18 |
| RapiD | AI-assisted OpenStreetMap editor; off-topic for robot builders | 2026-11-18 |
| imagery-index | Index of aerial imagery for OpenStreetMap editing; off-topic | 2026-11-18 |
| mapillary_tools | Uploads street imagery to Mapillary; off-topic | 2026-11-18 |
| mapnik | Map tile rendering for web maps; off-topic | 2026-11-18 |
| grass | Desktop GIS suite; off-topic for robot builders | 2026-11-18 |
| HypridAStarTrailer | Dead link (404) | 2026-11-18 |
| pykep | Interplanetary trajectory design; off-topic | 2026-11-18 |
| mir | Libraries for building Wayland desktop shells; off-topic | 2026-11-18 |
| pencil | GUI mock-up and diagram tool; not a robot tool | 2026-11-18 |
| DDSP | Differentiable audio synthesis for music; off-topic | 2026-11-18 |
| NoiseTorch | Desktop microphone noise filter for calls; off-topic | 2026-11-18 |
| dotfiles of cornerman | One person's shell and editor configuration | 2026-11-18 |
| prompt-hjem | One person's zsh prompt | 2026-11-18 |
| mapscii | World map rendered in a terminal; a toy | 2026-11-18 |
| labelbox | Dead link (404); Labelbox is a commercial labelling service | 2026-11-18 |
| Automotive Graded Linux | Linux platform for car infotainment; off-topic | 2026-11-18 |
| AUTOSAR-Adaptive | Dead link (404) | 2026-11-18 |
| ocpp | Protocol for electric-vehicle chargers; off-topic | 2026-11-18 |
| airalab | Blockchain "robot economy" project; nothing a builder uses | 2026-11-18 |
| rdbox | Dead link (404) | 2026-11-18 |
| openwifi | Software-defined-radio Wi-Fi design for FPGAs; off-topic | 2026-11-18 |
| AndrOBD | Android car diagnostics over OBD; off-topic | 2026-11-18 |
| ddt4all | Renault ECU diagnostics tool; off-topic | 2026-11-18 |
| cabana | Car CAN reverse-engineering tool from comma.ai; off-topic | 2026-11-18 |
| opendbc | CAN message definitions for production cars; off-topic | 2026-11-18 |
| python-udsoncan | Car ECU diagnostics protocol (UDS); off-topic | 2026-11-18 |
| uds-c | Car ECU diagnostics (UDS, OBD-II) in C; off-topic | 2026-11-18 |
| autosar | Python tools for AUTOSAR car-software XML; off-topic | 2026-11-18 |
| Open-Vehicle-Monitoring-System-3 | Remote monitoring of electric cars; off-topic | 2026-11-18 |
| Tesla-API | Unofficial API to control Tesla cars; off-topic | 2026-11-18 |
| sick_scan | Dead link (404); sick_scan_xd replaces it | 2026-11-18 |
| CANalyzat0r | Security testing of proprietary car protocols; off-topic | 2026-11-18 |
| OpenTitan | Open silicon root-of-trust chip design; off-topic for robot builders | 2026-11-18 |
| Papers With Code | Shut down in 2025; the link redirects to Hugging Face | 2026-11-18 |
| awesome-satellite-imagery-datasets | Satellite imagery datasets; off-topic | 2026-11-18 |
| sentinelsat | Downloads Copernicus satellite images; off-topic | 2026-11-18 |
| Atlatec Sample Map Data | Dead link: the sample-data page redirects to the company site | 2026-11-18 |
| Lyft Level 5 Dataset | Dead link: the site does not answer; Lyft sold Level 5 in 2021 | 2026-11-18 |
| UTD19 | Urban traffic loop-detector data; off-topic | 2026-11-18 |
| ASTYX HIRES2019 DATASET | Dead link: the linked blog does not answer | 2026-11-18 |
| ilqr | Abandoned: a small Python iLQR library, no commit since 2019 | 2026-11-26 |
| ros2arduino | Abandoned: no commit since 2020; micro-ROS for Arduino replaces it | 2026-11-26 |
| decanstructor | Abandoned: a ROS 1 CAN analysis tool, no commit since 2022 | 2026-11-26 |
| ti_mmwave_rospkg | Abandoned: a ROS 1 TI mmWave radar driver, no commit since 2019; no licence file, only a `package.xml` tag | 2026-11-26 |
| pointgrey_camera_driver | Outdated: ROS 1 driver for FLIR's older FlyCapture SDK, no commit since 2022; flir_camera_driver (Spinnaker) serves ROS 2 | 2026-11-26 |
| oxford_gps_eth | Abandoned: a ROS 1 driver, no commit since 2020; OxTS publishes oxts_ros2_driver | 2026-11-26 |
| jetson_csi_cam | Abandoned: ROS 1 CSI camera package for Jetson TK1, TX1 and TX2, no commit since 2019 | 2026-11-26 |
