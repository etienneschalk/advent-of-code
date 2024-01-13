from collections import defaultdict
from dataclasses import dataclass
from functools import reduce

from advent_of_code.common import load_input_text_file_from_filename
from advent_of_code.protocols import AdventOfCodeProblem

PuzzleInput = list[str]


@dataclass(kw_only=True)
class AdventOfCodeProblem202315(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 15

    def solve_part_1(self, puzzle_input: PuzzleInput):
        return sum(hash_year_2023_day_15(i) for i in puzzle_input)

    def solve_part_2(self, puzzle_input: PuzzleInput):
        initialization_sequence = puzzle_input
        boxes = hashmap_process(initialization_sequence)
        return add_up_focusing_power(boxes)

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input(text)


def hashmap_process(
    initialization_sequence: PuzzleInput,
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


def render_step(boxes: dict[int, dict[str, int]], step: str) -> str:
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


def parse_input_text_file() -> PuzzleInput:
    text = load_input_text_file_from_filename(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> PuzzleInput:
    lines = text.strip().split(",")
    return lines


if __name__ == "__main__":
    print(AdventOfCodeProblem202315().solve_all())
