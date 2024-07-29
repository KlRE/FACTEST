import os
from datetime import datetime

import ollama
import re
import logging
from evaluate_waypoints import evaluate_waypoints
from prompts.init_prompt import get_init_prompt
from prompts.get_prompts import PromptStrategy
from convert_polytope_to_arrays import convert_env_polytope_to_arrays
from import_env import import_environment

from enum import Enum


class Model(Enum):
    LLAMA3_8b = 'llama'
    MISTRAL_NEMO_12b = 'mistral-nemo'


def parse_response(response):
    # Extract the portion of the text containing the path array
    path_section = re.search(r'path\s*=\s*(\[.*?\])', response, re.DOTALL).group(1)

    # Extract all coordinate pairs from the path array
    coordinate_pattern = re.compile(r'\(\d*\.\d+, \d*\.\d+\)')
    coordinates = coordinate_pattern.findall(path_section)

    # Convert the found coordinate pairs to a list of tuples
    path = [tuple(map(float, coord.strip('()').split(', '))) for coord in coordinates]

    return path


def path_from_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    # Use regex to find all arrays in the text
    array_pattern = re.compile(r'\[\(.*?\)\]', re.DOTALL)
    arrays = array_pattern.findall(text)

    # Extract the last array
    if arrays:
        last_array_text = arrays[-1]

        # Extract all coordinate pairs from the last array
        coordinate_pattern = re.compile(r'\(\d*\.\d+, \d*\.\d+\)')
        coordinates = coordinate_pattern.findall(last_array_text)

        # Convert the found coordinate pairs to a list of tuples
        last_array = [tuple(map(float, coord.strip('()').split(', '))) for coord in coordinates]

        return last_array
    else:
        logging.warning("No path found in file")


def iterative_prompt(env_str, prompting_strat: PromptStrategy, num_iterations=20, continue_path="", model='llama3',
                     directory="./logs"):
    Theta, G, O, workspace = import_environment(env_str)

    if continue_path == "":
        curent_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_directory = os.path.join(directory, model, env_str, curent_time)
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
        new_Theta, new_G, new_O, new_workspace = convert_env_polytope_to_arrays(Theta, G, O, workspace)
        init_prompt = get_init_prompt(new_Theta, new_G, new_O)

        logging.info("Asking initial prompt")
        logging.info(init_prompt)
        init_response = ollama.generate(model=model, prompt=init_prompt)
        logging.info(init_response['response'])
        while True:
            try:
                path = parse_response(init_response['response'])
                break
            except:
                logging.warning("Failed to parse response")
                init_response = ollama.generate(model=model, prompt=init_prompt)
                logging.info(init_response['response'])
        logging.info(f'Extracted path: {path}')

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
        feedback, obs_feedback, successful, starts_in_init, ends_in_goal = evaluate_waypoints(path, prompting_strat,
                                                                                              log_directory,
                                                                                              Theta, G, O, workspace,
                                                                                              iteration=i)
        logging.info(f"Feedback: {feedback}")
        logging.info(f'Starts in init: {starts_in_init}, Ends in goal: {ends_in_goal}')
        # response = ollama.chat(model='llama3', messages=[
        #     {
        #         'role': 'user',
        #         'content': feedback,
        #     },
        # ])
        response = ollama.generate(model=model, prompt=feedback)
        logging.info(response['response'])
        if successful:
            logging.info("Path is successful")
            return True, num_iterations
        while True:
            try:
                path = parse_response(response['response'])
                logging.info(f'Extracted path: {path}')
                break
            except:
                logging.warning("Failed to parse response")
                response = ollama.generate(model=model, prompt=feedback)
                logging.info(response['response'])

    return False, num_iterations


if __name__ == "__main__":
    # todo add argparse
    iterative_prompt(env_str='maze_2d', num_iterations=30, model='mistral-nemo')
