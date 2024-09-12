import matplotlib.pyplot as plt
import os
from typing import Union, List

import polytope as pc
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull


# plt.rc('axes', titlesize=35)


def plot_env(title, workspace, G, Theta, O, save=False, plot3d=False, dir='./plots/', show=True, path=None):
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

    if path:
        if isinstance(path, List):
            for idx, p in enumerate(path):
                xref_1 = [xval[0] for xval in p]
                xref_2 = [xval[1] for xval in p]
                # use differnt colors for different paths
                ax.plot(xref_1, xref_2, 'o-', linewidth=1, label=f'Path {idx + 1}')
            #  add legend
            ax.legend()

        else:
            xref_1 = [xval[0] for xval in path]
            xref_2 = [xval[1] for xval in path]
            ax.plot(xref_1, xref_2, 'o-', linewidth=1)

    ax.autoscale_view()
    # plt.axis('equal')
    plt.title(title)
    # hide axis
    ax.axis('off')
    if show:
        plt.show()

    if save:
        os.makedirs(dir, exist_ok=True)
        path = os.path.join(dir, title)

        fig.savefig(path, bbox_inches='tight')

    return fig, ax


def plotPoly(poly: Union[pc.Polytope, List[pc.Polytope]], ax=None, color='red'):  # Takes in tulip polytope and plots it
    if ax == None:
        fig, ax = plt.subplots()

    if isinstance(poly, pc.Polytope):
        poly.plot(ax, color=color, alpha=0.25, linestyle="solid", edgecolor="None", linewidth=0)

    else:
        for polygon in poly:
            polygon.plot(ax, color=color, alpha=0.25, linestyle="solid", edgecolor=color, linewidth=0)


def plotPoly_3d(poly, ax, color='r'):
    cubes = [pc.extreme(poly)]
    for cube in cubes:
        hull = ConvexHull(cube)

        # draw the polygons of the convex hull
        for s in hull.simplices:
            tri = Poly3DCollection([cube[s]])
            tri.set_edgecolor(color)
            tri.set_facecolor(color)
            tri.set_alpha(0.5)
            ax.add_collection3d(tri)


if __name__ == "__main__":
    # plot all the environments in this directory
    from envs.maze_2d import Theta, G, O, workspace

    # import importlib.util
    #
    # save = True
    #
    # for env in os.listdir('.'):
    #     if env.endswith('.py') and env != '__init__.py' and env != 'plot_env.py' and "3d" not in env:
    #         spec = importlib.util.spec_from_file_location(env, env)
    #         module = importlib.util.module_from_spec(spec)
    #         spec.loader.exec_module(module)
    #
    #         print('plotting ', env)
    #         plot_env(module.title, module.workspace, module.G, module.Theta, module.O, save, dir='./plots/manual/')
    # concatenate paths in array [(0.5, 3.5), (1.5, 3.5), (3.4, 4.45), (4.5, 4.45), (6.5, 4.75)]
    # [(0.5, 3.5), (1.5, 3.5), (2.8, 3.5), (2.8, 4.2), (3.4, 4.45), (4.5, 4.45), (6.5, 4.75)]
    # [(0.5, 3.5), (1.5, 3.5), (2.8, 3.5), (3.4, 3.5), (3.4, 4.45), (4.5, 4.45), (6.5, 4.75)]
    # [(0.5, 3.5), (1.5, 3.5), (2.8, 3.5), (2.8, 2.95), (3.4, 2.95), (3.4, 2.0), (4.5, 2.0), (5.5, 2.0), (5.5, 4.75), (6.5, 4.75)]
    # [(0.5, 3.5), (1.5, 3.5), (2.8, 3.5), (2.8, 4.0), (3.4, 4.0), (3.4, 4.45), (4.5, 4.45), (5.5, 4.45), (6.5, 4.75)]

    paths = [[(0.5, 3.5), (1.5, 3.5), (3.4, 4.45), (4.5, 4.45), (6.5, 4.75)],
             [(0.5, 3.5), (1.5, 3.5), (2.8, 3.5), (2.8, 4.2), (3.4, 4.45), (4.5, 4.45), (6.5, 4.75)],
             [(0.5, 3.5), (1.5, 3.5), (2.8, 3.5), (3.4, 3.5), (3.4, 4.45), (4.5, 4.45), (6.5, 4.75)],
             [(0.5, 3.5), (1.5, 3.5), (2.8, 3.5), (2.8, 2.95), (3.4, 2.95), (3.4, 2.0), (4.5, 2.0), (5.5, 2.0),
              (5.5, 4.75), (6.5, 4.75)],
             [(0.5, 3.5), (1.5, 3.5), (2.8, 3.5), (2.8, 4.0), (3.4, 4.0), (3.4, 4.45), (4.5, 4.45), (5.5, 4.45),
              (6.5, 4.75)]

             ]
    plot_env('Maze 2D', workspace, G, Theta, O, save=True, dir='./paper', plot3d=False, show=True, path=paths)
