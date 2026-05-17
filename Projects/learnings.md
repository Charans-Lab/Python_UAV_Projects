# Learning Notes
### This file contains new learnings from this project.

---

## 1. File Reading

In Python, to read a file we use the built-in function called [open()](https://www.w3schools.com/python/python_file_open.asp).

Consider a file with the following content:
```
Hi, this is a sample text for my file.
```

> **Note:** To open a file, use the built-in `open()` function.  
> The `open()` function returns a **file object**, which has a `read()` method for reading the content of the file.

### Basic Example
```python
f = open("D:\\myfiles\\welcome.txt")
print(f.read())
```
This will open the file and read the data.

> ⚠️ **Problem:** This code will **not close the file** after reading.  
> Leaving a file open results in **memory usage** and can **slow down** operations.

---

### Better Approach — Using the `with` Statement

Using the `with` statement, the file will open and read, and upon completion the file is **automatically closed**.

```python
with open("demofile.txt") as f:
    print(f.read())
```

✅ No need to manually close the file — `with` handles it!

---

### Output Type

> **Note:** The output of `file.read()` is of type **string**.  
> This means all the data inside the file will be read as one single string.

To convert the output to a **list** (one item per line), use `.splitlines()`:

```python
with open("/home/sai/py_uav/py_projects/Projects/project_4/geo location file.txt") as file:
    # mission_coordinates = file.read()             # returns a string
    mission_coordinates = file.read().splitlines()  # returns a list
print(mission_coordinates)
```

**Output:**
```
['1 47.3975396 8.5472023 90', '2 47.3975396 8.5472023 90', '3 47.3973713 8.5455290 90']
```

| Method | Returns | Example Output |
|---|---|---|
| `file.read()` | Single string | `'1 47.39...\n2 47.39...'` |
| `file.read().splitlines()` | List (strips `\n`) | `['1 47.39...', '2 47.39...']` |
| `file.readlines()` | List (keeps `\n`) | `['1 47.39...\n', '2 47.39...\n']` |

---

## 2. Asyncio

### What Problem Does It Solve?

In normal Python, tasks run **one after another** (line by line).  
This means if one task is waiting (e.g. network call, sleep), everything else also waits.

`asyncio` solves this by allowing tasks to run **concurrently** — while one task is waiting, another can run.

> 🍵 **Analogy:** Like a waiter in a restaurant — instead of waiting at Table 1 for food to arrive, he takes orders from Table 2 and Table 3 while Table 1's food is being prepared.

---

### Key Terms

| Term | Simple Meaning |
|---|---|
| **Synchronous** | Tasks run one after another |
| **Asynchronous** | Tasks run concurrently (overlapping) |
| **Coroutine** | A special function that can pause and resume |
| **Event Loop** | The manager that runs and schedules all tasks |
| **`async`** | Makes a function a coroutine |
| **`await`** | Pauses the current task and lets others run |

---

### Normal Python vs Asyncio

```python
# NORMAL — strict line by line
import time

def make_tea():
    print("Making tea...")
    time.sleep(3)           # waits 3 sec, blocks everything
    print("Tea ready!")

def make_coffee():
    print("Making coffee...")
    time.sleep(3)           # waits 3 sec, blocks everything
    print("Coffee ready!")

make_tea()
make_coffee()
# Total time = 3 + 3 = 6 seconds ❌
```

```python
# ASYNCIO — concurrent
import asyncio

async def make_tea():
    print("Making tea...")
    await asyncio.sleep(3)  # pauses tea, lets others run
    print("Tea ready!")

async def make_coffee():
    print("Making coffee...")
    await asyncio.sleep(3)  # pauses coffee, lets others run
    print("Coffee ready!")

async def main():
    await asyncio.gather(make_tea(), make_coffee())

asyncio.run(main())
# Total time = 3 seconds ✅
```

---

### Core Building Blocks

#### `async def` — Making a Coroutine
Adding `async` before `def` makes the function a **coroutine**.  
A coroutine does **not run immediately** when called — it needs the Event Loop to run it.

```python
async def greet():
    print("Hello!")

greet()         # ❌ Does nothing! Just creates a coroutine object
                # needs Event Loop to actually run
```

---

#### `await` — Pause and Resume
- `await` **pauses** the current coroutine.
- While paused, the **Event Loop runs other tasks**.
- When the awaited task is done, the **Event Loop resumes** this coroutine.

```python
async def main():
    print("Start")
    await asyncio.sleep(2)  # pause here for 2 sec, let others run
    print("End")            # resumes after 2 sec
```

> ⚠️ **Rule:** `await` can **only be used inside** an `async def` function.  
> By the time `await` is hit, the Event Loop is **already running** — `await` does NOT create the Event Loop!

---

#### `asyncio.run()` — Creates the Event Loop
This is the **entry point** of the async world.

```python
asyncio.run(main())
```

What it does step by step:
```
Step 1 → Creates the Event Loop (the Manager) 🟢
Step 2 → Hands main() to the Event Loop
Step 3 → Event Loop runs main()
Step 4 → When main() finishes → destroys the Event Loop 🔴
```

> ✅ `asyncio.run()` is the **only** thing that creates the Event Loop.  
> ✅ Call it **once** at the top level of your program.

---

#### `asyncio.gather()` — Run Multiple Tasks Together

```python
async def main():
    await asyncio.gather(make_tea(), make_coffee())
```

- Runs **all tasks at the same time** (concurrently).
- **Waits for all of them** to finish before moving forward.
- Without `await` on `gather()`, the tasks never actually run!

```python
# Without await ❌
async def main():
    asyncio.gather(make_tea(), make_coffee())
    print("done!")  # prints immediately, tea/coffee never made!

# With await ✅
async def main():
    await asyncio.gather(make_tea(), make_coffee())
    print("done!")  # prints only AFTER both tea and coffee are ready
```

---

### The Event Loop — The Manager

The Event Loop is created by `asyncio.run()` and is the **heart of asyncio**.  
It constantly watches all tasks and decides who runs next.

```
asyncio.run()  =  Hiring the Manager 👨‍💼
await          =  Worker telling Manager "I'm on a break, run others!"
Event Loop     =  Manager deciding who works next
```

**Full flow of how it all connects:**

```
asyncio.run(main())
        │
        ▼
Event Loop STARTS 🟢
        │
        ▼
runs main()
        │
        ▼
hits → await asyncio.gather(make_tea(), make_coffee())
                │
                ▼
         starts make_tea()
                │
         hits → await asyncio.sleep(3)
                │
                ├──► signals Event Loop: "I am pausing!"
                ▼
         Event Loop starts make_coffee()
                │
         hits → await asyncio.sleep(3)
                │
                ├──► signals Event Loop: "I am pausing!"
                │
         Event Loop watches both...
                │
         (3 seconds pass)
                │
                ▼
         Event Loop resumes make_tea()  ✅
         Event Loop resumes make_coffee() ✅
                │
                ▼
         main() finishes
                │
                ▼
Event Loop STOPS 🔴
```

---

### How `await` Interacts with the Event Loop

> ❓ **Doubt:** How can `await` signal the Event Loop if it doesn't create it?

**Answer:** By the time any `await` is hit, the Event Loop is **already alive** (created by `asyncio.run()`).  
`await` simply **signals** the already-running Event Loop — it never creates it.

```
WRONG THINKING:
await → creates Event Loop → runs task   ❌

CORRECT THINKING:
asyncio.run()  → creates Event Loop 🟢
                        │
                        └── runs main()
                                │
                                └── await hits
                                        │
                                        └── signals EXISTING Event Loop ✅
```

---

### Execution Order Inside `asyncio.gather()`

> ❓ **Doubt:** Which function runs first inside `gather()`? Python is line by line right?

`make_tea()` does start **first**, but the moment it hits `await`, it **steps aside** and `make_coffee()` starts immediately.

```
Time        make_tea()              make_coffee()
──────────────────────────────────────────────────
0.0000s  →  starts ▶️
0.0001s  →  hits await ⏸️           starts ▶️
0.0002s  →  sleeping 😴              hits await ⏸️
0.0002s  →  sleeping 😴              sleeping 😴
3.0001s  →  wakes up ✅
3.0002s  →                           wakes up ✅
```

The gap between them is **microseconds** — so small it feels simultaneous!

---

### Common Mistakes

```python
# ❌ Forgetting await on sleep
async def main():
    asyncio.sleep(2)          # nothing happens!
    await asyncio.sleep(2)    # ✅ correct

# ❌ Using await outside async function
def main():
    await asyncio.sleep(2)    # SyntaxError!

async def main():
    await asyncio.sleep(2)    # ✅ correct

# ❌ Using time.sleep() instead of asyncio.sleep()
async def main():
    time.sleep(2)             # blocks everything!
    await asyncio.sleep(2)    # ✅ correct — lets others run
```

---

### Quick Reference Table

| Code | What it does |
|---|---|
| `async def fn()` | Makes `fn` a coroutine |
| `fn()` | Creates coroutine object, does NOT run it |
| `await fn()` | Actually runs `fn` (only inside `async def`) |
| `asyncio.run(fn())` | Creates Event Loop and runs `fn` |
| `asyncio.gather(a(), b())` | Runs `a` and `b` concurrently |
| `await asyncio.sleep(n)` | Pauses task for `n` seconds, lets others run |
| `time.sleep(n)` | Blocks everything for `n` seconds ❌ |

---

### When to Use Asyncio

| Use Asyncio ✅ | Don't Use Asyncio ❌ |
|---|---|
| Fetching data from APIs | Heavy math/calculations |
| Reading/writing files | Simple single-task scripts |
| Database queries | CPU-intensive work |
| Web scraping | (use `multiprocessing` instead) |
| Drone telemetry / MAVLink communication | |