from dataclasses import dataclass

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = list[list[str]]


@dataclass(kw_only=True)
class AdventOfCodeProblem201625(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2016
    day: int = 25

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        text = text.strip()
        instructions = [line.split(" ") for line in text.split("\n")]
        return instructions

    def solve_part_1(self, puzzle_input: PuzzleInput):
        # Good old bruteforce works this one, no need to detect some permanent state loop!
        for a in range(200):
            registers = {"a": a, "b": 0, "c": 0, "d": 0}
            success = run_program(puzzle_input, registers)
            if success:
                print(f"Success for {a=}")
                return a
        return -1

    def solve_part_2(self, puzzle_input: PuzzleInput):
        return "No part 2"


def run_program(
    instructions: PuzzleInput, registers: dict[str, int], *, verbose: bool = False
) -> int:
    cursor = 0
    exec_count = 0
    program_length = len(instructions)
    out = 1  # we want a sequence of 0, 1, 0, 1... so start at 1 for comparison

    MAX_EXEC_COUNT = 40000
    while cursor < program_length and (exec_count < MAX_EXEC_COUNT):
        instr = instructions[cursor]
        cursor += 1
        exec_count += 1
        if verbose and exec_count % 100 == 0:
            print(
                f"    {exec_count:05d} {cursor:02d} {" ".join(instr):<12} "
                f"{"|".join(f"{k}:{v:>5}" for k,v in registers.items())}"
            )

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
            case "out":
                value_or_register = instr[1]
                if value_or_register.isnumeric():
                    value = int(value_or_register)
                else:
                    value = registers[value_or_register]
                if value == out:
                    return False  # same value :/
                out = value

    return True


if __name__ == "__main__":
    print(AdventOfCodeProblem201625().solve())
