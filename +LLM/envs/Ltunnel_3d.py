import polytope as pc
import numpy as np

title = '3D L-tunnel Environment'
A = np.array([[-1, 0, 0],
              [1, 0, 0],
              [0, -1, 0],
              [0, 1, 0],
              [0, 0, -1],
              [0, 0, 1]])

b1 = np.array([0, 40, 0, 5, -25, 40])
b2 = np.array([0, 10, 0, 5, -5, 25])
b3 = np.array([-30, 40, 0, 5, -5, 25])
b4 = np.array([-15, 25, 0, 5, 0, 20])
b5 = np.array([0, 40, 0, 5, 5, 0])
b6 = np.array([0, 40, 0, 5, -40, 45])
b7 = np.array([0, 40, -5, 10, 0, 40])
b8 = np.array([0, 40, 5, 0, 0, 40])

O1 = pc.Polytope(A, b1)
O2 = pc.Polytope(A, b2)
O3 = pc.Polytope(A, b3)
O4 = pc.Polytope(A, b4)
O5 = pc.Polytope(A, b5)
O6 = pc.Polytope(A, b6)
O7 = pc.Polytope(A, b7)
O8 = pc.Polytope(A, b8)

O = [O1, O2, O3, O4, O5, O6, O7, O8]

b_init = np.array([-0.5, 1.5, -2, 3, -2, 3])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-38, 40, -1.5, 3.5, -1.5, 3.5])
G = pc.Polytope(A, b_goal)

b_workspace = np.array([0, 40, 0, 40, 0, 40])

if __name__ == "__main__":
    from plot_env import plot_env

    plot_env(title, None, G, Theta, O, plot3d=True)
