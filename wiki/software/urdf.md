---
type: tool
name: URDF and xacro
summary: The XML robot description format of ROS - links, joints, inertia, visual and collision geometry - with xacro macros on top; the one file that robot_state_publisher, RViz, ros2_control, MoveIt 2 and Gazebo all read.
tags: [ros2, urdf, xacro, robot-description, robot-state-publisher, joint-state-publisher, sdf, mjcf, inertia, meshes, check-urdf]
kind: library
area: ros2
support:
license: BSD-3-Clause
links: {repo: "https://github.com/ros/urdfdom", docs: "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/URDF-Main.html", site: "https://wiki.ros.org/urdf/XML"}
version: {tested: , latest: 4.0.2, as_of: 2026-11-18}
platforms: [linux, windows, macos]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://github.com/ros/urdfdom", title: "urdfdom README: URDF versions 1.0, 1.1 and 1.2", accessed: 2026-11-18}
  - {url: "https://github.com/ros/urdfdom/tree/jazzy/urdf_parser", title: "urdfdom parser and tools, jazzy branch (model.cpp, joint.cpp, check_urdf, urdf_to_graphviz)", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Building-a-Visual-Robot-Model-with-URDF-from-Scratch.html", title: "ROS 2 docs (Jazzy): Building a visual robot model with URDF from scratch", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Adding-Physical-and-Collision-Properties-to-a-URDF-Model.html", title: "ROS 2 docs (Jazzy): Adding physical and collision properties", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Using-Xacro-to-Clean-Up-a-URDF-File.html", title: "ROS 2 docs (Jazzy): Using xacro to clean up your code", accessed: 2026-11-18}
  - {url: "https://github.com/ros/xacro/wiki", title: xacro wiki, accessed: 2026-11-18}
  - {url: "https://github.com/ros/robot_state_publisher/tree/jazzy", title: "robot_state_publisher README (jazzy)", accessed: 2026-11-18}
  - {url: "https://github.com/ros/joint_state_publisher", title: joint_state_publisher README, accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Releases/Release-Lyrical-Luth.html", title: "ROS 2 Lyrical Luth release notes: URDF and robot_state_publisher", accessed: 2026-11-18}
  - {url: "https://github.com/gazebosim/sdf_tutorials/blob/master/docs/urdf/sdf_extensions.md", title: "SDFormat extensions to URDF (the gazebo tag)", accessed: 2026-11-18}
  - {url: "https://github.com/gazebosim/sdformat/blob/main/src/parser_urdf.cc", title: "libsdformat URDF parser source (massless link handling)", accessed: 2026-11-18}
  - {url: "https://mujoco.readthedocs.io/en/stable/modeling.html#curdf", title: "MuJoCo documentation: URDF extensions", accessed: 2026-11-18}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files (humble, jazzy, lyrical)", accessed: 2026-11-18}
  - {url: "https://github.com/ros2/ros2/blob/jazzy/ros2.repos", title: "ROS 2 Jazzy core repos file", accessed: 2026-11-18}
---

# URDF and xacro

URDF (Unified Robot Description Format) is the XML file that describes a robot as a tree of links
joined by joints, each link with optional inertia, visual and collision geometry [1][3]. Xacro adds
properties, macros and arguments so the file stays short and parametric [5]. A builder writes one
description and every ROS tool reads it: robot_state_publisher turns it into TF frames, RViz draws
it, ros2_control finds its joints in it, and Gazebo and MuJoCo can load it [7][10][12].

## When to use it

- **Use it** for any robot that runs ROS 2: the description is how the rest of the stack learns
  your geometry. Write xacro, not raw URDF, once the robot has repeated parts or variants [5].
- **Know its limits.** URDF is a tree with one root link [3], so closed chains (four-bar linkages,
  parallel grippers) need a mimic joint or a simulator-specific format.
- **Use SDF** for whole Gazebo worlds and simulator-only features, and **MJCF** for MuJoCo work
  where contacts, tendons and actuators matter; keep URDF as the source for ROS and convert [10][12].

## Setup

Jazzy versions [13]: `urdfdom` 4.0.2 (the parser), `urdf` 2.10.1 (the ROS 2 wrapper), `xacro`
2.1.1, `robot_state_publisher` 3.3.4, `joint_state_publisher` 2.4.3. Lyrical ships `urdfdom`
6.0.0, which adds URDF versions 1.1 and 1.2 [1][9][13].

```bash
sudo apt install ros-jazzy-xacro ros-jazzy-robot-state-publisher \
  ros-jazzy-joint-state-publisher-gui ros-jazzy-urdf-launch ros-jazzy-urdf-tutorial
```

- `urdf`, `urdfdom` and `robot_state_publisher` are in the ROS 2 core repos, so Windows and macOS
  builds include them; xacro and joint_state_publisher are not [14]. `check_urdf` and
  `urdf_to_graphviz` are built with urdfdom and are on the path once Jazzy is sourced [2].

## How an agent works with it

The skill [skills/ros2-robot-description/SKILL.md](../../skills/ros2-robot-description/SKILL.md)
covers the full workflow. A description package usually holds `urdf/robot.urdf.xacro`, `meshes/`
and a launch file. Meshes are referenced as `package://<package>/meshes/<file>` [3], which points
into the installed package, so install `urdf/` and `meshes/` into its `share/` folder.

**Elements.** A `<link>` holds `<inertial>` (mass in kg, the inertia tensor's six values, and an
`<origin>` at the centre of mass), plus any number of `<visual>` and `<collision>` blocks with a
box, cylinder, sphere or mesh [3][4]. A `<joint>` has a type (`revolute`, `continuous`,
`prismatic`, `fixed`, `floating`, `planar`), a parent, a child, an `<origin>`, an `<axis>`, and a
`<limit>` [1][2]. Xacro adds `<xacro:property>`, `<xacro:macro params="...">`, `<xacro:arg>`
read with `$(arg name)`, `<xacro:include>`, `${...}` Python expressions and `<xacro:if>` [6].

**Commands an agent runs** [2][5]:

```bash
xacro urdf/robot.urdf.xacro use_mock:=true > /tmp/robot.urdf   # expand, args as name:=value
check_urdf /tmp/robot.urdf                    # parses it and prints the link tree
urdf_to_graphviz /tmp/robot.urdf robot        # writes robot.gv and robot.pdf
ros2 launch urdf_launch display.launch.py urdf_package:=my_robot_description \
  urdf_package_path:=urdf/robot.urdf.xacro    # RViz plus joint sliders
```

The last line uses [urdf_launch](https://github.com/ros/urdf_launch), which the xacro tutorial
recommends [5]. `check_urdf` also reads stdin (`xacro robot.urdf.xacro | check_urdf -`); it only
proves the XML parses into one tree, without opening meshes or judging inertia [2].

**At run time** robot_state_publisher takes the URDF in its `robot_description` parameter, which
must be set at startup, and republishes it on the `robot_description` topic with transient-local
QoS [7]. It publishes fixed joints once on `/tf_static` and movable joints on `/tf` whenever
`/joint_states` updates them [7]. On a desk, joint_state_publisher (or its `_gui` sliders) fills
`/joint_states` for every movable joint [8]; on the robot, ros2_control's joint_state_broadcaster
does (see [ros2_control](ros2-control.md)). In a launch file, wrap the xacro call as
`ParameterValue(Command(['xacro ', path]), value_type=str)` [5].

**Inertia from CAD.** Export from the CAD model, not by hand. Common exporters:
[onshape-to-robot](https://github.com/Rhoban/onshape-to-robot), the
[SolidWorks exporter](https://github.com/ros/solidworks_urdf_exporter),
[fusion2urdf-ros2](https://github.com/dheena2k2/fusion2urdf-ros2),
[FreeCAD CROSS](https://github.com/galou/freecad.cross) and [Phobos](https://github.com/dfki-ric/phobos)
for Blender. Check what you get: mass in kg, tensor in kg·m² about the centre of mass, axes
aligned with the inertial `<origin>` [4]. CAD reports often use g, mm and g·mm² about the part
origin; 1 g·mm² is 1e-9 kg·m². Compare each link with a box or cylinder of the same mass and size
(the formulas are linked from [4]).

**Starting points.** Before modelling a common robot, look in
[awesome-robot-descriptions](https://github.com/robot-descriptions/awesome-robot-descriptions)
(URDF, xacro and MJCF models with their licences),
[robot_descriptions.py](https://github.com/robot-descriptions/robot_descriptions.py) (loads them
from Python, downloading on first use), and
[MuJoCo Menagerie](https://github.com/google-deepmind/mujoco_menagerie) (curated MJCF). Each model
keeps its own licence.

**Converting.**

- **To SDF (Gazebo):** Gazebo converts URDF on load; run `gz sdf -p robot.urdf` to see the result.
  Add SDF content with `<gazebo reference="link_name">` blocks. Fixed joints are lumped into their
  parent link by default; set `<preserveFixedJoint>true</preserveFixedJoint>` in the joint's
  `<gazebo>` block to keep one [10].
- **From SDF:** the ROS package [sdformat_urdf](https://github.com/ros/sdformat_urdf) parses SDF
  into a URDF model.
- **To MJCF (MuJoCo):** MuJoCo loads URDF directly. Add a `<mujoco><compiler meshdir="..."
  discardvisual="false"/></mujoco>` element under `<robot>`, load, save as MJCF, and edit the MJCF
  from then on [12].

## Traps

- **URDF 1.1 and 1.2 break Jazzy.** `quat_xyzw`, `<capsule>` and acceleration, deceleration and
  jerk limits need `version="1.1"` or `"1.2"` on `<robot>` [1]. Jazzy's parser throws on any
  version but 1.0 [2], so a Lyrical-style file will not load on Jazzy or Humble. RViz cannot draw
  capsules yet [9].
- **Bad inertia.** An identity tensor equals a 0.1 m box of 600 kg; about 1e-3 kg·m² suits a
  mid-sized link [4]. Zero or near-zero inertia can collapse the model in real-time controllers
  [4]. In Gazebo, a link without mass under a movable joint is dropped with its children, and the
  only sign is a `not modeled in sdf` warning [11].
- **Missing limits and axes.** `revolute` and `prismatic` joints need `<limit>`, with `effort` and
  `velocity` required in URDF 1.0; a joint without `<axis>` silently uses x (1, 0, 0) [1][2].
- **Meshes in millimetres.** STL is the common format; DAE can carry its own colours [3]. A mesh
  exported in mm needs `scale="0.001 0.001 0.001"` or it renders 1000 times too big [3]. Tools
  outside ROS do not resolve `package://` paths; MuJoCo needs `meshdir` [12].
- **Links stacked at the origin** in RViz mean TF is missing for movable joints: nothing publishes
  `/joint_states` for them [7]. Run exactly one source, not joint_state_publisher next to a
  joint_state_broadcaster.
- **Xacro surprises** [5][6]: without `xmlns:xacro="http://www.ros.org/wiki/xacro"` on `<robot>` the
  file does not parse; properties are evaluated lazily, so they cannot be reassigned; `${}` cannot
  hold braces; there are no loops (recurse a macro); a comment right before a xacro tag is removed.
- **Late subscribers miss the description** unless they use transient-local QoS on
  `robot_description` [7]. In Lyrical, robot_state_publisher can instead subscribe to that topic
  with `use_robot_description_topic` [9].
- **MuJoCo does not check URDF.** Mistyped attributes in a URDF or its `<mujoco>` block are
  silently ignored, and a joint's `effort` limit becomes its actuator force range [12].

## Alternatives

- **SDFormat** for Gazebo worlds and models, **MJCF** for MuJoCo: both richer than URDF, both
  reachable from it as above. **USD** is Isaac Sim's format (a later page).

## Sources

1. [urdfdom README: URDF versions 1.0, 1.1 and 1.2](https://github.com/ros/urdfdom), accessed 2026-11-18
2. [urdfdom parser and tools, jazzy branch (model.cpp, joint.cpp, check_urdf, urdf_to_graphviz)](https://github.com/ros/urdfdom/tree/jazzy/urdf_parser), accessed 2026-11-18
3. [ROS 2 docs (Jazzy): Building a visual robot model with URDF from scratch](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Building-a-Visual-Robot-Model-with-URDF-from-Scratch.html), accessed 2026-11-18
4. [ROS 2 docs (Jazzy): Adding physical and collision properties](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Adding-Physical-and-Collision-Properties-to-a-URDF-Model.html), accessed 2026-11-18
5. [ROS 2 docs (Jazzy): Using xacro to clean up your code](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/Using-Xacro-to-Clean-Up-a-URDF-File.html), accessed 2026-11-18
6. [xacro wiki](https://github.com/ros/xacro/wiki), accessed 2026-11-18
7. [robot_state_publisher README (jazzy)](https://github.com/ros/robot_state_publisher/tree/jazzy), accessed 2026-11-18
8. [joint_state_publisher README](https://github.com/ros/joint_state_publisher), accessed 2026-11-18
9. [ROS 2 Lyrical Luth release notes: URDF and robot_state_publisher](https://docs.ros.org/en/jazzy/Releases/Release-Lyrical-Luth.html), accessed 2026-11-18
10. [SDFormat extensions to URDF (the gazebo tag)](https://github.com/gazebosim/sdf_tutorials/blob/master/docs/urdf/sdf_extensions.md), accessed 2026-11-18
11. [libsdformat URDF parser source (massless link handling)](https://github.com/gazebosim/sdformat/blob/main/src/parser_urdf.cc), accessed 2026-11-18
12. [MuJoCo documentation: URDF extensions](https://mujoco.readthedocs.io/en/stable/modeling.html#curdf), accessed 2026-11-18
13. [rosdistro distribution files (humble, jazzy, lyrical)](https://github.com/ros/rosdistro), accessed 2026-11-18
14. [ROS 2 Jazzy core repos file](https://github.com/ros2/ros2/blob/jazzy/ros2.repos), accessed 2026-11-18
