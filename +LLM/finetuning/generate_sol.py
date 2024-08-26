from matplotlib import pyplot as plt
from rich.progress import track

from envs.plot_env import plotPoly
from factest.factest_base_z3 import FACTEST_Z3
from import_env import Env
from prompts.Prompter import Prompter, Model
from prompts.full_path_prompt import FullPathPrompt


def generate_prob_w_sol():
    while True:
        try:
            Theta, G, O, workspace = Env.generate_env(num_obstacles=5)
            FACTEST_prob = FACTEST_Z3(Theta, G, O, workspace=workspace)
            result_dict = FACTEST_prob.run()
            result_keys = list(result_dict.keys())
            xref = result_dict[result_keys[0]]['xref']

            xref_1 = [xval[0] for xval in xref]
            xref_2 = [xval[1] for xval in xref]
            fig, ax = plt.subplots()
            plotPoly(workspace, ax, 'yellow')
            plotPoly(Theta, ax, 'blue')
            plotPoly(G, ax, 'green')
            plotPoly(O, ax, 'red')
            ax.plot(xref_1, xref_2, marker='o')
            ax.autoscale()

            plt.show()
            return Theta, G, O, workspace, xref

        except Exception as e:
            print(e)
            continue


def generate_synth_ds(samples=10, model: Model = Model.GEMINI_1_5_PRO_VERTEX, file_dir="."):
    """
    Generate synthetic dataset for the factest problem
    """
    ds_file_path = f"{file_dir}/synthetic_ds.txt"

    with open(ds_file_path, "w") as ds_file:
        ds_file.write("""{
    "conversations": [""")
        for i in track(range(samples)):
            Theta, G, O, workspace, xref = generate_prob_w_sol()
            prompter = FullPathPrompt(model, Theta, G, O, workspace)
            init_prompt = prompter.get_init_prompt()
            prompt = f"""
You are given the following environment with the following prompt:
{init_prompt}
--------------------------------------------------------------------------
This is the initial prompt for the problem. You are given the correct solution to this Problem. The solution is the following path:
{xref}
--------------------------------------------------------------------------
Please write a detailed description, why the solution is correct. Analyze the path, the environment and the spatial relationships between them.
Write this as an explanation of the solution.
"""
            successful, response = prompter.prompt_model(prompt)

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
                ds_file.write(f"{data_entry},")
        ds_file.write("]}")


if __name__ == "__main__":
    generate_synth_ds(10)
