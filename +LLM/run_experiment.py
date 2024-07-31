import os

from import_env import Env
from iterative_prompt import iterative_prompt
from datetime import datetime
from prompts.get_prompts import PromptStrategy


def run_experiment(prompting_strat=PromptStrategy.FULL_PATH, num_iterations=30, description="", model='mistral-nemo'):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"./experiments/{current_time}"
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
    run_experiment(description="First experiment", model='mistral-nemo')
