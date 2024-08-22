from typing import Union, List

import polytope as pc
import numpy as np


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
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import polytope as pc
    from scipy.spatial import ConvexHull
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Define a polytope (example)
    A = np.array([[-1, 0, 0],
                  [1, 0, 0],
                  [0, -1, 0],
                  [0, 1, 0],
                  [0, 0, -1],
                  [0, 0, 1]])
    b = np.array([[0], [1], [0], [1], [0], [1]])
    poly = pc.Polytope(A, b)

    # Plot the polytope
    plotPoly_3d(poly, ax, color='g')

    # Show plot
    plt.show()
