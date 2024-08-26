import base64
import json
import logging
import os
import re
import textwrap
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple, Any

import groq
import ollama
import vertexai
from anthropic import Anthropic
from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI
from supabase import create_client
from vertexai.generative_models import GenerativeModel, Image


# added /home/erik/miniconda3/envs/factest/lib/python3.10/site-packages/supafunc/_sync.py line 32 timeout=300

class Model(Enum):
    LLAMA3_8b = 'llama3.1'
    MISTRAL_NEMO_12b = 'mistral-nemo'
    LLAMA3_1_8b_Groq = 'llama-3.1-8b-instant'
    LLAMA3_1_70b_Groq = 'llama-3.1-70b-versatile'
    LLAMA3_70b_Groq = 'llama3-70b-8192'
    GEMINI_1_5_PRO = 'gemini-1.5-pro'
    GEMINI_1_5_FLASH = 'gemini-1.5-flash'
    GEMINI_1_5_PRO_VERTEX = 'gemini-1.5-pro-001'
    GEMINI_1_5_FLASH_VERTEX = 'gemini-1.5-flash-001'
    GPT_4o = 'gpt-4o-2024-08-06'
    SONNET = 'claude-3-5-sonnet-20240620'

    def __str__(self):
        return self.value


class PromptStrategy(Enum):
    FULL_PATH = 'full_path'
    STEP_BY_STEP = 'step_by_step'
    FULL_PATH_BREAK_POINTS = 'full_path_break_points'
    FULL_PATH_VALID_SUBPATH = 'full_path_valid_subpath'
    FULL_PATH_VALID_PATH_BREAK_POINTS = 'full_path_valid_path_break_points'

    @staticmethod
    def from_str(label):
        for prompt in PromptStrategy:
            if prompt.value == label:
                return prompt
        raise ValueError(f"Invalid label: {label}")

    def __str__(self):
        return self.value


class SinglePrompt(Enum):
    SOLVABLE_PROMPT = 'solvable_prompt'

    def __str__(self):
        return self.value


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
            self.model = model
        else:
            raise ValueError("Model must be of type Model Enum")

        if model == Model.LLAMA3_1_8b_Groq or model == Model.LLAMA3_1_70b_Groq:
            load_dotenv()
            self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        elif model == Model.GEMINI_1_5_PRO or model == Model.GEMINI_1_5_FLASH:
            load_dotenv()
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_KEY")
            self.client = create_client(url, key)

        elif model == Model.GEMINI_1_5_PRO_VERTEX or model == Model.GEMINI_1_5_FLASH_VERTEX:
            vertexai.init(project="gentle-keyword-432706-b3", location="us-central1")
            self.client = GenerativeModel(model.value)
            self.curr_loc = 1

        elif model == Model.GPT_4o:
            load_dotenv()
            self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        elif model == Model.SONNET:
            load_dotenv()
            self.client = Anthropic(
                api_key=os.environ.get("ANTHROPIC_API_KEY"),
            )

        self.Theta = Theta
        self.G = G
        self.O = O
        self.workspace = workspace
        self.sleeptime = 5

    @abstractmethod
    def get_init_instruction(self):
        """
        Get the initial prompt for the task
        :return: Initial prompt
        """
        pass

    @abstractmethod
    def get_task_description(self):
        """
        Get the task description for the given environment
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
    def get_output_format(self):
        """
        Get the output format for the task
        :return: Output format
        """
        pass

    def _prompt_model(self, prompt: str, retry, image_path=None):
        """
        Prompt the model depending on the model type
        """
        if image_path is not None:
            logging.info(f"Prompting with Image from {image_path}")

        if self.model == Model.LLAMA3_8b or self.model == Model.MISTRAL_NEMO_12b:
            if image_path:
                logging.warning("Image not supported for LLAMA3_8b and MISTRAL_NEMO_12b")
            return ollama.generate(model=self.model.value, prompt=prompt)['response']

        elif (self.model == Model.LLAMA3_1_8b_Groq or self.model == Model.LLAMA3_1_70b_Groq
              or self.model == Model.LLAMA3_70b_Groq or self.model == Model.GPT_4o):

            if retry:
                time.sleep(4)
            if not (image_path and self.model == Model.GPT_4o):
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model=self.model.value,
                )
            else:
                with open("/home/erik/FACTEST/+LLM/envs/plots/manual/Box.png", mode='rb') as file:
                    img = file.read()
                img_b64 = base64.b64encode(img).decode('utf-8')
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{img_b64}"
                                    }
                                }

                            ],
                        }
                    ],
                    model=self.model.value,
                )

            return chat_completion.choices[0].message.content

        elif self.model == Model.GEMINI_1_5_PRO or self.model == Model.GEMINI_1_5_FLASH:
            if retry:
                time.sleep(self.sleeptime)
                self.sleeptime *= 1.3
            else:
                self.sleep_time = 5

                response = self.client.functions.invoke(
                    "prompt",
                    invoke_options={
                        "headers": {
                            "Content-Type": "application/json",
                            "x-region": "us-west-1",  # fetch from Gemini API from (supabase) server outside of europe
                        },  # not needed when using the API from the US, rewrite this to use Gemini package directly
                        "body": {
                            "secret": "ButtrFly",
                            "prompt": prompt,
                            "model": self.model.value,
                        }
                    }
                )
                return json.loads(response)["text"]

        elif self.model == Model.GEMINI_1_5_PRO_VERTEX or self.model == Model.GEMINI_1_5_FLASH_VERTEX:
            locations = ["us-central1", "europe-west1", "europe-west2", "europe-west4", "europe-west6"]
            if retry:
                time.sleep(self.sleeptime)
                vertexai.init(project="gentle-keyword-432706-b3", location=locations[self.curr_loc])
                self.curr_loc = (self.curr_loc + 1) % len(locations)
                logging.info(f"Switching to Gemini location {locations[self.curr_loc]}")
            else:
                self.sleep_time = 5

            if image_path:
                image = Image.load_from_file(image_path)
                response = self.client.generate_content([prompt, image])
            else:
                response = self.client.generate_content(prompt)

            return response.text

        elif self.model == Model.SONNET:
            response = self.client.messages.create(
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="claude-3-haiku-20240307",
            )
            return response.content[0].text

    def prompt_model(self, prompt: str, image_path=None, max_attempts=30, log_message='Prompting model',
                     parse_response=True) -> Tuple[
        bool, Any]:
        """
        Prompt the model with the given prompt and parse the response
        :param prompt: Prompt
        :param image_path: Image path
        :param max_attempts: Maximum number of attempts
        :param log_message: Log message
        :return: (bool) Successful, (Any) Parsed response
        """
        successful = False
        logging.info(log_message)
        logging.info(prompt)
        retry = False
        for i in range(max_attempts):
            try:
                response = self._prompt_model(prompt, retry, image_path=image_path)
                logging.info(response)
                if parse_response:
                    parsed_response = self.parse_response(response)
                    logging.info(f'Parsed response: {parsed_response}')
                    successful = True
                    return successful, parsed_response

                successful = True
                return successful, response
            except groq.RateLimitError as e:
                logging.warning(f"Rate limit error: {e}.\n Trying again in 3 minutes")
                time.sleep(180)
            except Exception as e:
                logging.warning(f"Failed to parse response because of Exception {type(e)}{e} Trying attempt {i + 1}")
            retry = True
        return successful, None

    def prompt_init(self, img_path=None):
        """
        Prompt the initial instruction
        :return: Parsed response
        """
        init_prompt = self.get_init_prompt(use_img=img_path is not None)
        return self.prompt_model(init_prompt, image_path=img_path)

    def get_init_prompt(self, use_img=False):
        """
        Get the initial prompt for the task
        :return: Initial prompt
        """
        task_desc = self.get_task_description()
        task_data = self.get_task_data()
        init_prompt = self.get_init_instruction()
        path_format = self.get_output_format()
        image_description = self.get_image_description(path_given=False) if use_img else ""
        return task_desc + task_data + image_description + init_prompt + path_format

    def get_task_data(self):
        """
        Get the task description for the given environment
        """

        o = ""
        for i, obstacle in enumerate(self.O):
            o += f"\t\t\tObstacle {i + 1}: {obstacle.tolist()}\n"

        task_description = f"""
## Provided Data
    Start Position (Quadrilateral): Defined by the clockwise coordinates of its four vertices [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = {self.Theta.tolist()}
        Note: You can choose any point within this Quadrilateral to start the path.
    Goal Position (Quadrilateral): Defined by the clockwise coordinates of its four vertices [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = {self.G.tolist()}
        Note: You can choose any point within this Quadrilateral to end the path.
    Obstacles (Quadrilaterals): Each obstacle is defined by the clockwise coordinates of its four vertices [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]:
{o}
    """
        return task_description

    def get_image_description(self, path_given: bool):
        image_description = f"""
## Provided Image
    The attached image shows the environment with the start set, goal set, and obstacles. The start set is colored blue, the goal set is colored green, and the obstacles are colored red."""
        if path_given:
            image_description += f"""
    The image also displays the path you provided, represented by blue waypoints that are connected in a straight line by a blue line.
"""
        else:
            image_description += "\n"
        return image_description

    def get_example_solution(self):
        """
        Get the example solution for the task
        """
        pass


class PathPrompter(Prompter, ABC):
    """Abstract class for LLM prompters which can implement different prompting strategies for path planning tasks."""

    def __init__(self, model: Model, Theta, G, O, workspace, use_history=False, ):
        super().__init__(model, Theta, G, O, workspace)
        self.use_history = use_history
        if use_history:
            self.history = []

    @abstractmethod
    def get_feedback(self, path: List[Tuple], intersections, starts_in_init: bool, ends_in_goal: bool):
        """
        Get the feedback for the given environment
        :param path: Path
        :param intersections: Intersections
        :param starts_in_init: Starts in initial set
        :param ends_in_goal: Ends in goal set
        :param use_img: Use image
        :return: Feedback
        """
        pass

    def prompt_feedback(self, path, intersections, starts_in_init, ends_in_goal, path_img=None):
        """
        Prompt the feedback
        :param path: Path
        :param intersections: Intersections
        :param starts_in_init: Starts in initial set
        :param ends_in_goal: Ends in goal set
        :param path_img: image path
        """
        feedback = self.get_feedback_prompt(path, intersections, starts_in_init, ends_in_goal,
                                            use_img=path_img is not None)
        return self.prompt_model(feedback, path_img)

    def get_feedback_prompt(self, path: List[Tuple], intersections, starts_in_init: bool,
                            ends_in_goal: bool, use_img: bool):
        """
        Get the feedback prompt for the given environment
        :param path: Path
        :param intersections: Intersections
        :param starts_in_init: Starts in initial set
        :param ends_in_goal: Ends in goal set
        :param use_img: Use image
        """
        task_desc = self.get_task_description()
        task_data = self.get_task_data()
        feedback_str = self.get_feedback(path, intersections, starts_in_init, ends_in_goal)
        path_format = self.get_output_format()
        image_description = self.get_image_description(path_given=True) if use_img else ""
        history_str = ""
        if self.use_history:
            if len(self.history) > 0:
                for i, (path, feedback) in enumerate(self.history):
                    feedback = textwrap.indent(feedback, "\t")
                    history_str += f"### Attempt {i + 1}:{feedback}\n"
                history_str = "\n\n## History\n" + history_str
            self.history.append((path, "\n".join(feedback_str.split("\n")[:-4])))

        return task_desc + task_data + image_description + feedback_str + path_format + history_str

    def parse_response(self, response):
        """
        Parse the response to extract the path array
        Example response:
        path = [
            (0.0, 0.0),
            (1.0, 1.0),
            (2.0, 2.0),
            (3.0, 3.0),
            (4.0, 4.0),
            (5.0, 5.0)
        ]
        :param response: Response
        :return: Path array
        """
        # Extract the portion of the text containing the path array
        path_section = re.search(r'new_path\s*=\s*(\[.*?])', response, re.DOTALL).group(1)
        # Extract all coordinate pairs from the path array
        coordinate_pattern = re.compile(r'\([+-]?(?:\d*\.)?\d+, [+-]?(?:\d*\.)?\d+\)')
        coordinates = coordinate_pattern.findall(path_section)

        # Convert the found coordinate pairs to a list of tuples
        path = [tuple(map(float, coord.strip('()').split(', '))) for coord in coordinates]
        if len(path) == 0:
            raise ValueError("No path found in response")
        return path

    def get_output_format(self):
        """
        Get the output format for the task
        :return: Output format
        """
        return """
## Path Format:
    Provide the new path as an array of waypoints in the following format:
    new_path = [
        (waypoint_x1, waypoint_y1),    
        ...,
        (waypoint_xn, waypoint_yn)       
    ]
    """

    def obstacle_feedback(self, intersections, path):
        """
        Get the feedback for the obstacle avoidance
        :param intersections: Intersections
        :param path: Path
        :return: (str) Feedback, (bool) Intersecting
        """
        intersecting = True
        obstacle_report = []
        for i, intersection in enumerate(intersections):
            if len(intersection) > 0:
                obstacle_report.append(
                    f'\t\tSegment {i + 1} between points {path[i]} and {path[i + 1]} intersects with obstacle(s):')
                for idx, obs in intersection:
                    obstacle_report.append(
                        f"\t\t\tObstacle {idx + 1}: {self.O[idx].tolist()}")

        if len(obstacle_report) == 0:
            intersecting = False
            return 'No intersections found. You avoided all obstacles!', intersecting

        return '\n'.join(obstacle_report), intersecting


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
    print(prompter.get_task_data())
    prompter = Prompter.from_Prompt_Strategy(PromptStrategy.STEP_BY_STEP, Model.LLAMA3_8b, Theta, G, O, workspace)
    print(prompter.get_init_prompt())
    print(prompter.get_feedback_prompt(path=path, obstacle_feedback="obstacle_feedback", starts_in_init=True,
                                       ends_in_goal=True))
