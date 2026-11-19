---
type: tool
name: rosbridge_suite
summary: JSON-over-WebSocket bridge that lets browsers, scripts and other non-ROS programs publish, subscribe, call services and send action goals on a ROS 2 graph; used with roslibjs or roslibpy.
tags: [rosbridge, websocket, json, cbor, roslibjs, roslibpy, rosapi, robot-web-tools, web-ui, teleop]
kind: library
area: ros2
support:
license: BSD-3-Clause
links: {repo: "https://github.com/RobotWebTools/rosbridge_suite", docs: "https://github.com/RobotWebTools/rosbridge_suite/blob/jazzy/ROSBRIDGE_PROTOCOL.md", site: "https://robotwebtools.github.io/"}
version: {tested: , latest: "2.7.1", as_of: 2026-11-18}
platforms: [linux]
agent_access: api
registry:
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://index.ros.org/p/rosbridge_server/", title: "ROS Index: rosbridge_server versions per distro", accessed: 2026-11-18}
  - {url: "https://github.com/RobotWebTools/rosbridge_suite/blob/jazzy/rosapi/README.md", title: rosapi README (jazzy branch), accessed: 2026-11-18}
  - {url: "https://github.com/RobotWebTools/rosbridge_suite/blob/jazzy/ROSBRIDGE_PROTOCOL.md", title: rosbridge v2.1.0 protocol specification (jazzy branch), accessed: 2026-11-18}
  - {url: "https://github.com/RobotWebTools/rosbridge_suite/blob/jazzy/rosbridge_server/launch/rosbridge_websocket_launch.xml", title: rosbridge_websocket launch file (jazzy branch), accessed: 2026-11-18}
  - {url: "https://github.com/RobotWebTools/rosbridge_suite/blob/jazzy/rosbridge_server/CHANGELOG.rst", title: rosbridge_server changelog (jazzy branch), accessed: 2026-11-18}
  - {url: "https://www.tornadoweb.org/en/stable/netutil.html", title: "Tornado netutil: bind_sockets", accessed: 2026-11-18}
  - {url: "https://github.com/RobotWebTools/roslibjs/blob/develop/packages/roslib/README.md", title: roslibjs README, accessed: 2026-11-18}
  - {url: "https://github.com/gramaziokohler/roslibpy/blob/main/README.rst", title: roslibpy README, accessed: 2026-11-18}
---

# rosbridge_suite

rosbridge exposes a ROS 2 graph as JSON or CBOR over a WebSocket, so a browser or a script with no
ROS install can publish, subscribe, call services and send action goals [3]: dashboards, teleop pages.

## When to use it

For status, commands and small telemetry at human rates, from roslibjs [7] or roslibpy (whose ROS 2
support its README calls in progress [8]). Images, point clouds and full-rate plots need another bridge.

## Setup

Jazzy ships 2.7.1 (`jazzy` branch), Humble 2.0.8, Kilted 3.3.1, **Lyrical** and Rolling 4.2.1 (`ros2`) [1].

```bash
sudo apt install ros-jazzy-rosbridge-suite
ros2 launch rosbridge_server rosbridge_websocket_launch.xml address:=127.0.0.1
```

It serves port 9090, starts rosapi, and takes `ssl:=true` with `certfile` and `keyfile` for `wss://` [4].
Allow-lists (`topics_glob`, `services_glob`, `params_glob`, ...) [4] are strings such as `[/cmd_vel, /battery*]`:
empty allows all, `[]` blocks all, and outer quotes keep the value a string [2]. Client: `npm install roslib` [7].

## How an agent works with it

Any WebSocket client works; each message is a JSON object with an `op` field [3]:

```json
{"op": "subscribe", "topic": "/battery_state", "type": "sensor_msgs/msg/BatteryState", "throttle_rate": 500}
{"op": "call_service", "service": "/rosapi/topics", "id": "q1"}
```

Other ops: `advertise`, `publish`, `send_action_goal`, `cancel_action_goal`; graph queries use rosapi
services [2][3]. A reply to the `call_service` above proves the bridge works; see the
[ros2-web-bridge skill](../../skills/ros2-web-bridge/SKILL.md).

## Traps

- **No authentication, every interface.** ROS 2 rosbridge has no auth [5] and an empty `address` binds
  all interfaces [4][6]: anyone on port 9090 can drive `/cmd_vel`. Bind `127.0.0.1` behind a VPN or
  authenticating proxy, set the globs, and never expose it to the internet.
- **Images and point clouds choke it.** `uint8[]` travels as base64 text; CBOR is fastest for large
  arrays and `cbor-raw` skips conversion [3]. Subscribe with `"compression": "cbor"` and a `throttle_rate`.
- **Shared QoS.** Clients on one topic share a subscription, so the first one's QoS wins; without a
  `qos` field, subscribers match existing publishers, else best effort, depth 10 [3].
- **Unknown type.** A subscribe fails when rosbridge cannot resolve the type [3]: source the
  workspace with your custom interfaces in the shell that launches rosbridge.

## Alternatives

foxglove_bridge with [Foxglove](../tools/foxglove.md); web_video_server for camera streams; Zenoh
for remote links (see [rmw_zenoh](rmw-zenoh.md)); a native rclpy node when the client can run ROS.

## Sources

1. [ROS Index: rosbridge_server versions per distro](https://index.ros.org/p/rosbridge_server/), accessed 2026-11-18
2. [rosapi README (jazzy branch)](https://github.com/RobotWebTools/rosbridge_suite/blob/jazzy/rosapi/README.md), accessed 2026-11-18
3. [rosbridge v2.1.0 protocol specification (jazzy branch)](https://github.com/RobotWebTools/rosbridge_suite/blob/jazzy/ROSBRIDGE_PROTOCOL.md), accessed 2026-11-18
4. [rosbridge_websocket launch file (jazzy branch)](https://github.com/RobotWebTools/rosbridge_suite/blob/jazzy/rosbridge_server/launch/rosbridge_websocket_launch.xml), accessed 2026-11-18
5. [rosbridge_server changelog (jazzy branch)](https://github.com/RobotWebTools/rosbridge_suite/blob/jazzy/rosbridge_server/CHANGELOG.rst), accessed 2026-11-18
6. [Tornado netutil: bind_sockets](https://www.tornadoweb.org/en/stable/netutil.html), accessed 2026-11-18
7. [roslibjs README](https://github.com/RobotWebTools/roslibjs/blob/develop/packages/roslib/README.md), accessed 2026-11-18
8. [roslibpy README](https://github.com/gramaziokohler/roslibpy/blob/main/README.rst), accessed 2026-11-18
