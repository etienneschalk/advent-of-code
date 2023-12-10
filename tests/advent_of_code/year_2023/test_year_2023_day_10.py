from advent_of_code.year_2023.year_2023_day_10 import (
    logic_part_1,
    parse_text_input,
    render_pipes,
)

EXAMPLE_INPUT_1_1 = """
.....
.F-7.
.|.|.
.L-J.
.....
"""
EXAMPLE_INPUT_1_2 = """
.....
.S-7.
.|.|.
.L-J.
.....
"""
EXAMPLE_INPUT_1_3 = """
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""

EXAMPLE_INPUT_2_1 = """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""
EXAMPLE_INPUT_2_2 = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""

EXAMPLE_DISTANCES_1 = """
.....
.012.
.1.3.
.234.
.....
"""
EXAMPLE_DISTANCES_2 = """
..45.
.236.
01.78
14567
23...
"""


def test_year_2023_day_10_part_1():
    test_inputs = (
        EXAMPLE_INPUT_1_1,
        EXAMPLE_INPUT_1_2,
        EXAMPLE_INPUT_1_3,
        EXAMPLE_INPUT_2_1,
        EXAMPLE_INPUT_2_2,
    )
    expected = EXAMPLE_DISTANCES_1, EXAMPLE_DISTANCES_2
    parsed_inputs = [parse_text_input(test_input) for test_input in test_inputs]
    for p in parsed_inputs:
        print(render_pipes(p))

    result = logic_part_1(parsed_inputs[1])
    assert result == 4

    result = logic_part_1(parsed_inputs[2])
    assert result == 4

    result = logic_part_1(parsed_inputs[3])

    assert result == 8
    result = logic_part_1(parsed_inputs[4])
    assert result == 8
    ...


def test_year_2023_day_10_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
