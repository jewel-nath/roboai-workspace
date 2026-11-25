# Discovery and ROS traffic across robots

Part of [ops-fleet](../SKILL.md). How robots keep their ROS graphs apart, and how a fleet tool or an
operator's laptop joins one robot's graph on purpose. Choosing the middleware itself is in
[choose a ROS 2 middleware](../../../wiki/guides/choose-a-ros2-middleware.md); container
networking in [ops-docker-ci](../../ops-docker-ci/references/compose.md). Sources: ROS 2 docs
"The ROS_DOMAIN_ID", "Improved Dynamic Discovery" and "Using Fast DDS Discovery Server" (jazzy
branch), Fast DDS v2.14.7 source, `rmw_zenoh` README and design doc (jazzy branch),
`domain_bridge` README and examples (main, released 0.5.0 for Jazzy), all read 2026-11-25.

## The rule

Each robot is its own ROS graph: its own `ROS_DOMAIN_ID` (see the plan in
[identity-config.md](identity-config.md#domain-id-plan)), discovery limited to the robot, nothing
shared by default. Fleet tools then reach one robot at a time, or receive a few chosen topics.
VPN tunnels (WireGuard, Tailscale and similar) route unicast IP; do not count on DDS multicast
discovery crossing them. Every recipe below works over unicast.

| Middleware on the robots | Keep the robot private | A tool joins robot-01 |
|---|---|---|
| Fast DDS or Cyclone DDS, simple discovery | `ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST` | `ROS_DOMAIN_ID=11`, `ROS_STATIC_PEERS=robot-01` |
| Fast DDS Discovery Server | a server on the robot, nodes point at `127.0.0.1` | `ROS_DISCOVERY_SERVER=robot-01:11811`, `ROS_SUPER_CLIENT=TRUE` |
| `rmw_zenoh_cpp` | one router per robot (`rmw_zenohd`) | client session connected to `tcp/robot-01:7447`, `ROS_DOMAIN_ID=11` |

`robot-01` is the robot's name on the VPN (most mesh VPNs give one by DNS); an address works too.

## Simple discovery with static peers (Fast DDS, Cyclone DDS)

On the robot, in `/etc/my_robot/env.sh`: `ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST`. Its nodes find each
other and send nothing to the network on their own. A robot with two computers needs `SUBNET` (the default)
on its own network instead, or `ROS_STATIC_PEERS` naming the other computer. On the tool's machine:

```bash
export ROS_DOMAIN_ID=11                 # robot-01's domain
export ROS_STATIC_PEERS=robot-01        # ';'-separated; names or addresses
ros2 daemon stop                        # the daemon keeps the old settings otherwise
ros2 topic list
```

The Jazzy discovery tables show that across hosts it is enough for one side to list the other
as a static peer, as long as neither side has `OFF`. These variables do nothing under
`rmw_zenoh`, and do not exist on Humble.

## Fast DDS Discovery Server

Replaces multicast discovery with a server that clients register with; nodes learn only about
topics they use, which cuts discovery traffic on busy graphs. Jazzy ships Fast DDS 2.14.

```bash
# on the robot: a discovery server as a service (a unit like ops-bringup's Zenoh router unit)
fastdds discovery -i 0 -l 0.0.0.0 -p 11811      # --server-id, --udp-address, --udp-port
# /etc/my_robot/env.sh, for every node on the robot
export ROS_DISCOVERY_SERVER=127.0.0.1:11811
```

```bash
# a tool on the VPN looking at robot-01
export ROS_DISCOVERY_SERVER=robot-01:11811
export ROS_SUPER_CLIENT=TRUE      # receive the whole graph; TRUE/true/1 accepted
ros2 daemon stop && ros2 node list
```

- `ROS_DISCOVERY_SERVER` is positional: server id 1 alone is `";host:port"`. Several servers,
  separated by `;`, give redundancy.
- Without the super client setting, `ros2 topic list` and `ros2 bag record` see only part of
  the graph. Start the daemon after setting it.
- Robots with separate servers do not discover each other even on one domain; still give each
  its own domain, so a mistyped server cannot join two robots.
- Both ends must run Fast DDS; Cyclone DDS nodes do not use the server.
- Fast DDS XML profiles: Jazzy reads `FASTRTPS_DEFAULT_PROFILES_FILE` (the `mutation_tries`
  section of the Jazzy Discovery Server tutorial shows `FASTDDS_DEFAULT_PROFILES_FILE`, which Fast
  DDS 2.14 does not read); Lyrical's Fast DDS 3 reads `FASTDDS_DEFAULT_PROFILES_FILE`.

## rmw_zenoh: a router per robot

```bash
# on the robot, as a service before the ROS nodes (router unit in ops-bringup)
ros2 run rmw_zenoh_cpp rmw_zenohd
# /etc/my_robot/env.sh
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
export ROS_DOMAIN_ID=11
```

The default router listens on `tcp/[::]:7447` and exits on hosts without IPv6; set
`ZENOH_CONFIG_OVERRIDE='listen/endpoints=["tcp/0.0.0.0:7447"]'` for the router there. Nodes
connect to the local router by default.

A tool joins robot-01 as a client of its router:

```bash
export RMW_IMPLEMENTATION=rmw_zenoh_cpp ROS_DOMAIN_ID=11
export ZENOH_CONFIG_OVERRIDE='mode="client";connect/endpoints=["tcp/robot-01:7447"]'
ros2 topic hz /odom
```

A fleet router: each robot's router also connects to `tcp/fleet.example.com:7447` (set in the
robot router's `connect/endpoints`). Then:

- rmw_zenoh puts the domain ID first in every key expression
  (`<domain_id>/<fully_qualified_name>/<type>/<hash>`), so robots on different domains stay
  apart even through one router. **Robots on the same domain without namespaces become one
  graph**: robot-01's `/cmd_vel` subscriber receives robot-02's commands. Never connect routers
  of robots that share a domain unless every topic is namespaced.
- Data crosses the link only for topics someone subscribes to, at full rate. Throttle on the
  robot (`topic_tools throttle`) or use the router's `downsampling` rules (in the router config
  file), keyed on those key expressions, before a dashboard pulls a camera over LTE.
- The router config also has `access_control` rules; `zenoh_security_tools` (in the Jazzy
  release) generates configs with access control, authentication and encryption. Those secure
  Zenoh links; SROS 2 is in [arch-safety](../../arch-safety/SKILL.md).
- `zenoh-bridge-ros2dds` (used by Open-RMF's free_fleet) bridges DDS robots into Zenoh with its
  own key layout; it cannot talk to `rmw_zenoh` nodes.
- `rmw_zenoh` is Tier 1 only from Kilted (so on Lyrical); on Jazzy it is a released binary
  without Tier 1 support. Every process on a robot must use the same RMW.

## Sharing a few topics with domain_bridge (DDS)

`domain_bridge` (Apache-2.0, `ros-jazzy-domain-bridge` 0.5.0; not released for Lyrical) copies
chosen topics, services and actions from one domain to another, with remapping. Run one per robot,
to publish a few topics into a fleet domain under the robot's name:

```yaml
# /etc/my_robot/domain_bridge.yaml (rendered per robot)
name: robot_01_to_fleet
from_domain: 11
to_domain: 1
topics:
  diagnostics_toplevel_state:
    type: diagnostic_msgs/msg/DiagnosticStatus
    remap: robot_01/diagnostics_toplevel_state
  battery_state:
    type: sensor_msgs/msg/BatteryState
    remap: robot_01/battery_state
    qos:
      reliability: best_effort
```

```bash
ros2 run domain_bridge domain_bridge /etc/my_robot/domain_bridge.yaml
```

Bridge status and low-rate topics, not sensor streams: every message of a bridged topic is
copied into the other domain and sent over the link.

## Checks

- On robot-01: `ros2 topic list` shows only robot-01's topics, never another robot's.
- From a laptop on the VPN with the recipe for your middleware: `ros2 node list` shows robot-01's
  nodes and `ros2 topic hz /odom` shows data; with the variables unset, it shows nothing.
- `ros2 doctor --report` on the robot lists the RMW and domain you expect.
- For Zenoh fleet routers: two robots on different domains, both connected, do not see each
  other's topics.
