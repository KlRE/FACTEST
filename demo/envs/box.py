import polytope as pc
import numpy as np

A = np.array([[-1, 0],
              [ 1, 0],
              [ 0, -1],
              [ 0, 1]])

b1 = np.array([0.1, 0, 0, 10])
b2 = np.array([-10, 10.1, 0, 10])
b3 = np.array([0, 10, 0.1, 0])
b4 = np.array([0, 10, -10, 10.1])
b5 = np.array([-3, 7, -3, 7])
# TODO: Create more obstacles if needed

O1 = pc.Polytope(A, b1)
O2 = pc.Polytope(A, b2)
O3 = pc.Polytope(A, b3)
O4 = pc.Polytope(A, b4)
O5 = pc.Polytope(A, b5)
# TODO: Create more Polytope objects if needed

O = [O1, O2, O3, O4, O5]

b_init = np.array([-1.5, 2, -1.5, 2])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-8.5, 9.5, -8.5, 9.5])
G = pc.Polytope(A, b_goal)

b_workspace = np.array([0, 10, 0, 10])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from factest.plotting.plot_polytopes import plotPoly

    fig, ax = plt.subplots()

    plotPoly(workspace, ax, 'yellow')
    plotPoly(G, ax, 'green')
    plotPoly(Theta, ax, 'blue')

    i = 1
    for obstacle in O:
        print('plotting poly #', i)
        plotPoly(obstacle, ax, 'red')
        i += 1

    ax.set_xlim(-0.2, 10.2)
    ax.set_ylim(-0.2, 10.2)
    plt.show()