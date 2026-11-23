# A detection node on the image stream

Part of [perception-camera](../SKILL.md). Uses `cv_bridge` and `image_geometry` 4.1.0 and
`vision_msgs` 4.1.1 (Jazzy). The model sits behind one small adapter so it can be swapped; the
adapter shown uses Ultralytics, whose licence is the first thing to check.

## Pick a model, check its licence

| Model | Code and weights licence | Wiki |
|---|---|---|
| Ultralytics `ultralytics` package and its YOLO models | AGPL-3.0, or a paid Ultralytics Enterprise licence | [YOLO](../../../wiki/learning/models/yolo.md) |
| YOLOX (Megvii) | Apache-2.0 | [YOLO](../../../wiki/learning/models/yolo.md) |
| Segment Anything (SAM) and SAM 2 | Apache-2.0 | [Segment Anything](../../../wiki/learning/models/segment-anything.md) |
| SAM 3 | Meta's own SAM License | [Segment Anything](../../../wiki/learning/models/segment-anything.md) |
| Grounding DINO (open-vocabulary boxes from text) | Apache-2.0 | [Grounding DINO](../../../wiki/learning/models/grounding-dino.md) |
| FoundationPose (6D object pose) | NVIDIA Source Code License: research or evaluation only | [FoundationPose](../../../wiki/learning/models/foundationpose.md) |

- AGPL-3.0 reaches the code you combine with it: shipping the robot software, or offering it to
  users over a network, means offering its source under the same licence, unless you hold the
  commercial licence. Decide before the model is wired into a product.
- Weights can carry terms apart from the code (check the model card), and so can the dataset they
  were trained on.
- TensorRT, ONNX export and running on a Jetson are the later skill `learn-edge-deployment`;
  GPUs in containers are in [ops-docker-ci](../../ops-docker-ci/references/gpu-display.md).

## Python environment

Ubuntu 24.04 refuses `pip install` into the system Python (PEP 668, "externally-managed-
environment"), and `cv_bridge` is built against the apt NumPy 1.26. Keep ROS packages from apt
and put the model framework in a virtual environment that can still see them:

```bash
cd ~/ros2_ws
python3 -m venv --system-site-packages venv
touch venv/COLCON_IGNORE                     # colcon must not treat it as a package
source venv/bin/activate
pip install "numpy<2" ultralytics            # AGPL-3.0; pin the version you tested
python -c "import numpy, cv2, cv_bridge; print(numpy.__version__, cv2.__version__)"
source /opt/ros/jazzy/setup.bash && colcon build --packages-select my_robot_perception
head -1 install/my_robot_perception/lib/my_robot_perception/detector_node   # which python runs it
```

If that first line is `/usr/bin/python3`, the venv packages are not used; run
`python -m my_robot_perception.detector_node` with the venv active and the workspace sourced.
A NumPy 2 in the path makes `cv_bridge` fail on import with a NumPy 1.x/2.x message.

## 2D detections: `my_robot_perception/detector_node.py`

```python
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from rclpy.qos import HistoryPolicy, QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2D, Detection2DArray, ObjectHypothesisWithPose

# Best effort, depth 1: a slow model always gets the newest frame, never a backlog.
LATEST_FRAME = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT, history=HistoryPolicy.KEEP_LAST, depth=1)


class UltralyticsDetector:
    """Adapter: BGR image in, (label, score, cx, cy, w, h) in pixels out. AGPL-3.0."""

    def __init__(self, weights: str, min_score: float):
        from ultralytics import YOLO
        self._model = YOLO(weights)
        self._min_score = min_score

    def __call__(self, bgr):
        result = self._model(bgr, conf=self._min_score, verbose=False)[0]
        boxes = result.boxes
        return [(result.names[int(c)], float(s), *map(float, xywh))
                for xywh, s, c in zip(boxes.xywh.tolist(), boxes.conf.tolist(), boxes.cls.tolist())]


def to_detection(header, label, score, cx, cy, w, h) -> Detection2D:
    det = Detection2D(header=header)
    det.bbox.center.position.x = cx
    det.bbox.center.position.y = cy
    det.bbox.size_x = w
    det.bbox.size_y = h
    hyp = ObjectHypothesisWithPose()
    hyp.hypothesis.class_id = label
    hyp.hypothesis.score = score
    det.results.append(hyp)
    return det


class DetectorNode(Node):
    def __init__(self, name='detector', subscribe_2d=True):
        super().__init__(name)
        weights = self.declare_parameter('weights', '').value
        min_score = self.declare_parameter('min_score', 0.5).value
        self._detect = UltralyticsDetector(weights, min_score)
        self._bridge = CvBridge()
        if subscribe_2d:
            self._pub = self.create_publisher(Detection2DArray, 'detections', 10)
            self.create_subscription(Image, 'image', self._on_image, LATEST_FRAME)

    def _on_image(self, msg: Image):
        bgr = self._bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        # The input header goes on every output: same stamp, same optical frame.
        out = Detection2DArray(header=msg.header)
        out.detections = [to_detection(msg.header, *d) for d in self._detect(bgr)]
        self._pub.publish(out)


def main():
    rclpy.init()
    node = DetectorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
```

Run it on the rectified (or resized) stream:
`ros2 run my_robot_perception detector_node --ros-args -r image:=/camera/image_rect -p weights:=/path/to/model.pt`.
`package.xml` needs `rclpy`, `sensor_msgs`, `vision_msgs`, `cv_bridge` and, for the 3D node,
`image_geometry` and `message_filters`.

- `imgmsg_to_cv2(..., 'bgr8')` converts `rgb8`, `bgra8`, `mono8` and Bayer inputs; models trained
  on RGB need `cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)` unless their API expects BGR (Ultralytics
  takes BGR NumPy arrays).
- For `sensor_msgs/CompressedImage` input (`image/compressed`), use
  `compressed_imgmsg_to_cv2(msg, 'bgr8')`.
- Boxes are in the pixels of the image you fed the model. Detections from a resized stream need
  that stream's `camera_info` (the `small/` pair from `ResizeNode`), not the full-size one.
- Segmentation masks have no standard `vision_msgs` field; publish them as a `mono8` or `16UC1`
  label `Image` with the input header.

## 3D positions from aligned depth

Synchronise the colour image, the depth image registered to it (RealSense
`aligned_depth_to_color/image_raw`, OAK `stereo/image_raw`) and the colour `camera_info`; keep only
the newest set and run the model from a timer, so a slow model never works through a queue.

```python
import numpy as np
from image_geometry import PinholeCameraModel
from message_filters import ApproximateTimeSynchronizer, Subscriber
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import CameraInfo, Image
from vision_msgs.msg import Detection3D, Detection3DArray


def pixel_to_point(cam: PinholeCameraModel, depth_m: np.ndarray, u: float, v: float, half=3):
    """Point in the optical frame for raw pixel (u, v), from the median of valid depths around it."""
    h, w = depth_m.shape
    patch = depth_m[max(int(v) - half, 0):min(int(v) + half + 1, h),
                    max(int(u) - half, 0):min(int(u) + half + 1, w)]
    valid = patch[np.isfinite(patch) & (patch > 0.0)]
    if valid.size == 0:
        return None
    z = float(np.median(valid))
    ray = cam.project_pixel_to_3d_ray(cam.rectify_point((u, v)))   # a unit vector, not z = 1
    scale = z / ray[2]
    return ray[0] * scale, ray[1] * scale, z


class Detector3dNode(DetectorNode):            # reuses the adapter and bridge above
    def __init__(self):
        super().__init__('detector_3d', subscribe_2d=False)
        self._latest = None
        self._cam = PinholeCameraModel()
        self._pub3d = self.create_publisher(Detection3DArray, 'detections_3d', 10)
        subs = [Subscriber(self, Image, 'image', qos_profile=qos_profile_sensor_data),
                Subscriber(self, Image, 'depth', qos_profile=qos_profile_sensor_data),
                Subscriber(self, CameraInfo, 'camera_info', qos_profile=qos_profile_sensor_data)]
        self._sync = ApproximateTimeSynchronizer(subs, queue_size=5, slop=0.05)
        self._sync.registerCallback(lambda *msgs: setattr(self, '_latest', msgs))
        self.create_timer(0.1, self._process)

    def _process(self):
        if self._latest is None:
            return
        image, depth, info = self._latest
        self._latest = None
        self._cam.from_camera_info(info)
        depth_m = self._bridge.imgmsg_to_cv2(depth, desired_encoding='passthrough')
        if depth_m.dtype == np.uint16:             # 16UC1 is millimetres, 0 = no data
            depth_m = depth_m.astype(np.float32) / 1000.0
        out = Detection3DArray(header=image.header)
        for label, score, cx, cy, w, h in self._detect(
                self._bridge.imgmsg_to_cv2(image, desired_encoding='bgr8')):
            point = pixel_to_point(self._cam, depth_m, cx, cy)
            if point is None:
                continue
            det = Detection3D(header=image.header)
            det.bbox.center.position.x, det.bbox.center.position.y, det.bbox.center.position.z = point
            det.results.append(to_detection(image.header, label, score, cx, cy, w, h).results[0])
            out.detections.append(det)
        self._pub3d.publish(out)
```

Give it its own `main()` like the 2D node and remap `image`, `depth` and `camera_info` to the
colour, aligned-depth and colour-info topics.

- `rectify_point` undoes the colour camera's distortion; for detections made on `image_rect`
  with a depth image rectified to match, call `project_pixel_to_3d_ray((u, v))` directly.
- The box centre may fall on background; for thin or hollow objects sample a mask or the box's
  inner region and take a low percentile instead of the median.
- Points are in the colour optical frame at the image's stamp. Consumers transform them with tf2
  at that stamp ([frames.md](../../ros2-robot-description/references/frames.md)).
- `bbox.size` stays zero here: the depth of a 2D box says nothing about the object's extent.

## Checks

```bash
ros2 topic hz /detections                    # the model's real rate
ros2 topic delay /detections                 # age of the stamp on arrival: capture-to-result latency
ros2 topic echo --once /detections_3d --field detections
```

- A known object at a measured distance comes out at that distance in `detections_3d`.
- Latency stays flat over minutes; growth means frames are queuing somewhere.
- The node's licence and the model's licence are written down in the package before release.
