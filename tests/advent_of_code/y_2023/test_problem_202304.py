import numpy as np

from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2023.problem_202304 import (
    find_card_worth,
    find_winning_numbers_you_have,
    parse_text_input,
    update_card_instances,
)


def test_problem_20234_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
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


def test_problem_20234_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
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
