# Visual-inertial odometry: Kalibr calibration and OpenVINS

Part of [perception-slam](../SKILL.md). Checked against Kalibr `master` (commit 1f60227, March 2024),
OpenVINS `master` (2.7.0, commit 6948812, November 2025) and its calibration guide
(`docs/gs-calibration.dox`), and the rosbags converter docs. Camera intrinsics for ordinary use (the ROS
`camera_calibration` tool) are in [perception-camera](../../perception-camera/SKILL.md); Kalibr is needed here
because VIO needs the camera-IMU extrinsic and time offset.

## Licences and status

| System | Licence | ROS 2 / Jazzy |
|---|---|---|
| Kalibr | BSD with an advertising clause | ROS 1 only (catkin; Docker images up to Noetic). Run it in Docker on ROS 1 bags |
| OpenVINS | **GPL-3.0** | ROS 2 build with colcon; upstream CI Docker images stop at Humble (22.04); no rosdistro release |
| ORB-SLAM3 | **GPL-3.0** | ROS 1 Melodic examples; last upstream commit February 2022; ROS 2 only through community wrappers |
| VINS-Fusion | **GPL-3.0** | ROS 1 Kinetic/Melodic; last upstream commit July 2021 |

GPL-3.0 code linked into your robot software puts that program under GPL terms when you distribute it. Check
this before choosing ORB-SLAM3, VINS-Fusion or OpenVINS for a product; RTAB-Map's built-in odometry and
robot_localization are permissive.

## 1. Collect the right data

Requirements from the OpenVINS calibration guide:

- Camera drivers with correct stamps; short exposure (little motion blur); 20-30 Hz images.
- IMU at 200-500 Hz.
- An AprilGrid target, flat and rigid. Measure the printed tag size; do not trust the PDF's nominal size.
- For the camera-IMU run: 30-60 s of smooth motion that excites every rotation axis and some translation,
  with the target mostly in view.
- For IMU noise: a stationary recording of many hours (the guide suggests upwards of 20).

```bash
ros2 bag record -o calib_cam --topics /camera/color/image_raw
ros2 bag record -o calib_imucam --topics /camera/color/image_raw /imu/data_raw
ros2 bag record -o imu_static --topics /imu/data_raw     # sensor not touched for hours
```

## 2. Convert ROS 2 bags for Kalibr

```bash
python3 -m venv ~/.venvs/rosbags && ~/.venvs/rosbags/bin/pip install rosbags
~/.venvs/rosbags/bin/rosbags-convert --src calib_imucam --dst calib_imucam.bag
```

Older rosbags releases take the source as a positional argument (`rosbags-convert calib_imucam --dst ...`).

## 3. Run Kalibr in Docker

```bash
git clone https://github.com/ethz-asl/kalibr.git && cd kalibr
docker build -t kalibr -f Dockerfile_ros1_20_04 .
xhost +local:root
docker run -it -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:rw -v "$HOME/calib:/data" kalibr
# inside the container
source devel/setup.bash
```

`/data/aprilgrid.yaml` (values are an example; use your target's):

```yaml
target_type: 'aprilgrid'
tagCols: 6
tagRows: 6
tagSize: 0.088      # metres, measured edge of one tag
tagSpacing: 0.3     # gap between tags divided by tagSize
```

`/data/imu.yaml` (rates and noise from step 4):

```yaml
rostopic: /imu/data_raw
update_rate: 200.0
accelerometer_noise_density: 0.0     # from the Allan-variance run
accelerometer_random_walk: 0.0
gyroscope_noise_density: 0.0
gyroscope_random_walk: 0.0
```

Kalibr rejects zero values, which keeps a half-filled file from running.

```bash
# camera intrinsics (pinhole-equi for fisheye lenses)
rosrun kalibr kalibr_calibrate_cameras --bag /data/calib_cam.bag --target /data/aprilgrid.yaml \
  --models pinhole-radtan --topics /camera/color/image_raw --bag-freq 10.0
# camera-IMU extrinsic and time offset
rosrun kalibr kalibr_calibrate_imu_camera --bag /data/calib_imucam.bag --target /data/aprilgrid.yaml \
  --cams /data/calib_cam-camchain.yaml --imu /data/imu.yaml
```

Outputs, named after the bag: `<bag>-camchain.yaml`, then `<bag>-camchain-imucam.yaml` (`T_cam_imu`,
`timeshift_cam_imu`), `<bag>-imu.yaml`, `<bag>-results-imucam.txt` and `<bag>-report-imucam.pdf`. Set
`KALIBR_MANUAL_FOCAL_LENGTH_INIT=1` (the image sets it) when the focal length fails to initialize.

## 4. IMU noise from an Allan variance

OpenVINS recommends `allan_variance_ros` (ori-drs; a ROS 1 catkin package under BSD-3-Clause, though its
`package.xml` says "Proprietary"). Build it in the Kalibr container and run it on the converted static
bag. It gives `accelerometer_noise_density`, `accelerometer_random_walk`,
`gyroscope_noise_density` and `gyroscope_random_walk`. The OpenVINS guide suggests inflating them by about
10-20x for unmodelled errors and testing a few inflations. Datasheet values are a fallback.

## 5. Judge the calibration

From the OpenVINS guide:

- Camera reprojection error below about 0.2-0.5 px.
- In the IMU-camera report, accelerometer and gyroscope errors inside their 3-sigma bounds, and biases that
  stay inside theirs. If not, the noise values are wrong or the motion was too aggressive.
- The IMU dt plot in the report is steady (stamping problems show there).
- Translation and rotation agree with a tape measure and the CAD.

`T_cam_imu` maps points from the IMU frame into the camera frame: it is the pose of the IMU in the camera
optical frame. Put the result into the URDF (a joint from the optical frame to `imu_link`, or its inverse in
the other direction) so TF matches what the VIO uses.

## 6. Run OpenVINS

```bash
cd ~/ros2_ws/src && git clone https://github.com/rpng/open_vins.git
cd ~/ros2_ws && rosdep install --from-paths src --ignore-src -y
colcon build --packages-select ov_core ov_init ov_msckf ov_eval
ros2 launch ov_msckf subscribe.launch.py config_path:=/path/my_vio/estimator_config.yaml \
  max_cameras:=1 use_stereo:=false
```

Not tested upstream on Jazzy: expect build fixes. Make a config folder from one in `config/` (for example
`rs_d455`): `estimator_config.yaml` plus Kalibr's own files, named by `relative_config_imu`
(`kalibr_imu_chain.yaml`) and `relative_config_imucam` (`kalibr_imucam_chain.yaml`). The node subscribes to
the `rostopic` entries in those files. Useful keys in `estimator_config.yaml`: `max_cameras`, `use_stereo`,
`calib_cam_extrinsics`, `calib_cam_intrinsics`, `calib_cam_timeoffset` (online refinement),
`init_window_time`, `init_imu_thresh` (motion needed to initialize), `num_pts`, `use_klt`.

Outputs in the `ov_msckf` namespace: `odomimu` (`nav_msgs/Odometry`), `poseimu`, `pathimu`, point clouds.
Frames are fixed names: `global` → `imu` and `imu` → `cam0`. Turn that TF off with the node parameters
`publish_global_to_imu_tf: false` and `publish_calibration_tf: false`, and fuse `odomimu` into the local
EKF (pose with `_differential: true`, or its twist) so `odom` stays REP 105. OpenVINS needs motion to
initialize: start it, then move the sensor until it does.

## Checks

- Walk a measured straight line: the VIO distance matches (scale is right).
- Return to the start: the end pose is near the start; quantify with evo.
- At rest after initialization: no creep. Creep or explosion points to noise values, extrinsics or stamps.
