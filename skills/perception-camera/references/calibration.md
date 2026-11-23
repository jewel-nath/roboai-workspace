# Intrinsic calibration and camera_info

Part of [perception-camera](../SKILL.md). Checked against `camera_calibration` 5.0.13 and
`camera_info_manager` 5.1.8 (Jazzy branches). Camera-to-lidar and camera-to-IMU extrinsics belong
to [perception-lidar](../../perception-lidar/SKILL.md) and
[perception-slam](../../perception-slam/SKILL.md) (Kalibr).

## What `sensor_msgs/CameraInfo` holds

| Field | Meaning | Used for |
|---|---|---|
| `width`, `height` | Resolution the calibration was made at | Must equal the image size |
| `distortion_model`, `d` | `plumb_bob` (k1 k2 p1 p2 k3), `rational_polynomial` (8 values), `equidistant` (fisheye, 4) | Undistorting raw pixels |
| `k` | 3x3 intrinsics of the **raw** image: fx, fy, cx, cy | Raw pixel to ray, with `d` |
| `r` | Rectification rotation; identity for a single camera | Stereo pairs |
| `p` | 3x4 projection of the **rectified** image (fx', fy', cx', cy', Tx, Ty) | Rectified pixel to ray, stereo baseline |
| `binning_x/y`, `roi` | Sub-sampling and crop applied after calibration | Scaling K and P |
| `header.frame_id` | The optical frame (z forward, x right, y down) | Where rays and points live |

- A pixel in `image_raw` maps through `k` and `d`; a pixel in `image_rect` maps through `p`. Mixing
  them shifts every 3D point, worst at the image edges.
- `camera_calibration` computes `p` with OpenCV's `getOptimalNewCameraMatrix` at `alpha = 0`,
  so `p` differs from `k` even for one camera.
- An uncalibrated driver publishes `k` and `p` as zeros; `image_proc` then logs "requested but
  camera publishing ... is uncalibrated" and publishes nothing.
- RealSense and OAK publish their factory calibration; you normally do not recalibrate them with
  this tool (they offer no `set_camera_info`).

## The target

- A chessboard printed flat and glued to something rigid. `--size` counts **interior corners**
  (a board of 9 x 7 squares is `8x6`); `--square` is the measured square edge in metres. Measure
  the print: printers scale.
- ChArUco boards (`--pattern charuco --charuco_marker_size <m> --aruco_dict 5x5_250`, one set of
  options per board) still work when partly hidden; `circles` and `acircles` are the other
  patterns. Several boards of different sizes can be given with repeated `--size`/`--square`.
- Calibrate at the resolution and focus you will run. Changing either invalidates `k` and `d`.

## Monocular calibration

```bash
sudo apt install ros-jazzy-camera-calibration
ros2 service list | grep set_camera_info            # the driver's service, e.g. /camera/front_camera_driver/set_camera_info
ros2 run camera_calibration cameracalibrator --size 8x6 --square 0.025 --ros-args \
  -r image:=/camera/image_raw \
  -r camera/set_camera_info:=/camera/front_camera_driver/set_camera_info
```

- The node looks up the publisher's QoS for `image` and falls back to sensor-data QoS, so it
  connects to reliable and best-effort drivers alike.
- It waits for `camera/set_camera_info` at start-up. Without that service, add
  `--no-service-check` and use SAVE instead of COMMIT.
- Options: `-c <name>` sets `camera_name` in the result (default `narrow_stereo`; set it to the
  driver's `camera_name`, or `camera_info_manager` warns that the names do not match);
  `-k 3` or more radial terms for wide lenses; `--fix-principal-point`, `--zero-tangent-dist`;
  `--max-chessboard-speed 0.5` drops blurred samples from rolling-shutter cameras.
- Fisheye lenses: move the "Camera type" slider in the window to 1 before calibrating; the result
  uses the `equidistant` model.
- The bundled tutorial writes remaps without `--ros-args`; rcl still accepts that form in Jazzy
  but warns that it is deprecated.

**Moving the board.** Hold it still at each pose until the window highlights it. Cover the left,
right, top and bottom of the view, near and far, and tilted in both axes; get it into the corners,
where distortion is largest. The X, Y, Size and Skew bars fill as coverage grows. When CALIBRATE
lights up, press it and wait (the window greys out while it solves).

**Judge the result** in the window: straight edges in the scene must look straight after
undistortion; a failed solve shows a blank or warped image. The slider at the top sets the
rectified scale from 0.0 (only valid pixels, some of the view cropped) to 1.0 (all pixels, black
borders).

**Keep it.**
- SAVE writes `/tmp/calibrationdata.tar.gz` with the sample images, `ost.yaml` and `ost.txt`.
  Copy `ost.yaml` into your package (`my_robot_perception/config/front_camera_info.yaml`) and point
  `camera_info_url` at it.
- COMMIT sends the result to the driver through `set_camera_info`; `camera_info_manager` writes it
  to the driver's `camera_info_url`, or to `~/.ros/camera_info/<camera_name>.yaml` when the URL is
  empty. A `package://` URL usually points into the install space; check where it was written.
- Commit the YAML to the repository with the robot's name and the lens and resolution in the file
  name or a comment. Each physical camera needs its own file.

## The calibration file

```yaml
image_width: 1280
image_height: 720
camera_name: front_camera
camera_matrix: {rows: 3, cols: 3, data: [fx, 0, cx, 0, fy, cy, 0, 0, 1]}
distortion_model: plumb_bob
distortion_coefficients: {rows: 1, cols: 5, data: [k1, k2, p1, p2, k3]}
rectification_matrix: {rows: 3, cols: 3, data: [1, 0, 0, 0, 1, 0, 0, 0, 1]}
projection_matrix: {rows: 3, cols: 4, data: [fx', 0, cx', 0, 0, fy', cy', 0, 0, 0, 1, 0]}
```

The values are placeholders; the calibrator fills them. `camera_info_url` must be a URL:
`file:///home/user/front_camera_info.yaml` (three slashes for an absolute path) or
`package://my_robot_perception/config/front_camera_info.yaml`. A bare path is rejected with
"Invalid camera info URL" or "Camera calibration file ... not found".

## Stereo pairs

```bash
ros2 run camera_calibration cameracalibrator --size 8x6 --square 0.025 --approximate 0.05 \
  --ros-args -r left:=/stereo/left/image_raw -r right:=/stereo/right/image_raw \
  -r left_camera/set_camera_info:=/stereo/left_driver/set_camera_info \
  -r right_camera/set_camera_info:=/stereo/right_driver/set_camera_info
```

`--approximate` (seconds) pairs frames whose stamps differ; hardware-synchronised cameras can
leave it at 0. The result gives each camera its own `r` and a `p` whose `Tx` holds the baseline;
`stereo_image_proc` then computes disparity and points.

## Checking a calibration

```bash
ros2 launch image_proc image_proc.launch.py namespace:=camera     # or your own rectify node
ros2 run camera_calibration cameracheck --size 8x6 --square 0.025 --ros-args \
  -r monocular/image_rect:=/camera/image_rect -r monocular/camera_info:=/camera/camera_info
```

`cameracheck` prints a linearity RMS error (how straight the board's rows stay in the rectified
image) and a reprojection RMS error, both in pixels, for each frame in which it sees the board.
Move the board to the image corners: errors that grow there point to too few edge samples or too
few distortion terms. Two more checks:
- Recalibrate once more and compare fx, fy, cx, cy; large differences mean poor coverage.
- Measure something: an AprilTag of known size at a measured distance
  ([apriltag.md](apriltag.md)) must come out at that distance.
