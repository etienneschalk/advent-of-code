import pytest

from advent_of_code.year_2022.year_2022_day_01 import AdventOfCodeProblem202201
from advent_of_code.year_2022.year_2022_day_02 import AdventOfCodeProblem202202
from advent_of_code.year_2022.year_2022_day_03 import AdventOfCodeProblem202203
from advent_of_code.year_2022.year_2022_day_04 import AdventOfCodeProblem202204
from advent_of_code.year_2022.year_2022_day_05 import AdventOfCodeProblem202205

# from advent_of_code.year_2022.year_2022_day_06 import AdventOfCodeProblem202206
# from advent_of_code.year_2022.year_2022_day_07 import AdventOfCodeProblem202207
# from advent_of_code.year_2022.year_2022_day_08 import AdventOfCodeProblem202208
# from advent_of_code.year_2022.year_2022_day_09 import AdventOfCodeProblem202209
# from advent_of_code.year_2022.year_2022_day_10 import AdventOfCodeProblem202210
# from advent_of_code.year_2022.year_2022_day_11 import AdventOfCodeProblem202211
# from advent_of_code.year_2022.year_2022_day_12 import AdventOfCodeProblem202212
# from advent_of_code.year_2022.year_2022_day_13 import AdventOfCodeProblem202213
# from advent_of_code.year_2022.year_2022_day_14 import AdventOfCodeProblem202214
# from advent_of_code.year_2022.year_2022_day_15 import AdventOfCodeProblem202215
# from advent_of_code.year_2022.year_2022_day_16 import AdventOfCodeProblem202216
# from advent_of_code.year_2022.year_2022_day_17 import AdventOfCodeProblem202217
# from advent_of_code.year_2022.year_2022_day_18 import AdventOfCodeProblem202218
# from advent_of_code.year_2022.year_2022_day_19 import AdventOfCodeProblem202219
# from advent_of_code.year_2022.year_2022_day_20 import AdventOfCodeProblem202220
# from advent_of_code.year_2022.year_2022_day_21 import AdventOfCodeProblem202221
# from advent_of_code.year_2022.year_2022_day_22 import AdventOfCodeProblem202222
# from advent_of_code.year_2022.year_2022_day_23 import AdventOfCodeProblem202223
# from advent_of_code.year_2022.year_2022_day_24 import AdventOfCodeProblem202224
from advent_of_code.year_2022.year_2022_day_25 import AdventOfCodeProblem202225


@pytest.mark.integration
def test_integration_202201():
    assert AdventOfCodeProblem202201().solve_all() == {1: 69795, 2: 208437}


@pytest.mark.integration
def test_integration_202202():
    assert AdventOfCodeProblem202202().solve_all() == {1: 9759, 2: 12429}


@pytest.mark.integration
def test_integration_202203():
    assert AdventOfCodeProblem202203().solve_all() == {1: 8109, 2: 2738}


@pytest.mark.integration
def test_integration_202204():
    assert AdventOfCodeProblem202204().solve_all() == {1: 560, 2: 839}


@pytest.mark.integration
def test_integration_202205():
    assert AdventOfCodeProblem202205().solve_all() == {1: "HNSNMTLHQ", 2: "RNLFDJMCT"}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202206():
#     assert AdventOfCodeProblem202206().solve_all() == {1: None, 2: None}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202207():
#     assert AdventOfCodeProblem202207().solve_all() == {1: None, 2: None}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202208():
#     assert AdventOfCodeProblem202208().solve_all() == {1: None, 2: None}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202209():
#     assert AdventOfCodeProblem202209().solve_all() == {1: None, 2: None}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202210():
#     assert AdventOfCodeProblem202210().solve_all() == {1: None, 2: None}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202211():
#     assert AdventOfCodeProblem202211().solve_all() == {1: None, 2: None}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202212():
#     assert AdventOfCodeProblem202212().solve_all() == {1: None, 2: None}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202213():
#     assert AdventOfCodeProblem202213().solve_all() == {1: None, 2: None}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202214():
#     assert AdventOfCodeProblem202214().solve_all() == {1: None, 2: None}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202215():
#     assert AdventOfCodeProblem202215().solve_all() == {1: None, 2: None}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202216():
#     assert AdventOfCodeProblem202216().solve_all() == {1: None, 2: None}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202217():
#     assert AdventOfCodeProblem202217().solve_all() == {1: None, 2: None}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202218():
#     assert AdventOfCodeProblem202218().solve_all() == {1: None, 2: None}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202219():
#     assert AdventOfCodeProblem202219().solve_all() == {1: None, 2: None}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202220():
#     assert AdventOfCodeProblem202220().solve_all() == {1: None, 2: None}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202221():
#     assert AdventOfCodeProblem202221().solve_all() == {1: None, 2: None}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202222():
#     assert AdventOfCodeProblem202222().solve_all() == {1: None, 2: None}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202223():
#     assert AdventOfCodeProblem202223().solve_all() == {1: None, 2: None}


# @pytest.mark.skip(reason="not solved yet")
# @pytest.mark.integration
# def test_integration_202224():
#     assert AdventOfCodeProblem202224().solve_all() == {1: None, 2: None}


@pytest.mark.integration
def test_integration_202225():
    assert AdventOfCodeProblem202225().solve_all() == {
        1: "2=01-0-2-0=-0==-1=01",
        2: "Part 2 of Day 25 is having solved all the 49 previous problems!",
    }
