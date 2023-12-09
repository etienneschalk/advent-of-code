from advent_of_code.year_2023.year_2023_day_09 import (
    parse_text_input,
    predict_next_value_backward,
    predict_next_value_forward,
)

EXAMPLE_INPUT = """

0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45

"""


def test_year_2023_day_09_part_1():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)

    expected_predictions = [18, 28, 68]
    actual_predictions = [predict_next_value_forward(arr) for arr in parsed_input]

    assert actual_predictions == expected_predictions
    assert sum(actual_predictions) == 114
    ...


def test_year_2023_day_09_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)

    expected_predictions = [-3, 0, 5]
    actual_predictions = [predict_next_value_backward(arr) for arr in parsed_input]

    assert actual_predictions == expected_predictions
    assert sum(actual_predictions) == 2
    ...
