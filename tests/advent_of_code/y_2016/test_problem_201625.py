import pytest

from advent_of_code.common.store import ExpectedAnswersStore
from advent_of_code.y_2016.problem_201625 import AdventOfCodeProblem201625


@pytest.mark.integration
def test_integration_201625(expected_answers_2016: ExpectedAnswersStore):
    problem = AdventOfCodeProblem201625()
    assert problem.solve() == expected_answers_2016.retrieve(problem)
