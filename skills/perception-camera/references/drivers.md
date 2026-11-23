# Camera drivers on Jazzy

Part of [perception-camera](../SKILL.md). Versions are the Jazzy binary releases in
`ros/rosdistro` on 2026-11-19; parameter names were read from each package's source.

## Which driver

| Camera | Package (Jazzy release) | Start it with | Notes |
|---|---|---|---|
| USB / UVC webcam | `usb_cam` 0.8.1 | `ros2 run usb_cam usb_cam_node_exe` | Decodes MJPEG (`pixel_format: mjpeg2rgb`), so high resolutions fit through USB 2 |
| USB / UVC webcam | `v4l2_camera` 0.7.3 | `ros2 run v4l2_camera v4l2_camera_node` | YUYV, UYVY, GREY; every V4L2 control becomes a parameter; QoS overrides |
| libcamera, Raspberry Pi camera modules | `camera_ros` 0.8.1 | `ros2 run camera_ros camera_node` | The bloomed `libcamera` lacks some Pi modules; full support needs the raspberrypi fork built from source |
| Intel RealSense D400 | `realsense2_camera` 4.59.2, `librealsense2` 2.59.2 | `ros2 launch realsense2_camera rs_launch.py` | Factory calibrated; publishes its own TF |
| Luxonis OAK (RVC2: OAK-D, OAK-D Pro, ...) | `depthai_ros_driver` 2.13.0 (DepthAI v2) | `ros2 launch depthai_ros_driver camera.launch.py` | OAK4 (RVC4) needs DepthAI v3: build the `v3_jazzy` branch from source |
| Stereolabs ZED | not in rosdistro | `zed-ros2-wrapper` from source | Needs the proprietary ZED SDK and an NVIDIA GPU with CUDA |
| GStreamer source (IP / RTSP camera) | `gscam` 2.0.2 | `ros2 run gscam gscam_node` | Takes a GStreamer pipeline string |

Install the processing side with the driver: `ros-jazzy-image-pipeline`,
`ros-jazzy-image-transport-plugins`, `ros-jazzy-rqt-image-view`.

## USB cameras

```bash
sudo apt install v4l-utils
v4l2-ctl --list-devices                         # one camera often owns several /dev/videoN
v4l2-ctl -d /dev/video0 --list-formats-ext      # pixel formats, sizes and rates it offers
ls -l /dev/v4l/by-id/                           # stable names that survive replugging
groups | grep video                             # the user needs the video group
```

Only one node of a camera delivers frames; the others carry metadata. Many UVC cameras reach full
rate at high resolution only in MJPEG (usb_cam's README lists a camera with YUYV 1280x720 at
10 Hz and MJPEG at 30 Hz). `usb_cam` prints the device's modes at start-up.

`my_robot_perception/config/front_camera.yaml` for `usb_cam`:

```yaml
/**:
  ros__parameters:
    video_device: /dev/v4l/by-id/usb-<maker>_<model>-video-index0   # symlinks are resolved
    pixel_format: mjpeg2rgb        # MJPEG from the camera, rgb8 on image_raw
    image_width: 1280
    image_height: 720              # a mode the camera lists
    framerate: 30.0
    camera_name: front_camera      # must equal camera_name inside the calibration file
    camera_info_url: package://my_robot_perception/config/front_camera_info.yaml
    frame_id: camera_optical_frame # default is "default_cam"; always set it
```

- `usb_cam` publishes `image_raw` and `camera_info` through `image_transport` (reliable, depth 100)
  and offers `~/set_camera_info` (for example `/camera/front_camera_driver/set_camera_info`).
- `ros2 run usb_cam usb_cam_node_exe --ros-args -p pixel_format:=test` prints the formats the
  driver supports.
- `v4l2_camera` uses `image_size: [1280, 720]`, `pixel_format: YUYV`, `output_encoding: rgb8`,
  `camera_frame_id`, `camera_info_url`, and a parameter per camera control (`brightness`,
  `white_balance_automatic`, ...). QoS: `-p qos_overrides./camera/image_raw.publisher.reliability:=best_effort`
  (start-up only).
- `camera_ros` takes `width`, `height`, `format`, `role`, `frame_id`, `camera_info_url`. rosdep
  installs the bloomed `libcamera`; with a system or self-built libcamera, pass
  `--skip-keys=libcamera`. Small sizes on Pi modules may pick a cropped sensor mode; set
  `sensor_mode` to keep the full field of view.

## Launch: driver plus a composed image_proc chain

`my_robot_perception/launch/front_camera.launch.py`:

```python
from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import ComposableNodeContainer, Node
from launch_ros.descriptions import ComposableNode
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    params = PathJoinSubstitution(
        [FindPackageShare('my_robot_perception'), 'config', 'front_camera.yaml'])

    driver = Node(
        package='usb_cam', executable='usb_cam_node_exe', name='front_camera_driver',
        namespace='camera', parameters=[params], output='screen')

    # Rectify, then a half-size copy for a model; one process, no serialisation between them.
    image_chain = ComposableNodeContainer(
        name='image_proc_container', namespace='camera',
        package='rclcpp_components', executable='component_container',
        composable_node_descriptions=[
            ComposableNode(
                package='image_proc', plugin='image_proc::RectifyNode', name='rectify',
                namespace='camera',
                remappings=[('image', 'image_raw'), ('image_rect', 'image_rect')]),
            ComposableNode(
                package='image_proc', plugin='image_proc::ResizeNode', name='resize',
                namespace='camera',
                parameters=[{'scale_width': 0.5, 'scale_height': 0.5}],
                # camera_info topics follow the image topics (Jazzy image_pipeline)
                remappings=[('image/image_raw', 'image_rect'),
                            ('resize/image_raw', 'small/image_rect')]),
        ],
        output='screen')

    return LaunchDescription([driver, image_chain])
```

- Each `image_proc` node subscribes only while its output has a subscriber, and copies the
  publisher's reliability when it does. Test with `ros2 topic hz /camera/image_rect`.
- `ResizeNode` scales `camera_info` with the image; feed the model the `small/` pair together. Its
  output base is `resize/image_raw` in the Jazzy source (the package docs say `resized/`).
- The drivers are components too (`usb_cam::UsbCamNode`, `v4l2_camera::V4L2Camera`,
  `realsense2_camera::RealSenseNodeFactory`, `depthai_ros_driver::Camera`); load the driver into
  the same container with `extra_arguments=[{'use_intra_process_comms': True}]` when copying full
  frames between processes costs too much CPU.
- A grey camera with a Bayer sensor needs `image_proc::DebayerNode` first (`image_raw` to
  `image_mono` and `image_color`); `ros2 launch image_proc image_proc.launch.py namespace:=camera`
  runs debayer plus two rectify nodes (`image_rect`, `image_rect_color`).

## Intel RealSense

```bash
sudo apt install ros-jazzy-realsense2-camera ros-jazzy-realsense2-description
ros2 launch realsense2_camera rs_launch.py camera_namespace:=camera camera_name:=front \
  rgb_camera.color_profile:=640x480x30 depth_module.depth_profile:=640x480x30 \
  align_depth.enable:=true enable_sync:=true pointcloud.enable:=true
ros2 param describe /camera/front rgb_camera.color_profile   # supported profiles
```

| Topic (namespace `camera`, name `front`) | Content |
|---|---|
| `/camera/front/color/image_raw`, `.../color/camera_info` | RGB8 colour image |
| `/camera/front/depth/image_rect_raw` | 16UC1 depth in mm, depth optical frame |
| `/camera/front/aligned_depth_to_color/image_raw` | Depth resampled to the colour camera (with `align_depth.enable`) |
| `/camera/front/depth/color/points` | Point cloud (with `pointcloud.enable`), in the depth optical frame |

- Defaults are `camera_namespace:=camera camera_name:=camera`, hence `/camera/camera/...` topics.
- Frames are named from `camera_name`: `front_link`, `front_color_optical_frame`,
  `front_depth_optical_frame`. `publish_tf` (default true) publishes them from the factory extrinsics.
- Attach to the robot with the description macro and let the driver publish the rest:
  `<xacro:include filename="$(find realsense2_description)/urdf/_d435.urdf.xacro"/>` and
  `<xacro:sensor_d435 parent="base_link" name="front"><origin xyz="0.2 0 0.3" rpy="0 0 0"/></xacro:sensor_d435>`.
  With `use_nominal_extrinsics:=true` the macro adds the optical frames itself; then launch the
  driver with `publish_tf:=false`, or the frames get two parents.
- Old parameter names (`depth_width`, `align_depth`, `filters`, `<stream>_frame_id`) are gone;
  profiles are `<module>.<stream>_profile`. Several cameras: one launch each with its own
  `camera_name` and `serial_no:=_<serial>` (the leading `_` keeps it a string).
- Depth filters are parameters: `decimation_filter.enable`, `spatial_filter.enable`,
  `temporal_filter.enable`, `hole_filling_filter.enable`.
- Images are published with SYSTEM_DEFAULT QoS (reliable); `color_qos:=SENSOR_DATA` changes it.
- No device found or permission denied: the udev rules are missing. The vendor's
  `librealsense2-udev-rules` package or `scripts/setup_udev_rules.sh` in the librealsense repo
  installs them. Use a USB 3 port and cable; `rs-enumerate-devices` (vendor tools) lists modes.

## Luxonis OAK (depthai-ros 2.x on Jazzy)

```bash
sudo apt install ros-jazzy-depthai-ros
ros2 launch depthai_ros_driver camera.launch.py camera_model:=OAK-D-PRO \
  parent_frame:=base_link cam_pos_x:=0.2 cam_pos_z:=0.3 pointcloud.enable:=true
```

- Topics under `/oak`: `rgb/image_raw`, `rgb/camera_info`, `rgb/image_rect` (the launch adds an
  `image_proc` rectify node, `rectify_rgb:=true`), `stereo/image_raw` (16UC1 depth, aligned to the
  colour camera by default: `stereo.i_align_depth`), `points` with `pointcloud.enable:=true`.
- The launch runs a `robot_state_publisher` with the OAK model; `parent_frame` and `cam_pos_*`/
  `cam_roll`/`cam_pitch`/`cam_yaw` hang it on your robot. Do not also put it in your URDF.
- Settings live in a parameter file (`params_file:=`), grouped as `camera.*`, `rgb.*`,
  `stereo.*`, `nn.*` with `i_` prefixes (for example `camera.i_pipeline_type: RGBD`).
- On-device networks (`nn.*`, `camera.i_nn_type`) run models on the camera; check the model's
  licence as for any other.
- Device not found: add the udev rule `SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"`
  (Luxonis' USB vendor id) to `/etc/udev/rules.d/`, then `sudo udevadm control --reload-rules`
  and replug.

## Checks

```bash
ros2 topic list | grep -E 'image_raw|camera_info'
ros2 topic hz /camera/image_raw                         # the rate you configured
ros2 topic echo --once --no-arr /camera/camera_info     # width/height match the image, frame_id is optical
ros2 topic echo --once /camera/camera_info --field k    # k[0] (fx) stays 0.0 until calibrated
ros2 run tf2_ros tf2_echo base_link camera_optical_frame
ros2 run rqt_image_view rqt_image_view /camera/image_raw
```
