from dataclasses import dataclass

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = list[str]


@dataclass(kw_only=True)
class AdventOfCodeProblem201607(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2016
    day: int = 7

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return text.strip().split("\n")

    def solve_part_1(self, puzzle_input: PuzzleInput):
        validities = []
        for line in puzzle_input:
            hypernet = False
            valid = False
            for i in range(3, len(line)):
                if line[i] == "[":
                    hypernet = True
                elif line[i] == "]":
                    hypernet = False
                elif line[i] == line[i - 1] == line[i - 2] == line[i - 3]:
                    # All same four characters are not a valid abba sequence.
                    pass
                else:
                    if (line[i] == line[i - 3]) and (line[i - 1] == line[i - 2]):
                        if hypernet:
                            valid = False
                            break
                        else:
                            valid = True
            validities.append(valid)
        return sum(validities)

    def solve_part_2(self, puzzle_input: PuzzleInput):
        validities = []
        all_candidates = []
        for line in puzzle_input:
            candidates = {False: set(), True: set()}
            hypernet = False
            for i in range(2, len(line)):
                if line[i] == "[":
                    hypernet = True
                elif line[i] == "]":
                    hypernet = False
                elif line[i] == line[i - 1] == line[i - 2]:
                    # All same three characters are not a valid abba sequence.
                    pass
                elif line[i - 1] in "[]":
                    # Avoid the case where a square bracket is the middle letter
                    pass
                else:
                    if line[i] == line[i - 2]:
                        couple = (
                            (line[i - 1], line[i])
                            if hypernet
                            else (line[i], line[i - 1])
                        )
                        candidates[hypernet].add(couple)
            print(candidates)
            all_candidates.append(candidates)
        intersections = [set.intersection(c[False], c[True]) for c in all_candidates]
        print(intersections)
        validities = [len(inter) > 0 for inter in intersections]
        print(validities)
        return sum(validities)


if __name__ == "__main__":
    print(AdventOfCodeProblem201607().solve())
