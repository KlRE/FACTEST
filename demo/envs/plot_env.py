import matplotlib.pyplot as plt
from factest.plotting.plot_polytopes import plotPoly


def plot_env(title, workspace, G, Theta, O, save=False):
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

    if save:
        path = './plots/'
        os.makedirs(path, exist_ok=True)
        fig.savefig(path + title)


if __name__ == "__main__":
    # plot all the environments in this directory
    # import all the environments
    import os
    import importlib.util
    import shutil

    save = True  # if save is True, it will REMOVE all plot files from the plots directory

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
