feedback_prompt = """
## Your generated path:
    path = {path}

## Feedback
    Start set: {start_feedback}
    Obstacle Issue: {obstacle_feedback}
    End set: {end_feedback}

## Instructions for Correction
    {instruct_start}{instruct_end}Obstacle Avoidance: Adjust the path to avoid intersecting obstacles. You may add waypoints at problematic waypoints to move around obstacles.
"""


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

    feedback = feedback_prompt.format(path=path, obstacle_feedback=obstacle_feedback, Theta=Theta, G=G, O=O,
                                      workspace=workspace, start_feedback=start_feedback, end_feedback=end_feedback,
                                      instruct_start=instruct_start, instruct_end=instruct_end)
    return feedback


init_prompt = """
Instructions
    Path Array: Output the path as an array of waypoints.
    Start and End: The path must begin at any point within the start set and end at any point within the goal set.
    Obstacle Avoidance: Verify that the path does not intersect any obstacles.
"""


def get_init_instruction(Theta, G, O):
    return init_prompt.format(Theta=Theta, G=G, O=O)
