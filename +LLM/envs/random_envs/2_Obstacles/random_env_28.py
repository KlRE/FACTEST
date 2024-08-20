import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[0.9180623535361904, 0.39643601629971886], [0.9965457582448798, 0.08304547985373972], [-0.9958932064677041, 0.09053574604251814], [-0.8944271909999159, -0.4472135954999581]])
b1 = np.array([23.149776846554627, 20.37105620812241, -15.689844789168472, -22.494843853647886])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[0.2800000000000003, -0.96], [-0.279329540830131, -0.9601952966035754], [0.9746917402366387, 0.22355315143042173], [-0.8799053976571924, 0.4751489147348839]])
b2 = np.array([2.9240000000000057, -6.752791649568418, 19.80502079152392, -8.672347599309289])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
