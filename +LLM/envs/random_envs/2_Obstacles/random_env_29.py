import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[0.316227766016838, -0.948683298050514], [0.982872186934322, -0.1842885350501858], [-0.9982226157912, -0.05959538004723559], [0.24253562503633277, 0.970142500145332]])
b1 = np.array([4.079338181617211, 18.207707262958316, -16.236761293869396, 11.399174376707647])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[0.5098023903017334, -0.860291533634174], [0.20863847177051867, -0.9779928364243077], [-0.02478577154316087, 0.9996927855741535], [-0.8364611295797533, -0.5480262573108733]])
b2 = np.array([-7.322036830708627, -13.887498277225173, 18.55545476959497, -14.932273337359948])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
