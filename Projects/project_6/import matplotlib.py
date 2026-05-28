import matplotlib.pyplot as plt

time     = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
altitude = [0, 2, 4, 7, 9, 9.8, 10, 10, 9.5, 5, 0]
speed    = [0, 2, 4, 5, 5, 5,   5,  4,  3,   2, 0]
battery  = [100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90]

# Step 1 — add label to EACH plot
plt.plot(time, altitude, color="blue",   label="Altitude (m)")   # ✅ label
plt.plot(time, speed,    color="green",  label="Speed (m/s)")    # ✅ label
plt.plot(time, battery,  color="orange", label="Battery (%)")    # ✅ label

# Step 2 — call legend ONCE — collects all labels!
plt.legend()

plt.title("Drone Mission Telemetry")
plt.xlabel("Time (seconds)")
plt.grid(True)
plt.show()