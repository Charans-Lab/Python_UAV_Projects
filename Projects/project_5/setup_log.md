# Learning Notes
### This file contains new learnings from this project.

---

## Project 5 — Classes and OOP

**Plan:** Refactor Project 4 (`mission.py`) into a class-based design.  
Same functionality, different structure. The goal is learning OOP in a context you already understand.

### Resources
- [Real Python — OOP in Python 3](https://realpython.com/python3-object-oriented-programming/) — clear and practical
- [Python Official Tutorial — Section 9: Classes](https://docs.python.org/3/tutorial/classes.html) — the canonical reference
- YouTube — Corey Schafer's "Python OOP Tutorial 1: Classes and Instances" and "Tutorial 2: Class Variables" (~40 minutes total)

---

### Q1 — What's the difference between a class and an instance?

A class is a **blueprint** and an instance is what we **build using the blueprint**.

**Example:**  
To build a house I need a design. Based on this design I can build N number of houses.  
The design is the **class** and those N houses are called **instances**.

> **Note:** Each instance will have unique values. For example, the N houses share the same design (class) but the colour, location, and size will differ for each instance.

```python
class House:                        # blueprint (class)
    def __init__(self, color, location):
        self.color = color
        self.location = location

house1 = House("Red", "Mumbai")     # instance 1
house2 = House("Blue", "Pune")      # instance 2
# same blueprint, different values!
```

---

### Q2 — What does `self` mean and why is it there?

`self` refers to the **current instance** of the class.  
When you access any particular object, `self` represents that specific object.

**Why is it there?**  
When you call a method on an instance, Python needs to know **which instance** to work on. `self` is how Python passes that information automatically.

```python
class Drone:
    def __init__(self, name):
        self.name = name        # self = this particular drone object

drone1 = Drone("Alpha")
drone2 = Drone("Beta")

# When drone1.land() is called, self = drone1
# When drone2.land() is called, self = drone2
# self tells Python WHICH drone to act on!
```

> **Note:** You don't pass `self` manually when calling a method — Python passes it automatically behind the scenes.

---

### Q3 — What's `__init__` and when does it run?

`__init__` is a **special method** (also called a constructor) used to assign initial values to every object when it is created.  
It runs **automatically as soon as the object is created**.

```python
class Drone:
    def __init__(self, name, altitude):  # runs automatically on creation
        self.name = name
        self.altitude = altitude

drone1 = Drone("Alpha", 100)    # __init__ runs HERE automatically
# drone1.name = "Alpha"
# drone1.altitude = 100
```

> **Analogy:** `__init__` is like a **registration form** that gets filled automatically every time a new instance is born.

---

### Q4 — What's the difference between an attribute and a method?

- **Attribute** — A variable that **holds a value** inside an instance.
- **Method** — A **function defined inside a class** that performs a task on the instance.

```python
class Drone:
    def __init__(self, name, altitude):
        self.name = name          # attribute — stores a value
        self.altitude = altitude  # attribute — stores a value

    def fly(self):                # method — performs a task
        print(f"{self.name} is flying at {self.altitude}m")

drone1 = Drone("Alpha", 50)
print(drone1.name)    # accessing attribute → "Alpha"
drone1.fly()          # calling method → "Alpha is flying at 50m"
```

| | Attribute | Method |
|---|---|---|
| What it is | A variable | A function |
| What it does | Stores data | Performs an action |
| How to access | `drone1.name` | `drone1.fly()` |

---

### Q5 — Why use a class instead of just functions and dictionaries?

**Reason 1 — Data and behavior live together (Encapsulation)**  
In the dictionary version, the data (drone state) is in one place and the functions are scattered elsewhere. With classes, they are bundled together. The drone "knows" how to take off. This is called **encapsulation**.

**Reason 2 — You can't accidentally pass the wrong thing**  
In the dict version, you could write `takeoff(some_other_dict, 10)` and Python wouldn't complain until something inside crashed. With a class, `some_other_dict.takeoff(10)` doesn't exist — you'd get an error immediately.

**Reason 3 — Classes scale when you have many similar things**  
Imagine a swarm of 10 drones. With dicts, you have 10 dicts and a bunch of free-floating functions that each take "which drone." With classes, you have 10 drone instances and each one carries its own behavior. Much cleaner.

```python
# Dict version — messy ❌
drone1 = {"name": "Alpha", "altitude": 0}
drone2 = {"name": "Beta", "altitude": 0}
takeoff(drone1, 50)   # which dict? easy to mix up!

# Class version — clean ✅
drone1 = Drone("Alpha")
drone2 = Drone("Beta")
drone1.takeoff(50)    # drone1 knows its own takeoff!
drone2.takeoff(30)
```

**Reason 4 — You can use Inheritance**  
A `QuadcopterDrone` and a `FixedWingDrone` might share most behavior but differ in some specifics. Classes let you express this naturally — both inherit from `Drone` but override specific methods. You can't do this cleanly with dicts and functions.

```python
class Drone:            # parent class
    def takeoff(self):
        print("Taking off...")

class QuadcopterDrone(Drone):   # inherits from Drone
    def takeoff(self):
        print("Quadcopter taking off vertically!")

class FixedWingDrone(Drone):    # inherits from Drone
    def takeoff(self):
        print("Fixed wing taking off on runway!")
```

**Reason 5 — The practical one (Most important for your career path)**  
ROS 2 nodes are classes. Most robotics frameworks are class-based. SLAM, MAVSDK's higher-level abstractions, OpenCV's image processing pipelines — all class-based. If you can't write classes, you can't participate in the ecosystem. **This is not optional for your career path.**

---

### Quick Cheat Sheet

```python
class Drone:                            # class = blueprint
    def __init__(self, name):           # __init__ = runs on creation
        self.name = name                # self = this specific instance
                                        # name = attribute (stores value)

    def fly(self):                      # fly = method (performs task)
        print(f"{self.name} is flying")

drone1 = Drone("Alpha")                 # instance 1
drone2 = Drone("Beta")                  # instance 2
drone1.fly()                            # Alpha is flying
drone2.fly()                            # Beta is flying
```

| Term | Meaning | Example |
|---|---|---|
| Class | Blueprint | `class Drone:` |
| Instance | Object built from blueprint | `drone1 = Drone("Alpha")` |
| `self` | Refers to current instance | `self.name` |
| `__init__` | Runs automatically on creation | `def __init__(self, name):` |
| Attribute | Variable inside instance | `self.name = name` |
| Method | Function inside class | `def fly(self):` |


----------------------------
# warings in code:
```
Received ack for not-existing command: 176! Ignoring... (mavlink_command_sender.cpp:304)
```
Reason 1 — Timing issue
Command was sent → drone took too long to reply
MAVSDK moved on → reply arrived late
MAVSDK says "I don't remember sending this!" → ignores it

Reason 2 — Simulator behaviour
PX4 simulator sometimes sends extra acknowledgements
that don't match any pending command

Reason 3 — Duplicate ack
Drone sent the same acknowledgement twice
Second one arrives → MAVSDK already processed first one