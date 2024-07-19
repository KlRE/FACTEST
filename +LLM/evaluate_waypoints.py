import sys, os

currFile = os.path.abspath(__file__)
factestPath = currFile.replace('/+LLM/evaluate_waypoints.py', '/factest/synthesis')
sys.path.append(factestPath)

from factest.synthesis.factest_base_z3 import FACTEST_Z3
import matplotlib.pyplot as plt
from factest.plotting.plot_polytopes import plotPoly
from feedback_prompt import get_feedback
from datetime import datetime
from convert_polytope_to_arrays import convert_env_polytope_to_arrays

SAVE_PATH = '../images/llama3/1'

path = [(0.4, 3.6), (1.2, 3.8), (1.5, 3.9), (1.7, 3.85), (2.05, 3.15), (2.2, 2.95), (2.25, 2.75), (2.4, 2.6),
        (2.65, 2.5), (2.8, 2.9), (3.1, 3.0), (3.35, 3.7), (3.45, 3.85), (3.55, 3.95), (4.0, 4.2), (4.2, 4.6), (4.5, 4.8),
        (4.65, 4.9), (5.05, 5.15), (5.35, 5.45), (5.55, 5.65), (6.0, 4.95), (6.1, 4.85), (6.2, 4.75), (6.25, 5.0)]



def evaluate_waypoints(path, SAVE_PATH,Theta, G, O, workspace):
    FACTEST_prob = FACTEST_Z3(Theta, G, O, workspace=workspace, model=None, seg_max=0, part_max=0,
                              print_statements=True)
    xref = path

    obs_feedback = FACTEST_prob.evaluate_waypoints(xref)
    new_Theta, new_G, new_O, new_workspace = convert_env_polytope_to_arrays(Theta, G, O, workspace)
    feedback = get_feedback(str(xref), obs_feedback, new_Theta, new_G, new_O, new_workspace)

    xref_1 = [xval[0] for xval in xref]
    xref_2 = [xval[1] for xval in xref]

    increase_factor = 0.2
    x_min, x_max = -workspace.b[0], workspace.b[1]
    y_min, y_max = -workspace.b[2], workspace.b[3]

    x_range = x_max - x_min
    y_range = y_max - y_min

    new_x_min = x_min - increase_factor * x_range
    new_x_max = x_max + increase_factor * x_range
    new_y_min = y_min - increase_factor * y_range
    new_y_max = y_max + increase_factor * y_range

    fig, ax = plt.subplots()
    plotPoly(workspace, ax, 'yellow')
    plotPoly(Theta, ax, 'blue')
    plotPoly(G, ax, 'green')
    plotPoly(O, ax, 'red')
    ax.plot(xref_1, xref_2, marker='o')

    ax.set_xlim(new_x_min, new_x_max)
    ax.set_ylim(new_y_min, new_y_max)

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
    plt.savefig(f'{SAVE_PATH}/plot_{dt_string}.png')
    plt.show()

    # append path to file
    path_file = open(f'{SAVE_PATH}/path.txt', 'a')
    path_file.write(str(xref) + '\n')
    return feedback, obs_feedback


if __name__ == "__main__":
    feedback, obs_f = evaluate_waypoints(path, SAVE_PATH)
    print(feedback)
    print(obs_f)
