import numpy as np

from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2023.problem_202322 import (
    compute_disintegrable_bricks,
    compute_fallen_bricks,
    compute_safely_removable_bricks_count,
    compute_support_counts,
    compute_supported_bricks,
    create_elevation_map,
    create_space_datacuboid,
    fill_space_with_bricks_identifiers,
    parse_text_input,
    solve_part_2,
)

EXPECTED_SPACE_PART_1 = np.array(
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

EXPECTED_SUPPORTED_BRICKS_PART_1 = {
    1: (2, 3),
    2: (4, 5),
    3: (4, 5),
    4: (6,),
    5: (6,),
    6: (7,),
    7: (),
}
EXPECTED_SUPPORT_COUNTS_PART_1 = {2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 1}
EXPECTED_CAN_BE_DISINTEGRATED_PART_1 = {
    1: False,
    2: True,
    3: True,
    4: True,
    5: True,
    6: False,
    7: True,
}


def test_problem_202322_part_1_whole(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    unsorted_bricks = parse_text_input(test_input)

    result = compute_safely_removable_bricks_count(unsorted_bricks)

    assert result == 5


def test_problem_202322_part_1_details(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    unsorted_bricks = parse_text_input(test_input)

    # Bricks that are the closest to the ground have the most priority (low-leaning z)
    sorted_bricks = sorted(unsorted_bricks, key=lambda b: b.rank)

    # The input is well-formed, no need to max min min max, positions are ordered.
    assert np.all([sorted_brick.is_position_ordered for sorted_brick in sorted_bricks])

    elevation_map = create_elevation_map(sorted_bricks)

    fallen_bricks = compute_fallen_bricks(sorted_bricks, elevation_map)

    space = create_space_datacuboid(fallen_bricks)

    fill_space_with_bricks_identifiers(fallen_bricks, space)

    assert np.all(space == EXPECTED_SPACE_PART_1)

    supported_bricks = compute_supported_bricks(fallen_bricks, space)

    assert supported_bricks == EXPECTED_SUPPORTED_BRICKS_PART_1

    support_counts = compute_support_counts(supported_bricks)

    # Unsafe when support_count == 1 (it means one support only)
    # Note: brick 1 (A) is not in the list, the ground supports it
    assert support_counts == EXPECTED_SUPPORT_COUNTS_PART_1

    can_be_disintegrated = compute_disintegrable_bricks(
        supported_bricks, support_counts
    )

    assert can_be_disintegrated == EXPECTED_CAN_BE_DISINTEGRATED_PART_1

    safely_removable_bricks = sum(can_be_disintegrated.values())

    assert safely_removable_bricks == 5


def test_problem_202322_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    unsorted_bricks = parse_text_input(test_input)
    # Bricks that are the closest to the ground have the most priority (low-leaning z)
    sorted_bricks = sorted(unsorted_bricks, key=lambda b: b.rank)

    # The input is well-formed, no need to max min min max, positions are ordered.
    assert np.all([sorted_brick.is_position_ordered for sorted_brick in sorted_bricks])

    elevation_map = create_elevation_map(sorted_bricks)

    fallen_bricks = compute_fallen_bricks(sorted_bricks, elevation_map)

    space = create_space_datacuboid(fallen_bricks)

    fill_space_with_bricks_identifiers(fallen_bricks, space)

    assert np.all(space == EXPECTED_SPACE_PART_1)

    supported_bricks = compute_supported_bricks(fallen_bricks, space)

    assert supported_bricks == EXPECTED_SUPPORTED_BRICKS_PART_1

    support_counts = compute_support_counts(supported_bricks)

    # Unsafe when support_count == 1 (it means one support only)
    # Note: brick 1 (A) is not in the list, the ground supports it
    assert support_counts == EXPECTED_SUPPORT_COUNTS_PART_1

    can_be_disintegrated = compute_disintegrable_bricks(
        supported_bricks, support_counts
    )

    assert can_be_disintegrated == EXPECTED_CAN_BE_DISINTEGRATED_PART_1

    safely_removable_bricks = sum(can_be_disintegrated.values())

    assert safely_removable_bricks == 5

    result = solve_part_2(supported_bricks, support_counts, True)

    assert result == 7
