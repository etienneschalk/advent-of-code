from advent_of_code.year_2023.year_2023_day_13 import (
    find_number_of_cols_above_symmetry_axis,
    find_number_of_rows_above_symmetry_axis,
    parse_text_input,
    render_2d_data_array,
    summarize_pattern_notes,
)

EXAMPLE_INPUT = """

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

"""

EXAMPLE_PROBLEMATIC = """

#......#...
.#.#.##....
##..####.##
...##....##
..#...##...
#..#.......
##..#.#..##
###..#.####
###..#.#.##

"""


def test_year_2023_day_13_part_1_problematic():
    test_input = EXAMPLE_PROBLEMATIC
    pattern = parse_text_input(test_input)[0]

    # Vertical symmetry
    assert find_number_of_rows_above_symmetry_axis(pattern.T, "col", "row") == 10
    assert find_number_of_cols_above_symmetry_axis(pattern) == 10

    # Horizontal symmetry
    assert find_number_of_rows_above_symmetry_axis(pattern) == 0


def test_year_2023_day_13_part_1():
    test_input = EXAMPLE_INPUT
    patterns = parse_text_input(test_input)

    example_1, example_2 = patterns

    print(render_2d_data_array(example_1))
    print(render_2d_data_array(example_2))

    # Vertical symmetry
    assert (
        find_number_of_rows_above_symmetry_axis(
            example_1.T.rename({"col": "row", "row": "col"})
        )
        == 5
    )
    assert (
        find_number_of_rows_above_symmetry_axis(
            example_2.T.rename({"col": "row", "row": "col"})
        )
        == 0
    )
    assert find_number_of_cols_above_symmetry_axis(example_1) == 5
    assert find_number_of_cols_above_symmetry_axis(example_2) == 0

    # Horizontal symmetry
    assert find_number_of_rows_above_symmetry_axis(example_1) == 0
    assert find_number_of_rows_above_symmetry_axis(example_2) == 4

    assert summarize_pattern_notes(patterns) == 405
    ...


def test_year_2023_day_13_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    ...
