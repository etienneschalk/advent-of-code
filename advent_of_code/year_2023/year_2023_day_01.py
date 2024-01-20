from dataclasses import dataclass
from typing import Literal, get_args

from advent_of_code.protocols import AdventOfCodeProblem

# Do not use the type keyword, as values are used dynamically
# in the code too (not only the type declarations)
Keys = Literal["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
type Mappings = dict[Literal["default", "reversed"], dict[Keys, str]]
type PuzzleInput = list[str]


@dataclass(kw_only=True)
class AdventOfCodeProblem202301(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 1

    def solve_part_1(self, puzzle_input: PuzzleInput):
        return compute_calibration_sum(puzzle_input)

    def solve_part_2(self, puzzle_input: PuzzleInput):
        corrected = correct_input_for_part_2(puzzle_input)
        return compute_calibration_sum(corrected)

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input(text)


def parse_text_input(text: str) -> list[str]:
    words = text.strip().split("\n")

    # Input validation: only lowercase-alphanumeric characters
    assert all(
        all((is_lowercase_alphanumeric_character(c)) for c in word) for word in words
    )
    # Note: there is no "a"...
    assert all(all(ord(c) != "a" for c in word) for word in words)

    return words


def is_lowercase_alphanumeric_character(c: str):
    return (ord("a") <= ord(c) <= ord("z")) or (ord("0") <= ord(c) <= ord("9"))


def compute_calibration_sum(words: list[str]) -> int:
    return sum(recover_calibration_value(word) for word in words)


def recover_calibration_value(word: str) -> int:
    digits = [c for c in word if c.isdigit()]
    return 10 * int(digits[0]) + int(digits[-1])


def correct_input_for_part_2(words: list[str]) -> list[str]:
    mappings = build_part_2_mappings()

    return [replace_first_last_spelled_digits(word, mappings) for word in words]


def build_part_2_mappings() -> Mappings:
    mapping = build_part_2_mapping()
    reversed_mapping = {k[::-1]: v for k, v in mapping.items()}
    return {"default": mapping, "reversed": reversed_mapping}


def build_part_2_mapping():
    keys = get_args(Keys)
    values = (str(i) for i in range(1, 10))
    mapping = dict(zip(keys, values))
    return mapping


def replace_first_last_spelled_digits(word: str, mappings: Mappings) -> str:
    word = replace_first_spelled_digit(word, mappings["default"])
    word = replace_first_spelled_digit(word[::-1], mappings["reversed"])[::-1]
    return word


def replace_first_spelled_digit(word: str, mapping: dict[Keys, str]) -> str:
    # The count = 1 is very important to only replace what's needed!
    word_dict = {
        source: word.replace(source, target, 1) for source, target in mapping.items()
    }

    rank_mapping = {k: find_first_digit_index(v, False) for k, v in word_dict.items()}
    rank_mapping_non_none = {k: v for k, v in rank_mapping.items() if v is not None}

    # Do nee to substitute if not needed! (don't doing so = wrong result)
    if len(set(rank_mapping_non_none.values())) == 1:
        return word

    # The -1 is necessary to make the type checker happy
    correct_digit_key = min(
        rank_mapping_non_none, key=lambda k: rank_mapping_non_none.get(k, -1)
    )
    corrected_word = word_dict[correct_digit_key]

    return corrected_word


def find_first_digit_index(word: str, reverse: bool):
    for i, c in enumerate(reversed(word) if reverse else word):
        if c.isdigit():
            return i


if __name__ == "__main__":
    print(AdventOfCodeProblem202301().solve())
