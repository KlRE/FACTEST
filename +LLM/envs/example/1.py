import polytope as pc
import numpy as np

title = '2D Box Environment'
A = np.array([[-1, 0],
              [1, 0],
              [0, -1],
              [0, 1]])

b_init = np.array([0, 1, 0, 1])
Theta = pc.Polytope(A, b_init)

b_goal = np.array([-4, 5, -4, 5])
G = pc.Polytope(A, b_goal)

b_unsafe1 = np.array([-3, 3.5, 0, 5])
b_unsafe2 = np.array([-3, 7, -5.5, 6])
b_unsafe3 = np.array([-3, 7, 1, 0])

O1 = pc.Polytope(A, b_unsafe1)
O2 = pc.Polytope(A, b_unsafe2)
O3 = pc.Polytope(A, b_unsafe3)

O = [O1, O2, O3]

b_workspace = np.array([0, 7, 1, 7])
workspace = pc.Polytope(A, b_workspace)

if __name__ == "__main__":
    from envs.plot_env import plot_env
    from prompts.full_path_prompt import FullPathPrompt
    from prompts.Prompter import Model
    from prompts.step_by_step_prompt import StepByStepPrompt
    from convert_polytope_to_arrays import convert_env_polytope_to_arrays

    plot_env(title, workspace, G, Theta, O)
    Theta, G, O, workspace = convert_env_polytope_to_arrays(Theta, G, O, workspace)
    step_by_step_prompt = StepByStepPrompt(Model.LLAMA3_8b, Theta, G, O, workspace)
    print(step_by_step_prompt.get_init_prompt())

    full_path_prompt = FullPathPrompt(Model.LLAMA3_8b, Theta, G, O, workspace)
    print(full_path_prompt.get_init_prompt())
