from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.year_2023.problem_202309 import (
    AdventOfCodeProblem202309,
    predict_next_value_backward,
    predict_next_value_forward,
)


def test_problem_202309_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = AdventOfCodeProblem202309.parse_text_input(test_input)

    expected_predictions = [18, 28, 68]
    actual_predictions = [predict_next_value_forward(arr) for arr in parsed_input]

    assert actual_predictions == expected_predictions
    assert sum(actual_predictions) == 114
    ...


def test_problem_202309_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = AdventOfCodeProblem202309.parse_text_input(test_input)

    expected_predictions = [-3, 0, 5]
    actual_predictions = [predict_next_value_backward(arr) for arr in parsed_input]

    assert actual_predictions == expected_predictions
    assert sum(actual_predictions) == 2
    ...
