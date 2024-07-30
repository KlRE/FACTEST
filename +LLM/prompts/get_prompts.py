from enum import Enum


class PromptStrategy(Enum):
    FULL_PATH = 'full_path'
    STEP_BY_STEP = 'step_by_step',

    @staticmethod
    def from_str(label):
        for prompt in PromptStrategy:
            if prompt.value == label:
                return prompt
        raise ValueError(f"Invalid label: {label}")


def get_feedback_prompt(prompt: PromptStrategy, path: str, obstacle_feedback: str, starts_in_init: bool,
                        ends_in_goal: bool, Theta, G, O, workspace):
    """
    Get the feedback prompt for the given environment
    :param prompt: Prompt strategy
    :param path: Path
    :param obstacle_feedback: Obstacle feedback
    :param starts_in_init: Starts in initial set
    :param ends_in_goal: Ends in goal set
    :param Theta: Initial set
    :param G: Goal set
    :param O: Obstacle set
    :param workspace: Workspace
    """
    if prompt == PromptStrategy.FULL_PATH:
        from prompts.entire_path import get_feedback
    elif prompt == PromptStrategy.STEP_BY_STEP:
        from prompts.step_by_step import get_feedback
    else:
        assert False, "Should not reach here"
    task_desc = get_task_description(Theta, G, O, workspace)
    feedback = get_feedback(path, obstacle_feedback, starts_in_init, ends_in_goal, Theta, G, O, workspace)
    path_format = get_path_output_format()

    return task_desc + feedback + path_format


def get_init_prompt(promptStrat: PromptStrategy, Theta, G, O, workspace):
    """
    Get the initial prompt for the task
    :return: Initial prompt
    """
    if promptStrat == PromptStrategy.FULL_PATH:
        from prompts.entire_path import get_init_instruction
    elif promptStrat == PromptStrategy.STEP_BY_STEP:
        from prompts.step_by_step import get_init_instruction
    else:
        assert False, "Should not reach here"

    task_desc = get_task_description(Theta, G, O, workspace)
    init_prompt = get_init_instruction(Theta, G, O)
    path_format = get_path_output_format()
    return task_desc + init_prompt + path_format


def get_task_description(Theta, G, O, workspace):
    """
    Get the task description for the given environment
    :param Theta: Initial set
    :param G: Goal set
    :param O: Obstacle set
    :param workspace: Workspace
    :return: Task description
    """
    if isinstance(O, list) and isinstance(O[0], tuple):
        o = "[\n"
        for i, obstacle in enumerate(O):
            o += f"\t\t\t{obstacle},   # Obstacle {i + 1}\n"
        o += "\t\t]"
        O = o

    task_description = f"""
# Motion Planning Task
## Goal: Come up with a path that starts in the start set, ends in the goal set, and avoids obstacles.

## Path Requirements
    Waypoints: The path should be represented as an array of waypoints and the path will be constructed by connecting these waypoints linearly.
    Non-Crossing: Ensure the path and especially the linearly connected segments do not cross any obstacles.
    Start and End: The path must start within the start set and end in the goal set.

## Provided Data
    Start Position (Rectangular Set): (xmin, xmax, ymin, ymax) = {Theta}
        Note: You can choose any point within this rectangle to start the path.
    Goal Position (Rectangular Set): (xmin, xmax, ymin, ymax) = {G}
        Note: You can choose any point within this rectangle to end the path.
    Obstacles (Rectangles):
        obstacles = {O}
"""
    return task_description


def get_path_output_format():
    """
    Get the output format for the task
    :return: Output format
    """
    return """
## Path Format:
    Provide the path as an array of float waypoints.
    
    Example Path Output:
    path = [
        (waypoint_x1, waypoint_y1),    
        (waypoint_x2, waypoint_y2),
        (waypoint_x3, waypoint_y3),
        ...,
        (waypoint_xn, waypoint_yn)       
    ]
    """


if __name__ == "__main__":
    # Test the prompt generation
    Theta = (0, 1, 0, 1)
    G = (4, 5, 4, 5)
    O = [(2, 3, 2, 3), (1, 2, 1, 2)]
    workspace = (0, 5, 0, 5)
    prompt = get_init_prompt(Theta, G, O, workspace)
    print(prompt)
    prompt = get_feedback_prompt(PromptStrategy.FULL_PATH, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                                 "No obstacle intersection", True, True, Theta, G, O, workspace)
    print(prompt)
    prompt = get_feedback_prompt(PromptStrategy.STEP_BY_STEP, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                                 "No obstacle intersection", True, True, Theta, G, O, workspace)
    print(prompt)
