import random
import polytope as pc
import numpy as np


def generate_env(num_obstacles: int):
    """
    Generate a random environment with the given number of obstacles. The obstacles are randomly placed in the workspace.
    The workspace is a 10x10 square. The start set is a 2x2 square in the bottom left corner. The goal set is a 2x2 square in the top right corner.
    """
    # Define the workspace
    A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
    b_workspace = np.array([0, 10, 0, 10])  # (-xmin, xmax, -ymin, ymax)
    workspace = pc.Polytope(A, b_workspace)

    # Define the start set
    b_init = np.array([0, 2, 0, 2])
    Theta = pc.Polytope(A, b_init)

    # Define the goal set
    b_goal = np.array([-8, 10, -8, 10])
    G = pc.Polytope(A, b_goal)

    # Define the obstacles
    O = []
    generated_obstacles = 0
    while generated_obstacles < num_obstacles:
        xmin = random.uniform(0, 8)
        xmax = random.uniform(xmin + 1, 10)
        ymin = random.uniform(0, 8)
        ymax = random.uniform(ymin + 1, 10)
        # check if overlaps with start or goal
        if xmin <= 2 and ymin <= 2 or xmax >= 8 and ymax >= 8:
            continue
        b = np.array([-xmin, xmax, -ymin, ymax])
        O.append(pc.Polytope(A, b))
        generated_obstacles += 1

    return Theta, G, O, workspace


if __name__ == "__main__":
    from plot_env import plot_env

    for _ in range(10):
        Theta, G, O, workspace = generate_env(5)
        plot_env("Random Environment", workspace, G, Theta, O)
