from dataclasses import dataclass
from typing import Literal

import numpy as np

from advent_of_code.common.protocols import AdventOfCodeProblem

type Direction = Literal["L", "R"]
type PuzzleInput = list[int]


@dataclass(kw_only=True)
class AdventOfCodeProblem201901(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2019
    day: int = 1

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return [int(word) for word in text.strip().split("\n")]

    def solve_part_1(self, puzzle_input: PuzzleInput):
        return (np.array(puzzle_input) // 3 - 2).sum()

    def solve_part_2(self, puzzle_input: PuzzleInput):
        total = 0
        for value in puzzle_input:
            total_fuel = 0
            fuel = value // 3 - 2
            while fuel > 0:
                total_fuel += fuel
                fuel = fuel // 3 - 2
            print(total_fuel)
            total += total_fuel
        return total


if __name__ == "__main__":
    print(AdventOfCodeProblem201901().solve())
