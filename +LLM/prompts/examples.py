def full_path_ex():
    return """
## Example
### Provided Data
Start Position (Quadrilateral): Defined by the clockwise coordinates of its four vertices [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = [[1.0, 1.0], [0.0, 1.0], [0.0, 0.0], [1.0, 0.0]]
    Note: You can choose any point within this Quadrilateral to start the path.
Goal Position (Quadrilateral): Defined by the clockwise coordinates of its four vertices [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = [[5.0, 5.0], [4.0, 5.0], [4.0, 4.0], [5.0, 4.0]]
    Note: You can choose any point within this Quadrilateral to end the path.
Obstacles (Quadrilaterals): Each obstacle is defined by the clockwise coordinates of its four vertices [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]:
    Obstacle 1: [[3.5, 5.0], [3.0, 5.0], [3.0, 0.0], [3.5, 0.0]]
    Obstacle 2: [[7.0, 6.0], [3.0, 6.0], [3.0, 5.5], [7.0, 5.5]]
    Obstacle 3: [[7.0, 0.0], [3.0, 0.0], [3.0, -1.0], [7.0, -1.0]]
### Example Response
There is a horizontal gap between obstacles 1 and 2. The path can be planned to move through this gap.
{...Further Analysis of the Environment and its spatial relationships}

new_path = [
    (0.5, 0.5), # start in the start set
    (0.0, 5.25), # move upwards to get on the level as the gap and avoid touching Obstacle 1 by adding 0.25 to the y-coordinate
    (3.75, 5.25), # move rightwards to reach the gap
    (4.5, 4.5) # move downwards to end in the goal set
]
"""
