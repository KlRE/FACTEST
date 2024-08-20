import polytope as pc
import numpy as np

title = '2D Random Obstacle Environment 3'

A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
b_init = np.array([0.0, 2.0, 0.0, 2.0])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-18.0, 20.0, -18.0, 20.0])
G = pc.Polytope(A, b_goal)

A1 = np.array([[0.25912856608734974, 0.9658428372346683], [-0.9761870601839527, -0.2169304578186563], [0.9957851087622359, -0.09171704949125849], [0.9662349396012464, -0.2576626505603326]])
b1 = np.array([17.107196790239414, -18.254698025439918, 18.579253739800667, 17.21830662369421])
O1 = pc.Polytope(A1, b1)
A2 = np.array([[0.8436614877321075, 0.5368754921931596], [-0.367658889371089, 0.9299607201739315], [0.9943091539198089, -0.10653312363426552], [-0.4327310675847713, -0.9015230574682737]])
b2 = np.array([22.14227922802359, 12.930779409116134, 16.633371703429944, -16.717843577691667])
O2 = pc.Polytope(A2, b2)
O = [O1, O2]

b_workspace = np.array([2.0, 22.0, 2.0, 22.0])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    plot_env(title, workspace, G, Theta, O)
