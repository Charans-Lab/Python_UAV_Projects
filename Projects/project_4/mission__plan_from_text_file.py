import asyncio
import logging


from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan


# Enable INFO level logging by default so that INFO messages are shown
logging.basicConfig(level=logging.INFO)



async def run():
    drone = System()
    print("---waiting for drone to connect")
    await drone.connect(system_address="udpin://0.0.0.0:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("___drone connected!")
            break
    print_mission_progress_task = asyncio.ensure_future(print_mission_progress(drone))

    running_tasks = [print_mission_progress_task]
    termination_task = asyncio.ensure_future(observe_is_in_air(drone, running_tasks))

    
    
    with open("/home/sai/py_uav/py_projects/Projects/project_4/geo location file.txt") as file:
        mission_coordinates = file.read().splitlines()

    no_of_waypoints = len(mission_coordinates)
    waypoints_list = []


    def check_altitude(altitude, waypoint_number):
        if altitude > 120:
            print(f"waypoint number: {waypoint_number}, Altitude is:{altitude}, exceeds. 120m is DGCA limit")

    for i in range(no_of_waypoints):
    
        waypoint_number, latitude, longitude, altitude = mission_coordinates[i].split()
        waypoint_number= int(waypoint_number)
        latitude = float(latitude)
        longitude = float(longitude)
        altitude = float(altitude)
        each_waypoint =[waypoint_number, latitude, longitude, altitude]

    
        waypoints_list.append(each_waypoint)
        check_altitude(altitude,waypoint_number)

    mission_items = []
    for wp in waypoints_list:
        mission_items.append(MissionItem(
            wp[1],   # latitude
            wp[2],   # longitude
            wp[3],   # altitude
            10,      # speed in m/s
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
    mission_plan = MissionPlan(mission_items)



    await drone.mission.set_return_to_launch_after_mission(True)

    print("-- Uploading mission")
    await drone.mission.upload_mission(mission_plan)

    print("Waiting for global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_local_position_ok and health.is_global_position_ok:
            print("global position ok! and ready to takeoff")
            break
    print('Arming Drone')
    await drone.action.arm()

    print("starting mission")
    await drone.mission.start_mission()

    await termination_task

    
    

async def print_mission_progress(drone):
    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: {mission_progress.current}/{mission_progress.total}")

async def observe_is_in_air(drone, running_tasks):
    """Monitors whether the drone is flying or not and
    returns after landing"""

    was_in_air = False

    async for is_in_air in drone.telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            for task in running_tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            await asyncio.get_event_loop().shutdown_asyncgens()

            return

asyncio.run(run())