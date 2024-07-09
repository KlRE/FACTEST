import matplotlib.pyplot as plt
import numpy as np

# Define the coordinates of the start position and the goal position
start_xmin, start_ymin, start_xmax, start_ymax = 0.4, 3.6, 0.6, 3.4
goal_xmin, goal_ymin, goal_xmax, goal_ymax = 6.25, 5.0, 6.75, 4.5

# Define the coordinates of obstacles
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

# Create the plot
fig, ax = plt.subplots()

# Plot start position and goal position as rectangles
ax.add_patch(plt.Rectangle((start_xmin, start_ymin), (start_xmax-start_xmin), (start_ymax-start_ymin),
edgecolor='black', facecolor='red'))
ax.add_patch(plt.Rectangle((goal_xmin, goal_ymin), (goal_xmax-goal_xmin), (goal_ymax-goal_ymin),
edgecolor='black', facecolor='green'))

# Plot obstacles as rectangles
for obstacle in obstacles:
    xmin, xmax, ymin, ymax = obstacle
    ax.add_patch(plt.Rectangle((xmin, ymin), (xmax-xmin), (ymax-ymin), edgecolor='black', facecolor='gray'))

# Set the limits of the plot
ax.set_xlim(0, 7)
ax.set_ylim(0, 6)

# Display the plot
plt.show()
