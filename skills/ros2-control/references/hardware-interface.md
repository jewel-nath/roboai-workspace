# A ros2_control hardware interface on Jazzy

A complete `SystemInterface` plugin for a robot whose joints take velocity commands and report
position and velocity (wheels of a differential-drive base, or velocity-driven arm joints). It uses
the API that works unchanged on Jazzy (ros2_control 4.34 or newer), Kilted and Lyrical: `on_init`
takes `HardwareComponentInterfaceParams`, the framework creates the interfaces from the
`<ros2_control>` tag, and the plugin reads and writes them with `set_state` and `get_command`.

Package layout (`ament_cmake`):

```text
my_robot_hardware/
  CMakeLists.txt
  package.xml
  my_robot_hardware.xml                 # pluginlib description
  include/my_robot_hardware/motor_bus.hpp
  include/my_robot_hardware/my_robot_system.hpp
  src/motor_bus.cpp                     # your driver: serial, CAN, I2C ...
  src/my_robot_system.cpp
```

## The driver seam

Keep bus code out of the plugin. The plugin only needs these calls; implement them for your board.

```cpp
// include/my_robot_hardware/motor_bus.hpp
#pragma once
#include <string>
#include <vector>

namespace my_robot_hardware
{
// One request/response exchange per call, with a timeout well under one control period.
class MotorBus
{
public:
  bool open(const std::string & port, int baud_rate);
  void close();
  bool enable(bool on);
  bool read_joints(std::vector<double> & ticks, std::vector<double> & ticks_per_s);
  bool write_velocities(const std::vector<double> & ticks_per_s);
};
}  // namespace my_robot_hardware
```

## Header

```cpp
// include/my_robot_hardware/my_robot_system.hpp
#ifndef MY_ROBOT_HARDWARE__MY_ROBOT_SYSTEM_HPP_
#define MY_ROBOT_HARDWARE__MY_ROBOT_SYSTEM_HPP_

#include <string>
#include <vector>

#include "hardware_interface/system_interface.hpp"
#include "my_robot_hardware/motor_bus.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_lifecycle/state.hpp"

namespace my_robot_hardware
{
class MyRobotSystem : public hardware_interface::SystemInterface
{
public:
  hardware_interface::CallbackReturn on_init(
    const hardware_interface::HardwareComponentInterfaceParams & params) override;
  hardware_interface::CallbackReturn on_configure(const rclcpp_lifecycle::State & previous) override;
  hardware_interface::CallbackReturn on_cleanup(const rclcpp_lifecycle::State & previous) override;
  hardware_interface::CallbackReturn on_activate(const rclcpp_lifecycle::State & previous) override;
  hardware_interface::CallbackReturn on_deactivate(const rclcpp_lifecycle::State & previous) override;
  hardware_interface::return_type read(
    const rclcpp::Time & time, const rclcpp::Duration & period) override;
  hardware_interface::return_type write(
    const rclcpp::Time & time, const rclcpp::Duration & period) override;

private:
  std::string port_;
  int baud_rate_{0};
  double ticks_per_rad_{0.0};
  std::vector<std::string> position_names_;  // "<joint>/position"
  std::vector<std::string> velocity_names_;  // "<joint>/velocity", state and command
  std::vector<double> rx_ticks_, rx_rate_, tx_rate_;  // sized once in on_init
  MotorBus bus_;
};
}  // namespace my_robot_hardware

#endif  // MY_ROBOT_HARDWARE__MY_ROBOT_SYSTEM_HPP_
```

## Implementation

```cpp
// src/my_robot_system.cpp
#include "my_robot_hardware/my_robot_system.hpp"

#include <algorithm>
#include <cmath>
#include <string>

#include "hardware_interface/lexical_casts.hpp"
#include "hardware_interface/types/hardware_interface_type_values.hpp"

namespace my_robot_hardware
{
using hardware_interface::CallbackReturn;
using hardware_interface::return_type;
using hardware_interface::HW_IF_POSITION;
using hardware_interface::HW_IF_VELOCITY;

CallbackReturn MyRobotSystem::on_init(
  const hardware_interface::HardwareComponentInterfaceParams & params)
{
  // The base class parses the <ros2_control> tag into info_ and creates the interfaces
  if (SystemInterface::on_init(params) != CallbackReturn::SUCCESS) {
    return CallbackReturn::ERROR;
  }
  try {
    port_ = info_.hardware_parameters.at("port");
    baud_rate_ = std::stoi(info_.hardware_parameters.at("baud_rate"));
    ticks_per_rad_ = hardware_interface::stod(info_.hardware_parameters.at("ticks_per_rad"));
  } catch (const std::exception & e) {
    RCLCPP_FATAL(get_logger(), "Missing or invalid <param> in <hardware>: %s", e.what());
    return CallbackReturn::ERROR;
  }
  if (!(ticks_per_rad_ > 0.0)) {
    RCLCPP_FATAL(get_logger(), "ticks_per_rad must be positive");
    return CallbackReturn::ERROR;
  }

  for (const auto & joint : info_.joints) {
    const bool ok = joint.command_interfaces.size() == 1 &&
      joint.command_interfaces[0].name == HW_IF_VELOCITY &&
      joint.state_interfaces.size() == 2 &&
      joint.state_interfaces[0].name == HW_IF_POSITION &&
      joint.state_interfaces[1].name == HW_IF_VELOCITY;
    if (!ok) {
      RCLCPP_FATAL(
        get_logger(), "Joint '%s' needs command [velocity] and state [position, velocity]",
        joint.name.c_str());
      return CallbackReturn::ERROR;
    }
    position_names_.push_back(joint.name + "/" + HW_IF_POSITION);
    velocity_names_.push_back(joint.name + "/" + HW_IF_VELOCITY);
  }
  rx_ticks_.assign(info_.joints.size(), 0.0);
  rx_rate_.assign(info_.joints.size(), 0.0);
  tx_rate_.assign(info_.joints.size(), 0.0);
  return CallbackReturn::SUCCESS;  // no I/O here: on_init also runs for tests and tooling
}

CallbackReturn MyRobotSystem::on_configure(const rclcpp_lifecycle::State &)
{
  if (!bus_.open(port_, baud_rate_)) {
    RCLCPP_ERROR(get_logger(), "Cannot open %s", port_.c_str());
    return CallbackReturn::FAILURE;  // stays unconfigured and can be retried
  }
  for (const auto & [name, description] : joint_state_interfaces_) {
    set_state(name, 0.0);
  }
  for (const auto & [name, description] : joint_command_interfaces_) {
    set_command(name, 0.0);
  }
  return CallbackReturn::SUCCESS;
}

CallbackReturn MyRobotSystem::on_cleanup(const rclcpp_lifecycle::State &)
{
  bus_.close();
  return CallbackReturn::SUCCESS;
}

CallbackReturn MyRobotSystem::on_activate(const rclcpp_lifecycle::State &)
{
  // Start at standstill; a position interface would copy its state into its command instead
  for (const auto & name : velocity_names_) {
    set_command(name, 0.0);
  }
  return bus_.enable(true) ? CallbackReturn::SUCCESS : CallbackReturn::ERROR;
}

CallbackReturn MyRobotSystem::on_deactivate(const rclcpp_lifecycle::State &)
{
  std::fill(tx_rate_.begin(), tx_rate_.end(), 0.0);
  bus_.write_velocities(tx_rate_);
  bus_.enable(false);
  return CallbackReturn::SUCCESS;
}

return_type MyRobotSystem::read(const rclcpp::Time &, const rclcpp::Duration &)
{
  if (!bus_.read_joints(rx_ticks_, rx_rate_)) {
    RCLCPP_ERROR_THROTTLE(get_logger(), *get_clock(), 1000, "Joint read failed");
    return return_type::ERROR;  // the component goes to on_error and its controllers stop
  }
  for (std::size_t i = 0; i < position_names_.size(); ++i) {
    set_state(position_names_[i], rx_ticks_[i] / ticks_per_rad_);
    set_state(velocity_names_[i], rx_rate_[i] / ticks_per_rad_);
  }
  return return_type::OK;
}

return_type MyRobotSystem::write(const rclcpp::Time &, const rclcpp::Duration &)
{
  for (std::size_t i = 0; i < velocity_names_.size(); ++i) {
    const double command = get_command(velocity_names_[i]);
    // A controller that has not written yet leaves NaN; never send it to a motor
    tx_rate_[i] = std::isfinite(command) ? command * ticks_per_rad_ : 0.0;
  }
  return bus_.write_velocities(tx_rate_) ? return_type::OK : return_type::ERROR;
}

}  // namespace my_robot_hardware

#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(my_robot_hardware::MyRobotSystem, hardware_interface::SystemInterface)
```

Notes:

- Units are SI: rad, rad/s, m, m/s, N·m. Convert encoder ticks in the plugin, nowhere else.
- `set_state(name, value)` and `get_command(name)` look the name up and may wait for a lock. That
  is fine for most robots. For hard real time, look up the handles once in `on_configure` with
  `get_state_interface_handle(name)` / `get_command_interface_handle(name)` (Jazzy 4.40 or newer)
  and use the handle overloads with the wait flag set to `false`.
- On Lyrical, `set_state(name, 0)` with an `int` throws at run time; always pass a `double`.
- `get_node()` gives the component its own rclcpp node for a diagnostics publisher; keep its
  callbacks out of `read()` and `write()`.

Export and build it as shown in [hardware-package.md](hardware-package.md).

Sources: control.ros.org Jazzy, "Writing a Hardware Component" and the Humble to Jazzy migration
guide; `hardware_interface` headers on the ros2_control `jazzy` branch (4.50.0) and `master`
(6.13.0, Lyrical); ros2_control_demos `jazzy` example 2.
