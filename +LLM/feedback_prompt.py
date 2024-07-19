from polytope import Polytope

feedback_prompt = """
Path Validation and Feedback Task
Task Overview

Generate a feasible path for a 2D motion planning problem that:

    Start Position: Begins within the start set.
    Goal Position: Ends within the goal set.
    Avoids Obstacles: Does not intersect any obstacles.

Provided Data
    The following data are rectangles in the form (xmin, xmax, ymin, ymax).

    Start Position (Rectangular Set): {Theta}
    Goal Position (Rectangular Set): {G}
    Obstacles (Rectangles):
    obstacles = {O}

Path Received
Your generated path:
path = {path}

Feedback
    Start set: Correct, The path starts in the correct start set.
    Obstacle Issue: {obstacle_feedback}
    End set: Correct, The path ends inside the goal set.

Instructions for Correction
    Obstacle Avoidance: Adjust the path to avoid intersecting obstacles. You may add waypoints at problematic waypoints to move around obstacles.
    Note: Only output the array of waypoints representing the path. Do not include any code or algorithm details. You can add comments for each waypoint to explain the path.
    However only return one array in this form:
    path = [(a,b), #bla bla
            (c,d), #more explanation
            ....
            ]
            
Do not provide any other text or explanation except for the path array.
Please revise the path accordingly and provide the corrected array of waypoints."""

def get_feedback(path: str, obstacle_feedback: str, Theta, G, O, workspace):
    if isinstance(O, list) and isinstance(O[0], tuple):
        o = "[\n"
        for i, obstacle in enumerate(O):
            o += f"    {obstacle},   # Obstacle {i + 1}\n"
        o += "]"
        O = o

    feedback = feedback_prompt.format(path=path, obstacle_feedback=obstacle_feedback, Theta=Theta, G=G, O=O, workspace=workspace)
    return feedback