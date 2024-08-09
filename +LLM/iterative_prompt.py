import argparse
import os
from datetime import datetime

import ollama
import re
import logging
from evaluate_waypoints import evaluate_waypoints
from prompts.Prompter import Model, PromptStrategy

from convert_polytope_to_arrays import convert_env_polytope_to_arrays
from import_env import import_environment, Env
from prompts.full_path_break_points import FullPathBreakPointsPrompt
from prompts.full_path_prompt import FullPathPrompt
from prompts.full_path_valid_path import FullPathValidPathPrompt
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


def iterative_prompt(env: Env, prompting_strat: PromptStrategy, model=Model.LLAMA3_8b, num_iterations=20,
                     use_history=False,
                     continue_path="",
                     directory="./logs"):
    """
    Iteratively prompts the user for feedback on a path until a successful path is found or the maximum number of iterations is reached.
    If continue_path is provided, the function will continue from the path in the file.
    :param env: The environment to prompt for
    :param prompting_strat: The prompting strategy to use
    :param num_iterations: The maximum number of iterations to run
    :param use_history: Use history for prompting
    :param continue_path: The path to continue from if any or empty string
    :param model: The model to use for prompting
    :param directory: The directory to save logs
    """
    Theta, G, O, workspace = import_environment(env)
    new_Theta, new_G, new_O, new_workspace = convert_env_polytope_to_arrays(Theta, G, O, workspace)
    env_str = env.value
    if prompting_strat == PromptStrategy.FULL_PATH:
        Prompter = FullPathPrompt(model, new_Theta, new_G, new_O, new_workspace, use_history)
    elif prompting_strat == PromptStrategy.STEP_BY_STEP:
        Prompter = StepByStepPrompt(model, new_Theta, new_G, new_O, new_workspace, use_history)
    elif prompting_strat == PromptStrategy.FULL_PATH_BREAK_POINTS:
        Prompter = FullPathBreakPointsPrompt(model, new_Theta, new_G, new_O, new_workspace, use_history, 2)
    elif prompting_strat == PromptStrategy.FULL_PATH_VALID_SUBPATH:
        Prompter = FullPathValidPathPrompt(model, new_Theta, new_G, new_O, new_workspace, use_history)
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
        successful_prompt, path = Prompter.prompt_init()

        if not successful_prompt:
            logging.warning("Failed to get initial prompt")
            return False, -1

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
    path = [(0.5, 3.5), (2, 3.5)]
    for i in range(num_iterations):
        logging.info(f"Iteration {i + 1}")
        intersections, successful, starts_in_init, ends_in_goal = evaluate_waypoints(path, log_directory,
                                                                                     Theta, G, O, workspace,
                                                                                     iteration=i + 1)
        logging.info(f'Starts in init: {starts_in_init}, Ends in goal: {ends_in_goal}')

        if successful:
            logging.info("Path is successful")
            return True, i
        successful_prompt, path = Prompter.prompt_feedback(path, intersections, starts_in_init, ends_in_goal)
        if not successful_prompt:
            logging.warning("Failed to get feedback prompt")
            return False, i

    return False, num_iterations


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run an iterative prompt experiment.')
    parser.add_argument('--env', type=Env, choices=list(Env), required=True, help='The environment to prompt for')
    parser.add_argument('--prompting_strat', type=PromptStrategy, choices=list(PromptStrategy),
                        default=PromptStrategy.FULL_PATH, help='Prompt strategy to use')
    parser.add_argument('--model', type=Model, choices=list(Model), default=Model.LLAMA3_8b,
                        help='Model to use for prompting')
    parser.add_argument('--num_iterations', type=int, default=20, help='Number of iterations to run')
    parser.add_argument('--use_history', type=bool, help='Use history for prompting')
    parser.add_argument('--continue_path', type=str, default="",
                        help='The path to continue from if any or empty string')
    parser.add_argument('--directory', type=str, default="./logs", help='The directory to save logs')

    args = parser.parse_args()

    iterative_prompt(env=args.env, prompting_strat=args.prompting_strat, model=args.model,
                     num_iterations=args.num_iterations, use_history=args.use_history, continue_path=args.continue_path,
                     directory=args.directory)
