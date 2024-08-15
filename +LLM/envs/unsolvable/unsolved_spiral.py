import polytope as pc
import numpy as np

title = '2D Spiral Environment'
A = np.array([[-1, 0],
              [1, 0],
              [0, -1],
              [0, 1]])

b0 = np.array([-0.25, 0.75, -0.25, 0.75])
Theta = pc.Polytope(A, b0)

b1 = np.array([-4, 5, -4, 5])
G = pc.Polytope(A, b1)

b2 = np.array([2, 15, 2, 0])
b3 = np.array([2, 0, 0, 15])
b4 = np.array([-1, 4, -1, 14])
b5 = np.array([-4, 14, -1, 4])
b6 = np.array([-5, 14, -4, 10])
b7 = np.array([-4, 14, -11, 14])
b8 = np.array([-13, 14, -10, 11])

O1 = pc.Polytope(A, b2)
O2 = pc.Polytope(A, b3)
O3 = pc.Polytope(A, b4)
O4 = pc.Polytope(A, b5)
O5 = pc.Polytope(A, b6)
O6 = pc.Polytope(A, b7)
O7 = pc.Polytope(A, b8)

O = [O1, O2, O3, O4, O5, O6, O7]

workspace = pc.Polytope(A, np.array([0, 15, 0, 15]))

if __name__ == "__main__":
    from envs.plot_env import plot_env

    plot_env(title, workspace, G, Theta, O)
