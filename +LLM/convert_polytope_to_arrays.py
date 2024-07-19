from polytope import Polytope
from typing import List

def convert_env_polytope_to_arrays(Theta: Polytope, G: Polytope, O: List[Polytope], workspace: Polytope):
    # assume rectangles are given as [-x_min, x_max, -y_min, -y_max] and parallel to coordinate axes
    Theta = (-Theta.b[0], Theta.b[1], -Theta.b[2], Theta.b[3])
    G = (-G.b[0], G.b[1], -G.b[2], G.b[3])
    O = [(-obs.b[0], obs.b[1], -obs.b[2], obs.b[3]) for obs in O]
    workspace = (-workspace.b[0], workspace.b[1], -workspace.b[2], workspace.b[3])
    return Theta, G, O, workspace
