# Grasp poses

Part of [manip-grasping](../SKILL.md). Three ways to get a pose for the `tcp` link, from cheapest
to most general, and how to filter them. Code written for this skill, not run. Contact-GraspNet
details were read from its repository (`NVlabs/contact_graspnet`, commit 7217060).

## The convention used everywhere here

- A grasp is the pose of `tcp` in `base_link` at the moment the fingers close. `tcp` sits midway
  between the fingertips; its **z axis points out of the palm toward the object** (the approach
  direction) and its **x axis runs from one finger to the other** (the closing direction). This
  matches Contact-GraspNet's grasp frame, so its output needs only a shift (below).
- Pre-grasp: the grasp moved back along its own z by the approach distance.
- A parallel gripper is the same grasp after 180 degrees about z. Keep whichever of the two is
  closer to the wrist's current yaw, or the wrist may spin half a turn.
- Make MoveIt plan for `tcp` (end-effector link in the SRDF, or `end_effector_link` in calls; see
  [manip-moveit2](../../manip-moveit2/SKILL.md)), so no flange offset is applied by hand.

## 1. Top-down heuristic (box-like or cylindrical objects on a table)

Input: the object's points in `base_link` with z up, already cut from the table (depth above the
table plane, or a detection mask projected through the depth image; see
[perception-camera](../../perception-camera/SKILL.md) and [perception-lidar](../../perception-lidar/SKILL.md)).

```python
# my_robot_manipulation/my_robot_manipulation/grasp_heuristics.py
import numpy as np


def top_down_grasp(points, max_opening, finger_depth, min_z, margin=0.01, tool_yaw=0.0):
    """points: Nx3 object points in base_link. Returns (4x4 tcp pose, width) or None.

    max_opening: widest finger gap (m); finger_depth: how far the fingertips go below the
    object's top (m); min_z: lowest allowed tcp z (table height plus fingertip clearance).
    """
    centre = points[:, :2].mean(axis=0)
    xy = points[:, :2] - centre
    _, vecs = np.linalg.eigh(np.cov(xy.T))     # ascending: first column = narrowest direction
    narrow = vecs[:, 0]
    width = np.ptp(xy @ narrow) + margin        # object extent across the fingers, plus margin
    if width > max_opening:
        return None
    x_axis = np.array([narrow[0], narrow[1], 0.0])
    if np.dot(x_axis[:2], [np.cos(tool_yaw), np.sin(tool_yaw)]) < 0:
        x_axis = -x_axis                         # pick the twin closer to the current wrist yaw
    z_axis = np.array([0.0, 0.0, -1.0])          # approach straight down
    y_axis = np.cross(z_axis, x_axis)            # right-handed: y = z x x
    pose = np.eye(4)
    pose[:3, :3] = np.column_stack([x_axis, y_axis, z_axis])
    pose[:3, 3] = [centre[0], centre[1], max(points[:, 2].max() - finger_depth, min_z)]
    return pose, width
```

Good for blocks, boxes, bottles standing up and anything you can pinch from above. It ignores the
object's shape below the top and its mass distribution: grasp near the centre of mass and lift
slowly. A point-cloud library can do the same with an oriented bounding box ([Open3D](../../../wiki/software/open3d.md),
[PCL](../../../wiki/software/pcl.md)).

## 2. From an object pose and a grasp library (known objects with a mesh)

A pose estimator gives the object frame; you define a few good grasps once in that frame.
[FoundationPose](../../../wiki/learning/models/foundationpose.md) through Isaac ROS publishes
`vision_msgs/Detection3DArray` on `pose_estimation/output` and a TF frame `fp_object`. The research
code and weights are research-and-evaluation only (NVIDIA Source Code License); Isaac ROS
FoundationPose is Apache-2.0 code with weights under an NVIDIA model licence, on an NVIDIA GPU.
An AprilTag stuck on a fixture is a licence-free pose source for parts that always sit in one jig.

```yaml
# my_robot_manipulation/config/grasps/mug.yaml: tcp poses in the object's mesh frame (metres, rad)
object_frame: fp_object
z_symmetry_steps: 1      # n > 1: object looks the same every 360/n degrees about its z axis
grasps:
  - {name: rim, xyz: [0.0, 0.035, 0.09], rpy: [3.1416, 0.0, 0.0], width: 0.012}
  - {name: body_side, xyz: [0.05, 0.0, 0.05], rpy: [0.0, -1.5708, 0.0], width: 0.08}
```

```python
import numpy as np
from scipy.spatial.transform import Rotation


def library_grasps(base_obj, entries, z_steps=1):
    """base_obj: 4x4 object pose in base_link (from TF). Returns [(name, 4x4 tcp pose, width)]."""
    out = []
    for k in range(z_steps):
        spin = np.eye(4)
        spin[:3, :3] = Rotation.from_euler('z', 2 * np.pi * k / z_steps).as_matrix()
        for e in entries:
            obj_tcp = np.eye(4)
            obj_tcp[:3, :3] = Rotation.from_euler('xyz', e['rpy']).as_matrix()  # URDF-style rpy
            obj_tcp[:3, 3] = e['xyz']
            out.append((e['name'], base_obj @ spin @ obj_tcp, e['width']))
    return out
```

Check the mesh's units and origin first: the poses are only as good as the mesh frame and the
estimator's fit. Show `fp_object` and each candidate in RViz on the real object before moving.

## 3. Learned 6-DoF grasps: Contact-GraspNet (cluttered or unknown objects)

[Contact-GraspNet](../../../wiki/learning/models/contact-graspnet.md) proposes grasps for a Franka
Panda-style parallel gripper from one depth image. **Licence: NVIDIA Source Code License,
non-commercial (research or evaluation only)**, for the code, its derivatives and in practice the
weights; do not ship it in a product. Its README tested Python 3.7, TensorFlow 2.2 and CUDA 11.1,
which cannot run in Jazzy's Python 3.12: run it in its own conda environment or container and pass
data across (files, a socket, or a small ROS node inside that environment with its own ROS
install). Unofficial PyTorch ports exist; read their licences on the wiki page.

- **Input:** depth in metres (ROS `16UC1` depth is millimetres: divide by 1000), the 3x3 `K` from
  `camera_info`, and ideally a segmentation map of the target (`--local_regions --filter_grasps`
  then keep grasps on that segment only). `--z_range` crops the cloud by distance.
- **Output:** per segment, `pred_grasps_cam` (Nx4x4, in the depth image's optical frame), `scores`,
  `contact_pts` and `gripper_openings`.
- **Frame:** each 4x4 is the Panda hand base: z = approach, x = closing direction, and the point
  between the contacts lies 0.1034 m along z (`gripper_depth` in `build_6d_grasp`). Convert:

```python
import numpy as np

PANDA_HAND_TO_CONTACTS = np.eye(4)
PANDA_HAND_TO_CONTACTS[2, 3] = 0.1034   # from contact_graspnet.build_6d_grasp


def cgn_to_tcp(base_optical, pred_grasps_cam, scores, openings, max_opening):
    """base_optical: 4x4 camera_color_optical_frame pose in base_link (TF after hand-eye)."""
    keep = []
    for g, s, w in zip(pred_grasps_cam, scores, openings):
        if w > max_opening:
            continue                      # your fingers cannot open that far
        keep.append((float(s), base_optical @ g @ PANDA_HAND_TO_CONTACTS, float(w)))
    return sorted(keep, key=lambda c: -c[0])
```

If your `tcp` is not at the fingertip centre, multiply by your own fixed offset as well. Its grasps
assume Panda fingers (an 8 cm stroke per the wiki page); for a smaller or longer gripper, the
width filter above and the depth check below carry the difference.

## Filter and rank, whatever the source

1. **Width:** object width plus margin below the gripper's maximum opening.
2. **Approach:** reject approaches from below the table; prefer near-vertical ones
   (`z_tcp . (0, 0, -1)` close to 1) unless the task needs a side grasp.
3. **Reachable and collision-free:** call move_group's `/compute_ik` service
   (`moveit_msgs/srv/GetPositionIK`: `ik_request.group_name: arm`, `ik_link_name: tcp`,
   `pose_stamped` in `base_link`, `avoid_collisions: true`, a short `timeout`) for the grasp **and**
   the pre-grasp. The target object must be in the planning scene for the pre-grasp check and
   removed (or its collisions allowed) for the grasp check.
4. **Rank:** model score, then approach angle, then distance from the current pose. Try the next
   candidate when planning or the grasp check fails, not the same one again.

Check before any motion: publish the survivors as a `geometry_msgs/PoseArray` or as TF frames and
look at them in RViz over the point cloud: fingers on both sides of the object, z into it.

Sources: NVlabs/contact_graspnet README, License.pdf, `contact_graspnet.py` (`build_6d_grasp`),
`contact_grasp_estimator.py`; Isaac ROS FoundationPose via the wiki page; moveit_msgs `ros2`
(`GetPositionIK.srv`, `PositionIKRequest.msg`); moveit2 `jazzy` (`capability_names.hpp`).
