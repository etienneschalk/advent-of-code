import itertools
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = npt.NDArray[np.integer]


@dataclass(kw_only=True)
class AdventOfCodeProblem201907(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2019
    day: int = 7

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return np.array([int(word) for word in text.strip().split(",")], dtype=int)

    def solve_part_1(self, puzzle_input: PuzzleInput):
        program = puzzle_input.copy()
        # TODO unit tests
        max_input = -1  # assume not negative...
        max_setting_sequence = None
        for setting_sequence in itertools.permutations(range(4 + 1), 5):
            input = [0]
            for amplifier in range(4 + 1):
                the_inputs = [setting_sequence[amplifier], input[0]]
                input = run_program([*program], the_inputs)
            if (max_input is None) or (input[0] > max_input):
                max_setting_sequence = setting_sequence
                max_input = input[0]
            print(setting_sequence, input)
        print(max_setting_sequence)
        return max_input

    def solve_part_2(self, puzzle_input: PuzzleInput):
        return -1


def run_program(program, the_inputs: list[int]) -> list[int]:
    the_output = []

    pc = 0  # Program Counter

    # c should always be 0 for opcode 1 and 2, as 3rd param is dest.
    while True:
        instruction = program[pc]
        opcode = instruction % 100
        c = (instruction % 1000) // 100
        b = (instruction % 10000) // 1000
        # a = (instruction % 100000) // 10000

        # print("-----")
        # print(f"{instruction:07d}", a, b, c, f"{opcode:02d}")

        if opcode == 99:
            break

        address_1 = program[pc + 1]
        if c == 0:
            value_1 = program[address_1]
        else:
            value_1 = address_1
        # print(address_1, value_1)

        if opcode in (1, 2, 5, 6, 7, 8):
            address_2 = program[pc + 2]
            if b == 0:
                value_2 = program[address_2]
            else:
                value_2 = address_2
            # print(address_2, value_2)

        if opcode in (1, 2, 7, 8):
            address_3 = program[pc + 3]
            # if a == 0:
            #     value_3 = program[address_3]
            # else:
            #     value_3 = address_3
            # print(address_3, value_3)

        if opcode == 1:
            # addition
            program[address_3] = value_1 + value_2  # type: ignore
            pc += 4
        elif opcode == 2:
            # multiplication
            program[address_3] = value_1 * value_2  # type: ignore
            pc += 4
        elif opcode == 3:
            # input
            program[address_1] = the_inputs.pop(0)
            pc += 2
        elif opcode == 4:
            # output
            the_output.append(value_1)
            pc += 2
        elif opcode == 5:
            # jump-if-true
            if value_1:
                pc = value_2  # type: ignore
            else:
                pc += 3
        elif opcode == 6:
            # jump-if-false
            if value_1:
                pc += 3
            else:
                pc = value_2  # type: ignore
        elif opcode == 7:
            # less than
            program[address_3] = int(value_1 < value_2)  # type: ignore
            pc += 4
        elif opcode == 8:
            # equals
            program[address_3] = int(value_1 == value_2)  # type: ignore
            pc += 4

    # print(the_output)
    # print("END")
    return the_output


if __name__ == "__main__":
    print(AdventOfCodeProblem201907().solve())
