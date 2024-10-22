from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = npt.NDArray[np.integer]


@dataclass(kw_only=True)
class AdventOfCodeProblem201902(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2019
    day: int = 2

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return np.array([int(word) for word in text.strip().split(",")], dtype=int)

    def solve_part_1(self, puzzle_input: PuzzleInput):
        program = puzzle_input
        program[1] = 12
        program[2] = 2
        run_program(program)
        output = program[0]
        return output

    def solve_part_2(self, puzzle_input: PuzzleInput):
        target = 19690720
        for noun in range(100):
            for verb in range(100):
                program = puzzle_input.copy()
                program[1] = noun
                program[2] = verb
                run_program(program)
                output = program[0]
                if output == target:
                    return 100 * noun + verb
        return -1


def run_program(program):
    pc = 0  # Program Counter
    while program[pc] != 99:
        if program[pc] == 1:
            program[program[pc + 3]] = (
                program[program[pc + 1]] + program[program[pc + 2]]
            )
            pc += 4
        elif program[pc] == 2:
            program[program[pc + 3]] = (
                program[program[pc + 1]] * program[program[pc + 2]]
            )
            pc += 4


if __name__ == "__main__":
    print(AdventOfCodeProblem201902().solve())
