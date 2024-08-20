import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[-0.8637789008984335, 0.5038710255240861], [-0.31622776601683655, -0.9486832980505144], [0.9615239476408234, 0.2747211278973779], [0.5913636636275166, -0.8064049958557061]])
b1 = np.array([-0.6262397031513651, -18.246342099171546, 15.988769643627403, -6.650153199156735])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[0.9315776194850602, 0.36354248565270647], [0.3162277660168381, -0.9486832980505138], [0.19611613513818413, 0.9805806756909202], [-0.909688003863034, -0.41529234958964595]])
b2 = np.array([10.072398993115298, 2.5614449047363896, 10.256873867727025, -8.3117797396442])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
