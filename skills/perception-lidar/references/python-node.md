# A point-cloud node in Python

Part of [perception-lidar](../SKILL.md): an rclpy node that removes the ground from a 3D cloud,
groups the rest into obstacles and publishes them as a cloud and as boxes. It uses only NumPy and
SciPy, which Ubuntu 24.04 ships, so `rosdep` installs everything. Checked against `sensor_msgs_py`
in common_interfaces 5.3.8 (`jazzy`); the three helper functions were run on synthetic data with
NumPy 1.26 and SciPy 1.13, the node itself was not run. Package and node layout follow
[ros2-core python-nodes.md](../../ros2-core/references/python-nodes.md).

The node expects a cloud in a frame whose z axis points up and whose z = `ground_z` is the floor,
such as `base_footprint`: feed it the CropBox output from [filters.md](filters.md), which transforms
the cloud there. On a level lidar's own frame, set `ground_z` to minus the mount height.

## `my_robot_perception/obstacle_extractor.py`

```python
"""Remove the ground from a lidar cloud and group the rest into obstacles."""
import numpy as np
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree
from sensor_msgs.msg import PointCloud2, PointField
from sensor_msgs_py import point_cloud2
from visualization_msgs.msg import Marker, MarkerArray

# Output layout: x, y, z and the cluster id in 'intensity', so RViz can colour by cluster.
FIELDS = [PointField(name=name, offset=4 * i, datatype=PointField.FLOAT32, count=1)
          for i, name in enumerate(('x', 'y', 'z', 'intensity'))]


def voxel_downsample(xyz, size):
    """Keep one point per voxel of edge `size` (0 disables)."""
    if size <= 0.0:
        return xyz
    keys = np.floor(xyz / size).astype(np.int64)
    _, first = np.unique(keys, axis=0, return_index=True)
    return xyz[first]


def fit_ground(xyz, tolerance, max_tilt, iterations, rng):
    """RANSAC plane whose normal is within max_tilt of +z, as (normal, offset); None if none."""
    if len(xyz) < 3:
        return None
    best, best_count = None, 0
    cos_tilt = np.cos(max_tilt)
    for _ in range(iterations):
        p0, p1, p2 = xyz[rng.choice(len(xyz), 3, replace=False)]
        normal = np.cross(p1 - p0, p2 - p0)
        length = np.linalg.norm(normal)
        if length < 1e-9:
            continue
        normal /= length
        if abs(normal[2]) < cos_tilt:
            continue  # too steep for ground: a wall or the side of a box
        offset = -normal @ p0
        count = np.count_nonzero(np.abs(xyz @ normal + offset) < tolerance)
        if count > best_count:
            best, best_count = (normal, offset), count
    return best


def euclidean_clusters(xyz, tolerance):
    """Label points so that any two closer than `tolerance` share a label."""
    pairs = cKDTree(xyz).query_pairs(r=tolerance, output_type='ndarray')
    n = len(xyz)
    graph = coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(n, n))
    return connected_components(graph, directed=False)[1]


class ObstacleExtractor(Node):

    def __init__(self):
        super().__init__('obstacle_extractor')
        self._voxel = self.declare_parameter('voxel_size', 0.05).value
        self._ground_z = self.declare_parameter('ground_z', 0.0).value
        self._ground_band = self.declare_parameter('ground_band', 0.3).value
        self._ground_tol = self.declare_parameter('ground_tolerance', 0.05).value
        self._max_tilt = np.radians(self.declare_parameter('max_ground_tilt_deg', 10.0).value)
        self._max_z = self.declare_parameter('max_obstacle_z', 2.0).value
        self._cluster_tol = self.declare_parameter('cluster_tolerance', 0.3).value
        self._min_points = self.declare_parameter('min_cluster_points', 10).value
        self._rng = np.random.default_rng(0)
        self.create_subscription(PointCloud2, 'points', self._on_cloud, qos_profile_sensor_data)
        self._cloud_pub = self.create_publisher(PointCloud2, 'obstacles', qos_profile_sensor_data)
        self._box_pub = self.create_publisher(MarkerArray, 'obstacle_boxes', 10)

    def _on_cloud(self, msg):
        xyz = point_cloud2.read_points_numpy(msg, field_names=('x', 'y', 'z'), skip_nans=True)
        xyz = xyz[np.isfinite(xyz).all(axis=1)].astype(np.float64)  # some drivers lie in is_dense
        xyz = voxel_downsample(xyz, self._voxel)
        # Fit the plane only to points near the expected floor, so a wall can never win.
        near_floor = xyz[np.abs(xyz[:, 2] - self._ground_z) < self._ground_band]
        plane = fit_ground(near_floor, self._ground_tol, self._max_tilt, 100, self._rng)
        if plane is None:
            height = xyz[:, 2] - self._ground_z
        else:
            normal, offset = plane
            height = (xyz @ normal + offset) * np.sign(normal[2])
        obstacles = xyz[(height > self._ground_tol) & (xyz[:, 2] < self._max_z)]
        labels = np.zeros(0, dtype=np.int64)
        if len(obstacles):
            labels = euclidean_clusters(obstacles, self._cluster_tol)
            large = np.bincount(labels)[labels] >= self._min_points
            obstacles, labels = obstacles[large], labels[large]
        self._publish(msg.header, obstacles, labels)

    def _publish(self, header, xyz, labels):
        cloud = np.column_stack([xyz, labels]).astype(np.float32)
        self._cloud_pub.publish(point_cloud2.create_cloud(header, FIELDS, cloud))
        markers = MarkerArray(markers=[Marker(header=header, action=Marker.DELETEALL)])
        for i, label in enumerate(np.unique(labels)):
            points = xyz[labels == label]
            low, high = points.min(axis=0), points.max(axis=0)
            box = Marker(header=header, ns='obstacles', id=i, type=Marker.CUBE,
                         action=Marker.ADD)
            box.pose.position.x, box.pose.position.y, box.pose.position.z = \
                ((low + high) / 2.0).tolist()
            box.pose.orientation.w = 1.0
            box.scale.x, box.scale.y, box.scale.z = np.maximum(high - low, 0.05).tolist()
            box.color.r, box.color.a = 1.0, 0.5
            markers.markers.append(box)
        self._box_pub.publish(markers)


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleExtractor()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
```

## Package files

`package.xml` (inside `<package>`):

```xml
<exec_depend>rclpy</exec_depend>
<exec_depend>sensor_msgs</exec_depend>
<exec_depend>sensor_msgs_py</exec_depend>
<exec_depend>visualization_msgs</exec_depend>
<exec_depend>python3-numpy</exec_depend>
<exec_depend>python3-scipy</exec_depend>
```

`setup.py`: `'obstacle_extractor = my_robot_perception.obstacle_extractor:main'` under
`entry_points['console_scripts']`. Run it on the filtered cloud:

```bash
ros2 run my_robot_perception obstacle_extractor --ros-args -r points:=/lidar/points_filtered \
  -p cluster_tolerance:=0.3 -p max_obstacle_z:=1.8
```

## Notes

- **Read and write clouds with NumPy.** `read_points_numpy` returns an N×k float array (all requested
  fields must share one type: ask for `x y z` only when the cloud also has `uint16` rings).
  `read_points` returns a structured array for mixed types. `create_cloud(header, fields, array)`
  and `create_cloud_xyz32(header, xyz)` build the message from NumPy without a Python loop; a
  `struct.pack` loop per point is far too slow for a 3D lidar.
- `skip_nans=True` only acts when the message says `is_dense: false`; the extra `isfinite` mask
  covers drivers that set it wrongly.
- `query_pairs` memory grows with the number of neighbour pairs. Voxel first, and keep
  `cluster_tolerance` a few voxels wide. If `ros2 topic hz /obstacles` falls below the lidar's
  rate, the callback is too slow: voxel coarser, crop harder, or use the C++ node in
  [cpp-node.md](cpp-node.md).
- The ground fit is a per-frame RANSAC on a horizontal plane. On ramps, kerbs or rough outdoor
  ground, one plane is not enough: Patchwork++ (BSD-2-Clause, `pip install pypatchworkpp`, and a
  ROS 2 wrapper documented for Humble, built from source) fits ground patch by patch.
- **To transform in Python** instead of upstream: `from tf2_sensor_msgs import do_transform_cloud`
  (whole message) or `transform_points` (an N×3 array), with a transform looked up at
  `msg.header.stamp` as in
  [ros2-robot-description frames.md](../../ros2-robot-description/references/frames.md).

## Open3D instead of NumPy

Open3D (MIT) has the same steps built in: `voxel_down_sample(voxel_size)`,
`remove_statistical_outlier(nb_neighbors, std_ratio)`, `remove_radius_outlier(nb_points, radius)`,
`segment_plane(distance_threshold, ransac_n, num_iterations)`, which returns `[a, b, c, d]` and
the inlier indices, `cluster_dbscan(eps, min_points)` (label -1 is noise), and
`get_axis_aligned_bounding_box()` or `get_oriented_bounding_box()`. It is best for offline work on
PCD files and for registration (see [calibration.md](calibration.md)). Inside a ROS node on Jazzy:

- Ubuntu 24.04 has no `python3-open3d` package (its rosdep key is null on noble; the key
  `python3-open3d-pip` installs from PyPI). Wheels for Python 3.12 start at 0.19.0 (on Linux,
  x86_64 only); 0.20.0 adds Linux aarch64.
- Install it into a virtual environment that sees the ROS packages, following the Jazzy how-to
  "Using Python Packages with ROS 2":

  ```bash
  python3 -m venv --system-site-packages ~/venvs/lidar
  ~/venvs/lidar/bin/pip install open3d
  export PYTHONPATH=$HOME/venvs/lidar/lib/python3.12/site-packages:$PYTHONPATH   # in the node's shell
  ```

- Keep NumPy at Ubuntu's 1.26 in that environment: ROS 2 Jazzy's compiled message modules are
  built against it, and a pip upgrade to NumPy 2 breaks their import. `pip install open3d` leaves
  the system NumPy in place because it satisfies Open3D's `numpy>=1.18`.
- `segment_plane` has no orientation constraint, so check the normal yourself before calling the
  plane ground: the largest plane in a corridor can be a wall.
