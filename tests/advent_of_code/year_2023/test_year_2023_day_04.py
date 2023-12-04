import numpy as np

from advent_of_code.year_2023.year_2023_day_04 import (
    find_card_worth,
    find_winning_numbers_you_have,
    parse_text_input,
    update_card_instances,
)

EXAMPLE_INPUT = """

Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11

"""


def test_year_2023_day_4_part_1():
    test_input = EXAMPLE_INPUT
    cards = parse_text_input(test_input)

    expected_winning_numbers_you_have = [
        {48, 83, 17, 86},
        {32, 61},
        {1, 21},
        {84},
        set(),
        set(),
    ]
    winning_numbers_you_have = [find_winning_numbers_you_have(card) for card in cards]
    assert winning_numbers_you_have == expected_winning_numbers_you_have

    expected_card_worths = [8, 2, 2, 1, 0, 0]
    card_worths = [find_card_worth(card) for card in cards]
    assert card_worths == expected_card_worths

    assert sum(card_worths) == 13


def test_year_2023_day_4_part_2():
    test_input = EXAMPLE_INPUT
    cards = parse_text_input(test_input)

    expected_instances = [
        np.array([1, 2, 2, 2, 2, 1]),
        np.array([1, 2, 4, 4, 2, 1]),
        np.array([1, 2, 4, 8, 6, 1]),
        np.array([1, 2, 4, 8, 14, 1]),
        np.array([1, 2, 4, 8, 14, 1]),
        np.array([1, 2, 4, 8, 14, 1]),
    ]

    instances = np.ones(len(cards), dtype=int)
    for card in cards:
        update_card_instances(instances, card)
        assert (instances == expected_instances[card.identifier - 1]).all()

    assert sum(instances) == 30
