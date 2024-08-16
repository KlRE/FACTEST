def full_path_ex():
    return ""
    return """
## Example
### Provided Data
Start Position (Rectangular Set): (xmin, xmax, ymin, ymax) = (0.0, 1.0, 0.0, 1.0)
    Note: You can choose any point within this rectangle to start the path.
Goal Position (Rectangular Set): (xmin, xmax, ymin, ymax) = (4.0, 5.0, 4.0, 5.0)
    Note: You can choose any point within this rectangle to end the path.
Obstacles (Rectangular Sets): (xmin, xmax, ymin, ymax):
    obstacles = [
        (3.0, 3.5, 0.0, 5.0),   # Obstacle 1
        (3.0, 7.0, 5.5, 6.0),   # Obstacle 2
        (3.0, 7.0, -1.0, 0.0),   # Obstacle 3
    ]
### Example Response
    There is a horizontal gap between obstacles 1 and 2. The path can be planned to move through this gap.
    new_path = [
        (0.5, 0.5), # start in the start set
        (0.0, 5.25), # move upwards to get on the level as the gap and avoid touching Obstacle 1 by adding 0.25 to the y-coordinate
        (3.75, 5.25), # move rightwards to reach the gap
        (4.5, 4.5) # move downwards to end in the goal set
    ]
"""
