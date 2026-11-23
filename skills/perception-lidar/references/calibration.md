# Lidar extrinsics: lidar to camera, lidar to lidar

Part of [perception-lidar](../SKILL.md): find the transform between a lidar and a camera (or a second
lidar), write it into the URDF, and prove it. Camera intrinsics come first and belong to
[perception-camera](../../perception-camera/SKILL.md). Checked against the
`direct_visual_lidar_calibration` docs and CI on `main`, SciPy's `Rotation` API, and the RViz
`jazzy` Camera display; the conversion script was run on the tool's sample `calib.json`.

## What is being calibrated

The result is one rigid transform: from the frame in the cloud's `header.frame_id` (for Ouster
`os_lidar`, not `os_sensor`) to the camera's optical frame (z forward, x right, y down). Start from
the CAD or tape-measured value already in the URDF; calibration refines it. Mount both sensors on
one rigid bracket first: a bracket that flexes makes any calibration worthless.

## Targetless: direct_visual_lidar_calibration

koide3's `direct_visual_lidar_calibration` (MIT) aligns lidar intensity with the camera image, with
no target. It handles spinning and non-repetitive (Livox) lidars and pinhole, fisheye and
omnidirectional cameras. It has no Jazzy binary; its CI builds Docker images for `jazzy`, `humble`
and `noetic` (`koide3/direct_visual_lidar_calibration:jazzy`), or build from source after GTSAM,
Ceres and Iridescence (its installation page pins the versions):

```bash
cd ~/ros2_ws/src && git clone --recursive https://github.com/koide3/direct_visual_lidar_calibration.git
cd ~/ros2_ws && colcon build --packages-select direct_visual_lidar_calibration
```

The optional automatic initial guess uses SuperGlue, whose licence forbids commercial use; the
manual initial guess avoids it.

**Collect data** (from the tool's data-collection page): the camera intrinsics are calibrated and the
sensors rigidly fixed; each bag holds `Image`, `CameraInfo` and `PointCloud2` and starts with the
rig at rest. A Livox stays still for 10 to 15 s; a spinning lidar is moved slowly up and down for
about 10 s (longer for 16 or 32 lines). Record several bags (the docs suggest 5 to 10) of scenes
with both structure and texture. The lidar must report a usable intensity channel.

**Run:**

```bash
ros2 run direct_visual_lidar_calibration preprocess bags/ preprocessed/ -a -d -v   # -d for spinning lidars
ros2 run direct_visual_lidar_calibration initial_guess_manual preprocessed/          # pick 3+ point pairs
ros2 run direct_visual_lidar_calibration calibrate preprocessed/
ros2 run direct_visual_lidar_calibration viewer preprocessed/                         # inspect the fit
```

`-a` picks the topics automatically and needs one image, camera_info and points topic per bag;
otherwise pass `--image_topic`, `--points_topic` and `--camera_info_topic`. The camera_info
`distortion_model` must be `plumb_bob` or `fisheye`, or give `--camera_model` and
`--camera_intrinsic` by hand. The result is in `preprocessed/calib.json`, under
`results.T_lidar_camera`, as `[x, y, z, qx, qy, qz, qw]`, with `p_lidar = T_lidar_camera * p_camera`:
the pose of the camera's optical frame in the lidar frame.

## From the result to the URDF

The URDF holds `camera_link` (x forward) and a fixed joint to `camera_optical_frame` with
`rpy="-pi/2 0 -pi/2"`, as in
[ros2-robot-description](../../ros2-robot-description/references/sensors-control-display.md). The
calibration gives the optical frame, so compose back to `camera_link` and express it in the camera
joint's parent. `tools/calib_to_urdf.py` in your package:

```python
"""Turn a lidar-camera calibration into the URDF origin of camera_link."""
import json
import sys

import numpy as np
from scipy.spatial.transform import Rotation


def matrix(xyz, quat_xyzw):
    """4x4 transform from a translation and an (x, y, z, w) quaternion."""
    t = np.eye(4)
    t[:3, :3] = Rotation.from_quat(quat_xyzw).as_matrix()
    t[:3, 3] = xyz
    return t


# calib.json: p_lidar = T_lidar_camera * p_camera, camera = optical frame (z forward).
values = json.load(open(sys.argv[1]))['results']['T_lidar_camera']
cloud_T_optical = matrix(values[:3], values[3:])

# From `ros2 run tf2_ros tf2_echo <parent> <cloud_frame>`: translation, then quaternion x y z w.
parent_T_cloud = matrix([float(v) for v in sys.argv[2:5]], [float(v) for v in sys.argv[5:9]])

# camera_link -> camera_optical_frame as in the URDF: rpy (-pi/2, 0, -pi/2), no offset.
link_T_optical = matrix([0, 0, 0], Rotation.from_euler('xyz', [-np.pi / 2, 0, -np.pi / 2]).as_quat())

parent_T_link = parent_T_cloud @ cloud_T_optical @ np.linalg.inv(link_T_optical)
xyz = parent_T_link[:3, 3]
rpy = Rotation.from_matrix(parent_T_link[:3, :3]).as_euler('xyz')  # URDF rpy: fixed axes x, y, z
print(f'<origin xyz="{xyz[0]:.4f} {xyz[1]:.4f} {xyz[2]:.4f}" '
      f'rpy="{rpy[0]:.4f} {rpy[1]:.4f} {rpy[2]:.4f}"/>')
```

```bash
ros2 run tf2_ros tf2_echo base_link os_lidar        # with the robot's description running
python3 calib_to_urdf.py preprocessed/calib.json 0.12 0 0.45  0 0 0 1   # its xyz, then x y z w
```

Paste the printed `<origin>` into the `camera_joint` (parent `base_link` here). With the tool's
sample result and an identity lidar pose it prints a near-zero `rpy`: a forward-looking camera.
SciPy's lower-case `'xyz'` is extrinsic x, then y, then z, which is URDF's roll, pitch, yaw. If the
camera driver publishes its own `camera_link` → optical TF (many depth-camera drivers do), use
that transform for `link_T_optical` instead of the URDF's.

## Prove it

- **RViz overlay, no code.** Add a Camera display on the **rectified** image (its `camera_info` must
  sit beside it), set Image Rendering to `background and overlay`, and enable the PointCloud2
  display with Color Transformer `AxisColor` or `Intensity`. Points must sit on the image's edges
  (door frames, poles, table corners) across the whole image, near and far. An offset of the same
  size on near and far objects is a rotation error; one that is large up close and shrinks with
  distance is a translation error (parallax).
  The Camera display projects with `camera_info`'s `P`, so on the raw, distorted image the overlay
  is off near the border even when the extrinsic is right.
- **Numbers.** `ros2 run tf2_ros tf2_echo os_lidar camera_optical_frame` must match `calib.json`.
- **Time.** Calibrate and check with the robot at rest. Any stamp offset between the camera and the
  lidar shows up as overlay error only while moving; check that with `ros2 topic delay` on both
  topics before blaming the extrinsic.

## Lidar to lidar: refine with ICP

For two lidars with overlapping views, save one cloud from each at the same moment with the robot
at rest (`pointcloud_to_pcd`, see [mapping-viz.md](mapping-viz.md)), take the URDF value as the
initial guess, and refine with Open3D (MIT; install as in [python-node.md](python-node.md)):

```python
import numpy as np
import open3d as o3d

source = o3d.io.read_point_cloud('rear_lidar.pcd').voxel_down_sample(0.05)    # rear lidar frame
target = o3d.io.read_point_cloud('front_lidar.pcd').voxel_down_sample(0.05)   # front lidar frame
target.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=0.2, max_nn=30))
init = np.eye(4)   # front_T_rear from the URDF: tf2_echo front_lidar_link rear_lidar_link
result = o3d.pipelines.registration.registration_icp(
    source, target, 0.2, init,
    o3d.pipelines.registration.TransformationEstimationPointToPlane())
print(result.fitness, result.inlier_rmse)   # share of matched points, their RMS distance (m)
print(result.transformation)                # refined front_T_rear
```

ICP converges only from a nearby guess, so keep the URDF value close. Low `fitness` means little
overlap or a bad start. Scenes with walls in several directions constrain all six degrees of
freedom; a long corridor leaves the motion along it free. Convert the result to an `<origin>` with
the same SciPy steps as above.
