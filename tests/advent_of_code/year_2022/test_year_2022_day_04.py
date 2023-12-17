from advent_of_code.year_2022.year_2022_day_04 import (
    compute_fully_contained_count,
    compute_overlapping_count,
    parse_text_input,
    render_input_visualization,
)

EXAMPLE_INPUT = """

2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8

"""

EXPECTED_VISUALIZATION = """

.234.....  2-4
.....678.  6-8

.23......  2-3
...45....  4-5

....567..  5-7
......789  7-9

.2345678.  2-8
..34567..  3-7

.....6...  6-6
...456...  4-6

.23456...  2-6
...45678.  4-8

"""


def test_year_2022_day_04_part_1():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)

    visu = render_input_visualization(parsed_input)
    assert visu == EXPECTED_VISUALIZATION.strip()

    expected_fully_contained_count = 2
    actual_fully_contained_count = compute_fully_contained_count(parsed_input)
    assert actual_fully_contained_count == expected_fully_contained_count


def test_year_2022_day_04_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)

    expected_overlapping_count = 4
    actual_overlapping_count = compute_overlapping_count(parsed_input)
    assert actual_overlapping_count == expected_overlapping_count
