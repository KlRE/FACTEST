import polytope as pc
import numpy as np

title = '2D Diagonal Wall Environment Unsolvable'
A = np.array([[-1, 0],
              [1, 0],
              [0, -1],
              [0, 1]])

b0 = np.array([0, 1, 0, 1])
Theta = pc.Polytope(A, b0)

b1 = np.array([-4, 5, -4, 5])
G = pc.Polytope(A, b1)

b2 = np.array([-4, 6, 2, 0])
b3 = np.array([-2, 4, 0, 2])
b4 = np.array([0, 2, -2, 4])

b5 = np.array([0.1, 0, 2, 7])
b6 = np.array([-6, 6.1, 2, 7])
b7 = np.array([0, 6, 2.1, -2])
b8 = np.array([0, 6, -7, 7.1])

O1 = pc.Polytope(A, b2)
O2 = pc.Polytope(A, b3)
O3 = pc.Polytope(A, b4)
O4 = pc.Polytope(A, b5)
O5 = pc.Polytope(A, b6)
O6 = pc.Polytope(A, b7)
O7 = pc.Polytope(A, b8)

O = [O1, O2, O3, O4, O5, O6, O7]

workspace = pc.Polytope(A, np.array([5, 7, 5, 7]))

if __name__ == "__main__":
    from envs.plot_env import plot_env

    plot_env(title, workspace, G, Theta, O)
