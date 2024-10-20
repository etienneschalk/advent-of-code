import ast

import pytest

from advent_of_code.common.store import ExampleInputsStore, ExpectedAnswersStore
from advent_of_code.y_2016.problem_201609 import AdventOfCodeProblem201609


@pytest.mark.integration
def test_integration_201609(expected_answers_2016: ExpectedAnswersStore):
    problem = AdventOfCodeProblem201609()
    assert problem.solve() == expected_answers_2016.retrieve(problem)


def test_problem_201609_part_1(example_inputs_2016: ExampleInputsStore):
    problem = AdventOfCodeProblem201609()
    example_inputs = example_inputs_2016.retrieve(__file__, "example_inputs_1")
    example_inputs = ast.literal_eval(example_inputs)
    for input, expected_output in example_inputs.items():
        actual_output_len = problem.solve_part_1(problem.parse_text_input(input))
        assert actual_output_len == len(expected_output)


def test_problem_201609_part_2(example_inputs_2016: ExampleInputsStore):
    problem = AdventOfCodeProblem201609()
    example_inputs = example_inputs_2016.retrieve(__file__, "example_inputs_2")
    example_inputs = ast.literal_eval(example_inputs)
    for input, expected_output in example_inputs.items():
        actual_output = problem.solve_part_2(problem.parse_text_input(input))
        assert actual_output == expected_output
