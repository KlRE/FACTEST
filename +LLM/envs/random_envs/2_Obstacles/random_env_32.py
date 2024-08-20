import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[0.049120959199793444, -0.9987928370624672], [0.08479983040050854, 0.9963980072059786], [-0.18589166810485092, 0.9825702456970679], [-0.07870248542000996, 0.9968981486534686]])
b1 = np.array([-15.076859743723276, 17.502684994665014, 13.97905344148477, 15.270905587662746])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[-1.0, 0.0], [-0.9847835588179368, -0.17378533390904816], [-0.42443387623071965, 0.9054589359588686], [0.8459256025956526, -0.5333009233755199]])
b2 = np.array([-16.5, -18.438623927749962, 5.673266145617286, 8.398570058813796])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
