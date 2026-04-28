import math
import matplotlib.pyplot as plt

with open("geo location file.txt") as file:
    Mission_coordinates = file.read().splitlines()

no_of_waypoints = len(Mission_coordinates)
waypoints_list = []
x = []
y = []
z = []
total_distance = 0

def check_altitude(altitude, waypoint_number):
      if altitude > 120:
            print(f"waypoint number: {waypoint_number}, Altitude is:{altitude}, exceeds. 120m is DGCA limit")

for i in range(no_of_waypoints):
    
    waypoint_number, latitude, longitude, altitude = Mission_coordinates[i].split()
    waypoint_number= int(waypoint_number)
    latitude = float(latitude)
    longitude = float(longitude)
    altitude = float(altitude)
    each_waypoint =[waypoint_number, latitude, longitude, altitude]
    x.append(longitude)
    y.append(latitude)
    z.append(waypoint_number)

    
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

for i in range(1, no_of_waypoints):
        point_a = waypoints_list[i-1]
        lat1 = point_a[1]
        lon1 = point_a[2]
    
        point_b = waypoints_list[i]
        lat2 = point_b[1]
        lon2 = point_b[2] 
        total_distance = total_distance + haversine(lat1,lon1,lat2,lon2)

print("Total mission Distancein km:", total_distance)
print("Time taken to complete mission in hours. ", total_distance/30)    # distance(km) / 30(km/h) = hours
print("Estimate Battery in Percentage :", (total_distance/30)*20)                # per hour my drone will consure 20% 

fig, ax = plt.subplots()

for i in range(len(z)):
    if i == 0:
        ax.scatter(x[i],y[i], marker='o', c= 'g')
        ax.annotate(z[i], xy= (x[i],y[i]))
    elif i == len(z):
        ax.scatter(x[i],y[i], marker='o', c='r')
        ax.annotate(z[i], xy= (x[i],y[i]))
    else:
        ax.scatter(x[i],y[i], marker='o', c= 'b')
        ax.annotate(z[i], xy= (x[i],y[i]))

plt.plot(x,y)
plt.xlabel("longitude")
plt.ylabel("latitude")
plt.title("Mission Plan-Total distance:")
plt.show()