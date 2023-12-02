from pathlib import Path


def parse_input_year_2023_day_1(text: str) -> list[str]:
    words = text.strip().split("\n")
    # Input validation: only lowercase-alphanumeric characters
    assert all(
        all((is_lowercase_alphanumeric_character(c)) for c in word) for word in words
    )
    return words


def correct_input_year_2023_day_1(words: list[str]) -> list[str]:
    mapping = build_part_2_mapping()

    return [substitute_spelled_calibration_digits(word, mapping) for word in words]


def recover_calibration_value(word: str) -> int:
    digits = [c for c in word if c.isdigit()]
    return 10 * int(digits[0]) + int(digits[-1])


def is_lowercase_alphanumeric_character(c: str):
    return (ord("a") <= ord(c) <= ord("z")) or (ord("0") <= ord(c) <= ord("9"))


def load_input_data():
    input_path = "resources/advent_of_code/year_2023/input_day_1.txt"
    input_path = Path(input_path)
    assert input_path.is_file()
    text = input_path.read_text()
    words = parse_input_year_2023_day_1(text)
    assert len(words) == 1000
    return words


def substitute_spelled_calibration_digits(word: str, mapping: dict[str, str]) -> str:
    word = substitute_spelled_calibration_digits_step(word, mapping, False)
    word = substitute_spelled_calibration_digits_step(word, mapping, True)
    return word


def substitute_spelled_calibration_digits_step(
    word: str, mapping: dict[str, str], reverse: bool
) -> str:
    word_dict = {}
    for source, target in mapping.items():
        word_dict[source] = word.replace(source, target)
    rank_mapping = {k: find_first_digit_index(v, reverse) for k, v in word_dict.items()}
    rank_mapping = {k: v for k, v in rank_mapping.items() if v is not None}
    correct_digit_key = min(rank_mapping, key=rank_mapping.get)
    corrected_word = word_dict[correct_digit_key]
    return corrected_word


def find_first_digit_index(word: str, reverse: bool):
    if reverse:
        word = reversed(word)
    for i, c in enumerate(word):
        if c.isdigit():
            return i


def build_part_2_mapping() -> dict[str, str]:
    keys = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
    values = (str(i) for i in range(1, 10))
    mapping = dict(zip(keys, values))
    return mapping


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


def compute_part_1():
    words = load_input_data()
    return compute_calibration_sum(words)


def compute_part_2():
    words = load_input_data()
    corrected = correct_input_year_2023_day_1(words)
    print(corrected)
    return compute_calibration_sum(corrected)


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()

    print({1: result_part_1, 2: result_part_2})


if __name__ == "__main__":
    main()
