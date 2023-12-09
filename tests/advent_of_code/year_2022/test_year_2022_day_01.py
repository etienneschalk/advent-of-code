from advent_of_code.year_2022.year_2022_day_01 import (
    compute_max_calories_part_1,
    compute_max_calories_part_2,
    parse_text_input,
)

EXAMPLE_INPUT = """

1000
2000
3000

4000

5000
6000

7000
8000
9000

10000

"""


def test_year_2022_day_01_part_1():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    assert compute_max_calories_part_1(parsed_input) == 24000


def test_year_2022_day_01_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    assert compute_max_calories_part_2(parsed_input) == 45000
