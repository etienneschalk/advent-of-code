from advent_of_code.year_2023.year_2023_day_07 import (
    MAPPING_SRC_TO_DEST_PART_2,
    compute_total_winnings,
    parse_text_input,
    sort_by_hand_type_part_1,
    sort_by_hand_type_part_2,
)

EXAMPLE_INPUT = """

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

"""


def test_year_2023_day_07_part_1():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)  # noqa: F841
    sorted_by_hand_type = sort_by_hand_type_part_1(parsed_input)
    total_winnings = compute_total_winnings(sorted_by_hand_type)
    assert total_winnings == 6440
    ...


def test_year_2023_day_07_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input, mapping=MAPPING_SRC_TO_DEST_PART_2)
    sorted_by_hand_type = sort_by_hand_type_part_2(
        parsed_input, mapping=MAPPING_SRC_TO_DEST_PART_2
    )
    total_winnings = compute_total_winnings(sorted_by_hand_type)
    assert total_winnings == 5905
    ...
