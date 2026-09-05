# Project 8 — Camera + OpenCV + ArUco Detection

You're moving from numbers to pixels.

- Every project so far consumed **structured telemetry** — floats with known meanings.
- Now the input is an **image**, and the work is extracting meaning from it.
- That's **perception**, and it's the foundation of everything on your roadmap: VIO, SLAM, obstacle avoidance, vision-based landing.

---

## Phase 1 — Get a camera into the simulation

- PX4's Gazebo worlds support camera-equipped models.
- Find the right model — there are variants with a **downward-facing camera**.
- Confirm the image is being published as a ROS 2 topic.
- Same verification discipline as Project 7 — check before writing any code:

```bash
ros2 topic list              # find the image topic
ros2 topic info <topic>      # confirm its message type
```

---

## Phase 2 — Subscribe to images in a node

- Structurally identical to your `px4_listener`: a node, a subscription, a callback.
- The new piece is **`cv_bridge`**, which converts ROS `sensor_msgs/Image` messages into OpenCV arrays.
- Connection back to Project 6: **an OpenCV image is a NumPy array.**
  - Shape is `(height, width, 3)` for colour.
  - Everything you learned about `shape` and array indexing applies directly.

---

## Phase 3 — Display and manipulate

- Show the live feed with `cv2.imshow()`.
- Convert to grayscale.
- Look at how the array **shape changes** when you do.
- This is where images stop being magic and become data.

---

## Phase 4 — ArUco detection

- ArUco markers are black-and-white square patterns that OpenCV can detect and identify.
- Detection gives you their **corner positions in the image**, and — with camera calibration — their **3D pose relative to the camera**.
- Steps: place a marker in the Gazebo world → fly over it → detect it → draw the detection on the image.

This last phase is the real payoff: your drone will know where a specific object is in the world, **from vision alone**. That's the primitive underneath precision landing, target tracking, and visual navigation.

---

## Before you start

- Read the OpenCV ArUco documentation.
- Get clear on two things:
  - What a **marker dictionary** is.
  - Why detection returns both **corners** and **IDs**.
- Same rule as before — enough understanding to start, not mastery.