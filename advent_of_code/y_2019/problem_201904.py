from dataclasses import dataclass

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = tuple[int, int]


@dataclass(kw_only=True)
class AdventOfCodeProblem201904(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2019
    day: int = 4

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        split = [int(w) for w in text.strip().split("-")]
        return split[0], split[1]

    def solve_part_1(self, puzzle_input: PuzzleInput):
        start, end = puzzle_input
        counter = 0
        for n in range(start, end + 1):
            w = str(n)
            digits = [int(d) for d in w]
            # order and presence of doubles
            if (sorted(digits) == digits) and any(
                digits[i] == digits[i + 1] for i in range(len(w) - 1)
            ):
                counter += 1
        return counter

    def solve_part_2(self, puzzle_input: PuzzleInput):
        start, end = puzzle_input
        counter = 0
        for n in range(start, end + 1):
            w = str(n)
            digits = [int(d) for d in w]
            # order and presence of doubles
            if (sorted(digits) == digits) and any(
                digits[i] == digits[i + 1] for i in range(len(w) - 1)
            ):
                if (
                    (digits[0] == digits[1] and digits[1] != digits[2])
                    or (digits[-1] == digits[-2] and digits[-2] != digits[-3])
                    or any(
                        (
                            digits[i] != digits[i + 1]
                            and digits[i + 1] == digits[i + 2]
                            and digits[i + 2] != digits[i + 3]
                        )
                        for i in range(len(w) - 2)
                    )
                ):
                    counter += 1
        return counter


if __name__ == "__main__":
    print(AdventOfCodeProblem201904().solve())
