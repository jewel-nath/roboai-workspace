# Python nodes (rclpy, Jazzy)

Templates for [ros2-core](../SKILL.md). Each one runs as written once the imports resolve; replace
the message types with the robot's own. Checked against the rclpy `jazzy` branch and the
`ros2/examples` `jazzy` branch.

## A node with a parameter, a subscription, a publisher and a timer

```python
import rclpy
from rcl_interfaces.msg import FloatingPointRange, ParameterDescriptor
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Range
from std_msgs.msg import Float32


class RangeFilter(Node):
    """Smooths a range sensor and republishes the result."""

    def __init__(self):
        super().__init__('range_filter')
        alpha_range = FloatingPointRange(from_value=0.0, to_value=1.0, step=0.0)
        self.declare_parameter('alpha', 0.3, ParameterDescriptor(
            description='Smoothing factor', floating_point_range=[alpha_range]))
        self._alpha = self.get_parameter('alpha').value
        self._value = None
        # Iron and later: react only after a change was accepted.
        self.add_post_set_parameters_callback(self._on_params_set)

        # Create every entity once, here; never inside a callback.
        self._pub = self.create_publisher(Float32, 'range/filtered', 10)
        self._sub = self.create_subscription(
            Range, 'range/raw', self._on_range, qos_profile_sensor_data)
        self._timer = self.create_timer(1.0, self._report)

    def _on_params_set(self, params):
        for param in params:
            if param.name == 'alpha':
                self._alpha = param.value

    def _on_range(self, msg: Range):
        if self._value is None:
            self._value = msg.range
        self._value += self._alpha * (msg.range - self._value)
        self._pub.publish(Float32(data=self._value))

    def _report(self):
        if self._value is None:
            self.get_logger().warning('no range received yet', throttle_duration_sec=5.0)


def main(args=None):
    rclpy.init(args=args)
    node = RangeFilter()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()  # plain shutdown() raises if Ctrl-C already shut the context down
```

- The descriptor range rejects `ros2 param set /range_filter alpha 2.0` before any callback runs.
- For rules a range cannot express, add `add_on_set_parameters_callback(cb)` returning
  `SetParametersResult(successful=False, reason='...')`. That callback must not change the node's
  state: a later callback can still reject the change.

## Service server and a non-blocking client

```python
from example_interfaces.srv import SetBool

# In the server node's __init__:
self._srv = self.create_service(SetBool, 'enable_motors', self._on_enable)

def _on_enable(self, request, response):
    response.success = self._driver.set_enabled(request.data)
    response.message = 'ok' if response.success else 'driver refused'
    return response

# In the client node's __init__:
self._cli = self.create_client(SetBool, 'enable_motors')

def request_enable(self):
    if not self._cli.service_is_ready():
        self.get_logger().warning('enable_motors not available')
        return
    future = self._cli.call_async(SetBool.Request(data=True))
    future.add_done_callback(self._on_enable_done)

def _on_enable_done(self, future):
    result = future.result()
    self.get_logger().info(f'enable_motors: {result.success} ({result.message})')
```

Never call `self._cli.call(...)` or `rclpy.spin_until_future_complete(...)` inside a callback on a
single-threaded executor: the callback waits for a response that the same thread must process, so
it deadlocks. From a plain script (outside any callback), `rclpy.spin_until_future_complete(node,
future)` is fine.

## Action server

```python
import time

from example_interfaces.action import Fibonacci
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup

# In __init__:
self._action = ActionServer(
    self, Fibonacci, 'fibonacci',
    execute_callback=self._execute,
    goal_callback=lambda goal: GoalResponse.ACCEPT,
    cancel_callback=lambda goal_handle: CancelResponse.ACCEPT,  # the default rejects every cancel
    callback_group=ReentrantCallbackGroup())

def _execute(self, goal_handle):
    feedback = Fibonacci.Feedback(sequence=[0, 1])
    for i in range(1, goal_handle.request.order):
        if goal_handle.is_cancel_requested:
            goal_handle.canceled()
            return Fibonacci.Result()
        feedback.sequence.append(feedback.sequence[i] + feedback.sequence[i - 1])
        goal_handle.publish_feedback(feedback)
        time.sleep(0.5)  # stands in for real work
    goal_handle.succeed()
    return Fibonacci.Result(sequence=feedback.sequence)
```

Spin this node with a `MultiThreadedExecutor` (below); with the default executor a long
`_execute` blocks cancel requests and every other callback. Test it with
`ros2 action send_goal --feedback /fibonacci example_interfaces/action/Fibonacci "{order: 5}"`.

## Lifecycle node

```python
from rclpy.lifecycle import LifecycleNode, LifecycleState, TransitionCallbackReturn
from std_msgs.msg import String


class Driver(LifecycleNode):
    def __init__(self):
        super().__init__('driver')
        self.declare_parameter('port', '/dev/ttyUSB0')
        self._pub = None
        self._timer = None

    def on_configure(self, state: LifecycleState) -> TransitionCallbackReturn:
        self._port = self.get_parameter('port').value  # open the device here
        self._pub = self.create_lifecycle_publisher(String, 'status', 10)
        return super().on_configure(state)

    def on_activate(self, state: LifecycleState) -> TransitionCallbackReturn:
        self._timer = self.create_timer(0.1, self._tick)
        return super().on_activate(state)  # enables the lifecycle publishers

    def on_deactivate(self, state: LifecycleState) -> TransitionCallbackReturn:
        self.destroy_timer(self._timer)
        return super().on_deactivate(state)

    def on_cleanup(self, state: LifecycleState) -> TransitionCallbackReturn:
        self.destroy_lifecycle_publisher(self._pub)  # close the device here
        return super().on_cleanup(state)

    def on_shutdown(self, state: LifecycleState) -> TransitionCallbackReturn:
        return super().on_shutdown(state)

    def _tick(self):
        self._pub.publish(String(data=f'ok on {self._port}'))
```

Return `TransitionCallbackReturn.FAILURE` from a callback to refuse the transition. Drive it with
`ros2 lifecycle set /driver configure`, then `activate`; `ros2 lifecycle get /driver` shows the state.

## Executors and callback groups

```python
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor

# In __init__: the slow timer gets its own group so it cannot block the fast subscription.
self._slow_group = MutuallyExclusiveCallbackGroup()
self.create_timer(1.0, self._slow_work, callback_group=self._slow_group)

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.try_shutdown()
```

- Everything created without `callback_group=` lands in the node's default group, which is
  mutually exclusive. A `MultiThreadedExecutor` alone therefore changes nothing for one node.
- A `ReentrantCallbackGroup` lets the same callback run in parallel with itself; protect shared
  state with a lock.
- A synchronous call inside a callback needs the client in a different group from that callback,
  or a reentrant group. Async calls avoid the question.
