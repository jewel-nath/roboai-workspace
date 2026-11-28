# Guides

Decision guides: one question, the options compared, and a recommendation with its conditions.
Template: [templates/guide.md](../../templates/guide.md).

- Name a file after the decision: `choose-an-actuator.md`, `choose-a-slam-package.md`.
- Compare options that have their own pages, and link to them.
- Say when the recommendation changes: budget, payload, skill level, ROS 2 or not.

## Index

<!-- index:start -->
| Guide | Question | Recommendation |
|---|---|---|
| [Choose a deployment method](choose-a-deployment-method.md) | How should I package, install and update the software on my ROS 2 robot? | Native for the first robot: ROS 2 Jazzy from apt, a colcon workspace and a hand-written systemd unit; from the second robot or the first field deployment, versioned releases - Docker Engine and Compose images deployed by digest, or your own debs on small hosts - with a health-gated rollout and rollback; jetson-containers or Isaac ROS images for CUDA on Jetson; an A/B OS update tool only when a failed OS update must never strand a robot. |
| [Choose a Nav2 planner and controller](choose-a-nav2-planner-and-controller.md) | Which Nav2 global planner and controller should my robot start with? | Smac 2D (or the shipped NavFn) with MPPI for a circular differential or omni base; Smac Hybrid-A* with MPPI or Regulated Pure Pursuit for a car-like or legged robot; Smac State Lattice with a footprint polygon for a non-circular base in tight spaces; Regulated Pure Pursuit when the CPU is small. |
| [Choose a robot learning policy](choose-a-robot-learning-policy.md) | Which policy should I train or fine-tune first for my robot? | ACT in LeRobot from about 50 demonstrations for one task on one arm; SmolVLA when one policy must follow language across tasks on a consumer GPU; pi0.5 or GR00T N1.7 only with a 40 GB-class training GPU and their weight terms read; Isaac Lab with RSL-RL PPO for locomotion, balance and in-hand skills nobody can teleoperate. |
| [Choose a robot simulator](choose-a-simulator.md) | Which simulator should I use for my robot? | Gazebo (Harmonic on Jazzy, Jetty on Lyrical) for a ROS 2 robot; MuJoCo for contact-rich control and learning; Isaac Sim only for photoreal sensors on an RTX GPU; CARLA for cars, Webots for teaching, Habitat only for embodied-AI navigation benchmarks. |
| [Choose a ROS 2 middleware](choose-a-ros2-middleware.md) | Which ROS 2 middleware (RMW) should my robot use? | Keep the default Fast DDS on one machine or a wired LAN; move the whole system to rmw_zenoh when nodes talk over Wi-Fi or across networks (Tier 1 from Kilted, so on Lyrical); use Cyclone DDS when the robot's SDK speaks it. |
| [Choose a SLAM system](choose-a-slam-system.md) | Which SLAM, odometry or state-estimation system should my robot run? | Fuse wheel odometry and IMU with robot_localization first; then SLAM Toolbox for a 2D lidar, RTAB-Map for an RGB-D or stereo camera or a 3D lidar (KISS-ICP, or RKO-LIO when an IMU is fitted, as its odometry), and OpenVINS for a camera plus IMU if GPL-3.0 suits you. |
| [Choose an arm motion planner](choose-an-arm-motion-planner.md) | Which motion planner should my robot arm use? | MoveIt 2 with OMPL's RRTConnect (the Jazzy default), KDL and TOTG for most ROS 2 arms, adding Pilz LIN for straight approaches; joint or position-only goals on 4- and 5-DoF hobby arms; cuRobo or Isaac ROS cuMotion only with an NVIDIA GPU and a need for millisecond or batched planning; Drake for optimisation work outside ROS. |
| [Choose an MCU and firmware stack](choose-an-mcu-and-firmware-stack.md) | Which microcontroller and firmware stack should run my robot's low-level loop, and how should it talk to ROS 2? | No MCU when smart serial-bus servos or CAN drives reach the computer through a USB adapter (ros2_control on the computer); otherwise an ESP32-S3 on ESP-IDF with micro-ROS on Jazzy, over USB or Wi-Fi, for a small base or servo robot; a Teensy 4.1 or STM32 Nucleo with a framed serial or CAN link into ros2_control for fast loops, many encoders or CAN joints; PX4 or ArduPilot on a flight controller for drones and outdoor rovers. |
<!-- index:end -->
