import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[-0.10827065342261295, 0.9941214541530831], [-0.9905498667663629, -0.1371530584753426], [0.9197781680807426, -0.39243868504778345], [0.016664352333993233, -0.9998611400396001]])
b1 = np.array([13.890140555453772, -9.558044252859428, 10.040298482769387, -8.157200467489739])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[-0.23560002562150337, 0.971850105688705], [-0.7071067811865507, -0.7071067811865445], [0.9048187022009939, 0.42579703632988003], [-0.1766640627937739, -0.9842712069938843]])
b2 = np.array([12.919716405019255, -23.193102422918756, 24.813322292123736, -19.443141996617644])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
