import pytest

from advent_of_code.common.store import ExampleInputsStore, ExpectedAnswersStore
from advent_of_code.y_2016.problem_201607 import AdventOfCodeProblem201607


@pytest.mark.integration
def test_integration_201607(expected_answers_2016: ExpectedAnswersStore):
    problem = AdventOfCodeProblem201607()
    assert problem.solve() == expected_answers_2016.retrieve(problem)


def test_problem_201607_part_1(example_inputs_2016: ExampleInputsStore):
    test_input = example_inputs_2016.retrieve(__file__, "example_inputs_part_1")
    aoc = AdventOfCodeProblem201607()
    assert aoc.solve_part_1(aoc.parse_text_input(test_input)) == 2


def test_problem_201607_part_2(example_inputs_2016: ExampleInputsStore):
    test_input = example_inputs_2016.retrieve(__file__, "example_inputs_part_2")
    aoc = AdventOfCodeProblem201607()
    assert aoc.solve_part_2(aoc.parse_text_input(test_input)) == 3
