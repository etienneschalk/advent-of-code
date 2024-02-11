from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.year_2023.year_2023_day_07 import (
    MAPPING_SRC_TO_DEST_PART_1,
    MAPPING_SRC_TO_DEST_PART_2,
    compute_total_winnings,
    map_puzzle_input,
    parse_text_input,
    sort_by_hand_type_part_1,
    sort_by_hand_type_part_2,
)


def test_year_2023_day_07_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = parse_text_input(test_input)
    mapped_input = map_puzzle_input(parsed_input, MAPPING_SRC_TO_DEST_PART_1)
    sorted_by_hand_type = sort_by_hand_type_part_1(mapped_input)
    total_winnings = compute_total_winnings(sorted_by_hand_type)
    assert total_winnings == 6440
    ...


def test_year_2023_day_07_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = parse_text_input(test_input)
    mapped_input = map_puzzle_input(parsed_input, MAPPING_SRC_TO_DEST_PART_2)
    sorted_by_hand_type = sort_by_hand_type_part_2(
        mapped_input, MAPPING_SRC_TO_DEST_PART_2
    )
    total_winnings = compute_total_winnings(sorted_by_hand_type)
    assert total_winnings == 5905
    ...
