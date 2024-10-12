# from dataclasses import dataclass
# from typing import Literal

# from advent_of_code.common.protocols import AdventOfCodeProblem

# type Direction = Literal["L", "R"]
# type PuzzleInput = list[tuple[Direction, int]]


# @dataclass(kw_only=True)
# class AdventOfCodeProblem201601(AdventOfCodeProblem[PuzzleInput]):
#     year: int = 2016
#     day: int = 1

#     @staticmethod
#     def parse_text_input(text: str) -> PuzzleInput:
#         return [(el[0], int(el[1])) for el in text.strip().split(", ")]

#     def solve_part_1(self, puzzle_input: PuzzleInput):
#         print(puzzle_input)
#         return result

#     def solve_part_2(self, puzzle_input: PuzzleInput):
#         return result


# if __name__ == "__main__":
#     print(AdventOfCodeProblem201601().solve())
