import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
def plot_environment(obstacles, start, goal):
    # Create a new figure
    fig, ax = plt.subplots(figsize=(10, 10))
    plt.xlim(0, 7)
    plt.ylim(0, 5)

    # Plot each obstacle
    for (xmin, xmax, ymin, ymax) in obstacles:
        rect = patches.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, linewidth=1, edgecolor='r', facecolor='r',
                                 alpha=0.5)
        ax.add_patch(rect)

    # Plot the start position
    (xmin, xmax, ymin, ymax) = start
    start_rect = patches.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, linewidth=1, edgecolor='g', facecolor='g',
                                   alpha=0.5)
    ax.add_patch(start_rect)

    # Plot the goal position
    (xmin, xmax, ymin, ymax) = goal
    goal_rect = patches.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, linewidth=1, edgecolor='b', facecolor='b',
                                  alpha=0.5)
    ax.add_patch(goal_rect)

    # Add labels and legend
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("2D Maze Navigation")
    plt.legend(['Obstacles', 'Start Position', 'Goal Position'], loc='upper right')

    # Show the plot
    plt.grid(True)
    plt.show()


# Define start and goal positions
start = (0.4, 0.6, 3.4, 3.6)
goal = (6.25, 6.75, 4.5, 5.0)

# Plot the environment
plot_environment(obstacles, start, goal)
