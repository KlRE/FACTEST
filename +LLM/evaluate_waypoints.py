import sys, os

currFile = os.path.abspath(__file__)
factestPath = currFile.replace('/+LLM/evaluate_waypoints.py', '/factest/synthesis')
sys.path.append(factestPath)
envs = currFile.replace('/+LLM/evaluate_waypoints.py', '/demo/envs')
sys.path.append(envs)

from factest.synthesis.factest_base_z3 import FACTEST_Z3
from demo.envs.maze_2d import Theta, G, O, workspace
import matplotlib.pyplot as plt
from factest.plotting.plot_polytopes import plotPoly
from feedback_prompt import get_feedback
from datetime import datetime

SAVE_PATH = '../images/llama3/1'

FACTEST_prob = FACTEST_Z3(Theta, G, O, workspace=workspace, model=None, seg_max=0, part_max=0, print_statements=True)


path = [(0.4, 3.6), (1.2, 3.8), (1.5, 3.9), (1.7, 3.85), (2.05, 3.15), (2.2, 2.95), (2.25, 2.75), (2.4, 2.6), (2.65, 2.5), (2.8, 2.9), (3.1,
3.0), (3.35, 3.7), (3.45, 3.85), (3.55, 3.95), (4.0, 4.2), (4.2, 4.6), (4.5, 4.8), (4.65, 4.9), (5.05, 5.15), (5.35, 5.45), (5.55, 5.65),
(6.0, 4.95), (6.1, 4.85), (6.2, 4.75), (6.25, 5.0)]

def evaluate_waypoints(path, SAVE_PATH):
    xref = path

    obs_feedback = FACTEST_prob.evaluate_waypoints(xref)
    feedback = get_feedback(str(xref), obs_feedback)

    xref_1 = [xval[0] for xval in xref]
    xref_2 = [xval[1] for xval in xref]

    fig, ax = plt.subplots()
    plotPoly(workspace, ax, 'yellow')
    plotPoly(Theta, ax, 'blue')
    plotPoly(G, ax, 'green')
    plotPoly(O, ax, 'red')
    ax.plot(xref_1, xref_2, marker='o')
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 6)


    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    plt.savefig(f'{SAVE_PATH}/plot_{dt_string}.png')
    plt.show()

    # append path to file
    path_file = open(f'{SAVE_PATH}/path.txt', 'a')
    path_file.write(str(xref) + '\n')
    return feedback

if __name__ == "__main__":
    evaluate_waypoints(path, SAVE_PATH)

