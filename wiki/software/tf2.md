---
type: tool
name: tf2
summary: The ROS 2 library that keeps every coordinate frame of a robot in one tree of transforms, buffered over time, so any node can ask where a sensor, wheel or gripper was relative to any other frame at a given moment.
tags: [ros2, tf2, transforms, coordinate-frames, rep-103, rep-105, static-transform-publisher, view-frames, tf2-echo, message-filter]
kind: library
area: ros2
support:
license: BSD-3-Clause
links: {repo: "https://github.com/ros2/geometry2", docs: "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Tf2-Main.html", site: }
version: {tested: , latest: 0.36.23, as_of: 2026-11-18}
platforms: [linux, windows, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/ros2/geometry2", title: "geometry2 repository (tf2, tf2_ros, tf2_ros_py, tf2_tools)", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html", title: "ROS 2 docs (Jazzy): Introducing tf2", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Static-Broadcaster-Py.html", title: "ROS 2 docs (Jazzy): Writing a static broadcaster (Python)", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Listener-Py.html", title: "ROS 2 docs (Jazzy): Writing a listener (Python)", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Learning-About-Tf2-And-Time-Cpp.html", title: "ROS 2 docs (Jazzy): Using time (C++)", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Debugging-Tf2-Problems.html", title: "ROS 2 docs (Jazzy): Debugging tf2 problems", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Using-Stamped-Datatypes-With-Tf2-Ros-MessageFilter.html", title: "ROS 2 docs (Jazzy): Using stamped datatypes with tf2_ros::MessageFilter", accessed: 2026-11-18}
  - {url: "https://www.ros.org/reps/rep-0103.html", title: "REP 103: Standard units of measure and coordinate conventions", accessed: 2026-11-18}
  - {url: "https://www.ros.org/reps/rep-0105.html", title: "REP 105: Coordinate frames for mobile platforms", accessed: 2026-11-18}
  - {url: "https://github.com/ros2/geometry2/blob/jazzy/tf2_ros/src/static_transform_broadcaster_program.cpp", title: "static_transform_publisher source, jazzy branch", accessed: 2026-11-18}
  - {url: "https://github.com/ros2/geometry2/blob/lyrical/tf2_ros/src/static_transform_broadcaster_program.cpp", title: "static_transform_publisher source, lyrical branch", accessed: 2026-11-18}
  - {url: "https://github.com/ros2/geometry2/blob/jazzy/tf2/src/buffer_core.cpp", title: "tf2 BufferCore source, jazzy branch", accessed: 2026-11-18}
  - {url: "https://control.ros.org/jazzy/doc/ros2_controllers/diff_drive_controller/doc/userdoc.html", title: "diff_drive_controller user documentation (Jazzy)", accessed: 2026-11-18}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files (humble, jazzy, lyrical)", accessed: 2026-11-18}
---

# tf2

tf2 keeps a robot's coordinate frames in one tree and stores every transform with its timestamp,
for 10 seconds by default, so a node can ask how frame A related to frame B at the moment a scan
was taken [2][5]. Every ROS 2 robot depends on it: robot_state_publisher feeds it from the
[URDF](urdf.md), odometry and localization add the mobile-base frames [9], and RViz, Nav2 and
MoveIt 2 read it.

## When to use it

- **Use it** whenever data measured in one frame is needed in another: a lidar point into
  `base_link`, a camera detection into `map`, a goal pose into the arm's base frame [2].
- **Static transforms** suit parts that never move relative to each other, such as a sensor mount;
  **dynamic** ones suit anything that moves [3]. Put fixed mounts in the URDF so
  robot_state_publisher publishes them, instead of running many static publishers.
- **Use something else** for data that is not a frame pose: joint commands and states go through
  [ros2_control](ros2-control.md), and object tracks are ordinary messages that carry a frame id.

## Setup

tf2 is part of every ROS 2 install. Jazzy ships geometry2 0.36.23, Lyrical 0.45.10 and Humble
0.25.24 [14]. The debugging tools and the tutorial demo [2]:

```bash
sudo apt install ros-jazzy-tf2-ros ros-jazzy-tf2-tools ros-jazzy-turtle-tf2-py
```

The tutorials give Windows and macOS build steps as well [3]. `view_frames` works only on Linux
[2] and calls Graphviz's `dot` to draw its PDF [1].

## How an agent works with it

The skill [skills/ros2-core/SKILL.md](../../skills/ros2-core/SKILL.md) covers TF debugging. Most of
the work is reading the tree from the command line:

```bash
ros2 run tf2_tools view_frames                 # listens 5 s, writes frames_<date>.gv and .pdf
ros2 run tf2_ros tf2_echo base_link laser_link # [source_frame] [target_frame], live
ros2 run tf2_ros tf2_monitor odom base_link    # rates and delays along the chain
ros2 topic echo /tf_static --once              # fixed transforms
ros2 run tf2_ros static_transform_publisher --x 0.1 --z 0.2 --yaw 1.5708 \
  --frame-id base_link --child-frame-id laser_link
```

`view_frames` takes `-t` (seconds to listen) and `-o` (output name) [1]. For
`static_transform_publisher`, only `--frame-id` and `--child-frame-id` are required; translation
is in metres, rotation either `--roll/--pitch/--yaw` in radians or `--qx/--qy/--qz/--qw`, never
both, and missing values default to the identity [3][10].

**In code** [1][4][5]: rclpy uses `Buffer`, `TransformListener(buffer, node)`,
`TransformBroadcaster(node)` and `StaticTransformBroadcaster(node)` from `tf2_ros`; rclcpp has the
same classes in `tf2_ros::`, plus `tf2_ros::MessageFilter`.

```python
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

self.tf_buffer = Buffer()
self.tf_listener = TransformListener(self.tf_buffer, self)
try:  # rclpy.time.Time() asks for the latest available transform
    t = self.tf_buffer.lookup_transform('base_link', 'laser_link', rclpy.time.Time())
except TransformException as ex:
    self.get_logger().warn(f'No transform yet: {ex}')
```

In C++ the latest transform is `tf2::TimePointZero`, and `lookupTransform()` takes an optional
timeout as its last argument [5]. For sensor messages, a `tf2_ros::MessageFilter` holds each
message until its transform is available [7].

**The conventions** that make other people's code work on your robot:

- **REP 103** [8]: SI units (metres, radians, seconds); right-handed frames with x forward, y left,
  z up on a body; east-north-up for local geographic frames; camera `_optical` frames with z
  forward, x right, y down; quaternions preferred for rotation.
- **REP 105** [9]: `base_link` is fixed to the robot; `odom` is continuous but drifts; `map` does not
  drift but jumps when localization corrects it. The tree is `map → odom → base_link`: an odometry
  source publishes `odom → base_link`, and localization publishes `map → odom`, never
  `map → base_link`, because a frame has one parent.

## Traps

- **"Lookup would require extrapolation into the future."** You asked for a time newer than the
  newest transform, usually `now()` [6]. Ask for the message's own stamp with a short timeout [5],
  use a MessageFilter for sensor data [7], or ask for the latest transform when that is good enough.
  `tf2_monitor` shows the delay on the chain [6].
- **Extrapolation into the past.** The buffer keeps about 10 s [5]; a lookup for older data fails.
  Process sensor data promptly or create the buffer with a longer cache.
- **Clocks that disagree.** tf2 compares header stamps [5], so mixed `use_sim_time` settings or
  unsynchronised computers break lookups. Set `use_sim_time` the same on every node and sync
  machine clocks. `TF_OLD_DATA` means a transform arrived older than the buffer's newest data by
  more than its window, and was dropped [12]; a looping bag or reset simulator often causes it.
- **Two publishers for one frame.** diff_drive_controller publishes `odom → base_link` by default
  (`enable_odom_tf`) [13]; add an EKF that does the same and the robot jitters. Keep one authority
  per transform [9].
- **Breaking the conventions.** Camera data in a body frame instead of an `_optical` frame comes out
  rotated; a compass heading used as yaw is wrong, because geographic yaw in ROS is zero pointing
  east and grows counter-clockwise [8]. Far from the `odom` origin, 32-bit data loses precision: REP 105 puts the
  limit near 83 km for centimetre accuracy [9].
- **Bad frame ids.** Ids must not be empty, must not start with `/` (ROS 1 habit), and a transform's
  parent and child must differ [12].
- **`static_transform_publisher` positional syntax.** Jazzy still accepts
  `x y z yaw pitch roll parent child`, with a deprecation warning (note: yaw first) [10]. Lyrical
  dropped it and stops with "Frame id must not be empty" [11]. Always use the flags.
- **Static and dynamic mixed up.** Static transforms are sent once at startup on `/tf_static` [3];
  a moving part published there stays frozen. Check with `ros2 topic echo /tf_static`.
- **Old headers and missing Python filter.** Humble code that includes
  `tf2_geometry_msgs/tf2_geometry_msgs.h` fails on Jazzy, where only `.hpp` headers exist; and
  tf2_ros_py has no MessageFilter, so Python nodes must wait on the buffer themselves [1].

## Alternatives

There is no real alternative inside ROS 2: every navigation, manipulation and visualization tool
expects tf2. Outside ROS, simulators keep their own frame trees (MuJoCo's body poses, Gazebo's
entity poses), and the [ros2_control](ros2-control.md) and [URDF](urdf.md) pages cover the two
sources that feed most of the tree.

## Sources

1. [geometry2 repository (tf2, tf2_ros, tf2_ros_py, tf2_tools)](https://github.com/ros2/geometry2), accessed 2026-11-18
2. [ROS 2 docs (Jazzy): Introducing tf2](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html), accessed 2026-11-18
3. [ROS 2 docs (Jazzy): Writing a static broadcaster (Python)](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Static-Broadcaster-Py.html), accessed 2026-11-18
4. [ROS 2 docs (Jazzy): Writing a listener (Python)](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Writing-A-Tf2-Listener-Py.html), accessed 2026-11-18
5. [ROS 2 docs (Jazzy): Using time (C++)](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Learning-About-Tf2-And-Time-Cpp.html), accessed 2026-11-18
6. [ROS 2 docs (Jazzy): Debugging tf2 problems](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Debugging-Tf2-Problems.html), accessed 2026-11-18
7. [ROS 2 docs (Jazzy): Using stamped datatypes with tf2_ros::MessageFilter](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Using-Stamped-Datatypes-With-Tf2-Ros-MessageFilter.html), accessed 2026-11-18
8. [REP 103: Standard units of measure and coordinate conventions](https://www.ros.org/reps/rep-0103.html), accessed 2026-11-18
9. [REP 105: Coordinate frames for mobile platforms](https://www.ros.org/reps/rep-0105.html), accessed 2026-11-18
10. [static_transform_publisher source, jazzy branch](https://github.com/ros2/geometry2/blob/jazzy/tf2_ros/src/static_transform_broadcaster_program.cpp), accessed 2026-11-18
11. [static_transform_publisher source, lyrical branch](https://github.com/ros2/geometry2/blob/lyrical/tf2_ros/src/static_transform_broadcaster_program.cpp), accessed 2026-11-18
12. [tf2 BufferCore source, jazzy branch](https://github.com/ros2/geometry2/blob/jazzy/tf2/src/buffer_core.cpp), accessed 2026-11-18
13. [diff_drive_controller user documentation (Jazzy)](https://control.ros.org/jazzy/doc/ros2_controllers/diff_drive_controller/doc/userdoc.html), accessed 2026-11-18
14. [rosdistro distribution files (humble, jazzy, lyrical)](https://github.com/ros/rosdistro), accessed 2026-11-18
