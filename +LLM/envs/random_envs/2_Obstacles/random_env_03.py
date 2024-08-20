import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[-0.9146866040947617, -0.40416384832094115], [0.447213595499958, 0.8944271909999161], [0.9670745372626466, -0.2544932992796438], [0.7661915431257925, 0.6426122619764711]])
b1 = np.array([-18.91912245771816, 22.62900793229787, 15.707326431539617, 22.575463080358027])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[-0.4472135954999565, -0.8944271909999166], [0.20300045060530655, -0.9791786440961847], [-0.48307734291133475, 0.8755776840267944], [0.5240974256643347, 0.851658316704544]])
b2 = np.array([-12.119488438048863, -10.843806423216407, 8.825219208311447, 17.62932715578406])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
