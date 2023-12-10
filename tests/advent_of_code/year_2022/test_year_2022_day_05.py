from advent_of_code.year_2022.year_2022_day_05 import (
    logic_part_1,
    logic_part_2,
    parse_text_input,
)

EXAMPLE_INPUT = """

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2

"""


def test_year_2022_day_05_part_1():
    test_input = EXAMPLE_INPUT
    procedure = parse_text_input(test_input)
    result = logic_part_1(procedure)
    assert result == "CMZ"


def test_year_2022_day_05_part_2():
    test_input = EXAMPLE_INPUT
    procedure = parse_text_input(test_input)
    result = logic_part_2(procedure)
    assert result == "MCD"
