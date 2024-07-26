from enum import Enum
import importlib


# Step 1: Define an enum for the environments
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


# Step 2: Create a dictionary mapping enum values to module paths
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
}


# Step 3: Function to import the necessary modules dynamically
def import_environment(env_inp):
    try:
        if isinstance(env_inp, str):
            env = Env(env_inp)
        elif isinstance(env_inp, Env):
            env = env_inp
        else:
            raise ValueError('Invalid input')

        module_path = env_modules[env]
        module = importlib.import_module(module_path)
        Theta = getattr(module, 'Theta')
        G = getattr(module, 'G')
        O = getattr(module, 'O')
        workspace = getattr(module, 'workspace')

        return Theta, G, O, workspace

    except KeyError:
        raise ValueError(f'Environment {env_inp} not found')
    except AttributeError as e:
        raise ImportError(f'Failed to import environment {env_inp}: {e}')


if __name__ == "__main__":
    for env in Env:
        Theta, G, O, workspace = import_environment(env)
        print(f'{env.value}: {Theta}, {G}, {O}, {workspace}')

    Theta, G, O, workspace = import_environment('maze_2d')
    print(Theta, G, O, workspace)
