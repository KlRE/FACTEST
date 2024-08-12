from typing import List, Tuple

from prompts.Prompter import PathPrompter
from prompts.examples import full_path_ex


class FullPathPrompt(PathPrompter):
    task_description_template = """
# Motion Planning Task
## Goal: Come up with a path that starts in the start set, ends in the goal set, and avoids obstacles.

## Path Requirements
    Waypoints: The path should be represented as an array of waypoints and the path will be constructed by connecting these waypoints with a straight line. Use arbitrary waypoints that do not always have to be parallel to one axis.
    Non-Crossing: Ensure the path and especially the segments do not cross any obstacles. Make sure to keep a distance from the obstacles, because touching the obstacles is considered as crossing.
    Start and End: The path must start within the start set and end in the goal set.
{breakpoint_section}
"""

    init_prompt_template = """
## Instructions
    Path Array: Output the path as an array of waypoints, where you are allowed to use arbitrary waypoints that do not always have to be parallel to one axis.
    Start and End: The path must begin at any point within the start set and end at any point within the goal set.
    Obstacle Avoidance: Verify that the path does not intersect any obstacles.
{breakpoint_instruction}
    No code: Do not include any code in your response and do not try to solve this with an algorithm.
"""

    feedback_prompt_template = """
## Your generated path:
    path = {path}

## Feedback
    Start set: {start_feedback}
    End set: {end_feedback}
    {obstacle_feedback}
{breakpoint_feedback}

## Instructions for Correction
    No code: Do not include any code in your response.
    Chain of Thought: Explain your thought process and the changes you made to the path. Analyze the spatial relationships between the obstacles and work out segments that are valid and invalid.
    {instruct_start}{instruct_end}{obstacle_instruct}{breakpoint_instruct}{validpath_instruct}
"""

    def __init__(self, model, Theta, G, O, workspace, use_history, include_breakpoints=False, num_sections=3):
        super().__init__(model, Theta, G, O, workspace, use_history)
        self.include_breakpoints = include_breakpoints
        if self.include_breakpoints:
            self.num_sections = num_sections
            self.breakpoints = self.find_breakpoints()
            self.breakpoint_prompt = self.get_breakpoint_prompt()
        else:
            self.breakpoints = []
            self.breakpoint_prompt = ""

    def get_task_description(self):
        breakpoint_section = ""
        if self.include_breakpoints:
            breakpoint_section = """
    Breakpoints: The path must pass through specified breakpoints dividing the environment into sections."""
        return self.task_description_template.format(breakpoint_section=breakpoint_section)

    def get_init_instruction(self) -> str:
        breakpoint_instruction = ""
        if self.include_breakpoints:
            breakpoint_instruction = f"""
    Breakpoints: Choose one waypoint from each set of breakpoints. The path should pass through one of the breakpoints of each set.
{self.breakpoint_prompt}"""
        return self.init_prompt_template.format(breakpoint_instruction=breakpoint_instruction)

    def get_init_prompt(self):
        return self.get_task_description() + self.get_init_instruction() + full_path_ex()

    def get_feedback_prompt(self, path: List[Tuple], intersections, starts_in_init: bool,
                            ends_in_goal: bool):
        obstacle_feedback, intersecting, intersection_idx = self.obstacle_feedback(intersections, path)

        if starts_in_init:
            start_feedback = "Correct, the path starts in the correct start set."
            instruct_start = ""
        else:
            start_feedback = f"Incorrect, the path does not start in the correct start set {self.Theta}."
            instruct_start = "Start Position: Begin within the specified rectangular start set.\n"

        if ends_in_goal:
            end_feedback = "Correct, the path ends inside the goal set."
            instruct_end = ""
        else:
            end_feedback = f"Incorrect, the path does not end inside the goal set {self.G}."
            instruct_end = "Goal Position: End within the specified rectangular goal set.\n"

        if intersecting:
            valid_subpath = path[:intersection_idx + 1]
            obstacle_feedback_text = f"""Obstacle Avoidance:
    First segment to cross with an Obstacle (Rectangular Sets): (xmin, xmax, ymin, ymax):
{obstacle_feedback}
    Longest valid subpath from start: {valid_subpath}"""
            obstacle_instruct = "Obstacle Avoidance: Adjust the path to avoid intersecting obstacles. You may add waypoints at problematic waypoints to move around obstacles. You are not limited to only using parallel segments.\n"
            validpath_instruct = "\t\tPath Adjustments: Try to either continue from the valid subpath or suggest a new path in case the current path ends in a dead end.\n"
        else:
            obstacle_feedback_text = "Obstacle Avoidance: Your path does not cross any obstacles."
            obstacle_instruct = ""
            validpath_instruct = ""

        breakpoint_feedback = ""
        breakpoint_instruct = ""
        if self.include_breakpoints:
            missing_breakpoints = self.check_path_through_breakpoints(path)
            if missing_breakpoints:
                missing_breakpoints_str = ""
                for i in missing_breakpoints:
                    missing_breakpoints_str += f"\t\tBreakpoint Set {i + 1}: {self.breakpoints[i]}\n"
                breakpoint_feedback = f"Breakpoints: The path is missing the following breakpoint sets:\n{missing_breakpoints_str}"
                breakpoint_instruct = "Breakpoints: Ensure the path passes through one of the breakpoints of each set.\n"
            else:
                breakpoint_feedback = "Breakpoints: The path passes through all required breakpoints."

        feedback = self.feedback_prompt_template.format(
            path=path,
            start_feedback=start_feedback,
            end_feedback=end_feedback,
            obstacle_feedback=obstacle_feedback_text,
            breakpoint_feedback=breakpoint_feedback,
            instruct_start=instruct_start,
            instruct_end=instruct_end,
            obstacle_instruct=obstacle_instruct,
            breakpoint_instruct=breakpoint_instruct,
            validpath_instruct=validpath_instruct
        )
        return feedback + full_path_ex()

    def get_feedback(self, path: List[Tuple], intersections, starts_in_init: bool, ends_in_goal: bool) -> str:
        return self.get_feedback_prompt(path, intersections, starts_in_init, ends_in_goal)

    def obstacle_feedback(self, intersections, path):
        """
        Get the feedback for the obstacle avoidance
        :param intersections: Intersections
        :param path: Path
        :return: (str) Feedback, (bool) Intersecting, (int) Index of first intersection
        """
        intersecting = True

        for i, intersection in enumerate(intersections):
            if len(intersection) > 0:
                obstacle_report = (f'\t\tSegment {i + 1} between points {path[i]} and {path[i + 1]} intersects with '
                                   f'obstacle(s):\n')

                for idx, obs in intersection:
                    obstacle_report += f"\t\t\tObstacle {idx + 1}: ({-obs.b[0]}, {obs.b[1]}, {-obs.b[2]}, {obs.b[3]})\n"
                return obstacle_report, intersecting, i
        intersecting = False
        return 'No intersections found. You avoided all obstacles!', intersecting, -1

    def find_breakpoints(self):
        """
        Given environment parameters divide the environment into num_sections sections vertically. Find the breakpoints where segments meet
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


if __name__ == "__main__":
    from prompts.Prompter import Model

    # Example environment parameters
    Theta = (0, 1, 0, 1)
    G = (4, 5, 4, 5)
    O = [(2, 3, 2, 3), (1, 2, 1, 2)]
    workspace = (0, 5, 0, 5)
    path = [(0, 0), (1, 1), (2.4, 5.5), (3, 3), (4.4, 0.5), (5, 5)]
    intersections = []

    # Example usage without breakpoints
    prompter_no_bp = FullPathPrompt(Model.LLAMA3_8b, Theta, G, O, workspace, use_history=False,
                                    include_breakpoints=False)
    print("=== Without Breakpoints ===")
    print(prompter_no_bp.get_init_prompt())
    print(prompter_no_bp.get_feedback_prompt(path=path, intersections=intersections, starts_in_init=True,
                                             ends_in_goal=True))

    # Example usage with breakpoints
    prompter_with_bp = FullPathPrompt(Model.LLAMA3_8b, Theta, G, O, workspace, use_history=False,
                                      include_breakpoints=True, num_sections=3)
    print("=== With Breakpoints ===")
    print(prompter_with_bp.get_init_prompt())
    print(prompter_with_bp.get_feedback_prompt(path=path, intersections=intersections, starts_in_init=True,
                                               ends_in_goal=True))
