import asyncio
import matplotlib.pyplot as plt
import numpy as np
from mavsdk import System


class ImuAnalyzer:
    def __init__(self, num_samples):
        self.drone = System()
        self.num_samples = num_samples
        self.accel_samples = []

    async def connect(self):        
        print("....waiting drone to connect")
        await self.drone.connect(system_address="udpin://0.0.0.0:14540")
        async for state in self.drone.core.connection_state():
            if state.is_connected:
                print("Drone Connected....")
                break

    async def collect_imu(self):
        async for imu in self.drone.telemetry.imu():
            accel = imu.acceleration_frd
            self.accel_samples.append([accel.forward_m_s2, accel.right_m_s2, accel.down_m_s2])
            if len(self.accel_samples) >= self.num_samples:
                break
    def analyze(self):
        self.data = np.array(self.accel_samples)
        print(f"Data Shape: {np.shape(self.data)}")
        mean_per_axis  = np.mean(self.data, axis=0)
        std_per_axis = np.std(self.data, axis=0)
        
        print(f"Mean acceleration per axis (F,R,D): {mean_per_axis}")   
        print(f"Std dev per axis (F,R,D):{std_per_axis}")

        gravity_magnitude = np.sqrt(np.sum(mean_per_axis ** 2))
        print(f"Measured gravity magnitude: {gravity_magnitude:.4f} m/s^2")

    def plot(self):
        x = np.arange(self.num_samples)
        accel_forward = self.data[:,0]
        accel_right = self.data[:,1]
        accel_down = self.data[:,2]
        
        fig, ax = plt.subplots()            
        ax.plot(x,accel_forward, color = "blue", label ="accel forward m/s2")
        ax.plot(x,accel_right, color = "orange", label ="accel right m/s2")
        ax.plot(x,accel_down, color = "green" ,label ="accel downward m/s2")
        plt.legend()
        plt.title("IMU_Analaccel_forwardsis")
        plt.xlabel("imu_samples")
        plt.ylabel("accelration")        
        fig.savefig("IMU_analysis.png")
        plt.show()
        
        
    async def run(self):
        await self.connect()
        await self.collect_imu()
        self.analyze()
        self.plot()
        print(f"colleted {len(self.accel_samples)} samples")
        print(self.accel_samples[0:5])

async def main():
    analyzer = ImuAnalyzer(200)
    await analyzer.run()

asyncio.run(main())

    
