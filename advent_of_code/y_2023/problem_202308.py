from dataclasses import dataclass

import numpy as np

from advent_of_code.common.common import load_input_text_file_from_filename
from advent_of_code.common.protocols import AdventOfCodeProblem


@dataclass(frozen=True, kw_only=True)
class Network:  # poignée
    instructions: str
    nodes: dict[str, tuple[str, str]]


type PuzzleInput = Network


@dataclass(kw_only=True)
class AdventOfCodeProblem202308(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 8

    def solve_part_1(self, puzzle_input: PuzzleInput):
        network = puzzle_input
        steps = count_required_steps(network)
        return steps

    def solve_part_2(self, puzzle_input: PuzzleInput):
        network = puzzle_input
        sources = tuple(
            sorted(key for key in network.nodes.keys() if key.endswith("A"))
        )
        targets = tuple(
            sorted(key for key in network.nodes.keys() if key.endswith("Z"))
        )
        assert len(sources) == len(targets)
        steps = compute_steps_for_part_2(network, sources, "Z")
        return steps

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input(text)


def count_required_steps(
    network: Network, starting_node: str = "AAA", target_node: str = "ZZZ"
) -> int:
    current_node = starting_node
    i = steps = 0
    while current_node != target_node:
        i = steps % len(network.instructions)
        instruction = network.instructions[i]
        current_node = network.nodes[current_node][int(instruction == "R")]
        steps += 1
    return steps


def count_required_steps_simultaneously_bruteforce(
    network: Network,
    starting_node_tuple: tuple[str, ...],
    target_end_letter: str,
) -> int:
    current_node_tuple = starting_node_tuple
    instructions_length = len(network.instructions)
    instructions = np.array(
        list(inst == "R" for inst in network.instructions), dtype=np.uint8
    )
    i = steps = 0
    stop_condition = False
    while not stop_condition:
        instruction: np.uint8 = instructions[i]
        current_node_tuple = tuple(
            network.nodes[c][instruction] for c in current_node_tuple
        )
        steps += 1
        i = steps % instructions_length
        stop_condition = all(c.endswith(target_end_letter) for c in current_node_tuple)

    return steps


def compute_steps_for_part_2(
    network: Network, source_nodes: tuple[str, ...], target_end_letter: str
):
    histories: dict[str, list[tuple[str, int]]] = {}

    for source_node in source_nodes:
        histories[source_node] = detect_loop(network, source_node, target_end_letter)

    # Find lowest common multiple for all loop lengths (ignoring target node)
    steps = np.lcm.reduce([len(h[:-1]) for h in histories.values()])
    return steps


def detect_loop(network: Network, starting_node: str, target_end_letter: str):
    current_node = starting_node
    instructions_length = len(network.instructions)
    instructions = np.array(
        list(inst == "R" for inst in network.instructions), dtype=np.uint8
    )
    i = steps = 0
    history: list[tuple[str, int]] = []
    while True:
        history.append((current_node, i))
        instruction: np.uint8 = instructions[i]
        current_node = network.nodes[current_node][instruction]
        steps += 1
        i = steps % instructions_length

        if current_node.endswith(target_end_letter):
            history.append((current_node, i))  # for visualization purposes
            return history


def parse_input_text_file() -> PuzzleInput:
    text = load_input_text_file_from_filename(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> PuzzleInput:
    lines = text.strip().split("\n")
    instructions = lines[0]

    nodes = dict(parse_node_from_line(line) for line in lines[2:])

    ...
    return Network(instructions=instructions, nodes=nodes)


def parse_node_from_line(line: str) -> tuple[str, tuple[str, str]]:
    node = line[0:3]
    left = line[7:10]
    right = line[12:15]
    return (node, (left, right))


if __name__ == "__main__":
    print(AdventOfCodeProblem202308().solve())
