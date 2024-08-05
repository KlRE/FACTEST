import argparse
import os

from import_env import Env
from iterative_prompt import iterative_prompt
from datetime import datetime

from prompts.Prompter import PromptStrategy, Model


def run_experiment(prompting_strat=PromptStrategy.FULL_PATH, num_iterations=30, description="",
                   model=Model.MISTRAL_NEMO_12b):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"./experiments/{prompting_strat.value}/{current_time}"
    os.makedirs(path, exist_ok=True)
    log_results_file = open(f"{path}/log_results.txt", "a")
    log_results_file.write(f"Experiment: {description}\n")
    log_results_file.write(f"Number of iterations: {num_iterations}\n")
    log_results_file.write(f"Model: {model}\n")
    log_results_file.write("-----------------------------\n")
    for env in Env:
        successful, num_iterations_ran = iterative_prompt(env.value, prompting_strat, model, num_iterations,
                                                          directory=path)
        log_results_file.write(f"{env.value}: {successful} after {num_iterations_ran} iterations\n")

    log_results_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run an iterative prompt experiment.')
    parser.add_argument('--prompting_strat', type=PromptStrategy, choices=list(PromptStrategy),
                        default=PromptStrategy.FULL_PATH, help='Prompt strategy to use.')
    parser.add_argument('--num_iterations', type=int, default=30, help='Number of iterations to run.')
    parser.add_argument('--description', type=str, default="", help='Description of the experiment.')
    parser.add_argument('--model', type=Model, choices=list(Model), default=Model.MISTRAL_NEMO_12b,
                        help='Model to use for the experiment.')

    args = parser.parse_args()

    run_experiment(prompting_strat=args.prompting_strat, num_iterations=args.num_iterations,
                   description=args.description, model=args.model)
