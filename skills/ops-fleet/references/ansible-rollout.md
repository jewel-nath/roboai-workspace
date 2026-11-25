# Rolling out a release with Ansible

Part of [ops-fleet](../SKILL.md). Ansible runs from one control machine over SSH (through the
VPN, [remote-access.md](remote-access.md)); robots need only SSH and Python 3, which Ubuntu
has. ansible-core is GPL-3.0-or-later; it runs on your machine and is not shipped to robots.
Checked against the Ansible docs "Controlling playbook execution", "Error handling in
playbooks" and "Blocks" (latest, read 2026-11-25).

## Layout

```text
fleet-ops/                     # its own git repository
  ansible.cfg
  inventory/fleet.yml
  inventory/group_vars/all/release.yml    # the release being rolled out
  inventory/group_vars/all/vault.yml      # ansible-vault encrypted
  inventory/host_vars/robot-01.yml        # identity, overlay, calibration refs
  templates/env.sh.j2  templates/robot.env.j2  templates/robot.yaml.j2  templates/env.j2
  playbooks/provision.yml  playbooks/status.yml  playbooks/rollout.yml
```

```yaml
# inventory/fleet.yml - names resolve on the VPN
all:
  vars:
    ansible_user: ops
    compose_dir: /opt/my_robot
  children:
    canary:
      hosts:
        robot-01:
    fleet:
      hosts:
        robot-02:
        robot-03:
```

```yaml
# inventory/group_vars/all/release.yml
release_version: "1.4.0"
release_image: ghcr.io/my-org/my_robot@sha256:<digest from CI>
```

```jinja
{# templates/env.j2 -> /opt/my_robot/.env #}
MY_ROBOT_IMAGE={{ release_image }}
MY_ROBOT_RELEASE={{ release_version }}
```

`provision.yml` renders `env.sh` and `robot.env`, the parameter overlay and secrets from
[identity-config.md](identity-config.md), installs the compose project from
[releases.md](releases.md) with a first `.env` and `/etc/my_robot/release`, and logs in to the
registry with the read-only token; run it whenever a robot's `host_vars` change.

## Status of the fleet

```yaml
# playbooks/status.yml - which robots answer, are healthy, and run which release
- name: Fleet status
  hosts: all
  gather_facts: false
  tasks:
    - name: Ask the health endpoint on the robot
      ansible.builtin.uri:
        url: http://127.0.0.1:8080/healthz
        status_code: [200, 503]
      register: health
    - name: Report
      ansible.builtin.debug:
        msg: "{{ health.json.release }} healthy={{ health.json.healthy }} {{ health.json.problems }}"
```

The `uri` module runs on the robot, so `127.0.0.1` is the robot's own endpoint. Robots that do not
answer show as `UNREACHABLE`.

## The rollout playbook

```yaml
# playbooks/rollout.yml
- name: Find robots that are online, healthy and idle
  hosts: "{{ target | default('all') }}"
  gather_facts: false
  ignore_unreachable: true
  tasks:
    - name: Health before the change
      ansible.builtin.uri:
        url: http://127.0.0.1:8080/healthz
      register: before
      ignore_errors: true
    # Add your own idle check here (docked, no task running); never update a robot mid-task.
    - name: Sort robots into ready and not_ready
      ansible.builtin.group_by:
        key: "{{ 'ready' if (before.status | default(-1)) == 200 else 'not_ready' }}"

- name: Switch ready robots to the release, a few at a time
  hosts: ready
  serial: [1, "25%"]            # one robot first, then a quarter of the rest per batch
  max_fail_percentage: 0        # one failed robot stops the following batches
  become: true
  vars:
    health_url: http://127.0.0.1:8080/healthz
  pre_tasks:
    - name: Pull the image while the old release still runs
      ansible.builtin.command: docker pull {{ release_image }}
    - name: Remember the running release
      ansible.builtin.copy:
        src: "{{ compose_dir }}/.env"
        dest: "{{ compose_dir }}/.env.previous"
        remote_src: true
    - name: Read the running release marker
      ansible.builtin.slurp:
        src: /etc/my_robot/release
      register: previous_marker
  tasks:
    - name: Switch, check, and roll back on any failure
      block:
        - name: Point compose at the new digest
          ansible.builtin.template:
            src: env.j2
            dest: "{{ compose_dir }}/.env"
        - name: Write the release marker
          ansible.builtin.copy:
            content: "{{ release_version }}\n"
            dest: /etc/my_robot/release
        - name: Recreate the container and wait for its healthcheck
          ansible.builtin.command:
            cmd: docker compose up -d --wait --wait-timeout 180
            chdir: "{{ compose_dir }}"
        - name: Healthy on the new release for a while
          ansible.builtin.uri:
            url: "{{ health_url }}"
          register: after
          until: after.status == 200 and (after.json.release | default('')) == release_version
          retries: 12             # example: 2 minutes; size it to your startup time
          delay: 10
      rescue:
        - name: Restore the previous digest
          ansible.builtin.copy:
            src: "{{ compose_dir }}/.env.previous"
            dest: "{{ compose_dir }}/.env"
            remote_src: true
        - name: Restore the previous marker
          ansible.builtin.copy:
            content: "{{ previous_marker.content | b64decode }}"
            dest: /etc/my_robot/release
        - name: Start the previous release
          ansible.builtin.command:
            cmd: docker compose up -d --wait --wait-timeout 180
            chdir: "{{ compose_dir }}"
        - name: Mark this robot failed so the rollout stops
          ansible.builtin.fail:
            msg: "{{ release_version }} failed on {{ inventory_hostname }}; previous release restored"
```

```bash
ansible-playbook playbooks/status.yml
ansible-playbook playbooks/rollout.yml -e target=canary     # one robot, then watch it work
ansible-playbook playbooks/rollout.yml -e target=fleet      # the rest, in batches
```

Why it is written this way:

- `rescue` exists only inside a `block`; at play level Ansible rejects it.
- A rescue that succeeds **clears the failure**: the play goes on and `max_fail_percentage`
  is not triggered. The final `ansible.builtin.fail` is what stops the next batches.
- `max_fail_percentage` must be exceeded, not reached, and with `serial` it applies to each
  batch; `0` stops at the first failed robot.
- Pulling and the backup sit in `pre_tasks`, outside the block: if the pull fails nothing has
  changed, so there is nothing to roll back.
- The first play keeps offline robots from failing a batch: Ansible's handling of unreachable
  hosts under `serial` is easy to get wrong, so only robots that answered are rolled out. The
  others run the old release until a later run reaches them; `status.yml` shows who lags.
- Canary soak time is your decision: run the canary, let it do real work for hours or a day,
  then the rest.

## Variant: apt releases

Replace the compose steps with an exact install of every release package and a service restart
(names and version suffix from [releases.md](releases.md)):

```yaml
- name: Install the release packages at one version
  ansible.builtin.apt:
    name: "{{ release_packages | map('regex_replace', '$', '=' ~ release_version ~ '-0noble') | list }}"
    update_cache: true
    allow_downgrade: true          # the same task installs the previous version in rescue
- name: Restart the robot
  ansible.builtin.systemd_service:
    name: my-robot.service
    state: restarted
```

with `release_packages: [ros-jazzy-my-robot-bringup, ros-jazzy-my-robot-driver, ros-jazzy-my-robot-msgs]`
in `group_vars`, and the rescue repeating both tasks with the previous version.

## Robots that are rarely reachable

When robots sit behind networks you cannot reach, invert the direction: `ansible-pull` on a
systemd timer clones the `fleet-ops` repository on the robot and runs a local playbook
(`ansible-pull -U <repo> -i localhost, playbooks/local.yml`), or use an OTA server
([ota-tools.md](ota-tools.md)) that robots poll.

## Checks

- `ansible-playbook --syntax-check playbooks/rollout.yml` passes; `--check` against the canary
  shows only the expected changes.
- On a test robot, a deliberately broken release (a digest whose container exits) is rolled back
  and the run stops before the next batch.
- After a rollout, `status.yml` shows every reachable robot healthy on `release_version`.
