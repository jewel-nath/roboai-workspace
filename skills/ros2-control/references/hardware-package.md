# Packaging a ros2_control hardware plugin

How the plugin from [hardware-interface.md](hardware-interface.md) is exported so the controller
manager can load it: the pluginlib description, CMake, `package.xml`, and a load check.

## Plugin description: `my_robot_hardware.xml`

```xml
<library path="my_robot_hardware">
  <class name="my_robot_hardware/MyRobotSystem"
         type="my_robot_hardware::MyRobotSystem"
         base_class_type="hardware_interface::SystemInterface">
    <description>ros2_control system interface for my_robot's motor controller.</description>
  </class>
</library>
```

`name` is what the URDF `<plugin>` tag uses; `type` must match `PLUGINLIB_EXPORT_CLASS`;
`path` is the library target name.

## CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.16)
project(my_robot_hardware LANGUAGES CXX)

find_package(ament_cmake REQUIRED)
set(DEPS hardware_interface pluginlib rclcpp rclcpp_lifecycle)
foreach(dep IN ITEMS ${DEPS})
  find_package(${dep} REQUIRED)
endforeach()

add_library(my_robot_hardware SHARED src/my_robot_system.cpp src/motor_bus.cpp)
target_compile_features(my_robot_hardware PUBLIC cxx_std_17)
target_include_directories(my_robot_hardware PUBLIC
  $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include/${PROJECT_NAME}>)
target_link_libraries(my_robot_hardware PUBLIC
  hardware_interface::hardware_interface
  pluginlib::pluginlib
  rclcpp::rclcpp
  rclcpp_lifecycle::rclcpp_lifecycle)

# Without this line the controller manager cannot find the plugin
pluginlib_export_plugin_description_file(hardware_interface my_robot_hardware.xml)

install(DIRECTORY include/ DESTINATION include/${PROJECT_NAME})
install(TARGETS my_robot_hardware EXPORT export_my_robot_hardware
  ARCHIVE DESTINATION lib LIBRARY DESTINATION lib RUNTIME DESTINATION bin)

ament_export_targets(export_my_robot_hardware HAS_LIBRARY_TARGET)
ament_export_dependencies(${DEPS})
ament_package()
```

`package.xml` needs `<buildtool_depend>ament_cmake</buildtool_depend>` and a `<depend>` for each
of `hardware_interface`, `pluginlib`, `rclcpp` and `rclcpp_lifecycle`.

## Check it loads

```bash
colcon build --packages-select my_robot_hardware && source install/setup.bash
ros2 launch my_robot_bringup robot.launch.py hardware:=real
ros2 control list_hardware_components -v   # my_robot_system: active, interfaces listed
```

If the log says the plugin class does not exist, compare the URDF `<plugin>` text with the XML
`name`, check the export line in CMake, and source the workspace in the shell that launches.

Sources: control.ros.org Jazzy, "Writing a Hardware Component"; ros2_control_demos `jazzy`
example 2 (CMake and plugin XML layout).
