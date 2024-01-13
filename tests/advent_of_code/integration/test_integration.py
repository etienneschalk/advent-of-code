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
from advent_of_code.year_2023.year_2023_day_13 import AdventOfCodeProblem202313
from advent_of_code.year_2023.year_2023_day_15 import AdventOfCodeProblem202315
from advent_of_code.year_2023.year_2023_day_18 import AdventOfCodeProblem202318
from advent_of_code.year_2023.year_2023_day_20 import AdventOfCodeProblem202320

# Bash:
# pytest --with-integration -k integration


@pytest.mark.integration
def test_integration_year_2023():
    assert AdventOfCodeProblem202301().solve_all() == {1: 54630, 2: 54770}
    assert AdventOfCodeProblem202302().solve_all() == {1: 2061, 2: 72596}
    assert AdventOfCodeProblem202303().solve_all() == {1: 529618, 2: 77509019}
    assert AdventOfCodeProblem202304().solve_all() == {1: 23750, 2: 13261850}
    assert AdventOfCodeProblem202305().solve_all() == {1: 323142486, 2: 79874951}
    assert AdventOfCodeProblem202306().solve_all() == {1: 2269432, 2: 35865985}
    assert AdventOfCodeProblem202307().solve_all() == {1: 252052080, 2: 252898370}
    assert AdventOfCodeProblem202308().solve_all() == {1: 15871, 2: 11283670395017}
    assert AdventOfCodeProblem202309().solve_all() == {1: 1884768153, 2: 1031}
    assert AdventOfCodeProblem202310().solve_all() == {1: 6599, 2: 477}
    assert AdventOfCodeProblem202311().solve_all() == {1: 9370588, 2: 746207878188}
    # assert AdventOfCodeProblem202312().solve_all() == {1: TODO, 2: TODO}
    assert AdventOfCodeProblem202313().solve_all() == {1: 34918, 2: 33054}
    # assert AdventOfCodeProblem202314().solve_all() == {1: TODO, 2: TODO}
    assert AdventOfCodeProblem202315().solve_all() == {1: 514281, 2: 244199}
    # assert AdventOfCodeProblem202316().solve_all() == {1: TODO, 2: TODO}
    # assert AdventOfCodeProblem202317().solve_all() == {1: TODO, 2: TODO}
    assert AdventOfCodeProblem202318().solve_all() == {1: 47139, 2: 173152345887206}
    # assert AdventOfCodeProblem202319().solve_all() == {1: TODO, 2: TODO}
    assert AdventOfCodeProblem202320().solve_all() == {1: 684125385, 2: 225872806380073}
