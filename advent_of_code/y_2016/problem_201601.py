from dataclasses import dataclass
from typing import Literal

from advent_of_code.common.protocols import AdventOfCodeProblem

type Direction = Literal["L", "R"]
type PuzzleInput = list[tuple[Direction, int]]


@dataclass(kw_only=True)
class AdventOfCodeProblem201601(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2016
    day: int = 1

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return [(el[0], int(el[1:])) for el in text.strip().split(", ")]  # type: ignore

    def solve_part_1(self, puzzle_input: PuzzleInput):
        orientation = 0  # 0 N, 1 E, 2 S, 3 W, increases when turning right (clockwise)
        quantities = [0, 0, 0, 0]  # 0 N, 1 E, 2 S, 3 W
        for direction, quantity in puzzle_input:
            sign = 1 if direction == "R" else -1
            orientation = (orientation + sign) % 4
            quantities[orientation] += quantity
        dn = quantities[0] - quantities[2]
        de = quantities[0 + 1] - quantities[2 + 1]
        result = abs(dn) + abs(de)
        return result

    def solve_part_2(self, puzzle_input: PuzzleInput):
        return 0


if __name__ == "__main__":
    print(AdventOfCodeProblem201601().solve())
