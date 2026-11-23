# A point-cloud node in C++ with PCL

Part of [perception-lidar](../SKILL.md): the same job as [python-node.md](python-node.md) (voxel
grid, level-ground removal, Euclidean clusters) with PCL, for clouds too large for Python. Checked
against PCL 1.14.0 headers (Ubuntu 24.04's `libpcl-dev`) and pcl_conversions 2.6.5 (`jazzy`); not
compiled. Node conventions follow [ros2-core cpp-nodes.md](../../ros2-core/references/cpp-nodes.md).

Like the Python node it expects a z-up frame such as `base_footprint` (the CropBox stage in
[filters.md](filters.md) provides it). It publishes the obstacle points with the cluster id in
`intensity`; colour by Intensity in RViz to see the clusters.

## `src/cloud_segmenter.cpp`

```cpp
#include <cmath>
#include <memory>
#include <vector>

#include <Eigen/Core>
#include <pcl/filters/extract_indices.h>
#include <pcl/filters/filter.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/search/kdtree.h>
#include <pcl/segmentation/extract_clusters.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl_conversions/pcl_conversions.h>
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/point_cloud2.hpp>

using Cloud = pcl::PointCloud<pcl::PointXYZ>;

class CloudSegmenter : public rclcpp::Node
{
public:
  CloudSegmenter()
  : Node("cloud_segmenter")
  {
    voxel_ = static_cast<float>(declare_parameter("voxel_size", 0.05));
    ground_tolerance_ = declare_parameter("ground_tolerance", 0.05);
    max_tilt_ = declare_parameter("max_ground_tilt_deg", 10.0) * M_PI / 180.0;
    cluster_tolerance_ = declare_parameter("cluster_tolerance", 0.3);
    min_points_ = declare_parameter("min_cluster_points", 10);
    pub_ = create_publisher<sensor_msgs::msg::PointCloud2>("obstacles", rclcpp::SensorDataQoS());
    sub_ = create_subscription<sensor_msgs::msg::PointCloud2>(
      "points", rclcpp::SensorDataQoS(),
      [this](sensor_msgs::msg::PointCloud2::ConstSharedPtr msg) {on_cloud(*msg);});
  }

private:
  void on_cloud(const sensor_msgs::msg::PointCloud2 & msg)
  {
    Cloud raw;
    pcl::fromROSMsg(msg, raw);  // copies x, y, z; other fields are ignored
    auto cloud = std::make_shared<Cloud>();
    pcl::Indices kept;
    pcl::removeNaNFromPointCloud(raw, *cloud, kept);

    auto down = std::make_shared<Cloud>();
    pcl::VoxelGrid<pcl::PointXYZ> voxel;
    voxel.setInputCloud(cloud);
    voxel.setLeafSize(voxel_, voxel_, voxel_);
    voxel.filter(*down);

    pcl::PointCloud<pcl::PointXYZI> labelled;
    if (!down->empty()) {
      const auto obstacles = remove_ground(down);
      label_clusters(obstacles, labelled);
    }
    sensor_msgs::msg::PointCloud2 out;
    pcl::toROSMsg(labelled, out);
    out.header = msg.header;  // toROSMsg copies PCL's empty header; restore stamp and frame
    pub_->publish(out);
  }

  Cloud::Ptr remove_ground(const Cloud::Ptr & cloud) const
  {
    pcl::SACSegmentation<pcl::PointXYZ> seg;
    seg.setOptimizeCoefficients(true);
    // A plane perpendicular to +z within max_tilt_: level ground, never a wall.
    seg.setModelType(pcl::SACMODEL_PERPENDICULAR_PLANE);
    seg.setAxis(Eigen::Vector3f::UnitZ());
    seg.setEpsAngle(max_tilt_);
    seg.setMethodType(pcl::SAC_RANSAC);
    seg.setDistanceThreshold(ground_tolerance_);
    seg.setMaxIterations(200);
    seg.setInputCloud(cloud);
    auto ground = std::make_shared<pcl::PointIndices>();
    pcl::ModelCoefficients coefficients;
    seg.segment(*ground, coefficients);  // empty inliers when no plane is found

    auto obstacles = std::make_shared<Cloud>();
    pcl::ExtractIndices<pcl::PointXYZ> extract;
    extract.setInputCloud(cloud);
    extract.setIndices(ground);
    extract.setNegative(true);  // keep everything except the ground
    extract.filter(*obstacles);
    return obstacles;
  }

  void label_clusters(
    const Cloud::Ptr & obstacles, pcl::PointCloud<pcl::PointXYZI> & labelled) const
  {
    if (obstacles->empty()) {
      return;
    }
    auto tree = std::make_shared<pcl::search::KdTree<pcl::PointXYZ>>();
    tree->setInputCloud(obstacles);
    std::vector<pcl::PointIndices> clusters;
    pcl::EuclideanClusterExtraction<pcl::PointXYZ> ec;
    ec.setClusterTolerance(cluster_tolerance_);
    ec.setMinClusterSize(static_cast<pcl::uindex_t>(min_points_));
    ec.setSearchMethod(tree);
    ec.setInputCloud(obstacles);
    ec.extract(clusters);

    for (std::size_t id = 0; id < clusters.size(); ++id) {
      for (const auto index : clusters[id].indices) {
        const auto & p = (*obstacles)[index];
        pcl::PointXYZI q;
        q.x = p.x;
        q.y = p.y;
        q.z = p.z;
        q.intensity = static_cast<float>(id);
        labelled.push_back(q);
      }
    }
  }

  float voxel_;
  double ground_tolerance_;
  double max_tilt_;
  double cluster_tolerance_;
  int min_points_;
  rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr pub_;
  rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr sub_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<CloudSegmenter>());
  rclcpp::shutdown();
  return 0;
}
```

## Build files

A package is either `ament_python` or `ament_cmake`, so put the C++ node in its own package, here
`my_robot_perception_cpp`. `CMakeLists.txt`, written the way `pcl_ros` itself links on Jazzy:

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_perception_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(pcl_conversions REQUIRED)
find_package(PCL REQUIRED COMPONENTS common filters sample_consensus search segmentation)

add_executable(cloud_segmenter src/cloud_segmenter.cpp)
target_compile_features(cloud_segmenter PUBLIC cxx_std_17)
target_include_directories(cloud_segmenter PRIVATE ${PCL_INCLUDE_DIRS})
target_link_libraries(cloud_segmenter ${PCL_LIBRARIES})
# Jazzy's pcl_conversions exports no CMake target, only include directories and dependencies.
ament_target_dependencies(cloud_segmenter rclcpp sensor_msgs pcl_conversions)

install(TARGETS cloud_segmenter DESTINATION lib/${PROJECT_NAME})
ament_package()
```

On Lyrical, where `ament_target_dependencies` is deprecated and pcl_conversions exports the
interface target `pcl_conversions::pcl_conversions`, replace the last two link lines with:

```cmake
target_link_libraries(cloud_segmenter
  rclcpp::rclcpp ${sensor_msgs_TARGETS} pcl_conversions::pcl_conversions ${PCL_LIBRARIES})
```

`package.xml`:

```xml
<buildtool_depend>ament_cmake</buildtool_depend>
<depend>rclcpp</depend>
<depend>sensor_msgs</depend>
<depend>pcl_conversions</depend>
<build_depend>libpcl-all-dev</build_depend>
<exec_depend>libpcl-common</exec_depend>
<exec_depend>libpcl-filters</exec_depend>
<exec_depend>libpcl-segmentation</exec_depend>
```

Build with optimisation: colcon sets no build type by default, and unoptimised PCL code is slow.

```bash
colcon build --packages-select my_robot_perception_cpp --cmake-args -DCMAKE_BUILD_TYPE=Release
ros2 run my_robot_perception_cpp cloud_segmenter --ros-args -r points:=/lidar/points_filtered
```

## Notes

- `pcl::fromROSMsg` and `pcl::toROSMsg` (from `pcl_conversions/pcl_conversions.h`, still a `.h`
  header on Jazzy) copy the data. For a zero-copy pipeline, make the node an `rclcpp_components`
  component and load it into the same container as the `pcl_ros` filters, with
  `use_intra_process_comms`.
- `fromROSMsg` into `PointXYZ` ignores extra fields; converting into a type whose fields the
  cloud lacks (say `PointXYZI` from a cloud with no `intensity`) logs "Failed to find match for
  field".
- `SACMODEL_PERPENDICULAR_PLANE` finds the largest level plane, which on a cluttered table-top scene
  can be the table, not the floor. Crop the height band first (CropBox `max_z` low), or check the
  plane's `d` coefficient against the expected floor height.
- `pcl_ros::transformPointCloud(target_frame, in, out, tf_buffer)` (library `pcl_ros_tf`, header
  `pcl_ros/transforms.hpp`) transforms a ROS cloud by TF, looking up at the cloud's stamp with a
  1 s timeout; add `pcl_ros` as a dependency to use it.
