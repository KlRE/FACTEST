import numpy as np
import polytope as pc
from matplotlib import pyplot as plt


def find_breakpoints(num_sections, Theta, G, O, workspace):
    """
    Given environment parameters divide the environment into num_sections sections vertically. Find the breakpoints where segments meet
    :param num_sections: The number of sections to divide the environment into
    :param Theta: The rectangular start set as an array/tuple
    :param G: The rectangular goal set as an array/tuple
    :param O: The list of rectangular obstacles as Polytopes
    :param workspace: The rectangular workspace
    """

    assert num_sections > 1, "Number of sections should be greater than 1"
    # assert len(Theta) == 4 and isinstance(Theta, (list, tuple,
    #                                               np.ndarray)), f"Theta should be a list or tuple of length 4, got length {len(Theta)} and type {type(Theta)}"
    #
    # assert len(G) == 4 and isinstance(G, (list, tuple, np.ndarray)), "G should be a list or tuple of length 4"
    # assert len(workspace) == 4 and isinstance(workspace,
    #                                           (list, tuple,
    #                                            np.ndarray)), "workspace should be a list or tuple of length 4"
    assert isinstance(O, list) and all(
        isinstance(obstacle, pc.Polytope) for obstacle in O), "O should be a list of Polytopes"

    G_xmin, G_xmax = -G.b[0], G.b[1]
    Theta_xmin, Theta_xmax = -Theta.b[0], Theta.b[1]
    workspace_ymin, workspace_ymax = -workspace.b[2], workspace.b[3]

    signed_segment_length = ((G_xmin + G_xmax) / 2 - (Theta_xmax + Theta_xmin) / 2) / num_sections
    print(signed_segment_length)
    breakpoints = [[] for _ in range(num_sections - 1)]

    upper_bound, lower_bound = workspace_ymax, workspace_ymin

    fig, ax = plt.subplots(figsize=(10, 10))
    for i in range(num_sections - 1):
        vertical_line = round(Theta_xmin + (i + 1) * signed_segment_length, 2)
        print(f"vertical_line: {vertical_line}")

        A_line = np.array([[1, 0], [-1, 0]])  # x_0 <= x <= x_0
        b_line = np.array([vertical_line, -vertical_line])

        meeting_obstacles = []
        for obstacle in O:
            A_obstacle, b_obstacle = obstacle.A, obstacle.b
            A_combined = np.vstack([A_obstacle, A_line])
            b_combined = np.hstack([b_obstacle, b_line])

            # Define the polytope with the new constraints
            intersection_polytope = pc.Polytope(A_combined, b_combined)

            # Compute the vertices of the intersection
            vertices = pc.extreme(intersection_polytope)
            print(intersection_polytope)
            intersection_polytope.plot(ax, color='red', alpha=0.5)
            if vertices:
                print("Intersection vertices with the vertical line x =", vertical_line, ":")
                print(vertices)
    plt.show()

    # meeting_obstacles.sort(key=lambda x: x[2])
    #
    # print(f"meeting_obstacles: {meeting_obstacles}")
    # for j in range(len(meeting_obstacles) + 1):
    #     if j == 0:
    #         lower = lower_bound
    #     else:
    #         lower = meeting_obstacles[j - 1][3]
    #
    #     if j == len(meeting_obstacles):
    #         upper = upper_bound
    #     else:
    #         upper = meeting_obstacles[j][2]
    #     if upper > lower:
    #         breakpoints[i].append((vertical_line, round((upper + lower) / 2, 2)))
    #
    # print(f"breakpoints: {breakpoints[i]}")


if __name__ == "__main__":
    from convert_polytope_to_arrays import convert_env_polytope_to_arrays
    from envs.maze_2d import Theta, G, O, workspace

    breakpoints = find_breakpoints(2, Theta, G, O, workspace)
