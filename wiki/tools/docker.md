---
type: tool
name: Docker
summary: Container runtime for shipping a tested ROS 2 image to a robot; Docker Engine (Apache-2.0, from Moby) on Linux runs the official ros images for Humble to Lyrical on amd64 and arm64. Docker Desktop is a separate VM-based product with paid terms for larger companies.
tags: [docker, docker-engine, moby, docker-desktop, compose, containers, ros-images, nvidia-container-toolkit, dds, real-time, deployment]
kind: tool
area: ros2
support: documented
license: Apache-2.0
links: {repo: "https://github.com/moby/moby", docs: "https://docs.docker.com", site: "https://www.docker.com"}
version: {tested: , latest: 29.10.1, as_of: 2026-11-25}
platforms: [linux]
agent_access: cli
registry:
evidence: researched
last_verified: 2026-11-25
sources:
  - {url: "https://docs.docker.com/desktop/setup/install/linux/", title: "Docker docs: Install Docker Desktop on Linux", accessed: 2026-11-25}
  - {url: "https://docs.docker.com/engine/install/ubuntu/", title: "Docker docs: Install Docker Engine on Ubuntu", accessed: 2026-11-25}
  - {url: "https://github.com/moby/moby", title: "moby/moby repository: LICENSE and release tags", accessed: 2026-11-25}
  - {url: "https://github.com/osrf/docker_images", title: "osrf/docker_images: README, ros/manifest.yaml and Dockerfiles behind the ros images", accessed: 2026-11-25}
  - {url: "https://docs.docker.com/reference/cli/docker/container/run/", title: "Docker docs: docker container run reference", accessed: 2026-11-25}
  - {url: "https://docs.docker.com/engine/containers/resource_constraints/", title: "Docker docs: Resource constraints, real-time scheduler", accessed: 2026-11-25}
  - {url: "https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html", title: NVIDIA Container Toolkit installation guide, accessed: 2026-11-25}
  - {url: "https://fast-dds.docs.eprosima.com/en/latest/docker/shm_docker.html", title: "Fast DDS docs: Leveraging Fast DDS SHM in Docker deployments", accessed: 2026-11-25}
---

# Docker

Docker runs each part of a robot's software in a container built from an image, so the robot runs
what passed CI. On a Linux robot use **Docker Engine**, released from the Apache-2.0 Moby repository
(newest 29.10.1) [2][3]. **Docker Desktop** (a VM; the way on Windows and macOS) is free only
below 250 employees and USD 10 million yearly revenue; larger firms and governments pay [1].
Dockerfiles, Compose and CI: the [ops-docker-ci skill](../../skills/ops-docker-ci/SKILL.md).

## When to use it

- Ship one image per robot release and roll back by tag; Compose starts the containers together [2].
- The official `ros` images give `ros-core`, `ros-base` and `perception` for Humble, Jazzy, Kilted,
  Lyrical and Rolling on amd64 and arm64; `osrf/ros` adds `desktop`, `desktop-full` and
  `simulation`, amd64 only [4]. All are Ubuntu plus ROS, with no CUDA [4].
- Jetson: [jetson-containers](jetson-containers.md). No containers: [Pixi](pixi.md) or apt
  ([ROS 2](ros2.md)); see [Choose a deployment method](../guides/choose-a-deployment-method.md).

## Setup

Ubuntu 24.04 with Jazzy, after adding Docker's apt repository as the install guide shows [2]:

```bash
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
docker run --rm ros:jazzy-ros-base-noble printenv ROS_DISTRO      # prints jazzy
```

Engine packages cover Ubuntu 22.04 to 26.10 on amd64, arm64, armhf, s390x and ppc64le;
`get.docker.com` is for testing only [2]. GPU: install the NVIDIA Container Toolkit (1.20.2), run
`sudo nvidia-ctk runtime configure --runtime=docker`, restart Docker [7], use `--gpus all` [5].
On one robot computer run each ROS 2 container with `--network host --ipc host` [8]; then
`docker exec <name> ros2 topic list` shows the host's topics. Devices: `--device /dev/<path>` [5].
Real-time: `--cap-add=sys_nice --ulimit rtprio=99`, plus `--cpu-rt-runtime` for a budget [6].

## Traps

- **Docker Desktop on the robot.** A VM sits between containers and host, Linux packages are amd64
  only, and beside Engine it fights over ports and switches the CLI to its `desktop-linux` context
  [1]. Use Engine on robots; `docker context use default` switches back.
- **Nodes listed, no data.** With `--network host` alone, Fast DDS sees one host but cannot reach
  the containers' separate shared memory; add `--ipc host` to every container [8].
- **USB device replugged.** `--device` binds at creation and is unsafe for devices that come and
  go: allow its major number with `--device-cgroup-rule` and recreate the node from udev, or
  restart [5]. `--privileged` grants every device and capability and is no sandbox [5].
- **Real-time flags fail at start.** `--cpu-rt-runtime` needs `CONFIG_RT_GROUP_SCHED` in the
  kernel (`/sys/fs/cgroup/cpu.rt_runtime_us` exists) and the daemon flag; bad values can make the
  host unusable [6]. Check `ulimit -r` inside the container.
- **Open ports, moving tags.** Ports published with `-p` bypass ufw and firewalld rules [2].
  `ros:latest` is Lyrical [4]: pin `ros:jazzy-ros-base-noble` or a digest.

## Alternatives

Podman, which NVIDIA's toolkit supports through CDI [7]; Pixi and jetson-containers (above).

## Sources

1. [Docker docs: Install Docker Desktop on Linux](https://docs.docker.com/desktop/setup/install/linux/), accessed 2026-11-25
2. [Docker docs: Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/), accessed 2026-11-25
3. [moby/moby repository: LICENSE and release tags](https://github.com/moby/moby), accessed 2026-11-25
4. [osrf/docker_images: README, ros/manifest.yaml and Dockerfiles behind the ros images](https://github.com/osrf/docker_images), accessed 2026-11-25
5. [Docker docs: docker container run reference](https://docs.docker.com/reference/cli/docker/container/run/), accessed 2026-11-25
6. [Docker docs: Resource constraints, real-time scheduler](https://docs.docker.com/engine/containers/resource_constraints/), accessed 2026-11-25
7. [NVIDIA Container Toolkit installation guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html), accessed 2026-11-25
8. [Fast DDS docs: Leveraging Fast DDS SHM in Docker deployments](https://fast-dds.docs.eprosima.com/en/latest/docker/shm_docker.html), accessed 2026-11-25
