from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True, kw_only=True)
class Card:
    identifier: int
    winning_numbers: list[int]
    numbers_you_have: list[int]


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    cards = load_input_text_file()
    card_worths = [find_card_worth(card) for card in cards]
    return sum(card_worths)


def compute_part_2():
    cards = load_input_text_file()
    instances = np.ones(len(cards), dtype=int)
    for card in cards:
        update_card_instances(instances, card)
    return sum(instances)


def load_input_text_file() -> list[Card]:
    input_path = "resources/advent_of_code/year_2023/input_year_2023_day_4.txt"
    input_path = Path(input_path)
    assert input_path.is_file()
    text = input_path.read_text()
    cards = parse_text_input(text)
    assert len(cards) == 214
    return cards


def parse_text_input(text: str) -> list[Card]:
    lines = text.strip().split("\n")
    cards: list[Card] = []
    for line in lines:
        colon_split = line.split(":")
        identifier = int(colon_split[0][4:])
        pipe_split = colon_split[1].split("|")
        winning_numbers = np.fromstring(pipe_split[0], np.int8, sep=" ")
        numbers_you_have = np.fromstring(pipe_split[1], np.int8, sep=" ")
        card = Card(
            identifier=identifier,
            winning_numbers=winning_numbers,
            numbers_you_have=numbers_you_have,
        )
        cards.append(card)
    return cards


def find_winning_numbers_you_have(card: Card) -> set[int]:
    winning_numbers_set = set(card.winning_numbers)
    assert len(winning_numbers_set) == len(card.winning_numbers)
    numbers_you_have_set = set(card.numbers_you_have)
    assert len(numbers_you_have_set) == len(card.numbers_you_have)

    winning_numbers_in_numbers_you_have_set = {
        winning_number
        for winning_number in winning_numbers_set
        if winning_number in numbers_you_have_set
    }

    return winning_numbers_in_numbers_you_have_set


def find_card_worth(card: Card) -> int:
    number_set = find_winning_numbers_you_have(card)
    if not number_set:
        return 0
    return 2 ** (len(number_set) - 1)


# Mutates instances in place. An instance count = "number of cards"
def update_card_instances(instances: np.ndarray, card: Card):
    start = card.identifier
    offset = len(find_winning_numbers_you_have(card))
    current_card_instance_count = instances[start - 1]
    instances[start : start + offset] += current_card_instance_count


if __name__ == "__main__":
    main()
