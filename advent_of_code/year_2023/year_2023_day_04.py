from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from advent_of_code.protocols import AdventOfCodeProblem

type PuzzleInput = list[Card]


@dataclass(frozen=True, kw_only=True)
class Card:
    identifier: int
    winning_numbers: npt.NDArray[np.int32]
    numbers_you_have: npt.NDArray[np.int32]


@dataclass(kw_only=True)
class AdventOfCodeProblem202304(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 4

    def solve_part_1(self, puzzle_input: PuzzleInput):
        cards = puzzle_input
        card_worths = [find_card_worth(card) for card in cards]
        return sum(card_worths)

    def solve_part_2(self, puzzle_input: PuzzleInput):
        cards = puzzle_input
        instances = np.ones(len(cards), dtype=np.int32)
        for card in cards:
            update_card_instances(instances, card)
        return sum(instances)

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input(text)


def parse_text_input(text: str) -> list[Card]:
    lines = text.strip().split("\n")
    cards: list[Card] = []
    for line in lines:
        colon_split = line.split(":")
        identifier = int(colon_split[0][4:])
        pipe_split = colon_split[1].split("|")
        winning_numbers = np.fromstring(pipe_split[0], np.int32, sep=" ")
        numbers_you_have = np.fromstring(pipe_split[1], np.int32, sep=" ")
        card = Card(
            identifier=identifier,
            winning_numbers=winning_numbers,
            numbers_you_have=numbers_you_have,
        )
        cards.append(card)
    assert len(cards) == 214
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
def update_card_instances(instances: npt.NDArray[np.int32], card: Card):
    start = card.identifier
    offset = len(find_winning_numbers_you_have(card))
    current_card_instance_count = instances[start - 1]
    instances[start : start + offset] += current_card_instance_count


if __name__ == "__main__":
    print(AdventOfCodeProblem202304().solve_all())
