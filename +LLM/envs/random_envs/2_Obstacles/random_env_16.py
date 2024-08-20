import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[-0.7911056046385767, 0.6116795912153944], [0.4523761374446805, 0.8918272423909417], [-0.034761587248573346, -0.9993956333964842], [0.9155194540230325, -0.402273699494969]])
b1 = np.array([2.1661613256907835, 15.522964030601752, -3.804655724356355, 9.343847033786584])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[-0.6000000000000001, -0.8000000000000002], [0.10202886549856917, 0.9947814386110525], [0.36765888937108915, -0.9299607201739315], [0.3303504247281063, 0.9438583563660174]])
b2 = np.array([-16.12, 19.916034545320766, -12.5609578203958, 19.854060526159177])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
