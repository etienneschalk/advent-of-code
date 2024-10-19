import re
from dataclasses import dataclass
from typing import Iterator, Self

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = ProblemData


@dataclass(kw_only=True, frozen=True)
class ProblemData:
    instructions: list["Instruction"]
    content: str


@dataclass(kw_only=True, frozen=True)
class Instruction:
    width: int
    repeat: int
    span: tuple[int, int]

    @classmethod
    def parse_list_from_text(cls, text: str) -> list[Self]:
        instructions = [
            cls(
                width=int(_match.group(2)),
                repeat=int(_match.group(3)),
                span=_match.span(),
            )
            for _match in re.finditer(r"(\((\d+)x(\d+)\))+?", text)
        ]
        return instructions


@dataclass(kw_only=True)
class AdventOfCodeProblem201609(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2016
    day: int = 9

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        text = text.strip()
        instructions = Instruction.parse_list_from_text(text)
        return ProblemData(instructions=instructions, content=text)

    def solve_part_1(self, puzzle_input: PuzzleInput):
        concat = self.solve_part_1_internal(puzzle_input)
        return len(concat)

    def solve_part_1_internal(self, puzzle_input: PuzzleInput) -> str:
        instructions = puzzle_input.instructions
        content = puzzle_input.content

        cursor: int = 0
        decoded: list[str] = []
        instr_iter: Iterator[Instruction] = iter(instructions)
        instr = next(instr_iter, None)

        while instr and (cursor < len(content)):
            print(instr)
            decoded.append(content[cursor : instr.span[0]])
            start = instr.span[1]
            cursor = start + instr.width
            decoded.append(content[start:cursor] * instr.repeat)

            # Skip instructions that are part of the data segment.
            while instr and instr.span[0] < cursor:
                instr = next(instr_iter, None)

        # Add the rest of the text.
        decoded.append(content[cursor:])
        print(decoded)
        concat = "".join(decoded)
        return concat

    def solve_part_2(self, puzzle_input: PuzzleInput):
        return -1


if __name__ == "__main__":
    print(AdventOfCodeProblem201609().solve())
