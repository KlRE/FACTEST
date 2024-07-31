import logging
import re
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple

import ollama


class Model(Enum):
    LLAMA3_8b = 'llama'
    MISTRAL_NEMO_12b = 'mistral-nemo'


class PromptStrategy(Enum):
    FULL_PATH = 'full_path'
    STEP_BY_STEP = 'step_by_step',

    @staticmethod
    def from_str(label):
        for prompt in PromptStrategy:
            if prompt.value == label:
                return prompt
        raise ValueError(f"Invalid label: {label}")


class Prompter(ABC):
    """Abstract class for LLM prompters which can implement different prompting strategies."""

    def __init__(self, model: Model, Theta, G, O, workspace):
        """
        Initialize the prompter. Currently takes in arrays. Todo change to polytopes and import conversion function here
        :param model: Model
        :param Theta: Initial set
        :param G: Goal set
        :param O: Obstacle set
        :param workspace: Workspace
        """
        if isinstance(model, Model):
            self.model = model.value
        else:
            raise ValueError("Model must be of type Model Enum")

        self.Theta = Theta
        self.G = G
        self.O = O
        self.workspace = workspace

    @staticmethod
    def from_Prompt_Strategy(Prompt_Strategy: PromptStrategy, model: Model, Theta, G, O, workspace):
        print(isinstance(model, Model), type(model))
        if Prompt_Strategy == PromptStrategy.FULL_PATH:
            from prompts.full_path_prompt import FullPathPrompt
            return FullPathPrompt(model, Theta, G, O, workspace)
        elif Prompt_Strategy == PromptStrategy.STEP_BY_STEP:
            from prompts.step_by_step_prompt import StepByStepPrompt
            return StepByStepPrompt(model, Theta, G, O, workspace)
        else:
            raise ValueError(f"Invalid Prompt Strategy: {Prompt_Strategy}")

    @abstractmethod
    def get_feedback(self, path: List[Tuple], obstacle_feedback: str, starts_in_init: bool, ends_in_goal: bool):
        """
        Get the feedback for the given environment
        :param path: Path
        :param obstacle_feedback: Obstacle feedback
        :param starts_in_init: Starts in initial set
        :param ends_in_goal: Ends in goal set
        :return: Feedback
        """
        pass

    @abstractmethod
    def get_init_instruction(self):
        """
        Get the initial prompt for the task
        :return: Initial prompt
        """
        pass

    @abstractmethod
    def parse_response(self, response: str):
        """
        Parse the response
        :param response: Response
        :return: Parsed response
        """
        pass

    @abstractmethod
    def get_path_output_format(self):
        """
        Get the output format for the task
        :return: Output format
        """
        pass

    def prompt_model(self, prompt: str, max_attempts=5, ):
        """
        Prompt the model with the given prompt and parse the response
        :param prompt: Prompt
        :param max_attempts: Maximum number of attempts
        """
        logging.info("Prompting model")
        logging.info(prompt)
        response = ollama.generate(model=self.model, prompt=prompt)
        logging.info(response['response'])
        for i in range(max_attempts):
            try:
                parsed_response = self.parse_response(response['response'])
                logging.info(f'Parsed response: {parsed_response}')
                return parsed_response
            except:
                logging.warning(f"Failed to parse response. Trying attempt {i + 1}")
                response = ollama.generate(model=self.model, prompt=prompt)
                logging.info(response['response'])
        raise ValueError("Failed to parse response")

    def prompt_init(self):
        """
        Prompt the initial instruction
        :return: Parsed response
        """
        init_prompt = self.get_init_prompt()
        return self.prompt_model(init_prompt)

    def prompt_feedback(self, path, obstacle_feedback, starts_in_init, ends_in_goal):
        """
        Prompt the feedback
        :param path: Path
        :param obstacle_feedback: Obstacle feedback
        :param starts_in_init: Starts in initial set
        :param ends_in_goal: Ends in goal set
        """
        feedback = self.get_feedback(path, obstacle_feedback, starts_in_init, ends_in_goal)
        return self.prompt_model(feedback)

    def get_feedback_prompt(self, path: List[Tuple], obstacle_feedback: str, starts_in_init: bool,
                            ends_in_goal: bool):
        """
        Get the feedback prompt for the given environment
        :param path: Path
        :param obstacle_feedback: Obstacle feedback
        :param starts_in_init: Starts in initial set
        :param ends_in_goal: Ends in goal set
        """
        task_desc = self.get_task_description()
        feedback = self.get_feedback(path, obstacle_feedback, starts_in_init, ends_in_goal)
        path_format = self.get_path_output_format()

        return task_desc + feedback + path_format

    def get_init_prompt(self):
        """
        Get the initial prompt for the task
        :return: Initial prompt
        """
        task_desc = self.get_task_description()
        init_prompt = self.get_init_instruction()
        path_format = self.get_path_output_format()
        return task_desc + init_prompt + path_format

    def get_task_description(self):
        """
        Get the task description for the given environment
        """
        if isinstance(self.O, list) and isinstance(self.O[0], tuple):
            o = "[\n"
            for i, obstacle in enumerate(self.O):
                o += f"\t\t\t{obstacle},   # Obstacle {i + 1}\n"
            o += "\t\t]"
            O = o

        task_description = f"""
# Motion Planning Task
## Goal: Come up with a path that starts in the start set, ends in the goal set, and avoids obstacles.

## Path Requirements
    Waypoints: The path should be represented as an array of waypoints and the path will be constructed by connecting these waypoints linearly.
    Non-Crossing: Ensure the path and especially the linearly connected segments do not cross any obstacles.
    Start and End: The path must start within the start set and end in the goal set.

## Provided Data
    Start Position (Rectangular Set): (xmin, xmax, ymin, ymax) = {self.Theta}
        Note: You can choose any point within this rectangle to start the path.
    Goal Position (Rectangular Set): (xmin, xmax, ymin, ymax) = {self.G}
        Note: You can choose any point within this rectangle to end the path.
    Obstacles (Rectangles):
        obstacles = {O}
    """
        return task_description


class PathPrompter(Prompter, ABC):
    def parse_response(self, response):
        # Extract the portion of the text containing the path array
        path_section = re.search(r'path\s*=\s*(\[.*?])', response, re.DOTALL).group(1)
        # Extract all coordinate pairs from the path array
        coordinate_pattern = re.compile(r'\([+-]?(?:\d*\.)?\d+, [+-]?(?:\d*\.)?\d+\)')
        coordinates = coordinate_pattern.findall(path_section)

        # Convert the found coordinate pairs to a list of tuples
        path = [tuple(map(float, coord.strip('()').split(', '))) for coord in coordinates]

        return path

    def get_path_output_format(self):
        """
        Get the output format for the task
        :return: Output format
        """
        return """
## Path Format:
    Provide the path as an array of waypoints.

    Example Path Output:
    path = [
        (waypoint_x1, waypoint_y1),    
        (waypoint_x2, waypoint_y2),
        (waypoint_x3, waypoint_y3),
        ...,
        (waypoint_xn, waypoint_yn)       
    ]
    """


if __name__ == "__main__":
    Theta = (0, 1, 0, 1)
    G = (4, 5, 4, 5)
    O = [(2, 3, 2, 3), (1, 2, 1, 2)]
    workspace = (0, 5, 0, 5)
    path = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]

    prompter = Prompter.from_Prompt_Strategy(PromptStrategy.FULL_PATH, Model.LLAMA3_8b, Theta, G, O, workspace)
    print(prompter.get_init_prompt())
    print(prompter.get_feedback_prompt(path=path, obstacle_feedback="obstacle_feedback", starts_in_init=True,
                                       ends_in_goal=True))
    print(prompter.get_feedback(path=path, obstacle_feedback="obstacle_feedback", starts_in_init=True,
                                ends_in_goal=True))
    print(prompter.get_init_instruction())
    print(prompter.get_task_description())
    prompter = Prompter.from_Prompt_Strategy(PromptStrategy.STEP_BY_STEP, Model.LLAMA3_8b, Theta, G, O, workspace)
    print(prompter.get_init_prompt())
    print(prompter.get_feedback_prompt(path=path, obstacle_feedback="obstacle_feedback", starts_in_init=True,
                                       ends_in_goal=True))
