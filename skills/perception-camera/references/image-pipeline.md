# Image transport, QoS and depth processing

Part of [perception-camera](../SKILL.md). Checked against `image_transport` 5.1.8,
`image_transport_plugins` 4.0.7 and `image_pipeline` 5.0.13 (`jazzy` branches) and REP 118.
Browser streaming is in [ros2-web-bridge](../../ros2-web-bridge/references/camera-streaming.md).

## Topic names

A camera namespace holds `image_raw` and `camera_info` with identical stamps; processing adds
`image_mono`, `image_color`, `image_rect` and `image_rect_color` beside them. Every node that
needs calibration subscribes through an `image_transport` camera subscriber, which takes
`camera_info` from the same namespace as the image. In Jazzy, remapping `image` to
`/camera/image_raw` therefore also selects `/camera/camera_info`. If a driver publishes the info
elsewhere, remap the fully resolved info name (`/camera/camera_info:=/other/camera_info`).

## Transports

With `ros-jazzy-image-transport-plugins` installed, each `image_transport` publisher adds
sub-topics; `ros2 run image_transport list_transports` lists the plugins.

| Sub-topic | Message | Use for | Parameters (on the publishing node) |
|---|---|---|---|
| `<base>/compressed` | `CompressedImage`, JPEG or PNG | Colour and mono images over Wi-Fi, bags, viewers | `<base>.compressed.format` (`jpeg`), `.jpeg_quality` (1-100, default 95), `.png_level` (0-9, default 3) |
| `<base>/compressedDepth` | `CompressedImage`, PNG or RVL | Depth images (16UC1, 32FC1) | `<base>.compressedDepth.depth_max` (default 10.0 m), `.depth_quantization`, `.png_level` |
| `<base>/zstd` | `CompressedImage` | Lossless general compression | `<base>.zstd.zstd_level` (default 3) |
| `<base>/theora` | `theora_image_transport/Packet` | Video-style streams | |

- `<base>` is the topic's last name: `image_raw.compressed.jpeg_quality` on the driver node.
  `ros2 param list /camera/front_camera_driver | grep compressed` shows the exact names.
- JPEG is lossy: fine for viewing and for most detectors, wrong for depth and doubtful for
  calibration and fiducials. Depth goes through `compressedDepth`: 16UC1 is compressed losslessly
  but pixels beyond `depth_max` become 0; 32FC1 is quantised as inverse depth.
- Subscribers pick a transport: `image_pipeline` nodes and `apriltag_ros` take an
  `image_transport` parameter (`depth_image_transport` for depth inputs), for example
  `-p image_transport:=compressed`. A Python node on Jazzy subscribes to `<base>/compressed` as
  `sensor_msgs/msg/CompressedImage` (no `image_transport` Python API in Jazzy).
- A driver that publishes raw only (or a remote machine that should decode once) uses the
  `republish` component; on Jazzy the transports are parameters:

```bash
ros2 run image_transport republish --ros-args -p in_transport:=compressed -p out_transport:=raw \
  -r in/compressed:=/camera/image_raw/compressed -r out:=/camera/image_raw_decoded
```

  The positional form `republish compressed raw` in older READMEs (usb_cam's among them) is the
  Humble syntax.

## QoS

REP 2003: drivers publish sensor data with the system-default QoS (reliable) and the first
consumer subscribes with sensor-data QoS (best effort), which accepts reliable and best-effort
publishers. `image_pipeline` nodes follow it: they subscribe best effort, copy the input
publisher's reliability when they connect, and publish reliable.

- Override a node's QoS with parameters, fully resolved topic name, at start-up only:

```yaml
/**:
  ros__parameters:
    qos_overrides:
      /camera/image_rect:
        publisher: {reliability: best_effort, history: keep_last, depth: 1}
```

  Only `reliability`, `history` and `depth` can be overridden. RealSense uses its own
  parameters (`color_qos:=SENSOR_DATA`, `depth_qos:=...`).
- Over Wi-Fi, a reliable image publisher with a slow subscriber retransmits and stalls; publish
  best effort, or subscribe best effort to the compressed sub-topic.
- `image_pipeline` nodes subscribe lazily: they connect to their input only while something
  subscribes to their output, so an idle `image_rect` topic costs nothing and shows no data.

## Depth images (REP 118)

| Encoding | Unit | Invalid pixel | Who publishes it |
|---|---|---|---|
| `32FC1` | metres along the optical z axis | NaN (and ±Inf per REP 117) | Canonical form; Gazebo depth cameras |
| `16UC1` | millimetres | 0 | RealSense (`Z16`), OAK, OpenNI-style drivers |

`cv_bridge` passes both through unchanged (`desired_encoding='passthrough'`). Convert 16UC1 to
metres yourself (`depth.astype(np.float32) / 1000.0`, zeros to NaN) or with
`depth_image_proc::ConvertMetricNode` (`image_raw` in, `image` out).

## depth_image_proc components

| Component | Inputs | Output | Note |
|---|---|---|---|
| `PointCloudXyzNode` | `image_rect` (depth), `camera_info` | `points` | `depth_image_transport` parameter |
| `PointCloudXyzrgbNode` | `depth_registered/image_rect`, `rgb/image_rect_color`, `rgb/camera_info` | `points` | Depth must already be in the colour camera's frame and size |
| `RegisterNode` | `depth/image_rect`, `depth/camera_info`, `rgb/camera_info` | `depth_registered/image_rect`, `depth_registered/camera_info` | Needs TF from the depth optical frame to the colour optical frame |
| `PointCloudXyziNode` | `depth/image_rect`, `intensity/image_rect`, `intensity/camera_info` | `points` | IR or grey intensity |
| `PointCloudXyzRadialNode` | `depth/image_raw`, `depth/camera_info` | `points` | Radial (ToF) depth, unrectified: uses K and D, not P. The `Xyzi`/`Xyzrgb` radial variants take `intensity/` or `rgb/` image and info |
| `ConvertMetricNode` | `image_raw` (16UC1) | `image` (32FC1) | |
| `DisparityNode` | `left/image_rect`, `right/camera_info` | `left/disparity` | Only to feed stereo tools |

Coloured cloud from a RealSense whose depth the driver already aligned:

```python
from launch import LaunchDescription
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode


def generate_launch_description():
    cloud = ComposableNode(
        package='depth_image_proc', plugin='depth_image_proc::PointCloudXyzrgbNode',
        name='point_cloud_xyzrgb', namespace='camera/front',
        parameters=[{'queue_size': 10}],
        remappings=[('depth_registered/image_rect', 'aligned_depth_to_color/image_raw'),
                    ('rgb/image_rect_color', 'color/image_raw'),
                    ('rgb/camera_info', 'color/camera_info'),
                    ('points', 'depth_registered/points')])
    return LaunchDescription([ComposableNodeContainer(
        name='depth_container', namespace='camera/front', package='rclcpp_components',
        executable='component_container', composable_node_descriptions=[cloud],
        output='screen')])
```

- The driver's own point cloud (`pointcloud.enable:=true` on RealSense and OAK) is usually
  cheaper; use `depth_image_proc` for cameras without one, for simulated depth cameras, or to
  build clouds from a bag.
- The XYZRGB node pairs depth and colour with an approximate time policy unless `exact_sync` is
  true; raise `queue_size` when the two streams arrive far apart.
- Outputs are ordered clouds in the camera's optical frame. Filtering, downsampling and
  registration of clouds belong to [perception-lidar](../../perception-lidar/SKILL.md).
- Jazzy's executable `point_cloud_xyzrgb_radial_node` loads the XYZI radial plugin by mistake
  (fixed in the Lyrical release); load `depth_image_proc::PointCloudXyzrgbRadialNode` as a
  component instead.

## Recording

```bash
ros2 bag record /camera/image_raw/compressed /camera/camera_info /tf /tf_static
ros2 bag record /camera/front/aligned_depth_to_color/image_raw/compressedDepth \
  /camera/front/color/image_raw/compressed /camera/front/color/camera_info /tf_static
```

Record `camera_info` and TF with the images, or the bag cannot be rectified or projected later.
Decode on playback with `republish` (above) for nodes that want raw images.
