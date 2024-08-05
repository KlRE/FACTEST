def find_breakpoints(num_sections, Theta, G, O, workspace):
    """
    Given environment parameters divide the environment into num_sections sections vertically. Find the breakpoints where segments meet
    :param num_sections: The number of sections to divide the environment into
    :param Theta: The rectangular start set
    :param G: The rectangular goal set
    :param O: The list of rectangular obstacles
    :param workspace: The rectangular workspace
    """

    signed_segment_length = ((G[1] + G[0]) / 2 - (Theta[1] + Theta[0]) / 2) / num_sections
    print(signed_segment_length)
    breakpoints = [[] for _ in range(num_sections - 1)]

    upper_bound, lower_bound = workspace[3], workspace[2]
    for i in range(num_sections - 1):
        vertical_line = round(Theta[0] + (i + 1) * signed_segment_length, 2)
        print(f"vertical_line: {vertical_line}")
        meeting_obstacles = []
        for xmin, xmax, ymin, ymax in O:
            if xmin <= vertical_line <= xmax:
                meeting_obstacles.append((xmin, xmax, ymin, ymax))
        meeting_obstacles.sort(key=lambda x: x[2])
        print(f"meeting_obstacles: {meeting_obstacles}")
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

        print(f"breakpoints: {breakpoints[i]}")


if __name__ == "__main__":
    from convert_polytope_to_arrays import convert_env_polytope_to_arrays
    from envs.maze_2d import Theta, G, O, workspace

    new_Theta, new_G, new_O, new_workspace = convert_env_polytope_to_arrays(Theta, G, O, workspace)
    breakpoints = find_breakpoints(4, new_Theta, new_G, new_O, new_workspace)
