import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[-0.3555728284470829, 0.9346485776323322], [-0.010637695937359555, -0.9999434181118173], [0.995893206467704, 0.09053574604251825], [1.0, -0.0]])
b1 = np.array([15.292679390325539, -16.40013582662754, 11.063468166395761, 9.5])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[-0.996729048114676, 0.08081586876605508], [0.2611950472753572, 0.9652860442784946], [-0.053975258015000256, -0.9985422732775084], [0.7893522173763259, -0.6139406135149212]])
b2 = np.array([-9.937657995932536, 18.782195160378848, -13.27521470878936, 6.9726112534908635])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
