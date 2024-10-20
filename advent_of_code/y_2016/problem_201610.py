"""
Note about re.match vs re.search on StackOverflow:
https://stackoverflow.com/questions/20236775/python-python-re-search-speed-optimization-for-long-string-lines
"""

import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Literal

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
        regexp_1 = r"value (\d+) goes to bot (\d+)"
        regexp_2 = (
            r"bot (\d+) gives low to (output|bot) (\d+) and high to (output|bot) (\d+)"
        )
        regexp = rf"({regexp_1}|{regexp_2})"

        _matches = re.finditer(regexp, text.strip())
        instructions = []
        for m in _matches:
            if m.group(4) is None:
                instr = InitInstruction(m.group(0), int(m.group(2)), int(m.group(3)))
            else:
                instr = BotInstruction(
                    m.group(0),
                    int(m.group(4)),
                    str(m.group(5)),  # type: ignore
                    int(m.group(6)),
                    str(m.group(7)),  # type: ignore
                    int(m.group(8)),
                )
            instructions.append(instr)

        return instructions

    def solve_part_1(self, puzzle_input: PuzzleInput):
        wanted_low_value = 17
        wanted_high_value = 61
        return self.solve_internal(puzzle_input, wanted_low_value, wanted_high_value, 1)

    def solve_part_2(self, puzzle_input: PuzzleInput):
        wanted_low_value = 17
        wanted_high_value = 61
        return self.solve_internal(puzzle_input, wanted_low_value, wanted_high_value, 2)

    def solve_internal(
        self,
        instructions: PuzzleInput,
        wanted_low_value: int,
        wanted_high_value: int,
        part: int,
    ) -> int:
        bot_dict: dict[int, Bot] = defaultdict(lambda: Bot([]))
        output_dict: dict[int, int] = {}

        bot_instructions: list[BotInstruction]
        remaining_instructions: list[BotInstruction] = []

        # Execute init instructions first, bot instructions second.
        for instr in instructions:
            if not isinstance(instr, InitInstruction):
                remaining_instructions.append(instr)
                continue
            bot_dict[instr.bot_id].values.append(instr.value)

        while remaining_instructions:
            bot_instructions = remaining_instructions
            remaining_instructions = []

            for instr in bot_instructions:
                giving_bot = bot_dict[instr.bot_id]

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

                if low_value == wanted_low_value and high_value == wanted_high_value:
                    print(f"Found #{instr.bot_id}: {giving_bot}")

                    if part == 1:
                        return instr.bot_id

                giving_bot.values.clear()

        product = output_dict[0] * output_dict[1] * output_dict[2]
        return product


if __name__ == "__main__":
    print(AdventOfCodeProblem201610().solve())
