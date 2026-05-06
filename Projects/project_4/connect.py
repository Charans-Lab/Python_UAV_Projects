import asyncio
from mavsdk import System


async def main():
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")
    print("waiting for drone connection...")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone Connected!")
            break
          
    async for position in drone.telemetry.position():
            print(f"drone_location:{position}")
            break
    async for flight_mode in drone.telemetry.flight_mode():
            print(f"flight_mode:{flight_mode}")
            break
    async for battery in drone.telemetry.battery():
            print(f"battery_status: {battery}")
            break



asyncio.run(main())