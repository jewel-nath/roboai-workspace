# GPU, display and ARM64 images

Running RViz, rqt and Gazebo in containers, giving perception containers a GPU, and building for
ARM64 robot computers. Sources: NVIDIA Container Toolkit install guide and "Specialized
configurations with Docker" (checked 2026-11-18), Docker docs on Compose GPU support, the `osrf/ros`
tags on Docker Hub (2026-11-18) and `dusty-nv/jetson-containers` (2026-10-13).

## NVIDIA GPU

Host setup, once (Ubuntu, from NVIDIA's install guide):

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
  | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
  | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker   # writes /etc/docker/daemon.json
sudo systemctl restart docker
docker run --rm --gpus all ubuntu nvidia-smi          # must list the GPU
```

The host needs the NVIDIA driver; the container does not. Old guides use `apt-key` and a
per-distribution list URL; both are gone, and they skip the `nvidia-ctk runtime configure` step.

Compose (the `capabilities` field is required):

```yaml
services:
  perception:
    image: ghcr.io/my-org/my_robot_perception:jazzy
    network_mode: host
    ipc: host
    environment:
      NVIDIA_DRIVER_CAPABILITIES: compute,utility,graphics
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all          # or device_ids: ["0"]; not both
              capabilities: [gpu]
```

`NVIDIA_DRIVER_CAPABILITIES` defaults to `compute,utility`: enough for CUDA and `nvidia-smi`, not
for OpenGL. RViz and Gazebo need `graphics` (or `display`, or `all`). The value replaces the
default, so list everything you need.

Intel and AMD GPUs need no toolkit: pass `/dev/dri` (`devices: [/dev/dri]`) and give a non-root
container user the host's `video` and `render` groups. The `render` GID differs between hosts and
may not exist in the image, so pass it as a number: `group_add: [video, "<GID>"]` with the GID
from `getent group render` on the host.

## X11 display

```bash
xhost +SI:localuser:"$(id -un)"     # let your user's containers draw; undo with xhost -SI:...
docker run --rm -it --network host --ipc host \
  -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  --user "$(id -u):$(id -g)" \
  osrf/ros:jazzy-desktop rviz2
```

```yaml
services:
  rviz:
    image: my_robot_desktop:jazzy
    network_mode: host
    ipc: host
    user: "1000:1000"                 # the host user's UID:GID, to match the xhost rule
    environment:
      DISPLAY: ${DISPLAY}
      NVIDIA_DRIVER_CAPABILITIES: all # only with the GPU reservation above
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix:ro
    command: rviz2 -d /ws/install/my_robot_description/share/my_robot_description/rviz/view.rviz
```

- `xhost +SI:localuser:<name>` admits one local user. `xhost +` or `xhost +local:` admits every
  local process or container; avoid them on shared machines.
- The container user must match the admitted user, hence `--user`. A container running as root
  needs `xhost +SI:localuser:root`.
- Without a GPU, RViz and Gazebo fall back to software rendering (`LIBGL_ALWAYS_SOFTWARE=1`
  forces it); expect low frame rates with large point clouds.

## Wayland desktops

Ubuntu 24.04 defaults to Wayland but runs XWayland, so `DISPLAY` is set and the X11 recipe above
works unchanged for RViz and Gazebo. Native Wayland is optional: mount
`$XDG_RUNTIME_DIR/$WAYLAND_DISPLAY` into the container, set `WAYLAND_DISPLAY`,
`XDG_RUNTIME_DIR` and `QT_QPA_PLATFORM=wayland`, and install the Qt Wayland plugin
(`qtwayland5` for Jazzy's Qt 5; Lyrical uses Qt 6, `qt6-wayland`).

## Desktop images

`osrf/ros:jazzy-desktop` (RViz, rqt, demos) and `osrf/ros:jazzy-desktop-full` are published for
amd64 only. For a desktop image on ARM64, build it:

```dockerfile
FROM ros:jazzy-ros-base
RUN apt-get update && apt-get install -y --no-install-recommends ros-jazzy-desktop \
 && rm -rf /var/lib/apt/lists/*
```

Keep GUI tools in a separate image or service from the robot's runtime image: the runtime image
stays small and has no display dependencies.

## ARM64 images (Raspberry Pi, other arm64 boards)

The `ros:` library images are multi-arch (amd64 and arm64), so the Dockerfile needs no change.

```bash
docker run --privileged --rm tonistiigi/binfmt --install arm64    # QEMU, once per host
docker buildx create --name multi --use                            # a builder that can do multi-platform
docker buildx build --platform linux/arm64 --target runtime -t my_robot:arm64 --load .
docker run --rm --platform linux/arm64 my_robot:arm64 uname -m      # aarch64
docker buildx build --platform linux/amd64,linux/arm64 --target runtime \
  -t ghcr.io/my-org/my_robot:jazzy --push .
```

- Emulated compiling is slow. For large C++ workspaces build arm64 natively: on the robot, on an
  arm64 machine, or on GitHub's `ubuntu-24.04-arm` runners (see
  [github-actions.md](github-actions.md#image-workflow)).
- `--load` handles one platform with the classic image store; a multi-platform build must
  `--push` (or the Docker Engine must use the containerd image store).
- Install Python libraries from apt (`python3-numpy`), not pip: on Ubuntu 24.04 pip refuses
  system installs (externally managed environment), and wheels may not exist for arm64.

## Jetson

On Jetson use images built for its L4T/JetPack release, from NVIDIA's Isaac ROS environment or
`dusty-nv/jetson-containers`; the plain arm64 `ros:` images run there but without the CUDA and
TensorRT stack. jetson-containers builds ROS from source, so add ROS packages from source, not
with `apt`.
