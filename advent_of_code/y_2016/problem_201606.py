from dataclasses import dataclass

import pandas as pd

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = pd.DataFrame


@dataclass(kw_only=True)
class AdventOfCodeProblem201606(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2016
    day: int = 6

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return pd.DataFrame([list(el) for el in text.strip().split("\n")])

    def solve_part_1(self, puzzle_input: PuzzleInput):
        return "".join(list(puzzle_input.mode().loc[0]))

    def solve_part_2(self, puzzle_input: PuzzleInput):
        df = puzzle_input
        return "".join(
            df[col].value_counts(ascending=True).index[0]
            for col in df  # type: ignore
        )


if __name__ == "__main__":
    print(AdventOfCodeProblem201606().solve())
