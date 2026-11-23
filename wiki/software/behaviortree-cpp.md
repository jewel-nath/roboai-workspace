---
type: tool
name: BehaviorTree.CPP
summary: MIT-licensed C++17 behavior-tree library that runs Nav2's navigation logic and robot mission layers; v4 (behaviortree_cpp 4.11.1) is released from Humble to Rolling, v3.8 only for Humble and Jazzy. Its Groot2 editor is closed-source freeware with a paid PRO tier.
tags: [behavior-tree, task-logic, nav2, xml, blackboard, groot2, ros2, cpp, state-machine, mission-planning]
kind: library
area: nav
support:
license: MIT
links: {repo: "https://github.com/BehaviorTree/BehaviorTree.CPP", docs: "https://www.behaviortree.dev/docs/intro", site: "https://www.behaviortree.dev"}
version: {tested: , latest: 4.11.1, as_of: 2026-11-24}
platforms: [linux, windows, macos]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-24
sources:
  - {url: "https://github.com/BehaviorTree/BehaviorTree.CPP", title: "BehaviorTree.CPP repository, master and v3.8 branches: README, LICENSE, package.xml, CHANGELOG, CMakeLists, headers, sources, 3rdparty; issue tracker", accessed: 2026-11-24}
  - {url: "https://www.behaviortree.dev/docs/migration", title: "BT.CPP docs: Migration from BT.CPP 3.x to 4.x", accessed: 2026-11-24}
  - {url: "https://www.behaviortree.dev/docs/nodes-library/SequenceNode", title: "BT.CPP docs: Sequences", accessed: 2026-11-24}
  - {url: "https://www.behaviortree.dev/docs/tutorial-basics/tutorial_02_basic_ports", title: "BT.CPP docs: Blackboard and ports", accessed: 2026-11-24}
  - {url: "https://www.behaviortree.dev/groot", title: "Groot2 page: features, Free and PRO tiers, downloads, FAQ", accessed: 2026-11-24}
  - {url: "https://github.com/BehaviorTree/Groot2", title: "Groot2 repository: README changelog and issue tracker (no source code)", accessed: 2026-11-24}
  - {url: "https://github.com/BehaviorTree/Groot", title: "Groot (version 1) repository: README with deprecation notice and licence", accessed: 2026-11-24}
  - {url: "https://github.com/BehaviorTree/BehaviorTree.ROS2", title: "BehaviorTree.ROS2 repository: README, LICENSE, package.xml, docs", accessed: 2026-11-24}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling", accessed: 2026-11-24}
  - {url: "https://github.com/ros-navigation/navigation2", title: "Nav2 repository, humble and jazzy branches: nav2_behavior_tree package.xml, default BT XML, bt_navigator and BT engine sources, nav2_params.yaml", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/jazzy/configuration_and_development/configuration_guide/core_servers/configuring_bt_navigator/", title: "Nav2 docs (Jazzy): Behavior-Tree Navigator configuration", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/jazzy/tutorials/plugin_tutorials/writing_new_bt_plugin/", title: "Nav2 docs (Jazzy): Writing a New Behavior Tree Plugin", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/jazzy/tutorials/general_tutorials/groot_tutorials/groot2/groot2/", title: "Nav2 docs (Jazzy): Groot2, interacting with behavior trees", accessed: 2026-11-24}
  - {url: "https://docs.nav2.org/jazzy/configuration_and_development/migration_guides/iron/Iron/", title: "Nav2 docs: Iron to Jazzy migration guide", accessed: 2026-11-24}
---

# BehaviorTree.CPP

BT.CPP runs task logic written as an XML tree of reusable C++ nodes, loaded at run time, with
typed data passed through a shared blackboard [1]. Nav2's `bt_navigator` runs every navigation
goal as one of these trees [10][11], and the library works without ROS too [1]. MIT; Davide
Faconti (Auryn Robotics) maintains it: 4.11.1 on 2026-11-12, last commit 2026-11-13, 16 open
issues [1]. Its editor, **Groot2, is closed-source freeware with a paid PRO tier** [5][6].

## When to use it

- **Use it** to change how Nav2 behaves (recoveries, replanning, docking) by editing the XML and
  adding node plugins [11][12], or for mission logic that must react (stop on low battery, drop a
  task for a new goal) in place of a hand-written state machine, with or without ROS [1].
- **ROS 2 without Nav2:** BehaviorTree.ROS2 adds action, service and topic node wrappers and a tree
  executor behind a ROS action (Apache-2.0, BT.CPP 4.6+, last commit 2025-11-25). It has no
  rosdistro release; build it from source [8][9].
- **Use something else** on a Python-only robot (py_trees); for a fixed sequence with no
  reactions, a plain state machine is simpler.

## Versions

| Line | ROS package, apt name on Jazzy | Binary releases | Used by |
|---|---|---|---|
| v4 | `behaviortree_cpp`, `ros-jazzy-behaviortree-cpp` | 4.11.1 on Humble, Jazzy, Kilted, Lyrical, Rolling | Nav2 Jazzy and later |
| v3.8 | `behaviortree_cpp_v3`, `ros-jazzy-behaviortree-cpp-v3` | 3.8.7 on Humble, 3.8.8 on Jazzy | Nav2 Humble |

The `v3.8` branch only gets fixes (3.8.8, 2026-06-03) [1][9]; Nav2 moved to v4 in Jazzy [14].
From 3 to 4 [1][2]: headers move from `behaviortree_cpp_v3/` to `behaviortree_cpp/`; `<root>`
gains `BTCPP_format="4"`; `SequenceStar` becomes `SequenceWithMemory` and `AsyncActionNode`
becomes `ThreadedAction`; `<SubTreePlus>` syntax replaces the old `<SubTree>`; `<Script>` and
pre-conditions replace `SetBlackboard`; a new `SKIPPED` status appears; `tickRoot()` gives way to
`tickWhileRunning()`. The repo's `convert_v3_to_v4.py` converts XML; review what it writes.

## Setup

```bash
sudo apt install ros-jazzy-behaviortree-cpp      # v4; Nav2 already pulls it in
sudo apt install ros-jazzy-behaviortree-cpp-v3   # only for old v3 code
```

Without ROS: Conan, vcpkg (`behaviortree-cpp`), pixi or plain CMake, C++17. ZeroMQ (Groot2 link)
and SQLite (logging) are optional, through `BTCPP_GROOT_INTERFACE` and `BTCPP_SQLITE_LOGGING` [1].
CI covers Ubuntu, Windows, macOS and ROS 2 Humble, Jazzy, Lyrical and Rolling [1]. CPU only.

**Groot2** 1.10.0 (2026-11-09) has a Windows x86-64 installer, a Linux x86-64 installer or
AppImage, and a Linux aarch64 AppImage (still 1.9.0); no macOS build. **Free:** the editor,
multi-file projects, and the live monitor and log replay for trees of up to 20 nodes. **PRO** adds
any tree size, a blackboard view, breakpoints, fault injection and node search [5].
PRO is 590 EUR a year, a floating licence for one machine at a time, with a 30-day trial; it
needs internet to activate and every 7 days after [5]. The Groot2 repo has a changelog and an
issue tracker but no source or LICENSE file [6]. The FAQ promises an escrow release under
Apache-2.0 if Auryn Robotics closes, and says nothing on commercial use of the free tier [5].
Groot 1 (MIT) is in maintenance mode and works only with BT.CPP 3.8 [7].

## How an agent works with it

**The XML** (node names other than the built-ins are examples):

```xml
<root BTCPP_format="4" main_tree_to_execute="MainTree">
  <BehaviorTree ID="MainTree">
    <ReactiveSequence>
      <BatteryOK/>                 <!-- condition, re-checked on every tick -->
      <FollowPath path="{path}"/>  <!-- reads {path} from the blackboard; the one long action -->
    </ReactiveSequence>
  </BehaviorTree>
</root>
```

**Ticks.** The executor ticks the root; nodes return `SUCCESS`, `FAILURE` or `RUNNING`, and
conditions must not return `RUNNING` [1]. A `Sequence` resumes a running child without re-checking
earlier ones; a `ReactiveSequence` starts from its first child on every tick, so its conditions
are re-checked; a `SequenceWithMemory` also retries a failed child instead of restarting [3].

**Ports** [4]. A node declares `providedPorts()` with `InputPort<T>` and `OutputPort<T>`;
`getInput<T>()` returns an `Expected<T>` to check, and `setOutput()` writes. In XML a port takes a
literal or a `{key}`; ports sharing a key are joined through the blackboard. Scripted pre- and
post-conditions (`_skipIf`, `_failureIf`, `_while`, `_onSuccess`, `_onHalted` and others) go on
any node as attributes [1].

**A custom node** [1]. Derive from `BT::SyncActionNode` for one-tick work or
`BT::StatefulActionNode` (`onStart`, `onRunning`, `onHalted`) for long work. Register it with
`factory.registerNodeType<MyNode>("MyNode")`, or export it with `BT_REGISTER_NODES` and load it
with `registerFromPlugin`; then `registerBehaviorTreeFromFile`, `createTree` and
`tree.tickWhileRunning()`.

**Logging** [1]: `StdCoutLogger` prints transitions; `FileLogger2` (`.btlog`) and `SqliteLogger`
(`.db3`) record them for replay in Groot2, which needs those suffixes; `MinitraceLogger` writes a
Chrome-tracing JSON; `Groot2Publisher` serves the live monitor over ZeroMQ on port 1667.

**In Nav2 (Jazzy)** [10][11][12][13]:

- `bt_navigator` ticks `default_nav_to_pose_bt_xml` (defaults in `nav2_bt_navigator/behavior_trees`)
  every `bt_loop_duration` (10 ms); a `NavigateToPose` goal may name its own `behavior_tree`.
- Nav2's nodes (`ComputePathToPose`, `FollowPath`, `Spin`, `BackUp`, `RecoveryNode` and more) are
  plugins in `nav2_behavior_tree`; Groot2 needs their palette, `nav2_tree_nodes.xml`.
- A node that calls a ROS 2 action derives from `nav2_behavior_tree::BtActionNode<ActionT>`,
  overrides `on_tick()`, exports with `BT_REGISTER_NODES` and goes in `plugin_lib_names`.
- Live view: `navigate_to_pose.enable_groot_monitoring: true` serves Groot2 on port 1667
  (`navigate_through_poses` on 1669).

**Checking it works:** `ros2 lifecycle get /bt_navigator` says `active`, a goal from RViz succeeds
in simulation, the log has no "already registered" or unknown-node errors, and Groot2 shows the
tree ticking. [skills/nav-nav2/SKILL.md](../../skills/nav-nav2/SKILL.md) covers Nav2 bring-up.

## Traps

- **Wrong major version.** Nav2 Humble builds against v3, Jazzy against v4 [10][14]. Humble's apt
  has both, so a plugin built against the wrong one will not load.
- **v3 habits.** A `<root>` without `BTCPP_format` only prints a warning [1], then fails on
  `SequenceStar`, old `<SubTree>` remapping or `SetBlackboard`; convert it [2]. Custom control and
  decorator nodes must also skip past children that return `SKIPPED` [2][14].
- **Nav2 plugins listed twice.** Jazzy loads its built-in BT libraries itself and appends
  `plugin_lib_names` [10][11]. A Humble-era list registers each node twice; BT.CPP throws "ID
  [...] already registered" and the navigator fails to configure [1]. List only your own.
- **Blocking ticks.** A `SyncActionNode` that waits stalls the whole tree, Nav2's 10 ms loop too;
  return `RUNNING` from a stateful node instead. Under a `ReactiveSequence`, a child that returns
  `RUNNING` halts all the others [1], so put conditions first and one action last [3].
- **Port types.** Ports joined by a `{key}` must share a type, or `createTree` throws [4].
- **Groot2 and Nav2.** Nav2's default navigate-to-pose tree has 28 nodes by our count [10], over
  the free tier's 20-node limit for monitoring and replay [5]. Editing is free; watching it live
  needs PRO.
- **Minor releases change behaviour.** 4.11 made `Finally` a built-in ID (a custom node of that
  name now fails to register), reserved `_onlyIf` and `_onStart`, and changed script literals [1].
  Every distro got 4.11.1 through apt at once [9]; read the CHANGELOG after updating.

## Alternatives

[Nav2](nav2.md) is the stack this library drives. Others: py_trees and py_trees_ros (Python),
SMACH and FlexBE (state machines), BehaviorTree.ROS2 for trees outside Nav2 [8].

## Sources

1. [BehaviorTree.CPP repository, master and v3.8 branches: README, LICENSE, package.xml, CHANGELOG, CMakeLists, headers, sources, 3rdparty; issue tracker](https://github.com/BehaviorTree/BehaviorTree.CPP), accessed 2026-11-24
2. [BT.CPP docs: Migration from BT.CPP 3.x to 4.x](https://www.behaviortree.dev/docs/migration), accessed 2026-11-24
3. [BT.CPP docs: Sequences](https://www.behaviortree.dev/docs/nodes-library/SequenceNode), accessed 2026-11-24
4. [BT.CPP docs: Blackboard and ports](https://www.behaviortree.dev/docs/tutorial-basics/tutorial_02_basic_ports), accessed 2026-11-24
5. [Groot2 page: features, Free and PRO tiers, downloads, FAQ](https://www.behaviortree.dev/groot), accessed 2026-11-24
6. [Groot2 repository: README changelog and issue tracker (no source code)](https://github.com/BehaviorTree/Groot2), accessed 2026-11-24
7. [Groot (version 1) repository: README with deprecation notice and licence](https://github.com/BehaviorTree/Groot), accessed 2026-11-24
8. [BehaviorTree.ROS2 repository: README, LICENSE, package.xml, docs](https://github.com/BehaviorTree/BehaviorTree.ROS2), accessed 2026-11-24
9. [rosdistro distribution files: humble, jazzy, kilted, lyrical, rolling](https://github.com/ros/rosdistro), accessed 2026-11-24
10. [Nav2 repository, humble and jazzy branches: nav2_behavior_tree package.xml, default BT XML, bt_navigator and BT engine sources, nav2_params.yaml](https://github.com/ros-navigation/navigation2), accessed 2026-11-24
11. [Nav2 docs (Jazzy): Behavior-Tree Navigator configuration](https://docs.nav2.org/jazzy/configuration_and_development/configuration_guide/core_servers/configuring_bt_navigator/), accessed 2026-11-24
12. [Nav2 docs (Jazzy): Writing a New Behavior Tree Plugin](https://docs.nav2.org/jazzy/tutorials/plugin_tutorials/writing_new_bt_plugin/), accessed 2026-11-24
13. [Nav2 docs (Jazzy): Groot2, interacting with behavior trees](https://docs.nav2.org/jazzy/tutorials/general_tutorials/groot_tutorials/groot2/groot2/), accessed 2026-11-24
14. [Nav2 docs: Iron to Jazzy migration guide](https://docs.nav2.org/jazzy/configuration_and_development/migration_guides/iron/Iron/), accessed 2026-11-24
