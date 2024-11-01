from rrt_star import RRTStar
from grid_map import GridMap
from sensors import GPS, IMU
from kalman_filter import KalmanFilter
from ssh_communicator import SSHCommunicator
import time
import numpy as np

def main():
    # Define start and goal positions
    start = (-60, -250)
    goal = (-58, -250)

    # Define boundaries
    boundaries = (-60, -56)

    # Load the grid map
    grid_map = GridMap('3dmap.ply')  # Update with your PLY file path

    # Initialize RRT* planner
    rrt_star = RRTStar(start=start, goal=goal, occupancy_grid=grid_map.occupancy_grid, boundaries=boundaries)

    # Plan the path
    path = rrt_star.planning()

    # Initialize the SSH communicator
    ssh_comm = SSHCommunicator(hostname='your_rover_ip', port=22, username='your_username', password='your_password')  # Update with your SSH credentials

    # Initialize sensors and Kalman filter
    gps = GPS()
    imu = IMU()
    kf = KalmanFilter()

    # Simulated real-time updates for localization
    for coord in path:
        while True:
            # Read real-time GPS and IMU data
            gps_data = gps.get_position()  # Example format: (lat, lon)
            imu_data = imu.get_orientation()  # Orientation in degrees
            
            # Apply Kalman Filter to update position
            estimated_position = kf.update(gps_data, imu_data)
            
            # Calculate distance to the next waypoint
            distance = np.linalg.norm(np.array(coord) - np.array(estimated_position))
            
            # Send command to the rover if within a certain distance
            if distance < 1.0:  # Adjust the threshold as needed
                command = f"move_to {coord[0]} {coord[1]}"  # Example command format
                output = ssh_comm.send_command(command)
                print(f"Sent command: {command}, Output: {output}")  # For debugging purposes
                break
            
            time.sleep(0.1)  # Short delay for real-time updates

    # Close the SSH connection when done
    ssh_comm.close_connection()

if __name__ == "__main__":
    main()

