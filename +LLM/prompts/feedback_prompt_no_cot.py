from enum import Enum


class FeedbackPrompt(Enum):
    FULL_PATH = 'full_path'
    STEP_BY_STEP = 'step_by_step',


def get_feedback(path: str, obstacle_feedback: str, starts_in_init: bool, ends_in_goal: bool, Theta, G, O, workspace):
    if isinstance(O, list) and isinstance(O[0], tuple):
        o = "[\n"
        for i, obstacle in enumerate(O):
            o += f"    {obstacle},   # Obstacle {i + 1}\n"
        o += "]"
        O = o

    if starts_in_init:
        start_feedback = "Correct, The path starts in the correct start set."
        instruct_start = ""
    else:
        start_feedback = f"Incorrect, The path does not start in the correct start set {Theta}."
        instruct_start = "Start Position: Begin within the specified rectangular start set.\n"

    if ends_in_goal:
        end_feedback = "Correct, The path ends inside the goal set."
        instruct_end = ""
    else:
        end_feedback = f"Incorrect, The path does not end inside the goal set {G}."
        instruct_end = "Goal Position: End within the specified rectangular goal set.\n"
    feedback_prompt = f"""
    Path Validation and Feedback Task

    Generate a feasible path for a 2D motion planning problem that:

        Start Position: Begins within the start set.
        Goal Position: Ends within the goal set.
        Avoids Obstacles: The path is defined by waypoints which are linearly connected. Ensure that no segment between any two consecutive waypoints intersects with any obstacles.

    Approach: This will be done waypoint by waypoint. The last waypoint should be adjusted to avoid intersecting obstacles.

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
        Start set: {start_feedback}
        Obstacle Issue: {obstacle_feedback}
        End set: {end_feedback}

    Instructions for Correction:
        {instruct_start}Adjust Only the Last Waypoint: Modify the last waypoint (currently {path[-1]}) so that the final segment does not intersect any obstacles and ends within the goal set.
        Segment Integrity: Ensure that the entire segment from {path[-2]} to the new last waypoint does not intersect any obstacles. The path should be valid for all segments between waypoints.
        Avoid Direct Placement: Do not place the last waypoint directly into the goal set. Instead, adjust it step-by-step while ensuring it avoids obstacles and finally ends within the goal set.
        Do not add or remove any waypoints; only adjust the last waypoint.

    Output Format:
    Provide the path with the adjusted last waypoint only. Do not include any code or algorithm details. Only return the array of waypoints representing the updated path, formatted as follows:

    path = [(x1, y1), # Waypoint 1 starts in start set,
            (x2, y2), # Waypoint 2 changes direction to avoid obstacles,
            ...,
            (new_x, new_y)] # Adjusted last waypoint within the goal set and avoiding obstacles

    """
    return feedback_prompt
    # feedback = feedback_prompt.format(path=path, obstacle_feedback=obstacle_feedback, Theta=Theta, G=G, O=O,
    #                                   workspace=workspace, start_feedback=start_feedback, end_feedback=end_feedback,
    #                                   instruct_start=instruct_start, instruct_end=instruct_end)
    # return feedback
