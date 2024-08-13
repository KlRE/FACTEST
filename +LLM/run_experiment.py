import argparse
import logging
import os

from import_env import Env, import_environment
from iterative_prompt import iterative_prompt
from datetime import datetime

from prompts.Prompter import PromptStrategy, Model


def run_experiment(prompting_strat=PromptStrategy.FULL_PATH, num_iterations=30, description="",
                   model=Model.MISTRAL_NEMO_12b, use_history=False, specific_envs=[], use_random_env=False,
                   random_env_obstacles=[3], num_random_envs=10):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if use_random_env:
        path = f"./experiments/random_env/{prompting_strat.value}/{current_time}"
    else:
        path = f"./experiments/{prompting_strat.value}/{current_time}"

    os.makedirs(path, exist_ok=True)
    log_results_file = open(f"{path}/log_results.txt", "a")
    log_results_file.write(f"Experiment: {description}\n")
    log_results_file.write(f"Number of iterations: {num_iterations}\n")
    log_results_file.write(f"Model: {model}\n")
    log_results_file.write(f"Prompting strategy: {prompting_strat}\n")
    log_results_file.write(f"Use history: {use_history}\n")
    log_results_file.write("-----------------------------\n")
    if use_random_env:
        for obs in random_env_obstacles:
            log_results_file.write(f"Random environment with {obs} obstacles\n")
            successfuls = []
            num_iterations_needed = []
            for i in range(num_random_envs):
                env_polytopes = Env.generate_env(obs)
                successful, num_iterations_ran = iterative_prompt(env_polytopes, f"Env {i}", prompting_strat,
                                                                  model, num_iterations, use_history,
                                                                  directory=f"{path}/{obs}_Obs")
                log_results_file.write(f"Random Env {i}: {successful} after {num_iterations_ran} iterations\n")
                successfuls.append(successful)
                num_iterations_needed.append(num_iterations_ran)

            success_rate = sum(successfuls) / num_random_envs
            avg_num_iterations = sum(num_iterations_needed) / num_random_envs
            if sum(successfuls) > 0:
                avg_successful_iterations = sum(
                    [num_iterations_needed[i] for i in range(num_random_envs) if successfuls[i]]) / sum(successfuls)
            else:
                avg_successful_iterations = -1

            log_results_file.write(f"Success Rate: {success_rate * 100:.2f}%\n")
            log_results_file.write(f"Average Number of Iterations: {avg_num_iterations:.2f}\n")
            log_results_file.write(
                f"Average Number of Iterations for Successful Runs: {avg_successful_iterations:.2f}\n")
            log_results_file.write("-----------------------------\n")

    else:
        envs = Env if specific_envs == [] else specific_envs
        for env in envs:
            env_polytopes = import_environment(env)
            successful, num_iterations_ran = iterative_prompt(env_polytopes, env.value, prompting_strat, model,
                                                              num_iterations, use_history,
                                                              directory=path)
            log_results_file.write(f"{env.value}: {successful} after {num_iterations_ran} iterations\n")

    log_results_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run an iterative prompt experiment.')
    parser.add_argument('--prompting_strat', type=PromptStrategy, choices=list(PromptStrategy),
                        default=PromptStrategy.FULL_PATH, help='Prompt strategy to use.')
    parser.add_argument('--num_iterations', type=int, default=30, help='Number of iterations to run.')
    parser.add_argument('--use_history', action='store_true', help='Use history in the prompter.')
    parser.add_argument('--description', type=str, default="", help='Description of the experiment.')
    parser.add_argument('--model', type=Model, choices=list(Model), default=Model.MISTRAL_NEMO_12b,
                        help='Model to use for the experiment.')
    parser.add_argument('--specific_envs', type=Env, nargs="+", choices=list(Env), default=[])
    parser.add_argument('--use_random_env', action='store_true', help='Use a random environment for the experiment.')
    parser.add_argument('--random_env_obstacles', type=int, nargs="+", default=[3],
                        help='Number of obstacles in the random environment.')
    parser.add_argument('--num_random_envs', type=int, default=10, help='Number of random environments to use.')

    args = parser.parse_args()

    run_experiment(prompting_strat=args.prompting_strat, num_iterations=args.num_iterations,
                   use_history=args.use_history, specific_envs=args.specific_envs,
                   description=args.description, model=args.model, use_random_env=args.use_random_env,
                   random_env_obstacles=args.random_env_obstacles, num_random_envs=args.num_random_envs)
