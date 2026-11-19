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
| [Choose a ROS 2 middleware](choose-a-ros2-middleware.md) | Which ROS 2 middleware (RMW) should my robot use? | Keep the default Fast DDS on one machine or a wired LAN; move the whole system to rmw_zenoh when nodes talk over Wi-Fi or across networks (Tier 1 from Kilted, so on Lyrical); use Cyclone DDS when the robot's SDK speaks it. |
<!-- index:end -->
