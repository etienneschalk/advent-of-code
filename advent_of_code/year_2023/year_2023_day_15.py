from collections import defaultdict
from functools import reduce

from advent_of_code.common import load_input_text_file

ProblemDataType = list[str]


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    parsed_input = parse_input_text_file()
    return sum(hash_year_2023_day_15(i) for i in parsed_input)


def compute_part_2():
    initialization_sequence = parse_input_text_file()
    boxes = hashmap_process(initialization_sequence)
    return add_up_focusing_power(boxes)


def hashmap_process(
    initialization_sequence: ProblemDataType,
) -> dict[int, dict[str, int]]:
    boxes = defaultdict(dict)
    for step in initialization_sequence:
        if step[-1] == "-":
            label = step[:-1]
            box = hash_year_2023_day_15(label)
            boxes[box].pop(label, None)
        else:
            label, focal_length = step.split("=")
            box = hash_year_2023_day_15(label)
            boxes[box][label] = int(focal_length)
    return boxes


def add_up_focusing_power(boxes: dict[int, dict[str, int]]) -> int:
    return sum(
        (box + 1)
        * sum(
            slot * focal_length for slot, focal_length in enumerate(lenses.values(), 1)
        )
        for box, lenses in boxes.items()
    )


def render_step(boxes, step) -> str:
    return f'After "{step}":\n' + "\n".join(
        (f"Box {k}: {render_box(v)}" for k, v in boxes.items() if v)
    )


def render_box(box: dict[str, int]) -> str:
    return " ".join(f"[{k} {v}]" for k, v in box.items())


def hash_year_2023_day_15_imperative(string: str):
    value = 0
    for c in string:
        value = ((value + ord(c)) * 17) % 256
    return value


def hash_year_2023_day_15(string: str):
    return reduce(lambda x, y: ((x + ord(y)) * 17) % 256, string, 0)


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    lines = text.strip().split(",")
    return lines


if __name__ == "__main__":
    main()
