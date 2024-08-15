import matplotlib.pyplot as plt
import numpy as np

# Define the coordinates of the start position, obstacles, and goal position
start_positions = [(0.3, 0.7, 3.3, 3.7)]
goal_position = [(6.25, 6.75, 4.5, 5.0)]

obstacles = [
    (1.0, 3.0, 0.9, 1.0),   # Obstacle 1
    (1.0, 5.0, 3.9, 4.0),   # Obstacle 2
    (0.9, 1.0, 2.0, 3.0),   # Obstacle 3
    (1.0, 2.0, 2.9, 3.0),   # Obstacle 4
    (1.9, 2.0, 2.0, 3.0),   # Obstacle 5
    (2.0, 4.0, 1.9, 2.0),   # Obstacle 6
    (3.9, 4.0, 1.0, 3.0),   # Obstacle 7
    (2.9, 3.0, 3.0, 4.0),   # Obstacle 8
    (4.0, 6.0, 0.9, 1.0),   # Obstacle 9
    (4.9, 5.0, 2.0, 4.0),   # Obstacle 10
    (5.0, 6.0, 1.9, 2.0),   # Obstacle 11
    (5.9, 6.0, 2.0, 5.0),   # Obstacle 12
    (0.0, 7.0, 0.0, 0.1),   # Obstacle 13
    (0.0, 0.1, 0.0, 3.0),   # Obstacle 14
    (0.0, 0.1, 4.0, 5.0),   # Obstacle 15
    (0.0, 6.0, 4.9, 5.0),   # Obstacle 16
    (6.9, 7.0, 0.0, 5.0),   # Obstacle 17
    (0.1, 0.0, 0.0, 5.0),   # Obstacle 18
    (7.0, 7.1, 0.0, 5.0),   # Obstacle 19
    (0.0, 7.0, 0.1, 0.0),   # Obstacle 20
    (0.0, 7.0, 5.0, 5.1)    # Obstacle 21
]

# Create a new figure and set its size
fig = plt.figure(figsize=(10, 8))

# Iterate over the start positions and plot them as rectangles
for x_min, x_max, y_min, y_max in start_positions:
    rect = plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, color='blue')
    plt.gca().add_patch(rect)

# Iterate over the obstacles and plot them as rectangles
for xmin, xmax, ymin, ymax in obstacles:
    rect = plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, color='red')
    plt.gca().add_patch(rect)

# Plot the goal position as a rectangle
goal_xmin, goal_xmax, goal_ymin, goal_ymax = goal_position[0]
rect = plt.Rectangle((goal_xmin, goal_ymin), goal_xmax - goal_xmin, goal_ymax - goal_ymin, color='green')
plt.gca().add_patch(rect)

# Set the x and y limits of the plot
plt.xlim(0, 7.1)
plt.ylim(0, 5.1)

# Show the plot
plt.show()
