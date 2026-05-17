### Fly your waypoints 
Now you'll have actual context for what you're writing. The script will:

Read waypoints from geo location file.txt (reuse Project 2 code)
Connect, wait for health
Set the waypoints as a Mission using MAVSDK's mission plugin (the right tool — not GoTo in a loop)
Upload the mission to the drone
Arm, start mission, monitor progress
Wait for mission complete, then RTL or land