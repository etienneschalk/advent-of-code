import pytest

from advent_of_code.common.store import ExampleInputsStore, ExpectedAnswersStore
from advent_of_code.y_2016.problem_201610 import AdventOfCodeProblem201610


@pytest.mark.integration
def test_integration_201610(expected_answers_2016: ExpectedAnswersStore):
    problem = AdventOfCodeProblem201610()
    assert problem.solve() == expected_answers_2016.retrieve(problem)


def test_problem_201610_part_1(example_inputs_2016: ExampleInputsStore):
    problem = AdventOfCodeProblem201610()
    example_input = example_inputs_2016.retrieve(__file__, "example_input")
    puzzle_input = problem.parse_text_input(example_input)

    wanted_low_value = 2
    wanted_high_value = 5
    assert (
        problem.solve_internal(puzzle_input, wanted_low_value, wanted_high_value, 1)
        == 2
    )


def test_problem_201610_part_2(example_inputs_2016: ExampleInputsStore):
    problem = AdventOfCodeProblem201610()
    example_input = example_inputs_2016.retrieve(__file__, "example_input")
    puzzle_input = problem.parse_text_input(example_input)

    wanted_low_value = 2
    wanted_high_value = 61
    return (
        problem.solve_internal(puzzle_input, wanted_low_value, wanted_high_value, 2)
        == 5 * 2 * 3
    )
