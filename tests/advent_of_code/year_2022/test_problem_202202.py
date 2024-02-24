from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.year_2022.problem_202202 import (
    compute_scores_for_part_1,
    compute_scores_for_part_2,
    parse_text_input,
)


def test_problem_202202_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = parse_text_input(test_input)
    scores = compute_scores_for_part_1(parsed_input)
    assert scores == (8, 1, 6)
    total_score = sum(scores)
    assert total_score == 15


def test_problem_202202_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)

    parsed_input = parse_text_input(test_input)
    scores = compute_scores_for_part_2(parsed_input)
    assert scores == (4, 1, 7)
    total_score = sum(scores)
    assert total_score == 12
