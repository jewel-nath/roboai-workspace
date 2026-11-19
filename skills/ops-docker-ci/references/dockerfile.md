# Multi-stage Dockerfile for a colcon workspace

A Dockerfile for a workspace laid out as `./src/<packages>`, written for ROS 2 Jazzy and checked
against `osrf/docker_images` (2026-11-14) and the `ros` library file on Docker Hub (2026-11-18).
Change the distro with `--build-arg ROS_DISTRO=lyrical`.

## Layout

```text
my_robot_ws/
├── .dockerignore
├── .gitattributes          # *.sh text eol=lf
├── Dockerfile
├── docker/ros_entrypoint.sh
└── src/
    ├── my_robot_description/
    ├── my_robot_driver/
    └── my_robot_bringup/
```

## Stages

| Stage | From | Holds | Rebuilds when |
|---|---|---|---|
| `manifests` | `ros-base` | only `package.xml` and `COLCON_IGNORE` files | any file in `src/` changes (cheap) |
| `deps` | `ros-base` | build, test and exec dependencies from rosdep | a `package.xml` changes |
| `build` | `deps` | sources, `build/`, `install/` | any source file changes |
| `runtime` | `ros-core` | exec dependencies and `install/` only, non-root user | a manifest or `install/` changes |

The `manifests` stage is the cache trick: Docker `COPY` of a glob flattens folders, so instead the
stage copies all of `src/`, keeps only the manifests, and later stages copy that result. BuildKit
compares the copied files by content, so a source edit that leaves every `package.xml` untouched
reuses the `deps` layer.

## Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
ARG ROS_DISTRO=jazzy

# Keep only the package manifests, so the dependency layer survives source edits.
FROM ros:${ROS_DISTRO}-ros-base AS manifests
COPY src /ws/src
RUN mkdir /manifests && cd /ws \
 && find src \( -name package.xml -o -name COLCON_IGNORE \) -exec cp --parents -t /manifests {} +

# Build, test and exec dependencies of every package.
FROM ros:${ROS_DISTRO}-ros-base AS deps
WORKDIR /ws
COPY --from=manifests /manifests/src src
RUN apt-get update \
 && rosdep update --rosdistro "$ROS_DISTRO" \
 && rosdep install --from-paths src --ignore-src -y \
 && rm -rf /var/lib/apt/lists/*

FROM deps AS build
COPY src src
RUN . "/opt/ros/$ROS_DISTRO/setup.sh" \
 && colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release --event-handlers console_direct+

# Runtime: no compilers, no sources, only what the packages need to run.
FROM ros:${ROS_DISTRO}-ros-core AS runtime
COPY --from=manifests /manifests/src /tmp/manifests/src
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3-rosdep \
 && rosdep init && rosdep update --rosdistro "$ROS_DISTRO" \
 && rosdep install --from-paths /tmp/manifests/src --ignore-src -y -t exec \
 && rm -rf /var/lib/apt/lists/* /tmp/manifests

# Ubuntu 24.04 and later images already give UID 1000 to "ubuntu"; free it first.
ARG USERNAME=ros
ARG UID=1000
RUN if id -u ubuntu >/dev/null 2>&1; then userdel ubuntu && rm -rf /home/ubuntu; fi \
 && useradd -m -u "$UID" -s /bin/bash "$USERNAME"

COPY --from=build /ws/install /ws/install
COPY --chmod=0755 docker/ros_entrypoint.sh /ros_entrypoint.sh
USER $USERNAME
WORKDIR /ws
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["ros2", "launch", "my_robot_bringup", "robot.launch.py"]
```

Notes on the choices:

- `ros-base` already has colcon, rosdep (initialised), vcstool, `build-essential` and git, so the
  build stages install nothing by hand. Its rosdep cache dates from when the image was built,
  hence `rosdep update` before `rosdep install`.
- `ARG ROS_DISTRO` before the first `FROM` only feeds `FROM` lines. Inside stages `$ROS_DISTRO`
  comes from the `ENV ROS_DISTRO` the official images set.
- `rosdep install -t exec` in the runtime stage installs only run dependencies. Without it the
  runtime image starts but fails at launch with missing packages (`xacro`,
  `robot_state_publisher`, Python modules).
- **The RMW is a dependency too.** If the robot uses Cyclone DDS or Zenoh, put
  `<exec_depend>rmw_cyclonedds_cpp</exec_depend>` (or `rmw_zenoh_cpp`) in the bringup package's
  `package.xml`, so rosdep installs it into the runtime image. Fast DDS ships with the binaries.
- Release builds: add `-DCMAKE_BUILD_TYPE=RelWithDebInfo` instead when you need backtraces.

## Entrypoint

`docker/ros_entrypoint.sh` (the base image has its own, but it sources only `/opt/ros`):

```bash
#!/bin/bash
set -e
source "/opt/ros/$ROS_DISTRO/setup.bash"
source /ws/install/setup.bash
exec "$@"
```

`exec` replaces the shell, so `ros2 launch` runs as PID 1 and receives the signal from
`docker stop`. Keep the file LF-only: a CRLF checkout on Windows fails with
`/bin/bash^M: bad interpreter`. Add `*.sh text eol=lf` to `.gitattributes`.

## .dockerignore

```text
.git
build/
install/
log/
**/__pycache__/
**/*.pyc
*.bag
*.mcap
```

Without it, a local `build/` or a large bag goes into every build context upload.

## Build and run

```bash
docker build --target runtime -t my_robot:jazzy .
docker run --rm my_robot:jazzy ros2 pkg executables my_robot_bringup
docker build --target runtime --build-arg ROS_DISTRO=lyrical -t my_robot:lyrical .
```

Check the cache works: edit a `.cpp` file, rebuild, and the `deps` steps must print `CACHED`.

## Tests in the image

Run the tests in the `build` stage image, where sources and `build/` exist:

```bash
docker build --target build -t my_robot:build .
docker run --rm my_robot:build bash -c \
  'source install/setup.bash && colcon test --event-handlers console_direct+ && colcon test-result --verbose'
```

`colcon test` exits 0 even when tests fail unless you pass `--return-code-on-test-failure`;
`colcon test-result` exits 1 on any failure or error, so keep it last. Result files are in
`build/<pkg>/test_results/<pkg>/*.xml` (ament_cmake) and `build/<pkg>/pytest.xml` (ament_python).

## Faster rebuilds (optional)

ccache through a BuildKit cache mount keeps compiler output between local builds:

```dockerfile
FROM deps AS build
RUN apt-get update && apt-get install -y --no-install-recommends ccache \
 && rm -rf /var/lib/apt/lists/*
COPY src src
RUN --mount=type=cache,target=/root/.cache/ccache \
    . "/opt/ros/$ROS_DISTRO/setup.sh" \
 && colcon build --event-handlers console_direct+ --cmake-args -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_C_COMPILER_LAUNCHER=ccache -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
```

Cache mounts live in the local builder. On hosted CI runners they start empty every run; the
layer cache (`type=gha`, see [github-actions.md](github-actions.md)) is what carries over.

## Development image

For editing on the host and building in the container, use the `deps` stage with the sources
bind-mounted (compose service in [compose.md](compose.md#development-container)):

```bash
docker build --target deps -t my_robot:dev .
docker run --rm -it --network host --ipc host -v "$PWD/src:/ws/src" my_robot:dev \
  bash -c 'colcon build --symlink-install && bash'
```

`--symlink-install` links Python files and launch/config files from `src/`, so edits apply
without rebuilding; C++ still needs `colcon build`. Do not ship this image.

## Private sources and secrets

Never pass a token with `ARG` or `ENV`: both stay in the image metadata (`docker history`), and
`mode=max` layer caches export the build stages too.

1. **Preferred: fetch private repos before the build.** In CI, check them out into `src/` with a
   token from the secret store (`actions/checkout` with `repository:` and `token:`), then build.
   The Dockerfile never sees a credential.
2. **If the build must fetch them,** mount the secret for one `RUN`; it is not stored in a layer.
   Remove the token from the clone's remote in the same `RUN`, or it stays in `.git/config`:

```dockerfile
RUN --mount=type=secret,id=git_token \
    url=https://github.com/my-org/my_robot_private.git \
 && git clone "https://x-access-token:$(cat /run/secrets/git_token)@${url#https://}" src/my_robot_private \
 && git -C src/my_robot_private remote set-url origin "$url"
```

```bash
docker build --secret id=git_token,env=GIT_TOKEN --target runtime -t my_robot:jazzy .
```

Put that `RUN` in the `manifests` stage (with `WORKDIR /ws`, before the `find`), so rosdep sees
the private manifests, and add `COPY --from=manifests /ws/src/my_robot_private src/my_robot_private`
to the `build` stage.

For SSH keys: `RUN --mount=type=ssh git clone git@github.com:my-org/my_robot_private.git ...` with
`docker build --ssh default`. In GitHub Actions the same goes through `docker/build-push-action`'s
`secrets:` and `ssh:` inputs, fed from `${{ secrets.NAME }}`.

## Pinning the base image

- Always name the distro: `ros:latest` points at Lyrical (Ubuntu 26.04) since that release.
- `ros:jazzy-ros-base-noble` also pins the Ubuntu release.
- For reproducible builds pin a digest, `FROM ros:jazzy-ros-base-noble@sha256:<digest>`, and let
  Dependabot or Renovate raise the digest updates; otherwise `docker build --pull` picks up the
  regular rebuilds of the official images.
