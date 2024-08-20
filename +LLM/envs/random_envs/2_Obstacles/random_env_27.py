import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[-0.9968777365489148, -0.0789606127959537], [-0.05872202195147009, 0.9982743731749959], [0.24253562503633253, -0.970142500145332], [0.9995411791453814, 0.0302891266407692]])
b1 = np.array([-18.4817184325529, 9.542328567113936, 4.001837813099485, 19.715192530476628])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[0.389639990836698, 0.9209672510685588], [0.9740972002433518, -0.22612970719934966], [-0.4307295862149383, 0.90248103778368], [-0.24027356783612724, -0.970705214057954]])
b2 = np.array([13.003349148741075, 15.314199555254408, 0.7978752811314802, -5.009223342247581])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
