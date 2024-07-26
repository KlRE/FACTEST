import sys, os
from typing import List

currFile = os.path.abspath(__file__)
modelPath = currFile.replace('/factest/synthesis/factest_base_z3.py', '')
sys.path.append(modelPath)

import numpy as np
import polytope as pc
import z3

from common_functions import partition_polytope


class FACTEST_Z3():
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

    def add_initial_constraints(self, init_poly):
        init_center = init_poly.chebXc
        for j in range(self.dims):
            self.s.add(self.x_ref_terms[0][j] == init_center[j])

    def add_goal_constraints(self, num_segs, err_bounds):
        A_goal = self.goal_poly.A
        b_goal = self.goal_poly.b

        err = err_bounds[-1]

        for row in range(len(A_goal)):  # remove this part?
            A_row = A_goal[row]
            b_val = b_goal[row] - np.linalg.norm(A_row) * err  # TODO: Need to deal with the bloating

            row_sum = 0
            for j in range(self.dims):
                row_sum += self.x_ref_terms[num_segs][j] * A_row[j]

            self.s.add(row_sum <= b_val)

        goal_center = self.goal_poly.chebXc
        for j in range(self.dims):
            self.s.add(self.x_ref_terms[num_segs][j] == goal_center[j])

    def add_unsafe_constraints(self, num_segs, err_bounds):
        for seg in range(num_segs):
            err = err_bounds[seg]

            for obstacle in self.unsafe_polys:
                A_obs = obstacle.A
                b_obs = obstacle.b

                obs_constraints = []
                for row in range(len(A_obs)):
                    A_row = A_obs[row]
                    b_val = b_obs[row] + np.linalg.norm(A_row) * err  # TODO: Need to deal with the bloating

                    row_sum_0 = 0
                    row_sum_1 = 0
                    for j in range(self.dims):
                        row_sum_0 += self.x_ref_terms[seg][j] * A_row[j]
                        row_sum_1 += self.x_ref_terms[seg + 1][j] * A_row[j]
                    print(type(row_sum_0), type(b_val))
                    row_constraint = z3.And(row_sum_0 > b_val, row_sum_1 > b_val)
                    obs_constraints.append(row_constraint)

                self.s.add(z3.Or(tuple(obs_constraints)))

    def add_workspace_constraints(self, num_segs, err_bounds):
        try:
            A_workspace = self.workspace.A
            b_workspace = self.workspace.b

            for i in range(num_segs + 1):
                err = err_bounds[num_segs - 1]

                for row in range(len(A_workspace)):
                    A_row = A_workspace[row]
                    b_val = b_workspace[row] - np.linalg.norm(A_row) * err  # TODO: Need to deal with the bloating

                    row_sum = 0
                    for j in range(self.dims):
                        row_sum += self.x_ref_terms[i][j] * A_row[j]

                    self.s.add(row_sum <= b_val)
        except:
            print('no workspace!')

    def get_xref(self, init_poly):
        for num_segs in range(1, self.seg_max + 1):
            self.x_ref_terms = [[z3.Real('xref_%s[%s]' % (j + 1, i)) for j in range(self.dims)] for i in
                                range(num_segs + 1)]
            self.s = z3.Solver()

            if self.model != None:
                err_bounds = [self.model.errBound(init_poly, i) for i in range(num_segs)]
            else:
                err_bounds = [0 for i in range(num_segs)]

            self.add_initial_constraints(init_poly)
            self.add_goal_constraints(num_segs, err_bounds)
            self.add_unsafe_constraints(num_segs, err_bounds)
            self.add_workspace_constraints(num_segs, err_bounds)

            x_ref = None
            if self.s.check() == z3.sat:
                x_ref = []
                if self.print_statements:
                    print('SAT for %s segments' % (num_segs))
                m = self.s.model()
                for x_val_term in self.x_ref_terms:
                    x_val = [m[x_val_term[i]] for i in range(self.dims)]
                    x_ref.append([float(x_val[i].as_fraction()) for i in range(self.dims)])

                return x_ref
            else:
                if self.print_statements:
                    print('UNSAT for %s segments' % (num_segs))
                pass

        return x_ref

    def run(self, force_partition=False):
        if not force_partition:
            init_poly = self.initial_parts[0]['poly']
            depth = self.initial_parts[0]['depth']

            xref = self.get_xref(init_poly)

            self.initial_parts[0] = {'poly': init_poly, 'depth': depth, 'xref': xref}

        k = 0
        while len(self.final_parts.keys()) != len(self.initial_parts.keys()):
            poly_keys = list(self.initial_parts.keys())
            i = 0
            new_dict = {}
            for key in poly_keys:
                init_poly = self.initial_parts[key]['poly']
                depth = self.initial_parts[key]['depth']
                xref = self.initial_parts[key]['xref']

                if depth >= self.part_max or xref != None:
                    self.final_parts[k] = self.initial_parts[key]
                    k += 1
                    new_dict[i] = self.initial_parts[key]
                    i += 1
                else:
                    new_polys = partition_polytope(init_poly, self.dims)
                    for poly in new_polys:
                        xref = self.get_xref(poly)
                        new_dict[i] = {'poly': poly, 'depth': depth + 1, 'xref': xref}
                        i += 1

            self.initial_parts = new_dict

        return self.final_parts

    def evaluate_waypoints(self, xrefs: List):
        # returns  a string with the obstacles that the path intersects with and
        #          True if the path is successful, False otherwise
        # todo add the workspace constraints
        ends_in_goal = False
        starts_in_init = False
        successful = False

        num_segs = len(xrefs) - 1
        err_bounds = [0 for i in range(num_segs)]
        self.s = z3.Solver()

        intersections = [[] for i in range(num_segs)]
        for seg in range(num_segs):  # test which segment intersects with which obstacle
            err = err_bounds[seg]

            for idx, obstacle in enumerate(self.unsafe_polys):
                A_obs = obstacle.A
                b_obs = obstacle.b

                obs_constraints = []
                for row in range(len(A_obs)):
                    A_row = A_obs[row]
                    b_val = b_obs[row] + np.linalg.norm(A_row) * err  # TODO: Need to deal with the bloating

                    row_sum_0 = 0
                    row_sum_1 = 0
                    for j in range(self.dims):
                        row_sum_0 += xrefs[seg][j] * A_row[j]
                        row_sum_1 += xrefs[seg + 1][j] * A_row[j]
                    # print(type(row_sum_0), type(b_val))
                    row_constraint = z3.And(bool(row_sum_0 >= b_val), bool(row_sum_1 >= b_val))
                    obs_constraints.append(row_constraint)

                self.s.add(z3.Or(tuple(obs_constraints)))
                if self.s.check() != z3.sat:
                    intersections[seg].append((idx, obstacle))
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

        obstacle_report = []
        for i, intersection in enumerate(intersections):
            if len(intersection) > 0:
                obstacle_report.append(
                    f'Segment {i + 1} between points {xrefs[i]} and {xrefs[i + 1]} intersects with obstacle(s):')
                for idx, obs in intersection:
                    obstacle_report.append(f"Obstacle {idx + 1}: ({-obs.b[0]}, {obs.b[1]}, {-obs.b[2]}, {obs.b[3]})")

        if len(obstacle_report) == 0 and starts_in_init and ends_in_goal:
            successful = True
            obstacle_feedback_str = 'No intersections found. You solved this task successfully!'
        else:
            obstacle_feedback_str = '\n'.join(obstacle_report)

        return obstacle_feedback_str, successful, starts_in_init, ends_in_goal


if __name__ == "__main__":
    # TODO: Make sure that this section is clean and works with current FACTEST setup
    import matplotlib.pyplot as plt
    from factest.plotting.plot_polytopes import plotPoly

    print('testing!')

    A = np.array([[-1, 0],
                  [1, 0],
                  [0, -1],
                  [0, 1]])
    b_init = np.array([[0], [1], [0], [1]])
    b_goal = np.array([[-4], [5], [-4], [5]])
    b_unsafe1 = np.array([[-3], [3.5], [0], [5]])
    b_unsafe2 = np.array([[-3], [7], [-5.5], [6]])
    b_unsafe3 = np.array([[-3], [7], [1], [0]])
    b_workspace = np.array([0, 7, 1, 7])

    initial_poly = pc.Polytope(A, b_init)
    goal_poly = pc.Polytope(A, b_goal)
    unsafe_polys = [pc.Polytope(A, b_unsafe1), pc.Polytope(A, b_unsafe2), pc.Polytope(A, b_unsafe3)]
    workspace_poly = pc.Polytope(A, b_workspace)

    FACTEST_prob = FACTEST_Z3(initial_poly, goal_poly, unsafe_polys, workspace=workspace_poly)
    # result_dict = FACTEST_prob.run()
    # result_keys = list(result_dict.keys())
    # xref = result_dict[result_keys[0]]['xref']

    # print(result_dict)
    xref = [[0.5, 0.5], [0.0, 3.25], [3.75, 5.25], [4.5, 4.5]]
    FACTEST_prob.evaluate_waypoints(xref)
    xref_1 = [xval[0] for xval in xref]
    xref_2 = [xval[1] for xval in xref]

    fig, ax = plt.subplots()
    plotPoly(workspace_poly, ax, 'yellow')
    plotPoly(initial_poly, ax, 'blue')
    plotPoly(goal_poly, ax, 'green')
    plotPoly(unsafe_polys, ax, 'red')
    ax.plot(xref_1, xref_2, marker='o')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    plt.show()
