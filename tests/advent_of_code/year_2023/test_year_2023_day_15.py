from advent_of_code.year_2023.year_2023_day_15 import (
    NORTH,
    compute_total_load,
    get_list_of_str,
    parse_text_input,
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


def test_year_2023_day_15_part_1():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    list_of_str = get_list_of_str(parsed_input, NORTH)
    total_load = compute_total_load(list_of_str)
    assert total_load == 136
    ...


def test_year_2023_day_15_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    ...
