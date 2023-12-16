from advent_of_code.year_2023.year_2023_day_16 import (
    do_part_1,
    parse_text_input,
    render_parsed_input,
)

EXAMPLE_INPUT = r"""

.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....


"""


def test_year_2023_day_16_part_1():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    print()
    print(render_parsed_input(parsed_input))
    assert do_part_1(parsed_input) == 46
    ...


def test_year_2023_day_16_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    ...
