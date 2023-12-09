from dataclasses import dataclass

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
    source_set = set(key for key in network.nodes.keys() if key.endswith("A"))
    target_set = set(key for key in network.nodes.keys() if key.endswith("Z"))
    assert len(source_set) == len(target_set)
    sources = tuple(source_set)
    targets = tuple(target_set)
    steps = count_required_steps_simultaneously(network, sources, targets)
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


def count_required_steps_simultaneously(
    network: Network,
    starting_node_tuple: tuple[str, ...],
    target_node_tuple: tuple[str, ...],
) -> int:
    current_node_tuple = starting_node_tuple
    target_node_set = set(target_node_tuple)
    i = steps = 0
    while set(current_node_tuple) != target_node_set:
        i = steps % len(network.instructions)
        instruction = network.instructions[i]
        if instruction == "L":
            index = 0
        elif instruction == "R":
            index = 1
        current_node_tuple = tuple(network.nodes[c][index] for c in current_node_tuple)
        steps += 1
    return steps


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
