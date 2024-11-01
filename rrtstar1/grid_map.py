import pyntcloud

def create_grid_map(ply_file, grid_resolution):
    # Load the point cloud data from a PLY file using Pyntcloud
    point_cloud = pyntcloud.PyntCloud.from_file(ply_file)
    
    # Create a 2D occupancy grid based on the point cloud and the grid resolution
    occupancy_grid = {}  # Placeholder for the actual occupancy grid creation logic
    
    # Define boundaries for the grid (adjust based on point cloud)
    boundaries = {
        'x_min': -60,
        'x_max': -56,
        'y_min': -254,
        'y_max': -250
    }
    
    # Implement logic to convert the point cloud to a 2D occupancy grid
    return occupancy_grid, boundaries

