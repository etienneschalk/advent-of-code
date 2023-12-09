from advent_of_code.year_2022.year_2022_day_02 import (
    compute_scores_for_part_1,
    compute_scores_for_part_2,
    parse_text_input,
)

EXAMPLE_INPUT = """

A Y
B X
C Z

"""


def test_year_2022_day_02_part_1():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    scores = compute_scores_for_part_1(parsed_input)
    assert scores == (8, 1, 6)
    total_score = sum(scores)
    assert total_score == 15


def test_year_2022_day_02_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    scores = compute_scores_for_part_2(parsed_input)
    assert scores == (4, 1, 7)
    total_score = sum(scores)
    assert total_score == 12
