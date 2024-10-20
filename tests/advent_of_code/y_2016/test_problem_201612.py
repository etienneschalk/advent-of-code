import pytest

from advent_of_code.common.store import ExampleInputsStore, ExpectedAnswersStore
from advent_of_code.y_2016.problem_201612 import AdventOfCodeProblem201612


@pytest.mark.integration
def test_integration_201612(expected_answers_2016: ExpectedAnswersStore):
    problem = AdventOfCodeProblem201612()
    assert problem.solve() == expected_answers_2016.retrieve(problem)


def test_problem_201612_part_1(example_inputs_2016: ExampleInputsStore):
    problem = AdventOfCodeProblem201612()
    example_input = example_inputs_2016.retrieve(__file__, "example_input")
    puzzle_input = problem.parse_text_input(example_input)
    assert problem.solve_part_1(puzzle_input) == 42


def test_problem_201612_part_2(example_inputs_2016: ExampleInputsStore):
    pass  # no example given for part 2
