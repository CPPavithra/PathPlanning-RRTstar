import serial
import time
from rrt_star import RRTStar
from grid_map import create_grid_map

# Set up the serial connection with the Arduino (adjust the port and baud rate as necessary)
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Change '/dev/ttyUSB0' to the correct port
time.sleep(2)  # Allow time for the connection to establish

def send_coordinates_to_arduino(coords):
    for (x, y) in coords:
        command = f"{x},{y}\n"  # Format the coordinates
        ser.write(command.encode('utf-8'))  # Send the command to Arduino
        time.sleep(1)  # Adjust the wait time as necessary to give Arduino time to process

try:
    # Create the occupancy grid and boundary limits for path planning
    ply_file = '3dmap.ply'  # Replace this with the actual path of your 3D map
    grid_resolution = 0.05  # Adjust based on your requirements
    occupancy_grid, boundaries = create_grid_map(ply_file, grid_resolution)

    # Define start and goal positions
    start = (-59.5546, -253.523)
    goal = (-57.6546, -253.523)
    
    # Initialize and execute RRT* planning
    rrt_star = RRTStar(start=start, goal=goal, rand_area=[-60, -56], occupancy_grid=occupancy_grid, boundaries=boundaries)
    path_coordinates = rrt_star.planning()

    # Send the path coordinates to Arduino
    send_coordinates_to_arduino(path_coordinates)

finally:
    ser.close()  # Ensure the serial connection is closed

