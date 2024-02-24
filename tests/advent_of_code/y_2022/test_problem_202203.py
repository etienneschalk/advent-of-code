from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2022.problem_202203 import (
    compute_priority_sum,
    find_shared_items_for_part_1,
    find_shared_items_for_part_2,
    parse_text_input,
)


def test_problem_202203_part_1(example_inputs_2022: ExampleInputsStore):
    test_input = example_inputs_2022.retrieve(__file__)

    parsed_input = parse_text_input(test_input)
    assert parsed_input[0][0] == "vJrwpWtwJgWr"
    assert parsed_input[0][1] == "hcsFMMfFFhFp"
    assert parsed_input[1][0] == "jqHRNqRjqzjGDLGL"
    assert parsed_input[1][1] == "rsFMfFZSrLrFZsSL"
    assert parsed_input[2][0] == "PmmdzqPrV"
    assert parsed_input[2][1] == "vPwwTWBwg"

    expected_shared_items = ("p", "L", "P", "v", "t", "s")
    actual_shared_items = find_shared_items_for_part_1(parsed_input)
    assert actual_shared_items == expected_shared_items

    priority_sum = compute_priority_sum(actual_shared_items)
    assert priority_sum == 157


def test_problem_202203_part_2(example_inputs_2022: ExampleInputsStore):
    test_input = example_inputs_2022.retrieve(__file__)

    parsed_input = parse_text_input(test_input)

    expected_shared_items = ("r", "Z")
    actual_shared_items = find_shared_items_for_part_2(parsed_input)
    assert actual_shared_items == expected_shared_items

    priority_sum = compute_priority_sum(actual_shared_items)
    assert priority_sum == 70
