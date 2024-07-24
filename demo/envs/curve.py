import polytope as pc
import numpy as np

title = '2D Curve Environment'
A = np.array([[-1, 0],
              [1, 0],
              [0, -1],
              [0, 1]])

b0 = np.array([-6, 7, 4, -3])
Theta = pc.Polytope(A, b0)

b1 = np.array([-6, 7, -5, 6])
G = pc.Polytope(A, b1)

b2 = np.array([-1, 3, 4, -2])
b3 = np.array([1, 1, 2, 0])
b4 = np.array([3, -1, 0, 2])
b5 = np.array([1, 1, -2, 4])
b6 = np.array([-1, 3, -4, 6])

shift = 6
b8 = np.array([b2[0] - shift, b2[1] + shift, b2[2], b2[3]])
b9 = np.array([b3[0] - shift, b3[1] + shift, b3[2], b3[3]])
b10 = np.array([b4[0] - shift, b4[1] + shift, b4[2], b4[3]])
b11 = np.array([b5[0] - shift, b5[1] + shift, b5[2], b5[3]])
b12 = np.array([b6[0] - shift, b6[1] + shift, b6[2], b6[3]])

O1 = pc.Polytope(A, b2)
O2 = pc.Polytope(A, b3)
O3 = pc.Polytope(A, b4)
O4 = pc.Polytope(A, b5)
O5 = pc.Polytope(A, b6)
O6 = pc.Polytope(A, b8)
O7 = pc.Polytope(A, b9)
O8 = pc.Polytope(A, b10)
O9 = pc.Polytope(A, b11)
O10 = pc.Polytope(A, b12)

O = [O1, O2, O3, O4, O5, O6, O7, O8, O9, O10]

workspace = pc.Polytope(A, np.array([3, 9, 5, 7]))

if __name__ == "__main__":
    from plot_env import plot_env

    plot_env(title, workspace, G, Theta, O)
