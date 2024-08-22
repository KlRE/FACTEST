from typing import List
import matplotlib.pyplot as plt

from z3 import *

from envs.plot_env import plotPoly

SAVE_PATH = '../old_files/+llm/images/llama3/1'

new_path = [
    (0.5, 3.5),
    (1.0, 3.5),
    (1.5, 3.5),
    (2.0, 3.5),
    (2.5, 3.5),
    (3.0, 3.5)
]


# path = [(0.5, 3.5), (1.5, 3.5), (2.5, 3.5), (2.5, 2.5), (3.5, 2.5), (3.5, 3.0), (5.0, 5.0)] leads to incorrect collision detection todo

def evaluate_waypoints(path, SAVE_PATH, Theta, G, O, workspace, iteration, save=True):
    FACTEST_prob = CollisionDetector(Theta, G, O, workspace=workspace, model=None, seg_max=0, part_max=0,
                                     print_statements=True)
    xref = path

    intersections, successful, starts_in_init, ends_in_goal = FACTEST_prob.detect_Collisions(xref)

    xref_1 = [xval[0] for xval in xref]
    xref_2 = [xval[1] for xval in xref]

    fig, ax = plt.subplots()
    plotPoly(workspace, ax, 'yellow')
    plotPoly(Theta, ax, 'blue')
    plotPoly(G, ax, 'green')
    plotPoly(O, ax, 'red')
    ax.plot(xref_1, xref_2, marker='o')

    ax.autoscale_view()

    plt.title(f'Path evaluation for iteration {iteration}')

    if save:
        plt.savefig(f'{SAVE_PATH}/plot_{iteration}.png')
        path_file = open(f'{SAVE_PATH}/path.txt', 'a')
        path_file.write(str(xref) + '\n')

    # plt.show()

    return intersections, successful, starts_in_init, ends_in_goal


class CollisionDetector():
    def __init__(self, initial_poly, goal_poly, unsafe_polys, model=None, workspace=None, seg_max=3, part_max=2,
                 print_statements=False):
        self.initial_parts = {0: {'poly': initial_poly, 'depth': 0, 'xref': None}}
        self.final_parts = {}
        self.goal_poly = goal_poly
        self.unsafe_polys = unsafe_polys
        self.workspace = workspace

        self.model = model

        self.dims = len(self.goal_poly.A[0])
        self.seg_max = seg_max
        self.part_max = part_max
        self.print_statements = print_statements

    def detect_Collisions(self, xrefs: List):
        # returns  a string with the obstacles that the path intersects with and
        #          True if the path is successful, False otherwise
        # todo add the workspace constraints
        ends_in_goal = False
        starts_in_init = False
        successful = False
        intersects = False

        num_segs = len(xrefs) - 1

        self.s = z3.Solver()

        intersections = [[] for i in range(num_segs)]
        for seg in range(num_segs):  # test which segment intersects with which obstacle

            for idx, obstacle in enumerate(self.unsafe_polys):
                x = Real('x')  # possible intersection point x
                y = Real('y')  # possible intersection point y
                a = Real('a')  # a is the parameter for the line segment
                constraints = [a <= 1, a >= 0]  # a is between 0 and 1
                A_obs = obstacle.A
                b_obs = obstacle.b

                for j in range(len(A_obs)):  # add the obstacle constraints so that x and y are within the obstacle
                    constraints.append(A_obs[j][0] * x + A_obs[j][1] * y <= b_obs[j])

                # add the line segment constraints so that x and y are on the line segment
                constraints.append(x == a * xrefs[seg][0] + (1 - a) * xrefs[seg + 1][0])
                constraints.append(y == a * xrefs[seg][1] + (1 - a) * xrefs[seg + 1][1])

                self.s.add(constraints)
                if self.s.check() == z3.sat:  # if the constraints are satisfiable, then the line segment intersects with the obstacle
                    intersections[seg].append((idx, obstacle))
                    intersects = True
                self.s.reset()

        # check for goal constraints
        A_goal = self.goal_poly.A
        b_goal = self.goal_poly.b

        for row in range(len(A_goal)):
            A_row = A_goal[row]
            b_val = b_goal[row]

            row_sum = 0
            for j in range(self.dims):
                row_sum += xrefs[-1][j] * A_row[j]

            self.s.add(bool(row_sum <= b_val))
        ends_in_goal = self.s.check() == z3.sat
        self.s.reset()

        # check for initial constraints
        A_init = self.initial_parts[0]['poly'].A
        b_init = self.initial_parts[0]['poly'].b

        for row in range(len(A_init)):
            A_row = A_init[row]
            b_val = b_init[row]

            row_sum = 0
            for j in range(self.dims):
                row_sum += xrefs[0][j] * A_row[j]

            self.s.add(bool(row_sum <= b_val))
        starts_in_init = self.s.check() == z3.sat
        self.s.reset()

        successful = starts_in_init and ends_in_goal and not intersects

        return intersections, successful, starts_in_init, ends_in_goal


if __name__ == "__main__":
    from import_env import import_environment, Env

    Theta, G, O, workspace = import_environment(Env.MAZE_2D)
    intersections, succ, si, eg = evaluate_waypoints(new_path, SAVE_PATH, Theta, G, O, workspace, 1, save=False)
    print(intersections[4][0][1].tolist(), succ, si, eg)
