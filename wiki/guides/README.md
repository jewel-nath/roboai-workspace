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
| [Choose a robot simulator](choose-a-simulator.md) | Which simulator should I use for my robot? | Gazebo (Harmonic on Jazzy, Jetty on Lyrical) for a ROS 2 robot; MuJoCo for contact-rich control and learning; Isaac Sim only for photoreal sensors on an RTX GPU; CARLA for cars, Webots for teaching, Habitat only for embodied-AI navigation benchmarks. |
| [Choose a ROS 2 middleware](choose-a-ros2-middleware.md) | Which ROS 2 middleware (RMW) should my robot use? | Keep the default Fast DDS on one machine or a wired LAN; move the whole system to rmw_zenoh when nodes talk over Wi-Fi or across networks (Tier 1 from Kilted, so on Lyrical); use Cyclone DDS when the robot's SDK speaks it. |
| [Choose a SLAM system](choose-a-slam-system.md) | Which SLAM, odometry or state-estimation system should my robot run? | Fuse wheel odometry and IMU with robot_localization first; then SLAM Toolbox for a 2D lidar, RTAB-Map for an RGB-D or stereo camera or a 3D lidar (KISS-ICP, or RKO-LIO when an IMU is fitted, as its odometry), and OpenVINS for a camera plus IMU if GPL-3.0 suits you. |
<!-- index:end -->
