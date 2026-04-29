## Project 3: Visualize the Mission on a Map
# Goal: take your working mission planner and add a visual plot of the flight path.
What the program should do (building on v2.1):

Everything v2.1 does (read waypoints from file, compute distance, check altitudes, print summary) — unchanged.
After the summary, create a 2D plot:

 X-axis: longitude
 Y-axis: latitude
 Each waypoint as a dot
 Lines connecting consecutive waypoints (the flight path)
 Each waypoint labeled with its number
 Start waypoint in green, end waypoint in red, middle waypoints in blue
 Title showing "Mission Plan — Total Distance: XXX.XX km"
 Axis labels: "Longitude" and "Latitude"


Save the plot as mission_map.png in the same folder.
Display the plot in a window.



## Project 3: Mission Visualization

Adds a 2D plot of the flight path using matplotlib. Shows
waypoints as colored dots (green=start, red=end, blue=middle),
connected by lines, with the total distance in the title.

![Mission Map](Projects/Project-3/mission_map.png)