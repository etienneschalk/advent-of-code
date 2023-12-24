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


def compute_part_2():
    hiking_trail = parse_input_text_file()
    hk = hiking_trail
    target = (133, (130, 128))
    result = solve_part_2(hk, target)
    return result


def solve_part_2(hiking_trail, target):
    hk = hiking_trail
    starting_position: Position = (1, 2)
    tree = compute_exploration_tree(hk, starting_position)
    flat = flatten_exploration_tree(tree)
    flat = create_flat_simplified_tuple(flat)
    flatset = create_flatset(flat)

    # Lucky that the dicts are ordered!
    start_node_pos = next(iter(flatset))
    # because the node encode the weights, the weight must be know in advance
    # (already known for step 1)
    track = []
    explore_flatset(flatset, start_node_pos, set(), 0, 0, target, track)

    print(track)

    # Minus one, start excluded...
    result = np.max(np.array([t[2] for t in track])) - 1
    return result


def create_flatset(flat):
    flatset = {k: set(v) for k, v in flat.items()}

    flatset
    for node in flatset:
        for c in flatset[node]:
            flatset[c].add(node)
    flatset

    return flatset


def explore_flatset(
    flatset,
    start_node_pos_weight: tuple[int, Position],
    explored: set[tuple[int, Position]],
    depth: int,
    steps: int,
    target_node_pos_weight: tuple[int, Position],
    track: set[int],  # set containing all weights for target
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


def make_undirected_graph(flat, bidirectional: bool = False):
    couples_forward = {}
    couples_backward = {}
    for node, children in flat.items():
        for child in children:
            # Cheap trick: ordered set backed by dict...
            couples_forward[node, child] = None
            couples_backward[child, node] = None
    if bidirectional:
        couples = {**couples_forward, **couples_backward}
    else:
        # For graphviz, use display trick instead
        # otherwise the graph is very bad looking...
        couples = couples_forward
    return couples


# def make_undirected_graph(flat):
#     for node in flat.values():
#         for c in node.children:
#             c.children.append(node)


# def make_undirected_graph(flat):
#     undirected = {}
#     for node in flat.values():
#         new_children = []
#         for c in node.children:
#             new_children.append(replace(c, children=tuple([*c.children, node])))
#         new_node = replace(node, children=tuple(new_children))
#         undirected[new_node.starting_position] = new_node
#     return undirected


def create_flat_simplified(to_flatten: dict):
    flat_simplified = {
        format_node(v): [format_node(c) for c in v.children]
        for k, v in to_flatten.items()
    }

    return flat_simplified


def create_flat_simplified_tuple(to_flatten: dict):
    flat_simplified = {
        label_pk_node(v): [label_pk_node(c) for c in v.children]
        for k, v in to_flatten.items()
    }

    return flat_simplified


def label_pk_node(node) -> tuple[int, int, int]:
    return (node.length, node.starting_position)


def format_node(node: TrailNode) -> str:
    return f"{node.length}\n{node.starting_position}"


if __name__ == "__main__":
    main()
