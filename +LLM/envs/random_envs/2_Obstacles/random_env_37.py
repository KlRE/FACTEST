import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[-0.9913160239432814, 0.1315011052169658], [0.9611873844983672, -0.2758963788837904], [-0.98058067569092, 0.19611613513818493], [0.0, 1.0]])
b1 = np.array([-13.202710963783378, 11.703346394586601, -11.92386101640157, 18.2])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[-0.7226418571476991, -0.6912226459673645], [-0.7146687659935234, 0.6994630475681289], [0.8843847528469698, -0.4667586195581226], [0.9893591353648533, -0.14549399049483128]])
b2 = np.array([-14.770171175875365, 3.234256309081324, 4.161521587007691, 10.004166786424605])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
