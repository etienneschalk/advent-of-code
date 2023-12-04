from advent_of_code.common import load_input_text_file


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    data = parse_input_text_file()  # noqa: F841
    ...
    return None


def compute_part_2():
    data = parse_input_text_file()  # noqa: F841
    ...
    return None


def parse_input_text_file() -> ...:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ...:
    lines = text.strip().split("\n")
    ...
    return lines


if __name__ == "__main__":
    main()
