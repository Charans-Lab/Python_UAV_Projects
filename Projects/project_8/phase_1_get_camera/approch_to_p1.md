# Project 8 — Phase 1: Camera in Gazebo → ROS 2 Topic

**Goal:** get a drone with a downward-facing camera into Gazebo, bridge its image stream into the ROS 2 graph, and verify the topic is publishing — before writing any node code.

Breaking the problem into two stages:

1. Spawn a drone that has a downward-facing camera.
2. Bridge that camera image from Gazebo transport into a ROS 2 topic.

---

## Stage 1 — Spawn a drone with a downward-facing camera

PX4 ships several Gazebo airframe models. One of them carries a mono camera pointed **downward**.

```bash
make px4_sitl gz_x500_mono_cam_down
```

Confirm the camera is publishing on the **Gazebo** side first:

```bash
gz topic -l | grep camera
```

Only once that shows up is there anything to bridge.

> **Naming note:** `gz_x500_mono_cam` is the **forward**-facing variant; `gz_x500_mono_cam_down` is the **downward**-facing one. The `_down` suffix is the whole difference.

---

## Stage 2 — Bridge the image into ROS 2

This needs the **`ros_gz_bridge`** package, using its **`parameter_bridge`** executable.

### Syntax

```bash
ros2 run ros_gz_bridge parameter_bridge '<topic>@<ROS2_type><direction><Gazebo_type>'
```

The middle delimiter sets the **direction** of the bridge:

| Delimiter | Direction | Meaning |
|---|---|---|
| `@` | Gazebo ↔ ROS 2 | Bidirectional |
| `[` | Gazebo → ROS 2 | Gazebo publishes, ROS subscribes |
| `]` | ROS 2 → Gazebo | ROS publishes, Gazebo subscribes |

### Command

```bash
ros2 run ros_gz_bridge parameter_bridge \
  '/world/default/model/x500_mono_cam_down_0/link/camera_link/sensor/camera/image@sensor_msgs/msg/Image@gz.msgs.Image'
```

Expected output — note that only a **GZ→ROS** bridge is created:

```text
[INFO] [ros_gz_bridge]: Creating GZ->ROS Bridge:
  [/world/default/.../camera/image (gz.msgs.Image)
   -> /world/default/.../camera/image (sensor_msgs/msg/Image)] (Lazy 0)
```

The bridge must **stay running** in its own terminal. Kill it and the ROS topic disappears.

---

## Verification

**1. Topic exists**

```bash
ros2 topic list | grep image
# /world/default/model/x500_mono_cam_down_0/link/camera_link/sensor/camera/image
```

**2. Type is correct** — this is the step that confirms the bridge did its job:

```bash
ros2 topic info /world/default/model/x500_mono_cam_down_0/link/camera_link/sensor/camera/image
# Type: sensor_msgs/msg/Image
# Publisher count: 1
```

**3. Data is actually flowing**

```bash
ros2 topic hz /world/default/model/x500_mono_cam_down_0/link/camera_link/sensor/camera/image
```

```text
average rate: 29.377   min: 0.030s  max: 0.064s  std dev: 0.00589s  window: 31
average rate: 29.815   min: 0.030s  max: 0.064s  std dev: 0.00439s  window: 62
average rate: 29.336   min: 0.029s  max: 0.067s  std dev: 0.00610s  window: 91
average rate: 29.555   min: 0.029s  max: 0.067s  std dev: 0.00544s  window: 122
average rate: 28.956   min: 0.029s  max: 0.131s  std dev: 0.00980s  window: 149
```

A steady ~30 Hz confirms the sensor is running at its configured rate and the bridge is keeping up.

**4. Visual sanity check** (optional but fast):

```bash
ros2 run rqt_image_view rqt_image_view
```

If a picture appears, Phase 1 is done.

---

## Improvements worth making now

### Shorten the topic name

The bridged topic keeps Gazebo's full path, which is unusable to type and will be hard-coded into the node later. Remap it:

```bash
ros2 run ros_gz_bridge parameter_bridge \
  '/world/default/model/x500_mono_cam_down_0/link/camera_link/sensor/camera/image@sensor_msgs/msg/Image[gz.msgs.Image' \
  --ros-args -r /world/default/model/x500_mono_cam_down_0/link/camera_link/sensor/camera/image:=/camera/image_raw
```

Then everything downstream just subscribes to `/camera/image_raw`.

### Bridge `camera_info` too

Phase 4 (ArUco **pose** estimation) needs the camera intrinsics — focal length and principal point. Gazebo publishes those on a matching `camera_info` topic. Bridge it now:

```bash
'<...>/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo'
```

Without it you can get marker **corners in pixels**, but not the marker's **3D pose**.

---

## Personal learnings

### 1. Gazebo images reach ROS 2 through `ros_gz_bridge`

The `parameter_bridge` executable does the message-type translation between Gazebo transport and the ROS 2 graph.

### 2. Why bridge at all — why not subscribe to the Gazebo topic directly?

Technically possible. Gazebo transport has Python bindings; a script could subscribe to `gz.msgs.Image` and process it with OpenCV. It would work.

Why nobody does it:

- **The program would live in Gazebo's world, not ROS's.** It can't subscribe to `/fmu/out/vehicle_local_position_v1`, so the camera code has no access to the drone's position. Vision-based navigation is fundamentally about fusing *what the camera sees* with *where the drone is* — two messaging systems means no shared graph.
- **No ROS tooling.** No `ros2 topic echo`, no `rqt_image_view`, no `ros2 bag`. That last one matters enormously: recording sensor data and replaying it while developing algorithms is how perception work actually gets done.
- **Nothing downstream can consume the output.** If an ArUco node detects a marker and wants to tell a control node, that control node is in ROS. You'd be publishing into the wrong universe.

**The structural reason:** Gazebo is a simulator — it disappears the moment you move to real hardware. A real camera publishes `sensor_msgs/Image` through a ROS driver. If the perception code subscribes to `sensor_msgs/Image`, it doesn't care whether the frames came from Gazebo, a RealSense, or a rosbag. The same node runs unchanged in sim and on the drone.