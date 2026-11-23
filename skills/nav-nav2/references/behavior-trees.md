# Customizing Nav2's behavior trees (Jazzy)

Part of [nav-nav2](../SKILL.md). Checked against `nav2_bt_navigator` and `nav2_behavior_tree` 1.3.14 (`jazzy`
branch, `nav2_tree_nodes.xml`) and the docs.nav2.org behavior tree and Groot pages. Jazzy uses BehaviorTree.CPP 4.x
(`ros-jazzy-behaviortree-cpp`, MIT). Writing new BT node plugins is outside this skill; see the Nav2 tutorial
"Writing a New Behavior Tree Plugin" and [BehaviorTree.CPP](../../../wiki/software/behaviortree-cpp.md).

## How `bt_navigator` picks a tree

- Each navigator has a default: `default_nav_to_pose_bt_xml` and `default_nav_through_poses_bt_xml`, full paths.
  Unset, they load `navigate_to_pose_w_replanning_and_recovery.xml` and
  `navigate_through_poses_w_replanning_and_recovery.xml` from `nav2_bt_navigator`'s share directory.
- A goal may name another tree in its `behavior_tree` field (`NavigateToPose`, `NavigateThroughPoses`), or with
  `BasicNavigator.goToPose(pose, behavior_tree=path)`.
- The navigator keeps the loaded tree and reloads only when the requested file name changes. After editing the
  file, restart Nav2 or set `always_reload_bt_xml: true` while iterating.
- All Nav2 BT node libraries load automatically in Jazzy; `plugin_lib_names` lists only your own or extra ones
  (for example the docking nodes in [docking.md](docking.md)).
- `error_code_names` (`compute_path_error_code`, `follow_path_error_code`) are the blackboard keys whose codes are
  reported when navigation aborts; add the key of any action whose error code you wire into the tree.

## Shipped trees

In `$(ros2 pkg prefix nav2_bt_navigator)/share/nav2_bt_navigator/behavior_trees/`:

| File | Behavior |
|---|---|
| `navigate_to_pose_w_replanning_and_recovery.xml` | default: replan at 1 Hz; on failure clear costmaps, spin, wait, back up in turn |
| `navigate_to_pose_w_replanning_goal_patience_and_recovery.xml` | the default, plus waiting near the goal for an obstacle to clear before taking a long detour |
| `nav_to_pose_with_consistent_replanning_and_if_path_becomes_invalid.xml` | replan every 15 s or when the path is blocked, with recoveries |
| `navigate_w_recovery_and_replanning_only_if_path_becomes_invalid.xml` | replan only when the path is blocked, with recoveries |
| `navigate_w_replanning_distance.xml`, `_speed.xml`, `_time.xml` | replan every 1 m, in proportion to speed, or at 1 Hz; no recoveries |
| `navigate_w_replanning_only_if_goal_is_updated.xml` | plan once, replan only for a new goal; no recoveries |
| `odometry_calibration.xml` | drive a square, for odometry calibration |

Planner and controller IDs in these trees (`GridBased`, `FollowPath`) must match the plugin names in
`planner_server` and `controller_server`; choosing those plugins is in [nav-planning](../../nav-planning/SKILL.md).

## A custom tree: no reversing, replan by distance

For a robot with no rear sensing: never back up, replan every 0.5 m, and recover by clearing, waiting, then
spinning. Ports and node names are those of Jazzy's `nav2_tree_nodes.xml`.

```xml
<!-- my_robot_navigation/behavior_trees/navigate_no_backup.xml -->
<root BTCPP_format="4" main_tree_to_execute="MainTree">
  <BehaviorTree ID="MainTree">
    <RecoveryNode number_of_retries="4" name="NavigateRecovery">
      <PipelineSequence name="NavigateWithReplanning">
        <DistanceController distance="0.5">
          <RecoveryNode number_of_retries="1" name="ComputePathToPose">
            <ComputePathToPose goal="{goal}" path="{path}" planner_id="GridBased"
                               error_code_id="{compute_path_error_code}"/>
            <ClearEntireCostmap name="ClearGlobalCostmap-Context"
                                service_name="global_costmap/clear_entirely_global_costmap"/>
          </RecoveryNode>
        </DistanceController>
        <RecoveryNode number_of_retries="1" name="FollowPath">
          <FollowPath path="{path}" controller_id="FollowPath" error_code_id="{follow_path_error_code}"/>
          <ClearEntireCostmap name="ClearLocalCostmap-Context"
                              service_name="local_costmap/clear_entirely_local_costmap"/>
        </RecoveryNode>
      </PipelineSequence>
      <ReactiveFallback name="RecoveryFallback">
        <GoalUpdated/>
        <RoundRobin name="RecoveryActions">
          <Sequence name="ClearingActions">
            <ClearEntireCostmap name="ClearLocalCostmap-Subtree"
                                service_name="local_costmap/clear_entirely_local_costmap"/>
            <ClearEntireCostmap name="ClearGlobalCostmap-Subtree"
                                service_name="global_costmap/clear_entirely_global_costmap"/>
          </Sequence>
          <Wait wait_duration="3.0"/>
          <Spin spin_dist="1.57" error_code_id="{spin_error_code}"/>
        </RoundRobin>
      </ReactiveFallback>
    </RecoveryNode>
  </BehaviorTree>
</root>
```

```yaml
bt_navigator:
  ros__parameters:
    default_nav_to_pose_bt_xml: $(find-pkg-share my_robot_navigation)/behavior_trees/navigate_no_backup.xml
```

How the pieces work:

- `PipelineSequence` keeps ticking earlier children while later ones run, so planning continues during
  `FollowPath`. `DistanceController` ticks its child on the first tick and then each time the robot has moved
  `distance` metres; `RateController hz` does the same by time.
- `RecoveryNode number_of_retries` runs the first child, and on failure the second, then retries the first.
  The outer one bounds how many recovery rounds a goal gets before it aborts.
- `RoundRobin` runs one recovery per failure, moving to the next each time; `GoalUpdated` under
  `ReactiveFallback` interrupts recovery when a new goal arrives.
- `ClearEntireCostmap` service names are `<costmap>/clear_entirely_<costmap>`. Other common nodes: `BackUp`
  (`backup_dist`, `backup_speed`), `DriveOnHeading`, `ClearCostmapAroundRobot`, `GoalReached`, `IsBatteryLow`,
  `IsStuck`, `TruncatePath`, `SpeedController`.
- BehaviorTree.CPP 4 names: `SequenceWithMemory` (was `SequenceStar`), `<SubTree ID="..."/>` (was `SubTreePlus`);
  custom control and decorator nodes must handle a child returning `SKIPPED`. Convert v3 XML with
  `convert_v3_to_v4.py` from the BehaviorTree.CPP repository.

## Editing and watching trees with Groot 2

- Groot 2 edits BehaviorTree.CPP 3 and 4 trees; the original Groot works only with v3. Groot 2 is
  proprietary: the free tier edits any tree but monitors and replays logs of at most 20 nodes; the PRO tier
  (EUR 590 per year floating licence, behaviortree.dev, checked 2026-11-24) adds unlimited monitoring and the
  blackboard view. Nav2's default tree has more than 20 nodes, so live monitoring of it needs PRO.
- Editing: load the palette `$(ros2 pkg prefix nav2_behavior_tree)/share/nav2_behavior_tree/nav2_tree_nodes.xml`,
  then open the tree file. Unknown nodes mean the palette lacks them, not that the tree is wrong.
- Monitoring (off by default):

```yaml
bt_navigator:
  ros__parameters:
    navigate_to_pose:
      plugin: "nav2_bt_navigator::NavigateToPoseNavigator"
      enable_groot_monitoring: true
      groot_server_port: 1667            # node default; navigate_through_poses defaults to 1669
```

Without Groot, the same structure is readable in the XML; `ros2 topic echo /behavior_tree_log` shows node status
changes as they happen.

## Checks

- At activation `bt_navigator` logs no XML or `not registered` errors; a typo in a node name or port fails here.
- A goal through a corridor blocked by a box triggers the recoveries in the order written, then aborts after the
  outer retry count with an error code.
- The tree file is installed by the package and referenced with `$(find-pkg-share ...)`, not a home-directory path.
