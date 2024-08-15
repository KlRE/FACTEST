import argparse
import logging
import os
from datetime import datetime
from typing import Tuple, List
import polytope as pc

from convert_polytope_to_arrays import convert_env_polytope_to_arrays
from import_env import Env, import_environment
from prompts.Prompter import SinglePrompt, Model


def single_prompt(env: Tuple[pc.Polytope, pc.Polytope, List[pc.Polytope], pc.Polytope], env_name: str,
                  prompting_strat: SinglePrompt, model=Model.LLAMA3_8b, directory="./logs"):
    Theta, G, O, workspace = env
    new_Theta, new_G, new_O, new_workspace = convert_env_polytope_to_arrays(Theta, G, O, workspace)

    if prompting_strat == SinglePrompt.SOLVABLE_PROMPT:
        from prompts.solvable_prompt import SolvablePrompt
        Prompter = SolvablePrompt(model, new_Theta, new_G, new_O, new_workspace)
    else:
        raise ValueError(f"Invalid Single Prompt Strategy: {prompting_strat}")

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_directory = os.path.join(directory, env_name)
    os.makedirs(log_directory, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        handlers=[
            logging.FileHandler(f"{log_directory}/{current_time}.txt"),
            logging.StreamHandler()
        ],
        force=True
    )

    logging.info("Asking prompt")
    successful_prompt, answer = Prompter.prompt_init()

    if not successful_prompt:
        logging.warning("Failed to get initial prompt")
        raise ValueError("Failed to get initial prompt")

    return answer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a single prompt')
    parser.add_argument('--env', type=Env, choices=list(Env), required=True, help='The environment to prompt for')
    parser.add_argument('--prompting_strat', type=SinglePrompt, choices=list(SinglePrompt),
                        default=SinglePrompt.SOLVABLE_PROMPT, help='Prompt strategy to use')
    parser.add_argument('--model', type=Model, choices=list(Model), default=Model.LLAMA3_1_70b_Groq,
                        help='Model to use for prompting')
    parser.add_argument('--directory', type=str, default="./logs", help='The directory to save logs')

    args = parser.parse_args()
    env = import_environment(args.env)

    log_directory = os.path.join(args.directory, args.prompting_strat.value, args.model.value)

    single_prompt(env, args.env.value, args.prompting_strat, args.model, args.directory)
