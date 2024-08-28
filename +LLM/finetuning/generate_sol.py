import json
import logging
import time

import numpy as np
from matplotlib import pyplot as plt
from rich.progress import track

from convert_polytope_to_arrays import convert_env_polytope_to_arrays
from envs.plot_env import plotPoly, plot_env
from factest.factest_base_z3 import FACTEST_Z3
from import_env import Env
from prompts.Prompter import Prompter, Model
from prompts.full_path_prompt import FullPathPrompt


def generate_prob_w_sol(num_obstacles=5):
    while True:
        try:
            Theta, G, O, workspace = Env.generate_env(num_obstacles=num_obstacles)
            FACTEST_prob = FACTEST_Z3(Theta, G, O, workspace=workspace)
            result_dict = FACTEST_prob.run()
            result_keys = list(result_dict.keys())
            xref = result_dict[result_keys[0]]['xref']
            xref = np.round(xref, 2).tolist()

            # plot_env(f"Random Environment {num_obstacles} Obstacles", workspace, G, Theta, O, save=True,
            #          dir=f'./syn_data/',
            #          path=xref)
            del FACTEST_prob  # otherwise leaks memory
            return Theta, G, O, workspace, xref

        except Exception as e:
            print(e)
            continue


def generate_synth_ds(samples=10, model: Model = Model.GEMINI_1_5_PRO_VERTEX, file_dir=".", prompt_model=False):
    """
    Generate synthetic dataset for the factest problem
    """
    np.random.seed(42)
    ds_file_path = f"{file_dir}/synthetic_ds2{'_pathonly' if not prompt_model else ''}.json"
    ds_file_backup_path = f"{file_dir}/synthetic_ds2{'_pathonly' if not prompt_model else ''}.txt"
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
    )

    with open(ds_file_backup_path, "w") as ds_file:
        interactions = {
            "conversations": []
        }
        ds_file.write("""{
    "conversations": [\n""")
        for i in track(range(samples)):
            Theta, G, O, workspace, xref = generate_prob_w_sol((i % 10) + 1)
            new_Theta, new_G, new_O, new_workspace = convert_env_polytope_to_arrays(Theta, G, O, workspace)
            prompter = FullPathPrompt(model, new_Theta, new_G, new_O, new_workspace)
            init_prompt = prompter.get_init_prompt()

            if prompt_model:
                prompt = f"""
    You are given the following environment with the following prompt:
    {init_prompt}
    --------------------------------------------------------------------------
    This was the initial prompt for the problem. You are now given the correct solution to this Problem. The solution is the following path:
    {xref}
    --------------------------------------------------------------------------
    Please write a detailed description, why the solution is correct. Analyze the path, the environment and the spatial relationships between them.
    Write this as an explanation of the solution. Refer to the solution as one that you found yourself.
    """
                successful, response = prompter.prompt_model(prompt, parse_response=False)

                if successful:
                    path_str = f"""Therefore, the correct path would be:   
    ```
    new_path = {xref}
    ```"""
                    full_response = response + path_str
                    data_entry = {
                        "input": init_prompt,
                        "output": full_response
                    }
                    interactions["conversations"].append(data_entry)
                    ds_file.write(
                        "\t\t{\n\t\t\t\"input\": \"" + init_prompt + "\",\n\t\t\t\"output\": \"" + full_response + "\"\n\t\t},\n")
            else:
                data_entry = {
                    "input": init_prompt,
                    "output": str(xref)
                }
                interactions["conversations"].append(data_entry)
                ds_file.write(
                    "\t\t{\n\t\t\t\"input\": \"" + init_prompt + "\",\n\t\t\t\"output\": \"" + str(
                        xref) + "\"\n\t\t},\n")
        ds_file.write("]}")
    json.dump(interactions, open(ds_file_path, 'w'), indent=4)
    logging.log(logging.INFO, f"Dataset saved to {ds_file_path} with {samples} samples.")


def read_ds_file(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    # for i in track(range(10)):
    #     for j in range(3):
    #         generate_prob_w_sol(i)
    #         time.sleep(1)

    generate_synth_ds(300, prompt_model=True)
    # ds = read_ds_file("synthetic_ds.txt")
    # print(ds)
    # for obj in ds["conversations"]:
    #     print(obj['input'])
    #     print(obj['output'])
    #     print("\n")
