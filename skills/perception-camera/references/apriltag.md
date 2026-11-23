# AprilTag detection with apriltag_ros

Part of [perception-camera](../SKILL.md). Checked against `apriltag_ros` 3.4.0 (tag `3.4.0`,
MIT), `apriltag_msgs` 2.0.2 and the AprilTag library 3.4.5 (BSD-2-Clause), all Jazzy binaries.
The library page is [apriltag](../../../wiki/software/apriltag.md).

## What it does

`apriltag_node` (component `AprilTagNode`) subscribes to a **rectified** image `image_rect` and
its `camera_info` through an `image_transport` camera subscriber, detects tags and publishes:

- `detections` (`apriltag_msgs/msg/AprilTagDetectionArray`): per tag `family`, `id`, `hamming`,
  `decision_margin`, `centre`, `corners` and the homography, with the image header.
- `/tf`: one transform per tag from the image's optical frame to `tag36h11:<id>` (family name
  plus id) or to the name you give in `tag.frames`. The tag frame has x right, y down and z into
  the tag, seen from the camera.

The pose uses `P` from `camera_info`, so feed it `image_rect`, not a distorted `image_raw`, and
both messages must carry the same stamp (an `image_proc` rectify node keeps the driver's stamp).

## Parameters

`my_robot_perception/config/apriltag.yaml` (node name `apriltag` by default):

```yaml
/**:
  ros__parameters:
    image_transport: raw            # or compressed
    qos_profile: sensor_data        # default is reliable; sensor_data accepts both kinds of publisher
    family: 36h11                   # 16h5, 25h9, 36h11, Circle21h7, Circle49h12, Custom48h12, Standard41h12, Standard52h13
    size: 0.100                     # metres; see "Tag size" below
    max_hamming: 0                  # corrected bits allowed; 0 rejects most false positives
    pose_estimation_method: pnp     # or homography
    detector:
      threads: 2
      decimate: 2.0                 # faster quad search on a smaller image; lower it for small or distant tags
      blur: 0.0
      refine: true
      sharpening: 0.25
    tag:                            # optional: only these ids get a TF
      ids: [0, 7]
      frames: [dock_tag, shelf_tag] # same length as ids, or empty
      sizes: [0.100, 0.160]         # per-tag sizes, or empty to use size
```

`family`, `size`, `tag.*`, `qos_profile` and `image_transport` are read-only after start-up;
`detector.*` and `max_hamming` can be changed with `ros2 param set /apriltag ...` while tuning.
`family` must match the printed tags; 36h11 is the default.

## Tag size

`size` is the length of the edge where the tag's black and white borders meet, which is where
the detector places the corners. It is not the outer edge of the printed square. For a 36h11 tag
that is the outer edge of the black square; for families with the white border inside (the
AprilTag README shows Custom48h12) it lies inside the printed square. A wrong size scales every
distance by the same factor, which is an easy check: a tag 1.00 m away that reads 1.25 m means
`size` is 25 % too large.

## Run it

```bash
sudo apt install ros-jazzy-apriltag-ros
ros2 run apriltag_ros apriltag_node --ros-args \
  -r image_rect:=/camera/image_rect \
  --params-file $(ros2 pkg prefix my_robot_perception)/share/my_robot_perception/config/apriltag.yaml
```

`camera_info` follows the image (`/camera/camera_info`). In a launch file, load
`apriltag_ros::AprilTagNode` into the same container as the rectify node to skip a copy of every
frame.

## Use the poses

- A tag at a known place in the world gives the camera's pose; a tag on an object gives the
  object's pose in `base_link` through TF:
  `ros2 run tf2_ros tf2_echo base_link dock_tag`.
- Look up the transform at the image's stamp, not the latest time, when the robot moves.
- A fixed tag in view is a quick check of the camera's mounting in the URDF: its pose in
  `base_link` must not change while the robot drives past it.
- Several tags on one rigid board give a steadier pose; `apriltag_ros` does not fuse bundles, so
  average their implied board poses yourself.
- `image_proc::TrackMarkerNode` covers a single ArUco marker (`dictionary`, `marker_id`,
  `marker_size`), publishing `tracked_pose` (`PoseStamped`).

## Checks

```bash
ros2 topic hz /detections
ros2 topic echo --once /detections --field detections
ros2 run tf2_ros tf2_echo camera_optical_frame tag36h11:0   # z = distance in front of the camera
```

- The z distance matches a tape measure; x grows when the tag moves right in the image.
- `hamming` is 0 and `decision_margin` is high for real tags; detections that come and go with
  low margins are glare, blur or a tag that is too small in the image.
- Tags far from the image centre still give the same distance as in the centre; if not, the
  calibration or the rectified input is wrong.
