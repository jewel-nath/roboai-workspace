# Releases: what a robot runs, and how it goes back

Part of [ops-fleet](../SKILL.md). A release is one immutable, versioned artifact that every robot
can install and any robot can return to. Written for ROS 2 Jazzy on Ubuntu 24.04 (`noble`).
Sources: ROS 2 docs "Building a custom deb package" (jazzy branch), bloom's Debian templates,
the aptly docs, the Docker Compose CLI reference (all read 2026-11-25).

## Pick one shape per fleet

| | Container image | Debian packages in your own apt repository |
|---|---|---|
| Built from | the multi-stage Dockerfile in [ops-docker-ci](../../ops-docker-ci/SKILL.md) | `bloom-generate rosdebian` per package |
| Version | git tag → image tag; robots run a **digest** | `<version>` in every `package.xml` |
| Install | digest in `.env`, `docker compose up -d --wait` | `apt install ros-jazzy-<pkg>=<version>-0noble` |
| Rollback | the previous digest | the previous version, downgrade allowed |
| Host needs | Docker Engine; ROS 2 only inside the image | ROS 2 Jazzy from apt on the host |
| Suits | most fleets; the image CI tested is the image that runs | small hosts without a container runtime |

**Not a release:** `rsync` of a workspace `install/` folder (what quick setups do). It has no
version, can stop half-copied, and a tree built with `--symlink-install` holds links into the
build machine's `src/` and `build/`, which do not exist on the robot. An `install/` built on
amd64 does not run on an arm64 robot. Use it on one bench robot, never across a fleet.

Whichever shape: write the version where the robot can report it. The health endpoint
([health.md](health.md)) and metrics ([observability.md](observability.md)) read
`/etc/my_robot/release`, which the rollout writes.

## Container images

Tag each image with the release version (`ghcr.io/my-org/my_robot:1.4.0`) in CI, and deploy the
digest CI printed (`docker/build-push-action` outputs `digest`), never `latest` or `jazzy`: a tag
can be moved, a digest cannot. The robot's compose project, `/opt/my_robot/compose.yaml`:

```yaml
services:
  robot:
    image: ${MY_ROBOT_IMAGE:?set in .env}
    network_mode: host
    ipc: host                       # Fast DDS shared memory, see ops-docker-ci compose.md
    restart: unless-stopped
    env_file: /etc/my_robot/robot.env   # identity, see identity-config.md
    volumes:
      - /etc/my_robot:/etc/my_robot:ro
      - /var/lib/my_robot:/var/lib/my_robot
      - /var/log/my_robot:/var/log/my_robot   # so bringup's log cleanup still applies
    environment:
      - ROS_LOG_DIR=/var/log/my_robot
    command: ros2 launch my_robot_bringup robot.launch.py
    healthcheck:                    # a 503 raises HTTPError, so the check exits non-zero
      test: ["CMD", "python3", "-c",
             "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/healthz', timeout=2)"]
      interval: 10s
      timeout: 5s
      start_period: 90s             # example: time the stack needs to come up; measure yours
      retries: 3
```

`/opt/my_robot/.env` (Compose reads `.env` from the project folder for `${...}`):

```bash
MY_ROBOT_IMAGE=ghcr.io/my-org/my_robot@sha256:<digest>
MY_ROBOT_RELEASE=1.4.0
```

Switching release by hand, the same steps the playbook in
[ansible-rollout.md](ansible-rollout.md) runs:

```bash
cd /opt/my_robot
cp .env .env.previous
sed -i 's|^MY_ROBOT_IMAGE=.*|MY_ROBOT_IMAGE=ghcr.io/my-org/my_robot@sha256:<new>|' .env
docker compose pull                     # download first; the switch is then only a restart
docker compose up -d --wait --wait-timeout 180   # exits non-zero if not healthy in time
# rollback
cp .env.previous .env && docker compose up -d --wait --wait-timeout 180
```

- There is no `docker compose rollback` command; rollback is the previous digest in `.env`.
- `--wait` waits for `healthy` only if the service has a `healthcheck`; without one it returns
  as soon as the container runs.
- Keep the previous image on disk until the new one is accepted. `docker image prune -a`
  removes every image no container uses, including the one you would roll back to.
- Robots pull with a read-only registry token (`docker login` once, at provisioning). Never put
  a token with push rights on a robot.

## Debian packages from your workspace

Bloom builds a `.deb` per package that installs into `/opt/ros/jazzy`, named
`ros-jazzy-<name-with-dashes>`, versioned `<package.xml version>-0noble`.

1. **One version for the whole workspace.** Bump every `package.xml` together
   (`catkin_prepare_release --version 1.4.0` from `python3-catkin-pkg`, or by hand).
2. **rosdep keys for your own packages**, so bloom can resolve them:

   ```yaml
   # /etc/ros/rosdep/my_robot.yaml
   my_robot_msgs:
     ubuntu: [ros-jazzy-my-robot-msgs]
   my_robot_driver:
     ubuntu: [ros-jazzy-my-robot-driver]
   ```

   ```bash
   echo "yaml file:///etc/ros/rosdep/my_robot.yaml" | sudo tee /etc/ros/rosdep/sources.list.d/50-my-robot.list
   rosdep update
   ```

3. **Build in dependency order, on the target architecture** (an arm64 runner or container):

   ```bash
   sudo apt install python3-bloom python3-rosdep fakeroot debhelper dh-python
   cd src/my_robot_msgs
   bloom-generate rosdebian --ros-distro jazzy
   fakeroot debian/rules binary     # writes ../ros-jazzy-my-robot-msgs_1.4.0-0noble_arm64.deb
   sudo apt install ../ros-jazzy-my-robot-msgs_1.4.0-0noble_arm64.deb   # before its dependants
   ```

4. **Publish with aptly** (MIT). Keep old versions in the repository: a version that is no longer
   published cannot be rolled back to.

   ```bash
   aptly repo create -distribution=noble -component=main my-robot      # once
   aptly repo add my-robot debs/1.4.0/
   aptly snapshot create my-robot-1.4.0 from repo my-robot
   aptly publish snapshot -architectures=arm64,amd64 my-robot-1.4.0    # first time; signs with GPG
   aptly publish switch noble my-robot-1.4.0                           # later releases
   ```

   Serve `<rootDir>/public` over HTTPS on `apt.fleet.example.com`. reprepro (GPL-2.0) is the
   older alternative.
5. **On the robot**, the repository and an exact version of every package in the release:

   ```text
   # /etc/apt/sources.list.d/my-robot.sources
   Types: deb
   URIs: https://apt.fleet.example.com
   Suites: noble
   Components: main
   Signed-By: /etc/apt/keyrings/my-robot.asc
   ```

   ```bash
   sudo apt update
   sudo apt install --allow-downgrades ros-jazzy-my-robot-bringup=1.4.0-0noble \
     ros-jazzy-my-robot-driver=1.4.0-0noble ros-jazzy-my-robot-msgs=1.4.0-0noble
   apt-cache policy ros-jazzy-my-robot-bringup   # installed and available versions
   ```

   Bloom writes dependencies between your packages without versions, so pinning only the top
   package can leave its dependencies at another release; list them all, as above.
   `--allow-downgrades` is what makes the same command a rollback.

- `sudo apt upgrade` on a robot also moves upstream ROS packages. Upgrade upstream ROS
  deliberately, as its own release, after a sync on the ROS 2 apt repository was tested; the ROS
  snapshot repository (`snapshots.ros.org/jazzy/<sync date>/ubuntu`, each sync kept at least six
  months) lets robots install exactly the sync you tested.
- Restart the services after an apt release (`systemctl restart my-robot.service`, unit from
  [ops-bringup](../../ops-bringup/SKILL.md)); installing files does not restart running nodes.
  The packages install into `/opt/ros/jazzy`, so `env.sh` sources only
  `/opt/ros/jazzy/setup.bash`; drop the workspace `install/setup.bash` line there.

## Checks

- `docker compose config --quiet` passes and `docker compose ps` shows the robot service
  `healthy`; `docker inspect --format '{{.Config.Image}}' <container>` shows the released
  digest (`{{.Image}}` is the local image ID, a different hash).
- Or `apt-cache policy` shows every release package at the released version.
- A rollback to the previous release, run on purpose on one robot, comes back healthy.
- `/etc/my_robot/release` and `/healthz` report the version you shipped.
