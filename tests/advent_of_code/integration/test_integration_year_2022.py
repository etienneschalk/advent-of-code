import pytest

from advent_of_code.common.store import ExpectedAnswersStore
from advent_of_code.year_2022.year_2022_day_01 import AdventOfCodeProblem202201
from advent_of_code.year_2022.year_2022_day_02 import AdventOfCodeProblem202202
from advent_of_code.year_2022.year_2022_day_03 import AdventOfCodeProblem202203
from advent_of_code.year_2022.year_2022_day_04 import AdventOfCodeProblem202204
from advent_of_code.year_2022.year_2022_day_05 import AdventOfCodeProblem202205
from advent_of_code.year_2022.year_2022_day_25 import AdventOfCodeProblem202225


@pytest.mark.integration
def test_integration_202201(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202201()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202202(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202202()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202203(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202203()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202204(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202204()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202205(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202205()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202225(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202225()
    assert problem.solve() == expected_answers.retrieve(problem)
