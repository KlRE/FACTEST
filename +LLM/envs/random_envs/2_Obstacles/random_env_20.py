import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[-0.9429903335828894, 0.3328201177351378], [-0.2003962361487063, 0.9797149322825656], [-0.10202886549856958, -0.9947814386110525], [0.7719302356170494, 0.6357072528611]])
b1 = np.array([-2.3352878261082095, 14.502007622628069, -15.508387555782562, 20.864820192119666])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[0.7787539090832831, 0.6273295378726446], [0.06049506040189014, -0.9981684966311909], [-0.6643638388299201, 0.7474093186836595], [-0.8436614877321074, -0.5368754921931597]])
b2 = np.array([22.027919600541864, -14.515789743433594, 5.705224465951927, -18.759963627206687])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
