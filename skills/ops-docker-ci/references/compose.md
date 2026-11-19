# docker compose for a robot: networking, middleware and devices

Compose files for a robot split into containers, written for ROS 2 Jazzy and Docker Engine on
Linux. Sources: ROS 2 docs "Improved Dynamic Discovery" and "Running ROS 2 nodes in Docker"
(jazzy branch, 2026-11-16), the Fast DDS docs "Leveraging Fast DDS SHM in Docker deployments",
the `rmw_fastrtps`, `rmw_cyclonedds` and `rmw_zenoh` sources and README (jazzy branches,
2026-11). The file is `compose.yaml`; the old top-level `version:` key is obsolete, leave it out.

## Pick a network layout

| Layout | How discovery works | Choose it when |
|---|---|---|
| [Host network](#host-network-one-robot-computer) | Normal DDS multicast on the host's interfaces | One robot computer; containers must reach host tools and other machines |
| [Compose bridge network](#bridge-network-isolated-stacks) | Multicast between containers on that network only | Sim or test stacks that must not leak onto the LAN; several stacks on one host |
| [Bridge plus static peers](#static-peers) | Unicast to listed hosts | Networks that drop multicast (overlay networks, some VPNs) |
| [Zenoh router](#zenoh) | TCP to `rmw_zenohd` | Multi-host, Wi-Fi, Docker Desktop, or when DDS discovery traffic is a problem |

All containers that should talk need the same `ROS_DOMAIN_ID` and the same RMW. On Linux, domain
IDs 0 to 101 avoid the ephemeral port range (ROS 2 docs, "The ROS_DOMAIN_ID").

## Host network: one robot computer

```yaml
x-ros: &ros
  image: ghcr.io/my-org/my_robot:jazzy
  network_mode: host
  ipc: host                  # shared memory transport across containers (Fast DDS, Zenoh)
  restart: unless-stopped
  environment:
    ROS_DOMAIN_ID: "42"
    ROS_AUTOMATIC_DISCOVERY_RANGE: SUBNET   # LOCALHOST keeps all traffic on this computer

services:
  description:
    <<: *ros
    command: ros2 launch my_robot_description description.launch.py
  driver:
    <<: *ros
    command: ros2 launch my_robot_driver driver.launch.py
    devices:
      - /dev/serial/by-id/usb-My_Vendor_My_MCU-if00:/dev/my_robot_mcu
    group_add: [dialout]
  camera:
    <<: *ros
    image: ghcr.io/my-org/my_robot_perception:jazzy
    command: ros2 launch my_robot_perception camera.launch.py
    devices: [/dev/video0]
    group_add: [video]
```

- **`ipc: host` is not optional with Fast DDS** (the default RMW). With host networking, Fast DDS
  sees every container as the same host and sends data through shared memory; with separate IPC
  namespaces the segments are invisible, so `ros2 topic list` works but no messages arrive.
  Alternatives: `FASTDDS_BUILTIN_TRANSPORTS=UDPv4` on every container (no shared memory at all).
- Shared memory segments in `/dev/shm` belong to the user that made them. Run every container
  that shares IPC, and any host process in the same graph, with the same UID.
- With `network_mode: host`, `ports:` and `networks:` do not apply; Docker ignores published
  ports.

## Bridge network: isolated stacks

```yaml
services:
  sim:
    image: my_robot_sim:jazzy
    command: ros2 launch my_robot_bringup sim.launch.py headless:=true
    networks: [ros]
    environment: {ROS_DOMAIN_ID: "7"}
  navigation:
    image: ghcr.io/my-org/my_robot:jazzy
    command: ros2 launch my_robot_bringup navigation.launch.py use_sim_time:=true
    networks: [ros]
    environment: {ROS_DOMAIN_ID: "7"}

networks:
  ros: {}
```

- Containers on one bridge network discover each other with default settings (the ROS 2 docs run
  `talker` and `listener` this way). Nothing outside the network sees them, including the host.
- Each container has its own network namespace, so Fast DDS treats them as different hosts and
  uses UDP; no shared memory setup is needed, and none is used.
- **Do not set `ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST` here:** localhost is the container
  itself, so every container ends up alone.
- `/dev/shm` inside each container is 64 MB by default; raise `shm_size:` if one container moves
  large messages between its own processes over shared memory.

## Static peers

When multicast is dropped, list the peers. Jazzy's `ROS_STATIC_PEERS` takes a `;`-separated list
of addresses; `rmw_fastrtps_cpp` resolves DNS names, so compose service names work:

```yaml
    environment:
      ROS_DOMAIN_ID: "7"
      ROS_STATIC_PEERS: "sim;navigation"
```

`rmw_cyclonedds_cpp` turns the same variable into a Cyclone `<Peers>` list and sets
`ParticipantIndex` to `auto` with `MaxAutoParticipantIndex` 32. If you write a Cyclone XML file
by hand (`CYCLONEDDS_URI=file:///config/cyclonedds.xml`) with multicast off, set those two
yourself: in Cyclone DDS 0.10 (Jazzy) `ParticipantIndex` defaults to `none`, which makes unicast
discovery impossible, and `MaxAutoParticipantIndex` defaults to 9, about ten ROS processes per
address.

```xml
<CycloneDDS xmlns="https://cdds.io/config">
  <Domain Id="any">
    <General><AllowMulticast>false</AllowMulticast></General>
    <Discovery>
      <ParticipantIndex>auto</ParticipantIndex>
      <MaxAutoParticipantIndex>32</MaxAutoParticipantIndex>
      <Peers><Peer address="sim"/><Peer address="navigation"/></Peers>
    </Discovery>
  </Domain>
</CycloneDDS>
```

## Zenoh

`rmw_zenoh_cpp` needs a router; without one, nodes do not discover each other because Zenoh
multicast scouting is off by default. `ROS_AUTOMATIC_DISCOVERY_RANGE` and `ROS_STATIC_PEERS` are
ignored by `rmw_zenoh`. Install `ros-jazzy-rmw-zenoh-cpp` in the image (an `exec_depend` on
`rmw_zenoh_cpp`, see [dockerfile.md](dockerfile.md#dockerfile)).

With host networking, run one router per computer; nodes connect to `tcp/localhost:7447` by
default, so they need only `RMW_IMPLEMENTATION=rmw_zenoh_cpp`. On a bridge network, point the
nodes at the router's service name:

```yaml
x-zenoh: &zenoh
  image: ghcr.io/my-org/my_robot:jazzy
  networks: [ros]
  depends_on: [zenoh-router]
  environment:
    RMW_IMPLEMENTATION: rmw_zenoh_cpp
    ZENOH_CONFIG_OVERRIDE: 'mode="client";connect/endpoints=["tcp/zenoh-router:7447"]'

services:
  zenoh-router:
    image: ghcr.io/my-org/my_robot:jazzy
    command: ros2 run rmw_zenoh_cpp rmw_zenohd
    networks: [ros]
    environment:
      RMW_IMPLEMENTATION: rmw_zenoh_cpp
      # the default listens on IPv6 [::] only and exits on hosts without IPv6
      ZENOH_CONFIG_OVERRIDE: 'listen/endpoints=["tcp/0.0.0.0:7447"]'
  driver:
    <<: *zenoh
    command: ros2 launch my_robot_driver driver.launch.py

networks:
  ros: {}
```

- In `client` mode every message goes through the router; that is the simplest working layout
  for containers. To reach another computer's router, list its `tcp/<ip>:7447` in the router's
  `connect/endpoints`.
- If a node starts before the router, it keeps running and connects when the router appears.
- Zenoh shared memory is off by default; enabling it
  (`ZENOH_CONFIG_OVERRIDE='transport/shared_memory/enabled=true'`) across containers needs
  `ipc: host` or a shared tmpfs volume mounted at `/dev/shm`.

## Devices

- Pass stable paths: `/dev/serial/by-id/...` or a udev symlink, not `/dev/ttyUSB0`, which changes
  with plug order. Map it to a fixed name inside (`:/dev/my_robot_mcu`).
- `devices:` binds the node when the container starts. A device unplugged and replugged gets a new
  node; restart the container, or for hot-plug bind-mount `/dev` and allow the major number with
  `device_cgroup_rules` (for example `'c 188:* rmw'` for `ttyUSB`).
- Add the group that owns the device (`dialout` for serial, `video` for cameras) with
  `group_add:` when the container runs as a non-root user. Avoid `privileged: true`.

## Development container

```yaml
services:
  dev:
    build: {context: ., target: deps}
    image: my_robot:dev
    network_mode: host
    ipc: host
    environment: {ROS_DOMAIN_ID: "42"}
    volumes:
      - ./src:/ws/src
      - ws-build:/ws/build
      - ws-install:/ws/install
      - ws-log:/ws/log
    command: sleep infinity

volumes:
  ws-build:
  ws-install:
  ws-log:
```

```bash
docker compose up -d dev
docker compose exec dev bash -c 'colcon build --symlink-install'
docker compose exec dev bash -c 'source install/setup.bash && ros2 launch my_robot_bringup robot.launch.py'
```

Named volumes keep `build/` and `install/` between restarts, so only changed packages rebuild.

## Checks

```bash
docker compose config --quiet                     # the file parses
docker compose exec driver ros2 node list         # discovery: nodes from every service appear
docker compose exec driver ros2 topic hz /my_robot/joint_states   # data flows, not just discovery
docker compose exec driver printenv RMW_IMPLEMENTATION ROS_DOMAIN_ID
```

Discovery without data almost always means shared memory: check `ipc: host` and the UIDs.
