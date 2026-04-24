import math

no_of_waypoints = int(input("Enter the no.of waypoint"))
waypoints_list = []
distance = 0
for i in range(no_of_waypoints):
    latitude, longitude, altitude = input("enter the latitude longitude altitude").split()
    each_waypoint =[latitude, longitude, altitude]
    float_each_waypoint =[float(item) for item in each_waypoint]
    waypoints_list.append(float_each_waypoint)


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
        print("warming mission height is greater than 120m")
    def haversine(lat1, lon1, lat2, lon2):
        global distance
        
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
        a_to_b_distance = c*rad
        # print(a_to_b_distance)
        distance = distance + c
        
        return rad * c
    
    
haversine(lat1,lon1,lat2,lon2) 
print("Total mission distance:", distance)
print("Time taken to complete mission. ", distance/2 ) # Note:considering mission speed 2km/h
print("Estimate Battery :", distance/2*10  ) #Note:battery usage 10% for 1min

