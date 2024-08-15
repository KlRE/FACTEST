import random
from enum import Enum
import importlib
from typing import Tuple, List

import numpy as np
import polytope as pc


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
        b_workspace = np.array([2, 12, 2, 12])  # (-xmin, xmax, -ymin, ymax)
        workspace = pc.Polytope(A, b_workspace)

        # Define the start set
        b_init = np.array([0, 2, 0, 2])
        Theta = pc.Polytope(A, b_init)

        # Define the goal set
        b_goal = np.array([-8, 10, -8, 10])
        G = pc.Polytope(A, b_goal)

        # Define the obstacles
        O = []
        generated_obstacles = 0
        while generated_obstacles < num_obstacles:
            # Generate random obstacle rounded to one decimal place
            xmin = round(random.uniform(0, 9), 1)
            xmax = round(random.uniform(xmin + 0.5, 10), 1)
            ymin = round(random.uniform(0, 10), 1)
            ymax = round(random.uniform(ymin + 0.5, 10), 1)
            # check if overlaps with start or goal
            if xmin <= 2 and ymin <= 2 or xmax >= 8 and ymax >= 8:
                continue
            b = np.array([-xmin, xmax, -ymin, ymax])
            O.append(pc.Polytope(A, b))
            generated_obstacles += 1

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

    UnsolvableEnv.BOX: 'envs.unsolvable.box',
    UnsolvableEnv.BOX_2: 'envs.unsolvable.box_2',
    UnsolvableEnv.CANYON: 'envs.unsolvable.canyon',
    UnsolvableEnv.CURVE: 'envs.unsolvable.curve',
    UnsolvableEnv.DIAGONAL_WALL: 'envs.unsolvable.diagonal_wall',
    UnsolvableEnv.EASY: 'envs.unsolvable.easy',
    UnsolvableEnv.MAZE_2D: 'envs.unsolvable.maze_2d',
    UnsolvableEnv.SCOTS_HSCC16: 'envs.unsolvable.scots_hscc16',
    UnsolvableEnv.SPIRAL: 'envs.unsolvable.spiral',
    UnsolvableEnv.WALL: 'envs.unsolvable.wall',
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


if __name__ == "__main__":
    from envs.plot_env import plot_env

    for _ in range(10):
        Theta, G, O, workspace = Env.generate_env(5)
        plot_env("Random Environment", workspace, G, Theta, O)

    # for env in Env:
    #     Theta, G, O, workspace = import_environment(env)
    #     print(f'{env.value}: {Theta}, {G}, {O}, {workspace}')
    #
    # Theta, G, O, workspace = import_environment('maze_2d')
    # print(Theta, G, O, workspace)
