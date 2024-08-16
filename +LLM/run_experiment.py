import argparse
import logging
import os
import time

from import_env import Env, import_environment
from iterative_prompt import iterative_prompt
from datetime import datetime
from rich.progress import Progress, TimeElapsedColumn

from prompts.Prompter import PromptStrategy, Model


def log_success_rate(successfuls, num_iterations_needed, path_lens, log_results_file):
    # filter out invalid runs (num_iterations_needed == -1)
    successfuls = [successfuls[i] for i in range(len(successfuls)) if num_iterations_needed[i] != -1]
    path_lens = [path_lens[i] for i in range(len(path_lens)) if num_iterations_needed[i] != -1]
    num_iterations_needed = [num_iterations_needed[i] for i in range(len(num_iterations_needed)) if
                             num_iterations_needed[i] != -1]
    num_runs = len(successfuls)

    success_rate = sum(successfuls) / num_runs
    avg_num_iterations = sum(num_iterations_needed) / num_runs
    avg_path_len = sum(path_lens) / num_runs

    if sum(successfuls) > 0:
        avg_successful_iterations = sum(
            [num_iterations_needed[i] for i in range(num_runs) if successfuls[i]]) / sum(successfuls)
        avg_successful_path_len = sum([path_lens[i] for i in range(num_runs) if successfuls[i]]) / sum(successfuls)
    else:
        avg_successful_iterations = -1
        avg_successful_path_len = -1

    log_results_file.write(f"Success Rate: {success_rate * 100:.2f}%\n")
    log_results_file.write(f"Average Number of Iterations: {avg_num_iterations:.2f}\n")
    log_results_file.write(
        f"Average Number of Iterations for Successful Runs: {avg_successful_iterations:.2f}\n")
    log_results_file.write(f"Average Path Length: {avg_path_len:.2f}\n")
    log_results_file.write(f"Average Path Length for Successful Runs: {avg_successful_path_len:.2f}\n")


def run_experiment(prompting_strat=PromptStrategy.FULL_PATH, num_iterations=30, description="",
                   model=Model.MISTRAL_NEMO_12b, use_history=False, specific_envs=[], evaluations_per_env=1,
                   use_random_env=False, random_env_obstacles=[3], num_random_envs=10):
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

    with Progress(*Progress.get_default_columns(), TimeElapsedColumn(), refresh_per_second=1,
                  speed_estimate_period=600) as pb:
        if use_random_env:
            t1 = pb.add_task('Prompting Env', total=num_random_envs)
            t2 = pb.add_task('Run experiment', total=len(random_env_obstacles))

            for num_obs, obs in enumerate(random_env_obstacles):
                log_results_file.write(f"Random environment with {obs} obstacles\n")
                successfuls = []
                num_iterations_needed = []
                path_lens = []
                pb.reset(t1)

                for i in range(num_random_envs):
                    env_polytopes = Env.generate_env(obs)
                    successful, num_iterations_ran, path_len = iterative_prompt(env_polytopes, f"Env {i}",
                                                                                prompting_strat,
                                                                                model, num_iterations, use_history,
                                                                                directory=f"{path}/{obs}_Obs")
                    log_results_file.write(
                        f"Random Env {i}: {successful} after {num_iterations_ran} iterations with path length {path_len}\n")
                    successfuls.append(successful)
                    num_iterations_needed.append(num_iterations_ran)
                    path_lens.append(path_len)

                    pb.update(task_id=t1, completed=i + 1)

                log_success_rate(successfuls, num_iterations_needed, path_lens, log_results_file)
                log_results_file.write("-----------------------------\n")

                pb.update(task_id=t2, completed=num_obs + 1)

            elapsed = pb.tasks[1].elapsed
            s_time = time.strftime("%Hh:%Mm:%Ss", time.gmtime(elapsed))
            log_results_file.write(f"Total time: {s_time}\n")

        else:
            envs = Env if specific_envs == [] else specific_envs
            t1 = pb.add_task('Prompting Env', total=evaluations_per_env)
            t2 = pb.add_task('Run experiment', total=len(envs))

            for num_env, env in enumerate(envs):
                successfuls = []
                num_iterations_needed = []
                path_lens = []
                pb.reset(t1)

                for i in range(evaluations_per_env):
                    env_polytopes = import_environment(env)
                    successful, num_iterations_ran, path_len = iterative_prompt(env_polytopes, env.value,
                                                                                prompting_strat, model,
                                                                                num_iterations, use_history,
                                                                                directory=path)
                    log_results_file.write(
                        f"{env.value} {i + 1}: {successful} after {num_iterations_ran} iterations with path length {path_len}\n")
                    successfuls.append(successful)
                    num_iterations_needed.append(num_iterations_ran)
                    path_lens.append(path_len)

                    pb.update(task_id=t1, completed=i + 1)

                log_success_rate(successfuls, num_iterations_needed, path_lens, log_results_file)
                log_results_file.write("-----------------------------\n")

                pb.update(task_id=t2, completed=num_env + 1)

            elapsed = pb.tasks[1].elapsed
            s_time = time.strftime("%Hh:%Mm:%Ss", time.gmtime(elapsed))
            log_results_file.write(f"Total time: {s_time}\n")

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
    parser.add_argument('--evaluations_per_env', type=int, default=1,
                        help="Number of evaluations per environment. Does not apply to random environments.")
    parser.add_argument('--use_random_env', action='store_true', help='Use a random environment for the experiment.')
    parser.add_argument('--random_env_obstacles', type=int, nargs="+", default=[3],
                        help='Number of obstacles in the random environment.')
    parser.add_argument('--num_random_envs', type=int, default=10, help='Number of random environments to use.')

    args = parser.parse_args()

    run_experiment(prompting_strat=args.prompting_strat, num_iterations=args.num_iterations,
                   use_history=args.use_history, specific_envs=args.specific_envs,
                   evaluations_per_env=args.evaluations_per_env,
                   description=args.description, model=args.model, use_random_env=args.use_random_env,
                   random_env_obstacles=args.random_env_obstacles, num_random_envs=args.num_random_envs)
