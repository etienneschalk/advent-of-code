import sys

import numpy as np

from advent_of_code.common import load_input_text_file

ProblemDataType = np.ndarray


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    maze = parse_input_text_file()
    ...
    print(render_pipes(maze))
    result = logic_part_1(maze)
    return result


def compute_part_2():
    data = parse_input_text_file()
    ...
    return None


def logic_part_1(maze: ProblemDataType):
    print("Current recursion limit:")
    print(sys.getrecursionlimit())
    sys.setrecursionlimit(15_000)
    print("New recursion limit:")
    print(sys.getrecursionlimit())

    i, j = locate_starting_index(maze)
    neighbours = get_neighbour_indices(i, j)
    neighbour_dict = dict(
        zip(("top", "bottom", "left", "right"), get_neighbour_indices(i, j))
    )
    allowed_pipes = {
        "top": {"│", "┐", "┌"},
        "bottom": {"│", "┘", "└"},
        "left": {"─", "└", "┌"},
        "right": {"─", "┐", "┘"},
    }
    values_dict = {}
    for direction, neighbour in neighbour_dict.items():
        if maze[neighbour] not in allowed_pipes[direction]:
            print(f"Skipped {direction}")
            continue

        distance = 0
        values = np.zeros_like(maze, dtype=np.int32)
        values[i, j] = -1

        explore_maze(maze, values, distance, *neighbour)
        values_dict[neighbour] = values
    minimum_distances = np.minimum(*values_dict.values())
    maximum = np.max(minimum_distances)
    return maximum


def locate_starting_index(maze: ProblemDataType) -> tuple[int, int]:
    i, j = np.nonzero(maze == "S")
    assert i.size == 1
    assert j.size == 1
    return i[0], j[0]


def get_neighbour_indices(i: int, j: int) -> tuple[tuple[int, int], ...]:
    # top bottom left right
    return ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1))


def explore_maze(
    maze: ProblemDataType, values: ProblemDataType, distance: int, i: int, j: int
):
    distance += 1
    values[i, j] = distance

    if maze[i, j] == "│":
        candidates = ((i - 1, j), (i + 1, j))
    elif maze[i, j] == "─":
        candidates = ((i, j - 1), (i, j + 1))
    elif maze[i, j] == "└":
        candidates = ((i - 1, j), (i, j + 1))
    elif maze[i, j] == "┘":
        candidates = ((i - 1, j), (i, j - 1))
    elif maze[i, j] == "┐":
        candidates = ((i, j - 1), (i + 1, j))
    elif maze[i, j] == "┌":
        candidates = ((i, j + 1), (i + 1, j))
    else:
        return

    for candidate in candidates:
        # If a value is non-zero, the cell has already been explored
        if not values[candidate]:
            explore_maze(maze, values, distance, *candidate)


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    mapping = {
        "|": "║",
        "-": "═",
        "L": "╚",
        "J": "╝",
        "7": "╗",
        "F": "╔",
        ".": "░",
        "S": "S",
    }
    mapping = {
        "|": "│",
        "-": "─",
        "L": "└",
        "J": "┘",
        "7": "┐",
        "F": "┌",
        ".": "░",
        "S": "S",
    }
    for src, tgt in mapping.items():
        text = text.replace(src, tgt)
    lines = text.strip().split("\n")
    input_array = np.array([np.array(list(line)) for line in lines])
    return input_array


def render_pipes(data: ProblemDataType) -> str:
    return "\n".join("".join(line) for line in data)


if __name__ == "__main__":
    main()
