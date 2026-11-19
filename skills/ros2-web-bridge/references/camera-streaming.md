# Camera images to a browser (Jazzy)

Raw `sensor_msgs/msg/Image` is far too large for a browser link: a 640x480 RGB frame is about
0.9 MB, so 30 Hz is about 28 MB/s. Send JPEG frames, at a lower rate and size, through one of
the paths below. Checked against web_video_server 3.1.0 (Jazzy release, `ros2` branch).

## 1. Make sure a compressed topic exists

Camera drivers that publish through `image_transport` also publish `<topic>/compressed` once the
plugins are installed:

```bash
sudo apt install ros-jazzy-image-transport-plugins
ros2 topic list | grep compressed      # /camera/image_raw/compressed
ros2 topic hz /camera/image_raw/compressed
```

If the driver publishes only raw images, republish them (Jazzy's `republish` is a component with
parameters, not positional arguments):

```bash
ros2 run image_transport republish --ros-args \
  -p in_transport:=raw -p out_transport:=compressed \
  -r in:=/camera/image_raw -r out/compressed:=/camera/image_raw/compressed
```

The JPEG quality is a parameter of the publishing node, named after the topic and transport, for
example `image_raw.compressed.jpeg_quality`; `ros2 param list <camera node>` shows the exact name.

## 2a. web_video_server: plain HTTP, works in an `<img>` tag

```bash
sudo apt install ros-jazzy-web-video-server
ros2 run web_video_server web_video_server --ros-args \
  -p address:=127.0.0.1 -p port:=8080 -p default_stream_type:=ros_compressed
```

URLs (behind the proxy, under the path you map to it):

| URL | Gives |
|---|---|
| `/` | List of image topics with links |
| `/stream?topic=/camera/image_raw&type=ros_compressed` | The camera's own JPEG frames as MJPEG, no re-encoding |
| `/stream?topic=/camera/image_raw&type=mjpeg&width=640&height=360&quality=70` | Re-encoded MJPEG at a chosen size and quality |
| `/stream?topic=/camera/image_raw&type=h264&bitrate=500000` | H.264 in MP4, much less bandwidth, more CPU |
| `/snapshot?topic=/camera/image_raw` | One JPEG |
| `/stream_viewer?topic=/camera/image_raw` | A page that shows the stream |

- `type=ros_compressed` subscribes to `<topic>/compressed` and falls back to MJPEG if it is
  missing. It costs almost no CPU on the robot.
- `mjpeg`, `png`, `h264`, `vp8`, `vp9` decode and re-encode on the robot; watch the CPU.
- `qos_profile=sensor_data` in the URL matches best-effort camera publishers.
- `default_transport=compressed` in the URL makes the server subscribe to the compressed
  transport, which helps when web_video_server runs on another machine than the camera.
- It has no login and sends `Access-Control-Allow-Origin: *`; bind it to `127.0.0.1` and serve
  it through the authenticating proxy.

```html
<img src="/video/stream?topic=/camera/image_raw&type=ros_compressed" alt="Front camera">
```

## 2b. Through rosbridge

Subscribe to the `sensor_msgs/msg/CompressedImage` topic with a throttle, and show the bytes:

```js
const camera = new Topic({
  ros,
  name: "/camera/image_raw/compressed",
  messageType: "sensor_msgs/msg/CompressedImage",
  throttle_rate: 200,  // 5 frames per second at most
  queue_length: 1,
});
camera.subscribe((msg) => {
  // With the default JSON encoding, uint8[] data arrives as a base64 string
  document.getElementById("cam").src = `data:image/jpeg;base64,${msg.data}`;
});
```

Fine for a small preview. For a smooth feed use web_video_server or foxglove_bridge, which avoid
JSON and base64.

## 2c. Through your own FastAPI service

The service in [fastapi-rclpy.md](fastapi-rclpy.md) keeps the newest JPEG from the compressed
topic and serves `/video.mjpg` at a fixed rate. Use it when the camera must sit behind the same
login and API as the rest of the dashboard, and add more than one viewer only through that one
subscription.

## 2d. Foxglove

The Foxglove app shows `CompressedImage` and `CompressedVideo` topics directly through
foxglove_bridge. It suits engineers debugging, not an operator dashboard.

## Check

- `ros2 topic hz` on the compressed topic shows the camera rate.
- The browser's network panel shows a steady stream at the expected size per frame.
- `top` on the robot: the streaming process is not the busiest one, unless you chose a
  re-encoding stream type on purpose.

Sources: web_video_server `ros2` branch README, `web_video_server.cpp` and
`ros_compressed_streamer.cpp`; image_common `jazzy` branch `republish.cpp`; rosbridge
`ROSBRIDGE_PROTOCOL.md` (binary fields and compression).
