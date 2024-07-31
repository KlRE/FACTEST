from typing import List, Tuple

from prompts.Prompter import PathPrompter


class StepByStepPrompt(PathPrompter):
    current_path = []
    expected_length = 1

    def get_feedback(self, path: List[Tuple], intersections, starts_in_init: bool, ends_in_goal: bool) -> str:
        obstacle_feedback, intersecting = self.obstacle_feedback(intersections, path)

        if starts_in_init:
            start_feedback = "Correct, The path starts in the correct start set."
            instruct_start = ""
        else:
            start_feedback = f"Incorrect, The path does not start in the correct start set {self.Theta}."
            instruct_start = "Start Position: Begin within the specified rectangular start set.\n"

        if ends_in_goal:
            end_feedback = "Correct, The path ends inside the goal set."
            instruct_end = ""
        else:
            end_feedback = f"Incorrect, The path does not end inside the goal set {self.G}."
            instruct_end = "Goal Position: End within the specified rectangular goal set.\n"

        feedback_prompt_1 = f"""
## Your generated path:
    path = {path}

## Feedback
    Start set: {start_feedback}
    Obstacle Avoidance:
{obstacle_feedback}

    
## Instructions for Correction:
    No code: Do not include any code in your response.
"""
        if intersecting:
            feedback_prompt_2 = f"""
    {instruct_start}Adjust Only the Last Waypoint: Modify the last waypoint (currently {path[-1]}) so that the final segment does not intersect any obstacles and ends within the goal set. Do not add any waypoints to the array.
      The length of the array should be {len(path)} after correction. Since we are moving step-by-step, do not stray too far from the last waypoint.
    Segment Integrity: Ensure that the entire segment from {path[-2]} to the new last waypoint does not intersect any obstacles. The path should be valid for all segments between waypoints.
    Avoid Direct Placement: Do not place the last waypoint directly into the goal set. Instead, adjust it step-by-step while ensuring it avoids obstacles and finally ends within the goal set.
    Do not add or remove any waypoints; only adjust the last waypoint.
        """
        elif not starts_in_init:
            feedback_prompt_2 = f"""
    {instruct_start}Adjust the First Waypoint: Modify the first waypoint (currently {path[0]}) so that the path starts within the start set. Do not add any waypoints to the array.
    """
        else:
            self.expected_length += 1
            feedback_prompt_2 = f"""
    Add one (1) new waypoint to your current array of waypoints. So the new path will be of length {len(path) + 1}.
    No code: Do not include any code in your response.
    {instruct_start}{instruct_end}Obstacle Avoidance: Set the new waypoint to avoid intersecting obstacles. 
    Segment Integrity: Ensure that the entire segment from {path[-1]} to the new last waypoint does not intersect any obstacles. The path should be valid for all segments between waypoints.
    Avoid Direct Placement: Do not place the last waypoint directly into the goal set. Instead, adjust it step-by-step while ensuring it avoids obstacles and finally ends within the goal set.
    Do not add or remove any waypoints; only adjust the last waypoint.
        """

        return feedback_prompt_1 + feedback_prompt_2

    def get_init_instruction(self) -> str:
        init_prompt = """
## Instructions
    Path Array: Output the first waypoint of the path. So, an array consisting of one waypoint.
    Start: The path must begin at any point within the start set.
    Obstacle Avoidance: Verify that the point does not intersect with any obstacles.
    No code: Do not include any code in your response and do not try solve this with an algorithm.
        """
        return init_prompt.format(Theta=self.Theta, G=self.G, O=self.O)

    def parse_response(self, response):
        path = super().parse_response(response)
        if len(path) != self.expected_length:
            raise ValueError(f"Expected path of length {self.expected_length}, got path of length {len(path)}")
        return path


if __name__ == "__main__":
    from prompts.Prompter import Model

    Theta = (0, 1, 0, 1)
    G = (4, 5, 4, 5)
    O = [(2, 3, 2, 3), (1, 2, 1, 2)]
    workspace = (0, 5, 0, 5)
    path = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]

    prompter = StepByStepPrompt(Model.LLAMA3_8b, Theta, G, O, workspace)
    print(prompter.get_init_prompt())
    print(prompter.get_feedback_prompt(path=path, obstacle_feedback="obstacle_feedback", starts_in_init=True,
                                       ends_in_goal=True))
    print(prompter.get_feedback(path=path, obstacle_feedback="obstacle_feedback", starts_in_init=True,
                                ends_in_goal=True))
    print(prompter.get_init_instruction())
    print(prompter.get_task_description())
