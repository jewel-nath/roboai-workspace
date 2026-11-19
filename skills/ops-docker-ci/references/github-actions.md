# GitHub Actions for a ROS 2 workspace

Workflows that build and test a colcon workspace and ship its image. Action versions checked
against the action repositories on 2026-11-18: `ros-tooling/setup-ros@v0.7`,
`ros-tooling/action-ros-ci@v0.4`, `actions/checkout@v7`, `actions/upload-artifact@v7`,
`docker/setup-qemu-action@v4`, `docker/setup-buildx-action@v4`, `docker/login-action@v4`,
`docker/metadata-action@v6`, `docker/build-push-action@v7`,
`EnricoMi/publish-unit-test-result-action@v2`. Check for newer majors before copying.

## Pick a path

| Path | What it does | Use it for |
|---|---|---|
| [action-ros-ci](#package-ci-with-action-ros-ci) | rosdep, `colcon build`, `colcon test`, `colcon test-result` in one step | Every repository with ROS packages; the default |
| [Image workflow](#image-workflow) | Builds the Dockerfile, runs tests in the build stage, pushes the runtime image | Repositories that ship a container to the robot |
| [industrial_ci](#industrial_ci) | Runs its own Docker container per configuration; extra checks (prerelease, ABI, clang-tidy) | Wide matrices or ROS-Industrial style checks |

## Package CI with action-ros-ci

`.github/workflows/ros-ci.yml`:

```yaml
name: ros-ci
on:
  pull_request:
  push:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read
  checks: write          # test report (publish-unit-test-result)
  pull-requests: write   # test report comment

jobs:
  build-and-test:
    runs-on: ubuntu-24.04
    strategy:
      fail-fast: false
      matrix:
        include:
          - ros_distro: jazzy
            image: rostooling/setup-ros-docker:ubuntu-noble-ros-jazzy-ros-base-latest
          - ros_distro: lyrical
            image: rostooling/setup-ros-docker:ubuntu-resolute-ros-lyrical-ros-base-latest
    container:
      image: ${{ matrix.image }}
    steps:
      - uses: ros-tooling/action-ros-ci@v0.4
        id: ros_ci
        with:
          target-ros2-distro: ${{ matrix.ros_distro }}
          package-name: my_robot_description my_robot_driver my_robot_bringup
      - uses: actions/upload-artifact@v7
        if: always()
        with:
          name: colcon-logs-${{ matrix.ros_distro }}
          path: ${{ steps.ros_ci.outputs.ros-workspace-directory-name }}/log
      - uses: EnricoMi/publish-unit-test-result-action@v2
        if: always()
        with:
          check_name: tests (${{ matrix.ros_distro }})
          files: |
            ${{ steps.ros_ci.outputs.ros-workspace-directory-name }}/build/*/test_results/**/*.xml
            ${{ steps.ros_ci.outputs.ros-workspace-directory-name }}/build/*/pytest.xml
```

How it behaves (from the action's source):

- It creates a workspace `ros_ws`, imports the repository at the triggering commit, runs
  `rosdep install`, `colcon build` and `colcon test --event-handlers=console_direct+`, then
  `colcon test-result --all` (shown, never fails) and `colcon test-result --verbose`, whose
  non-zero exit fails the job. No `actions/checkout` step is needed.
- The `rostooling/setup-ros-docker` images carry colcon, rosdep and vcs; the `-ros-base-` tags add
  the ROS binaries, so runs start faster. Each ROS distro needs its Ubuntu: Jazzy `noble`, Lyrical
  `resolute`, Humble `jammy`.
- Useful inputs: `package-name` (space separated; empty builds everything),
  `vcs-repo-file-url` (a `.repos` file of source dependencies), `rosdep-skip-keys`,
  `extra-cmake-args`, `colcon-extra-args`, `skip-tests`, `import-token` (a PAT, from
  `${{ secrets.NAME }}`, for private repositories).
- Without a container, run `ros-tooling/setup-ros@v0.7` with
  `required-ros-distributions: jazzy` first; its README recommends a container because
  `apt-get update` on bare runners is flaky.

The test report step is optional; `colcon test-result --verbose` in the log already names each
failure. On pull requests from forks the token is read-only and the report step cannot write
checks; keep it `if: always()` and do not switch to `pull_request_target` to get write access.

## Image workflow

`.github/workflows/image.yml`: build the `build` stage, test it, and push a multi-arch runtime
image from `main` and from version tags. The Dockerfile is the one in
[dockerfile.md](dockerfile.md#dockerfile).

```yaml
name: image
on:
  pull_request:
  push:
    branches: [main]
    tags: ["v*"]

permissions:
  contents: read
  packages: write        # push to ghcr.io with GITHUB_TOKEN

jobs:
  image:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v7
      - uses: docker/setup-qemu-action@v4
      - uses: docker/setup-buildx-action@v4

      - name: Build the build stage
        uses: docker/build-push-action@v7
        with:
          context: .
          target: build
          load: true
          tags: my_robot:ci
          cache-from: type=gha,scope=my_robot
          cache-to: type=gha,mode=max,scope=my_robot

      - name: Test
        run: |
          mkdir -p test-results
          docker run --rm -v "$PWD/test-results:/out" my_robot:ci bash -c '
            source install/setup.bash
            colcon test --event-handlers console_direct+
            colcon test-result --result-files-only | xargs -r cp --parents -t /out
            colcon test-result --verbose'

      - uses: actions/upload-artifact@v7
        if: always()
        with:
          name: test-results
          path: test-results

      - uses: docker/login-action@v4
        if: github.event_name != 'pull_request'
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - id: meta
        uses: docker/metadata-action@v6
        with:
          images: ghcr.io/my-org/my_robot      # lowercase; github.repository may not be
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha

      - name: Push the runtime image
        if: github.event_name != 'pull_request'
        uses: docker/build-push-action@v7
        with:
          context: .
          target: runtime
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: |
            type=gha,scope=my_robot
            type=gha,scope=my_robot-runtime
          cache-to: type=gha,mode=max,scope=my_robot-runtime
```

- `load: true` works for one platform only; the multi-platform step must `push`.
- `type=gha` caches layers in the GitHub Actions cache, shared by `scope`. GitHub evicts old
  entries under its own size limits; a cold cache just means a full build.
- The arm64 half runs under QEMU and compiles slowly. For large workspaces, build each platform on
  its own runner (`ubuntu-24.04` and `ubuntu-24.04-arm`), push by digest, and join them with
  `docker buildx imagetools create`; Docker's "Multi-platform image" CI guide has the pattern.
- Registry names must be lowercase. `github.repository` keeps the owner's capitals, so write the
  image name out or lowercase it.

## industrial_ci

```yaml
jobs:
  industrial_ci:
    runs-on: ubuntu-24.04
    strategy:
      fail-fast: false
      matrix:
        env:
          - {ROS_DISTRO: jazzy, ROS_REPO: main}
          - {ROS_DISTRO: jazzy, ROS_REPO: testing}
          - {ROS_DISTRO: lyrical, ROS_REPO: main}
    steps:
      - uses: actions/checkout@v7
      - uses: ros-industrial/industrial_ci@master   # pin a commit SHA; tag 0.10.0 predates Jazzy
        env: ${{ matrix.env }}
```

- It picks the Ubuntu release from `ROS_DISTRO` and runs everything in Docker, so the runner's
  Ubuntu version does not matter.
- `ROS_REPO` defaults to `testing` (the ROS shadow-fixed repository, packages before they sync);
  `main` is what users install. Testing both catches upstream breakage early.
- Other variables: `UPSTREAM_WORKSPACE` (source dependencies), `DOCKER_IMAGE` (your own base
  image), `CCACHE_DIR` (with `actions/cache`), `AFTER_SCRIPT`. See its `doc/index.rst`.

## Tests that touch the ROS graph

- Hosted runners are separate VMs, and each job container gets its own Docker network, so jobs do
  not see each other's topics. On self-hosted runners that run jobs side by side they do.
- Isolate them with `ament_add_ros_isolated_gtest` and `ament_add_ros_isolated_pytest_test` from
  `ament_cmake_ros`, which pick a free `ROS_DOMAIN_ID` per test, or give each job its own
  `ROS_DOMAIN_ID` in `env:`.
- Give launch tests explicit timeouts; a node that never starts otherwise hangs the job until the
  workflow timeout. Set `timeout-minutes:` on the job too.

## Secrets and permissions

- Secrets come only from the repository or organisation secret store, read as
  `${{ secrets.NAME }}`. Never write a token, password or key into a workflow, a Dockerfile, a
  `.repos` file, or a build argument.
- Pass secrets to the image build with `build-push-action`'s `secrets:` (for example
  `git_token=${{ secrets.PRIVATE_REPO_TOKEN }}`) and read them with `RUN --mount=type=secret`;
  see [dockerfile.md](dockerfile.md#private-sources-and-secrets).
- Set `permissions:` to the least each workflow needs. `GITHUB_TOKEN` with `packages: write` is
  enough for `ghcr.io`; another registry needs its own token secret.
- Pull requests from forks get no secrets. `actions/checkout@v7` refuses to check out fork code
  under `pull_request_target` unless told to; leave that guard on.
- Pin third-party actions to a full commit SHA when the repository's policy asks for it; GitHub's
  security hardening guide recommends it.
