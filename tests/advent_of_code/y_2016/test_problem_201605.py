import pytest

from advent_of_code.y_2016.problem_201605 import AdventOfCodeProblem201605


@pytest.mark.parametrize("puzzle_input,expected", [("abc", "18f47a30")])
def test_problem_202205_part_1(puzzle_input: str, expected: str):
    result = AdventOfCodeProblem201605().solve_part_1(puzzle_input)
    assert result == expected


@pytest.mark.parametrize("puzzle_input,expected", [("abc", "05ace8e3")])
def test_problem_202205_part_2(puzzle_input: str, expected: str):
    result = AdventOfCodeProblem201605().solve_part_2(puzzle_input)
    assert result == expected


@pytest.mark.integration
@pytest.mark.parametrize("puzzle_input,expected", [("abbhdwsy", "801b56a7")])
def test_problem_202205_part_1_integration(puzzle_input: str, expected: str):
    result = AdventOfCodeProblem201605().solve_part_1(puzzle_input)
    assert result == expected


@pytest.mark.integration
@pytest.mark.parametrize("puzzle_input,expected", [("abbhdwsy", "424a0197")])
def test_problem_202205_part_2_integration(puzzle_input: str, expected: str):
    result = AdventOfCodeProblem201605().solve_part_2(puzzle_input)
    assert result == expected
