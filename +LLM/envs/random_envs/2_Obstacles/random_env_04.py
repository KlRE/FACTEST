import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[0.9908301680442992, -0.13511320473331218], [0.8656198954419587, -0.5007017042262313], [-0.13621834047872847, 0.9906788398452959], [-0.9875494683780145, -0.15730876487437392]])
b1 = np.array([16.79457134835089, 10.042039434083035, 11.592180774739765, -12.840764901662094])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[-0.14284970606061217, 0.9897443919913853], [-0.07754358600819261, -0.9969889629624745], [0.0, 1.0], [0.628337107087621, -0.7779411802037217]])
b2 = np.array([15.76346506378857, -16.144574606905675, 17.5, -5.5712556828435815])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
