import pytest

from advent_of_code.common.store import ExampleInputsStore, ExpectedAnswersStore
from advent_of_code.y_2016.problem_201602 import AdventOfCodeProblem201602


@pytest.mark.integration
def test_integration_201602(expected_answers_2016: ExpectedAnswersStore):
    problem = AdventOfCodeProblem201602()
    assert problem.solve() == expected_answers_2016.retrieve(problem)


def test_problem_202201_part_1(example_inputs_2016: ExampleInputsStore):
    example_input = example_inputs_2016.retrieve(__file__, "example_input")
    # 1 2 3
    # 4 5 6
    # 7 8 9
    result = AdventOfCodeProblem201602().solve_part_1(example_input)
    assert result == "1985"


def test_problem_202201_part_2(example_inputs_2016: ExampleInputsStore):
    example_input = example_inputs_2016.retrieve(__file__, "example_input")
    #     1
    #   2 3 4
    # 5 6 7 8 9
    #   A B C
    #     D
    result = AdventOfCodeProblem201602().solve_part_2(example_input)
    assert result == "5DB3"
