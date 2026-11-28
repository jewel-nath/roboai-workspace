# Running the micro-ROS agent

Part of [fw-rtos-micro-ros](../SKILL.md). Checked on 2026-11-27 against `micro-ROS/micro-ROS-Agent`
`jazzy` (micro_ros_agent 5.0.2, which builds Micro XRCE-DDS Agent v2.4.3), the Micro XRCE-DDS Agent
v2.4.3 source (command-line parser, serial transport), `micro-ROS/docker` `jazzy`, the
`microros/micro-ros-agent` tags on Docker Hub, and `ros/rosdistro` (`jazzy`, `lyrical`, `humble`).
The recipes were not run.

## What it is

- A ROS 2 node that wraps the Micro XRCE-DDS Agent. Each MCU is a client; the agent creates the
  DDS participant, topics, publishers and subscribers on its behalf.
- It always speaks **Fast DDS** (it links `rmw_fastrtps_shared_cpp`), whatever
  `RMW_IMPLEMENTATION` says. A robot on a DDS middleware sees the MCU's topics; a robot on
  `rmw_zenoh_cpp` does not, because rmw_zenoh does not talk to DDS nodes
  ([choose a ROS 2 middleware](../../../wiki/guides/choose-a-ros2-middleware.md)).
- The **domain ID comes from the firmware** (`rcl_init_options_set_domain_id`, 0 when not set),
  not from `ROS_DOMAIN_ID` in the agent's environment.
- **No apt package.** No rosdistro release has `micro_ros_agent` (checked `jazzy`, `lyrical`,
  `humble`); `micro_ros_msgs` is released (`ros-jazzy-micro-ros-msgs`). Build it or use Docker.

## Build from source

Into the robot's own workspace, so one `setup.bash` covers the agent and the robot:

```bash
cd /home/robot/ros2_ws
git clone -b jazzy https://github.com/micro-ROS/micro-ROS-Agent.git src/micro-ROS-Agent
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -y        # brings ros-jazzy-micro-ros-msgs
colcon build --packages-up-to micro_ros_agent
source install/setup.bash
ros2 run micro_ros_agent micro_ros_agent --help
```

- The build downloads Micro XRCE-DDS Agent v2.4.3 from GitHub (a CMake superbuild), so the build
  machine needs network access. Robots without it: build in the image ([ops-docker-ci](../../ops-docker-ci/SKILL.md)).
- `micro_ros_setup`'s `create_agent_ws.sh` + `build_agent.sh` do the same in a separate workspace
  ([build-paths.md](build-paths.md)).
- Record the commit you built (`git -C src/micro-ROS-Agent rev-parse HEAD`).

## Run

```bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/my_robot_mcu -b 115200   # UART or USB-UART bridge
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/my_robot_mcu             # native USB CDC
ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888                           # Wi-Fi or Ethernet
ros2 run micro_ros_agent micro_ros_agent multiserial --devs "/dev/my_robot_mcu /dev/my_robot_mcu2" -b 115200
```

- Options: `-D`/`--dev`, `-b`/`--baudrate` (default 115200; `--baud` is not an option and is
  ignored), `-p`/`--port`, `-v` 0 to 6 (default 4; 6 prints every message). Other transports:
  `udp6`, `tcp4`, `tcp6`, `pseudoterminal`, `canfd`.
- The rate must match the firmware's UART on USB-UART bridges (CP210x, CH340, FTDI); native USB CDC
  (Teensy, Pico, STM32 USB, ESP32-S3 USB) ignores it.
- 8N1 serial carries at most baud / 10 bytes per second: 11 520 B/s at 115200, 92 160 B/s at 921600,
  before XRCE framing. Check the sum of message sizes times rates against that.
- The agent waits for a missing serial device ("Serial port not found ... waiting for connection")
  and reopens the port after a read error, so it survives MCU resets and replugging.
- A connecting MCU logs `session established` and `create_client` at the default verbosity.
- One agent can serve several UDP clients. Each MCU needs its own node name; set distinct client
  keys with `rmw_uros_options_set_client_key` if you want stable identities.

## Docker

```bash
docker run -it --rm -v /dev:/dev --privileged --net=host \
  microros/micro-ros-agent:jazzy serial --dev /dev/my_robot_mcu -b 115200
docker run -it --rm --net=host microros/micro-ros-agent:jazzy udp4 --port 8888
```

- Tags on Docker Hub (2026-11-27): `humble`, `jazzy`, `kilted`, `rolling`; amd64 and arm64. No
  `lyrical` tag yet. Pin a digest in deployments.
- The image builds the agent on `ros:jazzy` and runs on `ros:jazzy-ros-core` with
  `RMW_IMPLEMENTATION=rmw_fastrtps_cpp` and Fast DDS shared memory switched off
  (`MICROROS_DISABLE_SHM=1`), so processes outside the container receive its data over UDP.
- `-v /dev:/dev --privileged` is upstream's form: the container sees the device again after the
  MCU resets. `--device /dev/my_robot_mcu` exposes only the node present at start, and a reset MCU
  may come back under another node. `--privileged` gives the container every device; weigh that.
- The agent README lists a known issue: serial ports used by the agent inside Docker sometimes
  show heavy packet loss. Prefer the native build for serial links; Docker suits UDP.

## Start it with the robot

In the bringup launch file ([ops-bringup](../../ops-bringup/SKILL.md)):

```python
from launch_ros.actions import Node

micro_ros_agent = Node(
    package='micro_ros_agent', executable='micro_ros_agent', name='micro_ros_agent',
    arguments=['serial', '--dev', '/dev/my_robot_mcu', '-b', '115200'],
    respawn=True, respawn_delay=2.0, output='screen')
```

Arguments before `--ros-args` go to the agent's own parser, so the list form above works.

Or as its own unit, using the environment file from ops-bringup:

```ini
# /etc/systemd/system/my-robot-uros-agent.service
[Unit]
Description=micro-ROS agent for my_robot
Wants=network-online.target
After=network-online.target

[Service]
Type=exec
User=robot
ExecStart=/bin/bash -c 'source /etc/my_robot/env.sh && exec ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/my_robot_mcu -b 115200'
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
```

## Device name and permissions

- A udev rule gives the MCU a stable name and keeps ModemManager off it:
  `SUBSYSTEM=="tty", ATTRS{idVendor}=="<vid>", ATTRS{idProduct}=="<pid>", ATTRS{serial}=="<serial>", SYMLINK+="my_robot_mcu", ENV{ID_MM_DEVICE_IGNORE}="1"`.
  Finding the attributes and testing the rule: [ops-bringup udev](../../ops-bringup/references/udev.md).
  Serial-port details on Linux: [fw-serial-can](../../fw-serial-can/SKILL.md).
- The user running the agent is in `dialout`.
- Do not open the port with a serial monitor while the agent runs; only one process gets the data.

## Checks

```bash
ros2 node list                         # /my_robot_firmware once the MCU connects
ros2 topic list                        # its topics
ros2 topic info -v /cmd_vel            # QoS of both sides
ros2 topic hz /wheel_states
```

Restart the agent (`systemctl restart my-robot-uros-agent`, or kill the launch node) and confirm the
node and its rate come back within a few seconds, with the motors stopped meanwhile.
