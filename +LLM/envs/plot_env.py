import matplotlib.pyplot as plt

import os
import sys

currFile = os.path.abspath(__file__)

factestPath2 = currFile.replace('/+LLM/envs/plot_env.py', '')
sys.path.append(factestPath2)

from factest.plotting.plot_polytopes import plotPoly, plotPoly_3d


def plot_env(title, workspace, G, Theta, O, save=False, plot3d=False, dir='./plots/'):
    """
    Plot the environment with the workspace, goal region, initial region, and obstacles
    """
    if plot3d:
        plotPolytope = plotPoly_3d
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # set the axis limits
        ax.set_xlim(-50, 55)
        ax.set_ylim(-10, 55)
        ax.set_zlim(-30, 35)
    else:
        plotPolytope = plotPoly
        fig, ax = plt.subplots()

    if workspace:
        plotPolytope(workspace, ax, 'yellow')
    plotPolytope(G, ax, 'green')
    plotPolytope(Theta, ax, 'blue')

    i = 1
    for obstacle in O:
        print('plotting poly #', i)
        plotPolytope(obstacle, ax, 'red')
        i += 1

    ax.autoscale_view()
    plt.title(title)
    # plt.show()

    if save:
        os.makedirs(dir, exist_ok=True)
        path = os.path.join(dir, title)
        fig.savefig(path)

    return fig, ax


if __name__ == "__main__":
    # plot all the environments in this directory
    # import all the environments
    import os
    import importlib.util

    save = False  # if save is True, it will REMOVE all plot files from the plots directory

    if save:  # only remove files
        for file in os.listdir('./plots/'):
            os.remove('./plots/' + file)

    for env in os.listdir('.'):
        if env.endswith('.py') and env != '__init__.py' and env != 'plot_env.py':
            spec = importlib.util.spec_from_file_location(env, env)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            print('plotting ', env)
            plot_env(module.title, module.workspace, module.G, module.Theta, module.O, save)
