import numpy as np
import polytope as pc
from matplotlib import pyplot as plt
from z3 import *

from envs.plot_env import plot_env
from import_env import Env


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

    x = Real('x')
    y = Real('y')
    G_xmin, G_xmax = -G.b[0], G.b[1]
    Theta_xmin, Theta_xmax = -Theta.b[0], Theta.b[1]
    workspace_ymin, workspace_ymax = -workspace.b[2], workspace.b[3]

    signed_segment_length = ((G_xmin + G_xmax) / 2 - (Theta_xmax + Theta_xmin) / 2) / num_sections
    print(signed_segment_length)
    breakpoints = [[] for _ in range(num_sections - 1)]

    upper_bound, lower_bound = workspace_ymax, workspace_ymin
    print(f"upper_bound: {upper_bound}, lower_bound: {lower_bound}")
    for i in range(num_sections - 1):
        vertical_line = round(Theta_xmin + (i + 1) * signed_segment_length, 2)
        print(f"vertical_line: {vertical_line}")

        meeting_obstacles = []

        for obstacle in O:
            solver = Optimize()
            constraints = [
                x == vertical_line
            ]
            A_obstacle, b_obstacle = obstacle.A, obstacle.b

            for j in range(len(A_obstacle)):
                constraints.append(A_obstacle[j][0] * x + A_obstacle[j][1] * y <= b_obstacle[j])

            solver.add(constraints)

            solver.push()
            solver.minimize(y)
            if solver.check() == sat:
                m = solver.model()
                y_min = m[y].as_decimal(2)
            else:
                y_min = None
            solver.pop()

            solver.push()
            solver.maximize(y)
            if solver.check() == sat:
                m = solver.model()
                y_max = m[y].as_decimal(2)
            else:
                y_max = None
            solver.pop()
            if y_min is not None and y_max is not None:
                # remove possible question marks
                y_min = y_min.replace("?", "")
                y_max = y_max.replace("?", "")
                meeting_obstacles.append((float(y_min), float(y_max)))

        meeting_obstacles.sort(key=lambda y: y[0])

        print(f"meeting_obstacles: {meeting_obstacles}")

        if len(meeting_obstacles) == 0:
            breakpoints[i].append((vertical_line, round((upper_bound + lower_bound) / 2, 2)))

        else:
            for j in range(len(meeting_obstacles) + 1):
                if j == 0:
                    lower = lower_bound
                else:
                    lower = max(lower, meeting_obstacles[j - 1][1])

                if j == len(meeting_obstacles):
                    upper = upper_bound
                else:
                    upper = meeting_obstacles[j][0]

                if upper > lower:
                    breakpoints[i].append((vertical_line, round((upper + lower) / 2, 2)))

        print(f"breakpoints: {breakpoints[i]}")
    return breakpoints


if __name__ == "__main__":
    from convert_polytope_to_arrays import convert_env_polytope_to_arrays

    # from envs.maze_2d import Theta, G, O, workspace

    Theta, G, O, workspace = Env.generate_env(3)
    fig, ax = plot_env("Random Environment", workspace, G, Theta, O)

    breakpoints = find_breakpoints(4, Theta, G, O, workspace)

    # plot breakpoints
    for bp in breakpoints:
        for x, y in bp:
            ax.plot(x, y, 'bo')
    fig.show()
