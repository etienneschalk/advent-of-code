import numpy as np

from advent_of_code.common import load_input_text_file

ProblemDataType = ...


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    data = parse_input_text_file()
    ...
    return None


def compute_part_2():
    data = parse_input_text_file()
    ...
    return None


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    lines = text.strip().split("\n")
    parsed = []
    for line in lines:
        record, group = line.split(" ")
        group = tuple(int(c) for c in group.split(","))
        parsed.append((np.fromstring(record, dtype="<S1"), group))
    return parsed


if __name__ == "__main__":
    main()
