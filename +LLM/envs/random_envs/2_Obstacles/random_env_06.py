import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[-0.31622776601683666, 0.9486832980505142], [-0.7848827655334264, 0.6196442885790205], [0.67028625796877, 0.7421026427511384], [0.35112344158839176, -0.9363291775690445]])
b1 = np.array([8.127053586632755, -0.3015602204417926, 16.35977245342348, -3.8857660869115342])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[0.9146866040947617, 0.4041638483209416], [0.9995842091710027, -0.028834159879932833], [-0.9976625651734409, 0.06833305240913978], [-0.9620129872629926, -0.2730036855746332]])
b2 = np.array([20.79954794148507, 17.789715507255856, -15.15080438015447, -17.151131541838733])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
