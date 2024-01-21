import pytest

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

# TODO use /home/tselano/dev/advent-of-code/resources/advent_of_code/year_2023/expected_results_year_2023.json


@pytest.mark.integration
def test_integration_202301():
    assert AdventOfCodeProblem202301().solve() == {1: 54630, 2: 54770}


@pytest.mark.integration
def test_integration_202302():
    assert AdventOfCodeProblem202302().solve() == {1: 2061, 2: 72596}


@pytest.mark.integration
def test_integration_202303():
    assert AdventOfCodeProblem202303().solve() == {1: 529618, 2: 77509019}


@pytest.mark.integration
def test_integration_202304():
    assert AdventOfCodeProblem202304().solve() == {1: 23750, 2: 13261850}


@pytest.mark.integration
def test_integration_202305():
    assert AdventOfCodeProblem202305().solve() == {1: 323142486, 2: 79874951}


@pytest.mark.integration
def test_integration_202306():
    assert AdventOfCodeProblem202306().solve() == {1: 2269432, 2: 35865985}


@pytest.mark.integration
def test_integration_202307():
    assert AdventOfCodeProblem202307().solve() == {1: 252052080, 2: 252898370}


@pytest.mark.integration
def test_integration_202308():
    assert AdventOfCodeProblem202308().solve() == {1: 15871, 2: 11283670395017}


@pytest.mark.integration
def test_integration_202309():
    assert AdventOfCodeProblem202309().solve() == {1: 1884768153, 2: 1031}


@pytest.mark.integration
def test_integration_202310():
    assert AdventOfCodeProblem202310().solve() == {1: 6599, 2: 477}


@pytest.mark.integration
def test_integration_202311():
    assert AdventOfCodeProblem202311().solve() == {1: 9370588, 2: 746207878188}


@pytest.mark.integration
def test_integration_202312():
    assert AdventOfCodeProblem202312().solve() == {1: 7670, 2: 157383940585037}


@pytest.mark.integration
def test_integration_202313():
    assert AdventOfCodeProblem202313().solve() == {1: 34918, 2: 33054}


@pytest.mark.integration
def test_integration_202314():
    assert AdventOfCodeProblem202314().solve() == {1: 110677, 2: 90551}


@pytest.mark.integration
def test_integration_202315():
    assert AdventOfCodeProblem202315().solve() == {1: 514281, 2: 244199}


@pytest.mark.slow
@pytest.mark.integration
def test_integration_202316():
    assert AdventOfCodeProblem202316().solve() == {1: 7236, 2: 7521}


@pytest.mark.slow
@pytest.mark.integration
def test_integration_202317():
    assert AdventOfCodeProblem202317().solve() == {1: 1001, 2: 1197}


@pytest.mark.integration
def test_integration_202318():
    assert AdventOfCodeProblem202318().solve() == {1: 47139, 2: 173152345887206}


@pytest.mark.integration
def test_integration_202319():
    assert AdventOfCodeProblem202319().solve() == {1: 348378, 2: 121158073425385}


@pytest.mark.integration
def test_integration_202320():
    assert AdventOfCodeProblem202320().solve() == {1: 684125385, 2: 225872806380073}


@pytest.mark.slow
@pytest.mark.integration
def test_integration_202321():
    assert AdventOfCodeProblem202321().solve() == {1: 3740, 2: 620962518745459}


@pytest.mark.integration
def test_integration_202322():
    assert AdventOfCodeProblem202322().solve() == {1: 393, 2: 58440}


@pytest.mark.slow
@pytest.mark.integration
def test_integration_202323():
    assert AdventOfCodeProblem202323().solve() == {1: 1998, 2: 6434}


@pytest.mark.integration
def test_integration_202324():
    assert AdventOfCodeProblem202324().solve() == {1: 19523, 2: 566373506408017}


@pytest.mark.integration
def test_integration_202325():
    assert AdventOfCodeProblem202325().solve() == {
        1: 601310,
        2: "Part 2 of Day 25 is having solved all the 49 previous problems!",
    }
