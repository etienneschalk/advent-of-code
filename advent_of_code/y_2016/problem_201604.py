import re
from collections import Counter
from dataclasses import dataclass

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = list[list[str]]


@dataclass(kw_only=True)
class AdventOfCodeProblem201604(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2016
    day: int = 4

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return [
            [str(found) for found in re.search(r"(.+)-(\d+)\[(.+)\]", line).groups()]  # type:ignore
            for line in text.strip().split("\n")
        ]

    def solve_part_1(self, puzzle_input: PuzzleInput):
        counted = [
            (el, Counter(el[0].replace("-", "")).most_common()) for el in puzzle_input
        ]
        result = sum(
            int(room[0][1])
            for room in counted
            if "".join(el[0] for el in sorted(room[1], key=lambda x: (-x[1], x[0])))[:5]
            == room[0][2]
        )
        return result

    def solve_part_2(self, puzzle_input: PuzzleInput):
        counted = [
            (el, Counter(el[0].replace("-", "")).most_common()) for el in puzzle_input
        ]
        filtered = [
            room[0]
            for room in counted
            if "".join(el[0] for el in sorted(room[1], key=lambda x: (-x[1], x[0])))[:5]
            == room[0][2]
        ]
        couples = [
            (
                "".join(
                    (
                        " "
                        if c == "-"
                        else chr((((ord(c) - ord("a")) + int(room[1])) % 26) + ord("a"))
                    )
                    for c in room[0]
                ),
                int(room[1]),
            )
            for room in filtered
        ]
        north_pole_storage_room_id = [
            room_id for string, room_id in couples if "northpole" in string
        ][0]
        return north_pole_storage_room_id


if __name__ == "__main__":
    print(AdventOfCodeProblem201604().solve())
