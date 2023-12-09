from dataclasses import dataclass

import numpy as np

from advent_of_code.common import load_input_text_file


@dataclass(frozen=True, kw_only=True)
class Network:  # poignée
    instructions: str
    nodes: dict[str, tuple[str, str]]


ProblemDataType = Network


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    network = parse_input_text_file()
    steps = count_required_steps(network)
    return steps


def compute_part_2():
    network = parse_input_text_file()
    sources = tuple(sorted(key for key in network.nodes.keys() if key.endswith("A")))
    targets = tuple(sorted(key for key in network.nodes.keys() if key.endswith("Z")))
    assert len(sources) == len(targets)
    steps = compute_steps_for_part_2(network, sources, "Z")
    return steps


def count_required_steps(
    network: Network, starting_node: str = "AAA", target_node: str = "ZZZ"
) -> int:
    current_node = starting_node
    i = steps = 0
    while current_node != target_node:
        i = steps % len(network.instructions)
        instruction = network.instructions[i]
        if instruction == "L":
            index = 0
        elif instruction == "R":
            index = 1
        current_node = network.nodes[current_node][index]
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
    while not all(c.endswith(target_end_letter) for c in current_node_tuple):
        instruction = instructions[i]
        current_node_tuple = tuple(
            network.nodes[c][instruction] for c in current_node_tuple
        )
        steps += 1
        i = steps % instructions_length

    return steps


def compute_steps_for_part_2(
    network: Network, source_nodes: tuple[str, ...], target_end_letter: str
):
    histories = {}

    for source_node in source_nodes:
        histories[source_node] = detect_loop(network, source_node, target_end_letter)

    # Find lowest common multiple for all loop lengths
    steps = np.lcm.reduce([len(h) for h in histories.values()])
    return steps


def detect_loop(network: Network, starting_node: str, target_end_letter: str) -> list:
    current_node = starting_node
    instructions_length = len(network.instructions)
    instructions = np.array(
        list(inst == "R" for inst in network.instructions), dtype=np.uint8
    )
    i = steps = 0
    found_target_node = None
    history = []
    while True:
        if current_node.endswith(target_end_letter):
            found_target_node = current_node
        if current_node == found_target_node:
            return history

        history.append((current_node, i))
        current_node = network.nodes[current_node][instructions[i]]
        steps += 1
        i = steps % instructions_length


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
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
    main()
