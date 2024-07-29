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
        from prompts.entire_path_feedback_prompt import get_feedback
    elif prompt == PromptStrategy.STEP_BY_STEP:
        from prompts.step_by_step_feedback_prompt import get_feedback
    else:
        assert False, "Should not reach here"

    return get_feedback(path, obstacle_feedback, starts_in_init, ends_in_goal, Theta, G, O, workspace)


def get_task_description(Theta, G, O, workspace):
    """
    Get the task description for the given environment
    :param Theta: Initial set
    :param G: Goal set
    :param O: Obstacle set
    :param workspace: Workspace
    :return: Task description
    """
    task_description = f"""
    Motion Planning Task
    Goal: A path that starts in the start set, ends in the goal set, and avoids obstacles.

    Path Requirements
        Waypoints: The path should be represented as an array of waypoints and the path will be constructed by connecting these waypoints linearly.
        Non-Crossing: Ensure the path and especially the linearly connected segments do not cross any obstacles.
        Start and End: The path must start within the start set and end in the goal set.

    Provided Data
        Start Position (Rectangular Set): (xmin, xmax, ymin, ymax) = {Theta}
            Note: You can choose any point within this rectangle to start the path.
        Goal Position (Rectangular Set): (xmin, xmax, ymin, ymax) = {G}
            Note: You can choose any point within this rectangle to end the path.
        Obstacles (Rectangles):

        obstacles = {O}
    """
    return task_description
