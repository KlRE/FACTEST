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

FACTEST_prob = FACTEST_Z3(Theta, G, O, workspace=workspace, model=None, seg_max=0, part_max=0, print_statements=True)

path = [
    (0.5, 3.5),     # Start point within the start position
    (0.5, 1.5),     # Move down to avoid obstacles
    (2.0, 1.5),     # Move right to avoid obstacle 6
    (2.0, 2.5),     # Move up to avoid obstacle 6
    (3.5, 2.5),     # Move right to avoid obstacle 7
    (3.5, 3.5),     # Move up to avoid obstacle 7
    (4.5, 3.5),     # Move right to avoid obstacle 10
    (4.5, 4.1),     # Move up to avoid obstacle 10
    (5.2, 4.1),     # Move right to avoid obstacle 10
    (5.2, 4.5),     # Move up to avoid obstacle 12
    (6.3, 4.5),     # Move right to avoid obstacle 12
    (6.5, 4.75)     # End point within the goal position
]






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
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)


save_path = '../images/3'

now = datetime.now()
dt_string = now.strftime("%d%m%Y%H%M%S")
plt.savefig(f'{save_path}/plot_{dt_string}.png')
plt.show()

# append path to file
path_file = open(f'{save_path}/path.txt', 'a')
path_file.write(str(xref) + '\n')

