---
type: guide
name: Choose a ROS 2 middleware
summary: Which RMW to run under ROS 2 (Fast DDS, Cyclone DDS or rmw_zenoh), decided by machines, Wi-Fi, large data, containers, networks and robot SDKs; with the defaults per distro and how to switch and check.
tags: [ros2, middleware, rmw, dds, fast-dds, cyclone-dds, zenoh, wifi, multi-machine, docker, discovery]
question: Which ROS 2 middleware (RMW) should my robot use?
options: [fast-dds, cyclone-dds, rmw-zenoh]
recommendation: "Keep the default Fast DDS on one machine or a wired LAN; move the whole system to rmw_zenoh when nodes talk over Wi-Fi or across networks (Tier 1 from Kilted, so on Lyrical); use Cyclone DDS when the robot's SDK speaks it."
evidence: researched
last_verified: 2026-11-18
sources:
  - {url: "https://reps.openrobotics.org/rep-2000/", title: "REP 2000: ROS 2 Releases and Target Platforms", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/lyrical/Releases/lyrical/supported-platforms.html", title: Lyrical Luth supported platforms and middleware, accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/lyrical/ROS-Framework/middleware/About-Different-Middleware-Vendors.html", title: "ROS 2 docs: Different ROS 2 middleware vendors (Lyrical)", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/How-To-Guides/Working-with-multiple-RMW-implementations.html", title: "ROS 2 docs: Working with multiple RMW implementations", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Getting-Started-With-Ros2doctor.html", title: "ROS 2 docs: Using ros2doctor to identify issues", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/How-To-Guides/DDS-tuning.html", title: "ROS 2 docs: Addressing common DDS tuning issues", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Tutorials/Advanced/Improved-Dynamic-Discovery.html", title: "ROS 2 docs: Improved Dynamic Discovery", accessed: 2026-11-18}
  - {url: "https://github.com/ros2/rmw_zenoh", title: "rmw_zenoh README, rolling and jazzy branches", accessed: 2026-11-18}
  - {url: "https://github.com/ros2/rmw_fastrtps", title: "rmw_fastrtps README, jazzy and rolling branches", accessed: 2026-11-18}
  - {url: "https://fast-dds.docs.eprosima.com/en/latest/docker/shm_docker.html", title: "Fast DDS docs: Leveraging Fast DDS SHM in Docker deployments", accessed: 2026-11-18}
  - {url: "https://discourse.openrobotics.org/t/ros-2-alternative-middleware-report/33771", title: "Open Robotics Discourse: ROS 2 Alternative middleware report (2023-09-27)", accessed: 2026-11-18}
  - {url: "https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Domain-ID.html", title: "ROS 2 docs: The ROS_DOMAIN_ID", accessed: 2026-11-18}
---

# Choose a ROS 2 middleware

Which RMW, the layer that carries [ROS 2](../tools/ros2.md) messages between nodes, should your
robot run? For builders on Jazzy or Lyrical whose nodes must find each other on one or more
machines. The options: [Fast DDS](../software/fast-dds.md), [Cyclone DDS](../software/cyclone-dds.md)
and [rmw_zenoh](../software/rmw-zenoh.md).

## Short answer

- **One machine or a wired LAN:** keep the default, Fast DDS. Nothing to install or tune.
- **Wi-Fi, several networks, or a laptop driving a robot:** rmw_zenoh, Tier 1 on Kilted and Lyrical
  [1][2]. Jazzy has it untiered [1][8]: test it, or keep Fast DDS with its Discovery Server.
- **A robot SDK that speaks DDS**, as Unitree's speaks Cyclone DDS
  ([Unitree Go2](../robots/unitree-go2.md)): run that DDS in every node that talks to the robot.
- Whatever you choose, every node in the system runs the same RMW [3].

## Defaults per distro

| Distro | Default | Other Tier 1 RMWs | Source |
|---|---|---|---|
| Humble (to May 2027) | Fast DDS | Cyclone DDS, RTI Connext | [1] |
| Jazzy (to May 2029) | Fast DDS | Cyclone DDS, RTI Connext | [1] |
| Kilted | Fast DDS | Cyclone DDS, RTI Connext, rmw_zenoh | [1] |
| Lyrical (to May 2031) | Fast DDS | Cyclone DDS, RTI Connext, rmw_zenoh | [2] |

RTI Connext is Tier 1 except on arm64 [1][2]; Galactic alone defaulted to Cyclone DDS [1]. With
several RMWs installed and none chosen, Fast DDS wins, else the alphabetically first [3].

## What decides it

- **One machine or several.** DDS nodes discover everything on the subnet by multicast unless
  `ROS_AUTOMATIC_DISCOVERY_RANGE` says `LOCALHOST` or `OFF` [7]. rmw_zenoh stays inside one host
  until you link its routers [8].
- **Wi-Fi.** On lossy links, lost IP fragments fill the kernel's reassembly buffer and Linux holds
  them 30 s by default, so DDS traffic seems to hang. Use best-effort QoS for streams, or lower
  `net.ipv4.ipfrag_time` [6]. rmw_zenoh connects over TCP and turns multicast off [8]; the ROS core
  team chose Zenoh as its alternative middleware in 2023 [11].
- **Large data** (images, point clouds). On one host, Fast DDS uses shared memory by default [9];
  rmw_zenoh only after you enable it [8]. Between hosts, Fast DDS has a TCP `LARGE_DATA` mode [9]
  and Cyclone DDS needs larger kernel receive buffers [6]. Pack big arrays as primitives, as
  `PointCloud2` does, to cut serialisation cost [6].
- **Containers.** Fast DDS containers on the host network also need `--ipc=host`, or discovery
  works but data does not [10]. rmw_zenoh's optional shared memory needs `--ipc=host` or a shared
  tmpfs [8]. Container setup: [ops-docker-ci](../../skills/ops-docker-ci/SKILL.md).
- **Discovery across networks.** DDS multicast stays in one subnet; list remote hosts with
  `ROS_STATIC_PEERS` [7] or run the Fast DDS Discovery Server. rmw_zenoh links routers over TCP
  endpoints, and a laptop can join a robot's router as a client [8].
- **Vendor support.** A robot's own DDS fixes the choice. RTI Connext is commercial (with a research
  licence) and installed separately; RTI's microcontroller and safety-certified variants are not
  supported by ROS 2 [3].

## Options compared

| Option | Cost | Strengths | Limits | Best when |
|---|---|---|---|---|
| Fast DDS (`rmw_fastrtps_cpp`) | Free, Apache-2.0 [3] | Default, nothing to install; local shared memory; Discovery Server; TCP mode for large data [9] | Docker needs shared IPC [10]; Wi-Fi needs tuning [6] | One machine, wired LAN, most projects |
| Cyclone DDS (`rmw_cyclonedds_cpp`) | Free, EPL-2.0 [3] | Tier 1 in every current distro [1][2]; one XML sets interface and peers | Uses one network interface unless told; large messages need kernel tuning [6] | The robot's SDK speaks it; hosts with several NICs |
| rmw_zenoh (`rmw_zenoh_cpp`) | Free; Zenoh is EPL-2.0 [3] | No multicast; TCP; routers join networks; client mode [8] | Router per host; Tier 1 only from Kilted [1]; no DDS interop [3] | Wi-Fi, several networks, fleets on Lyrical |

Others: RTI Connext DDS (`rmw_connextdds`, above); GurumNetworks GurumDDS (`rmw_gurumdds_cpp`),
commercial, Tier 3 in Jazzy, not in Lyrical's table [1][2][3]; `rmw_fastrtps_dynamic_cpp`, Tier 2 [2].

## Switch and check

```bash
sudo apt install ros-jazzy-rmw-zenoh-cpp           # or ros-jazzy-rmw-cyclonedds-cpp
export RMW_IMPLEMENTATION=rmw_zenoh_cpp            # in every shell, launch host and service unit
ros2 daemon stop                                   # the CLI daemon keeps its old RMW
ros2 run rmw_zenoh_cpp rmw_zenohd                  # rmw_zenoh only: router, own terminal, per host
ros2 doctor --report                               # RMW MIDDLEWARE names the RMW in use
```

A stale daemon makes CLI tools fail, and an RMW that is not installed makes the node exit with an
error [4]. The report's RMW MIDDLEWARE section confirms the switch [5].

## All nodes must agree

- DDS vendors talk to each other only in limited cases, with no guarantee: use one ROS version and
  one RMW across the system [3].
- rmw_zenoh is not DDS [3], so it never sees DDS nodes, not even through zenoh-bridge-ros2dds [8].
- One `ROS_DOMAIN_ID` per system (default 0; pick from 0 to 101), and a different one for each
  robot sharing a network [12]. Match the discovery range too: a node set to `OFF` sees nobody [7].
- With rmw_zenoh, Humble and newer distros discover each other but silently drop messages [8].

## When the answer changes

- **Jazzy to Lyrical:** rmw_zenoh becomes Tier 1 [2], and Fast DDS moves from 2.14 to 3.6 [1][2],
  which renames some settings (see [Fast DDS](../software/fast-dds.md)).
- **A DDS robot joins a Zenoh system:** the robot's SDK wins, or you bridge at one node you write.
- **Many nodes but you must stay on DDS:** Fast DDS Discovery Server cuts discovery traffic.

## Sources

1. [REP 2000: ROS 2 Releases and Target Platforms](https://reps.openrobotics.org/rep-2000/), accessed 2026-11-18
2. [Lyrical Luth supported platforms and middleware](https://docs.ros.org/en/lyrical/Releases/lyrical/supported-platforms.html), accessed 2026-11-18
3. [ROS 2 docs: Different ROS 2 middleware vendors (Lyrical)](https://docs.ros.org/en/lyrical/ROS-Framework/middleware/About-Different-Middleware-Vendors.html), accessed 2026-11-18
4. [ROS 2 docs: Working with multiple RMW implementations](https://docs.ros.org/en/jazzy/How-To-Guides/Working-with-multiple-RMW-implementations.html), accessed 2026-11-18
5. [ROS 2 docs: Using ros2doctor to identify issues](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Getting-Started-With-Ros2doctor.html), accessed 2026-11-18
6. [ROS 2 docs: Addressing common DDS tuning issues](https://docs.ros.org/en/jazzy/How-To-Guides/DDS-tuning.html), accessed 2026-11-18
7. [ROS 2 docs: Improved Dynamic Discovery](https://docs.ros.org/en/jazzy/Tutorials/Advanced/Improved-Dynamic-Discovery.html), accessed 2026-11-18
8. [rmw_zenoh README, rolling and jazzy branches](https://github.com/ros2/rmw_zenoh), accessed 2026-11-18
9. [rmw_fastrtps README, jazzy and rolling branches](https://github.com/ros2/rmw_fastrtps), accessed 2026-11-18
10. [Fast DDS docs: Leveraging Fast DDS SHM in Docker deployments](https://fast-dds.docs.eprosima.com/en/latest/docker/shm_docker.html), accessed 2026-11-18
11. [Open Robotics Discourse: ROS 2 Alternative middleware report (2023-09-27)](https://discourse.openrobotics.org/t/ros-2-alternative-middleware-report/33771), accessed 2026-11-18
12. [ROS 2 docs: The ROS_DOMAIN_ID](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Domain-ID.html), accessed 2026-11-18
