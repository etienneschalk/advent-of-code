import re
from dataclasses import dataclass
from time import perf_counter
from typing import Sequence, Union

import numpy as np
import numpy.typing as npt

from advent_of_code.common import adapt_recursion_limit, parse_2d_string_array_to_uint8
from advent_of_code.constants import (
    EAST,
    NEIGHBOUR_MOVES,
    NORTH,
    SOUTH,
    WEST,
    Direction,
    Position,
)
from advent_of_code.protocols import AdventOfCodeProblem

ALLOWED_MOVES: dict[int, Direction] = {
    ord(b">"): EAST,
    ord(b"<"): WEST,
    ord(b"^"): NORTH,
    ord(b"v"): SOUTH,
}

type PuzzleInput = npt.NDArray[np.uint8]

type NodePrimaryKey = tuple[int, Position]
type FlatTreeList = dict[NodePrimaryKey, list[NodePrimaryKey]]
type FlatTreeSet = dict[NodePrimaryKey, set[NodePrimaryKey]]

type FlatTreeListStr = dict[str, list[str]]

type PositionToTreeNodeDict = dict[Position, TrailNode]

type RecursiveSequenceOfInts = Sequence[Union["RecursiveSequenceOfInts", int]]


@dataclass(kw_only=True)
class AdventOfCodeProblem202323(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 23

    def solve_part_1(self, puzzle_input: PuzzleInput):
        adapt_recursion_limit()

        hiking_trail = puzzle_input

        # Input observation: it seems that all crossroads
        # are separated by slopes
        # starting_position: Position = (0, 1)
        starting_position: Position = (1, 2)

        tree = compute_exploration_tree(hiking_trail, starting_position)
        bf = bruteforce_paths_in_exploration_tree(tree, 0)

        # It works ^^
        actual_result = compute_all_path_lengths(bf)
        max_path_length = actual_result[0]
        return max_path_length

    def solve_part_2(self, puzzle_input: PuzzleInput):
        adapt_recursion_limit()

        hiking_trail = puzzle_input
        target = (133, (130, 128))
        result = solve_part_2(hiking_trail, target)
        return result

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        input_array = parse_2d_string_array_to_uint8(text)

        # Circling everything by a wall to avoid static out of bounds checks
        padded_array = np.pad(input_array, pad_width=1, constant_values=ord(b"#"))
        return padded_array


@dataclass(kw_only=True)
class TrailNode:
    starting_position: Position
    length: int
    children: list["TrailNode"]


def solve_part_2(hiking_trail: PuzzleInput, target: tuple[int, tuple[int, int]]):
    hk = hiking_trail
    starting_position: Position = (1, 2)
    tree = compute_exploration_tree(hk, starting_position)
    flat_tree = flatten_exploration_tree(tree)
    flat = create_flat_simplified_tuple(flat_tree)
    flatset = create_flatset(flat)

    # Lucky that the dicts are ordered!
    start_node_pos = next(iter(flatset))
    # because the node encode the weights, the weight must be know in advance
    # (already known for step 1)
    track = []
    t1 = perf_counter()
    explore_flatset(flatset, start_node_pos, set(), 0, 0, target, track)
    t2 = perf_counter()

    # t2-t1=149.8870151930023 (time taken by bruteforce according to perf_counter)
    # so around 2min30
    print(f"{t2-t1=} (time taken by bruteforce according to perf_counter)")

    # Don't ever do this! (ultra long)
    # print(track)

    # Minus one, start excluded...
    result = np.max(np.array([t[2] for t in track])) - 1
    return int(result)


type RecursiveDictOfSetOfInts = Sequence[Union["RecursiveDictOfSetOfInts", int]]


def explore_flatset(
    flatset: FlatTreeSet,
    start_node_pos_weight: NodePrimaryKey,
    explored: set[NodePrimaryKey],
    depth: int,
    steps: int,
    target_node_pos_weight: NodePrimaryKey,
    track: list[
        tuple[int, NodePrimaryKey, int]
    ],  # list containing all weights for target
) -> None:
    pos_weight = start_node_pos_weight
    target = target_node_pos_weight
    explored.add(pos_weight)
    length = pos_weight[0]
    steps = steps + length  # first tuple member is weight
    # print(" " * depth, pos_weight, steps)
    if target == pos_weight:
        track.append((depth, pos_weight, steps))
    # Only explore target, avoid unnecessary backtracking
    if target in flatset[pos_weight]:
        child = target
        explore_flatset(flatset, child, explored, depth + 1, steps, target, track)
    else:
        for child in flatset[pos_weight]:
            if child in explored:
                continue
            explore_flatset(flatset, child, explored, depth + 1, steps, target, track)
    explored.remove(pos_weight)


# def analyze_exploration_tree(tree):
#     return (flatten_graph, path_lengths)


def bruteforce_paths_in_exploration_tree(
    tree: TrailNode, total_length: int = 0
) -> RecursiveSequenceOfInts | int:
    total_length += tree.length

    # Consume mono-children along the chain as long as possible
    while len(tree.children) == 1:
        tree = tree.children[0]
        total_length += tree.length
    if len(tree.children) == 0:
        return total_length
    else:
        return [
            bruteforce_paths_in_exploration_tree(child, total_length)
            for child in tree.children
        ]


def explore_hiking_trail(
    pos: Position,
    hiking_trail: PuzzleInput,
    explored: npt.NDArray[np.bool_],
    node: TrailNode,
    flat_graph: PositionToTreeNodeDict,
) -> None:
    node.length += 1
    explored[pos] = True

    for direction, move in NEIGHBOUR_MOVES.items():
        next_pos_array = pos + move
        next_pos: Position = next_pos_array[0], next_pos_array[1]
        if explored[next_pos]:
            continue
        if hiking_trail[next_pos] == ord(b"#"):
            continue
        if hiking_trail[next_pos] == ord(b"."):
            explore_hiking_trail(next_pos, hiking_trail, explored, node, flat_graph)
        # Resolved (issue was with flat graph construction)
        # Note: the test input only contains T-intersection
        # (at most 3 slopes). The actual input can contain up to 4, and this case
        # makes the current code fail. See the graphviz for the actual input: nodes
        # become orphan at coordinates of full intersections eg 66, 60
        # Note: at 32, 44, there is a full intersection, seemingly the first, and it
        # works
        # maybe the first full intersection is handled well but not the following,
        # the graph stops being a tree at this point. So the recursive dict
        # structure may be unadapted.
        elif ALLOWED_MOVES[hiking_trail[next_pos]] == direction:
            jumped_array = pos + 2 * move
            jumped: Position = jumped_array[0], jumped_array[1]
            if jumped in flat_graph:
                already_explored_child = flat_graph[jumped]
                node.children.append(already_explored_child)
            else:
                child = TrailNode(
                    starting_position=jumped,
                    length=1,  # offset because we jumped
                    children=[],
                )
                flat_graph[child.starting_position] = child
                node.children.append(child)
                explore_hiking_trail(jumped, hiking_trail, explored, child, flat_graph)


def compute_all_path_lengths(bf: RecursiveSequenceOfInts | int):
    flattened = [int(c) for c in re.findall(r"\d+", str(bf))]
    # Warning: The start position is NOT included in the longest path
    # action: take result and minus one.

    actual_result = np.array(list(reversed(sorted(flattened)))) - 1
    return actual_result


def make_undirected_graph(flat: FlatTreeList, *, bidirectional: bool = False):
    couples_forward: dict[tuple[NodePrimaryKey, NodePrimaryKey], None] = {}
    couples_backward: dict[tuple[NodePrimaryKey, NodePrimaryKey], None] = {}
    for node, children in flat.items():
        for child in children:
            # Cheap trick: ordered set backed by dict, with None values
            couples_forward[node, child] = None
            if bidirectional:
                couples_backward[child, node] = None
    if bidirectional:
        couples = {**couples_forward, **couples_backward}
    else:
        # For graphviz, use display trick instead
        # otherwise the graph is very bad looking...
        couples = couples_forward
    return couples


def compute_exploration_tree(hiking_trail: PuzzleInput, starting_position: Position):
    explored = np.zeros_like(hiking_trail, dtype=np.bool_)
    initial_tree = TrailNode(starting_position=starting_position, length=0, children=[])

    flat_graph: PositionToTreeNodeDict = {}
    flat_graph[initial_tree.starting_position] = initial_tree
    explore_hiking_trail(
        starting_position, hiking_trail, explored, initial_tree, flat_graph
    )
    return initial_tree


def flatten_exploration_tree(initial_tree: TrailNode) -> PositionToTreeNodeDict:
    graph: PositionToTreeNodeDict = {}

    q = [initial_tree]
    explored = set()
    while q:
        tree = q.pop(0)
        if tree.starting_position in explored:
            continue
        # Wrong, TODO ,[tree] and append if explored
        explored.add(tree.starting_position)
        graph[tree.starting_position] = tree
        q.extend(tree.children)

    return graph


def create_flat_simplified_tuple(to_flatten: PositionToTreeNodeDict) -> FlatTreeList:
    flat_simplified = {
        label_pk_node(v): [label_pk_node(c) for c in v.children]
        for v in to_flatten.values()
    }

    return flat_simplified


def create_flatset(flat: FlatTreeList) -> FlatTreeSet:
    flatset = {k: set(v) for k, v in flat.items()}

    for node in flatset:
        for c in flatset[node]:
            flatset[c].add(node)

    return flatset


def label_pk_node(node: TrailNode) -> NodePrimaryKey:
    return (node.length, node.starting_position)


def create_flat_simplified(to_flatten: PositionToTreeNodeDict) -> FlatTreeListStr:
    flat_simplified = {
        format_node(v): [format_node(c) for c in v.children]
        for v in to_flatten.values()
    }

    return flat_simplified


def format_node(node: TrailNode) -> str:
    return f"{node.length}\n{node.starting_position}"


if __name__ == "__main__":
    print(AdventOfCodeProblem202323().solve())
