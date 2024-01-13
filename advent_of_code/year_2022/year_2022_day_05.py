import re
from collections import namedtuple
from dataclasses import dataclass

import numpy as np

from advent_of_code.common import load_input_text_file_from_filename

InstructionTuple = namedtuple("InstructionTuple", ["move", "source", "destination"])
StacksType = dict[int, list[str]]


@dataclass(frozen=True, kw_only=True)
class RearrangementProcedure:
    stacks: StacksType
    instructions: tuple[InstructionTuple]


ProblemDataType = RearrangementProcedure


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    procedure = parse_input_text_file()
    result = logic_part_1(procedure)
    return result


def compute_part_2():
    procedure = parse_input_text_file()
    result = logic_part_2(procedure)
    return result


def common_logic(procedure: RearrangementProcedure, move_func) -> str:
    stacks = procedure.stacks
    for instruction in procedure.instructions:
        destination = stacks[instruction.destination]
        source = stacks[instruction.source]
        move_func(instruction, destination, source)
    answer = "".join(s[-1] for s in stacks.values())
    return answer


def logic_part_1(procedure: RearrangementProcedure) -> str:
    return common_logic(procedure, move_stacks_fifo)


def logic_part_2(procedure: RearrangementProcedure) -> str:
    return common_logic(procedure, move_stacks_lifo)


def move_stacks_fifo(instruction, destination, source):
    for _ in range(instruction.move):
        destination.append(source.pop())


def move_stacks_lifo(instruction, destination, source):
    destination.extend(reversed([source.pop() for _ in range(instruction.move)]))


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file_from_filename(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    stack_group, instruction_group = text.strip("\n").split("\n\n")

    stacks = parse_stack_text(stack_group)
    instructions = parse_instructions_text(instruction_group)

    return RearrangementProcedure(stacks=stacks, instructions=instructions)


def parse_stack_text(stack_group: str) -> StacksType:
    sa = stack_group.split("\n")
    max_length = max(len(line) for line in sa)
    sa = [line + " " * (max_length - len(line)) for line in sa]
    stacks = np.array([np.fromstring(line, dtype="<S1") for line in sa])
    stacks = np.flip(stacks.T, axis=1)[1::4][:, 1:].tolist()
    stacks = tuple(
        list(s.decode("utf-8") for s in stack if s != b" ") for stack in stacks
    )
    stacks = dict(zip(range(1, len(stacks) + 1), stacks))

    return stacks


def parse_instructions_text(instruction_group) -> tuple[InstructionTuple]:
    instructions = tuple(
        InstructionTuple(*(int(d) for d in re.findall(r"\d+", instruction)))
        for instruction in instruction_group.split("\n")
    )
    return instructions


if __name__ == "__main__":
    main()
