import sys, os

currFile = os.path.abspath(__file__)
factestPath = currFile.replace('/+LLM/evaluate_waypoints.py', '/factest/synthesis')
sys.path.append(factestPath)
factestPath2 = currFile.replace('/+LLM/evaluate_waypoints.py', '')
sys.path.append(factestPath2)
from factest.synthesis.factest_base_z3 import FACTEST_Z3
import matplotlib.pyplot as plt
from factest.plotting.plot_polytopes import plotPoly

SAVE_PATH = '../+llm/images/llama3/1'

new_path = [(2.0, 2.0), (5.0, 2.0), (7.5, 2.0), (8.0, 2.0), (8.6, 9.0)]


# path = [(0.5, 3.5), (1.5, 3.5), (2.5, 3.5), (2.5, 2.5), (3.5, 2.5), (3.5, 3.0), (5.0, 5.0)] leads to incorrect collision detection todo

def evaluate_waypoints(path, SAVE_PATH, Theta, G, O, workspace, iteration, save=True):
    FACTEST_prob = FACTEST_Z3(Theta, G, O, workspace=workspace, model=None, seg_max=0, part_max=0,
                              print_statements=True)
    xref = path

    intersections, successful, starts_in_init, ends_in_goal = FACTEST_prob.evaluate_waypoints(xref)

    xref_1 = [xval[0] for xval in xref]
    xref_2 = [xval[1] for xval in xref]

    fig, ax = plt.subplots()
    plotPoly(workspace, ax, 'yellow')
    plotPoly(Theta, ax, 'blue')
    plotPoly(G, ax, 'green')
    plotPoly(O, ax, 'red')
    ax.plot(xref_1, xref_2, marker='o')

    ax.autoscale_view()

    plt.title(f'Path evaluation for iteration {iteration}')

    if save:
        plt.savefig(f'{SAVE_PATH}/plot_{iteration}.png')
        path_file = open(f'{SAVE_PATH}/path.txt', 'a')
        path_file.write(str(xref) + '\n')

    plt.show()

    return intersections, successful, starts_in_init, ends_in_goal


if __name__ == "__main__":
    from import_env import import_environment

    Theta, G, O, workspace = import_environment('box')
    intersections, succ, si, eg = evaluate_waypoints(new_path, SAVE_PATH, Theta, G, O, workspace, 1)
