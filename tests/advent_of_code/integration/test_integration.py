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

# Bash:
# pytest --with-integration -k integration


@pytest.mark.integration
def test_integration():
    assert AdventOfCodeProblem202301().solve_all() == {1: 54630, 2: 54770}
    assert AdventOfCodeProblem202302().solve_all() == {1: 2061, 2: 72596}
    assert AdventOfCodeProblem202303().solve_all() == {1: 529618, 2: 77509019}
    assert AdventOfCodeProblem202304().solve_all() == {1: 23750, 2: 13261850}
    assert AdventOfCodeProblem202305().solve_all() == {1: 323142486, 2: 79874951}
    assert AdventOfCodeProblem202306().solve_all() == {1: 2269432, 2: 35865985}
    assert AdventOfCodeProblem202307().solve_all() == {1: 252052080, 2: 252898370}
    assert AdventOfCodeProblem202308().solve_all() == {1: 15871, 2: 11283670395017}
    assert AdventOfCodeProblem202309().solve_all() == {1: 1884768153, 2: 1031}
