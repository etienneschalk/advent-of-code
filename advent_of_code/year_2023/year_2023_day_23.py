import re
from dataclasses import asdict, dataclass

import numpy as np

from advent_of_code.common import adapt_recursion_limit, load_input_text_file, save_txt
from advent_of_code.constants import EAST, NEIGHBOUR_MOVES, NORTH, SOUTH, WEST, Position

ProblemDataType = ...

ALLOWED_MOVES = {b">": EAST, b"<": WEST, b"^": NORTH, b"v": SOUTH}


@dataclass(kw_only=True)
class TrailNode:
    starting_position: Position
    length: int
    children: list["TrailNode"]


def main():
    adapt_recursion_limit()

    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    hiking_trail = parse_input_text_file()
    hk = hiking_trail
    # Input observation: it seems that all crossroads
    # are separated by slopes
    # starting_position: Position = (0, 1)
    starting_position: Position = (1, 2)

    tree = compute_exploration_tree(hk, starting_position)
    bf = bruteforce_paths_in_exploration_tree(tree, 0)

    # It works ^^
    actual_result = compute_all_path_lengths(bf)
    max_path_length = actual_result[0]
    return max_path_length


# def analyze_exploration_tree(tree):
#     return (flatten_graph, path_lengths)


def flatten_exploration_tree(initial_tree: TrailNode):
    graph: dict[Position, TrailNode] = {}

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


def bruteforce_paths_in_exploration_tree(tree: TrailNode, total_length: int = 0):
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


def compute_exploration_tree(hk, starting_position):
    explored = np.zeros_like(hk, dtype=np.bool_)
    # length = -1  # exclude start
    length = 0
    pos = starting_position

    initial_tree = TrailNode(
        starting_position=starting_position,
        length=length,
        children=[],
    )
    explore_hiking_trail(pos, hk, explored, initial_tree)
    return initial_tree


def explore_hiking_trail(
    pos: Position,
    hk: np.ndarray,
    explored: np.ndarray,
    node: TrailNode,
    flat_graph=None,
) -> None:
    node.length += 1
    explored[pos] = True
    if flat_graph is None:
        flat_graph: dict[Position, TrailNode] = {}
        flat_graph[node.starting_position] = node
    for direction, move in NEIGHBOUR_MOVES.items():
        next_pos = tuple(pos + move)
        if explored[next_pos]:
            ...
        else:
            if hk[next_pos] == b"#":
                continue
            if hk[next_pos] == b".":
                explore_hiking_trail(next_pos, hk, explored, node, flat_graph)
            # Resolved (issue was with flat graph construction)
            # Note: the test input only contains T-intersection
            # (at most 3 slopes). The actual input can contain up to 4, and this case
            # makes the current code fail. See the graphviz for the actual input: nodes
            # become orphan at coordinates of full intersections eg 66, 60
            # Note: at 32, 44, there is a full intersection, seemingly the first, and it
            # works
            # maybe the first full intersection is handled well but not the following,
            # the graph stops being a tree at this point. So the recursive dict
            # structure may be inadapted.
            elif ALLOWED_MOVES[hk[next_pos]] == direction:
                jumped = tuple(pos + move + move)
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
                    explore_hiking_trail(jumped, hk, explored, child, flat_graph)


def compute_all_path_lengths(bf) -> np.ndarray:
    flattened = [int(c) for c in re.findall(r"\d+", str(bf))]
    flattened

    # Warning: The start position is NOT included in the longest path
    # action: take result and minus one.

    actual_result = np.array(list(reversed(sorted(flattened)))) - 1
    return actual_result


def compute_part_2():
    hiking_trail = parse_input_text_file()
    ...
    return None


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    lines = text.strip().split("\n")
    input_array = np.array([np.fromstring(line, dtype="<S1") for line in lines])
    # Circling everything by a wall to avoid static out of bounds checks
    padded_array = np.pad(input_array, pad_width=1, constant_values=b"#")
    return padded_array


def save_exploration_tree_txt(tree):
    dico = asdict(tree)

    import json

    txt = json.dumps(dico, indent=4, default=str)

    save_txt(
        txt,
        "part1.json",
        __file__,
        output_subdir="text",
    )


if __name__ == "__main__":
    main()
