import os
import sys
from datetime import datetime

import ollama
import re
import logging
from evaluate_waypoints import evaluate_waypoints
from init_prompt import get_init_prompt
from convert_polytope_to_arrays import convert_env_polytope_to_arrays

currFile = os.path.abspath(__file__)
envs = currFile.replace('/+LLM/iterative_prompt.py', '/demo/envs')
sys.path.append(envs)

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


def run(env_str, num_iterations=20, continue_path=""):
    if env_str == 'maze_2d':
        from demo.envs.maze_2d import Theta, G, O, workspace
    elif env_str == 'scots_hscc16':
        from demo.envs.scots_hscc16 import Theta, G, O, workspace
    elif env_str == 'box':
        from demo.envs.box import Theta, G, O, workspace
    elif env_str == 'easy':
        from demo.envs.easy import Theta, G, O, workspace
    elif env_str == 'hard':
        from demo.envs.hard import Theta, G, O, workspace
    else:
        raise ValueError(f'Environment {env_str} not found')

    if continue_path == "":
        directory = "./logs"
        curent_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_directory = os.path.join(directory, curent_time)
        os.makedirs(log_directory, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            handlers=[
                logging.FileHandler(f"{log_directory}/log.txt"),
                logging.StreamHandler()
            ]
        )
        new_Theta, new_G, new_O, new_workspace = convert_env_polytope_to_arrays(Theta, G, O, workspace)
        init_prompt = get_init_prompt(new_Theta, new_G, new_O)

        logging.info("Asking initial prompt")
        logging.info(init_prompt)
        init_response = ollama.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': init_prompt,
            },
        ])
        path = parse_response(init_response['message']['content'])

        logging.info(init_response['message']['content'])
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
            ]
        )
        path = path_from_file(f"{log_directory}/path.txt")
        logging.info(f"Continuing from path: {path}")


    for i in range(num_iterations):
        logging.info(f"Iteration {i + 1}")
        feedback, obs_feedback = evaluate_waypoints(path, log_directory, Theta, G, O, workspace)
        logging.info(f"Feedback: {obs_feedback}")
        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': feedback,
            },
        ])
        logging.info(response['message']['content'])
        while True:
            try:
                path = parse_response(response['message']['content'])
                break
            except:
                logging.warning("Failed to parse response")
                response = ollama.chat(model='llama3', messages=[
                    {
                        'role': 'user',
                        'content': feedback,
                    },
                ])
                logging.info(response['message']['content'])
            logging.info(f'Extracted path: {path}')



if __name__ == "__main__":
    run(env_str='box', num_iterations=20)
