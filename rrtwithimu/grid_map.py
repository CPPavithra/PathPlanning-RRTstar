import numpy as np
from pyntcloud import PyntCloud

class GridMap:
    def __init__(self, ply_file):
        self.ply_file = ply_file
        self.points = self.load_ply()
        self.occupancy_grid = self.create_occupancy_grid()

    def load_ply(self):
        cloud = PyntCloud.from_file(self.ply_file)
        return cloud.points.values  # Get points as a numpy array

    def create_occupancy_grid(self):
        # Create a simple occupancy grid (modify based on your needs)
        min_x, max_x = np.min(self.points[:, 0]), np.max(self.points[:, 0])
        min_y, max_y = np.min(self.points[:, 1]), np.max(self.points[:, 1])
        
        grid_size_x = int(max_x - min_x + 1)
        grid_size_y = int(max_y - min_y + 1)
        occupancy_grid = np.zeros((grid_size_x, grid_size_y))

        for point in self.points:
            x_index = int(point[0] - min_x)
            y_index = int(point[1] - min_y)
            if 0 <= x_index < grid_size_x and 0 <= y_index < grid_size_y:
                occupancy_grid[x_index, y_index] = 1  # Mark occupied
        
        return occupancy_grid

