import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[-0.9958932064677039, 0.09053574604251906], [-0.05815384271279062, 0.9983076332362365], [-0.28000000000000036, -0.9600000000000001], [0.4843158830168058, -0.8748932080303583]])
b1 = np.array([-5.631323403844644, 18.737168122061092, -19.420000000000005, -8.750494389603633])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[-0.806933620883472, 0.5906421348734693], [-0.9990958406831207, 0.04251471662481345], [0.9937986902559327, 0.11119425904961472], [0.011235245872283082, -0.9999368826331937]])
b2 = np.array([-6.100251795812884, -10.790235079377705, 19.588953623946836, 0.1213406554206582])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
