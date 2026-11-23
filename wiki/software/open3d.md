---
type: tool
name: Open3D
summary: MIT-licensed C++ and Python library for 3D data (point clouds, meshes, RGB-D), with ICP and global registration, TSDF reconstruction, GPU tensor paths and a modern viewer; pip wheels cover Python 3.10-3.14, but no ROS 2 glue is released for Jazzy.
tags: [open3d, point-cloud, mesh, rgbd, icp, registration, fpfh, ransac, tsdf, reconstruction, visualization, python, cuda, pointcloud2]
kind: library
area: perception
support:
license: MIT
links: {repo: "https://github.com/isl-org/Open3D", docs: "https://www.open3d.org/docs/latest/", site: "https://www.open3d.org"}
version: {tested: , latest: 0.20.0, as_of: 2026-11-23}
platforms: [linux, windows, macos]
agent_access: script
registry:
evidence: researched
last_verified: 2026-11-23
sources:
  - {url: "https://github.com/isl-org/Open3D", title: "Open3D repository: LICENSE, CHANGELOG, examples and docs sources (v0.19.0 and v0.20.0 tags, main)", accessed: 2026-11-23}
  - {url: "https://www.open3d.org/docs/latest/getting_started.html", title: "Open3D docs: Getting started", accessed: 2026-11-23}
  - {url: "https://pypi.org/project/open3d/", title: "open3d on PyPI (release history and wheel files)", accessed: 2026-11-23}
  - {url: "https://www.open3d.org/docs/latest/arm.html", title: "Open3D docs: ARM support", accessed: 2026-11-23}
  - {url: "https://www.open3d.org/docs/latest/tutorial/visualization/cpu_rendering.html", title: "Open3D docs: CPU (software) rendering", accessed: 2026-11-23}
  - {url: "https://www.open3d.org/docs/latest/tutorial/visualization/headless_rendering.html", title: "Open3D docs: Headless rendering (legacy OpenGL)", accessed: 2026-11-23}
  - {url: "https://www.open3d.org/docs/latest/sycl.html", title: "Open3D docs: SYCL backend (legacy versus tensor types)", accessed: 2026-11-23}
  - {url: "https://www.open3d.org/docs/latest/tutorial/t_pipelines/t_icp_registration.html", title: "Open3D docs: ICP registration (tensor)", accessed: 2026-11-23}
  - {url: "https://github.com/isl-org/Open3D/issues", title: "Open3D issue tracker", accessed: 2026-11-23}
  - {url: "https://github.com/ros-perception/perception_open3d", title: "perception_open3d repository: README, open3d_conversions package (ros2 branch)", accessed: 2026-11-23}
  - {url: "https://github.com/ros/rosdistro", title: "rosdistro: distribution files and rosdep base.yaml and python.yaml", accessed: 2026-11-23}
  - {url: "https://packages.ubuntu.com/search?keywords=open3d&searchon=names&suite=all&section=all", title: "Ubuntu packages: open3d", accessed: 2026-11-23}
  - {url: "https://docs.ros.org/en/jazzy/How-To-Guides/Using-Python-Packages.html", title: "ROS 2 docs (Jazzy): Using Python packages with ROS 2", accessed: 2026-11-23}
  - {url: "https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs_py/sensor_msgs_py/point_cloud2.py", title: "sensor_msgs_py point_cloud2.py, jazzy branch", accessed: 2026-11-23}
---

# Open3D

Open3D is an MIT-licensed library for 3D data, with a C++ core and a full Python API: point
clouds, triangle meshes and RGB-D images, ICP and feature-based registration, TSDF
reconstruction, ray casting and a Filament-based viewer [1]. Builders use it from Python to clean
and align scans, fuse depth frames into meshes, check a map against a scan, and prototype
point-cloud steps before (or instead of) writing them with [PCL](pcl.md) in C++.

## When to use it

- **Python work on point clouds:** scripts and notebooks over files exported from bags, dataset
  tools, quick ICP checks between a map and a scan.
- **Reconstruction from RGB-D:** TSDF integration, a dense RGB-D SLAM example, Poisson and
  ball-pivoting meshing [1].
- **GPU on a desktop NVIDIA card:** the standard x86_64 Linux wheel includes CUDA [2], used by the
  tensor API (`open3d.t`) [7][8].
- **Use [PCL](pcl.md) instead** for C++ nodes on Jazzy: `pcl_conversions` and `pcl_ros` ship as
  binaries; Open3D's ROS glue does not (see Traps). Use [OctoMap](octomap.md) for occupancy maps
  and [CloudCompare](../tools/cloudcompare.md) when a person wants to click through a cloud.

| | Open3D | PCL |
|---|---|---|
| Licence | MIT [1] | BSD-3-Clause |
| Language | Python and C++ | C++; no maintained Python binding |
| Jazzy apt | none; pip wheel | `libpcl-dev` 1.14.0, `ros-jazzy-pcl-ros` |
| GPU | CUDA in the x86_64 Linux wheel; SYCL | optional CUDA modules, source build |
| Newest release | 0.20.0, 16 Sep 2026 [3] | 1.15.1, 26 Aug 2025 |

## Setup

Open3D 0.20.0 has wheels for CPython 3.10 to 3.14 on Linux x86_64 and aarch64 (glibc 2.35+, so
Ubuntu 22.04 or newer), Windows x86_64 and macOS 11+ on Apple silicon; there is no Intel macOS
wheel for 0.20 [3]. Earlier releases: 0.19.0 (January 2025), 0.18.0 (January 2024) [3].

Ubuntu 24.04 has no `open3d` apt packages; 26.04 ships 0.19.0 [12]. With Jazzy, use the system
Python 3.12 in a virtual environment, as the ROS docs advise for pip packages [13]:

```bash
sudo apt install python3-venv
cd ~/ros_ws && python3 -m venv venv && touch venv/COLCON_IGNORE
source venv/bin/activate && pip install -U "pip>=20.3"
pip install open3d          # x86_64 Linux: with CUDA; `open3d-cpu` is the smaller CPU-only wheel
source /opt/ros/jazzy/setup.bash
python -c "import open3d as o3d, rclpy; print(o3d.__version__)"
```

- Open3D-ML models need the extra: `pip install open3d[ml]` [2]. A package can declare the
  rosdep key `python3-open3d-pip`, which installs from PyPI [11].
- **ARM64** wheels (Jetson, Raspberry Pi) have no CUDA; Jetson users who want CUDA build from
  source, and the GUI needs full OpenGL, so Raspberry Pi builds use `-DBUILD_GUI=OFF` [4].
- **Windows:** `open3d` is the CPU wheel; `open3d-cuda` and `open3d-xpu` add CUDA or Intel GPU
  support [2]. **C++:** prebuilt archives on GitHub releases (Linux x86_64 with or without CUDA
  12.6, macOS arm64, Windows); point CMake at one with `-DOpen3D_ROOT=` [2].

## How an agent works with it

Agents drive it through the Python API, as the examples in the repo do [1]. A scan-to-map check:

```python
import numpy as np, open3d as o3d
src = o3d.io.read_point_cloud("scan.pcd").voxel_down_sample(voxel_size=0.05)
dst = o3d.io.read_point_cloud("map.pcd").voxel_down_sample(voxel_size=0.05)
src, _ = src.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
dst.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
reg = o3d.pipelines.registration.registration_icp(
    src, dst, 0.2, np.eye(4),
    o3d.pipelines.registration.TransformationEstimationPointToPlane())
print(reg.fitness, reg.inlier_rmse)    # overlap share and RMSE of inlier pairs
print(reg.transformation)              # 4x4, scan into map frame
```

- **Other building blocks** [1]: `segment_plane` (RANSAC floor or table), `cluster_dbscan`,
  `compute_fpfh_feature` with `registration_ransac_based_on_feature_matching` for a global first
  guess when ICP has no initial pose, symmetric ICP (new in 0.20), NDT, colored ICP, multiway
  registration and pose-graph optimisation.
- **GPU:** convert with `o3d.t.geometry.PointCloud.from_legacy(pcd)`, move with `.cuda(0)`, and
  call `o3d.t.pipelines.registration.icp` or `multi_scale_icp`; the same code runs on CPU, CUDA
  or SYCL [8].
- **From a ROS 2 topic in Python:** `sensor_msgs_py` ships with Jazzy and needs no extra glue [14].

```python
from sensor_msgs_py import point_cloud2
xyz = point_cloud2.read_points_numpy(msg, field_names=("x", "y", "z"), skip_nans=True)
pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(xyz.astype(np.float64)))
out = point_cloud2.create_cloud_xyz32(msg.header, np.asarray(pcd.points))  # keeps frame_id
```

- **Check the result:** `fitness` near 1 and `inlier_rmse` near the sensor noise mean a good fit;
  `evaluate_registration` scores a known transform. Write the aligned cloud with
  `o3d.io.write_point_cloud` and view it with `o3d.visualization.draw_geometries`, or offscreen
  (Traps). The perception skill is [perception-lidar](../../skills/perception-lidar/SKILL.md).

## Traps

- **No ROS 2 binary glue on Jazzy.** `perception_open3d` (`open3d_conversions`, C++) is released
  only for Humble (0.2.1); Jazzy, Kilted, Lyrical and Rolling list it with no version [11]. Its
  `ros2` branch was last changed in May 2025 [10]. It depends on rosdep key `libopen3d-dev`, which
  has no Ubuntu 24.04 entry [11], so `rosdep install` fails on it: build it from source with
  `--skip-keys libopen3d-dev` and a C++ archive, or use `sensor_msgs_py` in Python as above.
- **conda breaks ROS.** ROS binaries need the interpreter they were built with; a conda Python
  usually differs, and `rclpy` will not load [13]. Use a venv from the system `python3`.
- **`read_points_numpy` needs one dtype.** It asserts that every field read has the same type;
  read only `x`, `y`, `z`, or use `read_points` for mixed fields [14].
- **The GPU only helps tensor code.** Legacy `open3d.geometry` types are CPU-only unless copied
  to tensor types [7]; `o3d.pipelines.registration.registration_icp` never touches CUDA.
- **Headless rendering changed in 0.20.** The legacy `Visualizer` now falls back to an EGL
  offscreen context when there is no display, with `libegl1` installed for software rendering
  [6]. The Filament renderer uses Vulkan; without a GPU, set
  `VK_DRIVER_FILES=/usr/share/vulkan/icd.d/lvp_icd.json` (Mesa lavapipe) and, offscreen,
  `EGL_PLATFORM=surfaceless` before importing `open3d` [5]. Advice to rebuild with OSMesa dates
  from 0.19 and earlier [1].
- **Thread limits moved in 0.20.** Open3D replaced OpenMP with TBB, so `OMP_NUM_THREADS` no longer
  applies; call `o3d.utility.set_max_threads(n)` [1]. Open3D 0.18 or older needs `numpy<2` [2].
- **Slow upstream support.** Releases are irregular (0.19 to 0.20 took 20 months) [3], and the
  tracker holds about 1,300 open issues; most opened in October and November 2026 had no reply
  when we looked [9]. Commits are frequent (last 13 November 2026) [1]; pin the version.

## Alternatives

- [PCL](pcl.md) for C++ and ROS 2 nodes; [CloudCompare](../tools/cloudcompare.md) as a GUI.
- [OctoMap](octomap.md) for occupancy; [KISS-ICP](kiss-icp.md) and [RTAB-Map](rtab-map.md) when
  you need odometry or SLAM rather than offline registration.
- Viewing live data: [Rerun](../tools/rerun.md), [Foxglove](../tools/foxglove.md). Other Python
  3D libraries (trimesh, PyVista) were not reviewed.

## Sources

1. [Open3D repository: LICENSE, CHANGELOG, examples and docs sources (v0.19.0 and v0.20.0 tags, main)](https://github.com/isl-org/Open3D), accessed 2026-11-23
2. [Open3D docs: Getting started](https://www.open3d.org/docs/latest/getting_started.html), accessed 2026-11-23
3. [open3d on PyPI (release history and wheel files)](https://pypi.org/project/open3d/), accessed 2026-11-23
4. [Open3D docs: ARM support](https://www.open3d.org/docs/latest/arm.html), accessed 2026-11-23
5. [Open3D docs: CPU (software) rendering](https://www.open3d.org/docs/latest/tutorial/visualization/cpu_rendering.html), accessed 2026-11-23
6. [Open3D docs: Headless rendering (legacy OpenGL)](https://www.open3d.org/docs/latest/tutorial/visualization/headless_rendering.html), accessed 2026-11-23
7. [Open3D docs: SYCL backend (legacy versus tensor types)](https://www.open3d.org/docs/latest/sycl.html), accessed 2026-11-23
8. [Open3D docs: ICP registration (tensor)](https://www.open3d.org/docs/latest/tutorial/t_pipelines/t_icp_registration.html), accessed 2026-11-23
9. [Open3D issue tracker](https://github.com/isl-org/Open3D/issues), accessed 2026-11-23
10. [perception_open3d repository: README, open3d_conversions package (ros2 branch)](https://github.com/ros-perception/perception_open3d), accessed 2026-11-23
11. [rosdistro: distribution files and rosdep base.yaml and python.yaml](https://github.com/ros/rosdistro), accessed 2026-11-23
12. [Ubuntu packages: open3d](https://packages.ubuntu.com/search?keywords=open3d&searchon=names&suite=all&section=all), accessed 2026-11-23
13. [ROS 2 docs (Jazzy): Using Python packages with ROS 2](https://docs.ros.org/en/jazzy/How-To-Guides/Using-Python-Packages.html), accessed 2026-11-23
14. [sensor_msgs_py point_cloud2.py, jazzy branch](https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs_py/sensor_msgs_py/point_cloud2.py), accessed 2026-11-23
