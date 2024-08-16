import argparse
import os
from datetime import datetime

from rich.progress import Progress, TimeElapsedColumn

from import_env import Env, UnsolvableEnv, import_environment
from prompts.Prompter import Model, SinglePrompt
from single_prompt import single_prompt


def identify_solvable_experiment(description="", model=Model.MISTRAL_NEMO_12b, specific_envs=[], evaluations_per_env=1):
    prompting_strat = SinglePrompt.SOLVABLE_PROMPT
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"./experiments/{prompting_strat.value}/{current_time}"

    os.makedirs(path, exist_ok=True)
    log_results_file = open(f"{path}/log_results.txt", "a")
    log_results_file.write(f"Experiment: {description}\n")
    log_results_file.write(f"Model: {model}\n")
    log_results_file.write(f"Prompting strategy: {prompting_strat}\n")
    log_results_file.write("-----------------------------\n")

    with Progress(*Progress.get_default_columns(), TimeElapsedColumn(), refresh_per_second=1,
                  speed_estimate_period=600) as pb:

        if specific_envs == []:
            solvable_envs = Env
            unsolvable_envs = UnsolvableEnv
        else:
            solvable_envs = []
            unsolvable_envs = []
            for env in specific_envs:
                if env in Env:
                    solvable_envs.append(env)
                else:
                    unsolvable_envs.append(env)

        t1 = pb.add_task('Prompting Env', total=evaluations_per_env)
        t2 = pb.add_task('Run experiment', total=len(solvable_envs) + len(unsolvable_envs))

        percentage_class_correct = []
        percentage_class_incorrect = []

        for num_env, env in enumerate(solvable_envs):
            pb.reset(t1)
            successfuls = []

            for i in range(evaluations_per_env):
                env_polytopes = import_environment(env)
                try:
                    solvable = single_prompt(env_polytopes, env.value, prompting_strat, model, directory=path)
                    successful = solvable
                    log_results_file.write(f"{env.value} {i + 1}: {'Correct' if successful else 'Incorrect'} \n")
                    successfuls.append(successful)

                except Exception as e:
                    log_results_file.write(f"{env.value} {i + 1}: {e} \n")
                    continue

                pb.update(task_id=t1, completed=i + 1)

            num_runs = len(successfuls)
            success_rate = sum(successfuls) / num_runs
            percentage_class_correct.append(success_rate)
            log_results_file.write(f"Success Rate: {success_rate * 100:.2f}%\n")
            log_results_file.write("-----------------------------\n")

            pb.update(task_id=t2, completed=num_env + 1)

        for num_env, env in enumerate(unsolvable_envs):
            successfuls = []
            pb.reset(t1)
            for i in range(evaluations_per_env):
                env_polytopes = import_environment(env)
                try:
                    solvable = single_prompt(env_polytopes, env.value, prompting_strat, model, directory=path)
                    successful = not solvable
                    log_results_file.write(f"{env.value} {i + 1}: {'Correct' if successful else 'Incorrect'} \n")
                    successfuls.append(successful)

                except Exception as e:
                    log_results_file.write(f" Unsolvable{env.value} {i + 1}: {e} \n")
                    continue

                pb.update(task_id=t1, completed=i + 1, refresh=True)

            num_runs = len(successfuls)
            success_rate = sum(successfuls) / num_runs
            percentage_class_incorrect.append(success_rate)
            log_results_file.write(f"Success Rate: {success_rate * 100:.2f}%\n")
            log_results_file.write("-----------------------------\n")

            pb.update(task_id=t2, completed=len(solvable_envs) + num_env + 1, refresh=True)

        log_results_file.write(
            f"Average Percentage of correct classifications: {sum(percentage_class_correct) / len(percentage_class_correct) * 100:.2f}%\n")
        log_results_file.write(
            f"Average Percentage of incorrect classifications: {sum(percentage_class_incorrect) / len(percentage_class_incorrect) * 100:.2f}%\n")

    log_results_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Identify solvable experiments')
    parser.add_argument('--description', type=str, default="", help='Description of the experiment')
    parser.add_argument('--model', type=Model, choices=list(Model), default=Model.LLAMA3_1_70b_Groq,
                        help='Model to use for prompting')
    parser.add_argument('--specific_envs', type=Env, choices=list(Env), nargs='+', default=[],
                        help='Specific environments to run')
    parser.add_argument('--evaluations_per_env', type=int, default=10, help='Number of evaluations per environment')

    args = parser.parse_args()

    identify_solvable_experiment(description=args.description, model=args.model, specific_envs=args.specific_envs,
                                 evaluations_per_env=args.evaluations_per_env)
