import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 2'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[-0.27472112789737796, -0.9615239476408232], [0.39391929857916735, -0.9191450300180583], [-0.894427190999916, -0.4472135954999578], [0.18666064582327038, 0.982424451701422]])
b1 = np.array([-17.238750775560472, -11.817578957375037, -9.167878707749136, 19.072788305331407])
O1 = pc.Polytope(A1, b1)
O = [O1]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
