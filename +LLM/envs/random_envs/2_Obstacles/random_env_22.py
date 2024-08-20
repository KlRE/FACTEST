import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[0.561883035583034, -0.8272166912750222], [0.17614925250552835, 0.9843634698838349], [-0.6900753335728398, -0.7237375449666363], [-0.9965457582448797, 0.08304547985373971]])
b1 = np.array([0.2356787177028848, 16.61501919956557, -17.164361589697116, -9.218048263765143])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[-0.9890901778818175, 0.14731130308878118], [-0.05547001962252326, -0.9984603532054125], [0.9738412097417933, 0.2272296156064182], [0.9761870601839531, 0.21693045781865541]])
b2 = np.array([-16.46519479095179, -7.366418605871051, 20.34354287150606, 20.304690851826216])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
