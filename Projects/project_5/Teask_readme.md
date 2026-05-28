Now — the real Project 5.
Refactor your Project 4 mission code into a class. This is where OOP starts doing real work for you, not just teaching you syntax.
What to build:
A class called DroneMission that owns:

The MAVSDK System object (as self.drone)
The waypoints file path (as self.waypoints_file)
The list of parsed waypoints (as self.waypoints, starts empty)
The MAVSDK mission plan (as self.mission_plan, starts as None)

Methods (most will be async):

async connect() — connect to PX4 and wait for connection state
async wait_for_health() — wait until global position is OK
load_waypoints() — read the file, parse it, store in self.waypoints (this one doesn't need to be async — no drone communication)
build_mission_plan() — convert self.waypoints into MissionItems, store in self.mission_plan (also doesn't need to be async)
async upload_mission() — upload self.mission_plan to the drone
async arm_and_start() — arm the drone and start the mission
async monitor_mission() — print mission progress, return when done
async run() — the orchestrator: calls all the above in the right order

Then at the bottom of the file:
```
python
async def main():
    mission = DroneMission("waypoints.txt")
    await mission.run()
```
asyncio.run(main())
That's it. The whole script comes down to two lines in main(). Compare that to your current Phase 4 code where everything is jumbled into one big run() function. That's the value of OOP.