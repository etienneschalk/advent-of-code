import itertools
from dataclasses import dataclass
from typing import Any

import numpy as np
import numpy.typing as npt

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = npt.NDArray[np.integer[Any]]


@dataclass(kw_only=True)
class AdventOfCodeProblem201907(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2019
    day: int = 7

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return np.array([int(word) for word in text.strip().split(",")], dtype=int)

    def solve_part_1(self, puzzle_input: PuzzleInput) -> int:
        program = puzzle_input
        max_output = -1  # assume not negative
        max_setting_sequence = None
        for setting_sequence in itertools.permutations(range(0, 4 + 1), 5):
            output = [0]
            for amplifier in range(4 + 1):
                the_inputs = [setting_sequence[amplifier], output[0]]
                output = run_program(program.copy(), the_inputs)
            if output[0] > max_output:
                max_setting_sequence = setting_sequence
                max_output = output[0]
            print(setting_sequence, output)
        print(max_setting_sequence)
        return max_output

    def solve_part_2(self, puzzle_input: PuzzleInput):
        print("\n".join(represent_program(puzzle_input.copy())))
        max_output = -1  # assume not negative
        max_setting_sequence = None
        for setting_sequence in itertools.permutations(range(5, 9 + 1), 5):
            # Instanciate once the programs, keep them running in the amplifiers.
            programs = [puzzle_input.copy() for _ in range(5)]
            # Start with negative offset as inc of amplifier ID is first instr in the loop.
            amplifier = -1
            # Store program pointers of each amplifier for context switching
            pcs = [0] * 5
            # The simulation terminates when all amplifiers alt.
            terminated = [False] * 5
            # Initial signals are made up of the setting sequence.
            signals = [[value] for value in setting_sequence]
            # An initial signal of value is injected one for the first amplifier.
            signals[0].append(0)
            # Filled after each amplifier program run, output of amp N is input of amp N+1
            output = []
            while True:
                amplifier = (amplifier + 1) % 5
                signals[amplifier].extend(output)
                print(amplifier, pcs, signals, output)
                output = run_program(
                    programs[amplifier], signals[amplifier], pcs[amplifier]
                )
                # Should contain something like: [output_signal, opcode, pc]
                # Retrieve the last opcode to know if the program did halt
                opcode = output.pop(-1)
                # Retrieve the pc for later context switching (round robin)
                pc = output.pop(-1)
                pcs[amplifier] = pc
                if opcode == 99:
                    print("halt")
                    terminated[amplifier] = True
                    if all(terminated):
                        break
            if output[0] > max_output:
                max_setting_sequence = setting_sequence
                max_output = output[0]
        print(max_setting_sequence)
        return max_output


def represent_program(program) -> list[str]:
    # Not 100% reliable as instructions and data are mixed together.
    # Data can be interpreted as instructions, which is incorrect.
    # Only for testing purposes.
    pc = 0  # program     pc = 0  # Program Counter
    sb: list[str] = []  # string builder

    # c should always be 0 for opcode 1 and 2, as 3rd param is dest.
    while True:
        if pc >= program.size:
            break

        instruction = program[pc]
        opcode = instruction % 100
        c = (instruction % 1000) // 100
        b = (instruction % 10000) // 1000
        a = (instruction % 100000) // 10000

        # print(instruction, pc, sb)

        if pc < program.size - 1:
            address_1 = program[pc + 1]

        if (pc < program.size - 2) and opcode in (1, 2, 5, 6, 7, 8):
            address_2 = program[pc + 2]

        if (pc < program.size - 3) and opcode in (1, 2, 7, 8):
            address_3 = program[pc + 3]

        if opcode == 1:
            # addition
            sb.append(
                "add "
                f"{"&" if c == 0 else " "}{address_1}"  # type: ignore
                " "
                f"{"&" if b == 0 else " "}{address_2}"  # type: ignore
                " "
                f"{"&" if a == 0 else " "}{address_3}"  # type: ignore
            )
            pc += 4
        elif opcode == 2:
            # multiplication
            sb.append(
                "mul "
                f"{"&" if c == 0 else " "}{address_1}"  # type: ignore
                " "
                f"{"&" if b == 0 else " "}{address_2}"  # type: ignore
                " "
                f"{"&" if a == 0 else " "}{address_3}"  # type: ignore
            )
            pc += 4
        elif opcode == 3:
            # input
            sb.append("in_ " f"{"&" if c == 0 else " "}{address_1}")  # type: ignore
            # note: should wait if no input available, and give turn to the next program
            # in a round-robin fashion
            pc += 2
        elif opcode == 4:
            # output
            sb.append("out " f"{"&" if c == 0 else " "}{address_1}")  # type: ignore
            pc += 2
        elif opcode == 5:
            # jump-if-true
            sb.append(
                "jnz "
                f"{"&" if c == 0 else " "}{address_1}"  # type: ignore
                " "
                f"{"&" if b == 0 else " "}{address_2}"  # type: ignore
            )
            pc += 3
        elif opcode == 6:
            # jump-if-false
            sb.append(
                "jnz "  # type: ignore
                f"{"&" if c == 0 else " "}{address_1}"  # type: ignore
                " "
                f"{"&" if b == 0 else " "}{address_2}"  # type: ignore
            )
            pc += 3
        elif opcode == 7:
            # less than
            sb.append(
                "lt_ "
                f"{"&" if c == 0 else " "}{address_1}"  # type: ignore
                " "
                f"{"&" if b == 0 else " "}{address_2}"  # type: ignore
                " "
                f"{"&" if a == 0 else " "}{address_3}"  # type: ignore
            )
            pc += 4
        elif opcode == 8:
            # equals
            sb.append(
                "eq_ "
                f"{"&" if c == 0 else " "}{address_1}"  # type: ignore
                " "
                f"{"&" if b == 0 else " "}{address_2}"  # type: ignore
                " "
                f"{"&" if a == 0 else " "}{address_3}"  # type: ignore
            )
            pc += 4
        elif opcode == 99 and instruction == 99:  # avoid interpreting 99999:
            sb.append("hlt")
            pc += 1
        else:  # what?
            pc += 1

    sb.append(f"{(program.size)=}")
    return sb


def run_program(program, the_inputs: list[int], pc: int = 0) -> list[int]:
    the_output = []

    # pc: Program Counter

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
            # note: should wait if no input available, and give turn to the next program
            # in a round-robin fashion
            if the_inputs:
                program[address_1] = the_inputs.pop(0)
                pc += 2
            else:
                break
                # # give hand to the next processor
                # # remember pc, add it last
                # the_output.append(pc)
                # return the_output
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

    # give hand to the next processor
    # remember pc, add it last
    the_output.append(pc)
    the_output.append(opcode)
    return the_output


if __name__ == "__main__":
    print(AdventOfCodeProblem201907().solve())
