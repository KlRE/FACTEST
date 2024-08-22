import matplotlib.pyplot as plt
import polytope as pc
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def plot_env(title, workspace, G, Theta, O, save=False, plot3d=False):
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
    plt.show()

    if save:
        path = './plots/'
        os.makedirs(path, exist_ok=True)
        fig.savefig(path + title)

def plotPoly(poly, ax=None, color='red'):  # Takes in tulip polytope and plots it
    if ax == None:
        fig, ax = plt.subplots()

    if type(poly) != list:
        poly_verts = pc.extreme(poly)
        polyPatch = Polygon(poly_verts, facecolor=color, edgecolor=color, alpha=0.25)
        ax.add_patch(polyPatch)

    else:
        for polygon in poly:
            poly_verts = pc.extreme(polygon)
            polyPatch = Polygon(poly_verts, facecolor=color, edgecolor=color, alpha=0.25)
            ax.add_patch(polyPatch)


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
