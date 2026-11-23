# Goals, waypoints and the initial pose (Jazzy)

Part of [nav-nav2](../SKILL.md). Checked against `nav2_msgs` and `nav2_simple_commander` 1.3.14 (`jazzy` branch).

## Interfaces

| Name | Type | Use |
|---|---|---|
| `/initialpose` | topic `geometry_msgs/msg/PoseWithCovarianceStamped` | tell AMCL (or slam_toolbox localization, or the loopback sim) where the robot is |
| `/navigate_to_pose` | action `nav2_msgs/action/NavigateToPose` | one goal; field `pose`, optional `behavior_tree` (XML path) |
| `/goal_pose` | topic `geometry_msgs/msg/PoseStamped` | fire-and-forget goal; `bt_navigator` turns it into the action |
| `/navigate_through_poses` | action `nav2_msgs/action/NavigateThroughPoses` | one continuous run through several poses, no stop between them |
| `/follow_waypoints` | action `nav2_msgs/action/FollowWaypoints` | one `navigate_to_pose` per pose, with a task (wait, photo) at each |
| `/follow_gps_waypoints` | action `nav2_msgs/action/FollowGPSWaypoints` | the same from latitude/longitude; needs `navsat_transform_node` ([perception-slam](../../perception-slam/SKILL.md)) |

Goals are `PoseStamped` in `map` (any frame in TF works; it is transformed). A zero stamp means "latest".

## RViz

`nav2_bringup`'s `rviz_launch.py` loads `nav2_default_view.rviz` with the Nav2 panel.

- **2D Pose Estimate** publishes `/initialpose`; drag in the direction the robot faces.
- **Nav2 Goal** sends `navigate_to_pose` and shows feedback in the panel; **2D Goal Pose** publishes `/goal_pose`.
- The panel's "Waypoint / Nav Through Poses Mode" collects several Nav2 Goal clicks and sends them as
  `follow_waypoints` or `navigate_through_poses`; "Save WPs" and "Load WPs" keep the list in a file. Startup, Pause
  and Reset drive the lifecycle managers.
- Displays worth adding: `/global_costmap/costmap`, `/local_costmap/costmap`, `/plan`, `/particle_cloud`,
  `/local_costmap/published_footprint`, and the collision monitor's polygon topics.

## Command line

```bash
# Initial pose with 0.5 m and 0.26 rad standard deviations (x, y, yaw variances at indices 0, 7, 35)
ros2 topic pub --once /initialpose geometry_msgs/msg/PoseWithCovarianceStamped \
  "{header: {frame_id: map}, pose: {pose: {position: {x: 0.0, y: 0.0}, orientation: {w: 1.0}},
    covariance: [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.07]}}"

# One goal, facing +y (yaw 90 degrees: z = sin(yaw/2), w = cos(yaw/2))
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "{pose: {header: {frame_id: map}, pose: {position: {x: 2.0, y: 1.0}, orientation: {z: 0.707, w: 0.707}}}}" \
  --feedback

# Waypoints
ros2 action send_goal /follow_waypoints nav2_msgs/action/FollowWaypoints \
  "{poses: [{header: {frame_id: map}, pose: {position: {x: 2.0, y: 0.0}, orientation: {w: 1.0}}},
            {header: {frame_id: map}, pose: {position: {x: 2.0, y: 2.0}, orientation: {w: 1.0}}}]}"

ros2 action list -t                                   # what the stack offers
ros2 service call /global_costmap/clear_entirely_global_costmap nav2_msgs/srv/ClearEntireCostmap
ros2 service call /local_costmap/clear_entirely_local_costmap nav2_msgs/srv/ClearEntireCostmap
```

`NavigateToPose` feedback carries `current_pose`, `distance_remaining`, `estimated_time_remaining`,
`navigation_time` and `number_of_recoveries`; the result has `error_code` and `error_msg`. `FollowWaypoints` feedback
has `current_waypoint`; its result lists `missed_waypoints` (`index`, `goal`, `error_code`).

## Python: `nav2_simple_commander`

`BasicNavigator` wraps the actions and services. Install `ros-jazzy-nav2-simple-commander` (part of
`navigation2`) and add it as an `<exec_depend>`.

```python
#!/usr/bin/env python3
# my_robot_navigation/scripts/patrol.py: drive a loop of waypoints, report missed ones
import math

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult


def make_pose(nav: BasicNavigator, x: float, y: float, yaw: float) -> PoseStamped:
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = nav.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.orientation.z = math.sin(yaw / 2.0)
    pose.pose.orientation.w = math.cos(yaw / 2.0)
    return pose


def main() -> None:
    rclpy.init()
    nav = BasicNavigator()

    # Skip this line if the robot is already localized (it re-seeds AMCL)
    nav.setInitialPose(make_pose(nav, 0.0, 0.0, 0.0))
    # Waits for AMCL (and its first pose) and bt_navigator to be active;
    # localizer='slam_toolbox' or 'robot_localization' for other setups
    nav.waitUntilNav2Active(localizer='amcl')

    waypoints = [
        make_pose(nav, 2.0, 0.0, 0.0),
        make_pose(nav, 2.0, 2.0, math.pi / 2),
        make_pose(nav, 0.0, 0.0, math.pi),
    ]
    nav.followWaypoints(waypoints)

    start = nav.get_clock().now()
    while not nav.isTaskComplete():          # spins the node for 0.1 s per call
        feedback = nav.getFeedback()
        if feedback:
            nav.get_logger().info(f'waypoint {feedback.current_waypoint + 1} of {len(waypoints)}')
        if (nav.get_clock().now() - start).nanoseconds > 600e9:
            nav.cancelTask()                 # give up after 10 minutes

    result = nav.getResult()
    if result == TaskResult.SUCCEEDED:
        nav.get_logger().info('patrol finished')
    else:
        nav.get_logger().error(f'patrol ended with {result}')

    nav.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Other calls worth knowing: `goToPose(pose)`, `goThroughPoses(poses)`, `followPath(path)`,
`getPath(start, goal)` (plan only, no motion), `spin()`, `backup()`, `clearAllCostmaps()`, `changeMap(yaml_path)`,
`dockRobotByID(dock_id)`, `undockRobot()`, `lifecycleStartup()` (when `autostart` is false). Each task call
returns after the goal is accepted; poll `isTaskComplete()` and read `getResult()` (`SUCCEEDED`, `CANCELED`,
`FAILED`, `UNKNOWN`). Only one task runs at a time per navigator.

## Waypoints or through-poses

- `FollowWaypoints`: stops at each pose, can run a task there (`WaitAtWaypoint`, `PhotoAtWaypoint`,
  `InputAtWaypoint`), and with `stop_on_failure: false` skips a pose it cannot reach and reports it as missed.
- `NavigateThroughPoses`: plans through all poses at once and drives without stopping; it fails as a whole.
  The Jazzy action field `poses` is `geometry_msgs/PoseStamped[]` (Lyrical: `nav_msgs/Goals`).
- A loop that runs forever (patrol) is a script around either action; keep the goal list in a YAML file in the
  package so the tested route is the committed one.

## Checks

- `ros2 topic echo --once /amcl_pose` is near where the robot stands after the initial pose.
- A goal ends with status `SUCCEEDED`; the robot is inside the goal checker tolerances.
- A goal inside a wall is rejected or fails quickly with an error code, not after minutes of recoveries.
- The waypoint script logs each waypoint and reports missed ones by index.
