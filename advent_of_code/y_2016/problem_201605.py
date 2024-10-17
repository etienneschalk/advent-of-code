import hashlib
from dataclasses import dataclass

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = str


@dataclass(kw_only=True)
class AdventOfCodeProblem201605(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2016
    day: int = 5

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return text

    def solve_part_1(self, puzzle_input: PuzzleInput):
        found = 0
        i = 0
        letters = []
        while found != 8:
            hash = hashlib.md5((puzzle_input + str(i)).encode()).hexdigest()
            if hash.startswith("00000"):
                letters.append(hash[5])
                found += 1
                print(i)
            i += 1
        result = "".join(letters)
        return result

    def solve_part_2(self, puzzle_input: PuzzleInput):
        found = 0
        i = 0
        letters = [" "] * 8
        while found != 8:
            hash = hashlib.md5((puzzle_input + str(i)).encode()).hexdigest()
            if hash.startswith("00000") and hash[5].isnumeric():
                index = int(hash[5])
                if (0 <= index < 8) and (letters[index] == " "):
                    found += 1
                    letters[index] = hash[6]
            i += 1
        result = "".join(letters)
        return result


if __name__ == "__main__":
    print(AdventOfCodeProblem201605().solve())
