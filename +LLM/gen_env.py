import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def generate_env(num_obstacles: int):
    # Define workspace bounds
    lower_bound = np.array([0, 0])
    upper_bound = np.array([20, 20])

    grid_size = 8
    overlap_fraction = 0.5
    overlap_size = grid_size * overlap_fraction

    num_rows = int((upper_bound[1] - lower_bound[1]) / (grid_size - overlap_size))
    num_cols = int((upper_bound[0] - lower_bound[0]) / (grid_size - overlap_size))

    grid_cells = []
    for x in range(num_cols):
        for y in range(num_rows):
            x_min = lower_bound[0] + x * (grid_size - overlap_size)
            x_max = x_min + grid_size
            y_min = lower_bound[1] + y * (grid_size - overlap_size)
            y_max = y_min + grid_size
            grid_cells.append((x_min, y_min, x_max, y_max))
    # print(grid_cells)
    np.random.shuffle(np.array(grid_cells))
    grid_cells = grid_cells[:num_obstacles]

    obstacles = []
    for (x_min, y_min, x_max, y_max) in grid_cells:
        x_max, y_max = min(x_max, upper_bound[0]), min(y_max, upper_bound[1])
        while True:  # Try multiple times to ensure obstacles are created
            points = np.random.uniform([x_min, y_min], [x_max, y_max], (4, 2))
            points = np.round(points, 1)
            if len(points) == 4:
                obstacles.append(points)
                break

    # Define start and goal sets
    Theta = np.array([[0, 0], [2, 0], [2, 2], [0, 2]])
    G = np.array([[18, 18], [20, 18], [20, 20], [18, 20]])

    # Define workspace
    workspace = np.array([[0, 0], [20, 0], [20, 20], [0, 20]])

    return Theta, G, obstacles, workspace


Theta, G, obstacles, workspace = generate_env(5)
print("Start set:", Theta)
print("Goal set:", G)
print("Obstacles:", obstacles)
print("Workspace:", workspace)

# Visualization
fig, ax = plt.subplots()
ax.add_patch(patches.Polygon(Theta, closed=True, fill=True, color='blue', alpha=0.5, label='Start'))
ax.add_patch(patches.Polygon(G, closed=True, fill=True, color='green', alpha=0.5, label='Goal'))
for obs in obstacles:
    ax.add_patch(patches.Polygon(obs, closed=True, fill=True, color='red', alpha=0.5))
ax.add_patch(patches.Polygon(workspace, closed=True, edgecolor='black', fill=False, linestyle='--'))
ax.autoscale_view()
plt.legend()
plt.grid(True)
plt.show()
