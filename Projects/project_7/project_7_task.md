# Project 7 — Your First ROS 2 Node

**Goal:** Cross the bridge from "Python scripts that use libraries" to "ROS 2 nodes inside a robotics framework." Write a node that subscribes to live drone data from PX4 and processes it.

This is the project that turns you from "someone learning Python for drones" into "someone who can read and write the kind of code real drone autonomy stacks are built on."

---

## The mental shift before you start

**MAVSDK was a library.** You imported it, called its functions, your code was in control.

**ROS 2 is a framework.** Your code lives inside it. A ROS 2 system is many small programs (called **nodes**) running at the same time, talking to each other through named channels (called **topics**). One node publishes data, others subscribe and react. Each node is independent — one crashing doesn't kill the others.

Why this architecture wins for robotics:
- **Modularity.** A camera node, a SLAM node, a planner node, a controller node — write them separately, swap them independently.
- **Distribution.** Nodes can run on different computers (companion computer + ground station + cloud) and talk transparently.
- **Tooling.** ROS 2 gives you `ros2 topic echo`, `rqt_graph`, `rosbag`, etc. — instant introspection and replay tools.

**Vocabulary you need from day one:**
- **Node** — a single program in a ROS 2 system. Usually a Python class inheriting from `rclpy.node.Node`, or a C++ class inheriting from `rclcpp::Node`.
- **Topic** — a named channel where messages flow (e.g. `/fmu/out/vehicle_local_position`).
- **Publisher** — a node side that *sends* messages on a topic.
- **Subscriber** — a node side that *receives* messages on a topic, via a callback function.
- **Message** — a typed data structure (e.g. `sensor_msgs/msg/Imu`). Every topic carries one message type.
- **Callback** — a function the framework calls automatically when a new message arrives.
- **`rclpy`** — the Python client library for ROS 2.

The shape of your first node is:

```python
import rclpy
from rclpy.node import Node

class DroneListener(Node):
    def __init__(self):
        super().__init__('drone_listener')
        self.subscription = self.create_subscription(...)

    def callback(self, msg):
        ...

def main():
    rclpy.init()
    node = DroneListener()
    rclpy.spin(node)
    rclpy.shutdown()

main()
```

Familiar shape: a class, with `__init__`, with methods, instantiated in `main()`. **Same structure as `DroneMission` and `IMUAnalyzer`.** The new piece is `super().__init__('drone_listener')` — **inheritance**. `DroneListener` inherits everything that a `Node` knows how to do, and then adds its own logic on top. Inheritance is the OOP concept you'll meet properly in this project.

---

## Prerequisite reading (~2 days, before any code)

Read the official **ROS 2 Jazzy Tutorials**, in this exact order:

1. **CLI tools — first 3 tutorials**
   - "Configuring your ROS 2 environment"
   - "Using turtlesim, ros2, and rqt"
   - "Understanding nodes"

2. **Topics tutorial:** "Understanding topics"

3. **Writing a simple publisher and subscriber (Python)** — this is the canonical first-node tutorial. Read it. Don't blindly copy yet.

URL pattern: `docs.ros.org/en/jazzy/Tutorials.html`

**Stop when you can answer these in `setup_log.md`, in your own words:**

1. What is a node? How is it different from a regular Python script?
2. What is a topic, and how does a publisher/subscriber pair work?
3. What does `rclpy.spin(node)` do? Why is it needed?
4. What does inheritance mean (`class DroneListener(Node):`)? What does the child class get from the parent?
5. What's the difference between running a Python file directly (`python my_node.py`) and running it via `ros2 run`?

If you can't answer #4 yet, that's fine — you'll meet inheritance properly during the build. But try.

---

## Phase 1 — Install ROS 2 Jazzy (~half a day, mostly waiting on downloads)

Run these commands in order. Read each one before you run it. If anything errors, paste me the exact error.

### 1.1 — Set the locale (ROS 2 needs UTF-8)

```bash
locale  # check current
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

### 1.2 — Enable Universe repository and install curl

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
```

### 1.3 — Add the ROS 2 GPG key and repository

```bash
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

### 1.4 — Install ROS 2 Jazzy desktop + dev tools

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install ros-jazzy-desktop -y
sudo apt install ros-dev-tools -y
```

This downloads ~2 GB. Be patient.

### 1.5 — Source ROS 2 in every new shell

Add this line to the end of `~/.bashrc` so it auto-runs in every new terminal:

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 1.6 — Verify

Open a new terminal and run:

```bash
ros2 --help
```

You should see the ROS 2 CLI help. Then run the demo talker/listener — two terminals:

**Terminal A:**
```bash
ros2 run demo_nodes_cpp talker
```

**Terminal B:**
```bash
ros2 run demo_nodes_py listener
```

The listener should print messages it receives from the talker. If yes → **ROS 2 is alive on your machine. Phase 1 done.** Commit a note to `setup_log.md`.

---

## Phase 2 — Hello ROS 2 (~2 days)

Goal: build the talker/listener yourself, the official way, so you understand the build system.

### 2.1 — Create a ROS 2 workspace

A workspace is just a directory with a `src/` subfolder where your packages live.

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

### 2.2 — Create a Python package

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python --license Apache-2.0 my_first_node \
  --dependencies rclpy std_msgs
```

This generates a `my_first_node/` folder with `package.xml`, `setup.py`, and a Python module folder. Look around inside it before doing anything else.

### 2.3 — Write the node

Create `~/ros2_ws/src/my_first_node/my_first_node/listener.py`:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MyListener(Node):
    def __init__(self):
        super().__init__('my_listener')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main():
    rclpy.init()
    node = MyListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 2.4 — Register the entry point

In `~/ros2_ws/src/my_first_node/setup.py`, in the `entry_points` section:

```python
entry_points={
    'console_scripts': [
        'listener = my_first_node.listener:main',
    ],
},
```

### 2.5 — Build the workspace

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

**Common gotcha:** every time you build, you must `source install/setup.bash` in any terminal that wants to use the package. Or add it to `~/.bashrc` like you did with `/opt/ros/jazzy/setup.bash`.

### 2.6 — Run it

**Terminal A:**
```bash
ros2 run demo_nodes_cpp talker   # publishes on /topic
```

**Terminal B:**
```bash
source ~/ros2_ws/install/setup.bash
ros2 run my_first_node listener
```

You should see your listener printing messages from the talker. **When this works, Phase 2 is done.** Commit the package to your repo.

---

## Phase 3 — Subscribe to PX4 sensor data (~1 week)

Now the real thing: write a node that listens to live data from your running PX4 SITL drone.

### 3.1 — Install the PX4 ↔ ROS 2 bridge

PX4 talks to ROS 2 through **`uXRCE-DDS`** (formerly `micro_ros_agent` / `microRTPS`). PX4 publishes its internal topics over a small DDS bridge, and ROS 2 picks them up.

```bash
sudo apt install ros-jazzy-px4-msgs ros-jazzy-px4-ros-com  # check exact names
sudo snap install micro-xrce-dds-agent --edge
```

> Package names for the bridge change occasionally. If those don't work, check the PX4 docs at `docs.px4.io` → "ROS 2 User Guide" for the current install method. **Read those docs.** They are the source of truth for this integration.

### 3.2 — Start everything in order

You'll need **three terminals**:

**Terminal A — micro-XRCE-DDS agent:**
```bash
MicroXRCEAgent udp4 -p 8888
```

**Terminal B — PX4 SITL:**
```bash
cd ~/drone-dev/PX4-Autopilot
make px4_sitl gz_x500
```

**Terminal C — your ROS 2 node** (you'll write this).

Once PX4 connects to the agent, ROS 2 will see PX4's topics. Verify:

```bash
ros2 topic list
```

You should see topics like `/fmu/out/vehicle_local_position`, `/fmu/out/vehicle_status`, `/fmu/out/sensor_combined`. These are PX4's internal data, now available to any ROS 2 node.

### 3.3 — Write the PX4 listener node

Inside your existing package (or a new one — your choice), write `px4_listener.py`:

```python
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy
from px4_msgs.msg import VehicleLocalPosition

class PX4Listener(Node):
    def __init__(self):
        super().__init__('px4_listener')
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=5
        )
        self.subscription = self.create_subscription(
            VehicleLocalPosition,
            '/fmu/out/vehicle_local_position',
            self.position_callback,
            qos_profile
        )

    def position_callback(self, msg):
        self.get_logger().info(
            f'x={msg.x:.2f}, y={msg.y:.2f}, z={msg.z:.2f}, '
            f'vx={msg.vx:.2f}, vy={msg.vy:.2f}, vz={msg.vz:.2f}'
        )

def main():
    rclpy.init()
    node = PX4Listener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

> The QoS settings matter. PX4 uses `BEST_EFFORT` reliability — if you use the default `RELIABLE`, your subscription will silently get no messages. This is one of the top gotchas with PX4 ↔ ROS 2.

Build, source, run:

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
ros2 run my_first_node px4_listener
```

You should see live x/y/z/velocity from your simulated drone, streamed via ROS 2. Move the drone in QGC (or upload a mission with your Project 5 script in a fourth terminal!) and watch the values change.

### 3.4 — Stretch goal: process the data

Don't just print. Use what you learned in Project 6:
- Collect 200 messages into a list.
- Convert to a NumPy array.
- Compute mean velocity, mean position.
- (Optional) plot it with matplotlib.

**This is the real shape of robotics work — subscribe, buffer, analyze, act.**

---

## Code-quality and habit checklist

Same habits as before:

- [ ] **Run before declaring done.** Every phase.
- [ ] **Read warnings.** Don't ignore them.
- [ ] **Commit small, commit often.** Phase 1 done = commit. Phase 2 listener works = commit.
- [ ] **Log to `setup_log.md`** at each phase: what you installed, what commands worked, what errors you hit and how you fixed them.
- [ ] **Don't push absolute paths or `__pycache__/` to GitHub.** Update `.gitignore` if needed.
- [ ] **PascalCase classes, snake_case methods and variables.**
- [ ] **One file per node**, named after the node it contains.

---

## Definition of done

- [ ] Prerequisite reading complete; five questions answered in `setup_log.md`.
- [ ] Phase 1: ROS 2 Jazzy installed; demo talker/listener works.
- [ ] Phase 2: your own listener node, in a workspace package, prints messages from the demo talker.
- [ ] Phase 3: `px4_listener` node subscribes to `/fmu/out/vehicle_local_position` and logs live position data from running SITL.
- [ ] Stretch goal: at least one analysis or plot of the buffered PX4 data.
- [ ] Workspace committed to your `Python_UAV_Projects` repo (under `Projects/Project-7/ros2_ws/src/...` or similar).
- [ ] README updated to list Project 7.

---

## What this unlocks

After Project 7, you can:

- Read and modify the source of any open-source ROS 2 drone stack (PX4, Auterion, many academic SLAM systems).
- Write your own perception nodes — they're just classes with subscriptions and callbacks.
- Combine multiple nodes into a real system (camera → object detection → controller → drone).

**The next projects in your roadmap** (after Project 7):
- **Project 8:** Camera + OpenCV — subscribe to a Gazebo camera, detect ArUco markers.
- **Project 9:** Closed-loop control — your node *commands* the drone based on what it sees.
- **Project 10+:** Choose your direction (vision-based landing, GPS-denied navigation, obstacle avoidance, swarm).

That's when you've crossed fully into autonomous drone engineering.

---

## When you're stuck

The setup phases especially are where you'll burn time on environment errors. The rule from earlier projects still applies: **stuck for 30 minutes on one specific error → bring me the exact error message and what you've tried.** Don't suffer for hours. Don't restart. Don't retreat to "I need to read more first." Bring the error, we debug.
