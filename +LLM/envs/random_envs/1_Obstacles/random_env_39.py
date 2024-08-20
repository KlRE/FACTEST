import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 2'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[0.06438227799796514, 0.9979253089684583], [0.8889745564266025, 0.4579565896743113], [-0.4332944348678781, -0.9012524245251862], [-0.40613846605344706, -0.9138115486202575]])
b1 = np.array([13.793903061064015, 21.284205970686635, -16.659304431800173, -16.34707325865126])
O1 = pc.Polytope(A1, b1)
O = [O1]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
