from advent_of_code.year_2023.year_2023_day_15 import (
    compute_total_load,
    get_list_of_str,
    parse_text_input,
    run_one_full_cycle,
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


def test_year_2023_day_15_part_2_more_iter():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)

    expected_1 = EXPECTED_PART_2_1_CYCLE.strip().split("\n")
    expected_2 = EXPECTED_PART_2_2_CYCLE.strip().split("\n")
    expected_3 = EXPECTED_PART_2_3_CYCLE.strip().split("\n")
    init_rot = 4

    max_iter = 32
    state = parsed_input
    state_history = [state]
    for i in range(max_iter):
        state = run_one_full_cycle(state, init_rot)
        state_history.append(state.flatten().tostring())

    # Period of T=7 does appear at some point
    empirical_period = 7  # by reading the state_history
    assert state_history[8] != state_history[8 - empirical_period]
    assert state_history[9] != state_history[9 - empirical_period]
    assert state_history[10] == state_history[10 - empirical_period]
    for k in range(10, 32):
        assert state_history[k] == state_history[k - empirical_period]
    ...
