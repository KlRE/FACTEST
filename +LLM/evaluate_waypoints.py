import sys, os

currFile = os.path.abspath(__file__)
factestPath = currFile.replace('/+LLM/evaluate_waypoints.py', '/factest/synthesis')
sys.path.append(factestPath)
envs = currFile.replace('/+LLM/evaluate_waypoints.py', '/demo/envs')
sys.path.append(envs)

from factest.synthesis.factest_base_z3 import FACTEST_Z3  # TODO: Need to update as MILP solver becomes available
from demo.envs.maze_2d import Theta, G, O, workspace
import matplotlib.pyplot as plt
from factest.plotting.plot_polytopes import plotPoly
from feedback_prompt import get_feedback

FACTEST_prob = FACTEST_Z3(Theta, G, O, workspace=workspace, model=None, seg_max=0, part_max=0, print_statements=True)

xref = [
    (0.5, 3.6),  # Start point in the start set
    (1.2, 3.4),
    (1.7, 3.8),  # Before the first issue
    (2.3, 4.2),  # Adjusted point to avoid (2.9, 3.0, 3.0, 4.0)
    (3.0, 4.5),  # Adjusted point to stay above the obstacle
    (3.7, 4.5),  # Adjusted point to stay consistent and avoid obstacles
    (4.5, 4.5),  # Adjusted point to stay consistent and avoid obstacles
    (5.2, 4.2),  # Adjusted point to avoid (4.9, 5.0, 2.0, 4.0)
    (5.8, 4.3),  # Adjusted point to avoid (5.9, 6.0, 2.0, 5.0)
    (6.25, 4.7)  # Adjusted end point to reach the goal set
]

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
plt.show()
