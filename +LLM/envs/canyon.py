import polytope as pc
import numpy as np

title = '2D Canyon Environment'
A = np.array([[-1, 0],
              [1, 0],
              [0, -1],
              [0, 1]])

theta = np.radians(30)
R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta), np.cos(theta)]])

# Rotate the A matrix
A = A @ R.T
b0 = np.array([0, 1, 0, 1])
Theta = pc.Polytope(A, b0)

b1 = np.array([-4, 5, 0, 1])
G = pc.Polytope(A, b1)

b2 = np.array([2, 7, -1, 3])
b3 = np.array([2, 7, 2, 0])

O1 = pc.Polytope(A, b2)
O2 = pc.Polytope(A, b3)

O = [O1, O2]

workspace = pc.Polytope(A, np.array([2, 7, 2, 3]))

if __name__ == "__main__":
    from plot_env import plot_env

    plot_env(title, workspace, G, Theta, O)
