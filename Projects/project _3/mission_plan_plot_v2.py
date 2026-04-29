import math
import matplotlib.pyplot as plt

with open("geo location file.txt") as file:
    mission_coordinates = file.read().splitlines()

waypoints_list = []
latitudes =[]
longitudes =[]
waypoint_numbers = []
total_distance = 0

def check_altitude(altitude, waypoint_number):
      if altitude > 120:
            print(f"waypoint number: {waypoint_number}, Altitude is:{altitude}, exceeds. 120m is DGCA limit")

for i in range(len(mission_coordinates)):
    
    waypoint_number, latitude, longitude, altitude = mission_coordinates[i].split()
    waypoint_number= int(waypoint_number)
    latitude = float(latitude)
    longitude = float(longitude)
    altitude = float(altitude)
    each_waypoint =[waypoint_number, latitude, longitude, altitude]
    latitudes.append(latitude)
    longitudes.append(longitude)
    waypoint_numbers.append(waypoint_number)
       
    waypoints_list.append(each_waypoint)
    check_altitude(altitude,waypoint_number)

def haversine(lat1, lon1, lat2, lon2):
                
        dLat = (lat2 - lat1) * math.pi / 180.0
        dLon = (lon2 - lon1) * math.pi / 180.0

        # convert to radians
        lat1 = (lat1) * math.pi / 180.0
        lat2 = (lat2) * math.pi / 180.0

        # apply formulae
        a = (pow(math.sin(dLat / 2), 2) + 
         pow(math.sin(dLon / 2), 2) * 
             math.cos(lat1) * math.cos(lat2));
        rad = 6371
        c = 2 * math.asin(math.sqrt(a))
        return c*rad

for i in range(1, len(mission_coordinates)):
        point_a = waypoints_list[i-1]
        lat1 = point_a[1]
        lon1 = point_a[2]
    
        point_b = waypoints_list[i]
        lat2 = point_b[1]
        lon2 = point_b[2] 
        total_distance = total_distance + haversine(lat1,lon1,lat2,lon2)

print(f"Total mission distance: {total_distance:.2f} km")
print(f"Estimated time: {total_distance/30:.2f} hours")    # distance(km) / 30(km/h) = hours
print(f"Estimate battery: {(total_distance/30)*20:.2f} %")                # per hour my drone will consure 20% 

fig, ax = plt.subplots()

for i in range(len(waypoint_numbers)):
    if i == 0:
        color = "g"        
    elif i == len(waypoint_numbers)-1:
        color = "r"       
    else:
        color = "b"
    ax.scatter(longitudes[i],latitudes[i], marker = 'o', c = color)
    ax.annotate(waypoint_numbers[i], xy= (longitudes[i],latitudes[i]))
 
plt.plot(longitudes,latitudes)
plt.xlabel("longitude")
plt.ylabel("latitude")
plt.title(f"Mission Plan-Total distance:{total_distance:.2f} km")
plt.savefig("mission_map.png", dpi=150, bbox_inches='tight')
plt.show()