import pytest

from advent_of_code.common.store import ExpectedAnswersStore
from advent_of_code.y_2016.problem_201603 import AdventOfCodeProblem201603


@pytest.mark.integration
def test_integration_201603(expected_answers_2016: ExpectedAnswersStore):
    problem = AdventOfCodeProblem201603()
    assert problem.solve() == expected_answers_2016.retrieve(problem)


def test_problem_202203_part_1():
    parsed = AdventOfCodeProblem201603.parse_text_input("5 10 25")
    assert parsed == [[5, 10, 25]]
    result = AdventOfCodeProblem201603().solve_part_1(parsed)
    assert result == 0
