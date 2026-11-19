# C++ nodes (rclcpp, Jazzy)

Templates for [ros2-core](../SKILL.md), checked against the rclcpp `jazzy` branch. Build setup is
in [packages.md](packages.md).

## A node with a parameter, a subscription, a publisher and a timer

```cpp
#include <chrono>
#include <memory>
#include <optional>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/range.hpp"
#include "std_msgs/msg/float32.hpp"

namespace my_robot_driver
{

class RangeFilter : public rclcpp::Node
{
public:
  explicit RangeFilter(const rclcpp::NodeOptions & options = rclcpp::NodeOptions())
  : Node("range_filter", options)
  {
    rcl_interfaces::msg::ParameterDescriptor desc;
    desc.description = "Smoothing factor";
    rcl_interfaces::msg::FloatingPointRange range;
    range.from_value = 0.0;
    range.to_value = 1.0;
    desc.floating_point_range.push_back(range);
    alpha_ = declare_parameter("alpha", 0.3, desc);

    // Keep the handle: dropping it unregisters the callback.
    post_set_handle_ = add_post_set_parameters_callback(
      [this](const std::vector<rclcpp::Parameter> & params) {
        for (const auto & p : params) {
          if (p.get_name() == "alpha") {alpha_ = p.as_double();}
        }
      });

    pub_ = create_publisher<std_msgs::msg::Float32>("range/filtered", 10);
    sub_ = create_subscription<sensor_msgs::msg::Range>(
      "range/raw", rclcpp::SensorDataQoS(),
      [this](const sensor_msgs::msg::Range & msg) {on_range(msg);});
    timer_ = create_wall_timer(std::chrono::seconds(1), [this]() {report();});
  }

private:
  void on_range(const sensor_msgs::msg::Range & msg)
  {
    value_ = value_ ? *value_ + alpha_ * (msg.range - *value_) : msg.range;
    std_msgs::msg::Float32 out;
    out.data = static_cast<float>(*value_);
    pub_->publish(out);
  }

  void report()
  {
    if (!value_) {
      RCLCPP_WARN_THROTTLE(get_logger(), *get_clock(), 5000, "no range received yet");
    }
  }

  double alpha_;
  std::optional<double> value_;
  rclcpp::node_interfaces::PostSetParametersCallbackHandle::SharedPtr post_set_handle_;
  rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr pub_;
  rclcpp::Subscription<sensor_msgs::msg::Range>::SharedPtr sub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

}  // namespace my_robot_driver

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<my_robot_driver::RangeFilter>());
  rclcpp::shutdown();
  return 0;
}
```

- Subscription callbacks take `const MsgT &`, `MsgT::ConstSharedPtr` or `MsgT::UniquePtr`. The
  `MsgT::SharedPtr` form (shared pointer to non-const) still compiles in Jazzy but is deprecated in
  Lyrical.
- Throttled logging takes the clock and a period in milliseconds.

## Non-blocking service client

```cpp
#include "example_interfaces/srv/set_bool.hpp"

using SetBool = example_interfaces::srv::SetBool;

// In the constructor:
client_ = create_client<SetBool>("enable_motors");

void request_enable()
{
  if (!client_->service_is_ready()) {
    RCLCPP_WARN(get_logger(), "enable_motors not available");
    return;
  }
  auto request = std::make_shared<SetBool::Request>();
  request->data = true;
  client_->async_send_request(
    request, [this](rclcpp::Client<SetBool>::SharedFuture future) {
      RCLCPP_INFO(get_logger(), "enable_motors: %s", future.get()->message.c_str());
    });
}
```

Waiting on the future (`future.get()`, `spin_until_future_complete`) inside a callback deadlocks a
single-threaded executor. Use the response callback as above.

## Lifecycle node

```cpp
#include "rclcpp_lifecycle/lifecycle_node.hpp"
#include "std_msgs/msg/string.hpp"

using CallbackReturn =
  rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn;

class Driver : public rclcpp_lifecycle::LifecycleNode
{
public:
  Driver()
  : LifecycleNode("driver") {}

  CallbackReturn on_configure(const rclcpp_lifecycle::State &) override
  {
    pub_ = create_publisher<std_msgs::msg::String>("status", 10);  // open the device here
    return CallbackReturn::SUCCESS;
  }

  CallbackReturn on_activate(const rclcpp_lifecycle::State & state) override
  {
    LifecycleNode::on_activate(state);  // activates the lifecycle publishers
    timer_ = create_wall_timer(std::chrono::milliseconds(100), [this]() {
        std_msgs::msg::String msg;
        msg.data = "ok";
        pub_->publish(msg);
      });
    return CallbackReturn::SUCCESS;
  }

  CallbackReturn on_deactivate(const rclcpp_lifecycle::State & state) override
  {
    timer_.reset();
    LifecycleNode::on_deactivate(state);
    return CallbackReturn::SUCCESS;
  }

  CallbackReturn on_cleanup(const rclcpp_lifecycle::State &) override
  {
    pub_.reset();  // close the device here
    return CallbackReturn::SUCCESS;
  }

private:
  rclcpp_lifecycle::LifecyclePublisher<std_msgs::msg::String>::SharedPtr pub_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<Driver>();
  rclcpp::spin(node->get_node_base_interface());
  rclcpp::shutdown();
  return 0;
}
```

A lifecycle publisher that was never activated drops every message with only a log line.

## Components (several nodes in one process)

Give the node class a constructor that takes `const rclcpp::NodeOptions &` (as `RangeFilter` does),
drop `main`, and register it at the end of the source file:

```cpp
#include "rclcpp_components/register_node_macro.hpp"
RCLCPP_COMPONENTS_REGISTER_NODE(my_robot_driver::RangeFilter)
```

```cmake
find_package(rclcpp_components REQUIRED)
add_library(range_filter_component SHARED src/range_filter.cpp)
target_link_libraries(range_filter_component PUBLIC
  rclcpp::rclcpp rclcpp_components::component ${sensor_msgs_TARGETS} ${std_msgs_TARGETS})
rclcpp_components_register_node(range_filter_component
  PLUGIN "my_robot_driver::RangeFilter"
  EXECUTABLE range_filter)
install(TARGETS range_filter_component
  ARCHIVE DESTINATION lib LIBRARY DESTINATION lib RUNTIME DESTINATION bin)
```

`rclcpp_components_register_node` also builds a standalone `range_filter` executable. Load the
component into a container from a launch file ([launch.md](launch.md)) or with
`ros2 component load /sensor_container my_robot_driver my_robot_driver::RangeFilter`. Zero-copy transport
between components also needs `use_intra_process_comms: true` in each node's extra arguments.
