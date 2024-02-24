from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2022.problem_202201 import (
    compute_max_calories_part_1,
    compute_max_calories_part_2,
    parse_text_input,
)


def test_problem_202201_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = parse_text_input(test_input)
    assert compute_max_calories_part_1(parsed_input) == 24000


def test_problem_202201_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = parse_text_input(test_input)
    assert compute_max_calories_part_2(parsed_input) == 45000
