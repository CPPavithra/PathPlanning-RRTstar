import random
import math

class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent

class RRTStar:
    def __init__(self, start, goal, rand_area, occupancy_grid, boundaries, max_iter=500, step_size=1.0):
        self.start = Node(start[0], start[1])  # Initialize start as a node
        self.goal = Node(goal[0], goal[1])    # Initialize goal as a node
        self.rand_area = rand_area  # Random area limits, e.g., [-60, -56]
        self.occupancy_grid = occupancy_grid  # 2D grid indicating obstacles
        self.boundaries = boundaries  # Area boundaries (xmin, xmax, ymin, ymax)
        self.max_iter = max_iter  # Maximum iterations for planning
        self.step_size = step_size  # Step size for node expansion
        self.goal_threshold = 1.0  # Distance to goal for stopping

    def planning(self):
        """Plans a path from start to goal."""
        nodes = [self.start]  # List to store tree nodes

        for i in range(self.max_iter):
            rand_point = self.get_random_point()  # Get a random point in the search space
            nearest_node = self.get_nearest_node(nodes, rand_point)  # Find the nearest node
            new_node = self.steer(nearest_node, rand_point)  # Steer towards the random point

            if not self.is_collision(nearest_node, new_node):  # If no collision, add new node
                nodes.append(new_node)
                if self.is_goal_reached(new_node):  # If goal is reached, extract the path
                    return self.extract_path(new_node)

        return None  # If no path found after max_iter

    def get_random_point(self):
        """Generates a random point within the defined search space."""
        x = random.uniform(self.rand_area[0], self.rand_area[1])
        y = random.uniform(self.rand_area[0], self.rand_area[1])
        return Node(x, y)

    def get_nearest_node(self, nodes, random_point):
        """Finds the nearest node to a random point."""
        return min(nodes, key=lambda node: self.euclidean_distance(node, random_point))

    def steer(self, nearest_node, random_point):
        """Steers from the nearest node towards the random point by a fixed step size."""
        direction = math.atan2(random_point.y - nearest_node.y, random_point.x - nearest_node.x)
        new_x = nearest_node.x + self.step_size * math.cos(direction)
        new_y = nearest_node.y + self.step_size * math.sin(direction)

        new_node = Node(new_x, new_y, nearest_node)  # New node's parent is the nearest node
        return new_node

    def is_collision(self, node1, node2):
        """Checks for collisions along the path between node1 and node2."""
        # Simple grid-based collision checking
        x1, y1 = node1.x, node1.y
        x2, y2 = node2.x, node2.y

        # Implement Bresenham's line algorithm or step through the path
        steps = int(max(abs(x2 - x1), abs(y2 - y1)))
        for i in range(steps + 1):
            u = i / steps
            x = int(x1 + u * (x2 - x1))
            y = int(y1 + u * (y2 - y1))

            if self.occupancy_grid[y][x] == 1:  # If grid cell is occupied
                return True  # Collision

        return False  # No collision

    def is_goal_reached(self, node):
        """Checks if the goal has been reached."""
        distance_to_goal = self.euclidean_distance(node, self.goal)
        return distance_to_goal < self.goal_threshold

    def euclidean_distance(self, node1, node2):
        """Calculates the Euclidean distance between two nodes."""
        return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)

    def extract_path(self, goal_node):
        """Extracts the path from start to goal by backtracking from the goal node."""
        path = []
        current_node = goal_node
        while current_node is not None:
            path.append((current_node.x, current_node.y))
            current_node = current_node.parent
        return path[::-1]  # Return reversed path

    def path_smoothing(self, path):
        """Optional: Path smoothing using a simple method."""
        smoothed_path = [path[0]]
        for i in range(1, len(path) - 1):
            if not self.is_collision(Node(path[i - 1][0], path[i - 1][1]), Node(path[i + 1][0], path[i + 1][1])):
                continue  # Skip the current point if a direct path is possible
            smoothed_path.append(path[i])
        smoothed_path.append(path[-1])
        return smoothed_path

