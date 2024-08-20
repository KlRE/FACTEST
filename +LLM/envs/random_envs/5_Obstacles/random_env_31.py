import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 6'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[0.8944271909999162, 0.44721359549995776], [-0.9996876464081229, -0.02499219116020254], [0.9626509401538991, 0.2707455769182837], [0.17888543819998215, -0.9838699100999078]])
b1 = np.array([23.433992404197795, -16.789754021424418, 21.178320683385774, -12.611423393098836])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[-0.6108034542918217, 0.7917822555634717], [0.7853555476209048, 0.6190449610658897], [-0.9246780984747163, 0.3807498052542946], [-0.3520642981319907, -0.9359758169850485]])
b2 = np.array([7.822808684967092, 22.028761136914838, -1.9798989873223394, -17.184172522481457])
O2 = pc.Polytope(A2, b2)
A3 = np.array([[-0.9892903635744847, 0.14596087331426816], [-0.044400613620720224, -0.9990138064662089], [-0.04833055142332247, 0.9988313960820002], [0.9304083928170915, -0.3665245183824906]])
b3 = np.array([-5.747614833619631, -10.414163924739965, 15.78475809485716, 7.350226303255024])
O3 = pc.Polytope(A3, b3)
A4 = np.array([[0.9982331517348172, 0.05941863998421531], [0.1788854381999828, 0.9838699100999075], [-0.694135570584232, -0.7198442954206853], [-0.9799366622741318, 0.19930915164897586]])
b4 = np.array([14.51835049374317, 14.766992923408608, -12.87750027057933, -9.91396938493948])
O4 = pc.Polytope(A4, b4)
A5 = np.array([[0.1761492525055283, 0.984363469883835], [-0.5754934061746132, -0.8178064193007668], [0.9221943818285312, 0.3867266762506737], [-0.3370726050823486, -0.9414786555748352]])
b5 = np.array([20.61153488729394, -20.81468782753655, 23.53678048073334, -20.28479690999016])
O5 = pc.Polytope(A5, b5)
O = [O1, O2, O3, O4, O5]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
