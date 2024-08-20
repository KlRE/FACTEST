import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[-0.9333456062030597, -0.35897907930886913], [0.3162277660168382, -0.9486832980505138], [0.0, 1.0], [0.9986178293325099, -0.05255883312276354]])
b1 = np.array([-16.340727690139722, -10.62525293816575, 17.7, 12.950496481448974])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[-0.9985681322700889, 0.05349472137161173], [0.9397934234884371, 0.34174306308670427], [-0.9578262852211519, -0.2873478855663445], [0.9397934234884373, -0.34174306308670416]])
b2 = np.array([-15.1764524531263, 21.61524874023405, -18.99369523593543, 11.089562397163565])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
