from dataclasses import dataclass
from typing import Mapping

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = str


@dataclass(kw_only=True)
class AdventOfCodeProblem201602(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2016
    day: int = 2

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return text

    def solve_part_1(self, puzzle_input: PuzzleInput):
        next_state: Mapping[str, Mapping[str | int, str | int]] = {
            "R": {1: 2, 2: 3, 3: 3, 4: 5, 5: 6, 6: 6, 7: 8, 8: 9, 9: 9},
            "L": {1: 1, 2: 1, 3: 2, 4: 4, 5: 4, 6: 5, 7: 7, 8: 7, 9: 8},
            "D": {1: 4, 4: 7, 7: 7, 2: 5, 5: 8, 8: 8, 3: 6, 6: 9, 9: 9},
            "U": {1: 1, 4: 1, 7: 4, 2: 2, 5: 2, 8: 5, 3: 3, 6: 3, 9: 6},
        }
        return solve(next_state, puzzle_input)

    def solve_part_2(self, puzzle_input: PuzzleInput):
        A = "A"
        B = "B"
        C = "C"
        D = "D"

        next_state = {
            "R": {
                1: 1,
                2: 3,
                3: 4,
                4: 4,
                5: 6,
                6: 7,
                7: 8,
                8: 9,
                9: 9,
                A: B,
                B: C,
                C: C,
                D: D,
            },
            "L": {
                1: 1,
                2: 2,
                3: 2,
                4: 3,
                5: 5,
                6: 5,
                7: 6,
                8: 7,
                9: 8,
                A: A,
                B: A,
                C: B,
                D: D,
            },
            "D": {
                1: 3,
                2: 6,
                3: 7,
                4: 8,
                5: 5,
                6: A,
                7: B,
                8: C,
                9: 9,
                A: A,
                B: D,
                C: C,
                D: D,
            },
            "U": {
                1: 1,
                2: 2,
                3: 1,
                4: 4,
                5: 5,
                6: 2,
                7: 3,
                8: 4,
                9: 9,
                A: 6,
                B: 7,
                C: 8,
                D: B,
            },
        }
        return solve(next_state, puzzle_input)


def solve(
    next_state: Mapping[str, Mapping[str | int, str | int]], puzzle_input: str
) -> str:
    lines = puzzle_input.strip().split("\n")
    position = 5
    positions = []
    for line in lines:
        for transition in line:
            position = next_state[transition][position]
        positions.append(position)
    return "".join(str(p) for p in positions)


if __name__ == "__main__":
    print(AdventOfCodeProblem201602().solve())
