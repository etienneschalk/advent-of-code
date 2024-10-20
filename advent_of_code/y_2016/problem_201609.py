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
        # Do not use the pre-parsed instruction, re-match them on the fly.
        decompressed_length = self.solve_part_2_internal(puzzle_input.content)
        return decompressed_length

    def solve_part_2_internal(self, content: str, cursor: int = 0) -> int:
        zone_end = len(content)

        total: int = 0
        while content:
            # https://stackoverflow.com/questions/20236775/
            # python-python-re-search-speed-optimization-for-long-string-lines
            # res = re.search(r"(\((\d+)x(\d+)\))+?", content)
            res = re.match(r"(.*?)(\((\d+)x(\d+)\))", content)
            if res is None:
                # Leaf case, return just the length of content
                return zone_end
            instr = Instruction.from_match_search(res)
            # Note: because of the usage of match instead of find, the span includes the prefix.
            data_segment_start = instr.span[1]
            data_segment_end = data_segment_start + instr.width
            prefix_len = data_segment_start - instr.span[0] - len(instr.representation)
            data_segment = content[data_segment_start:data_segment_end]
            recursive_result = self.solve_part_2_internal(data_segment)
            total += prefix_len + instr.repeat * recursive_result
            content = content[data_segment_end:]
        return total
        # total: int = 0
        # cursor: int = 0
        # instr_idx: int = 0
        # instr = instructions[instr_idx]
        # prefix_length = instr.span[0] - cursor
        # start = instr.span[1]
        # end = start + instr.width
        # suffix = zone_end - cursor
        # # Recursive but look ahead next instr to check if valid
        # # to avoid looping when should not
        # decoded_length = prefix_length + total * instr.repeat + suffix
        # return decoded_length


# def solve_part_2_internal(self, puzzle_input: PuzzleInput) -> str:
#     instructions = puzzle_input.instructions
#     content = puzzle_input.content

#     cursor: int = 0
#     decoded: list[str] = []
#     instr_iter: Iterator[Instruction] = iter(instructions)
#     instr = next(instr_iter, None)

#     decoded_length, cursor = self.decode_recursive(
#         puzzle_input, cursor, len(content), instr, instr_iter
#     )
#     # assert cursor == len(content)
#     return decoded_length

# def decode_recursive(
#     self,
#     puzzle_input: PuzzleInput,
#     cursor: int,
#     zone_end: int,
#     instr: Instruction,
#     instr_iter: Iterator[Instruction],
# ) -> int:
#     if instr is None:
#         return zone_end - cursor, zone_end
#     prefix_length = instr.span[0] - cursor
#     start = instr.span[1]
#     cursor = start + instr.width
#     total = 0
#     c = start
#     print(
#         f"Outer {instr=} {prefix_length=} {start=} {zone_end=} {cursor=} {total=} {c=}"
#     )
#     while c < cursor:
#         instr = next(instr_iter, None)
#         ll, c = self.decode_recursive(puzzle_input, c, cursor, instr, instr_iter)
#         total += ll
#         print(
#             f"Inner {prefix_length=} {start=} {zone_end=} {cursor=} {total=} {c=} {ll=}"
#         )

#     suffix = zone_end - cursor
#     decoded_length = prefix_length + total * instr.repeat + suffix
#     return decoded_length, cursor


if __name__ == "__main__":
    print(AdventOfCodeProblem201609().solve())
