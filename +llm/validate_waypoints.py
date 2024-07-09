from yices import *
import numpy as np

from envs.maze import problem


def ccw(A, B, C):
    """Check if the points A, B, and C are in counterclockwise order."""
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

def intersect(A, B, C, D):
    """Check if the line segments AB and CD intersect."""
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def check_waypoints_against_obstacles(waypoints, O, bloat_func, alpha):
    x_dim = len(waypoints[0])
    N = len(waypoints) - 1
    fmlas = []

    for (Ao, bo) in O:
        for i in range(N):
            fmla = []
            for row in range(len(Ao)):
                r = bloat_func(i, alpha)

                b = bo[row][0] + r
                str0 = ''
                str1 = ''
                for dim in range(x_dim):
                    a = Ao[row][dim]
                    str2 = f'(* {a} {waypoints[i][dim]})'
                    str3 = f'(* {a} {waypoints[i+1][dim]})'
                    if dim == 0:
                        str0 = str2
                        str1 = str3
                    else:
                        str0 = f'(+ {str0} {str2})'
                        str1 = f'(+ {str1} {str3})'

                fmla0 = f'(> {str0} {b})'
                fmla1 = f'(> {str1} {b})'
                fmla2 = f'(and {fmla0} {fmla1})'
                fmla.append(fmla2)
            fmla4 = ' '.join(fmla)
            fmlas.append('(or ' + fmla4 + ')')
    #constraints = f'(or {" ".join(fmlas)})'
    print(fmlas)
    return fmlas

def check_waypoints(waypoints, O, bloat_func, alpha):
    cfg = Config()
    cfg.default_config_for_logic('QF_LRA')
    ctx = Context(cfg)

    constraints = check_waypoints_against_obstacles(waypoints, O, bloat_func, alpha)
    fmlas = [Terms.parse_term(j) for j in constraints]
    ctx.assert_formulas(fmlas)

    status = ctx.check_context()
    print(status)
    if status == Status.SAT:
        print("Path doenst intersects with obstacles.")
        ctx.dispose()
        return None

    else:
        num_obstacles = len(O)
        obstacle_segments = [[] for _ in range(num_obstacles)]

        for i in range(len(waypoints) - 1):
            A = (waypoints[i][0], waypoints[i][1])
            B = (waypoints[i + 1][0], waypoints[i + 1][1])

            for j, (Ao, bo) in enumerate(O):
                bottom_left = (bo[0][0], bo[2][0])
                bottom_right = (bo[1][0], bo[2][0])
                top_right = (bo[1][0], bo[3][0])
                top_left = (bo[0][0], bo[3][0])

                edges = [
                    (bottom_left, bottom_right),  # Bottom edge
                    (bottom_right, top_right),   # Right edge
                    (top_right, top_left),       # Top edge
                    (top_left, bottom_left)      # Left edge
                ]

                for C, D in edges:
                    if intersect(A, B, C, D):
                        obstacle_segments[j].append(i+1)
                        break

        ctx.dispose()
        return obstacle_segments




def example_bloat(i, alpha):
    return 0

#Example usage
waypoints = [
    (3.0, 2.5),  # Move up to avoid obstacle
    (3.0, 4.0),  # Continue right
]

O = [
    (
        np.array([[-1, 0], [1, 0], [0, -1], [0, 1]]),  # Example obstacle
        np.array([[-10], [50], [-39], [40]])*0.1
    )
]

# Define the waypoints for the path
path = [
    (0.5, 3.0),  # Start
    (1.5, 3.0),  # Move right
    (2, 3.0),  # Move up
    (3.0, 2.5),  # Move up to avoid obstacle
    (3.0, 4.0),  # Continue right
    (3.5, 4.5),  # Move up to avoid obstacle
    (4.0, 4.2),  # Move right
    (5.0, 4.4),  # Continue right
    (5.5, 4.5),  # Continue right
    (6.5, 4.5)   # Goal
]

obs, theta, goal = problem()

obstacle_segments = check_waypoints(path, obs, example_bloat, alpha=0)



if obstacle_segments:
    for i, segments in enumerate(obstacle_segments):
        if segments:
            print(f"Obstacle {i+1} {obs[i]} intersects with segments: {segments}")
else:
    print("No obstacle intersections found.")
