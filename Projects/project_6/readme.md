# Project 6 — Sensor Data with NumPy (`IMUAnalyzer`)

**Goal:** Stop handling sensor values one at a time. Start treating them as *arrays of numbers you can do math on*. This is the mental shift behind every VIO, SLAM, and computer-vision system — they all process batches of sensor data with NumPy (or its C++ equivalent, Eigen).

This is the **last Python prerequisite before ROS 2**.

---

## Why this project matters

- **NumPy is non-negotiable for perception work.** Point clouds, images, rotation matrices, sensor batches — all NumPy arrays.
- **You will see real sensor noise for the first time.** The accelerometer doesn't read exactly 9.81 — it jitters. Understanding sensor noise is the entire reason the EKF (Extended Kalman Filter) exists. This connects directly back to the `is_global_position_ok` health check from Project 4/5.
- **It combines everything you've learned:** classes (Project 5), async telemetry (Phase 2 of Project 4), plotting (Project 3), plus the new piece — NumPy.

---

## Prerequisite reading (~2 days, before any code)

Read **"NumPy: the absolute basics for beginners"** at numpy.org.

Stop when you can answer these four questions in your own words (write them in `setup_log.md`):

1. What is an `ndarray`, and how is it different from a Python list?
2. What does "vectorized operation" mean — why is `np.mean(arr)` better than a `for` loop that sums and divides?
3. What is an array's `shape`? What's the shape of 200 IMU readings, each with x/y/z?
4. How do you compute a statistic along one axis (mean of each column) vs over the whole array?

### Anchor concept
A Python list of 200 readings is 200 separate objects scattered in memory. A NumPy array of 200 readings is **one contiguous block** you do math on all at once. At 200 Hz, that difference is "keeps up" vs "falls behind."

### Key NumPy facts to internalize
- **Uniform type → contiguous memory → speed.** A list holds pointers scattered in memory and type-checks each element; an array holds the actual numbers in one block, handed straight to optimized C / CPU vector instructions.
- **`axis` argument** (the #1 NumPy confusion — don't memorize, *test it and see*):
  ```python
  data = np.array(...)        # shape (200, 3)
  np.mean(data, axis=0)       # mean of each COLUMN -> 3 values [mean_x, mean_y, mean_z]
  np.mean(data, axis=1)       # mean of each ROW -> 200 values
  np.mean(data)               # mean of everything -> 1 value
  ```
  Mental model: `axis=0` operates **down the columns**, `axis=1` operates **across the rows**.
- **Column slicing:** `data[:, 0]` = "every row, column 0". Core NumPy you'll use forever.

---

## The build — incremental, same as Project 5

Build it as a **class** called `IMUAnalyzer`, one method at a time. Don't write the whole thing at once.

### Step 1 — Collect the data (no analysis yet)

Create `Project-6/imu_analyzer.py`. Write `__init__`, `connect()`, and `collect_imu()`.

Goal: connect to SITL, pull `num_samples` IMU readings, store them in `self.accel_samples` as a list of `[forward, right, down]`, then print the count and the first few. **No NumPy yet.**

The IMU stream is `drone.telemetry.imu()`. Each reading has an `acceleration_frd` field with `.forward_m_s2`, `.right_m_s2`, `.down_m_s2` (FRD = Forward-Right-Down, the drone's body frame).

```python
import asyncio
from mavsdk import System

class IMUAnalyzer:
    def __init__(self, num_samples):
        self.drone = System()
        self.num_samples = num_samples
        self.accel_samples = []

    async def connect(self):
        # reuse your Project 5 connection code
        ...

    async def collect_imu(self):
        async for imu in self.drone.telemetry.imu():
            accel = imu.acceleration_frd
            self.accel_samples.append(
                [accel.forward_m_s2, accel.right_m_s2, accel.down_m_s2]
            )
            if len(self.accel_samples) >= self.num_samples:
                break

    async def run(self):
        await self.connect()
        await self.collect_imu()
        print(f"Collected {len(self.accel_samples)} samples")
        print(self.accel_samples[:5])   # eyeball the first 5

async def main():
    analyzer = IMUAnalyzer(200)
    await analyzer.run()

asyncio.run(main())
```

**What to observe:** With the drone sitting still, `forward` and `right` should be near zero. `down` should be about -9.8 — that's gravity. Read the numbers and confirm.

### Step 2 — Measure gravity with NumPy

Add `import numpy as np` and write `analyze()`. **This is a regular method, not async** — it's pure computation on data you already have, no waiting on I/O.

It should:
1. Convert `self.accel_samples` into a NumPy array. Print its `shape` — confirm `(200, 3)`.
2. Compute the mean of each axis with `axis=0` → `[mean_forward, mean_right, mean_down]`.
3. Compute the standard deviation of each axis with `axis=0` → quantifies the noise.
4. Compute the **magnitude** of the mean acceleration vector: `sqrt(forward² + right² + down²)` → should be ~9.8 (gravity, regardless of axis).

```python
def analyze(self):
    self.data = np.array(self.accel_samples)
    print(f"Data shape: {self.data.shape}")

    mean_per_axis = np.mean(self.data, axis=0)
    std_per_axis = np.std(self.data, axis=0)

    print(f"Mean acceleration per axis (F,R,D): {mean_per_axis}")
    print(f"Std dev per axis (F,R,D): {std_per_axis}")

    gravity_magnitude = np.sqrt(np.sum(mean_per_axis ** 2))
    print(f"Measured gravity magnitude: {gravity_magnitude:.4f} m/s^2")
```

Call it in `run()` after `collect_imu()` (no `await` — it's a regular method).

**Expected output:**
- shape `(200, 3)`
- mean down ~-9.8, mean forward/right ~0 (printed in scientific notation, e.g. `-5.6e-03` = -0.0056 — **always read the exponent**)
- tiny std values (~0.004 in sim) — this is the sensor noise
- **gravity magnitude ~9.8** — your code measuring a fundamental constant

**Reflection to write down:** Which axis is noisiest? How large is the noise compared to the signal (~9.8 on the down axis)? That signal-to-noise ratio (~2000:1 in sim, far worse on real hardware) is exactly why the EKF exists.

### Step 3 — Plot it

Add a `plot()` method (regular `def`, not async) using matplotlib (reuse Project 3 skills).

- X-axis: sample number (0 to `num_samples-1`)
- Y-axis: acceleration
- Three lines: forward, right, down — different colors, with a legend
- Title, axis labels
- **Save first, then show:** `fig.savefig("imu_plot.png")` BEFORE `plt.show()` (avoids saving a blank image on some setups). Always include the file extension.

Column extraction:
```python
forward = self.data[:, 0]   # all rows, column 0
right   = self.data[:, 1]
down    = self.data[:, 2]
```

**What you'll see:** the down line flat at ~-9.8, forward/right near zero, tiny wiggles (the noise). At normal zoom the lines look perfectly flat — that *is* the 2000:1 signal-to-noise ratio made visual. To actually see the noise, plot just the down axis zoomed to a y-range like -9.79 to -9.82.

---

## Code quality checklist (the habits)

- [ ] Use descriptive variable names — `forward`, `right`, `down`, NOT `y`, `k`, `l`. (`l` looks like the digit `1`.)
- [ ] `analyze()` and `plot()` are regular methods (`def`), not `async`. Async is only for things that wait on I/O.
- [ ] `savefig()` BEFORE `show()`, and include the `.png` extension.
- [ ] No leftover commented-out debug prints. Git remembers history — you don't need commented graveyards.
- [ ] Declare all attributes in `__init__` (no stray `pass`).
- [ ] **Run the code and look at the output / plot before calling it done.**

---

## Definition of done

- [ ] Prerequisite reading complete; four NumPy questions answered in `setup_log.md`
- [ ] `IMUAnalyzer` collects 200 samples, analyzes them, measures gravity ~9.8, and plots all three axes
- [ ] Code is clean (checklist above)
- [ ] Committed and pushed: `"Project 6: IMU analysis with NumPy — measured gravity from sensor noise"`
- [ ] README updated to list Project 6

---

## What this unlocks

After Project 6 you've hit every Python prerequisite for ROS 2:
**classes, async/await, concurrency (`asyncio.gather`), NumPy arrays, real sensor data, and visualization.**

Next: **Project 7 — your first ROS 2 node.** A ROS 2 node is a class with `__init__`, methods, and a `main()` that instantiates it — exactly the shape you built in Projects 5 and 6.