import queue

import numpy as np
from advent_of_code.year_2023.year_2023_day_22 import Brick, parse_text_input

EXAMPLE_INPUT = """

1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9

"""


def test_year_2023_day_22_part_1():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)

    # Bricks that are the closest to the ground have the most priority (low-leaning z)
    sorted_bricks = sorted(parsed_input, key=lambda b: b.rank)

    # The input is nice, no need to max min min max, positions are ordered.
    assert np.all(
        [
            np.all(sorted_brick.position[1] - sorted_brick.position[0] >= 0)
            for sorted_brick in sorted_bricks
        ]
    )

    xmax = max(max(coord[0] for coord in b.position) for b in parsed_input)
    ymax = max(max(coord[1] for coord in b.position) for b in parsed_input)
    heatmap_shape = (xmax + 1, ymax + 1)
    heatmap = np.zeros(heatmap_shape, dtype=int)

    for brick in sorted_bricks:
        pos = brick.position

        # shadow = footprint x and y wise (z = constant, the closest to the ground)
        # use heatmap to know if the brick can still fall
        dx = pos[1][0] - pos[0][0]
        dy = pos[1][1] - pos[0][1]

        shadow = np.zeros(heatmap_shape, dtype=int)

        if dx == 0 and dy == 0:
            shadow[pos[0][0], pos[0][1]] = 1
        elif dx == 0:
            x = pos[0][0]
            min_y = pos[0][1]
            shadow[x, min_y : min_y + dy] = 1
        elif dy == 0:
            y = pos[0][1]
            min_x = pos[0][0]
            shadow[min_x : min_x + dx, y] = 1
        brick.shadow = shadow

    # priority_queue = queue.PriorityQueue()
    # next_queue = queue.PriorityQueue()
    # for b in sorted_bricks:
    #     priority_queue.put(b)

    falling = [*sorted_bricks]
    max_iter = 100
    iter_count = 0
    while falling and iter_count < max_iter:
        iter_count += 1
        brick: Brick = falling.pop(0)

        pos = brick.position
        lowz = brick.lowest_z

        # Intersect shadow at min z with heatmap
        # If touch, update heatmap with max z
        # and stop making this brick fall.

        # continue falling until it cannot anymore

    # max_simu_step = 50
    # for i in range(max_simu_step):
    #     max_iter = 100
    #     iter_count = 0
    #     while not priority_queue.empty() and iter_count < max_iter:
    #         iter_count += 1
    #         brick: Brick = priority_queue.get()

    #         if brick.rank > 0:
    #             brick.position[0] -= np.array([0, 0, 1])
    #             brick.position[1] -= np.array([0, 0, 1])
    #             next_queue.add(brick)
    #         # TODO : after the brick is settled, fill the ground cube

    #     priority_queue.clear()
    #     priority_queue, next_queue = next_queue, priority_queue

    ...
    # First, run the simulation to make the bricks fall
    # The simulation is settled when state(n+1) == state(n)
    # "they won't go down any further"

    # In this first phase it seams simpler to run the simul from the ground
    # (make fall the closest bricks from the ground to make room for the ones above
    # to fall too)

    # In a second part, I assume some graph theory can be used
    # "Touching" bricks make the graph connex
    # If removing a brick make the graph not connex anymore, then it is dangerous
    # to remove it as it means that bricks above will fall.
    # "Touching" means that z2 = z1 + 1 (fall is vertical)
    # Only the z axis connectivity seams interesting, at first.
    ...


def test_year_2023_day_22_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    ...
