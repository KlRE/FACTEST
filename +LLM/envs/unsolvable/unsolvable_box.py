import polytope as pc
import numpy as np

title = '2D Box Obstacle Boundary Environment Unsolvable'
A = np.array([[-1, 0],
              [1, 0],
              [0, -1],
              [0, 1]])

b_init = np.array([-1.5, 2, -1.5, 2])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-8.5, 9.5, -8.5, 9.5])
G = pc.Polytope(A, b_goal)

b1 = np.array([0.1, 0, 0, 10])
b2 = np.array([-10, 10.1, 0, 10])
b3 = np.array([0, 10, 0.1, 0])
b4 = np.array([0, 10, -10, 10.1])
b5 = np.array([-4.9, 5, 0, 10])

O1 = pc.Polytope(A, b1)
O2 = pc.Polytope(A, b2)
O3 = pc.Polytope(A, b3)
O4 = pc.Polytope(A, b4)
O5 = pc.Polytope(A, b5)

O = [O1, O2, O3, O4, O5]

b_workspace = np.array([0, 10, 0, 10])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env

    plot_env(title, workspace, G, Theta, O)
