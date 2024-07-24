import matplotlib.pyplot as plt
from factest.plotting.plot_polytopes import plotPoly


def plot_env(title, workspace, G, Theta, O):
    """
    Plot the environment with the workspace, goal region, initial region, and obstacles
    """

    fig, ax = plt.subplots()

    plotPoly(workspace, ax, 'yellow')
    plotPoly(G, ax, 'green')
    plotPoly(Theta, ax, 'blue')

    i = 1
    for obstacle in O:
        print('plotting poly #', i)
        plotPoly(obstacle, ax, 'red')
        i += 1
    ax.autoscale_view()
    plt.title(title)
    plt.show()
