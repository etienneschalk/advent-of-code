from dataclasses import dataclass
from typing import Any

import numpy as np
import numpy.typing as npt

from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = npt.NDArray[np.integer[Any]]


@dataclass(kw_only=True)
class AdventOfCodeProblem201909(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2019
    day: int = 9

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return np.array([int(word) for word in text.strip().split(",")], dtype=int)

    def solve_part_1(self, puzzle_input: PuzzleInput) -> int:
        program = np.array(
            [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
        )
        program = np.pad(program, (0, 100))
        output = run_program(program.copy(), [])
        assert (np.array(output) == program[: len(output)]).all()

        program = np.array([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
        output = run_program(program.copy(), [])
        assert len(str(output[0])) == 16

        program = np.array([104, 1125899906842624, 99])
        output = run_program(program.copy(), [])
        assert output[0] == program[1]

        program = puzzle_input
        program = np.pad(program, (0, 973))
        output = run_program(program.copy(), [1])

        return output

    def solve_part_2(self, puzzle_input: PuzzleInput):
        program = puzzle_input
        program = np.pad(program, (0, 1073))
        output = run_program(program.copy(), [2])
        return output


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
                f"{"&" if c == 0 else " "}{address_1}"
                " "
                f"{"&" if b == 0 else " "}{address_2}"
                " "
                f"{"&" if a == 0 else " "}{address_3}"
            )
            pc += 4
        elif opcode == 2:
            # multiplication
            sb.append(
                "mul "
                f"{"&" if c == 0 else " "}{address_1}"
                " "
                f"{"&" if b == 0 else " "}{address_2}"
                " "
                f"{"&" if a == 0 else " "}{address_3}"
            )
            pc += 4
        elif opcode == 3:
            # input
            sb.append("in_ " f"{"&" if c == 0 else " "}{address_1}")
            # note: should wait if no input available, and give turn to the next program
            # in a round-robin fashion
            pc += 2
        elif opcode == 4:
            # output
            sb.append("out " f"{"&" if c == 0 else " "}{address_1}")
            pc += 2
        elif opcode == 5:
            # jump-if-true
            sb.append(
                "jnz "
                f"{"&" if c == 0 else " "}{address_1}"
                " "
                f"{"&" if b == 0 else " "}{address_2}"
            )
            pc += 3
        elif opcode == 6:
            # jump-if-false
            sb.append(
                "jnz "
                f"{"&" if c == 0 else " "}{address_1}"
                " "
                f"{"&" if b == 0 else " "}{address_2}"
            )
            pc += 3
        elif opcode == 7:
            # less than
            sb.append(
                "lt_ "
                f"{"&" if c == 0 else " "}{address_1}"
                " "
                f"{"&" if b == 0 else " "}{address_2}"
                " "
                f"{"&" if a == 0 else " "}{address_3}"
            )
            pc += 4
        elif opcode == 8:
            # equals
            sb.append(
                "eq_ "
                f"{"&" if c == 0 else " "}{address_1}"
                " "
                f"{"&" if b == 0 else " "}{address_2}"
                " "
                f"{"&" if a == 0 else " "}{address_3}"
            )
            pc += 4
        elif opcode == 99 and instruction == 99:  # avoid interpreting 99999:
            sb.append("hlt")
            pc += 1
        else:  # what?
            pc += 1

    sb.append(f"{(program.size)=}")
    return sb


def run_program(
    program, the_inputs: list[int], pc: int = 0, verbose: int = 0
) -> list[int]:
    the_output = []
    relative_base = 0
    # pc: Program Counter

    # c should always be 0 for opcode 1 and 2, as 3rd param is dest.
    while True:
        instruction = program[pc]
        opcode = instruction % 100
        c = (instruction % 1000) // 100
        b = (instruction % 10000) // 1000
        a = (instruction % 100000) // 10000

        if verbose > 0:
            print(f"{instruction:05d}", a, b, c, f"{opcode:02d}")

        if opcode == 99:
            break

        address_1 = program[pc + 1]
        if c == 0:
            value_1 = program[address_1]
        elif c == 2:
            address_1 += relative_base
            value_1 = program[address_1]
        else:
            value_1 = address_1

        if opcode in (1, 2, 5, 6, 7, 8):
            address_2 = program[pc + 2]
            if b == 0:
                value_2 = program[address_2]
            elif b == 2:
                address_2 += relative_base
                value_2 = program[address_2]
            else:
                value_2 = address_2
        else:
            address_2 = value_2 = None

        if opcode in (1, 2, 7, 8):
            address_3 = program[pc + 3]
            if a == 2:
                address_3 += relative_base
        else:
            address_3 = value_3 = None

        if verbose > 1:
            assembly_instr = render_instruction(
                opcode, c, b, a, address_1, address_2, address_3
            )
            print(assembly_instr)
        if opcode == 1:
            # addition
            program[address_3] = value_1 + value_2  # type: ignore
            pc += 4
        elif opcode == 2:
            # multiplication
            program[address_3] = value_1 * value_2  # type: ignore
            pc += 4
        elif opcode == 3:
            if the_inputs:
                program[address_1] = the_inputs.pop(0)
                pc += 2
            else:
                break
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
        elif opcode == 9:
            relative_base += value_1
            pc += 2

    if verbose > 0:
        print("END")
    return the_output


def render_instruction(
    opcode: int,
    c: int,
    b: int,
    a: int,
    address_1: int,
    address_2: int | None,
    address_3: int | None,
):
    if opcode == 1:
        # addition
        return (
            "add "
            f"{"&" if c == 0 else " "}{address_1}"
            " "
            f"{"&" if b == 0 else " "}{address_2}"
            " "
            f"{"&" if a == 0 else " "}{address_3}"
        )
    elif opcode == 2:
        # multiplication
        return (
            "mul "
            f"{"&" if c == 0 else " "}{address_1}"
            " "
            f"{"&" if b == 0 else " "}{address_2}"
            " "
            f"{"&" if a == 0 else " "}{address_3}"
        )
    elif opcode == 3:
        # input
        return "in_ " f"{"&" if c == 0 else " "}{address_1}"
    elif opcode == 4:
        # output
        return "out " f"{"&" if c == 0 else " "}{address_1}"
    elif opcode == 5:
        # jump-if-true
        return (
            "jnz "
            f"{"&" if c == 0 else " "}{address_1}"
            " "
            f"{"&" if b == 0 else " "}{address_2}"
        )
    elif opcode == 6:
        # jump-if-false
        return (
            "jnz "
            f"{"&" if c == 0 else " "}{address_1}"
            " "
            f"{"&" if b == 0 else " "}{address_2}"
        )
    elif opcode == 7:
        # less than
        return (
            "lt_ "
            f"{"&" if c == 0 else " "}{address_1}"
            " "
            f"{"&" if b == 0 else " "}{address_2}"
            " "
            f"{"&" if a == 0 else " "}{address_3}"
        )
    elif opcode == 8:
        # equals
        return (
            "eq_ "
            f"{"&" if c == 0 else " "}{address_1}"
            " "
            f"{"&" if b == 0 else " "}{address_2}"
            " "
            f"{"&" if a == 0 else " "}{address_3}"
        )
    elif opcode == 9:
        # adjust the relative base (inc or dec by value 1)
        return "adj " f"{"&" if c == 0 else " "}{address_1}"
    elif opcode == 99:
        return "hlt"
    else:
        return "incorrect opcode"


if __name__ == "__main__":
    print(AdventOfCodeProblem201909().solve())
