import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[-0.2982749931359469, 0.9544799780350297], [-0.6033234874818593, -0.7974965639128028], [0.5784287773079325, 0.8157328910752896], [0.7694098843098922, 0.6387553756534956]])
b1 = np.array([13.517822688921107, -13.852168577528898, 15.386205476391005, 15.24447772667581])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[-0.18589166810485097, -0.9825702456970676], [0.6401843996644798, 0.7682212795973761], [-0.7071067811865476, -0.7071067811865476], [0.5087293121266412, 0.8609265282143155]])
b2 = np.array([-11.926278306555494, 18.578151278263206, -17.182694782833106, 17.292883309904823])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
