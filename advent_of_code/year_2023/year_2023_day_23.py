from dataclasses import dataclass
import numpy as np
from advent_of_code.common import load_input_text_file
from advent_of_code.constants import EAST, NEIGHBOUR_MOVES, NORTH, SOUTH, WEST, Position

ProblemDataType = ...

ALLOWED_MOVES = {b">": EAST, b"<": WEST, b"^": NORTH, b"v": SOUTH}


@dataclass(kw_only=True)
class TrailNode:
    starting_position: Position
    length: int
    children: list["TrailNode"]


def main():
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


def compute_exploration_tree(hk, starting_position):
    explored = np.zeros_like(hk, dtype=np.bool_)
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
    pos: Position, hk: np.ndarray, explored: np.ndarray, node: TrailNode
) -> None:
    node.length += 1
    explored[pos] = True
    for direction, move in NEIGHBOUR_MOVES.items():
        next_pos = tuple(pos + move)
        if not explored[next_pos]:
            if hk[next_pos] == b"#":
                continue
            if hk[next_pos] == b".":
                explore_hiking_trail(next_pos, hk, explored, node)
            elif ALLOWED_MOVES[hk[next_pos]] == direction:
                jumped = tuple(pos + move + move)
                child = TrailNode(
                    starting_position=jumped,
                    length=0,
                    children=[],
                )
                node.children.append(child)
                explore_hiking_trail(jumped, hk, explored, child)


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


if __name__ == "__main__":
    main()
