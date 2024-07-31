import os
from datetime import datetime

import ollama
import re
import logging
from evaluate_waypoints import evaluate_waypoints
from prompts.Prompter import Model, PromptStrategy

from convert_polytope_to_arrays import convert_env_polytope_to_arrays
from import_env import import_environment
from prompts.full_path_prompt import FullPathPrompt
from prompts.step_by_step_prompt import StepByStepPrompt


def path_from_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    # Use regex to find all arrays in the text
    array_pattern = re.compile(r'\[\(.*?\)]', re.DOTALL)
    arrays = array_pattern.findall(text)

    # Extract the last array
    if arrays:
        last_array_text = arrays[-1]

        # Extract all coordinate pairs from the last array
        coordinate_pattern = re.compile(r'\([+-]?(?:\d*\.)?\d+, [+-]?(?:\d*\.)?\d+\)')
        coordinates = coordinate_pattern.findall(last_array_text)

        # Convert the found coordinate pairs to a list of tuples
        last_array = [tuple(map(float, coord.strip('()').split(', '))) for coord in coordinates]

        return last_array
    else:
        logging.warning("No path found in file")


def iterative_prompt(env_str, prompting_strat: PromptStrategy, model=Model.LLAMA3_8b, num_iterations=20,
                     continue_path="",
                     directory="./logs"):
    """
    Iteratively prompts the user for feedback on a path until a successful path is found or the maximum number of iterations is reached.
    If continue_path is provided, the function will continue from the path in the file.
    :param env_str: The environment to prompt for
    :param prompting_strat: The prompting strategy to use
    :param num_iterations: The maximum number of iterations to run
    :param continue_path: The path to continue from if any or empty string
    :param model: The model to use for prompting
    :param directory: The directory to save logs
    """
    Theta, G, O, workspace = import_environment(env_str)
    new_Theta, new_G, new_O, new_workspace = convert_env_polytope_to_arrays(Theta, G, O, workspace)
    if prompting_strat == PromptStrategy.FULL_PATH:
        Prompter = FullPathPrompt(model, new_Theta, new_G, new_O, new_workspace)
    elif prompting_strat == PromptStrategy.STEP_BY_STEP:
        Prompter = StepByStepPrompt(model, new_Theta, new_G, new_O, new_workspace)
    else:
        raise ValueError(f"Invalid Prompt Strategy: {prompting_strat}")

    if continue_path == "":
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_directory = os.path.join(directory, model.value, env_str, current_time)
        os.makedirs(log_directory, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            handlers=[
                logging.FileHandler(f"{log_directory}/log.txt"),
                logging.StreamHandler()
            ],
            force=True
        )

        logging.info("Asking initial prompt")
        path = Prompter.prompt_init()

    else:
        log_directory = continue_path
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            handlers=[
                logging.FileHandler(f"{log_directory}/log.txt"),
                logging.StreamHandler()
            ],
            force=True
        )
        path = path_from_file(f"{log_directory}/path.txt")
        logging.info(f"Continuing from path: {path}")

    for i in range(num_iterations):
        logging.info(f"Iteration {i + 1}")
        obs_feedback, successful, starts_in_init, ends_in_goal = evaluate_waypoints(path, prompting_strat,
                                                                                    log_directory,
                                                                                    Theta, G, O, workspace,
                                                                                    iteration=i + 1)
        logging.info(f'Starts in init: {starts_in_init}, Ends in goal: {ends_in_goal}')

        if successful:
            logging.info("Path is successful")
            return True, i
        path = Prompter.prompt_feedback(path, obs_feedback, starts_in_init, ends_in_goal)
    return False, num_iterations


if __name__ == "__main__":
    string = """
     path = [
        (-6.0, -4.0),
        (+6.5, +3.75),
        (7.0, 3.0)
    ]

# Explanation:
- The path starts at the top-left corner of the start set to ensure it's within the specified rectangle.
- It then moves diagonally upwards and rightwards to avoid Obstacle 1.
- Finally, it moves horizontally to reach just outside Obstacle 5 and then vertically downwards to end inside the goal set."""
    # string = """
    # path = [
    #     (2.0, 1.5),
    #     (3.0, 2.5),      # Start just outside the obstacle on bottom edge
    #     (4.0, 4.0),     # Move right and up to avoid obstacle
    #     (6.0, 7.5),     # Continue right and up
    #     (8.0, 9.0),
    #     (8.5, 9.5)      # End in the goal set
    # ]
    # """

    iterative_prompt(env_str='maze_2d', prompting_strat=PromptStrategy.FULL_PATH, num_iterations=30,
                     model=Model.MISTRAL_NEMO_12b)
