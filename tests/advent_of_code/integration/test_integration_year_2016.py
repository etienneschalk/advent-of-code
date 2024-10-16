import pytest

from advent_of_code.common.store import ExpectedAnswersStore
from advent_of_code.y_2016.problem_201601 import AdventOfCodeProblem201601
from advent_of_code.y_2016.problem_201602 import AdventOfCodeProblem201602
from advent_of_code.y_2016.problem_201606 import AdventOfCodeProblem201606


@pytest.mark.integration
def test_integration_201601(expected_answers_2016: ExpectedAnswersStore):
    problem = AdventOfCodeProblem201601()
    assert problem.solve() == expected_answers_2016.retrieve(problem)


@pytest.mark.integration
def test_integration_201602(expected_answers_2016: ExpectedAnswersStore):
    problem = AdventOfCodeProblem201602()
    assert problem.solve() == expected_answers_2016.retrieve(problem)


@pytest.mark.integration
def test_integration_201606(expected_answers_2016: ExpectedAnswersStore):
    problem = AdventOfCodeProblem201606()
    assert problem.solve() == expected_answers_2016.retrieve(problem)
