import random
from enum import Enum
import importlib
from typing import Tuple, List

import numpy as np
import polytope as pc
from rich.progress import track
from scipy.spatial import ConvexHull


class Env(Enum):
    BOX = 'box'
    BOX_BOUNDARY = 'box_boundary'
    CANYON = 'canyon'
    CURVE = 'curve'
    DIAGONAL_WALL = 'diagonal_wall'
    EASY = 'easy'
    MAZE_2D = 'maze_2d'
    SCOTS_HSCC16 = 'scots_hscc16'
    SPIRAL = 'spiral'
    WALL = 'wall'

    def __str__(self):
        return self.value

    @staticmethod
    def generate_env(num_obstacles: int):
        """
        Generate a random environment with the given number of obstacles. The obstacles are randomly placed in the workspace.
        The workspace is a 10x10 square. The start set is a 2x2 square in the bottom left corner. The goal set is a 2x2 square in the top right corner.
        """
        # Define the workspace
        A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
        b_workspace = np.array([2, 22, 2, 22])  # (-xmin, xmax, -ymin, ymax)
        workspace = pc.Polytope(A, b_workspace)

        # Define the start set
        b_init = np.array([0, 2, 0, 2])
        Theta = pc.Polytope(A, b_init)

        # Define the goal set
        b_goal = np.array([-18, 20, -18, 20])
        G = pc.Polytope(A, b_goal)

        # Define the obstacles
        O = []
        generated_obstacles = 0

        lower_bound = np.array([0, 0])
        upper_bound = np.array([20, 20])

        while generated_obstacles < num_obstacles:
            while True:
                # Generate random points
                points = np.random.uniform(lower_bound, upper_bound, (4, 2))

                poly = pc.qhull(points)
                if len(poly.vertices) == 4 and not pc.is_adjacent(poly, Theta) and not pc.is_adjacent(poly, G):
                    O.append(poly)
                    generated_obstacles += 1
                    break

        return Theta, G, O, workspace


class UnsolvableEnv(Enum):
    BOX = 'box'
    BOX_2 = 'box_2'
    CANYON = 'canyon'
    CURVE = 'curve'
    DIAGONAL_WALL = 'diagonal_wall'
    EASY = 'easy'
    MAZE_2D = 'maze_2d'
    SCOTS_HSCC16 = 'scots_hscc16'
    SPIRAL = 'spiral'
    WALL = 'wall'

    def __str__(self):
        return self.value


env_modules = {
    Env.BOX: 'envs.box',
    Env.BOX_BOUNDARY: 'envs.box_boundary',
    Env.CANYON: 'envs.canyon',
    Env.CURVE: 'envs.curve',
    Env.DIAGONAL_WALL: 'envs.diagonal_wall',
    Env.EASY: 'envs.easy',
    Env.MAZE_2D: 'envs.maze_2d',
    Env.SCOTS_HSCC16: 'envs.scots_hscc16',
    Env.SPIRAL: 'envs.spiral',
    Env.WALL: 'envs.wall',

    UnsolvableEnv.BOX: 'envs.unsolvable.unsolvable_box',
    UnsolvableEnv.BOX_2: 'envs.unsolvable.unsolvable_box_2',
    UnsolvableEnv.CANYON: 'envs.unsolvable.unsolvable_canyon',
    UnsolvableEnv.CURVE: 'envs.unsolvable.unsolvable_curve',
    UnsolvableEnv.DIAGONAL_WALL: 'envs.unsolvable.unsolvable_diagonal_wall',
    UnsolvableEnv.EASY: 'envs.unsolvable.unsolvable_easy',
    UnsolvableEnv.MAZE_2D: 'envs.unsolvable.unsolvable_maze_2d',
    UnsolvableEnv.SCOTS_HSCC16: 'envs.unsolvable.unsolvable_scots_hscc16',
    UnsolvableEnv.SPIRAL: 'envs.unsolvable.unsolvable_spiral',
    UnsolvableEnv.WALL: 'envs.unsolvable.unsolvable_wall',
}


def import_environment(env) -> Tuple[pc.Polytope, pc.Polytope, List[pc.Polytope], pc.Polytope]:
    """
    Import the environment module based on the given environment name.
    :param env_inp: Environment name or Env enum
    """
    try:
        assert isinstance(env, Env) or isinstance(env, UnsolvableEnv), f'Invalid environment type: {type(env)}'

        module_path = env_modules[env]
        module = importlib.import_module(module_path)
        Theta: pc.Polytope = getattr(module, 'Theta')
        G: pc.Polytope = getattr(module, 'G')
        O: List[pc.Polytope] = getattr(module, 'O')
        workspace: pc.Polytope = getattr(module, 'workspace')

        return Theta, G, O, workspace

    except KeyError:
        raise ValueError(f'Environment {env} not found')
    except AttributeError as e:
        raise ImportError(f'Failed to import environment {env}: {e}')


import random


def create_environment_file(index, Theta, G, O, workspace):
    filename = f"random_env_{index:02d}.py"
    with open(filename, 'w') as f:
        f.write("import polytope as pc\n")
        f.write("import numpy as np\n\n")
        f.write(f"title = '2D Random Obstacle Environment {index}'\n\n")
        f.write("A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])\n")

        f.write(f"b_init = np.array({Theta.b.tolist()})\n")
        f.write("Theta = pc.Polytope(A, b_init)\n\n")

        f.write(f"b_goal = np.array({G.b.tolist()})\n")
        f.write("G = pc.Polytope(A, b_goal)\n\n")

        for i, obstacle in enumerate(O):
            f.write(f"b{i + 1} = np.array({obstacle.b.tolist()})\n")
            f.write(f"O{i + 1} = pc.Polytope(A, b{i + 1})\n")

        f.write(f"O = [{', '.join([f'O{i + 1}' for i in range(len(O))])}]\n\n")

        f.write(f"b_workspace = np.array({workspace.b.tolist()})\n")
        f.write("workspace = pc.Polytope(A, b_workspace)\n\n")

        f.write("if __name__ == \"__main__\":\n")
        f.write("    from envs.plot_env import plot_env\n")
        f.write("    plot_env(title, workspace, G, Theta, O)\n")


def generate_python_envs():
    random.seed(42)  # For reproducibility
    for i in track(range(20)):
        Theta, G, O, workspace = Env.generate_env(num_obstacles=i)
        create_environment_file(i + 1, Theta, G, O, workspace)
        print(f"Created environment_{i + 1:02d}.py")


if __name__ == "__main__":
    from envs.plot_env import plot_env

    for _ in range(10):
        Theta, G, O, workspace = Env.generate_env(3)
        plot_env("Random Environment", workspace, G, Theta, O)

    # generate_python_envs()
    # for env in Env:
    #     Theta, G, O, workspace = import_environment(env)
    #     print(f'{env.value}: {Theta}, {G}, {O}, {workspace}')
    #
    # Theta, G, O, workspace = import_environment('maze_2d')
    # print(Theta, G, O, workspace)
