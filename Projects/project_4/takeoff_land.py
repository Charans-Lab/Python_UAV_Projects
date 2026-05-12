import asyncio
from mavsdk import System

async def main():
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")
    
    print("Waiting for drone connection...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected!")
            break
    
    print("Waiting for global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("Global position OK, ready to fly")
            break
    
    print("Arming drone...")
    await drone.action.arm()
    
    print("Taking off...")
    await drone.action.takeoff()

    await asyncio.sleep(10)
    await drone.action.land()
    await asyncio.sleep(10)
    

    
    print("Mission complete")

asyncio.run(main())