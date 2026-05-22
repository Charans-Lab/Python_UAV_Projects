# project 5 MissionPlan using object oreinted programming.

import asyncio
from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan
from pathlib import Path
class DroneMission:
    def __init__(self, waypoints_location):
        
        self.waypoints_location = waypoints_location
        self.waypoints =[]
        self.mission_plan = None
        self.MISSION_SPEED_MS = 10.0
        self.DGCA_ALTITUDE_LIMIT_M = 120       

    def load_waypoints(self):
        with open(self.waypoints_location) as file:
            waypoints = [line for line in file.read().splitlines() if line.strip()]
                
        for i in range(len(waypoints)):
            waypoint_number, latitude, longitude,altitude = waypoints[i].split()            
            waypoint_number = int(waypoint_number)
            latitude = float(latitude)
            longitude = float(longitude)
            altitude = float(altitude)
            each_waypoint =[waypoint_number, latitude, longitude, altitude]            
            self.waypoints.append(each_waypoint)
            self.check_altitude(altitude, waypoint_number)
            
    def check_altitude(self, altitude, waypoint_number):
        if altitude > self.DGCA_ALTITUDE_LIMIT_M:
                print(f" waypoint:{waypoint_number}, altitude is {altitude} m, exceed DGCA limit {self.DGCA_ALTITUDE_LIMIT_M}m ")
        
    def build_mission_plan(self):     

        mission_items = []
        for wp in self.waypoints:            
            mission_items.append(MissionItem(
            wp[1],   # latitude
            wp[2],   # longitude
            wp[3],   # altitude
            self.MISSION_SPEED_MS,      # speed in m/s
            True,    # is_fly_through
            float('nan'),  # gimbal pitch
            float('nan'),  # gimbal yaw
            MissionItem.CameraAction.NONE,
            float('nan'),  # loiter time
            float('nan'),  # camera photo interval
            float('nan'),  # acceptance radius
            float('nan'),  # yaw_deg
            float('nan'),  # camera_photo_distance_m
            MissionItem.VehicleAction.NONE,
            ))
            
        self.mission_plan = MissionPlan(mission_items)
        

    async def connection_to_drone(self):
        self.drone = System()
        print("...waiting drone to connect")
        await self.drone.connect(system_address="udpin://0.0.0.0:14540")

        async for state in self.drone.core.connection_state():
            if state.is_connected:
                print("connected to drone....")
                break

    async def check_health(self):
        async for health in self.drone.telemetry.health():
            if health.is_global_position_ok:
                print("...drone health is good and gps fix")
                break
    
    async def upload_mission(self):
        await self.drone.mission.clear_mission()
        await asyncio.sleep(2)
        await self.drone.mission.set_return_to_launch_after_mission(True)
        print("uploading mission to drone....")
        await self.drone.mission.upload_mission(self.mission_plan)
    
    async def execute_mission(self):       
        print("arming drone")
        await self.drone.action.arm()
        print("starting mission drone takeing off...")
        await self.drone.mission.start_mission()

    async def mission_monitor(self):
        async for mission_progress in self.drone.mission.mission_progress():
            print(f"Mission progress: {mission_progress.current}/{mission_progress.total}")

            if mission_progress.current == mission_progress.total:
                print("Mission Completed, drone moving to home point")
                async for altitude in self.drone.telemetry.altitude():                    
                    if altitude.altitude_relative_m <= 0:
                        print("Drone landed....")
                        break
                break

    async def run(self):
        self.load_waypoints()
        self.build_mission_plan()
        await self.connection_to_drone()
        await self.check_health()
        await self.upload_mission()
        await asyncio.gather(self.execute_mission(), self.mission_monitor())    
        
  

async def main():
    waypoints_file = Path(__file__).parent / "waypoints.txt"    
    mission = DroneMission(waypoints_file)   
    await mission.run()

asyncio.run(main())



