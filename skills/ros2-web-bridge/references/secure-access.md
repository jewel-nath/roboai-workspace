# Secure access to a robot's web bridges

A bridge that can publish `/cmd_vel` is a remote control for a machine that can hurt people. None
of the ROS web bridges checks who connects, so the network setup is the security.

## What each bridge does by default (Jazzy releases)

| Bridge | Default bind | Login | Other defaults that matter |
|---|---|---|---|
| rosbridge_suite 2.7 | all interfaces (`address` empty), port 9090 | none: removed from the ROS 2 port in 2021 because rosauth is not maintained for ROS 2 | every topic, service and parameter allowed; any web page origin accepted |
| foxglove_bridge 3.6 | `0.0.0.0`, port 8765 | none on the local WebSocket | every topic, service and parameter allowed; clients may publish (`clientPublish`) |
| web_video_server 3.1 | `0.0.0.0`, port 8080 | none | `Access-Control-Allow-Origin: *` on streams |
| Your FastAPI service | what you pass to uvicorn | what you build | interactive docs at `/docs` |

"Any origin accepted" means that while an operator's browser can reach `ws://robot:9090`, any web
page open in that browser can open the same WebSocket and publish.

## Rules

1. Bind every bridge to `127.0.0.1` (rosbridge `address:=127.0.0.1`, foxglove_bridge
   `address:=127.0.0.1`, web_video_server `-p address:=127.0.0.1`, uvicorn `host="127.0.0.1"`).
2. Reach them through one authenticated, encrypted entry point: an SSH tunnel for one engineer, a
   VPN for a team, a reverse proxy with TLS and a login for a dashboard.
3. Never forward a bridge port on a router or expose it on a public cloud address. A robot
   reachable from the internet needs a VPN or a remote-access service that authenticates first.
4. Still restrict what each bridge exposes (rosbridge globs, foxglove whitelists and
   capabilities, a narrow FastAPI API). That limits the damage of a stolen login or a bug.
5. Stopping is not the web path's job alone: the base controller's command timeout, a hardware
   E-stop and the robot's own safety layer must stop the robot when the web side goes silent.

## One engineer: SSH tunnel

```bash
ssh -N -L 8765:127.0.0.1:8765 -L 9090:127.0.0.1:9090 user@my-robot.local
```

Then connect Foxglove to `ws://localhost:8765` and roslibjs to `ws://localhost:9090` on the
laptop. Nothing listens on the robot's network interfaces.

## A team on the robot's network: VPN

Put the robot and the operators on a WireGuard or similar VPN. Bind the bridges to `127.0.0.1`
and the reverse proxy below to the VPN address only, so the LAN and the internet never see them.

## A dashboard: reverse proxy with TLS and a login

Serve the dashboard page, the rosbridge WebSocket, the video and the API from one origin. The
browser WebSocket API cannot set an `Authorization` header, so the login has to be one the
browser sends by itself on the same origin: HTTP Basic over TLS, or a session cookie from an
identity proxy such as oauth2-proxy.

```nginx
# /etc/nginx/sites-available/my_robot   (nginx, TLS + HTTP Basic login)
server {
    listen 443 ssl;
    server_name my-robot.example.internal;
    ssl_certificate     /etc/nginx/tls/my-robot.crt;
    ssl_certificate_key /etc/nginx/tls/my-robot.key;

    auth_basic           "my_robot";
    auth_basic_user_file /etc/nginx/my_robot.htpasswd;   # htpasswd -c ... operator

    root /var/www/my_robot_dashboard;                    # the dashboard build

    location /rosbridge {
        proxy_pass http://127.0.0.1:9090/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 1h;                           # idle WebSockets stay open
    }
    location /video/ {
        proxy_pass http://127.0.0.1:8080/;               # web_video_server
        proxy_buffering off;                             # MJPEG must not be buffered
    }
    location /api/ {
        proxy_pass http://127.0.0.1:8000;                # FastAPI service
    }
}
```

- The page then connects to `wss://<same host>/rosbridge`, as in
  [rosbridge-clients.md](rosbridge-clients.md).
- Use a certificate the operators' browsers trust (an internal CA, or a public one if the name
  is public). A self-signed certificate trains people to click through warnings.
- Separate logins for "watch" and "drive" need two locations or an identity proxy with groups;
  the bridges themselves cannot tell users apart.
- A script that is not a browser (roslibpy) can send a header:
  `roslibpy.Ros(host="wss://my-robot.example.internal/rosbridge", headers={...})`.

## foxglove_bridge, restricted

```bash
ros2 launch foxglove_bridge foxglove_bridge_launch.xml address:=127.0.0.1 \
  topic_whitelist:="['^/odom$', '^/tf$', '^/tf_static$', '^/scan$', '^/camera/.*/compressed$']" \
  capabilities:="[parameters,services,connectionGraph,assets]" \
  service_whitelist:="['^/my_robot/.*']"
```

- Whitelists are ECMAScript regular expressions, so anchor them.
- Leaving `clientPublish` out of `capabilities` makes the bridge read-only; or keep it and set
  `client_topic_whitelist` to the topics a client may publish.
- `asset_uri_allowlist` controls which `package://` files (meshes, URDF) clients may fetch;
  keep the default unless a mesh fails to load.
- `remote_access:=true` (Foxglove's platform gateway, needs a device token) is the vendor's
  authenticated alternative to opening a port. Pass the token through the
  `FOXGLOVE_DEVICE_TOKEN` environment variable, not a parameter: parameters are readable by
  other nodes.

## Check

```bash
ss -ltnp | grep -E ':(9090|8765|8080|8000)\b'   # every line shows 127.0.0.1
# From another machine on the LAN: the raw ports refuse, the proxy asks for a login
curl -m 3 http://my-robot.local:9090/ ; curl -sI https://my-robot.example.internal/ | head -1
```

Sources: rosbridge_suite `jazzy` branch (`rosbridge_websocket.py` bind address,
`websocket_handler.py` origin check) and its changelog (1.0.5, authentication removed);
foxglove-sdk `ros/src/foxglove_bridge` README and launch file (3.6.3); web_video_server `ros2`
branch source; nginx WebSocket proxying documentation.
