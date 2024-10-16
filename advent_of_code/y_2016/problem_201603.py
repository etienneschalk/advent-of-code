import itertools
import re
from dataclasses import dataclass

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = list[list[int]]


@dataclass(kw_only=True)
class AdventOfCodeProblem201603(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2016
    day: int = 3

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return [
            [int(f) for f in re.findall(r"\d+", line)]
            for line in text.strip().split("\n")
        ]

    def solve_part_1(self, puzzle_input: PuzzleInput):
        # Not: flat triangle not allowed hence strict equality
        return sum(
            (tri[0] + tri[1]) > tri[2] for tri in (sorted(tri) for tri in puzzle_input)
        )

    def solve_part_2(self, puzzle_input: PuzzleInput):
        # Read groups of 3 vertically (transpose by blocks of 3x3)
        puzzle_input_altered = list(
            [batch[0][i], batch[1][i], batch[2][i]]
            for batch in itertools.batched(puzzle_input, 3)
            for i in range(3)
        )
        return self.solve_part_1(puzzle_input_altered)


if __name__ == "__main__":
    print(AdventOfCodeProblem201603().solve())
