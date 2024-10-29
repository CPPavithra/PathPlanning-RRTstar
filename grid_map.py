import numpy as np
from pyntcloud import PyntCloud

def create_grid_map(ply_file, grid_resolution):
    # Load the point cloud from the PLY file
    cloud = PyntCloud.from_file(ply_file)
    points = cloud.xyz  # Extract the points as a NumPy array

    # Define the boundaries
    min_x, max_x = np.min(points[:, 0]), np.max(points[:, 0])
    min_y, max_y = np.min(points[:, 1]), np.max(points[:, 1])

    # Create the occupancy grid
    x_bins = int((max_x - min_x) / grid_resolution)
    y_bins = int((max_y - min_y) / grid_resolution)
    occupancy_grid = np.zeros((x_bins, y_bins), dtype=bool)

    # Fill the occupancy grid
    for point in points:
        x_idx = int((point[0] - min_x) / grid_resolution)
        y_idx = int((point[1] - min_y) / grid_resolution)
        if 0 <= x_idx < x_bins and 0 <= y_idx < y_bins:
            occupancy_grid[x_idx, y_idx] = True

    return occupancy_grid, (min_x, max_x, min_y, max_y)

