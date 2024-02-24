import pytest

from advent_of_code.common.store import ExpectedAnswersStore
from advent_of_code.year_2023.year_2023_day_01 import AdventOfCodeProblem202301
from advent_of_code.year_2023.year_2023_day_02 import AdventOfCodeProblem202302
from advent_of_code.year_2023.year_2023_day_03 import AdventOfCodeProblem202303
from advent_of_code.year_2023.year_2023_day_04 import AdventOfCodeProblem202304
from advent_of_code.year_2023.year_2023_day_05 import AdventOfCodeProblem202305
from advent_of_code.year_2023.year_2023_day_06 import AdventOfCodeProblem202306
from advent_of_code.year_2023.year_2023_day_07 import AdventOfCodeProblem202307
from advent_of_code.year_2023.year_2023_day_08 import AdventOfCodeProblem202308
from advent_of_code.year_2023.year_2023_day_09 import AdventOfCodeProblem202309
from advent_of_code.year_2023.year_2023_day_10 import AdventOfCodeProblem202310
from advent_of_code.year_2023.year_2023_day_11 import AdventOfCodeProblem202311
from advent_of_code.year_2023.year_2023_day_12 import AdventOfCodeProblem202312
from advent_of_code.year_2023.year_2023_day_13 import AdventOfCodeProblem202313
from advent_of_code.year_2023.year_2023_day_14 import AdventOfCodeProblem202314
from advent_of_code.year_2023.year_2023_day_15 import AdventOfCodeProblem202315
from advent_of_code.year_2023.year_2023_day_16 import AdventOfCodeProblem202316
from advent_of_code.year_2023.year_2023_day_17 import AdventOfCodeProblem202317
from advent_of_code.year_2023.year_2023_day_18 import AdventOfCodeProblem202318
from advent_of_code.year_2023.year_2023_day_19 import AdventOfCodeProblem202319
from advent_of_code.year_2023.year_2023_day_20 import AdventOfCodeProblem202320
from advent_of_code.year_2023.year_2023_day_21 import AdventOfCodeProblem202321
from advent_of_code.year_2023.year_2023_day_22 import AdventOfCodeProblem202322
from advent_of_code.year_2023.year_2023_day_23 import AdventOfCodeProblem202323
from advent_of_code.year_2023.year_2023_day_24 import AdventOfCodeProblem202324
from advent_of_code.year_2023.year_2023_day_25 import AdventOfCodeProblem202325


@pytest.mark.integration
def test_integration_202301(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202301()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202302(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202302()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202303(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202303()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202304(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202304()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202305(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202305()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202306(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202306()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202307(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202307()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202308(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202308()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202309(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202309()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202310(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202310()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202311(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202311()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202312(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202312()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202313(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202313()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202314(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202314()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202315(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202315()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.slow
@pytest.mark.integration
def test_integration_202316(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202316()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.slow
@pytest.mark.integration
def test_integration_202317(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202317()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202318(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202318()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202319(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202319()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202320(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202320()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.slow
@pytest.mark.integration
def test_integration_202321(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202321()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202322(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202322()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.slow
@pytest.mark.integration
def test_integration_202323(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202323()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202324(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202324()
    assert problem.solve() == expected_answers.retrieve(problem)


@pytest.mark.integration
def test_integration_202325(expected_answers: ExpectedAnswersStore):
    problem = AdventOfCodeProblem202325()
    assert problem.solve() == expected_answers.retrieve(problem)
