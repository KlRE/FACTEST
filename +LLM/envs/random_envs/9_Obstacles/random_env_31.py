import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 10'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[-0.14614123375942337, -0.9892637362176346], [0.273383556184878, 0.9619051050949412], [-0.7071067811865469, -0.7071067811865481], [-0.9863939238321441, 0.1643989873053563]])
b1 = np.array([-19.235558852749943, 21.053571421304326, -19.233304448274097, -5.079928707735562])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[-0.7208330649018561, -0.6931087162517844], [0.9994059993535875, -0.03446227583977935], [-0.9995269630766538, 0.030754675786974134], [0.9325680982740896, 0.36099410255771214]])
b2 = np.array([-20.18887068698198, 17.837673974669546, -15.298913470230193, 21.79501894192187])
O2 = pc.Polytope(A2, b2)
A3 = np.array([[-0.8619342151577697, 0.5070201265633936], [-0.341743063086703, -0.9397934234884376], [0.6866235329637169, 0.727013152549817], [0.6139406135149202, -0.7893522173763265]])
b3 = np.array([-4.710216975773935, -19.778379776143005, 25.352564214195578, -2.376827232322057])
O3 = pc.Polytope(A3, b3)
A4 = np.array([[0.9067211118885073, 0.4217307497155848], [-0.4434356937903485, -0.8963061895762366], [0.3867266762506739, 0.922194381828531], [-0.8609265282143155, 0.5087293121266411]])
b4 = np.array([17.24667900961884, -16.922260859199344, 19.67843817998623, 5.376877498938498])
O4 = pc.Polytope(A4, b4)
A5 = np.array([[-0.34689587025541846, -0.9379036492090944], [0.9429903335828896, -0.33282011773513753], [-0.44721359549995887, -0.8944271909999154], [0.15118323329573913, 0.9885057561644475]])
b5 = np.array([-19.794906196389746, 4.809250701272736, -19.319627325598177, 20.253901469835316])
O5 = pc.Polytope(A5, b5)
A6 = np.array([[0.966705227861512, 0.25589256031628216], [0.8459256025956526, -0.5333009233755198], [0.6316729511622354, 0.7752349855172896], [-0.9976534220466451, -0.06846641131692688]])
b6 = np.array([22.251279744835855, 10.838881525432127, 23.538431152854585, -17.52544511395273])
O6 = pc.Polytope(A6, b6)
A7 = np.array([[-0.7926239891046001, 0.6097107608496924], [0.5491778866608373, -0.8357054797012742], [-0.513193961347478, 0.8582726594949203], [0.9863939238321439, 0.1643989873053563]])
b7 = np.array([3.9265372998720194, -5.489391136666369, 8.058030010330144, 16.620737616571606])
O7 = pc.Polytope(A7, b7)
A8 = np.array([[0.9751328557914598, -0.22162110358896814], [-0.5390536964233674, -0.8422714006615114], [0.19047746835532003, 0.9816915676774188], [-0.9629640197141817, -0.2696299255199713]])
b8 = np.array([13.922237727458977, -18.40531464725535, 18.60671823572469, -15.218683367562933])
O8 = pc.Polytope(A8, b8)
A9 = np.array([[-0.8911631156014922, -0.4536830406698507], [0.12073197664807696, -0.9926851413286331], [0.32852062494127254, 0.9444967967061592], [0.43347260995177017, 0.901166741741838]])
b9 = np.array([-11.141159241592474, 1.2985394821704273, 8.537429740661324, 9.574041092961071])
O9 = pc.Polytope(A9, b9)
O = [O1, O2, O3, O4, O5, O6, O7, O8, O9]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
