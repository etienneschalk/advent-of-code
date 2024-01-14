from dataclasses import dataclass

import numpy as np

from advent_of_code.common import adapt_recursion_limit
from advent_of_code.protocols import AdventOfCodeProblem

type PuzzleInput = dict[str, tuple[str, ...]]
type FlatSet = dict[str, set[str]]


@dataclass(kw_only=True)
class AdventOfCodeProblem202325(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 25

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input(text)

    def solve_part_1(self, puzzle_input: PuzzleInput):
        adapt_recursion_limit()
        components = puzzle_input
        # Nodes_to_disconnect: thanks graphviz...
        # Manual observation:
        # - vgf - jpn
        # - nmz - mnl
        # - fdb - txm
        nodes_to_disconnect = {"vgf": "jpn", "nmz": "mnl", "fdb": "txm"}
        nodes_to_explore = {"mpn", "nmz", "fdb"}
        disconnect_result = disconnect_then_explore(
            components, nodes_to_disconnect, nodes_to_explore
        )
        product_of_unique_group_sizes = compute_result_from_exploration(
            disconnect_result
        )
        unique_referenced_nodes = set.union(
            set(components.keys()), *[set(children) for children in components.values()]
        )
        assert len(unique_referenced_nodes) == sum(set(disconnect_result.values()))
        return product_of_unique_group_sizes

    def solve_part_2(self, puzzle_input: PuzzleInput):
        return "Part 2 of Day 25 is having solved all the 49 previous problems!"


def disconnect_then_explore(
    components: PuzzleInput,
    nodes_to_disconnect: dict[str, str],
    nodes_to_explore: set[str],
) -> dict[str, int]:
    disconnected = {k: v for k, v in components.items()}
    for k, v in nodes_to_disconnect.items():
        disconnected[k] = tuple(child for child in disconnected[k] if child != v)

    bidirectional = create_bidirectional(disconnected)

    result = {}
    for start_node in nodes_to_explore:
        explored = set()
        explore_bidirectional(bidirectional, start_node, explored, 0)
        result[start_node] = len(explored)
    return result


def compute_result_from_exploration(result: dict[str, int]) -> int:
    return int(np.prod(list(set(result.values()))))


def create_bidirectional(disconnected_components: PuzzleInput) -> FlatSet:
    flatset: FlatSet = {k: set(v) for k, v in disconnected_components.items()}
    futures: FlatSet = {}
    for node in flatset:
        for c in flatset[node]:
            if c in flatset:
                flatset[c].add(node)
            elif c in futures:
                futures[c].add(node)
            else:
                futures[c] = set()
    merged = {**flatset, **futures}
    return merged


def explore_bidirectional(
    flatset: FlatSet,
    start_node: str,
    explored: set[str],
    depth: int,
) -> None:
    explored.add(start_node)
    # print(depth)
    for child in flatset[start_node]:
        if child in explored:
            continue
        explore_bidirectional(flatset, child, explored, depth + 1)


def parse_text_input(text: str) -> PuzzleInput:
    lines = text.strip().split("\n")
    # cmg: qnr nvd lhk bvb
    components = {}
    for line in lines:
        source, targets = line.split(": ")
        components[source] = tuple(targets.split(" "))
    return components


if __name__ == "__main__":
    print(AdventOfCodeProblem202325().solve_all())
