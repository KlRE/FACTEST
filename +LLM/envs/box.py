import polytope as pc
import numpy as np

title = 'Box'
A = np.array([[-1, 0],
              [1, 0],
              [0, -1],
              [0, 1]])

O_vertices = [[5, 1], [1, 5], [5, 9], [9, 5]]

O1 = pc.qhull(np.array(O_vertices))

O = [O1]

b_init = np.array([-1.5, 2, -1.5, 2])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-8.5, 9.5, -8.5, 9.5])
G = pc.Polytope(A, b_goal)

b_workspace = np.array([0, 10, 0, 10])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from plot_env import plot_env

    plot_env(title, workspace, G, Theta, O, show=True)
