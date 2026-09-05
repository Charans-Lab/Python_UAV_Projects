# task:Phase 2  
— Subscribe to images in a node. Structurally identical to your px4_listener — a node, a subscription, a callback. The new piece is cv_bridge, which converts ROS sensor_msgs/Image messages into OpenCV arrays. And here's the connection to Project 6: an OpenCV image is a NumPy array. Shape (height, width, 3) for color. Everything you learned about shape and array indexing applies directly.


