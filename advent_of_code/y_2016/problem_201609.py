"""
Note about re.match vs re.search on StackOverflow:
https://stackoverflow.com/questions/20236775/python-python-re-search-speed-optimization-for-long-string-lines
"""

import re
from dataclasses import dataclass
from typing import Iterator, Self

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = str


@dataclass(kw_only=True, frozen=True)
class Instruction:
    width: int
    repeat: int
    span: tuple[int, int]
    representation: str

    @classmethod
    def parse_list_from_text(cls, text: str) -> list[Self]:
        instructions = [
            cls.from_match_finditer(_match)
            for _match in re.finditer(r"(\((\d+)x(\d+)\))+?", text)
        ]
        return instructions

    @classmethod
    def from_match_finditer(cls, _match: re.Match) -> Self:
        return cls(
            width=int(_match.group(2)),
            repeat=int(_match.group(3)),
            span=_match.span(),
            representation=_match.group(0),
        )

    @classmethod
    def from_match_search(cls, _match: re.Match) -> Self:
        return cls(
            width=int(_match.group(3)),
            repeat=int(_match.group(4)),
            span=_match.span(),
            representation=_match.group(2),
        )


@dataclass(kw_only=True)
class AdventOfCodeProblem201609(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2016
    day: int = 9

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return text.strip()

    def solve_part_1(self, puzzle_input: PuzzleInput):
        instructions = Instruction.parse_list_from_text(puzzle_input)
        concat = self.solve_part_1_internal(instructions, puzzle_input)
        return len(concat)

    def solve_part_1_internal(
        self, instructions: list[Instruction], content: str
    ) -> str:
        cursor: int = 0
        decoded: list[str] = []
        instr_iter: Iterator[Instruction] = iter(instructions)
        instr = next(instr_iter, None)

        while instr and (cursor < len(content)):
            decoded.append(content[cursor : instr.span[0]])
            start = instr.span[1]
            cursor = start + instr.width
            decoded.append(content[start:cursor] * instr.repeat)

            # Skip instructions that are part of the data segment.
            while instr and instr.span[0] < cursor:
                instr = next(instr_iter, None)

        # Add the rest of the text.
        decoded.append(content[cursor:])
        return "".join(decoded)

    def solve_part_2(self, puzzle_input: PuzzleInput):
        # Do not use the pre-parsed instruction, re-match them on the fly.
        decompressed_length = self.solve_part_2_internal(puzzle_input)
        return decompressed_length

    def solve_part_2_internal(self, content: str) -> int:
        total: int = 0

        while content:
            # Note the (.*?) to consume the beginning of the string.
            _match = re.match(r"(.*?)(\((\d+)x(\d+)\))", content)

            if _match is None:
                return total + len(content)  # Leaf case, no more instructions.

            # Note: Because of the usage of re.match instead of find, the span includes the prefix.
            instr = Instruction.from_match_search(_match)
            start = instr.span[1]
            end = start + instr.width
            prefix = start - instr.span[0] - len(instr.representation)
            decompressed = self.solve_part_2_internal(content[start:end])
            total += prefix + instr.repeat * decompressed
            content = content[end:]

        return total


if __name__ == "__main__":
    print(AdventOfCodeProblem201609().solve())
