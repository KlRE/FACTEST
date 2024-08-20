import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 5'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[-0.554700196225229, -0.8320502943378437], [-0.6751582587650209, 0.7376729123543748], [0.619644288579021, -0.7848827655334261], [0.9601952966035754, -0.27932954083013123]])
b1 = np.array([-18.748866632412742, 2.7356412410701223, -1.342562625254537, 11.504885462941017])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[-0.4472135954999599, -0.8944271909999151], [0.6578293866260034, -0.7531669788906415], [-0.869064731380397, -0.4946983855549952], [-0.016664352333993136, 0.9998611400396001]])
b2 = np.array([-15.563033123398547, -3.17474182241245, -14.327534863803592, 19.20566606492732])
O2 = pc.Polytope(A2, b2)
A3 = np.array([[0.8262273428075478, 0.5633368246415096], [-0.7203202134914811, 0.6936416870658706], [0.9276435179375498, -0.3734668708579745], [-0.9904922731777517, -0.13756837127468782]])
b3 = np.array([18.376047219806047, 5.423744422326596, 4.6370128578462735, -9.34914651182778])
O3 = pc.Polytope(A3, b3)
A4 = np.array([[-0.8232127859153061, -0.5677329558036597], [1.4634758051877144e-16, -1.0], [0.09480909262799493, 0.9954954725939523], [1.0, -0.0]])
b4 = np.array([-23.66594826267555, -16.599999999999998, 20.86274083279039, 17.4])
O4 = pc.Polytope(A4, b4)
O = [O1, O2, O3, O4]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
