# Remote access to robots

Part of [ops-fleet](../SKILL.md). Robots sit behind Wi-Fi, LTE and customer firewalls; reach them
through a VPN in which each robot is one identity, and expose nothing else. Licences and prices
were read from each project's repository and pricing page on 2026-11-25; re-check before buying.

## Choose a VPN

| Tool | Licence | Who runs the control plane | Cost | Fits |
|---|---|---|---|---|
| WireGuard (`wg-quick`) | GPL-2.0 (in the Linux kernel; `wireguard-tools` GPL-2.0) | you: a hub server and one config per robot | free | up to a few dozen robots, one hub you control |
| Tailscale | client BSD-3-Clause; coordination service proprietary | Tailscale | Personal plan free but **non-commercial only** (6 users, 50 tagged devices); Standard $8 and Premium $18 per user per month; fleet "Edge & IoT" terms by sales | mixed networks, NAT traversal, quick start |
| Headscale | BSD-3-Clause | you (self-hosted Tailscale-compatible server; Tailscale clients) | free | Tailscale's model without the SaaS |
| NetBird | client BSD-3-Clause; management, signal and relay AGPL-3.0 | NetBird cloud or you | cloud Free: 5 users, 100 machines; Team €6 and Business €12 per user per month | self-hostable mesh with a web UI |
| Nebula | MIT | you (lighthouses and a certificate authority) | free | large meshes, certificate-based identity |
| ZeroTier | client core MPL-2.0; the network controller is source-available | ZeroTier, or you under its licence | commercial self-hosting of the controller needs a licence; hosted plans | existing ZeroTier users |
| Husarnet | GPL-3.0 or MPL-2.0 (dual, by use) | Husarnet | Free: 5 devices, non-commercial; Standard from $10 per month | ROS-oriented peer-to-peer setups |

For a company fleet the free tiers of Tailscale and Husarnet do not apply (non-commercial only).
Self-hosting Headscale, NetBird or a WireGuard hub keeps the control plane yours.

## WireGuard hub (example)

A small server at `vpn.fleet.example.com` is the hub; robots and operators are peers. Keys live in
Ansible Vault, one pair per robot. `10.66.0.0/24` is an example private range; pick your own.

```ini
# /etc/wireguard/wg0.conf on robot-01 (rendered by Ansible)
[Interface]
Address = 10.66.0.11/24
PrivateKey = <robot-01 private key>

[Peer]
# the hub
PublicKey = <hub public key>
Endpoint = vpn.fleet.example.com:51820
AllowedIPs = 10.66.0.0/24
PersistentKeepalive = 25      # keeps the NAT mapping open; WireGuard's suggested value
```

```ini
# /etc/wireguard/wg0.conf on the hub (excerpt)
[Interface]
Address = 10.66.0.1/24
ListenPort = 51820
PrivateKey = <hub private key>

[Peer]
# robot-01
PublicKey = <robot-01 public key>
AllowedIPs = 10.66.0.11/32
```

```bash
sudo apt install wireguard-tools
sudo systemctl enable --now wg-quick@wg0
sudo wg show                  # a recent "latest handshake" per peer
```

The hub forwards between peers only with `net.ipv4.ip_forward=1`; add firewall rules on the hub so
operators reach robots, robots reach the fleet server, and robots do not reach each other.

## Access rules, whatever the VPN

- Operators → robots: SSH (22), and ROS or bridge ports only when someone is debugging.
- Robots → fleet server: logs, metrics, registry, apt repository ([observability.md](observability.md)).
- Robots → robots: nothing, unless your application needs it.
- In Tailscale, Headscale and NetBird, tag robots (`tag:robot`) and write these as ACLs; a robot's
  node key is a device identity, not a user's.
- A lost or retired robot: revoke its VPN key and registry token the same day.

## SSH on robots

```text
# /etc/ssh/sshd_config.d/10-fleet.conf
PasswordAuthentication no
PermitRootLogin no
AllowUsers ops
```

- sshd uses the **first** value it reads for most options, and Ubuntu reads
  `/etc/ssh/sshd_config.d/*.conf` in name order before the main file. A cloud-init or vendor file
  such as `50-cloud-init.conf` with `PasswordAuthentication yes` wins over a later file, so name
  yours to sort first. Check the result with `sudo sshd -T | grep -E 'passwordauthentication|permitrootlogin'`.
- One key per operator, managed as a list in the inventory (`ansible.posix.authorized_key`,
  `exclusive: true`). Rotation order: add the new key, log in with it, then remove the old one in a
  separate run. An OpenSSH certificate authority (`TrustedUserCAKeys`) with short-lived operator
  certificates avoids editing `authorized_keys` on every robot.
- Firewall last, carefully: `ufw allow in on wg0 to any port 22 proto tcp` **before**
  `ufw default deny incoming` and `ufw enable`, applied to the canary first. A rule that drops the
  VPN interface locks you out of a robot in the field.

## ROS tools over the VPN

- Discovery across the VPN: [discovery.md](discovery.md) (multicast does not cross; use static
  peers, a discovery server, or Zenoh).
- Foxglove or a browser dashboard: bind `foxglove_bridge` or rosbridge to `127.0.0.1` on the robot
  and tunnel (`ssh -L 8765:127.0.0.1:8765 ops@robot-01`), as in
  [ros2-web-bridge](../../ros2-web-bridge/references/secure-access.md). Never publish bridge ports
  to the internet: they allow publishing and service calls.
- Large topics over LTE cost money and latency; record on the robot and fetch the bag
  ([bags.md](bags.md)) instead of streaming.

## Checks

- From an operator machine: `ssh ops@robot-01 true` works; password login is refused
  (`ssh -o PubkeyAuthentication=no ops@robot-01` fails).
- From robot-01: robot-02's address does not answer (`ping -c1 -W2 <robot-02 VPN address>` fails),
  and the fleet server does.
- `ss -tulpn` on the robot shows no ROS bridge, health or metrics port on a public interface.
