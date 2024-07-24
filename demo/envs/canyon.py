import polytope as pc
import numpy as np

A = np.array([[-1, 0],
              [1, 0],
              [0, -1],
              [0, 1]])

b0 = np.array([0, 1, 0, 1])
Theta = pc.Polytope(A, b0)

b1 = np.array([-4, 5, -4, 5])
G = pc.Polytope(A, b1)

b2 = np.array([-2, 6, 0, 1])
b3 = np.array([0, 3, -2, 4])

O1 = pc.Polytope(A, b2)
O2 = pc.Polytope(A, b3)

O = [O1, O2]

workspace = pc.Polytope(A, np.array([5, 7, 5, 7]))

if __name__ == "__main__":
    from plot_env import plot_env

    plot_env('2d Canyon Environment', workspace, G, Theta, O)
