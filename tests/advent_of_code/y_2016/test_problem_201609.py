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
    example_inputs = example_inputs_2016.retrieve(__file__, "example_inputs")
    example_inputs = ast.literal_eval(example_inputs)
    for input, expected_output in example_inputs.items():
        actual_output = problem.solve_part_1_internal(problem.parse_text_input(input))
        assert actual_output == expected_output


def test_problem_201609_part_2(example_inputs_2016: ExampleInputsStore):
    problem = AdventOfCodeProblem201609()
    example_inputs = {
        # "(3x3)XYZ": len("XYZXYZXYZ"),
        # "X(8x2)(3x3)ABCY": len("XABCABCABCABCABCABCY"),
        # "(27x12)(20x12)(13x14)(7x10)(1x12)A": 241920,
        "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN": 445,
    }
    for input, expected_output in example_inputs.items():
        print("------------")
        actual_output = problem.solve_part_2_internal(problem.parse_text_input(input))
        print(input, expected_output, actual_output)
        assert actual_output == expected_output
