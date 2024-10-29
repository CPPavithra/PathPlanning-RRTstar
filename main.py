import time
import serial
from rrt_star import RRTStar
from grid_map import create_grid_map
import matplotlib.pyplot as plt

def send_waypoints_to_arduino(ser, nodes):
    """Send each node as a waypoint to the Arduino over serial and wait for acknowledgment."""
    for node in nodes:
        # Convert the node to a string format and send it over serial
        coords = f"{node[0]},{node[1]}\n"
        ser.write(coords.encode())
        print(f"Sent: {coords.strip()}")  # Log the sent waypoint
        
        # Wait for Arduino to acknowledge reaching the waypoint
        while True:
            if ser.in_waiting > 0:
                response = ser.readline().decode().strip()
                print("Arduino:", response)  # Log Arduino's response
                if response == "reached":
                    print("Waypoint reached:", coords.strip())
                    break
            time.sleep(0.1)

def visualize_path(nodes, edges, occupancy_grid, boundaries, filename='path1.png'):
    """Visualize and save the path on the occupancy grid."""
    plt.imshow(occupancy_grid, cmap='gray')
    for edge in edges:
        plt.plot([nodes[edge[0]][0], nodes[edge[1]][0]], 
                 [nodes[edge[0]][1], nodes[edge[1]][1]], 'r-')
    plt.title('RRT* Path Planning')
    plt.xlim(boundaries[0], boundaries[2])
    plt.ylim(boundaries[1], boundaries[3])
    plt.savefig(filename)
    plt.close()

def main():
    start = (-54.4546012878418, -90.22299194335938)
    goal = (-8.80459976196289, -166.62298583984375)
    plyfile = '3dmap.ply'
    grid_resolution = 0.05

    # Create grid map from the PLY file
    occupancy_grid, boundaries = create_grid_map(plyfile, grid_resolution)

    # Plan the RRT* path
    rrt_star = RRTStar(start, goal, occupancy_grid, boundaries)
    nodes, edges = rrt_star.plan()

    # Visualize and save the path on the occupancy grid
    visualize_path(nodes, edges, occupancy_grid, boundaries, filename='path1.png')

    # Initialize serial connection to Arduino (adjust COM port or /dev/ttyUSB0 as necessary)
    ser = serial.Serial('/dev/ttyUSB0', 9600)  # Replace with the correct port and baud rate
    time.sleep(2)  # Allow time for the Arduino to reset

    # Send nodes (waypoints) to Arduino
    send_waypoints_to_arduino(ser, nodes)

    ser.close()  # Close the serial connection after sending all waypoints

if __name__ == "__main__":
    main()

