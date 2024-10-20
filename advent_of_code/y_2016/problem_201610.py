"""
Note about re.match vs re.search on StackOverflow:
https://stackoverflow.com/questions/20236775/python-python-re-search-speed-optimization-for-long-string-lines
"""

from collections import defaultdict
import re
from dataclasses import dataclass
from typing import Iterator, Literal, Self

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = list[InitInstruction | BotInstruction]


@dataclass(frozen=True)
class Bot:
    values: list[int]

    @property
    def low(self) -> int:
        return min(self.values)

    @property
    def high(self) -> int:
        return max(self.values)


@dataclass(frozen=True)
class InitInstruction:
    representation: str
    value: int
    bot_id: int


@dataclass(frozen=True)
class BotInstruction:
    representation: str
    bot_id: int
    low_target_type: Literal["bot", "output"]
    low_target_id: int
    high_target_type: Literal["bot", "output"]
    high_target_id: int


@dataclass(kw_only=True)
class AdventOfCodeProblem201610(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2016
    day: int = 10

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        text text.strip()
        regexp_1 = r"value (\d+) goes to bot (\d+)"
        regexp_2 = (
            r"bot (\d+) gives low to (output|bot) (\d+) and high to (output|bot) (\d+)"
        )
        regexp = rf"({regexp_1}|{regexp_2})"
        print(regexp)
        _matches = list(re.finditer(regexp, puzzle_input))
        print(puzzle_input)
        print(_matches)
        instructions = []
        for m in _matches:
            if m.group(4) is None:
                instr = InitInstruction(m.group(0), int(m.group(2)), int(m.group(3)))
            else:
                instr = BotInstruction(
                    m.group(0),
                    int(m.group(4)),
                    m.group(5),
                    int(m.group(6)),
                    m.group(7),
                    int(m.group(8)),
                )
            print(instr)
            instructions.append(instr)
        return instructions

    def solve_part_1(self, puzzle_input: PuzzleInput):
        instructions = puzzle_input

        wanted_low_value = 2
        wanted_high_value = 5

        wanted_low_value = 17
        wanted_high_value = 61

        bot_dict: dict[int, Bot] = defaultdict(lambda: Bot([]))
        output_dict: dict[int, int] = {}

        found = None
        remaining_instructions = []

        # Execute init instructions first, bot instructions second.
        for instr in instructions:
            if not isinstance(instr, InitInstruction):
                remaining_instructions.append(instr)
                continue
            print()
            print("#", instr)
            print(dict(bot_dict))
            print(output_dict)

            bot_dict[instr.bot_id].values.append(instr.value)
        print(f"{bot_dict=}")
        print("-----")

        while remaining_instructions:
            instructions = remaining_instructions
            remaining_instructions = []
            for instr in instructions:
                print()
                print("Execute instruction:", instr)
                print(f"{dict(bot_dict)}=")
                print(f"{output_dict=}")

                giving_bot = bot_dict[instr.bot_id]
                print(f"{giving_bot=}")

                if len(giving_bot.values) < 2:
                    remaining_instructions.append(instr)
                    continue

                low_value = giving_bot.low
                if instr.low_target_type == "bot":
                    bot_dict[instr.low_target_id].values.append(low_value)
                else:
                    output_dict[instr.low_target_id] = low_value

                high_value = giving_bot.high
                if instr.high_target_type == "bot":
                    bot_dict[instr.high_target_id].values.append(high_value)
                else:
                    output_dict[instr.high_target_id] = high_value

                print(f"{low_value=} {high_value=}")
                if low_value == wanted_low_value and high_value == wanted_high_value:
                    print(f"Found #{instr.bot_id}: {giving_bot}")
                    found = instr.bot_id

                giving_bot.values.clear()

        print(dict(bot_dict))
        print(output_dict)
        print(f"{found=}")

        part_2 = output_dict[0] * output_dict[1] * output_dict[2]
        print(f"{part_2=}")

    def solve_part_2(self, puzzle_input: PuzzleInput):
        return -1


if __name__ == "__main__":
    print(AdventOfCodeProblem201610().solve())
