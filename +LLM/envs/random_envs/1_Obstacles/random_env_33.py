import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 2'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[0.30224386073392995, -0.9532306376993184], [0.8944271909999165, -0.44721359549995693], [-0.9557790087219501, -0.29408584883752337], [0.230877292467922, 0.9729828754005293]])
b1 = np.array([-12.029305657210424, 4.516857314549602, -13.572061923851697, 20.86635986854728])
O1 = pc.Polytope(A1, b1)
O = [O1]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
