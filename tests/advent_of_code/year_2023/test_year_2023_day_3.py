from advent_of_code.year_2023.year_2023_day_3 import (
    compute_adjacent_numbers,
    parse_text_input,
)

EXAMPLE_INPUT = """

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

"""


def test_year_2023_day_2_part_1():
    test_input = EXAMPLE_INPUT
    array = parse_text_input(test_input)

    flattened = compute_adjacent_numbers(array)
    assert flattened == [467, 35, 633, 617, 592, 755, 664, 598]
    assert 114 not in flattened
    assert 58 not in flattened
    assert sum(flattened) == 4361

    ...


def test_year_2023_day_2_part_2():
    ...
    # test_input = EXAMPLE_INPUT
    # games = parse_text_input(test_input)
