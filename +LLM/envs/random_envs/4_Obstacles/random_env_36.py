import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 5'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[-0.9968152785361251, 0.07974522228288969], [0.9623737903724554, 0.2717290702228108], [-0.9950371902099892, -0.09950371902099886], [0.0, -1.0]])
b1 = np.array([-14.150789694098838, 19.34597759540487, -16.59722033270262, -7.8])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[0.35112344158839104, 0.9363291775690449], [-0.2911616157826957, 0.9566738804288586], [0.5380354529218652, -0.8429222095775883], [-0.9639926182060738, 0.2659289981258136]])
b2 = np.array([23.057105997637716, 13.289448034653061, -5.895075112513895, -8.227178379517353])
O2 = pc.Polytope(A2, b2)
A3 = np.array([[-0.12403473458920847, -0.9922778767136677], [-0.28855095721796775, -0.9574645398596204], [0.6163082616581109, 0.7875050010075856], [0.09950371902099875, 0.9950371902099893]])
b3 = np.array([-17.27803852827674, -18.309869830740137, 20.80725170053521, 18.5474932255142])
O3 = pc.Polytope(A3, b3)
A4 = np.array([[0.7071067811865464, 0.7071067811865487], [-0.9954954725939522, -0.09480909262799554], [0.9340518348510854, 0.35713746626659143], [0.9486832980505139, -0.31622776601683783]])
b4 = np.array([16.26345596729061, -5.603217374314532, 10.52181919846958, 0.09486832980505344])
O4 = pc.Polytope(A4, b4)
O = [O1, O2, O3, O4]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
