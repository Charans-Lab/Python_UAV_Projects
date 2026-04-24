import math


input_file = open("F:\Study\Python\pyhton uav problem\geo location file.txt")
sai = input_file.read().splitlines()
print(len(sai))



no_of_waypoints = len(sai)
waypoints_list = []
Total_distance = 0
for i in range(no_of_waypoints):
    latitude, longitude, altitude = sai[i].split()
    # print(latitude,longitude,altitude)
    each_waypoint =[latitude, longitude, altitude]
    float_each_waypoint =[float(item) for item in each_waypoint]
    waypoints_list.append(float_each_waypoint)
# print(waypoints_list)
def haversine(lat1, lon1, lat2, lon2):
        distance = 0
        
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
        # a_to_b_distance = c*rad
        # # print(a_to_b_distance)
        # distance = distance + a_to_b_distance
        
        return c*rad
for i in range(1, no_of_waypoints):
        pointa = waypoints_list[i-1]
        lat1 = pointa[0]
        lon1 = pointa[1]
    
        pointb = waypoints_list[i]
        lat2 = pointb[0]
        lon2 = pointb[1]
        if pointa[2]> 120:
            print("warming mission height is greater than 120m")
        if pointb[2]> 120:
            print("warning mission height is greater than 120m")
        
        # haversine(lat1,lon1,lat2,lon2)  
        Total_distance = Total_distance + haversine(lat1,lon1,lat2,lon2)

print("Total mission Distancein km:", Total_distance)
print("Time taken to complete mission in hours. ", Total_distance/30)    # distance(km) / 30(km/h) = hours
print("Estimate Battery in Percentage :", (Total_distance/30)*20)                # per hour my drone will consure 20% 