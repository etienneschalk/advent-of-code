from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.year_2022.problem_202205 import (
    logic_part_1,
    logic_part_2,
    parse_text_input,
)


def test_problem_202205_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    procedure = parse_text_input(test_input)
    result = logic_part_1(procedure)
    assert result == "CMZ"


def test_problem_202205_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    procedure = parse_text_input(test_input)
    result = logic_part_2(procedure)
    assert result == "MCD"
