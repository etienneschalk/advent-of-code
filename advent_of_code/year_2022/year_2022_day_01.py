from dataclasses import dataclass

from advent_of_code.protocols import AdventOfCodeProblem

type PuzzleInput = list[list[int]]


@dataclass(kw_only=True)
class AdventOfCodeProblem202201(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2022
    day: int = 1

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input(text)

    def solve_part_1(self, puzzle_input: PuzzleInput):
        result = compute_max_calories_part_1(puzzle_input)
        return result

    def solve_part_2(self, puzzle_input: PuzzleInput):
        result = compute_max_calories_part_2(puzzle_input)
        return result


def compute_max_calories_part_1(parsed_input: PuzzleInput) -> int:
    return max(sum(group) for group in parsed_input)


def compute_max_calories_part_2(parsed_input: PuzzleInput, limit: int = 3) -> int:
    return sum(sorted((sum(group) for group in parsed_input), reverse=True)[:limit])


def parse_text_input(text: str) -> PuzzleInput:
    return [[int(n) for n in group.split("\n")] for group in text.strip().split("\n\n")]


if __name__ == "__main__":
    print(AdventOfCodeProblem202201().solve())
