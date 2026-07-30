# ROS 2 Learning Notes

**Author:** Sai Charan
**Setup:** ROS 2 Jazzy · Ubuntu 24.04 (Noble) · Python (`rclpy`)
**Purpose:** Personal reference and recall notes. Built progressively while learning.

---

## Table of Contents

1. [Learning Flow (Big Picture)](#1-learning-flow-big-picture)
2. [Environment & Sourcing](#2-environment--sourcing)
3. [Linux Filesystem Fundamentals](#3-linux-filesystem-fundamentals)
4. [The ROS 2 Workspace](#4-the-ros-2-workspace)
5. [Packages](#5-packages)
6. [Python OOP for ROS](#6-python-oop-for-ros)
7. [Anatomy of a Publisher Node](#7-anatomy-of-a-publisher-node)
8. [Running a Node: `python3` vs `ros2 run`](#8-running-a-node-python3-vs-ros2-run)
9. [Command Cheat Sheet](#9-command-cheat-sheet)
10. [Error → Cause Lookup](#10-error--cause-lookup)
11. [Misconceptions Corrected](#11-misconceptions-corrected)

---

## 1. Learning Flow (Big Picture)

The dependency chain — each step only makes sense after the one before it:

```
Install ROS 2  →  /opt/ros/jazzy exists on disk
       ↓
Source setup.bash  →  shell can now FIND ros2, rclpy, libraries
       ↓
Create workspace (~/ros2_ws/src)  →  a place for YOUR code
       ↓
Create a package inside src/  →  the unit of ROS 2 code
       ↓
Write a node (Python class inheriting from Node)
       ↓
colcon build  →  generates build/ install/ log/
       ↓
Source install/setup.bash  →  shell can now find YOUR package
       ↓
ros2 run <package> <executable>  →  node runs
```

**The single most important idea:** ROS 2 is not "installed into" your terminal. Each shell is blank until you *source* the setup files. Everything else depends on that.

---

## 2. Environment & Sourcing

### 2.1 What is bash?

- **Bash** = *Bourne Again SHell*
- It is the program running inside your terminal that reads and executes commands
- Default shell on Ubuntu
- A `.bash` file is just a script written in bash's language
- `setup.bash` = "a bash script that sets up ROS"

### 2.2 What does sourcing do?

```bash
source /opt/ros/jazzy/setup.bash
```

- Runs a script **inside your current shell** so its changes persist
- Contrast: running a script normally spawns a *child* process — variables set there vanish when it exits
- That distinction is the entire reason the command is `source` and not just running the file

### 2.3 What variables it sets

| Variable | Purpose |
|---|---|
| `PATH` | So typing `ros2` finds the command |
| `PYTHONPATH` | So Python can `import rclpy` |
| `LD_LIBRARY_PATH` | So compiled libraries can be found at runtime |
| `AMENT_PREFIX_PATH` | So ROS can locate installed packages |
| `CMAKE_PREFIX_PATH` | Used during builds |

`setup.bash` does two things only:
1. Prepends ROS locations to those variables
2. Sources per-package "environment hook" scripts

No magic — it is pure variable-setting.

### 2.4 Why every new shell?

- Each new terminal starts with a fresh, empty environment
- Variables do not carry over between terminals
- Auto-source the **underlay** by adding it to `~/.bashrc`:

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
```

> **Do NOT auto-source the overlay** (`~/ros2_ws/install/setup.bash`) in `.bashrc` while learning. Once you have multiple workspaces it creates confusing behaviour. Source it manually so you always know which environment you are in.

### 2.5 Mental model

> `$PATH` is the terminal's **phone book**. Typing a command makes the shell flip through it looking for the number. Sourcing adds ROS's entries to the phone book.
>
> Standing next to ROS's house (being in the folder) does not help if its number was never written down.

---

## 3. Linux Filesystem Fundamentals

### 3.1 `mkdir -p`

```bash
mkdir -p ~/ros2_ws/src
```

- `mkdir` = make directory
- `-p` = **parents** → "create any missing parent directories along this path"
- It does **not** mean "declare which folder is the parent"

Without `-p`, `mkdir` only creates the **last** item in the path; everything before must already exist:

```bash
mkdir ~/ros2_ws/src
# mkdir: cannot create directory ...: No such file or directory
```

**Bonus:** `-p` also makes the command silent if the directory already exists — safe to re-run.

### 3.2 The word "root" means three different things

| Term | Meaning |
|---|---|
| `/` | The **root directory** — top of the entire filesystem |
| `root` | The **root user** — administrator/superuser account (`sudo` borrows this) |
| `/root` | The **root user's home folder** — a normal directory, unrelated to `/` |

### 3.3 `~` is the HOME directory, not root

- `~` expands to `/home/<username>`
- Check with: `echo ~`, `whoami`, `pwd`
- `~/ros2_ws` really means `/home/<username>/ros2_ws`
- Home is the area you fully own — no `sudo` needed

### 3.4 Linux vs Windows filesystem

| Windows | Ubuntu |
|---|---|
| `C:\` | `/` |
| `C:\Users\<name>` | `/home/<name>` (i.e. `~`) |
| `C:\Program Files` | Scattered: `/usr/bin`, `/usr/lib`, `/opt` |
| Administrator | `root` user |

**Two ways the comparison breaks:**

1. **One tree, not many.** Windows gives each drive its own tree (`C:\`, `D:\`). Linux has a single tree from `/`. Other drives are *mounted into* it (e.g. a USB at `/media/<user>/MY_USB`) — they become branches, not separate trees.
2. **No single "Program Files".** A program's parts are deliberately split by *function*, not by application.

### 3.5 Key directories (Filesystem Hierarchy Standard)

| Path | Contains |
|---|---|
| `/usr/bin` | Executable programs |
| `/usr/lib` | Shared libraries |
| `/etc` | Configuration files |
| `/var` | Changing data (logs, databases) |
| `/home` | User files — **your stuff** |
| `/opt` | Optional third-party add-on software — **ROS 2 lives here** |

> **Analogy:** Windows organises software like complete **toolboxes** — each app gets its own box. Linux organises like a **workshop wall** — all hammers on one rack, all screwdrivers on another, regardless of which job they came with.

### 3.6 Why `/opt/ros/jazzy`?

- Follows the FHS convention: `/opt` is for optional add-on software
- The payoff is **predictability** — every tutorial, tool, and forum answer assumes this path
- Installing it somewhere custom puts you off the map

---

## 4. The ROS 2 Workspace

### 4.1 What it is

- An ordinary folder where you keep and build **your own** ROS 2 code
- Not a special file type — what makes it a workspace is the structure inside and running the build tool from it
- `ros2_ws` is **convention, not a rule**

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

**You only ever create `src/` by hand.** The other three folders appear on their own.

### 4.2 Underlay vs Overlay ⭐

| | Path | Meaning |
|---|---|---|
| **Underlay** | `/opt/ros/jazzy` | Official ROS 2 install |
| **Overlay** | `~/ros2_ws` | Your own packages, layered on top |

- The overlay does **not** replace the underlay — it sits above it
- ROS looks in the overlay first, then falls back to the underlay

**Always source in this order:**

```bash
source /opt/ros/jazzy/setup.bash      # underlay FIRST
source ~/ros2_ws/install/setup.bash   # then overlay
```

> **Analogy:** The underlay is the standard toolkit that came with your workbench. The overlay is the extra tray of tools *you* built and placed on top. You reach for your own tray first; if the tool isn't there, you reach into the standard kit underneath.

### 4.3 The four folders

```
~/ros2_ws/                 ← workspace root (run colcon build HERE)
├── src/                   ← YOU write code here. Git tracks THIS only.
├── build/                 ← auto. Scratch space. Ignore.
├── install/               ← auto. Finished output. SOURCE this.
└── log/                   ← auto. Build logs. For debugging failures.
```

#### `src/` — the only folder you own

- Created by: **you**
- The only folder you edit by hand
- The only folder you put in Git
- Contains **packages**, not loose files

#### `build/` — the scratch workspace

- Created by: colcon, automatically
- Intermediate artifacts: object files, CMake cache, temporary generated code
- Exists so messy build state never contaminates clean source or final output
- Enables **incremental builds** — only changed things get rebuilt, which is why the second build is much faster
- Never edit. Never commit.

> **Analogy:** the messy carpenter's bench — sawdust, offcuts, half-assembled parts. Necessary during work, not what you hand to the customer.

#### `install/` — the finished product ⭐

- Created by: colcon, automatically
- **This is what you source:** `source ~/ros2_ws/install/setup.bash`
- Contains `setup.bash` plus one subfolder per package (executables, Python modules, launch files, message definitions, config)
- Never edit. Never commit.

**⚠️ The crucial consequence: ROS runs the code in `install/`, NOT the code in `src/`.**

The classic beginner trap:
1. You edit a file in `src/`
2. You run your node
3. Nothing changed — confusion

Because `install/` still holds the **old** copy. Fix: `colcon build`.

**Time-saving shortcut for Python:**

```bash
colcon build --symlink-install
```

- Makes `install/` contain **symlinks** back to `src/` instead of copies
- Editing a Python file takes effect immediately, no rebuild
- **Still need to rebuild when:** you add a new file, change `setup.py`, or change `package.xml`

> **Analogy:** `install/` is the finished product on the shelf. Customers take from the shelf. Changing the blueprint (`src/`) changes nothing on the shelf until you manufacture again (`colcon build`).

#### `log/` — the record

- Created by: colcon, automatically
- One timestamped folder per build, plus a `latest_build` symlink
- Per-package `stdout` and `stderr`
- **When you actually use it:** a build fails and terminal output was too cluttered or scrolled past

> **Analogy:** the build's CCTV footage. Ignored until something goes wrong.

### 4.4 Building

```bash
cd ~/ros2_ws        # workspace ROOT, not inside src/
colcon build
```

- `colcon` = the ROS 2 build tool ("collective construction")
- Looks inside `src/`, finds every package, builds them
- Creates `build/`, `install/`, `log/` automatically
- **Common mistake:** running `colcon build` while inside `src/`. You are in the right place when `ls` shows `src`.

### 4.5 The everyday loop

```bash
cd ~/ros2_ws                  # 1. workspace root
# ...edit code in src/...
colcon build                  # 2. build
source install/setup.bash     # 3. source the overlay
ros2 run my_pkg my_node       # 4. run
```

### 4.6 Nuke and rebuild

`build/`, `install/`, and `log/` are 100% regenerable, so deleting them is safe and often fixes mysterious problems:

```bash
cd ~/ros2_ws
rm -rf build install log
colcon build
```

**Never do this to `src/`** — that is your actual work.

---

## 5. Packages

### 5.1 Creating one

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python my_first_pkg
```

A package is the basic unit of ROS 2 code.

### 5.2 Structure of a Python package

```
src/
└── my_first_pkg/
    ├── my_first_pkg/          ← your Python code goes here
    │   ├── __init__.py
    │   └── my_node.py
    ├── package.xml            ← metadata + dependencies
    ├── setup.py               ← build instructions, entry points
    ├── setup.cfg
    └── resource/
```

### 5.3 The two files that matter

**`package.xml`** — the package's ID card
- Name, version, maintainer
- **Dependencies** — what other packages it needs (`rclpy`, `std_msgs`, …)

**`setup.py`** — build instructions
- What to install
- **Entry points** — turns your script into a runnable node name:

```python
entry_points={
    'console_scripts': [
        'listener = my_first_node.listener:main',
    ],
},
```

Read as: *"create an executable called `listener`; when run, import module `my_first_node.listener` and call its `main` function."*

---

## 6. Python OOP for ROS

### 6.1 Why inheritance exists

Without it, shared behaviour gets written repeatedly and bugs get fixed in some places but not others.

**Core idea:** write shared behaviour **once** in a parent; write only the **differences** in the children.

### 6.2 Syntax

```python
class Parent:
    ...

class Child(Parent):     # ← Child inherits everything from Parent
    ...
```

Vocabulary (used interchangeably in docs):
- Parent = base class = superclass
- Child = derived class = subclass

### 6.3 Worked example

```python
class Drone:
    def __init__(self, name):
        self.name = name
        self.armed = False

    def arm(self):
        self.armed = True
        print(f"{self.name} armed")

    def takeoff(self):
        print(f"{self.name} taking off")


class Quadcopter(Drone):
    pass          # adds nothing — yet everything works
```

```python
q = Quadcopter("Q1")
q.arm()          # Q1 armed
q.takeoff()      # Q1 taking off
```

`Quadcopter` has no code at all, yet works — all inherited.

### 6.4 What gets inherited

- All methods of the parent
- The constructor `__init__`, **if the child does not define its own**
- Class attributes
- Inheritance is automatic — you never list what you want

**Direction matters:** inheritance flows **downward only**. Children get parents' methods; parents never get children's.

### 6.5 Adding new methods

```python
class Quadcopter(Drone):
    def spin_motors(self):
        print(f"{self.name} spinning 4 motors")
```

Now has three methods: two inherited, one its own.

### 6.6 Overriding

```python
class FixedWing(Drone):
    def takeoff(self):
        print(f"{self.name} needs a runway")
```

**The rule:** when a child defines a method with the same name as the parent's, the **child's version wins**. The parent's version isn't deleted — it just isn't the one that runs.

**Method resolution order** when calling `f.takeoff()`:
1. Look in `FixedWing` → found → use it, stop
2. (only if not found) look in `Drone`

### 6.7 `super()` — extending instead of replacing

```python
class Hexacopter(Drone):
    def takeoff(self):
        super().takeoff()                     # parent's version first
        print(f"{self.name} using 6 motors")  # then add mine
```

Output:
```
Hex1 taking off
Hex1 using 6 motors
```

### 6.8 `super().__init__()` — the critical case ⭐

**The trap:**

```python
class Hexacopter(Drone):
    def __init__(self, name, payload):
        self.payload = payload      # only this runs

h = Hexacopter("Hex1", 5)
print(h.name)     # AttributeError: no attribute 'name'
```

**Why:** the child's `__init__` **overrode** the parent's entirely. `self.name` and `self.armed` were never set. The parent's setup was silently skipped.

**The fix:**

```python
class Hexacopter(Drone):
    def __init__(self, name, payload):
        super().__init__(name)      # run parent's setup FIRST
        self.payload = payload      # then add my own
```

**Rules to memorise:**
- If the child defines `__init__`, Python does **not** call the parent's automatically
- You must call it yourself with `super().__init__(...)`
- It should be the **first** line — your setup usually depends on the parent's being done

> **Analogy — the family recipe:** Grandmother's recipe has 20 essential steps. You write your own version to add 3 steps. But writing your own version **replaces** hers entirely — those 20 steps are now gone. `super().__init__()` is the line that says *"first, do all 20 of grandmother's steps."* Without it, you're adding garnish to an empty plate.

### 6.9 `def __init__` vs `super().__init__()`

| | `def __init__(self):` | `super().__init__('name')` |
|---|---|---|
| **Action** | **Defines** a function | **Calls** a function |
| **Whose?** | Yours (the child's) | The parent's |
| **When does it run?** | Later, when an object is created | Immediately, at that line |
| **Giveaway** | `def` = defining | no `def` + `()` = calling |

### 6.10 The "is-a" test

Inheritance should express a genuine **is-a** relationship:

- A Quadcopter **is a** Drone ✅ inheritance
- A Drone **has a** battery ❌ that's *composition* — make it an attribute, not a parent

```python
isinstance(q, Quadcopter)   # True
isinstance(q, Drone)        # True  ← it IS a Drone too
```

This is exactly why `rclpy.spin(minimal_publisher)` works — your class genuinely *is* a `Node`.

---

## 7. Anatomy of a Publisher Node

### 7.1 What the program does

- Sends `"Hello World: 0"`, `1`, `2`… every 0.5 seconds
- Sends onto a **topic** (a named channel)
- Any node subscribed to that topic receives them
- **Publish/subscribe** is the core of how ROS 2 programs talk

### 7.2 Full code

```python
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    try:
        with rclpy.init(args=args):
            minimal_publisher = MinimalPublisher()
            rclpy.spin(minimal_publisher)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()
```

### 7.3 Imports

| Line | Meaning |
|---|---|
| `import rclpy` | **R**OS **C**lient **L**ibrary for **Py**thon — everything ROS in Python starts here |
| `from rclpy.executors import ExternalShutdownException` | An exception raised when ROS is shut down from *outside* the program. Imported only so it can be **caught** gracefully |
| `from rclpy.node import Node` | The `Node` base class — the most important concept in ROS 2 |
| `from std_msgs.msg import String` | Standard message type carrying a single piece of text |

**⚠️ ROS `String` ≠ Python `str`.** It is a structured container with a field inside it.

### 7.4 Class definition

```python
class MinimalPublisher(Node):
```

- `(Node)` = inherit all of ROS's node machinery
- This is why `create_publisher`, `create_timer`, and `get_logger` work despite never being written by you
- Without it: `AttributeError: 'MinimalPublisher' object has no attribute 'create_publisher'`
- **Almost every ROS 2 node you write will be a class inheriting from `Node`**

### 7.5 Constructor line by line

```python
super().__init__('minimal_publisher')
```

What this triggers inside `Node`:
- **Node registration** — announces itself; makes it visible to `ros2 node list`
- **Name assignment** — identity becomes `minimal_publisher`
- **Communication setup** — the DDS middleware participant is created
- **Namespace setup**
- **Parameter system** initialised
- **Logger creation** — makes `self.get_logger()` work
- **Interface methods activated** — `create_publisher`, `create_timer`, `create_subscription`

> Note: `'minimal_publisher'` (the ROS name) is separate from `MinimalPublisher` (the Python class name).

```python
self.publisher_ = self.create_publisher(String, 'topic', 10)
```

| Argument | Meaning |
|---|---|
| `String` | Message **type** — a promise that everything sent will be a `String`. ROS enforces this |
| `'topic'` | **Channel name.** Subscribers must use this exact same name |
| `10` | **Queue size / QoS depth.** Buffers up to 10 messages before dropping the oldest |

The trailing underscore in `publisher_` is a naming style only — no meaning to Python.

```python
timer_period = 0.5
self.timer = self.create_timer(timer_period, self.timer_callback)
```

- Fires repeatedly every 0.5 s
- **`self.timer_callback` has NO parentheses** — you are passing the function *itself* to be called later, not calling it now. Adding `()` would call it immediately, once — wrong.

```python
self.i = 0
```

- Stored on `self` so it survives **between** callbacks (a plain local variable would reset every time)

**State after `__init__` finishes:**
- Node exists, is named, is visible to ROS
- Publisher ready but has published nothing
- Timer armed but has not fired
- Counter at 0

**Nothing has run yet.** `__init__` only *prepares*.

> **Analogy:** `__init__` is the pre-flight checklist. `spin()` is the throttle.

### 7.6 The callback

```python
msg = String()
```
Creates an **empty** ROS `String` message — a container with an empty `data` field.

```python
msg.data = 'Hello World: %d' % self.i
```
- **This reveals why ROS `String` ≠ Python `str`** — you set the message's `.data` **field**, not the message itself
- `%d` gets replaced by the integer

```python
self.publisher_.publish(msg)
```
- Actually sends the message onto the `'topic'` channel
- Any subscriber receives it the moment this runs

```python
self.get_logger().info('Publishing: "%s"' % msg.data)
```
- `get_logger()` inherited from `Node`
- **Use this over `print()`** — adds timestamps and severity levels, integrates with ROS logging tools
- Purely so you can see what's being sent; not part of publishing

```python
self.i += 1
```
Increment so the next callback publishes the next number.

### 7.7 `main()`

```python
with rclpy.init(args=args):
```
- `rclpy.init()` **starts up ROS 2** for this program — must happen before any node exists
- The `with` form is a **context manager**: guarantees clean shutdown when the block ends, normally *or* via error

```python
minimal_publisher = MinimalPublisher()
```
- **Creates the node** — this is the moment `__init__` runs

```python
rclpy.spin(minimal_publisher)
```
- **Keeps the program alive and processing events**
- Without `spin`, the program would create the node, reach the end, and exit — the timer would never fire
- **Blocks** here, handling callbacks repeatedly, until Ctrl+C or shutdown

> **Mental model:** `spin` is the engine idling and responding. Remove it and the car is built but never turns on.

```python
except (KeyboardInterrupt, ExternalShutdownException):
    pass
```
- `KeyboardInterrupt` → you pressed **Ctrl+C**
- `ExternalShutdownException` → ROS shut down from outside
- `pass` = do nothing → no ugly red traceback
- **Why:** stopping with Ctrl+C is normal and expected, not a real error

```python
if __name__ == '__main__':
    main()
```
- Standard Python idiom, not ROS-specific
- Run the file **directly** → `__name__` is `'__main__'` → `main()` runs
- File **imported** by another → `__name__` is the module name → `main()` does **not** auto-run
- **Purpose:** the file can be both runnable and importable

### 7.8 Full execution flow

```
Program starts → main() runs
      ↓
rclpy.init() boots up ROS 2
      ↓
MinimalPublisher() created → node registers, publisher built,
                             timer started, counter = 0
      ↓
rclpy.spin() parks the program and keeps it responsive
      ↓
Every 0.5 s → timer fires → timer_callback runs
              → builds "Hello World: N"
              → publishes it
              → logs it
              → increments N
      ↓ (repeats forever)
Ctrl+C → KeyboardInterrupt caught → clean exit via the `with` block
```

### 7.9 Two traps to remember

- **`msg.data`, not `msg`.** ROS messages are structured containers; you fill their **fields**
- **`spin` is not optional decoration** — it's what makes an event-driven node actually run

---

## 8. Running a Node: `python3` vs `ros2 run`

```bash
# Way 1 — run the file directly
python3 ~/ros2_ws/src/my_first_node/my_first_node/listener.py

# Way 2 — run it through ROS
ros2 run my_first_node listener
```

### 8.1 What is NOT the difference ⚠️

- ❌ *"`python3` has no idea of dependencies."* **False.** `import rclpy` works fine. The node registers, publishes, and appears in `ros2 node list`. It is a **fully legitimate ROS 2 node** — there is no second-class mode.
- ❌ *"`ros2 run` makes everything ready from the ROS side."* **False.** `ros2 run` prepares *nothing*.

**The proof:**
- If `ros2 run` set up the ROS environment, then `ros2` itself would have to be findable *before* any setup happened
- But `ros2` is only findable because `PATH` was set
- And `PATH` was set by **sourcing**
- So `ros2` cannot be what enables ROS — it is itself a **product** of the environment being ready

**In an unsourced terminal, both fail:**
```bash
python3 .../listener.py     # ModuleNotFoundError: No module named 'rclpy'
ros2 run my_first_node listener   # ros2: command not found
```

> **Say it in this form: sourcing prepares; the runner only launches.**

### 8.2 The four real differences

#### Difference 1 — How the program is located

| `python3 <path>` | `ros2 run <pkg> <exe>` |
|---|---|
| You hand Python an **exact filesystem path** | You hand ROS a **package name + executable name** |
| Typo the path or wrong folder → fails | Location-independent, works from any directory |
| No concept of ROS packages — just sees a file | Looks up the package in the **ament index** via `AMENT_PREFIX_PATH`, finds the executable in `install/<pkg>/lib/<pkg>/` |

#### Difference 2 — WHICH copy of the code runs ⭐

| Method | Runs code from |
|---|---|
| `python3 ~/ros2_ws/src/.../listener.py` | **`src/`** — the file you just edited |
| `ros2 run my_first_node listener` | **`install/`** — possibly stale |

**Consequence:** edit `listener.py`, don't rebuild, run both ways:
- `python3` → shows your **new** code
- `ros2 run` → shows the **old** code

This is the source of the classic panic: *"I changed my file and nothing happened!"*

**Avoid it by:** running `colcon build` after every edit, or building once with `colcon build --symlink-install`.

#### Difference 3 — What actually calls `main()`

| `python3` | `ros2 run` |
|---|---|
| Executes file top to bottom | Runs a generated wrapper script in `install/` |
| Reaches `if __name__ == '__main__':` | Built from `entry_points` in `setup.py` |
| `__name__` **is** `'__main__'` → condition true → `main()` runs | **Imports** the module and calls `main()` directly |
| The guard block **starts your program** | `__name__` is **not** `'__main__'` → guard block **skipped entirely** |

Two completely different doors into the same function.

**Practical diagnostic:** if `ros2 run` says *"No executable found"* but `python3` works, your Python is fine — your **`setup.py` entry point** is missing or misspelled.

#### Difference 4 — Requirements

| | `python3 <path>` | `ros2 run` |
|---|---|---|
| Needs underlay sourced | Yes | Yes |
| Needs `colcon build` | **No** | **Yes** |
| Needs overlay sourced | **No** | **Yes** |
| Needs `setup.py` entry point | **No** | **Yes** |
| Needs exact file path | Yes | No |
| Runs code from | `src/` | `install/` |

`python3` has **fewer** requirements — it bypasses the whole build-and-install pipeline.

### 8.3 When to use which

**Use `python3 <path>` when:**
- Rapidly iterating on one file — edit, run, edit, run, no rebuild in the loop
- Isolating a problem: *"is my Python broken, or is my packaging broken?"*
- Fast sanity check that the logic works

**Use `ros2 run` when:**
- Verifying the package is correctly built and installed
- Doing anything real — this is the **standard, proper way**
- Using ROS arguments: `ros2 run my_first_node listener --ros-args -r __node:=my_listener`
- Preparing for **launch files**, which reference package + executable names and **cannot** use raw file paths

**Build habits around `ros2 run`** — launch files, deployment, and every tutorial assume package+executable naming. A system built on absolute file paths doesn't survive being moved to another machine.

### 8.4 Diagnostic habit ⭐

When a node misbehaves, **run it both ways**:

| Result | Diagnosis |
|---|---|
| Works with `python3`, fails with `ros2 run` | **Packaging** is broken (`setup.py`, or forgot to build) |
| Fails both ways | **Python code** is broken |

---

## 9. Command Cheat Sheet

### Environment

```bash
source /opt/ros/jazzy/setup.bash          # underlay
source ~/ros2_ws/install/setup.bash       # overlay
echo $PATH                                # inspect
printenv | grep -i ros                    # see all ROS variables
```

### Workspace

```bash
mkdir -p ~/ros2_ws/src                    # create workspace
cd ~/ros2_ws && colcon build              # build (from ROOT)
colcon build --symlink-install            # Python-friendly build
colcon build --packages-select my_pkg     # build one package only
rm -rf build install log && colcon build  # nuke and rebuild
```

### Packages

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python my_pkg
ros2 pkg list                             # all packages
ros2 pkg executables my_pkg               # what can I run from this package?
```

### Running & inspecting

```bash
ros2 run <pkg> <executable>
ros2 node list                            # running nodes
ros2 node info /minimal_publisher         # detail on one node
ros2 topic list                           # all topics
ros2 topic echo /topic                    # watch messages live
ros2 topic info /topic                    # type, publisher/subscriber count
ros2 topic hz /topic                      # publishing rate
ros2 interface show std_msgs/msg/String   # what fields does this message have?
```

### Linux basics

```bash
pwd            # where am I?
ls             # what's here?
cd ~/ros2_ws   # go somewhere
echo ~         # what does ~ expand to?
whoami         # which user am I?
cat <file>     # print a file's contents
```

---

## 10. Error → Cause Lookup

| Error | Likely cause | Fix |
|---|---|---|
| `ros2: command not found` | Underlay not sourced | `source /opt/ros/jazzy/setup.bash` |
| `ModuleNotFoundError: No module named 'rclpy'` | Underlay not sourced | Same as above |
| `Package 'my_pkg' not found` | Not built, or overlay not sourced | `colcon build` then `source install/setup.bash` |
| `No executable found` | `setup.py` entry point missing/misspelled, or not rebuilt | Check `entry_points`, then rebuild |
| Code changes have no effect | `install/` holds the old copy | `colcon build`, or use `--symlink-install` |
| `AttributeError: ... has no attribute 'create_publisher'` | Class doesn't inherit from `Node` | `class MyNode(Node):` |
| `AttributeError` on something that "should" exist | Forgot `super().__init__(...)` | Add it as the **first** line of `__init__` |
| `mkdir: cannot create directory: No such file or directory` | Parent directory doesn't exist | Use `mkdir -p` |
| Node starts then immediately exits | Missing `rclpy.spin(node)` | Add it |
| Build behaves strangely for no reason | Stale build artifacts | `rm -rf build install log && colcon build` |

---

## 11. Misconceptions Corrected

A log of things I got wrong, and the accurate version. **These are the highest-value items for recall.**

| # | I thought | Reality |
|---|---|---|
| 1 | "Ubuntu Debian 24" | Ubuntu and Debian are **different OSes**. Ubuntu is *built on* Debian. "Debian packages" refers only to the `.deb` **file format**. Correct phrasing: *"ROS 2 Jazzy on Ubuntu 24.04 using deb packages."* |
| 2 | I could dump ROS in my own folder and run commands from inside it without sourcing | **Being inside a folder does not let you run commands from it.** The shell searches `$PATH`, not your current directory (which isn't even in `$PATH` by default, for security). Sourcing is what sets those variables — skipping it means setting them all by hand |
| 3 | `-p` in `mkdir -p` declares the parent folder | `-p` = **"create any missing parent directories along this path."** It also makes re-running silent instead of erroring |
| 4 | `~` refers to the root directory | `~` is the **HOME** directory (`/home/<username>`). Root (`/`) is the top of the filesystem — a completely different place. And `/root` is a third thing: the root *user's* home |
| 5 | Root is like `C:` where software gets installed | Partly. But: (a) Linux has **one tree**, not one per drive — other drives mount *into* it; (b) there is **no single "Program Files"** — a program's parts are split by *function* across `/usr/bin`, `/usr/lib`, `/etc`, `/opt` |
| 6 | `class Name:` is the only class syntax | `class Child(Parent):` is equally valid — that's **inheritance**, standard Python. The `(Node)` in ROS code is what grants access to `create_publisher`, `create_timer`, `get_logger` |
| 7 | `def __init__` and `super().__init__()` are basically the same thing | One **defines** a function (runs later), the other **calls** the parent's (runs immediately). Defining your own `__init__` **overrides** the parent's — Python will **not** run it automatically |
| 8 | `python3 file.py` has no access to ROS dependencies; `ros2 run` sets ROS up | **Both false.** `python3` runs a fully legitimate ROS node if sourced. `ros2 run` prepares nothing — it only *finds and launches*. **Sourcing** is the only thing that prepares the environment |

---

## Next Topics

- [ ] Subscriber node (`create_subscription`) — the receiving half of pub/sub
- [ ] Running publisher + subscriber together
- [ ] Custom message types (`.msg` files)
- [ ] Services (request/response, vs topics' one-way stream)
- [ ] Parameters
- [ ] Launch files
- [ ] QoS settings in depth
- [ ] `tf2` / transforms
