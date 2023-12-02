from pathlib import Path
from typing import Literal

MappingsType = dict[Literal["default", "reversed"], dict[str, str]]


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()

    # TODO do not work!
    # Autre approche: bourrin et manuel, iterateur le long des char qui teste les chaines.
    # A l'endroit, et a l'envers, eg one -> eno
    # 54729 too low
    # 54771 too high
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    words = load_input_text_file()
    return compute_calibration_sum(words)


def compute_part_2():
    words = load_input_text_file()
    corrected = correct_input_for_part_2(words)
    # print(corrected)
    return compute_calibration_sum(corrected)


def load_input_text_file():
    input_path = "resources/advent_of_code/year_2023/input_day_1.txt"
    input_path = Path(input_path)
    assert input_path.is_file()
    text = input_path.read_text()
    words = parse_text_input(text)
    assert len(words) == 1000
    return words


def parse_text_input(text: str) -> list[str]:
    words = text.strip().split("\n")

    # Input validation: only lowercase-alphanumeric characters
    assert all(
        all((is_lowercase_alphanumeric_character(c)) for c in word) for word in words
    )

    return words


def is_lowercase_alphanumeric_character(c: str):
    return (ord("a") <= ord(c) <= ord("z")) or (ord("0") <= ord(c) <= ord("9"))


def compute_calibration_sum(words: list[str]) -> int:
    # Note: there is no "a"...
    assert all(all(ord(c) != "a" for c in word) for word in words)

    calibration_value_generator = (recover_calibration_value(word) for word in words)
    calibration_values = list(calibration_value_generator)
    for i in range(50):
        print(calibration_values[i * 20 : (i + 1) * 20])
    print()

    calibration_value_generator = (recover_calibration_value(word) for word in words)
    calibration_sum = sum(calibration_value_generator)

    print(calibration_sum)

    return calibration_sum


def recover_calibration_value(word: str) -> int:
    digits = [c for c in word if c.isdigit()]
    return 10 * int(digits[0]) + int(digits[-1])


def correct_input_for_part_2(words: list[str]) -> list[str]:
    mappings = build_part_2_mappings()

    return [replace_first_last_spelled_digits(word, mappings) for word in words]


def build_part_2_mappings() -> MappingsType:
    mapping = build_part_2_mapping()
    reversed_mapping = {k[::-1]: v for k, v in mapping.items()}
    return {"default": mapping, "reversed": reversed_mapping}


def build_part_2_mapping() -> dict[str, str]:
    keys = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
    values = (str(i) for i in range(1, 10))
    mapping = dict(zip(keys, values))
    return mapping


def replace_first_last_spelled_digits(word: str, mappings: MappingsType) -> str:
    word = replace_first_spelled_digit(word, mappings["default"])
    word = replace_first_spelled_digit(word[::-1], mappings["reversed"])[::-1]
    return word


def replace_first_spelled_digit(word: str, mapping: dict[str, str]) -> str:
    word_dict = {}

    for source, target in mapping.items():
        # The count = 1 is very important to only replace what's needed!
        word_dict[source] = word.replace(source, target, 1)
    rank_mapping = {k: find_first_digit_index(v, False) for k, v in word_dict.items()}
    rank_mapping = {k: v for k, v in rank_mapping.items() if v is not None}

    # Do nee to substitute if not needed! (don't doing so = wrong result)
    if len(set(rank_mapping.values())) == 1:
        return word

    correct_digit_key = min(rank_mapping, key=rank_mapping.get)
    corrected_word = word_dict[correct_digit_key]

    return corrected_word


def find_first_digit_index(word: str, reverse: bool):
    if reverse:
        word = reversed(word)
    for i, c in enumerate(word):
        if c.isdigit():
            return i


if __name__ == "__main__":
    main()
