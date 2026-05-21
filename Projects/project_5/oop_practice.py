
class Dronecontroller:
    def __init__(self,name):
        self.name = name
        self.altitude = 0
    
    def takeoff(self, target_altitude):
        print(f"Drone {self.name} taking off to {target_altitude}m")
        self.altitude = target_altitude
    
    def land(self):
        print(f"Drone {self.name} landing...")
        self.altitude = 0

alpha =Dronecontroller("alpha")
bravo = Dronecontroller("bravo")

alpha.takeoff(10)
bravo.land()

print(f"Drone {alpha.name}: altitude:{alpha.altitude}m")
print(f"Drone {bravo.name}: altitude: {bravo.altitude}m")