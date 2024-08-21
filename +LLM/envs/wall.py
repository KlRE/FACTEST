import polytope as pc
import numpy as np

title = 'Wall'
A = np.array([[-1, 0],
              [1, 0],
              [0, -1],
              [0, 1]])

b0 = np.array([0, 1, 0, 1])
Theta = pc.Polytope(A, b0)

b1 = np.array([-8, 9, 0, 1])
G = pc.Polytope(A, b1)

b2 = np.array([-4, 5, 3, 4])

o1_vertices = [[2, -4], [3, -4], [7, 4], [6, 4]]
O1 = pc.qhull(np.array(o1_vertices))

O = [O1, ]

workspace = pc.Polytope(A, np.array([0, 9, 6, 6]))

if __name__ == "__main__":
    from plot_env import plot_env

    plot_env(title, workspace, G, Theta, O)
