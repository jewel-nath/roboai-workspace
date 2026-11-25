# SROS2: keystore, enclaves and permissions

SROS2 turns on DDS-Security for ROS 2: participants prove who they are with certificates from your
certificate authority, traffic is signed and encrypted, and each enclave may only publish, subscribe,
call and serve what its signed permissions allow. It keeps strangers on the network from driving the
robot or reading its sensors. It is not a safety function, and it does not cover anything that
reaches the robot outside DDS (web bridges, SSH, the drives' own fieldbus).

Checked against `sros2` 0.13.6 (Jazzy binary), its `jazzy` branch and the ROS 2 Jazzy security
tutorials, 2026-11-25. Works with the DDS RMWs (Fast DDS, Cyclone DDS, Connext); secure traffic
between different vendors is not supported. `rmw_zenoh` uses its own route, below.

## What the tools create

```text
my_robot_keystore/
├── public/      ca.cert.pem, identity_ca.cert.pem, permissions_ca.cert.pem   (one CA by default)
├── private/     ca.key.pem and its links                                      NEVER on the robot
└── enclaves/
    ├── governance.xml, governance.p7s                                         domain-wide rules, signed
    └── my_robot/base/  cert.pem, key.pem, permissions.xml, permissions.p7s, links to the CA certs and governance
```

- `create_keystore` writes a governance file that refuses unauthenticated participants, encrypts
  discovery, liveliness, metadata and data, signs RTPS messages, and turns on read and write access
  control for every topic.
- The governance and every permissions file carry the domain ID taken from `ROS_DOMAIN_ID` **when they
  are generated** (0 if unset).
- `create_enclave` gives the new enclave a wildcard policy: every topic, service and action allowed.
  That is authentication and encryption, not access control, until you replace it with a policy.
- Certificates are valid for 3650 days from creation; permissions carry their own validity window.
  Keep the robot's clock right before ROS starts.

## Steps

1. **Make the keystore on a workstation**, not on the robot, with the robot's domain ID:

   ```bash
   export ROS_DOMAIN_ID=42                                  # the value the robot runs with
   ros2 security create_keystore ~/keystores/my_robot
   ```

2. **Choose enclaves: one per process.** The enclave is fixed when the process's context starts, from
   `--enclave` (or `ROS_SECURITY_ENCLAVE_OVERRIDE`, which wins). Every node in a process, so every node
   in a component container, shares it. Example set: `/my_robot/base` (ros2_control and drivers),
   `/my_robot/nav` (the Nav2 container), `/my_robot/safety` (stop gate, chain status), `/my_robot/teleop`,
   `/my_robot/bridge` (rosbridge or foxglove_bridge), `/my_robot/ops` (people's CLI).

3. **Write the policy.** A starting point from the running graph: launch the stack without security
   but with each process's `--enclave` set, then

   ```bash
   ros2 security generate_policy my_robot_policy.xml      # groups profiles by enclave
   ```

   and cut it down. Policy names are ROS names; the tools translate them to DDS names. A trimmed
   enclave for the stop gate:

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <policy version="0.2.0">
     <enclaves>
       <enclave path="/my_robot/safety">
         <profiles>
           <profile ns="/" node="stop_gate">
             <topics publish="ALLOW">
               <topic>rosout</topic>
               <topic>cmd_vel_gated</topic>
               <topic>~/lock</topic>
               <topic>~/state</topic>
             </topics>
             <topics subscribe="ALLOW">
               <topic>twist_mux/cmd_vel</topic>
               <topic>/safety/chain_ok</topic>
               <topic>/base_driver/heartbeat</topic>
             </topics>
             <topics publish="ALLOW" subscribe="ALLOW">
               <topic>/parameter_events</topic>
             </topics>
             <services reply="ALLOW">
               <service>~/reset</service>
               <service>~/describe_parameters</service>
               <service>~/get_parameter_types</service>
               <service>~/get_parameters</service>
               <service>~/list_parameters</service>
               <service>~/get_type_description</service>
             </services>
           </profile>
         </profiles>
       </enclave>
     </enclaves>
   </policy>
   ```

   The node's own `~/set_parameters` service is left out, so nobody can change its timeouts at run
   time. The `sros2` repository's `sros2/test/policies/common/` holds the per-node basics (logging,
   parameters, time, type description) to include with XInclude.

4. **Generate the artifacts** for every enclave in the policy (it creates missing enclaves too):

   ```bash
   ros2 security generate_artifacts -k ~/keystores/my_robot -p my_robot_policy.xml
   ros2 security list_enclaves ~/keystores/my_robot
   ```

   One enclave by hand: `ros2 security create_enclave <keystore> /my_robot/base`, then
   `ros2 security create_permission <keystore> /my_robot/base my_robot_policy.xml`.

5. **Deploy only what the robot needs**, as the
   [deployment guidelines](https://docs.ros.org/en/jazzy/Tutorials/Advanced/Security/Deployment-Guidelines.html)
   lay out: `public/`, `enclaves/governance.p7s` and the robot's own enclave folders, read-only, owned
   by the service user. `private/` stays with you: without it no permission can be changed later, and
   anyone holding it can mint identities.

6. **Run with enforcement.** In the systemd unit or the launch environment (in a container, mount the
   keystore read-only at the same path):

   ```bash
   ROS_SECURITY_KEYSTORE=/opt/my_robot/keystore
   ROS_SECURITY_ENABLE=true
   ROS_SECURITY_STRATEGY=Enforce      # anything else is permissive: missing keys mean no security
   ```

   Each process gets its enclave in the launch file:

   ```python
   Node(package='my_robot_safety', executable='stop_gate',
        ros_arguments=['--enclave', '/my_robot/safety'])
   ComposableNodeContainer(name='nav2_container', namespace='', package='rclcpp_components',
                           executable='component_container_isolated',
                           ros_arguments=['--enclave', '/my_robot/nav'], composable_node_descriptions=[])
   ```

7. **Use the CLI as a person** with its own enclave and no daemon (the daemon has no enclave):

   ```bash
   export ROS_SECURITY_ENCLAVE_OVERRIDE=/my_robot/ops
   ros2 topic list --no-daemon --spin-time 3
   ```

## Permissions that matter for safety

| Interface | Allow to |
|---|---|
| The base controller's command topic | The last hop only (stop gate or collision monitor) |
| `twist_mux` inputs | Their own sources (Nav2 container, teleop, bridge) |
| `/safety/chain_ok` publish | The node that reads the rated chain's status |
| `/stop_gate/reset` request | The operator's enclave (UI backend or `ops`) |
| `/collision_monitor/toggle` request | Nobody in normal operation |
| `/controller_manager/*` service requests (switch controllers, set hardware state, load, unload) | `ops` only |
| `.../set_parameters` requests on controllers, smoother, collision monitor, stop gate | Nobody, or `ops` during commissioning |
| Anything a web client can reach | Only what the bridge's enclave allows; see [ros2-web-bridge](../../ros2-web-bridge/references/secure-access.md) |

## rmw_zenoh

`rmw_zenoh` does not read `ROS_SECURITY_*`. Its `zenoh_security_tools` package (released with
`rmw_zenoh` 0.2.13 on Jazzy) turns an sros2 policy and enclaves into Zenoh session and router configs
with access control, authentication and encryption:

```bash
ros2 run zenoh_security_tools generate_configs --policy my_robot_policy.xml --ros-domain-id 42 \
  --session-config <default session config>.json5 --router-config <default router config>.json5 \
  --enclaves ~/keystores/my_robot/enclaves/my_robot
```

The two config arguments are rmw_zenoh's default configs to start from; the tool writes one config
per node in the policy, and each process gets its own through `ZENOH_SESSION_CONFIG_URI` (the router
through `ZENOH_ROUTER_CONFIG_URI`). With `--enclaves`, the tool expects one enclave folder per node
name in the policy, plus one for the router, so the enclave layout differs from the per-process one
above. Details: the package README.

## Checks

- Under `Enforce`, a process without an enclave folder fails to start.
- A process with security off on the same domain receives nothing.
- A node remapped to a topic outside its permissions fails to start.
- `tcpdump` on the robot's interface shows no readable payloads (the
  "Examine traffic" tutorial in the ROS 2 docs).
- `ls /opt/my_robot/keystore` on the robot shows no `private/`.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| Nodes start but nothing is secured | `ROS_SECURITY_STRATEGY` not `Enforce`, or `ROS_SECURITY_ENABLE` unset in the unit | Set both in the unit or launch environment; check a running node with `tr '\0' '\n' < /proc/<pid>/environ \| grep ROS_SECURITY` (`systemctl show` misses variables sourced from `env.sh`) |
| Secured nodes do not see each other | Keystore or permissions made with another `ROS_DOMAIN_ID` | Regenerate with the runtime domain ID |
| `ros2 topic list` is empty | The CLI uses the daemon, or has no enclave | `ROS_SECURITY_ENCLAVE_OVERRIDE`, `--no-daemon --spin-time 3` |
| One Nav2 node is refused a topic | The container's single enclave lacks it | The container's policy covers all its nodes, or split the container |
| `create_key` warns, or is unknown | Deprecated on Jazzy, removed from Kilted on | `create_enclave`, `list_enclaves` |
| Mixed Fast DDS and Cyclone DDS robots stop talking | Cross-vendor security is not supported | One RMW across the secured system |
| Fast DDS built from source has no security | Built without `-DSECURITY=ON` | Rebuild with it, or use the binaries |
| Everything fails some years later | Certificates expire 3650 days after creation | Calendar the renewal; keep `private/` safe for it |
