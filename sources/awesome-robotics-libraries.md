---
type: source
name: Awesome Robotics Libraries
registry: awesome-robotics-libraries
url: https://github.com/jslee02/awesome-robotics-libraries
commit: "98c7b97"
read_on: 2026-11-18
counts: {entries: 229, pages: 12, waiting: 19, index_only: 124, deferred: 33, rejected: 41}
---

# Awesome Robotics Libraries: what it gives RoboAI

A curated list of about 230 robotics libraries and simulators in 16 categories, from middleware,
robot description and dynamics through physics engines, simulators, planning, control,
optimisation, SLAM, perception, grasping and robot learning, each marked with its activity and
stars. Its own entry bar (stars, outside contributors, a commit within a year) keeps it cleaner
than most lists, and it holds most of the core open libraries a builder meets: it gives Phase 4
25 page candidates across the ros2, sim, manip, perception and learning batches, and its control
and optimisation sections to Phase 5. About a sixth of it is small, inactive code folded at the
end of each section.

## How it was read

- Read at commit `98c7b97` (2026-10-26) on 2026-11-18: the README in full (16 categories, 228
  entries), `CONTRIBUTING.md` and the linked `COMPARISONS.md`, which gets one index row. The README
  is generated from `data/*.yaml`; those files give each GitHub entry's last commit and licence as
  of 2026-10-12, and the Index only columns use them (— where the list gives none). AirSim and
  Legged Gym, checked as candidates, show the checked values.
- Page candidates were checked on 2026-11-18 with a shallow clone of the project's own repo (last
  commit, licence file). Notes from that check: cuRobo is now Apache-2.0; Isaac Sim's repo code is
  Apache-2.0 but it needs NVIDIA Omniverse components under other terms; CoppeliaSimLib on GitHub
  is GPL-3.0-or-later; OctoMap is BSD-3-Clause with its octovis viewer GPL-2.0; GTSAM is
  BSD-2-Clause; `ros2/ros2` is a repos manifest with no licence file (licences are per package).
  Cartographer's last commit is 2024-01-05. `foxglove/studio` now holds only a README (last
  commit 2024-03-11): the Foxglove app is closed source and needs an account.
- "MoveIt!" links `moveit/moveit` (MoveIt 1, ROS 1); its page is MoveIt 2, checked at
  `moveit/moveit2`. Bullet and PyBullet are one repo (`bullet3`), so PyBullet is rejected as a
  duplicate and Bullet's row carries the `tools/pybullet` page. Legged Gym's own README says its
  environments moved to Isaac Lab with limited updates, so it is index only.
- **Deferred to Phase 5:** the whole Control (8) and Optimization (22) sections, the two CAD
  exporters (phobos, onshape-to-robot) and the micro-ROS Arduino fork.
- No section holds only papers. `COMPARISONS.md` holds feature tables for physics engines and
  dynamics libraries, four benchmark links and five papers; the sim and manip batches can use its
  tables as a starting point, after checking them.
- Dead or moved on 2026-11-18: artiminds.com redirects to an unrelated streaming site;
  energid.com does not respond (the list already links a web-archive copy); the IBDS page shows
  the host's "not available" notice; neurorobotics.net and icub.org do not respond (the iCub Atlas
  page is unaffected); the Kineo link lands on a general Siemens page; Newton Dynamics' site link
  is a 2008 web-archive copy. The SDF and ODE Bitbucket links still load.
- Errors in the list: "RobotDK" is RoboDK, "SpaceVelAlg" is SpaceVecAlg, and hpipm's description
  repeats ifopt's "(Ipopt, Snopt)".
- Nothing in the fetched files was addressed to agents. `CONTRIBUTING.md` sets rules for
  AI-assisted suggestions to the list, which concern its contributors only. The Artiminds redirect
  is the one suspicious item.

## Pages made

| Entry | Page | Tier |
|---|---|---|
| ROS 2 | [ROS 2](../wiki/tools/ros2.md) | A |
| urdf | [URDF and xacro](../wiki/software/urdf.md) | A |
| Foxglove Studio | [Foxglove](../wiki/tools/foxglove.md) | B |
| Genesis | [Genesis](../wiki/tools/genesis.md) | B |
| MuJoCo | [MuJoCo](../wiki/tools/mujoco.md) | A |
| Bullet | [PyBullet](../wiki/tools/pybullet.md) | B |
| Webots | [Webots](../wiki/tools/webots.md) | B |
| Isaac Sim | [Isaac Sim](../wiki/tools/isaac-sim.md) | A |
| Gazebo Sim | [Gazebo](../wiki/tools/gazebo.md) | A |
| CoppeliaSim | [CoppeliaSim](../wiki/tools/coppeliasim.md) | B |
| MuJoCo Menagerie | [MuJoCo](../wiki/tools/mujoco.md) | A |
| CARLA | [CARLA](../wiki/tools/carla.md) | B |

## Waiting for a page

| Entry | Page | Tier | Batch | Why it matters |
|---|---|---|---|---|
| pinocchio | `software/pinocchio` | A | manip | Fast rigid-body dynamics with analytical derivatives; the base of much legged and arm control code |
| Drake | `software/drake` | A | manip | Planning, control and contact-rich simulation in one maintained toolbox; strong for manipulation |
| OMPL | `software/ompl` | A | manip | The sampling-based planner library behind MoveIt; the reference for RRT and PRM planners |
| MoveIt! | `software/moveit2` | A | manip | The standard ROS arm motion-planning framework; MoveIt 2 is what builders use today |
| cuRobo | `software/curobo` | B | manip | GPU collision-free motion generation, now Apache-2.0; a fast alternative to OMPL for arms |
| Cartographer | `software/cartographer` | B | perception | Google's 2D and 3D SLAM, still in many ROS robots; no commit since January 2024 |
| RTAB-Map | `software/rtab-map` | A | perception | Maintained RGB-D and lidar graph SLAM with ROS 2 support; a common choice for 3D mapping |
| GTSAM | `software/gtsam` | A | perception | Factor-graph library under many SLAM and visual-inertial systems; the tool for custom estimators |
| OctoMap | `software/octomap` | B | perception | The standard probabilistic 3D occupancy map; MoveIt uses it to sense obstacles |
| PCL | `software/pcl` | A | perception | The standard C++ point-cloud library for filtering, registration and segmentation |
| LeRobot | `learning/lerobot` | A | learning | Hugging Face's datasets, policies and low-cost robot support; the entry point for imitation learning |
| Stable-Baselines3 | `learning/stable-baselines3` | B | learning | The usual first RL library: reliable PyTorch algorithms behind a Gymnasium interface |
| Isaac Lab | `learning/isaac-lab` | A | learning | NVIDIA's GPU robot-learning framework on Isaac Sim; the standard for locomotion RL and sim-to-real |
| ManiSkill | `learning/maniskill` | A | learning | GPU-parallel manipulation simulation and benchmark on SAPIEN; widely used for robot learning |
| robosuite | `learning/robosuite` | A | learning | MuJoCo manipulation benchmark behind robomimic and many imitation-learning papers |
| ORB-SLAM2 | `software/orb-slam3` | B | perception | The classic feature-based visual SLAM and a baseline in papers; the ORB-SLAM3 page covers the family |
| Contact-GraspNet | `learning/contact-graspnet` | B | manip | Common 6-DoF grasp generator from depth point clouds; NVIDIA non-commercial licence, quiet since 2024 |
| Gymnasium | `learning/gymnasium` | B | learning | Gym's successor Gymnasium is the standard RL environment API; MuJoCo, ManiSkill and others use it |
| PythonRobotics | `software/pythonrobotics` | B | nav | Widely used, readable Python samples of planning, localisation and SLAM algorithms; MIT, maintained |

## Index only

| Entry | What it is | Last commit | Licence |
|---|---|---|---|
| Dimensional | Young LLM-agent framework for robots, fast-moving | 2026-10-12 | — |
| YARP | iCub's middleware, used mainly in the IIT ecosystem | 2026-10-07 | — |
| ros2_medkit | ROS 2 fault and diagnostics gateway with a REST API | 2026-10-06 | Apache-2.0 |
| Robot Control Stack (RCS) | Gymnasium layer over MuJoCo and real arms for learning | 2026-10-11 | AGPL-3.0 |
| Rock | Orocos-based robot software framework from DFKI | — | — |
| ROS | ROS 1; Noetic, its last release, reached end of life May 2025 | — | — |
| iCub | Robot; on the [iCub](../wiki/robots/icub.md) page | 2026-08-27 | — |
| Linorobot | Robot; not in the Atlas. The ROS 1 stack; linorobot2 replaced it | 2022-07-11 | BSD-2-Clause |
| onine | Robot; not in the Atlas | 2018-09-19 | — |
| AutoRally | Robot; on the [AutoRally](../wiki/robots/autorally.md) page | 2021-08-16 | — |
| SDF | Gazebo's model and world format; belongs on the Gazebo page | — | — |
| Robotics Library | Self-contained C++ kinematics, planning and control library | 2025-04-15 | GPL-3.0 or BSD-2-Clause |
| KDL | ROS's classic kinematics library, behind MoveIt's default IK plugin | 2026-09-23 | LGPL-2.1 |
| RBDL | Featherstone rigid-body dynamics; low activity, pinocchio covers it | 2025-06-09 | Zlib |
| PyDy | Symbolic multibody dynamics on SymPy | 2026-07-28 | BSD-3-Clause |
| RigidBodyDynamics.jl | Rigid-body dynamics in Julia | 2024-11-08 | MIT |
| idyntree | Floating-base dynamics and estimation from the iCub ecosystem | 2026-07-27 | LGPL-2.1 |
| RBDyn | Spatial-algebra dynamics from the mc_rtc ecosystem | 2026-10-05 | LGPL-3.0 |
| ARTE | MATLAB toolbox for teaching manipulator kinematics | 2026-04-29 | — |
| RobWork | SDU's C++ framework for robot simulation and control | — | Apache-2.0 |
| IKBT | Symbolic closed-form arm IK solver in Python | 2026-09-18 | — |
| ssik | Analytical IK for 6R and 7R arms, every branch | 2026-10-04 | BSD-3-Clause |
| Kinpy | Small pure-Python kinematics and IK | 2026-10-08 | MIT |
| RelaxedIK | Real-time feasible arm IK; inactive since 2023 | 2023-04-13 | MIT |
| Newton | GPU physics on NVIDIA Warp; Linux Foundation project in beta | 2026-10-12 | Apache-2.0 |
| PhysX | NVIDIA's engine under Isaac Sim; belongs on the Isaac Sim page | 2026-10-09 | BSD-3-Clause |
| Brax | JAX physics for RL; its physics users are pointed to MuJoCo MJX | 2026-10-07 | Apache-2.0 |
| CHRONO::ENGINE | Multiphysics: vehicles, granular terrain and flexible bodies | 2026-10-12 | BSD-3-Clause |
| Simbody | Multibody engine behind OpenSim biomechanics | 2026-09-28 | Apache-2.0 |
| ReactPhysics3d | Game-style rigid-body physics engine | 2025-01-09 | Zlib |
| DART | Multibody engine; Gazebo's default physics | 2026-10-12 | BSD-2-Clause |
| Newton Dynamics | Game-oriented rigid-body engine | 2026-01-17 | Zlib |
| siconos | Nonsmooth dynamical systems modelling and simulation | 2026-10-07 | Apache-2.0 |
| MBSim | Flexible and rigid multibody simulation | 2026-10-11 | not specified |
| MBDyn | General multibody dynamics analysis | — | GPL (the list gives 2.1) |
| ODE | Classic rigid-body engine; Gazebo Classic's default | — | LGPL-2.1 or BSD-3-Clause |
| PositionBasedDynamics | Position-based deformables, cloth and fluids | 2026-09-01 | MIT |
| Kratos | General multiphysics FEM framework, not robot-specific | 2026-10-12 | — |
| SOFA | Soft-body and medical simulation, with soft-robot plugins | 2026-10-12 | LGPL-2.1 |
| Ptera Software | Flapping-wing aerodynamics analysis | 2026-10-12 | MIT |
| Tiny Differentiable Simulator | Differentiable rigid-body physics; inactive since 2023 | 2023-04-26 | Apache-2.0 |
| Flex | Archived NVIDIA GPU particle physics; PhysX 5 and Warp supersede it | 2021-04-15 | — |
| RaiSim | Legged-RL physics engine; this repo is archived | 2020-11-26 | custom |
| AirSim | Unreal drone and car simulator; recent commits are upkeep only | 2026-09-15 | MIT |
| Habitat-Sim | Meta's embodied-AI simulator for navigation research | 2026-05-07 | MIT |
| Unity | Unity Robotics Hub: ROS bridge and tutorials for Unity | 2026-09-22 | — |
| AI2-THOR | Interactive household scenes for embodied AI | 2025-05-29 | Apache-2.0 |
| SAPIEN | Articulated-object simulator under ManiSkill | 2026-10-08 | — |
| Hexapod Robot Simulator | Browser hexapod IK and gait visualiser | 2026-01-01 | Apache-2.0 |
| mvsim | Light 2D multi-vehicle simulator with ROS | 2026-10-11 | GPL-3.0 |
| ARGoS | Large robot-swarm simulator | 2026-10-05 | — |
| MARS | DFKI simulator from the Rock ecosystem | 2025-09-01 | LGPL-3.0 |
| PyBullet_Industrial | PyBullet add-on for milling and 3D-printing processes | 2025-06-17 | MIT |
| AVIS Engine | Small autonomous-car simulator with a Python API | 2025-05-20 | — |
| Kineo | Siemens path-planning component; commercial, link now generic | — | — |
| Robot Virtual Worlds | Simulated worlds for educational robot kits; commercial | — | — |
| RobotDK | RoboDK: industrial-arm simulation and offline programming; commercial | — | — |
| RobotStudio | ABB's simulation and offline programming; commercial | — | — |
| Virtual Robotics Toolkit | Simulator for classroom robot kits; commercial | — | — |
| Visual Components | Factory simulation and visualisation; commercial | — | — |
| Gazebo Classic | Gazebo 11; archived, end of life January 2025 | 2024-12-03 | — |
| MORSE | Blender-based simulator; inactive since 2022 | 2022-03-22 | — |
| ROS Motion Planning | ROS planner and controller plugins; a teaching collection | 2026-03-28 | GPL-3.0 |
| Ruckig | Jerk-limited online trajectory generation; inside MoveIt 2's smoothing | 2026-09-29 | MIT |
| Python Motion Planning | Python planners and trackers for teaching | 2026-09-15 | GPL-3.0 |
| TOPP-RA | Time-optimal path parameterisation under limits | 2026-08-28 | MIT |
| Fields2Cover | Coverage path planning for field robots | 2026-09-21 | BSD-3-Clause |
| OpenRAVE | Historical planning environment; the origin of IKFast | 2026-10-02 | LGPL-3.0 |
| Klampt | Planning, control and simulation toolkit | 2026-01-10 | BSD-3-Clause |
| The Kautham Project | Small motion-planning toolkit for teaching and research | 2026-07-24 | — |
| CuiKSuite | Kinematic analysis and planning for closed-chain mechanisms | — | — |
| HPP | Path planning for humanoids and kinematic chains in clutter | — | — |
| trajopt | Historical trajectory optimiser; inactive since 2017 | 2017-05-23 | — |
| GPMP2 | Gaussian-process motion planner; inactive since 2022 | 2022-08-28 | — |
| AIKIDO | Planning and decision library; inactive since 2023 | 2023-03-10 | BSD-3-Clause |
| nanoflann | Header-only KD-tree nearest-neighbour search | 2026-10-11 | — |
| Sophus | Lie groups on Eigen, common in SLAM code | 2024-06-12 | — |
| manif | Header-only Lie theory for state estimation | 2025-11-01 | MIT |
| HYPRE | HPC sparse linear solvers; not robot-specific | 2026-10-11 | — |
| Fastor | C++ tensor algebra; not robot-specific | 2025-07-08 | MIT |
| spatialmath-python | Poses and rotations in Python, from Corke's toolbox family | 2026-09-16 | MIT |
| kindr | ANYbotics library for rigid-body transforms | 2025-02-15 | BSD-3-Clause |
| SpaceVelAlg | Spatial vector algebra on Eigen (the repo is SpaceVecAlg) | 2026-09-29 | BSD-2-Clause |
| FLANN | Approximate nearest neighbours; inactive, still used by PCL | 2022-10-27 | — |
| mrpt | Mobile-robot toolkit: SLAM, localisation and navigation | 2026-10-11 | BSD-3-Clause |
| ElasticFusion | Dense RGB-D SLAM; a research landmark | 2025-08-03 | — |
| fuse | Factor-graph sensor fusion for ROS | 2026-06-18 | — |
| FusionCore | Young ROS 2 UKF fusing GPS, IMU and wheel odometry | 2026-10-12 | Apache-2.0 |
| fiducials | Marker-based SLAM for ROS | 2025-11-26 | BSD-3-Clause |
| libpointmatcher | ICP library for 2D and 3D mapping | 2026-08-27 | BSD-3-Clause |
| Bonxai | Fast sparse 3D voxel grid | 2026-09-28 | MPL-2.0 |
| wavemap | Multi-resolution 3D occupancy mapping | 2024-12-10 | BSD-3-Clause |
| LSD-SLAM | Historical direct monocular SLAM | 2014-12-11 | GPL-3.0 |
| DSO | Historical direct sparse visual odometry | 2021-03-08 | GPL-3.0 |
| voxblox | TSDF and ESDF mapping; inactive since 2021 | 2021-11-22 | BSD-3-Clause |
| ViSP | Visual servoing library from Inria | 2026-10-12 | GPL-2.0 |
| BundleTrack | Model-free 6D pose tracking research code | 2026-04-13 | Apache-2.0 |
| AnyGrasp SDK | 6-DoF grasp detection SDK; closed library needing a licence key | 2026-07-13 | — |
| GraspNet API | Toolkit for the GraspNet-1Billion grasping benchmark | 2026-06-29 | MIT |
| GraspIt! | Classic grasp-planning simulator; inactive since 2020 | 2020-07-10 | — |
| CleanRL | Single-file RL algorithm implementations for study | 2026-04-20 | — |
| Legged Gym | Isaac Gym legged-RL environments; its README points to Isaac Lab | 2025-05-29 | BSD-3-Clause |
| Humanoid-Gym | Humanoid locomotion RL on Isaac Gym | 2024-11-01 | — |
| rl_games | Fast RL library behind Isaac Gym and Isaac Lab examples | 2026-09-29 | MIT |
| SKRL | Modular RL library; one of Isaac Lab's trainers | 2026-10-01 | MIT |
| AllenAct | Embodied-AI research framework; quiet since 2024 | 2024-07-23 | — |
| mlpack | General C++ machine-learning library | 2026-10-06 | — |
| DLL | One-developer C++ deep-learning library | 2025-05-27 | MIT |
| Any4LeRobot | Conversion and helper tools for LeRobot datasets | 2026-10-01 | MIT |
| ReductStore | Time-indexed blob storage for robot and IoT data | 2026-10-12 | Apache-2.0 |
| LeRobot Episode Scoring Toolkit | Scores and filters LeRobot dataset episodes | 2026-03-13 | Apache-2.0 |
| Awesome Machine Learning | General machine-learning list | 2026-10-09 | — |
| Awesome Deep Learning | General deep-learning list | 2025-05-26 | — |
| Awesome Artificial Intelligence | General AI list | 2026-08-15 | MIT |
| Awesome Robotics (Kiloreux) | A Phase 4 list with its own triage note | 2024-09-22 | — |
| Robotics Coursework | List of online robotics courses | 2026-08-31 | Unlicense |
| Awesome SLAM Datasets | List of SLAM datasets | 2024-12-13 | — |
| Awesome Collision Detection | Collision-detection libraries, by this list's author | 2026-10-10 | CC0-1.0 |
| Awesome Physical AI | Physical-AI papers and resources | 2026-06-24 | CC0-1.0 |
| Awesome VLA Study | Study guide to vision-language-action papers | 2026-03-21 | — |
| Awesome Computer Vision | General computer-vision list; inactive since 2021 | 2021-09-28 | — |
| Awesome Robotic Tooling | A Phase 4 list with its own triage note | 2023-04-30 | CC0-1.0 |
| Awesome Robotics (ahundt) | General robotics list; inactive since 2023 | 2023-03-19 | — |
| Comparisons (COMPARISONS.md) | Companion file: engine and dynamics-library feature tables, benchmarks, papers | — | CC0-1.0 |

## Deferred

| Entry | What it is | Phase |
|---|---|---|
| Micro-ROS for Arduino | Arduino Library Manager fork of micro-ROS, from Kaia.ai | 5 |
| phobos | Blender add-on that exports URDF and SMURF models | 5 |
| onshape-to-robot | Exports Onshape assemblies to URDF, SDF or MJCF | 5 |
| OCS2 | Optimal control and MPC toolbox for legged robots | 5 |
| Crocoddyl | Contact-aware optimal control with DDP solvers | 5 |
| TrajectoryOptimization | Trajectory optimisation in Julia | 5 |
| Bioptim | Musculoskeletal optimal control in Python | 5 |
| Ungar | C++ template library for optimal-control problems | 5 |
| Control Toolbox | C++ optimal control and MPC; inactive since 2021 | 5 |
| towr | Legged-robot trajectory optimisation; inactive since 2021 | 5 |
| FROST | MATLAB optimisation for hybrid systems; inactive since 2021 | 5 |
| Ceres Solver | Nonlinear least squares, used in SLAM and calibration | 5 |
| pymoo | Multi-objective optimisation in Python | 5 |
| CasADi | Symbolic differentiation and numerical optimisation, common for MPC | 5 |
| NLopt | Library of nonlinear optimisation algorithms | 5 |
| OSQP | Operator-splitting QP solver | 5 |
| Ipopt | Interior-point nonlinear solver | 5 |
| Pagmo | Parallel global optimisation | 5 |
| OptimLib | Small C++ nonlinear optimisation library | 5 |
| ifopt | Eigen interface to Ipopt and SNOPT | 5 |
| qpsolvers | One Python API over many QP solvers | 5 |
| hpipm | Interior-point QP solvers for MPC | 5 |
| Optimization Engine (OpEn) | Embedded nonconvex optimisation with code generation | 5 |
| SCS | Large-scale convex cone solver | 5 |
| ProxSuite | Proximal QP solvers from the pinocchio team | 5 |
| libcmaes | CMA-ES black-box optimisation | 5 |
| limbo | Gaussian processes and Bayesian optimisation | 5 |
| EXOTica | Optimisation toolset for robot motion | 5 |
| SHOT | Mixed-integer nonlinear solver | 5 |
| RobOptim | Numerical optimisation for robotics | 5 |
| lpsolvers | One Python API over LP solvers | 5 |
| eigen-qld | QLD QP solver for Eigen | 5 |
| sferes2 | Evolutionary computation; inactive since 2021 | 5 |

## Rejected

| Entry | Why | Date |
|---|---|---|
| Robopy | Inactive since 2021; Corke's Robotics Toolbox for Python covers it | 2026-11-18 |
| Trip | Small and inactive since 2022 | 2026-11-18 |
| trep | Small and inactive since 2023 | 2026-11-18 |
| metapod | Archived; inactive since 2018 | 2026-11-18 |
| Lively | Tiny and inactive since 2023 | 2026-11-18 |
| IBDS | Dead link: the page now shows the host's "not available" notice | 2026-11-18 |
| ARCSim | Graphics cloth simulator, unmaintained; not a robot tool | 2026-11-18 |
| Fluid Engine Dev - Jet | Graphics fluid engine, inactive since 2022; not a robot tool | 2026-11-18 |
| nphysics | Inactive since 2021; its makers point to Rapier instead | 2026-11-18 |
| qu3e | Archived small game physics engine | 2026-11-18 |
| Moby | Inactive since 2021, little use | 2026-11-18 |
| MBSlib | Inactive since 2016, little use | 2026-11-18 |
| PyBullet | Duplicate of Bullet: the same bullet3 repo | 2026-11-18 |
| Rigs of Rods | A soft-body driving game, not a robot simulator | 2026-11-18 |
| Neurorobotics Platform | Its site no longer responds; spiking-network simulation is too niche for builders | 2026-11-18 |
| Simbad | Abandoned: last SourceForge update 2013-05-02 | 2026-11-18 |
| Actin Simulation | Dead link: energid.com no longer responds; the list links an archived copy | 2026-11-18 |
| Artiminds | Dead link: the domain now redirects to an unrelated streaming site | 2026-11-18 |
| ROS Behavior Tree | Inactive since 2018; BehaviorTree.CPP took its place | 2026-11-18 |
| LibrePilot | Abandoned UAV autopilot, inactive since 2019 | 2026-11-18 |
| pymanoid | Archived; built on OpenRAVE | 2026-11-18 |
| TopiCo | Small and inactive since 2021 | 2026-11-18 |
| linalg.h | Small single-header maths library, inactive since 2023 | 2026-11-18 |
| Octree | Small neighbour-search code, inactive since 2019 | 2026-11-18 |
| Cover-Tree | Small and inactive since 2017 | 2026-11-18 |
| Kintinuous | Inactive since 2022; ElasticFusion by the same author supersedes it | 2026-11-18 |
| AprilSAM | Small and inactive since 2021 | 2026-11-18 |
| SRBA | Inactive since 2016 | 2026-11-18 |
| se(3)-TrackNet | Inactive research code; BundleTrack by the same author supersedes it | 2026-11-18 |
| DyNet | General neural-network toolkit, inactive since 2023; not robotics | 2026-11-18 |
| Ivy | Archived general ML framework; not robotics | 2026-11-18 |
| tiny-dnn | Abandoned since 2018 | 2026-11-18 |
| gym-gazebo | Archived in 2019; built for Gazebo Classic and OpenAI Gym | 2026-11-18 |
| Fido | Abandoned since 2017 | 2026-11-18 |
| MiniDNN | Small neural-network library, inactive since 2021; not robotics | 2026-11-18 |
| RLLib | Abandoned since 2016 (not Ray RLlib) | 2026-11-18 |
| gym-dart | Abandoned since 2020 | 2026-11-18 |
| Robot Gui | Small three.js demo, inactive since 2020 | 2026-11-18 |
| Awesome Gazebo | Archived; covers Gazebo Classic, inactive since 2021 | 2026-11-18 |
| Awesome Human Robot Interaction | Inactive since 2019 | 2026-11-18 |
| Awesome Grasping | Inactive since 2019 | 2026-11-18 |
