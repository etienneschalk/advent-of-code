import re
from dataclasses import dataclass
from typing import Literal, Self

import numpy as np
import numpy.typing as npt

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = list[Instruction]

LETTER_TO_FONT = {
    "Z": """
[[####.]
 [...#.]
 [..#..]
 [.#...]
 [#....]
 [####.]]
""",
    "F": """
[[####.]
 [#....]
 [###..]
 [#....]
 [#....]
 [#....]]
""",
    "H": """
[[#..#.]
 [#..#.]
 [####.]
 [#..#.]
 [#..#.]
 [#..#.]]
""",
    "S": """
[[.###.]
 [#....]
 [#....]
 [.##..]
 [...#.]
 [###..]]
""",
    "O": """
[[.##..]
 [#..#.]
 [#..#.]
 [#..#.]
 [#..#.]
 [.##..]]
""",
    "G": """
[[.##..]
 [#..#.]
 [#....]
 [#.##.]
 [#..#.]
 [.###.]]
""",
    "P": """
[[###..]
 [#..#.]
 [#..#.]
 [###..]
 [#....]
 [#....]]
""",
}


FONT_TO_LETTER = {v.strip(): k for k, v in LETTER_TO_FONT.items()}


@dataclass(frozen=True)
class Instruction:
    name: Literal["rect", "rotate row", "rotate column"]
    left_operand: int
    right_operand: int

    @classmethod
    def parse_list_from_text(cls, text: str) -> list[Self]:
        return [
            cls(matches[0], int(matches[1]), int(matches[2]))
            for matches in re.findall(
                r"(rect|rotate row|rotate column).*?(\d+).*?(\d+)", text
            )
        ]


@dataclass(kw_only=True)
class AdventOfCodeProblem201608(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2016
    day: int = 8

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        parsed = Instruction.parse_list_from_text(text)
        return parsed

    def solve_part_1(self, puzzle_input: PuzzleInput):
        screen = np.zeros((6, 50), dtype=np.uint8)
        self.execute_instructions(puzzle_input, screen)
        print(np.array2string(screen, separator="").replace("0", ".").replace("1", "#"))
        # wrap in str for easier auto download input as part 2 is str
        return str(screen.sum())

    def solve_part_2(self, puzzle_input: PuzzleInput):
        screen = np.zeros((6, 50), dtype=np.uint8)
        self.execute_instructions(puzzle_input, screen)
        font_width = 5
        split_count = screen.shape[1] // font_width
        split_arrays = np.split(screen, split_count, axis=1)
        letters = [
            (
                np.array2string(split_array, separator="")
                .replace("0", ".")
                .replace("1", "#")
            )
            for split_array in split_arrays
        ]
        result = "".join(FONT_TO_LETTER[letter] for letter in letters)
        return result

    def execute_instructions(
        self, instructions: PuzzleInput, screen: npt.NDArray[np.uint8]
    ) -> None:
        """
        Interpret instructions

        Parameters
        ----------
        instructions
            List of Instructions to execute
        screen
            Screen mutated in-place.
        """
        for instruction in instructions:
            if instruction.name == "rect":
                screen[: instruction.right_operand, : instruction.left_operand] = 1
            elif instruction.name == "rotate row":
                screen[instruction.left_operand] = np.roll(
                    screen[instruction.left_operand], instruction.right_operand
                )
            elif instruction.name == "rotate column":
                screen[:, instruction.left_operand] = np.roll(
                    screen[:, instruction.left_operand], instruction.right_operand
                )


if __name__ == "__main__":
    print(AdventOfCodeProblem201608().solve())
