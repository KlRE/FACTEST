import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[0.8384436163006372, 0.5449883505954141], [-0.9715203387831298, 0.23695618019100717], [0.997458699830735, -0.07124704998790984], [-0.7241379310344825, -0.6896551724137933]])
b1 = np.array([24.30648043655547, -13.748197574682242, 18.41023771687585, -21.075862068965517])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[0.4138029443011841, 0.9103664774626049], [0.9964482918573747, -0.0842068979034398], [-0.9999457509425375, 0.010416101572318218], [-0.08169323944527156, -0.9966575212323127]])
b2 = np.array([14.209993107302662, 16.689807164461833, -10.6879618233556, -1.970440935419949])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
