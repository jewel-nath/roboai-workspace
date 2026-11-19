# Packages and interfaces (Jazzy)

Build files for [ros2-core](../SKILL.md). Build-tool flags and workspace overlays are on the
[colcon](../../../wiki/tools/colcon.md) page.

## Which package type

| Package holds | Build type | Name like |
|---|---|---|
| Python nodes only | `ament_python` | `my_robot_nodes` |
| C++ nodes, or C++ and Python | `ament_cmake` | `my_robot_driver` |
| msg / srv / action definitions | `ament_cmake`, nothing else in it | `my_robot_interfaces` |
| Launch files and parameter YAML | `ament_cmake` (installs directories only) | `my_robot_bringup` |
| URDF, meshes, RViz config | `ament_cmake` | `my_robot_description` |

Keep interfaces in their own package so other packages (and other robots) can depend on the
messages without pulling in node code.

## ament_python: `setup.py`

`ros2 pkg create --build-type ament_python` writes `setup.py`, `setup.cfg`, `package.xml` and
`resource/<name>`. Add launch and config files to `data_files`, and one `console_scripts` entry per
node:

```python
import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'my_robot_nodes'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.*')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Maintainer Name',
    maintainer_email='maintainer@example.com',
    description='Nodes for my_robot',
    license='Apache-2.0',
    extras_require={'test': ['pytest']},
    entry_points={
        'console_scripts': [
            'range_filter = my_robot_nodes.range_filter:main',
        ],
    },
)
```

`setup.cfg` must keep the generated `[develop] script_dir=$base/lib/<pkg>` and
`[install] install_scripts=$base/lib/<pkg>` lines, or `ros2 run` cannot find the executables.

## ament_cmake: `CMakeLists.txt` for C++ nodes

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_driver)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(range_filter src/range_filter.cpp)
target_compile_features(range_filter PUBLIC cxx_std_17)
target_link_libraries(range_filter PUBLIC
  rclcpp::rclcpp ${sensor_msgs_TARGETS} ${std_msgs_TARGETS})

install(TARGETS range_filter DESTINATION lib/${PROJECT_NAME})
install(DIRECTORY launch config DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
```

- `target_link_libraries` with `<pkg>::<pkg>` or `${<pkg>_TARGETS}` works in Jazzy and later.
  The older `ament_target_dependencies(range_filter rclcpp std_msgs)`, still written by
  `ros2 pkg create` in Jazzy, is deprecated from Kilted on and warns at every build in Lyrical.
- Executables go to `lib/${PROJECT_NAME}`; that is where `ros2 run` looks.
- `install(DIRECTORY ...)` fails if a listed directory does not exist; list only real ones.

## `package.xml`

```xml
<?xml version="1.0"?>
<package format="3">
  <name>my_robot_driver</name>
  <version>0.1.0</version>
  <description>Driver for my_robot</description>
  <maintainer email="maintainer@example.com">Maintainer Name</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <depend>rclcpp</depend>
  <depend>sensor_msgs</depend>
  <depend>std_msgs</depend>
  <exec_depend>launch_ros</exec_depend>

  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
```

For an `ament_python` package the build tool is `ament_python` (no `buildtool_depend` on
ament_cmake), Python dependencies are `<exec_depend>`, and `<build_type>` is `ament_python`. List
every package the code imports or includes: `rosdep install` and the build farm read only this file.

## Interface package

```text
my_robot_interfaces/
  CMakeLists.txt
  package.xml
  msg/WheelState.msg
  srv/SetMode.srv
  action/Dock.action
```

```text
# msg/WheelState.msg
std_msgs/Header header
float64 position     # rad
float64 velocity     # rad/s
```

```text
# srv/SetMode.srv
uint8 MODE_IDLE=0
uint8 MODE_DRIVE=1
uint8 mode
---
bool success
string message
```

```text
# action/Dock.action
string dock_id
---
bool success
---
float32 distance_remaining   # m
```

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/WheelState.msg"
  "srv/SetMode.srv"
  "action/Dock.action"
  DEPENDENCIES std_msgs
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
```

```xml
  <buildtool_depend>ament_cmake</buildtool_depend>
  <buildtool_depend>rosidl_default_generators</buildtool_depend>
  <depend>std_msgs</depend>
  <exec_depend>rosidl_default_runtime</exec_depend>
  <member_of_group>rosidl_interface_packages</member_of_group>
```

- File names are CamelCase (`WheelState.msg`); field names are lower_snake_case; constants are
  UPPER_CASE with a value.
- Every package a field type comes from goes in `DEPENDENCIES` and in `package.xml`.
- Use the interfaces from another package as `my_robot_interfaces.msg.WheelState` (Python) or
  `my_robot_interfaces/msg/wheel_state.hpp` (C++), linking `${my_robot_interfaces_TARGETS}`.
- Using them from a C++ target in the same package needs
  `rosidl_get_typesupport_target(cpp_ts ${PROJECT_NAME} rosidl_typesupport_cpp)` and
  `target_link_libraries(my_node "${cpp_ts}")`. The old `rosidl_target_interfaces()` is deprecated
  in Jazzy and removed in Lyrical.
- Check with `ros2 interface show my_robot_interfaces/msg/WheelState` after sourcing the overlay.
