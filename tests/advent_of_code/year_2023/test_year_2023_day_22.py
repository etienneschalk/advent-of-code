from collections import defaultdict
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
    unsorted_bricks = parse_text_input(test_input)

    # Bricks that are the closest to the ground have the most priority (low-leaning z)
    sorted_bricks = sorted(unsorted_bricks, key=lambda b: b.rank)

    # The input is nice, no need to max min min max, positions are ordered.
    assert np.all(
        [
            np.all(sorted_brick.pos1 - sorted_brick.pos0 >= 0)
            for sorted_brick in sorted_bricks
        ]
    )

    xmax = max(max(b.x0, b.x1) for b in unsorted_bricks)
    ymax = max(max(b.y0, b.y1) for b in unsorted_bricks)
    zmax = max(max(b.z0, b.z1) for b in unsorted_bricks)
    heatmap_shape = (xmax + 1, ymax + 1)
    heatmap = np.zeros(heatmap_shape, dtype=int)

    # Create shadows of all bricks (projection along the z axis)
    fallen_bricks = []
    for idx, brick in enumerate(sorted_bricks, 1):
        # shadow = footprint x and y wise (z = constant, the closest to the ground)
        # use heatmap to know if the brick can still fall

        # Only use the x and y parts of the indexer for the heatmap
        indexer = brick.indexer[:2]
        peak = np.max(heatmap[indexer])
        new_peak = peak + brick.height
        heatmap[indexer] = new_peak
        dz = brick.z1 - new_peak
        dpos = np.array((0, 0, dz))
        fallen_position = (brick.pos0 - dpos, brick.pos1 - dpos)
        fallen_brick = Brick(
            position=fallen_position,
            falling=False,
            identifier=idx,
        )
        fallen_bricks.append(fallen_brick)
    # priority_queue = queue.PriorityQueue()
    # next_queue = queue.PriorityQueue()
    # for b in sorted_bricks:
    #     priority_queue.put(b)

    xmax = max(max(b.x0, b.x1) for b in fallen_bricks)
    ymax = max(max(b.y0, b.y1) for b in fallen_bricks)
    zmax = max(max(b.z0, b.z1) for b in fallen_bricks)
    # space_shape = (xmax + 1, ymax + 1, zmax + 1)
    space_shape = (xmax + 1, ymax + 1, zmax + 2)
    space = np.zeros(space_shape, dtype=int)
    for fallen_brick in fallen_bricks:
        space[fallen_brick.indexer] = fallen_brick.identifier
    assert np.all(
        space
        == np.array(
            [
                [
                    [0, 0, 2, 4, 0, 0, 0, 0],
                    [0, 0, 0, 4, 6, 0, 0, 0],
                    [0, 0, 3, 4, 0, 0, 0, 0],
                ],
                [
                    [0, 1, 2, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 6, 7, 7, 0],
                    [0, 1, 3, 0, 0, 0, 0, 0],
                ],
                [
                    [0, 0, 2, 5, 0, 0, 0, 0],
                    [0, 0, 0, 5, 6, 0, 0, 0],
                    [0, 0, 3, 5, 0, 0, 0, 0],
                ],
            ]
        )
    )

    # Write a function that compute this from space
    expected_supported = {
        1: (2, 3),
        2: (4, 5),
        3: (4, 5),
        4: (6,),
        5: (6,),
        6: (7,),
        7: (),
    }
    actual_supported: dict[int, tuple[int, ...]] = {}
    for fallen_brick in fallen_bricks:
        xx, yy, zz = fallen_brick.indexer
        if isinstance(zz, slice):
            # new_zz = slice(zz.start + 1, zz.stop + dz)
            new_zz = zz.stop
        else:  # zz is an int
            new_zz = zz + 1
        just_above_indexer = (xx, yy, new_zz)
        just_above = space[just_above_indexer]
        supported = tuple(np.unique(just_above[just_above > 0]))
        actual_supported[fallen_brick.identifier] = supported
        ...
    assert actual_supported == expected_supported
    expected_support_counts = defaultdict(int)
    for brick_id, supported_bricks_ids in expected_supported.items():
        for supported_brick_id in supported_bricks_ids:
            expected_support_counts[supported_brick_id] += 1
    # Unsafe when support_count == 1 (it means one support only)
    assert expected_support_counts == {2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 1}
    # Note: brick 1 (A) is not in the list, the ground supports it
    ...
    can_be_disintegrated = {
        brick_id: any(
            expected_support_counts[sb_id] > 1 for sb_id in supported_bricks_ids
        )
        or not supported_bricks_ids
        for brick_id, supported_bricks_ids in expected_supported.items()
    }

    assert can_be_disintegrated == {
        1: False,
        2: True,
        3: True,
        4: True,
        5: True,
        6: False,
        7: True,
    }

    # Done - now refactor
    falling = [*sorted_bricks]
    max_iter = 100
    iter_count = 0
    while falling and iter_count < max_iter:
        iter_count += 1
        brick: Brick = falling.pop(0)

        heatmap += brick.shadow * brick.height

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
