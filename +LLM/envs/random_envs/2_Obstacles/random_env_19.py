import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[0.9058823529411765, -0.42352941176470593], [0.03843312210120451, -0.9992611746313143], [-0.5214500094539748, 0.8532818336519593], [-0.7387660247839671, 0.6739619875222154]])
b1 = np.array([12.188235294117645, -5.665042197717526, 1.5169454820479338, -4.163011353694918])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[-0.5626240433067091, 0.8267128799608789], [0.916935025341359, -0.39903653880596174], [-0.8516583167045438, 0.5240974256643348], [-0.8125382506296853, -0.582907875451731]])
b2 = np.array([7.284259042321967, 6.809940590984297, 0.2620487128321689, -14.369562323635854])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
