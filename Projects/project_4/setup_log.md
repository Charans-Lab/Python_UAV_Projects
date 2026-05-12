## [flight modes(Multicopter)](https://docs.px4.io/main/en/flight_modes_mc/)

# Overview

Flight Modes are either manual or autonomous. Manual modes provide different levels of autopilot support when flying manually (using RC control sticks or a joystick), while autonomous modes can be fully controlled by the autopilot.

# manual-Easy modes in px4:
* [Position mode](https://docs.px4.io/main/en/flight_modes_mc/position) — Easiest and safest manual mode for vehicles that have a position fix/GPS. The roll and pitch sticks control acceleration over ground in the vehicle's forward-back and left-right directions (similar to a car's accelerator pedal), the yaw stick controls horizontal rotation, and the throttle controls speed of ascent-descent. Releasing sticks levels the vehicle, actively brakes it to a stop, and locks it to the current 3D position (even against wind and other forces).

- [Altitude mode](https://docs.px4.io/main/en/flight_modes_mc/altitude) — Easiest and safest non-GPS manual mode. The main difference when compared to Position mode is that when the sticks are released the vehicle will level and maintain altitude, but there is no active breaking or holding of horizontal position (the vehicle moves with it's current momentum and drifts with wind)

- [Stabilized mode](https://docs.px4.io/main/en/flight_modes_mc/manual_stabilized) — Releasing the sticks levels and maintains the vehicle horizontal posture (but not altitude or position). The vehicle will continue to move with momentum, and both altitude and horizontal position may be affected by wind. This mode is also used if "Manual mode" is selected in a ground station.


# Autonomous modes:
- [Hold](https://docs.px4.io/main/en/flight_modes_mc/hold) — Vehicle stops and hovers at its current position and altitude, maintaining its position against wind and other forces.
- [Return](https://docs.px4.io/main/en/flight_modes_mc/return) — Vehicle ascends to a safe altitude, flies a clear path to a safe location (home or a rally point) and then lands. This requires a global position estimate (GPS).

- [Mission](https://docs.px4.io/main/en/flight_modes_mc/mission) — Vehicle executes a predefined mission/flight plan that has been uploaded to the flight controller. This requires a global position estimate (GPS).
- [Takeoff](https://docs.px4.io/main/en/flight_modes_mc/takeoff) — Vehicle takes off vertically and then switches to Hold mode.
- [Land](https://docs.px4.io/main/en/flight_modes_mc/land) — Vehicle lands immediately.
- [Orbit](https://docs.px4.io/main/en/flight_modes_mc/orbit) - Vehicle flys in a circle, yawing so that it always faces towards the center. RC control can optionally be used to change the orbit radius, direction, speed and so on.
- [Follow Me](https://docs.px4.io/main/en/flight_modes_mc/follow_me) — Vehicle follows a beacon that is providing position setpoints. RC control can optionally be used to set the follow position.
- [Offboard](https://docs.px4.io/main/en/flight_modes/offboard) — Vehicle obeys position, velocity, or attitude, setpoints provided via MAVLink or ROS 2.




