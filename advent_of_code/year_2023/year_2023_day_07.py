from collections import Counter
from typing import Literal, get_args

from advent_of_code.common import load_input_text_file

ALL_LABELS = list("AKQJT98765432")
MAPPED_LABELS = list(range(len(ALL_LABELS)))
MAPPING_SRC_TO_DEST = {k: v for k, v in zip(ALL_LABELS, MAPPED_LABELS)}
MAPPING_DEST_TO_SRC = {k: v for k, v in zip(MAPPED_LABELS, ALL_LABELS)}

HandType = Literal[
    "Five of a kind",
    "Four of a kind",
    "Full house",
    "Three of a kind",
    "Two pair",
    "One pair",
    "High card",
]
UNIQUE_OCCURRENCES_TO_HAND_TYPE = {
    (5,): "Five of a kind",
    (4, 1): "Four of a kind",
    (3, 2): "Full house",
    (3, 1, 1): "Three of a kind",
    (2, 2, 1): "Two pair",
    (2, 1, 1, 1): "One pair",
    (1, 1, 1, 1, 1): "High card",
}

ALL_HAND_TYPES = list(get_args(HandType))


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    parsed_input = parse_input_text_file()  # noqa: F841
    total_winnings = compute_total_winnings(parsed_input)
    return total_winnings


def compute_total_winnings(parsed_input: list[tuple[Counter, int]]) -> int:
    sorted_by_hand_type = sort_by_hand_type(parsed_input)
    bids_times_ranks = (
        index * hand_and_bid[1]
        for index, hand_and_bid in enumerate(
            reversed([b for a in sorted_by_hand_type.values() for b in a]), 1
        )
    )
    total_winnings = sum(bids_times_ranks)
    return total_winnings


def sort_by_hand_type(
    hands_and_bids: list[tuple[Counter, int]]
) -> dict[HandType, Counter]:
    hand_types: dict[HandType, Counter] = {
        hand_type: [] for hand_type in ALL_HAND_TYPES
    }

    for hand_and_bid in hands_and_bids:
        hand = hand_and_bid[0]
        instances = tuple(sorted(Counter(hand).values(), reverse=True))
        hand_types[UNIQUE_OCCURRENCES_TO_HAND_TYPE[instances]].append(hand_and_bid)
    return hand_types


def compute_part_2():
    data = parse_input_text_file()  # noqa: F841
    ...
    return None


def parse_input_text_file() -> list[tuple[Counter, int]]:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> list[tuple[Counter, int]]:
    lines = text.strip().split("\n")
    # Assert that all cards are unique.
    assert len(set((line.split()[0] for line in lines))) == len(lines)
    return sorted(
        [
            (
                list(MAPPING_SRC_TO_DEST[v] for v in line.split()[0]),
                int(line.split()[1]),
            )
            for line in lines
        ]
    )


# def parse_text_input(text: str) -> list[tuple[Counter, int]]:
#     lines = text.strip().split("\n")
#     # Assert that all cards are unique.
#     assert len(set((line.split()[0] for line in lines))) == len(lines)
#     return sorted(
#         (
#             (
#                 (sorted(line.split()[0], key=lambda l: ALL_LABELS.index(l))),
#                 str(line.split()[1]),
#             )
#             for line in lines
#         ),
#     )


if __name__ == "__main__":
    main()
