import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 8'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[-0.9894610641341027, -0.1447991801171858], [0.14142135623730942, 0.9899494936611666], [0.10748184298009195, -0.9942070475658493], [0.520607424264656, -0.853796175794036]])
b1 = np.array([-5.820927040710869, 19.926269093836908, -15.122695307298919, -9.860304615572588])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[-0.7399400733959437, -0.6726727939963126], [-0.5368754921931593, -0.8436614877321075], [0.573462344363328, 0.8192319205190409], [0.5881716976750463, 0.8087360843031883]])
b2 = np.array([-13.191113490267691, -14.549325838434617, 14.721597611727162, 14.645475272108648])
O2 = pc.Polytope(A2, b2)
A3 = np.array([[-0.5122783012082032, -0.8588195049666942], [0.8904346821960806, 0.455111059789108], [-0.9333456062030596, -0.358979079308869], [0.05121475197315817, 0.9986876634765888]])
b3 = np.array([-20.194311973804556, 22.338038060692345, -17.862798986409324, 17.6229961539638])
O3 = pc.Polytope(A3, b3)
A4 = np.array([[7.263141282594485e-17, 1.0], [-0.9578262852211515, 0.28734788556634544], [0.888217643155949, 0.45942291887376674], [0.4606450807636063, -0.8875844239103631]])
b4 = np.array([14.800000000000002, -7.720079858882482, 21.721515604351687, -2.1324496665593258])
O4 = pc.Polytope(A4, b4)
A5 = np.array([[0.8574929257125437, 0.5144957554275275], [0.8944271909999166, 0.4472135954999564], [0.6000000000000004, 0.7999999999999997], [-0.6925318281897138, -0.7213873210309513]])
b5 = np.array([23.289507862352703, 23.031500168247824, 22.720000000000002, -22.971857850909622])
O5 = pc.Polytope(A5, b5)
A6 = np.array([[-0.7361676171009339, 0.6767992608831165], [0.358979079308869, -0.9333456062030596], [0.9991330730923519, 0.041630544712181895], [0.9486832980505139, -0.31622776601683766]])
b6 = np.array([-1.0413209680605164, -5.585714474046003, 17.064360277523136, 11.257708470199436])
O6 = pc.Polytope(A6, b6)
A7 = np.array([[0.92847669088526, 0.3713906763541025], [0.17888543819998262, 0.9838699100999077], [-0.31622776601683705, -0.9486832980505141], [-0.38461538461538486, -0.923076923076923]])
b7 = np.array([22.970513332501305, 20.93854054130803, -22.294057504187062, -22.961538461538463])
O7 = pc.Polytope(A7, b7)
O = [O1, O2, O3, O4, O5, O6, O7]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
