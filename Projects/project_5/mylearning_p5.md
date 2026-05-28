# Project 5 — Learning Notes
### OOP, Class-Based Drone Mission, Debugging

---

## 1. OOP Basics — Classes and Instances

A **class** is a blueprint and an **instance** is what we build using the blueprint.

```python
class House:                          # blueprint (class)
    def __init__(self, color, location):
        self.color = color
        self.location = location

house1 = House("Red", "Mumbai")       # instance 1
house2 = House("Blue", "Pune")        # instance 2
# same blueprint, different values!
```

> Each instance has **unique values** — same design, different colour and location.

---

## 2. Key OOP Terms

| Term | Meaning | Example |
|---|---|---|
| Class | Blueprint | `class Drone:` |
| Instance | Object built from blueprint | `drone1 = Drone("Alpha")` |
| `self` | Refers to current instance | `self.name` |
| `__init__` | Runs automatically on creation | `def __init__(self, name):` |
| Attribute | Variable that stores value inside instance | `self.name = name` |
| Method | Function defined inside class | `def fly(self):` |

---

## 3. `self` — What It Means and Why It Is There

`self` refers to the **current instance** of the class. Python passes it **automatically** — you never pass it manually when calling a method.

```python
class Drone:
    def __init__(self, name):
        self.name = name

    def fly(self):
        print(f"{self.name} is flying")   # self knows WHICH drone

drone1 = Drone("Alpha")
drone2 = Drone("Beta")
drone1.fly()    # self = drone1 → "Alpha is flying"
drone2.fly()    # self = drone2 → "Beta is flying"
```

---

## 4. `__init__` — The Constructor

`__init__` is a **special method** that runs **automatically** as soon as an object is created. It assigns initial values to the instance.

```python
class Drone:
    def __init__(self, name, altitude):
        self.name = name          # assigned on creation
        self.altitude = altitude  # assigned on creation

drone1 = Drone("Alpha", 100)    # __init__ runs HERE automatically
```

> ⚠️ **Common Typo:** `__int__` vs `__init__`  
> `__int__` = Python's convert-to-integer method  
> `__init__` = constructor that runs on object creation  
> **Always double check the spelling!**

---

## 5. Sharing Data Between Methods Using `self`

Variables inside a method are **local** — they die when the method ends.  
To share data between methods, store it in `self`.

```python
class DroneMission:
    def __init__(self):
        self.waypoints = []         # empty, shared across all methods

    def load_waypoints(self):
        self.waypoints = ["p1", "p2", "p3"]   # stored in self ✅

    def fly_mission(self):
        for point in self.waypoints:           # reads from self ✅
            print(f"flying to {point}")
```

> Think of `self` as a **shared notebook** — all methods can read and write to it!

| Where data lives | Who can see it |
|---|---|
| Normal variable inside method | Only that method |
| `self.variable` | ALL methods of that instance |

---

## 6. Calling Methods — Inside vs Outside Class

```python
# From OUTSIDE the class
alpha = DroneMission("waypoints.txt")
alpha.load_waypoints()        # use instance name

# From INSIDE the class (one method calling another)
def run_mission(self):
    self.load_waypoints()     # use self
    self.fly_mission()
```

---

## 7. Master Method Pattern

Instead of calling 10 methods manually, create ONE master method:

```python
class DroneMission:
    def load_waypoints(self): ...
    def build_mission(self): ...
    def connect(self): ...
    def fly(self): ...

    def run_mission(self):        # master method
        self.load_waypoints()
        self.build_mission()
        self.connect()
        self.fly()

# Only ONE call needed!
alpha = DroneMission("waypoints.txt")
alpha.run_mission()    # ✅ runs everything in order!
```

---

## 8. Single Responsibility Principle

Each method should do **ONE job only**!

```python
# ❌ Bad — one method doing two jobs
def load_waypoints(self):
    # loads waypoints
    # also checks altitude  ← should NOT be here!

# ✅ Good — each method one job
def load_waypoints(self):
    # ONLY loads waypoints

def check_altitude(self, altitude, waypoint_number):
    # ONLY checks altitude
    if altitude > self.DGCA_ALTITUDE_LIMIT_M:
        print(f"waypoint {waypoint_number} exceeds DGCA limit!")
```

> **Benefits:** Reusable, readable, easy to grow, easy to debug!

---

## 9. Why Use Classes Instead of Functions and Dictionaries?

| Reason | Explanation |
|---|---|
| **Encapsulation** | Data and behavior live together |
| **Safety** | Can't accidentally pass wrong thing |
| **Scale** | 10 drone instances each carry their own behavior |
| **Inheritance** | Share behavior, override specifics |
| **Career** | ROS2, MAVSDK, OpenCV — all class-based! |

---

## 10. `async def` Inside a Class

When a class method uses `await`, it **must be** `async def`:

```python
class DroneMission:
    async def connection_to_drone(self):     # ✅ async def
        await self.drone.connect(...)        # await works here!

    async def run(self):
        await self.connection_to_drone()     # ✅ await + ()
```

> `async def` does NOT create the Event Loop — it just makes `await` legal inside that method!  
> The Event Loop is already running from `asyncio.run()` at the top level.

---

## 11. Referencing vs Calling — The Most Common Mistake!

```python
# ❌ Referencing — does nothing!
self.load_waypoints       # just points to the method
await self.connection_to_drone    # TypeError!

# ✅ Calling — actually runs it!
self.load_waypoints()     # () executes the method
await self.connection_to_drone()  # () executes the coroutine
```

> **Golden Rule:** If you want to RUN a method — always add `()`!  
> Without `()` you are just talking ABOUT the method, not running it!

---

## 12. `async for` vs `async def` — Different Things!

```python
async def check_health(self):           # makes function pauseable
    async for health in self.drone.telemetry.health():   # handles live stream
        if health.is_global_position_ok:
            break
```

| Keyword | Purpose |
|---|---|
| `async def` | Makes the **function** pauseable — allows `await` inside |
| `async for` | Handles a **live stream** of data arriving continuously |

> `telemetry.health()`, `telemetry.altitude()`, `core.connection_state()` — all live streams → always use `async for`!

---

## 13. Sequential vs Concurrent in Class Methods

```python
# Sequential — execute_mission finishes FIRST, then monitor starts ❌
async def run(self):
    await self.execute_mission()    # waits until done
    await self.mission_monitor()    # starts too late! misses early progress

# Concurrent — both start at the same time ✅
async def run(self):
    await asyncio.gather(
        self.execute_mission(),
        self.mission_monitor()
    )
```

> When using `asyncio.gather()` inside a class — always use `self.method()` not just `method()`!

---

## 14. Float Comparison with Telemetry Data

Never use `==` for comparing drone telemetry values — they are floats!

```python
# ❌ Will never match exactly!
if alt.altitude_relative_m == target_altitude:

# ✅ Use >= instead
if alt.altitude_relative_m >= target_altitude:
    print("altitude reached!")
    break
```

> Real drone altitude readings are like `9.9999`, `10.0021` — never exactly `10.0000`!

---

## 15. MAVSDK Mission Methods Learned

| Method | What it does |
|---|---|
| `drone.action.arm()` | Arms the drone |
| `drone.action.takeoff()` | Sends takeoff command |
| `drone.action.land()` | Sends land command |
| `drone.action.set_takeoff_altitude(n)` | Sets takeoff altitude |
| `drone.mission.upload_mission(plan)` | Uploads mission to drone |
| `drone.mission.clear_mission()` | Clears existing mission from drone |
| `drone.mission.start_mission()` | Starts the uploaded mission |
| `drone.mission.set_return_to_launch_after_mission(True)` | RTL after mission |
| `drone.mission.mission_progress()` | Live stream of mission progress |

> ⚠️ `set_takeoff_altitude()` only **sets** the value — it does NOT make drone fly!  
> You still need `drone.action.takeoff()` to actually lift off!

---

## 16. Always Clear Old Mission Before Uploading

```python
async def upload_mission(self):
    await self.drone.mission.clear_mission()    # ✅ clears old mission first!
    await asyncio.sleep(2)                      # small delay for safety
    await self.drone.mission.upload_mission(self.mission_plan)
```

> Without clearing — drone may execute **old stored mission** from previous run!

---

## 17. File Path Using `pathlib`

```python
from pathlib import Path

# ✅ Best practice — finds file relative to script location
waypoints_file = Path(__file__).parent / "waypoints.txt"

# __file__  = full path of current script
# .parent   = folder that contains the script
# / "waypoints.txt" = adds filename to that folder
```

| Code | Meaning |
|---|---|
| `Path(__file__)` | Current script's full path |
| `Path(__file__).parent` | Folder containing the script |
| `Path("folder/").parent` | Go UP one folder level |
| `Path("folder/") / "file.txt"` | folder/file.txt |

---

## 18. Always Sanitize Input Files

Real world files are messy — always handle empty lines!

```python
# ❌ Crashes if file has empty lines at end
for line in waypoints:
    number, lat, lon, alt = line.split()   # ValueError if line is empty!

# ✅ Filter empty lines first
with open(self.waypoints_location) as file:
    waypoints = [line for line in file.read().splitlines() if line.strip()]
```

> Even a single invisible empty line at end of file will crash your code!  
> Always sanitize input before processing!

---

## 19. Common Errors Encountered and Fixed

| Error | Cause | Fix |
|---|---|---|
| `TypeError: DroneMission() takes no arguments` | `__int__` instead of `__init__` | Fix spelling → `__init__` |
| `TypeError: object method can't be used in await` | Missing `async` on method or missing `()` | Add `async def` and `()` |
| `TypeError: async for requires __aiter__` | Missing `()` on async generator | Add `()` to method call |
| `ValueError: not enough values to unpack` | Empty line in input file | Filter empty lines |
| Mission completed instantly | Old mission stored in drone | Call `clear_mission()` first |
| Mission progress skipping | `monitor` starts after `execute` | Use `asyncio.gather()` |
| `await` outside `async def` | `await` in normal function | Change to `async def` |

---

## 20. Final Working Class Structure

```python
class DroneMission:
    def __init__(self, waypoints_location):
        self.waypoints_location = waypoints_location
        self.waypoints = []
        self.mission_plan = None
        self.MISSION_SPEED_MS = 10.0
        self.DGCA_ALTITUDE_LIMIT_M = 120

    def load_waypoints(self): ...        # reads and parses waypoints file
    def check_altitude(self, ...): ...   # validates DGCA altitude limit
    def build_mission_plan(self): ...    # builds MissionPlan object

    async def connection_to_drone(self): ...  # connects to drone
    async def check_health(self): ...         # waits for GPS health
    async def upload_mission(self): ...       # clears + uploads mission
    async def execute_mission(self): ...      # arms + starts mission
    async def mission_monitor(self): ...      # monitors live progress

    async def run(self):                      # master method
        self.load_waypoints()
        self.build_mission_plan()
        await self.connection_to_drone()
        await self.check_health()
        await self.upload_mission()
        await asyncio.gather(               # concurrent! ✅
            self.execute_mission(),
            self.mission_monitor()
        )
```