import sys
from pathlib import Path

import numpy as np
import xarray as xr
from PIL import Image
from skimage.morphology import flood_fill

from advent_of_code.common import load_input_text_file

ProblemDataType = np.ndarray

DIR_B = np.array((1, 0))
DIR_T = -DIR_B
DIR_R = np.array((0, 1))
DIR_L = -DIR_R
DIR_TL = DIR_T + DIR_L
DIR_TR = DIR_T + DIR_R
DIR_BL = DIR_B + DIR_L
DIR_BR = DIR_B + DIR_R

PATTERNS = {
    "│": np.bool_(
        np.array(
            [
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 0],
            ]
        )
    ),
    "─": np.bool_(
        np.array(
            [
                [0, 0, 0],
                [1, 1, 1],
                [0, 0, 0],
            ]
        )
    ),
    "└": np.bool_(
        np.array(
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 0, 0],
            ]
        )
    ),
    "┘": np.bool_(
        np.array(
            [
                [0, 1, 0],
                [1, 1, 0],
                [0, 0, 0],
            ]
        )
    ),
    "┐": np.bool_(
        np.array(
            [
                [0, 0, 0],
                [1, 1, 0],
                [0, 1, 0],
            ]
        )
    ),
    "┌": np.bool_(
        np.array(
            [
                [0, 0, 0],
                [0, 1, 1],
                [0, 1, 0],
            ]
        )
    ),
    "░": np.bool_(
        np.array(
            [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ]
        )
    ),
    # "S",
}


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    maze = parse_input_text_file()
    print(render_2d_array_to_text(maze))
    result, minimum_distances = logic_part_1(maze)
    return result


def compute_part_2():
    maze = parse_input_text_file()
    print(render_2d_array_to_text(maze))
    result, minimum_distances = logic_part_1(maze)
    arr = minimum_distances
    main_loop = np.where(minimum_distances != 0, maze, "░")

    i, j = locate_starting_index(main_loop)
    neighbour_dict = get_neighbour_indices_dict(i, j)
    allowed_pipes = get_allowed_pipes_for_direction()
    directions = []
    for direction, neighbour in neighbour_dict.items():
        if main_loop[neighbour] in allowed_pipes[direction]:
            directions.append(direction)

    good_pipe = get_good_pipe(directions)

    main_loop[i, j] = good_pipe
    print(render_2d_array_to_text(main_loop))
    arr_3x = np.zeros(3 * np.array(arr.shape), dtype=np.bool_)

    # Ignore padded contour (1px)
    for i in range(1, arr.shape[0] - 1):
        for j in range(1, arr.shape[1] - 1):
            fill_macro_pixel_3x(main_loop, arr_3x, i, j)
    ...
    result = arr_3x
    grey = np.uint8(arr_3x) * 255
    print(render_2d_array_to_text(grey))

    save_img(arr_3x, Path("generated/arr_3x_1.png").resolve())
    filled = flood_fill(
        grey, (grey.shape[0] // 2, grey.shape[0] // 2), 128, tolerance=1
    )

    save_img(filled, Path("generated/arr_3x_2.png").resolve())
    xda = xr.DataArray(filled, dims=("i", "j"))
    coarsened = xda.coarsen(i=3, j=3).all()
    coarsened_img = np.uint8(coarsened) * 255
    save_img(coarsened_img, Path("generated/arr_3x_3.png").resolve())

    result = np.sum(coarsened).item()

    return result


def save_img(arr_3x: np.ndarray, path: Path):
    im = Image.fromarray(arr_3x)
    im.save(path)
    print(path)


def get_good_pipe(directions):
    if set(directions) == {"bottom", "top"}:
        good_pipe = "│"
    elif set(directions) == {"left", "right"}:
        good_pipe = "─"
    elif set(directions) == {"bottom", "right"}:
        good_pipe = "┌"
    elif set(directions) == {"bottom", "left"}:
        good_pipe = "┐"
    elif set(directions) == {"right", "top"}:
        good_pipe = "└"
    elif set(directions) == {"left", "top"}:
        good_pipe = "┘"
    return good_pipe


# def compute_part_2():
#     maze = parse_input_text_file()
#     print(render_2d_array_to_text(maze))
#     result, minimum_distances = logic_part_1(maze)
#     arr = minimum_distances
#     main_loop = np.where(minimum_distances != 0, maze, "░")
#     print(render_2d_array_to_text(main_loop))
#     arr_2x = np.zeros(2 * np.array(arr.shape), dtype=np.bool_)
#     # Ignore padded contour (1px)
#     for i in range(1, arr.shape[0] - 1):
#         for j in range(1, arr.shape[1] - 1):
#             fill_macro_pixel(main_loop, arr_2x, i, j)
#     ...
#     result = arr_2x
#     print(render_2d_array_to_text(arr_2x))

#     return result


def logic_part_1(maze: ProblemDataType):
    adapt_recursion_limit()

    i, j = locate_starting_index(maze)
    neighbour_dict = get_neighbour_indices_dict(i, j)
    allowed_pipes = get_allowed_pipes_for_direction()

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
    print(render_2d_array_to_text((minimum_distances != 0)))

    maximum = np.max(minimum_distances)
    return maximum, minimum_distances


def get_allowed_pipes_for_direction():
    allowed_pipes = {
        "top": {"│", "┐", "┌"},
        "bottom": {"│", "┘", "└"},
        "left": {"─", "└", "┌"},
        "right": {"─", "┐", "┘"},
    }

    return allowed_pipes


def adapt_recursion_limit():
    print("Current recursion limit:")
    print(sys.getrecursionlimit())
    sys.setrecursionlimit(15_000)
    print("New recursion limit:")
    print(sys.getrecursionlimit())


def get_neighbour_indices_dict(i, j):
    neighbour_dict = dict(
        zip(("top", "bottom", "left", "right"), get_neighbour_indices(i, j))
    )

    return neighbour_dict


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


def explore_maze_part_2(
    maze: ProblemDataType,
    maze_2x: ProblemDataType,
    values: ProblemDataType,
    distance: int,
    i: int,
    j: int,
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
            explore_maze_part_2(maze, values, distance, *candidate)


def fill_macro_pixel_3x(
    maze: ProblemDataType, maze_3x: ProblemDataType, i: int, j: int
):
    maze_3x[3 * i : 3 * i + 3, 3 * j : 3 * j + 3] = PATTERNS[maze[i, j]]
    # for i in range(3):
    #     for j in range(3):
    #         maze_3x
    # if maze[i, j] == "│":
    #     candidates = ((i - 1, j), (i + 1, j))
    # elif maze[i, j] == "─":
    #     candidates = ((i, j - 1), (i, j + 1))
    # elif maze[i, j] == "└":
    #     candidates = ((i - 1, j), (i, j + 1))
    # elif maze[i, j] == "┘":
    #     candidates = ((i - 1, j), (i, j - 1))
    # elif maze[i, j] == "┐":
    #     candidates = ((i, j - 1), (i + 1, j))
    # elif maze[i, j] == "┌":
    #     candidates = ((i, j + 1), (i + 1, j))


def fill_macro_pixel(maze: ProblemDataType, maze_2x: ProblemDataType, i: int, j: int):
    # if maze[i, j] == "│":
    #     candidates = ((i - 1, j), (i + 1, j))
    # elif maze[i, j] == "─":
    #     candidates = ((i, j - 1), (i, j + 1))
    # elif maze[i, j] == "└":
    #     candidates = ((i - 1, j), (i, j + 1))
    # elif maze[i, j] == "┘":
    #     candidates = ((i - 1, j), (i, j - 1))
    # elif maze[i, j] == "┐":
    #     candidates = ((i, j - 1), (i + 1, j))
    # elif maze[i, j] == "┌":
    #     candidates = ((i, j + 1), (i + 1, j))
    n_dict = get_neighbour_indices_dict(i, j)
    to = maze[n_dict["top"]] != "░"
    bo = maze[n_dict["bottom"]] != "░"
    le = maze[n_dict["left"]] != "░"
    ri = maze[n_dict["right"]] != "░"
    tl = to and le
    tr = to and ri
    bl = bo and le
    br = bo and ri
    tl_coord = (2 * i, 2 * j)
    tr_coord = (2 * i, 2 * j + 1)
    bl_coord = (2 * i + 1, 2 * j)
    br_coord = (2 * i + 1, 2 * j + 1)
    maze_2x[tl_coord] = tl
    maze_2x[tr_coord] = tr
    maze_2x[bl_coord] = bl
    maze_2x[br_coord] = br


# def fill_macro_pixel(maze: ProblemDataType, maze_2x: ProblemDataType, i: int, j: int):
#     tl = maze[i, j]
#     tr = maze[i, j + 1]
#     bl = maze[i + 1, j]
#     br = maze[i + 1, j + 1]
#     tl_coord = (2 * i, 2 * j)
#     tr_coord = (2 * i, 2 * j + 1)
#     bl_coord = (2 * i + 1, 2 * j)
#     br_coord = (2 * i + 1, 2 * j + 1)
#     maze_2x[tl_coord] = tl
#     maze_2x[tr_coord] = tr
#     maze_2x[bl_coord] = bl
#     maze_2x[br_coord] = br


# def fill_macro_pixel(maze: ProblemDataType, maze_2x: ProblemDataType, i: int, j: int):
#     n_dict = get_neighbour_indices_dict(i, j)
#     t = maze[n_dict["top"]]
#     b = maze[n_dict["bottom"]]
#     l = maze[n_dict["left"]]
#     r = maze[n_dict["right"]]
#     tl = t and l
#     tr = t and r
#     bl = b and l
#     br = b and r
#     tl_coord = (2 * i, 2 * j)
#     tr_coord = (2 * i, 2 * (j + 1))
#     bl_coord = (2 * (i + 1), 2 * j)
#     br_coord = (2 * (i + 1), 2 * (j + 1))
#     maze_2x[tl_coord] = tl
#     maze_2x[tr_coord] = tr
#     maze_2x[bl_coord] = bl
#     maze_2x[br_coord] = br


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

    # Add a border of dots will ease later checks,
    # not having to care about data outside the borders
    padded_array = np.pad(input_array, pad_width=1, constant_values=b".")
    return padded_array


def render_2d_array_to_text(data: ProblemDataType) -> str:
    if data.dtype == np.bool_:
        data = np.int8(data)
        result = "\n".join("".join(str(c) for c in line) for line in data)
        result = result.replace("0", "░").replace("1", "▓")
    else:
        result = "\n".join("".join(str(c) for c in line) for line in data)
    return result


if __name__ == "__main__":
    main()
