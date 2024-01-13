from collections import Counter
from dataclasses import dataclass
from typing import Any, Literal, get_args

from advent_of_code.protocols import AdventOfCodeProblem

ALL_LABELS_PART_1 = tuple("AKQJT98765432")
MAPPED_LABELS_PART_1 = tuple(range(len(ALL_LABELS_PART_1)))
MAPPING_SRC_TO_DEST_PART_1 = {
    k: v for k, v in zip(ALL_LABELS_PART_1, MAPPED_LABELS_PART_1)
}


ALL_LABELS_PART_2 = tuple("AKQT98765432J")
MAPPED_LABELS_PART_2 = tuple(range(len(ALL_LABELS_PART_2)))
MAPPING_SRC_TO_DEST_PART_2 = {
    k: v for k, v in zip(ALL_LABELS_PART_2, MAPPED_LABELS_PART_2)
}

HandType = Literal[
    "Five of a kind",
    "Four of a kind",
    "Full house",
    "Three of a kind",
    "Two pair",
    "One pair",
    "High card",
]
UNIQUE_OCCURRENCES_TO_HAND_TYPE: dict[tuple[int, ...], str] = {
    (5,): "Five of a kind",
    (4, 1): "Four of a kind",
    (3, 2): "Full house",
    (3, 1, 1): "Three of a kind",
    (2, 2, 1): "Two pair",
    (2, 1, 1, 1): "One pair",
    (1, 1, 1, 1, 1): "High card",
}

ALL_HAND_TYPES = list(get_args(HandType))

type PuzzleInput = list[tuple[list[str], int]]
type HandAndBid = tuple[list[int], int]
type PuzzleMappedInput = list[HandAndBid]
type SortedByHandType = dict[Any, list[HandAndBid]]


@dataclass(kw_only=True)
class AdventOfCodeProblem202307(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 7

    def solve_part_1(self, puzzle_input: PuzzleInput):
        mapping = MAPPING_SRC_TO_DEST_PART_1
        mapped_input = map_puzzle_input(puzzle_input, mapping)
        sorted_by_hand_type = sort_by_hand_type_part_1(mapped_input)
        total_winnings = compute_total_winnings(sorted_by_hand_type)
        return total_winnings

    def solve_part_2(self, puzzle_input: PuzzleInput):
        mapping = MAPPING_SRC_TO_DEST_PART_2
        mapped_input = map_puzzle_input(puzzle_input, mapping)
        sorted_by_hand_type = sort_by_hand_type_part_2(mapped_input, mapping=mapping)
        total_winnings = compute_total_winnings(sorted_by_hand_type)
        return total_winnings

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input(text)


def compute_total_winnings(sorted_by_hand_type: SortedByHandType):
    bids_times_ranks = (
        index * hand_and_bid[1]
        for index, hand_and_bid in enumerate(
            reversed([b for a in sorted_by_hand_type.values() for b in a]), 1
        )
    )
    total_winnings = sum(bids_times_ranks)
    return total_winnings


def map_puzzle_input(
    puzzle_input: PuzzleInput, mapping: dict[str, int]
) -> PuzzleMappedInput:
    return sorted(
        [
            ([mapping[c] for c in list_of_hands], bid)
            for (list_of_hands, bid) in puzzle_input
        ]
    )


def sort_by_hand_type_part_1(
    hands_and_bids: PuzzleMappedInput,
) -> SortedByHandType:
    hand_types: SortedByHandType = {hand_type: [] for hand_type in ALL_HAND_TYPES}

    for hand_and_bid in hands_and_bids:
        hand = hand_and_bid[0]
        instances = tuple(sorted(Counter(hand).values(), reverse=True))
        hand_types[UNIQUE_OCCURRENCES_TO_HAND_TYPE[instances]].append(hand_and_bid)
    return hand_types


def sort_by_hand_type_part_2(
    hands_and_bids: PuzzleMappedInput,
    mapping: dict[str, int],
) -> SortedByHandType:
    hand_types: SortedByHandType = {hand_type: [] for hand_type in ALL_HAND_TYPES}

    joker_value = len(mapping) - 1
    sort_instances_func = list(UNIQUE_OCCURRENCES_TO_HAND_TYPE.keys()).index
    for hand_and_bid in hands_and_bids:
        hand = hand_and_bid[0]
        candidate_instances: list[tuple[int, ...]] = []
        if joker_value not in hand:
            best_instances = tuple(sorted(Counter(hand).values(), reverse=True))
        else:
            for j_candidate_value in MAPPED_LABELS_PART_2[:-1]:
                new_hand = [j_candidate_value if h == joker_value else h for h in hand]
                instances = tuple(sorted(Counter(new_hand).values(), reverse=True))
                candidate_instances.append(instances)
            best_instances = min(
                candidate_instances,
                key=sort_instances_func,
            )
        hand_types[UNIQUE_OCCURRENCES_TO_HAND_TYPE[best_instances]].append(hand_and_bid)
    return hand_types


def parse_text_input(text: str):
    lines = text.strip().split("\n")
    # Assert that all cards are unique.
    assert len(set((line.split()[0] for line in lines))) == len(lines)
    return [(list(line.split()[0]), int(line.split()[1])) for line in lines]


if __name__ == "__main__":
    print(AdventOfCodeProblem202307().solve_all())
