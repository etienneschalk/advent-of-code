from dataclasses import dataclass

from advent_of_code.common import load_input_text_file_from_filename
from advent_of_code.protocols import AdventOfCodeProblem

type ProblemLine = tuple[tuple[int, int], tuple[int, int]]
type PuzzleInput = tuple[ProblemLine, ...]


@dataclass(kw_only=True)
class AdventOfCodeProblem202204(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2022
    day: int = 4

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input(text)

    def solve_part_1(self, puzzle_input: PuzzleInput):
        fully_contained_count = compute_fully_contained_count(puzzle_input)
        return fully_contained_count

    def solve_part_2(self, puzzle_input: PuzzleInput):
        overlapping_count = compute_overlapping_count(puzzle_input)
        return overlapping_count


def compute_fully_contained_count(parsed_input: PuzzleInput):
    intersections = tuple(intersect_ranges_inclusive(*p) for p in parsed_input)
    fully_contained_count = sum(
        inter in set(pair) for inter, pair in zip(intersections, parsed_input)
    )

    return fully_contained_count


def compute_overlapping_count(parsed_input: PuzzleInput):
    intersections = tuple(intersect_ranges_inclusive(*p) for p in parsed_input)
    overlapping_count = sum(inter[0] <= inter[1] for inter in intersections)

    return overlapping_count


def intersect_ranges_inclusive(
    range_a: tuple[int, int], range_b: tuple[int, int]
) -> tuple[int, int]:
    return max(range_a[0], range_b[0]), min(range_a[1], range_b[1])


def render_input_visualization(input_data: PuzzleInput) -> str:
    max_value = max(i for p in input_data for j in p for i in j)
    digit_count = len(str(max_value))
    format_str = f"0{digit_count}d"
    format_str = "{:" + format_str + "}"
    return "\n\n".join(
        "\n".join(
            render_interval_bar(p[0], p[1], max_value, format_str)
            + "  "
            + render_interval(p, format_str)
            for p in line
        )
        for line in input_data
    )


def render_interval(p: tuple[int, int], format_str: str):
    return "-".join(format_str.format(i) for i in p)


def render_interval_bar(start: int, stop: int, max_value: int, format_str: str) -> str:
    digit_count = len(str(max_value))
    return "".join(
        (
            (digit_count * ".") * (start - 1),
            "".join(format_str.format(i) for i in range(start, stop + 1)),
            (digit_count * ".") * (max_value - stop),
        )
    )


def parse_input_text_file() -> PuzzleInput:
    text = load_input_text_file_from_filename(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> PuzzleInput:
    lines = text.strip().split("\n")
    parsed = tuple(parse_line(line) for line in lines)
    return parsed


def parse_line(line: str) -> ProblemLine:
    s = line.split(",")
    return parse_sub_line(s[0]), parse_sub_line(s[1])


def parse_sub_line(sub_line: str) -> tuple[int, int]:
    s = sub_line.split("-")
    return int(s[0]), int(s[1])


if __name__ == "__main__":
    print(AdventOfCodeProblem202204().solve_all())
