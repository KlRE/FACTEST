import polytope as pc
import numpy as np

A = np.array([[-1, 0],
              [1, 0],
              [0, -1],
              [0, 1]])

b0 = np.array([0, 1, 0, 1])
Theta = pc.Polytope(A, b0)

b1 = np.array([-4, 5, -4, 5])
goal = pc.Polytope(A, b1)

b2 = np.array([-4, 6, 2, 0])
b3 = np.array([-2, 4, 0, 2])
b4 = np.array([0, 2, -2, 4])

O1 = pc.Polytope(A, b2)
O2 = pc.Polytope(A, b3)
O3 = pc.Polytope(A, b4)

obstacles = [O1, O2, O3]

workspace = pc.Polytope(A, np.array([5, 7, 5, 7]))

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from factest.plotting.plot_polytopes import plotPoly

    fig, ax = plt.subplots()

    plotPoly(goal, ax, 'green')
    plotPoly(Theta, ax, 'blue')
    plotPoly(workspace, ax, 'yellow')

    i = 1
    for obstacle in obstacles:
        print('plotting poly #', i)
        plotPoly(obstacle, ax, 'red')
        i += 1

    ax.set_xlim(-5, 7)
    ax.set_ylim(-5, 7)

    plt.show()
