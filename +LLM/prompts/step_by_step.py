def get_feedback(path: str, obstacle_feedback: str, starts_in_init: bool, ends_in_goal: bool, Theta, G, O, workspace):
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
## Your generated path:
    path = {path}

## Feedback
    Start set: {start_feedback}
    Obstacle Issue: {obstacle_feedback}
    End set: {end_feedback}

## Instructions for Correction:
    {instruct_start}Adjust Only the Last Waypoint: Modify the last waypoint (currently {path[-1]}) so that the final segment does not intersect any obstacles and ends within the goal set.
    Segment Integrity: Ensure that the entire segment from {path[-2]} to the new last waypoint does not intersect any obstacles. The path should be valid for all segments between waypoints.
    Avoid Direct Placement: Do not place the last waypoint directly into the goal set. Instead, adjust it step-by-step while ensuring it avoids obstacles and finally ends within the goal set.
    Do not add or remove any waypoints; only adjust the last waypoint.
    """
    return feedback_prompt
    # feedback = feedback_prompt.format(path=path, obstacle_feedback=obstacle_feedback, Theta=Theta, G=G, O=O,
    #                                   workspace=workspace, start_feedback=start_feedback, end_feedback=end_feedback,
    #                                   instruct_start=instruct_start, instruct_end=instruct_end)
    # return feedback


init_prompt = """
Instructions
    Path Array: Output the first waypoint of the path.
    Start: The path must begin at any point within the start set.
    Obstacle Avoidance: Verify that the point does not intersect wiht any obstacles.
"""


def get_init_instruction(Theta, G, O):
    return init_prompt.format(Theta=Theta, G=G, O=O)
