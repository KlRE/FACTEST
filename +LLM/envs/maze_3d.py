import polytope as pc
import numpy as np

title = 'Maze_3d Environment'

A_cube = np.array([[-1, 0, 0],
                   [1, 0, 0],
                   [0, -1, 0],
                   [0, 1, 0],
                   [0, 0, -1],
                   [0, 0, 1]])

# Defining obstacles
b01 = np.array([0, 45, 5, 10, 10, -5])
b02 = np.array([5, 0, 5, 10, 10, 30])
b03 = np.array([-45, 50, 5, 10, 10, 30])
b04 = np.array([0, 25, 5, 10, 5, 0])
b05 = np.array([-30, 35, 5, 10, 0, 10])
b06 = np.array([-25, 30, 0, 10, 0, 10])
b07 = np.array([-35, 45, 5, 0, 0, 10])
b08 = np.array([-30, 45, 5, 5, -10, 25])
b09 = np.array([0, 45, -5, 10, -20, 25])
b10 = np.array([0, 45, 5, 0, -20, 25])
b11 = np.array([-15, 25, 5, 10, 0, 20])
b12 = np.array([0, 10, 0, 5, -5, 25])
b13 = np.array([0, 15, 5, 0, 0, 20])
b14 = np.array([0, 15, -5, 10, 0, 20])
b15 = np.array([0, 45, 5, 10, -25, 30])
b16 = np.array([5, 50, 10, -5, 10, 30])
b17 = np.array([5, 50, -10, 15, 10, 30])

# Creating polytopes for obstacles
O1 = pc.Polytope(A_cube, b01)
O2 = pc.Polytope(A_cube, b02)
O3 = pc.Polytope(A_cube, b03)
O4 = pc.Polytope(A_cube, b04)
O5 = pc.Polytope(A_cube, b05)
O6 = pc.Polytope(A_cube, b06)
O7 = pc.Polytope(A_cube, b07)
O8 = pc.Polytope(A_cube, b08)
O9 = pc.Polytope(A_cube, b09)
O10 = pc.Polytope(A_cube, b10)
O11 = pc.Polytope(A_cube, b11)
O12 = pc.Polytope(A_cube, b12)
O13 = pc.Polytope(A_cube, b13)
O14 = pc.Polytope(A_cube, b14)
O15 = pc.Polytope(A_cube, b15)
O16 = pc.Polytope(A_cube, b16)
O17 = pc.Polytope(A_cube, b17)

O = [O1, O2, O3, O4, O5, O6, O7, O8, O9, O10, O11, O12, O13, O14, O15, O16, O17]

# Initial region (Theta)
b_init = np.array([-0.5, 1.5, -2, 3, -2, 3])
Theta = pc.Polytope(A_cube, b_init)

# Goal region
b_goal = np.array([-38, 40, -1.5, 3.5, -1.5, 3.5])
G = pc.Polytope(A_cube, b_goal)

# Workspace boundaries
b_workspace = np.array([-50, 55, -10, 55, -30, 35])
workspace = pc.Polytope(A_cube, b_workspace)

if __name__ == "__main__":
    from plot_env import plot_env

    plot_env(title, workspace, G, Theta, O, plot3d=True)
