# Start with Phase 1. Get a camera model running in Gazebo and tell me what image topic you find.


Get a camera into the simulation. PX4's Gazebo worlds support camera-equipped models. You'll need to find the right model (there are variants with a downward-facing camera) and confirm the image is being published as a ROS 2 topic. Same verification discipline as Project 7: ros2 topic list, find the image topic, ros2 topic info for its type, before writing any code.