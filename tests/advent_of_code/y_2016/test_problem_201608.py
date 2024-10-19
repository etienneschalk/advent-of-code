import pytest

from advent_of_code.common.store import ExpectedAnswersStore
from advent_of_code.y_2016.problem_201608 import AdventOfCodeProblem201608


@pytest.mark.integration
def test_integration_201608(expected_answers_2016: ExpectedAnswersStore):
    problem = AdventOfCodeProblem201608()
    assert problem.solve() == expected_answers_2016.retrieve(problem)
