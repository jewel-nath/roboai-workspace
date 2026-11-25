# Hand-eye calibration

Part of [manip-grasping](../SKILL.md). Finds where the camera is relative to the arm, so a pose
seen in `camera_color_optical_frame` becomes a pose `base_link` can reach. Checked against
easy_handeye2 0.5.0 (`master`, 2026-08-20), MoveIt Calibration (`ros2` branch, 2025-11-28) and
the OpenCV `calibrateHandEye` documentation. Neither ROS package is in rosdistro for any distro;
both build from source on Jazzy. Not run.

## Which transform you solve

| Setup | Camera | Target (tag or board) | Result |
|---|---|---|---|
| Eye-in-hand | on the wrist | fixed on the table | `tool0` -> `camera_link` |
| Eye-to-hand (`eye_on_base` in easy_handeye2) | on a stand | fixed to the gripper | `base_link` -> `camera_link` |

The solver never needs to know where the target is; it cancels out. It needs pairs of
(`base_link` -> `tool0`, camera -> target) taken at many arm poses, still at each sample.

## Before sampling

- Camera intrinsics calibrated and `camera_info` correct ([perception-camera](../../perception-camera/SKILL.md)).
- A tag detector publishing the target as TF from the optical frame, for example `apriltag_ros`
  (`ros-jazzy-apriltag-ros`) on the rectified image, with `tag.frames: [calib_tag]` and the tag
  size measured after printing ([perception-camera apriltag reference](../../perception-camera/references/apriltag.md)).
  A large tag, or a ChArUco board with MoveIt Calibration, gives steadier poses than a small one.
- Robot TF correct: `ros2 run tf2_ros tf2_echo base_link tool0` matches the pendant.
- **No camera mount in the URDF while calibrating**, or behind a xacro argument. A frame has one
  parent: if the URDF already joins `tool0` to `camera_link`, the calibration's transform clashes
  with it. The driver keeps publishing `camera_link` -> `camera_color_optical_frame`.

## Option A: easy_handeye2 (LGPL-3.0, Python, rqt GUI)

```bash
cd ~/ws/src && git clone https://github.com/marcoesposito1988/easy_handeye2
sudo apt install python3-transforms3d python3-opencv
cd ~/ws && rosdep install -iyr --from-paths src   # its "python-transforms3d-pip" key does not exist
colcon build --packages-up-to easy_handeye2 && source install/setup.bash

# Eye-in-hand; robot driver, camera driver and apriltag_ros already running
ros2 launch easy_handeye2 calibrate.launch.py calibration_type:=eye_in_hand name:=wrist_cam \
  robot_base_frame:=base_link robot_effector_frame:=tool0 \
  tracking_base_frame:=camera_link tracking_marker_frame:=calib_tag
```

- `tracking_base_frame` is the camera's root frame (`camera_link`), not the optical frame: the
  tool looks up `camera_link` -> `calib_tag` through the driver's TF, and it publishes a dummy
  `tool0` -> `camera_link` while sampling so the tree is connected.
- The robot-motion GUI is not part of the current launch file: move the arm yourself (pendant,
  MoveIt in RViz), wait until it is still, then "Take Sample" in the rqt window. Rotate the tool as
  much as you can about each axis, both ways (the README asks for up to 90 degrees); translation
  matters less. Keep the tag in view and its TF steady.
- The result is recomputed after each sample (the algorithm is a drop-down). "Save" writes
  `~/.ros2/easy_handeye2/calibrations/wrist_cam.calib`.
- Use it: `ros2 launch easy_handeye2 publish.launch.py name:=wrist_cam` in every bringup that
  needs the camera, or copy the numbers into the URDF mount joint once and stop publishing it.
- `ros2 launch easy_handeye2 evaluate.launch.py name:=wrist_cam` opens an rqt evaluator for the
  saved calibration.

## Option B: MoveIt Calibration (BSD, C++, RViz panel)

```bash
cd ~/ws/src && git clone -b ros2 https://github.com/moveit/moveit_calibration
cd ~/ws && rosdep install -r --from-paths src --ignore-src --rosdistro jazzy -y
colcon build --packages-up-to moveit_calibration_gui --cmake-args -DCMAKE_BUILD_TYPE=Release
```

The README also says to `vcs import` a `moveit_calibration.repos` file; the `ros2` branch has no
such file, and its CI builds against Jazzy binaries, so skip that step. In RViz add the display
`moveit_rviz_plugin/HandEyeCalibration`: it detects an ArUco or ChArUco target (the README calls
ChArUco more accurate), takes a sample per button press, records the joint states so the same
poses can be replayed for a later recalibration, solves once it has five samples (Daniilidis
solver by default), and "Save camera pose" writes a launch file with a static transform publisher.
Its tutorial reports the result usually stops improving after about 12 to 15 samples; that page
in moveit2_tutorials is still marked as a MoveIt 1 page.

## Option C: OpenCV directly (cross-check or no GUI)

`cv2.calibrateHandEye` needs at least two motions with non-parallel rotation axes; take many more.
Eye-in-hand: pass gripper-in-base and target-in-camera; you get camera-in-gripper. Eye-to-hand:
pass base-in-gripper (the inverse) instead; you get camera-in-base.

```python
#!/usr/bin/env python3
# handeye_cv.py: eye-in-hand calibration from TF samples. apt: python3-opencv python3-scipy
import sys
import threading

import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.time import Time
from scipy.spatial.transform import Rotation
from tf2_ros import Buffer, TransformListener

BASE, EFFECTOR = 'base_link', 'tool0'
OPTICAL, CAM_ROOT, TARGET = 'camera_color_optical_frame', 'camera_link', 'calib_tag'


def to_matrix(tf):
    q, t = tf.transform.rotation, tf.transform.translation
    m = np.eye(4)
    m[:3, :3] = Rotation.from_quat([q.x, q.y, q.z, q.w]).as_matrix()
    m[:3, 3] = [t.x, t.y, t.z]
    return m


def main():
    rclpy.init()
    node = Node('handeye_cv')
    buf = Buffer()
    TransformListener(buf, node)
    threading.Thread(target=rclpy.spin, args=(node,), daemon=True).start()
    base_tool, cam_tag = [], []
    print('Hold the arm still, Enter = sample, q + Enter = solve')
    while sys.stdin.readline().strip() != 'q':
        try:
            g = buf.lookup_transform(BASE, EFFECTOR, Time())   # tool0 pose in base_link
            c = buf.lookup_transform(OPTICAL, TARGET, Time())  # tag pose in the optical frame
        except Exception as e:  # TF not available yet
            print('skipped:', e)
            continue
        age = node.get_clock().now() - Time.from_msg(c.header.stamp)
        if age.nanoseconds > 5e8:  # the tag TF stops updating when the tag is lost
            print('skipped: tag not seen in the last 0.5 s')
            continue
        base_tool.append(to_matrix(g))
        cam_tag.append(to_matrix(c))
        print(f'{len(base_tool)} samples')
    if len(base_tool) < 3:
        sys.exit('need at least 3 samples')

    R, t = cv2.calibrateHandEye(
        [m[:3, :3] for m in base_tool], [m[:3, 3] for m in base_tool],
        [m[:3, :3] for m in cam_tag], [m[:3, 3] for m in cam_tag],
        method=cv2.CALIB_HAND_EYE_PARK)
    tool_opt = np.eye(4)
    tool_opt[:3, :3], tool_opt[:3, 3] = R, t.ravel()

    # Consistency: the fixed tag seen from every sample should land on one point in base_link
    tags = np.array([(b @ tool_opt @ c)[:3, 3] for b, c in zip(base_tool, cam_tag)])
    print('tag position spread (std, mm):', np.round(tags.std(axis=0) * 1000, 1))

    # Express the result for the camera's root frame, which the URDF or a static TF uses
    root_opt = to_matrix(buf.lookup_transform(CAM_ROOT, OPTICAL, Time()))
    tool_root = tool_opt @ np.linalg.inv(root_opt)
    xyz = tool_root[:3, 3]
    rpy = Rotation.from_matrix(tool_root[:3, :3]).as_euler('xyz')  # URDF roll-pitch-yaw
    print(f'<origin xyz="{xyz[0]:.4f} {xyz[1]:.4f} {xyz[2]:.4f}" '
          f'rpy="{rpy[0]:.4f} {rpy[1]:.4f} {rpy[2]:.4f}"/>  <!-- {EFFECTOR} -> {CAM_ROOT} -->')
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Run it with `python3 handeye_cv.py` in a sourced shell. It is a recipe written for this skill and
was not run. Try other `method` values (`CALIB_HAND_EYE_TSAI`, `_HORAUD`, `_ANDREFF`,
`_DANIILIDIS`): if they disagree by more than your grasp tolerance, the samples are poor.

## Check the result

- **Spread:** the tag position computed through each sample (printed above, or easy_handeye2's
  evaluator) should agree within the accuracy your grasps need. Large spread: too little rotation
  between samples, an unsteady tag, a wrong tag size, or the arm still moving when sampled.
- **Touch test:** publish the result, have MoveIt move the `tcp` slowly to a point a few
  centimetres above a tag corner seen by the camera, then jog down by hand. The miss is your
  end-to-end error (calibration plus intrinsics plus robot accuracy).
- **Re-run** after the camera mount is bumped, the camera is refocused, or the gripper changes.

Sources: easy_handeye2 README, `docs/troubleshooting.md`, launch files and `__init__.py`;
moveit_calibration `ros2` README, plugin XML and CI workflow; moveit2_tutorials
`hand_eye_calibration_tutorial.rst` (marked `:moveit1:`); OpenCV `calibrateHandEye` reference
(docs.opencv.org, calib3d); rosdistro `rosdep/python.yaml` and `jazzy/distribution.yaml`.
