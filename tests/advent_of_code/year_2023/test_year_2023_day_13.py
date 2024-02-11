from advent_of_code.common.common import render_2d_data_array
from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.year_2023.year_2023_day_13 import (
    find_number_of_cols_above_symmetry_axis,
    find_number_of_rows_above_symmetry_axis,
    parse_text_input,
    summarize_pattern_notes,
)


def test_year_2023_day_13_part_1_problematic(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__, "EXAMPLE_PROBLEMATIC")
    pattern = parse_text_input(test_input)[0]

    # Vertical symmetry
    assert find_number_of_cols_above_symmetry_axis(pattern) == 10

    # Horizontal symmetry
    assert find_number_of_rows_above_symmetry_axis(pattern) == 0


def test_year_2023_day_13_part_2_problematic(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__, "EXAMPLE_PROBLEMATIC")
    pattern = parse_text_input(test_input)[0]

    # Vertical symmetry
    assert find_number_of_cols_above_symmetry_axis(pattern) == 10

    # Horizontal symmetry
    assert find_number_of_rows_above_symmetry_axis(pattern) == 0


def test_year_2023_day_13_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
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


def test_year_2023_day_13_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    patterns = parse_text_input(test_input)

    example_1, example_2 = patterns

    print(render_2d_data_array(example_1))
    print(render_2d_data_array(example_2))

    # Vertical symmetry
    # Old symmetry disappeared
    assert find_number_of_cols_above_symmetry_axis(example_1, smudge_mode=True) == 0
    # No change, there was no symmetry
    assert find_number_of_cols_above_symmetry_axis(example_2, smudge_mode=True) == 0

    # Horizontal symmetry
    # New expected symmetries
    # 0 -> 3
    assert find_number_of_rows_above_symmetry_axis(example_1, smudge_mode=True) == 3
    # 4 -> 1
    assert find_number_of_rows_above_symmetry_axis(example_2, smudge_mode=True) == 1

    # Change: 405 -> 400
    assert summarize_pattern_notes(patterns, smudge_mode=True) == 400
    ...
