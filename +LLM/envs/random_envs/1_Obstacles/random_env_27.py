import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 2'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[0.924678098474716, -0.3807498052542951], [-0.3328201177351375, -0.9429903335828896], [-0.033314830232638336, 0.9994449069791543], [-0.05121475197315826, 0.9986876634765888]])
b1 = np.array([8.572309901153835, -20.47398424267321, 18.912829123068867, 18.695945207801472])
O1 = pc.Polytope(A1, b1)
O = [O1]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
