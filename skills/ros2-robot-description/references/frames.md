# Frames: REP 103, REP 105 and checking the TF tree

Part of [ros2-robot-description](../SKILL.md). The [tf2](../../../wiki/software/tf2.md) page covers
the library itself.

## Conventions

REP 103 (units and axes) and REP 105 (mobile-base frames), as they apply to a description:

| Frame | Who publishes it | Rule |
|---|---|---|
| `map` | Localization (as `map` → `odom`) | World-fixed; may jump when localization corrects |
| `odom` | Odometry (as `odom` → `base_link` or `base_footprint`) | World-fixed; continuous, drifts |
| `base_footprint` (optional) | URDF root | On the ground under the base; parent of `base_link` |
| `base_link` | URDF | Rigidly attached to the base, x forward, y left, z up |
| `<part>_link` | URDF, `robot_state_publisher` | Body convention: x forward, y left, z up |
| `<camera>_optical_frame` | URDF (fixed joint from the camera link) | z forward, x right, y down; image messages use it |
| `earth` (multi-map only) | Static or localization | Parent of each robot's `map` |

- Units are SI (m, rad, kg, s), right-handed frames.
- The TF graph is a tree: one parent per frame. `map` is the parent of `odom`, `odom` of the base.
  Localization never publishes `map` → `base_link` directly.
- The URDF ends at the robot's root link. The robot's pose in the world is TF from odometry and
  localization, not a `floating` or `planar` joint: `robot_state_publisher` (through kdl_parser)
  turns those joints into fixed ones with a warning.
- Fixed sensor mounts belong in the URDF as fixed joints. Keep `static_transform_publisher` for
  frames outside the robot, such as a calibrated external camera:

```bash
ros2 run tf2_ros static_transform_publisher --x 1.2 --y 0 --z 2.1 \
  --roll 0 --pitch 0.6 --yaw 3.14159 --frame-id map --child-frame-id ceiling_camera_link
```

  The positional argument form still works but prints a deprecation warning.
- Several robots in one graph: give each `robot_state_publisher` a `frame_prefix` (for example
  `robot1/`) and run each robot in its own namespace.

## Inspecting the tree

```bash
ros2 run tf2_tools view_frames                       # 5 s of TF -> frames_<date>.pdf and .gv
ros2 run tf2_ros tf2_echo base_link camera_optical_frame
ros2 topic echo --once /tf_static                     # fixed joints from robot_state_publisher
```

`robot_state_publisher` sends fixed joints on `/tf_static` once and movable joints on `/tf` each
time a `/joint_states` message arrives. A movable joint with no joint state has no transform, and
RViz reports "No transform from [link] to [base_link]".

## Looking up a transform in code (rclpy)

```python
from geometry_msgs.msg import PoseStamped
from rclpy.node import Node
from rclpy.time import Time
from tf2_geometry_msgs import do_transform_pose_stamped
from tf2_ros import Buffer, TransformException, TransformListener


class FrameUser(Node):
    def __init__(self):
        super().__init__('frame_user')
        self._tf_buffer = Buffer()
        self._tf_listener = TransformListener(self._tf_buffer, self)

    def to_base(self, pose: PoseStamped) -> PoseStamped | None:
        try:
            # Time() asks for the latest transform; no timeout, so the callback never blocks.
            tf = self._tf_buffer.lookup_transform('base_link', pose.header.frame_id, Time())
        except TransformException as ex:
            self.get_logger().warning(f'cannot transform: {ex}', throttle_duration_sec=2.0)
            return None
        return do_transform_pose_stamped(pose, tf)
```

- `do_transform_pose` takes a `Pose`; for a `PoseStamped` use `do_transform_pose_stamped`.
- The listener shares the node's executor unless created with `spin_thread=True`. A
  `lookup_transform(..., timeout=...)` inside a callback on a single-threaded executor then waits
  for data that cannot arrive until the callback returns.
- To transform a sensor message, look up at the message's stamp instead of `Time()`; very recent
  stamps may not be in the buffer yet, so test with `can_transform` first (in C++,
  `tf2_ros::MessageFilter` does the waiting).
