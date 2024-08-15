import re

from prompts.Prompter import Prompter


class SolvablePrompt(Prompter):
    task_description = """
# Motion Planning Solvable Task
## Task: Determine if the given Environment is solvable or not. It is solvable if there exists a path that starts in the start set, ends in the goal set, and avoids obstacles.

## Path Requirements
    Waypoints: The path should be represented as an array of waypoints and the path will be constructed by connecting these waypoints linearly. Use arbitrary waypoints that do not always have to be parallel to one axis.
    Non-Crossing: Ensure the path and especially the linearly connected segments do not cross any obstacles. Make sure to keep a distance from the obstacles, because touching the obstacles is considered as crossing.
    Start and End: The path must start within the start set and end in the goal set.
    """

    initial_instruction = """
## Instructions
Solvable: Determine if the given environment is solvable or not. It is solvable if there exists a path that starts in the start set, ends in the goal set, and avoids obstacles. An answer is sufficient without a explicit path.
Chain of Reasoning: Provide a chain of reasoning that supports your answer. This can include any observations, insights, or logical deductions that you made while analyzing the environment.
Spatial Reasoning: Use spatial reasoning to analyze the environment. This includes understanding the relative positions of the start set, goal set, and obstacles.    
No code: Do not include any code in your response and do not try solve this with an algorithm.
"""

    output_format = """
## Output Format
- Chain of Reasoning: A textual description of the chain of reasoning that supports your answer.
- Solvable: A boolean value indicating whether the environment is solvable or not.

## Example
- Chain of Reasoning: The start set is completely enclosed by obstacles, so there is no way to reach the goal set without crossing obstacles.
- Solvable: False
"""

    def get_init_instruction(self):
        return self.initial_instruction

    def get_task_description(self):
        return self.task_description

    def parse_response(self, response: str):
        """
        Parse the response to get the Solvable value
        :param response: The response to parse
        :return: The Solvable value
        """
        search = re.search(r"Solvable\s*[:;,*.\-\s]*\s*(True|False)", response)
        Solvable = search.group(1)
        if Solvable == "True":
            return True
        elif Solvable == "False":
            return False
        else:
            raise ValueError("Invalid Solvable value: " + Solvable)

    def get_output_format(self):
        return self.output_format
