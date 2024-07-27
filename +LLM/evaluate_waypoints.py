import sys, os

currFile = os.path.abspath(__file__)
factestPath = currFile.replace('/+LLM/evaluate_waypoints.py', '/factest/synthesis')
sys.path.append(factestPath)

from factest.synthesis.factest_base_z3 import FACTEST_Z3
import matplotlib.pyplot as plt
from factest.plotting.plot_polytopes import plotPoly
from prompts.feedback_prompt import get_feedback
from convert_polytope_to_arrays import convert_env_polytope_to_arrays

SAVE_PATH = '../+llm/images/llama3/1'

path = [(0.5, 3.5), (1.5, 3.5), (2.5, 3.5), (2.5, 2.5), (3.5, 2.5), (3.5, 3.5), (4.0, 3.8), (6.3, 4.7)]


# path = [(0.5, 3.5), (1.5, 3.5), (2.5, 3.5), (2.5, 2.5), (3.5, 2.5), (3.5, 3.0), (5.0, 5.0)] leads to incorrect collision detection todo

def evaluate_waypoints(path, SAVE_PATH, Theta, G, O, workspace, iteration, save=True):
    FACTEST_prob = FACTEST_Z3(Theta, G, O, workspace=workspace, model=None, seg_max=0, part_max=0,
                              print_statements=True)
    xref = path

    obs_feedback, successful, starts_in_init, ends_in_goal = FACTEST_prob.evaluate_waypoints(xref)

    if successful:
        feedback = obs_feedback
    else:
        new_Theta, new_G, new_O, new_workspace = convert_env_polytope_to_arrays(Theta, G, O, workspace)
        feedback = get_feedback(xref, obs_feedback, starts_in_init, ends_in_goal, new_Theta, new_G, new_O,
                                new_workspace)

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

    # append path to file

    return feedback, obs_feedback, successful, starts_in_init, ends_in_goal


if __name__ == "__main__":
    from import_env import import_environment

    Theta, G, O, workspace = import_environment('maze_2d')
    feedback, obs_f, s, st, e = evaluate_waypoints(path, SAVE_PATH, Theta, G, O, workspace, 0, save=False)
    print(feedback)
    print(obs_f)
