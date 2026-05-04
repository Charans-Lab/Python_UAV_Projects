import asyncio
from mavsdk import System

async def main():
    drone = System()
    await drone.connect(system_address="udp://:14540")
    print("waiting for drone connection...")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone Connecte!")
            break

asyncio.run(main())