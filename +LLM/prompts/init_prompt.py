prompt = """
Motion Planning Task
Task Description
    Find a feasible path for a 2D motion planning problem. The path should:
    Start Position: Begin within a specified rectangular start set.
    Goal Position: End within a specified rectangular goal set.
    Avoid Obstacles: The path must not intersect any obstacles.

Path Requirements
    Waypoints: The path should be represented as an array of waypoints.
    Linear Connection: Each pair of consecutive waypoints should be linearly connected forming a continuous path.
    Non-Crossing: Ensure the path and especially the linearly connected segments do not cross any obstacles.
    Start and End: The path must start within the start set and end in the goal set.

Provided Data
    Start Position (Rectangular Set): (xmin, xmax, ymin, ymax) = {Theta}
        Note: You can choose any point within this rectangle to start the path.
    Goal Position (Rectangular Set): (xmin, xmax, ymin, ymax) = {G}
        Note: You can choose any point within this rectangle to end the path.
    Obstacles (Rectangles):

    obstacles = {O}

Instructions

    Path Array: Output the path as an array of waypoints.
    Start and End: The path must begin at any point within the start set and end at any point within the goal set.
    Obstacle Avoidance: Verify that the path does not intersect any obstacles.

Example Path Output:

path = [
    (start_x1, start_y1),    # Chosen point from the start set
    (waypoint_x2, waypoint_y2),
    (waypoint_x3, waypoint_y3),
    ...,
    (goal_xn, goal_yn)       # Chosen point from the goal set
]

Note: Only output the array of waypoints representing the path. Do not include any code or algorithm details.
You are allowed to add comments for each waypoint describing the use case.

Your task is to generate this path while meeting all the criteria.
"""


def get_init_prompt(Theta, G, O):
    if isinstance(O, list) and isinstance(O[0], tuple):
        o = "[\n"
        for i, obstacle in enumerate(O):
            o += f"    {obstacle},   # Obstacle {i + 1}\n"
        o += "]"
        O = o
    return prompt.format(Theta=Theta, G=G, O=O)
