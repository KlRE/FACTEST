from typing import List, Tuple

from prompts.Prompter import PathPrompter
from prompts.examples import full_path_ex


class FullPathValidPathPrompt(PathPrompter):
    task_description = f"""
# Motion Planning Task
## Goal: Come up with a path that starts in the start set, ends in the goal set, and avoids obstacles.

## Path Requirements
    Waypoints: The path should be represented as an array of waypoints and the path will be constructed by connecting these waypoints with a straight line. Use arbitrary waypoints that do not always have to be parallel to one axis.
    Non-Crossing: Ensure the path and especially the segments do not cross any obstacles. Make sure to keep a distance from the obstacles, because touching the obstacles is considered as crossing.
    Start and End: The path must start within the start set and end in the goal set.
    """

    init_prompt = """
        ## Instructions
            Path Array: Output the path as an array of waypoints, where you are allowed to use arbitrary waypoints that do not always have to be parallel to one axis.
            Start and End: The path must begin at any point within the start set and end at any point within the goal set.
            Obstacle Avoidance: Verify that the path does not intersect any obstacles.
            No code: Do not include any code in your response and do not try solve this with an algorithm.
            """

    feedback_prompt = """
    ## Your generated path:
        path = {path}

    ## Feedback
        Start set: {start_feedback}
        End set: {end_feedback}
        {subpath_feedback}


    ## Instructions for Correction
        No code: Do not include any code in your response.
        Chain of Thought: Explain your thought process and the changes you made to the path. Analyze the spatial relationships between the obstacles and work out segments that are valid and invalid.
        {instruct_start}{instruct_end}{obstacle_instruct}{validpath_instruct}
        """

    def get_feedback(self, path: List[Tuple], intersections, starts_in_init: bool, ends_in_goal: bool) -> str:
        """
        Get the feedback for the path (Will only be called if the maze is not solved)
        """
        obstacle_feedback, intersecting, intersection_idx = self.obstacle_feedback(intersections, path)

        if starts_in_init:
            start_feedback = "Correct, The path starts in the correct start set."
            instruct_start = ""
        else:
            start_feedback = f"Incorrect, The path does not start in the correct start set {self.Theta.tolist()}."
            instruct_start = "Start Position: Begin within the specified rectangular start set.\n"

        if ends_in_goal:
            end_feedback = "Correct, The path ends inside the goal set."
            instruct_end = ""
        else:
            end_feedback = f"Incorrect, The path does not end inside the goal set {self.G.tolist()}."
            instruct_end = "Goal Position: End within the specified rectangular goal set.\n"

        if intersecting:
            valid_subpath = path[:intersection_idx + 1]
            subpath_feedback = f"""First segment to cross with an Obstacle (Polygon): Defined by the clockwise coordinates of its four vertices [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]:
    {obstacle_feedback}\t\tLongest valid subpath from start: {valid_subpath}"""

        else:
            subpath_feedback = "Your path does not cross any obstacles"

        feedback = self.feedback_prompt.format(path=path, obstacle_feedback=obstacle_feedback, Theta=self.Theta,
                                               G=self.G, O=self.O,
                                               workspace=self.workspace, start_feedback=start_feedback,
                                               end_feedback=end_feedback,
                                               instruct_start=instruct_start, instruct_end=instruct_end,
                                               subpath_feedback=subpath_feedback,
                                               obstacle_instruct="" if not intersecting else "Obstacle Avoidance: Adjust "
                                                                                             "the path to avoid "
                                                                                             "intersecting obstacles. You "
                                                                                             "may add waypoints at "
                                                                                             "problematic waypoints to "
                                                                                             "move around obstacles. You are not limited to only using parallel segments.\n",
                                               validpath_instruct="" if not intersecting else "\t\tPath Adjustments: Try to "
                                                                                              "either continue from the "
                                                                                              "valid subpath or suggest a "
                                                                                              "new path in case the "
                                                                                              "current path ends in a "
                                                                                              "dead end.")
        return feedback

    def get_init_instruction(self) -> str:
        return self.init_prompt.format(Theta=self.Theta, G=self.G, O=self.O)

    def get_task_description(self):
        return self.task_description

    def get_init_prompt(self):
        return super().get_init_prompt() + full_path_ex()

    def get_feedback_prompt(self, path: List[Tuple], intersections, starts_in_init: bool,
                            ends_in_goal: bool):
        return super().get_feedback_prompt(path=path, intersections=intersections, starts_in_init=starts_in_init,
                                           ends_in_goal=ends_in_goal) + full_path_ex()

    def obstacle_feedback(self, intersections, path):
        """
        Get the feedback for the obstacle avoidance
        :param intersections: Intersections
        :param path: Path
        :return: (str) Feedback, (bool) Intersecting
        """
        intersecting = True

        for i, intersection in enumerate(intersections):
            if len(intersection) > 0:
                obstacle_report = (f'\t\tSegment {i + 1} between points {path[i]} and {path[i + 1]} intersects with '
                                   f'obstacle(s):\n')

                for idx, obs in intersection:
                    obstacle_report += f"\t\t\t\tObstacle {idx + 1}: {self.O[idx].tolist()})\n"
                return obstacle_report, intersecting, i
        intersecting = False
        return 'No intersections found. You avoided all obstacles!', intersecting, -1


if __name__ == "__main__":
    from prompts.Prompter import Model

    Theta = (0, 1, 0, 1)
    G = (4, 5, 4, 5)
    O = [(2, 3, 2, 3), (1, 2, 1, 2)]
    workspace = (0, 5, 0, 5)
    path = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    intersections = []

    prompter = FullPathValidPathPrompt(Model.LLAMA3_8b, Theta, G, O, workspace)
    print(prompter.get_init_prompt())
    print(prompter.get_feedback_prompt(path=path, intersections=intersections, starts_in_init=True,
                                       ends_in_goal=True))
    print(prompter.get_feedback(path=path, intersections=intersections, starts_in_init=True,
                                ends_in_goal=True))
    print(prompter.get_init_instruction())
    print(prompter.get_task_data())
