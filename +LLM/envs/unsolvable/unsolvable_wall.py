import polytope as pc
import numpy as np

title = '2D Wall Environment'
A = np.array([[-1, 0],
              [1, 0],
              [0, -1],
              [0, 1]])

b0 = np.array([0, 1, 0, 1])
Theta = pc.Polytope(A, b0)

b1 = np.array([-8, 9, 0, 1])
G = pc.Polytope(A, b1)

b1 = np.array([0.1, 0, 0, 10])
b2 = np.array([-2, 2.1, 0, 10])
b3 = np.array([0, 2, 0.1, 0])
b4 = np.array([0, 2, -10, 10.1])
b5 = np.array([-4, 5, 3, 4])

O1 = pc.Polytope(A, b1)
O2 = pc.Polytope(A, b2)
O3 = pc.Polytope(A, b3)
O4 = pc.Polytope(A, b4)
O5 = pc.Polytope(A, b5)

O = [O1, O2, O3, O4, O5]

workspace = pc.Polytope(A, np.array([0, 9, 5, 6]))

if __name__ == "__main__":
    from envs.plot_env import plot_env

    plot_env(title, workspace, G, Theta, O)
