with open("/home/sai/py_uav/py_projects/Projects/project_4/geo location file.txt") as file:
        # mission_coordinates = file.read()
        mission_coordinates = file.read().splitlines()
print(mission_coordinates)