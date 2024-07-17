
feedback_prompt = """
Path Validation and Feedback Task
Task Overview

Generate a feasible path for a 2D motion planning problem that:

    Start Position: Begins within the start set.
    Goal Position: Ends within the goal set.
    Avoids Obstacles: Does not intersect any obstacles.

Provided Data
    The following data are rectangles in the form (xmin, xmax, ymin, ymax).

    Start Position (Rectangular Set): (0.3, 0.7, 3.3, 3.7)
    Goal Position (Rectangular Set): (6.25, 6.75, 4.5, 5.0)
    Obstacles (Rectangles):
    obstacles = [
        (1.0, 3.0, 0.9, 1.0),   # Obstacle 1
        (1.0, 5.0, 3.9, 4.0),   # Obstacle 2
        (0.9, 1.0, 2.0, 3.0),   # Obstacle 3
        (1.0, 2.0, 2.9, 3.0),   # Obstacle 4
        (1.9, 2.0, 2.0, 3.0),   # Obstacle 5
        (2.0, 4.0, 1.9, 2.0),   # Obstacle 6
        (3.9, 4.0, 1.0, 3.0),   # Obstacle 7
        (2.9, 3.0, 3.0, 4.0),   # Obstacle 8
        (4.0, 6.0, 0.9, 1.0),   # Obstacle 9
        (4.9, 5.0, 2.0, 4.0),   # Obstacle 10
        (5.0, 6.0, 1.9, 2.0),   # Obstacle 11
        (5.9, 6.0, 2.0, 5.0),   # Obstacle 12
        (0.0, 7.0, 0.0, 0.1),   # Obstacle 13
        (0.0, 0.1, 0.0, 3.0),   # Obstacle 14
        (0.0, 0.1, 4.0, 5.0),   # Obstacle 15
        (0.0, 6.0, 4.9, 5.0),   # Obstacle 16
        (6.9, 7.0, 0.0, 5.0),   # Obstacle 17
        (0.1, 0.0, 0.0, 5.0),   # Obstacle 18
        (7.0, 7.1, 0.0, 5.0),   # Obstacle 19
        (0.0, 7.0, 0.1, 0.0),   # Obstacle 20
        (0.0, 7.0, 5.0, 5.1)    # Obstacle 21
    ]

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

Please revise the path accordingly and provide the corrected array of waypoints."""

def get_feedback(path: str, obstacle_feedback: str):
    feedback = feedback_prompt.format(path=path, obstacle_feedback=obstacle_feedback)
    return feedback