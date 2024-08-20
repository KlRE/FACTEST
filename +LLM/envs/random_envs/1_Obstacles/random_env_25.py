import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 2'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[0.982872186934322, 0.18428853505018508], [0.12403473458921017, 0.9922778767136675], [0.7592566023652972, -0.6507913734559678], [-0.948683298050514, -0.316227766016838]])
b1 = np.array([18.80971647745558, 21.172729194377904, 2.9502542263337443, -19.38476205683217])
O1 = pc.Polytope(A1, b1)
O = [O1]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
