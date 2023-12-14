import numpy as np
from advent_of_code.year_2023.year_2023_day_15 import (
    compute_total_load,
    get_list_of_str,
    parse_text_input,
    update_state,
)

EXAMPLE_INPUT = """

O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....

"""

EXPECTED_PART_2_1_CYCLE = """

.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....

"""

EXPECTED_PART_2_2_CYCLE = """

.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O

"""
EXPECTED_PART_2_3_CYCLE = """

.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O

"""


def test_year_2023_day_15_part_1():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    list_of_str = get_list_of_str(parsed_input, 3)
    total_load = compute_total_load(list_of_str)
    assert total_load == 136
    ...


def test_year_2023_day_15_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)

    expected_1 = EXPECTED_PART_2_1_CYCLE.strip().split("\n")
    expected_2 = EXPECTED_PART_2_2_CYCLE.strip().split("\n")
    expected_3 = EXPECTED_PART_2_3_CYCLE.strip().split("\n")
    init_rot = 4

    after_one_cycle = run_one_full_cycle(parsed_input, init_rot)
    assert get_list_of_str(after_one_cycle, 0) == expected_1
    after_two_cycles = run_one_full_cycle(after_one_cycle, init_rot)
    assert get_list_of_str(after_two_cycles, 0) == expected_2
    after_three_cycles = run_one_full_cycle(after_two_cycles, init_rot)
    assert get_list_of_str(after_three_cycles, 0) == expected_3
    ...


def run_one_full_cycle(parsed_input: np.ndarray, rot: int) -> np.ndarray:
    # North (initial starting rot = 3)
    rot -= 1
    list_of_str = get_list_of_str(parsed_input, rot)
    next_arr = update_state(list_of_str)
    next_arr = np.rot90(next_arr, 4 - rot)

    # West
    rot -= 1
    list_of_str = get_list_of_str(next_arr, rot)
    next_arr = update_state(list_of_str)
    next_arr = np.rot90(next_arr, 4 - rot)

    # South
    rot -= 1
    list_of_str = get_list_of_str(next_arr, rot)
    next_arr = update_state(list_of_str)
    next_arr = np.rot90(next_arr, 4 - rot)

    # East
    rot -= 1
    list_of_str = get_list_of_str(next_arr, rot)
    next_arr = update_state(list_of_str)
    next_arr = np.rot90(next_arr, 4 - rot)

    return next_arr
