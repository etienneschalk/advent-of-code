from dataclasses import dataclass

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = list[list[str]]


@dataclass(kw_only=True)
class AdventOfCodeProblem201612(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2016
    day: int = 12

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        text = text.strip()
        instructions = [line.split(" ") for line in text.split("\n")]
        return instructions

    def solve_part_1(self, puzzle_input: PuzzleInput):
        registers = {"a": 0, "b": 0, "c": 0, "d": 0}
        return run_program(puzzle_input, registers)

    def solve_part_2(self, puzzle_input: PuzzleInput):
        registers = {"a": 0, "b": 0, "c": 1, "d": 0}
        return run_program(puzzle_input, registers)


def run_program(instructions: PuzzleInput, registers: dict[str, int]) -> int:
    cursor = 0
    program_length = len(instructions)

    while cursor < program_length:
        instr = instructions[cursor]
        cursor += 1

        match instr[0]:
            case "inc":
                registers[instr[1]] += 1
            case "dec":
                registers[instr[1]] -= 1
            case "cpy":
                value_or_register = instr[1]
                register = instr[2]
                if value_or_register.isnumeric():
                    registers[register] = int(value_or_register)
                else:
                    registers[register] = registers[value_or_register]
            case "jnz":
                value_or_register = instr[1]
                distance = instr[2]
                if value_or_register.isnumeric():
                    value = int(value_or_register)
                else:
                    value = registers[value_or_register]
                if value != 0:
                    cursor += int(distance) - 1  # -1 for the global inc

    return registers["a"]


if __name__ == "__main__":
    print(AdventOfCodeProblem201612().solve())
