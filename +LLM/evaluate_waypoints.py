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

path = [(0.4, 3.6), (1.2, 3.8), (1.5, 3.7), (1.9, 3.4), (2.0, 3.2), (2.1, 2.9), (2.2, 2.8), (2.6, 3.1), (2.8, 3.2), (3.2, 3.5), (3.4, 3.6),
(3.7, 3.5), (3.8, 3.9), (4.0, 4.1), (4.2, 4.0), (4.6, 4.5), (4.7, 4.5), (4.8, 4.7), (5.0, 4.8), (5.2, 5.0), (5.5, 4.8), (5.6, 4.5), (5.9,
4.7), (6.0, 4.7), (6.25, 4.8)]

xref = path

obs_feedback = FACTEST_prob.evaluate_waypoints(xref)
feedback = get_feedback(str(xref), obs_feedback)
print(feedback)

xref_1 = [xval[0] for xval in xref]
xref_2 = [xval[1] for xval in xref]

fig, ax = plt.subplots()
plotPoly(workspace, ax, 'yellow')
plotPoly(Theta, ax, 'blue')
plotPoly(G, ax, 'green')
plotPoly(O, ax, 'red')
ax.plot(xref_1, xref_2, marker='o')
ax.set_xlim(0, 8)
ax.set_ylim(0, 8)


now = datetime.now()
dt_string = now.strftime("%d%m%Y%H%M%S")
plt.savefig(f'{SAVE_PATH}/plot_{dt_string}.png')
plt.show()

# append path to file
path_file = open(f'{SAVE_PATH}/path.txt', 'a')
path_file.write(str(xref) + '\n')

