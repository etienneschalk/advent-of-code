from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2022.problem_202204 import (
    compute_fully_contained_count,
    compute_overlapping_count,
    parse_text_input,
    render_input_visualization,
)


def test_problem_202204_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)

    parsed_input = parse_text_input(test_input)
    expected_visualization = example_inputs.retrieve(
        __file__, "EXPECTED_VISUALIZATION"
    ).strip()
    visu = render_input_visualization(parsed_input)
    assert visu == expected_visualization

    expected_fully_contained_count = 2
    actual_fully_contained_count = compute_fully_contained_count(parsed_input)
    assert actual_fully_contained_count == expected_fully_contained_count


def test_problem_202204_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)

    parsed_input = parse_text_input(test_input)

    expected_overlapping_count = 4
    actual_overlapping_count = compute_overlapping_count(parsed_input)
    assert actual_overlapping_count == expected_overlapping_count
