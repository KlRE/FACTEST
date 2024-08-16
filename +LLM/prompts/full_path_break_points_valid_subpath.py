from typing import List, Tuple

from prompts.Prompter import PathPrompter
from prompts.examples import full_path_ex


class FullPathBreakPointsValidSubPathPrompt(PathPrompter):
    """
    A prompter that asks the user to come up with a path that starts in the start set, ends in the goal set, and avoids obstacles.
    The path should pass through one of the breakpoints of each set. The path should be represented as an array of waypoints and the path will be constructed by connecting these waypoints linearly.
    The LLM will also get feedback on the longest valid subpath from the start to the first intersection.
    """

    task_description = f"""
# Motion Planning Task
## Goal: Come up with a path that starts in the start set, ends in the goal set, and avoids obstacles.

## Path Requirements
    Waypoints: The path should be represented as an array of waypoints and the path will be constructed by connecting these waypoints linearly. Use arbitrary waypoints that do not always have to be parallel to one axis.
    Non-Crossing: Ensure the path and especially the linearly connected segments do not cross any obstacles. Make sure to keep a distance from the obstacles, because touching the obstacles is considered as crossing.
    Start and End: The path must start within the start set and end in the goal set.
    Breakpoints: Ensure the path passes through one of the breakpoints of each set.
    """

    init_prompt = """
## Instructions
    Path Array: Output the path as an array of waypoints.
    Breakpoints: Choose one waypoint from each set of breakpoints. The path should pass through one of the breakpoints of each set.
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
    {instruct_breakpoints}

## Instructions for Correction
    No code: Do not include any code in your response.
    Chain of Thought: Explain your thought process and the changes you made to the path. Analyze the spatial relationships between the obstacles and work out segments that are valid and invalid.
    {instruct_start}{instruct_end}{obstacle_instruct}{validpath_instruct}
    Breakpoints: Ensure the path passes through one of the breakpoints of each set. Not all of them lead to a valid path, so you may need to adjust the path accordingly.
    """

    def __init__(self, model, Theta, G, O, workspace, use_history, num_sections=3):
        super().__init__(model, Theta, G, O, workspace, use_history)
        self.num_sections = num_sections
        self.breakpoints = self.find_breakpoints()

    def get_feedback(self, path: List[Tuple], intersections, starts_in_init: bool, ends_in_goal: bool) -> str:
        obstacle_feedback, intersecting, intersection_idx = self.obstacle_feedback(intersections, path)

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

        if intersecting:
            valid_subpath = path[:intersection_idx + 1]
            subpath_feedback = f"""First segment to cross with an Obstacle (Rectangular Sets): (xmin, xmax, ymin, ymax):
    {obstacle_feedback}\tLongest valid subpath from start: {valid_subpath}"""

        else:
            subpath_feedback = "Your path does not cross any obstacles"

        missing_breakpoints = self.check_path_through_breakpoints(path)
        if missing_breakpoints:
            missing_breakpoints_str = ""
            for i in missing_breakpoints:
                missing_breakpoints_str += f"\t\tBreakpoint Set {i + 1}: {self.breakpoints[i]}\n"
            instruct_breakpoints = f"Breakpoints: Ensure the path passes through one of the breakpoints of each set. Missing breakpoint sets:\n {missing_breakpoints_str}\t"
        else:
            instruct_breakpoints = ""

        feedback = self.feedback_prompt.format(path=path, obstacle_feedback=obstacle_feedback, Theta=self.Theta,
                                               G=self.G, O=self.O,
                                               workspace=self.workspace, start_feedback=start_feedback,
                                               end_feedback=end_feedback,
                                               instruct_start=instruct_start, instruct_end=instruct_end,
                                               subpath_feedback=subpath_feedback,
                                               obstacle_instruct="" if not intersecting else "Obstacle Avoidance: Adjust the path to avoid intersecting obstacles. You may add waypoints at problematic waypoints to move around obstacles.\n",
                                               validpath_instruct="" if not intersecting else "\t\tPath Adjustments: Try to either continue from the valid subpath or suggest a new path in case the current path ends in a dead end.",
                                               instruct_breakpoints=instruct_breakpoints)
        return feedback

    def get_init_instruction(self) -> str:
        return self.init_prompt.format(Theta=self.Theta, G=self.G, O=self.O,
                                       breakpoint_prompt=self.get_breakpoint_prompt())

    def get_task_description(self):
        return self.task_description

    def get_init_prompt(self):
        return super().get_init_prompt() + full_path_ex()

    def get_feedback_prompt(self, path: List[Tuple], intersections, starts_in_init: bool,
                            ends_in_goal: bool):
        return super().get_feedback_prompt(path=path, intersections=intersections, starts_in_init=starts_in_init,
                                           ends_in_goal=ends_in_goal) + full_path_ex()

    def get_task_data(self):
        bp_str = "Breakpoints:\n"
        for i, bp in enumerate(self.breakpoints):
            bp_str += f"\t\tBreakpoint Set {i + 1}: {bp}\n"
        return super().get_task_data() + f"{bp_str}"

    def find_breakpoints(self):
        """
        Given environment parameters, divide the environment into num_sections sections vertically. Find the breakpoints where segments meet.
        """
        Theta, G, O, workspace = self.Theta, self.G, self.O, self.workspace
        num_sections = self.num_sections
        signed_segment_length = ((G[1] + G[0]) / 2 - (Theta[1] + Theta[0]) / 2) / num_sections

        breakpoints = [[] for _ in range(num_sections - 1)]

        upper_bound, lower_bound = workspace[3], workspace[2]
        for i in range(num_sections - 1):
            vertical_line = round(Theta[0] + (i + 1) * signed_segment_length, 2)

            meeting_obstacles = []
            for xmin, xmax, ymin, ymax in O:
                if xmin <= vertical_line <= xmax:
                    meeting_obstacles.append((xmin, xmax, ymin, ymax))
            meeting_obstacles.sort(key=lambda x: x[2])

            for j in range(len(meeting_obstacles) + 1):
                if j == 0:
                    lower = lower_bound
                else:
                    lower = meeting_obstacles[j - 1][3]

                if j == len(meeting_obstacles):
                    upper = upper_bound
                else:
                    upper = meeting_obstacles[j][2]
                if upper > lower:
                    breakpoints[i].append((vertical_line, round((upper + lower) / 2, 2)))
        return breakpoints

    def get_breakpoint_prompt(self):
        prompt = f"""
Intermediate Breakpoints: You will be given multiple sets of breakpoints that divide the environment into sections. Choose one breakpoint from each set. The path should pass through one of the breakpoints of each set.
"""
        for i, bp in enumerate(self.breakpoints):
            prompt += f"\t\tBreakpoint Set {i + 1}: {bp}\n"
        return prompt

    def check_path_through_breakpoints(self, path):
        missing_breakpoints = []
        for i, bpset in enumerate(self.breakpoints):
            missing = True
            for bp in bpset:
                if bp in path:
                    missing = False
                    break
            if missing:
                missing_breakpoints.append(i)

        return missing_breakpoints

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
                obstacle_report = (f'\tSegment {i + 1} between points {path[i]} and {path[i + 1]} intersects with '
                                   f'obstacle(s):\n')

                for idx, obs in intersection:
                    obstacle_report += f"\t\t\tObstacle {idx + 1}: ({-obs.b[0]}, {obs.b[1]}, {-obs.b[2]}, {obs.b[3]})\n"
                return obstacle_report, intersecting, i
        intersecting = False
        return 'No intersections found. You avoided all obstacles!', intersecting, -1


if __name__ == "__main__":
    from prompts.Prompter import Model
    from convert_polytope_to_arrays import convert_env_polytope_to_arrays
    from envs.maze_2d import Theta, G, O, workspace

    Theta, G, O, workspace = convert_env_polytope_to_arrays(Theta, G, O, workspace)

    prompter = FullPathBreakPointsValidSubPathPrompt(Model.LLAMA3_8b, Theta, G, O, workspace, use_history=True)
    print(prompter.get_breakpoint_prompt())
    print(prompter.get_init_prompt())
    print(prompter.get_init_instruction())
    print(prompter.get_task_data())
    path = [(0, 0), (1, 1), (2.4, 0.5), (3, 3), (5, 5)]
    print(prompter.check_path_through_breakpoints(path))
    print(prompter.get_feedback_prompt(path=path, intersections=[], starts_in_init=True, ends_in_goal=True))
