import sys
from pathlib import Path

import numpy as np
import xarray as xr
from PIL import Image
from skimage.morphology import flood_fill

from advent_of_code.common import get_year_and_day_from_filename, load_input_text_file

ProblemDataType = np.ndarray

VERBOSE = False
SAVE_IMG = True
SAVE_TXT = False


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    maze = parse_input_text_file()
    if VERBOSE:
        print(render_2d_array_to_text(maze))
    result, _ = compute_farthest_point_part_1(maze)
    return result


def compute_part_2():
    maze = parse_input_text_file()
    if VERBOSE:
        print(render_2d_array_to_text(maze))
    _, minimum_distances = compute_farthest_point_part_1(maze)
    result = compute_tiles_enclosed_by_loop_part_2(maze, minimum_distances)
    return result


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    mapping = get_simple_pipes_mapping()
    for source, target in mapping.items():
        text = text.replace(source, target)
    lines = text.strip().split("\n")
    input_array = np.array([np.array(list(line)) for line in lines])

    # Add a border of dots will ease later checks,
    # not having to care about data outside the borders
    padded_array = np.pad(input_array, pad_width=1, constant_values=mapping["."])

    return padded_array


def compute_farthest_point_part_1(maze: np.ndarray) -> tuple[int, np.ndarray]:
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

    if VERBOSE:
        print(render_2d_array_to_text((minimum_distances != 0)))

    maximum = np.max(minimum_distances)
    return maximum, minimum_distances


def locate_starting_index(maze: ProblemDataType) -> tuple[int, int]:
    i, j = np.nonzero(maze == "S")
    assert i.size == 1
    assert j.size == 1
    return i[0], j[0]


def get_neighbour_indices_dict(i, j):
    return dict(zip(("top", "bottom", "left", "right"), get_neighbour_indices(i, j)))


def get_neighbour_indices(i: int, j: int) -> tuple[tuple[int, int], ...]:
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
        # Note: -1 is a special value for the start, as 0 also means empty.
        if not values[candidate]:
            explore_maze(maze, values, distance, *candidate)


def compute_tiles_enclosed_by_loop_part_2(
    maze: np.ndarray, minimum_distances: np.ndarray
):
    # Keep only the main loop, remove everything else
    main_loop = np.where(minimum_distances != 0, maze, "░")

    # Replace starting S by the correct pipe
    put_good_pipe_in_place_of_starting_point(main_loop)

    if VERBOSE:
        print(render_2d_array_to_text(main_loop))

    # Prepare the upscale of the main_loop
    raster_3x = rasterize_main_loop(main_loop)

    image = np.uint8(raster_3x) * 255
    if VERBOSE:
        print(render_2d_array_to_text(image))
    if SAVE_IMG:
        save_img(raster_3x, "arr_3x_1.png")

    # Use the Flood Fill algorithm to fill the loop from the exterior.
    # Start from a corner (here upper-left), as the array was padded,
    # guaranteeing free space on its boundaries.
    filled = flood_fill(image, (0, 0), 128, tolerance=1)
    if SAVE_IMG:
        save_img(filled, "arr_3x_2.png")

    # Coarsen to keep any filled macro-cell, then negate to get hole count.
    coarsened_xda = ~(xr.DataArray(filled, dims=("i", "j")).coarsen(i=3, j=3).any())

    if SAVE_IMG:
        coarsened_img = np.uint8(coarsened_xda) * 255
        save_img(coarsened_img, "arr_1x_result_3.png")

    result = np.sum(coarsened_xda).item()
    return result


def put_good_pipe_in_place_of_starting_point(main_loop):
    i, j = locate_starting_index(main_loop)
    neighbour_dict = get_neighbour_indices_dict(i, j)
    allowed_pipes = get_allowed_pipes_for_direction()
    directions = []
    for direction, neighbour in neighbour_dict.items():
        if main_loop[neighbour] in allowed_pipes[direction]:
            directions.append(direction)

    good_pipe = get_good_pipe(directions)

    main_loop[i, j] = good_pipe


def rasterize_main_loop(main_loop: np.ndarray):
    raster_3x = np.zeros(3 * np.array(main_loop.shape), dtype=np.bool_)
    pipe_to_pattern_mapping = get_pipe_to_pattern_mapping()

    # Rasterize the pipes. Each symbol maps to a 3x3 unique pattern.
    # Note: padded contour of empty cells is ignored.
    for i in range(1, main_loop.shape[0] - 1):
        for j in range(1, main_loop.shape[1] - 1):
            fill_macro_pixel_3x(main_loop, raster_3x, pipe_to_pattern_mapping, i, j)

            if SAVE_IMG:
                save_img(
                    raster_3x, f"arr_i{i:05d}_j{j:05d}.png", output_subdir="mazegen"
                )

    return raster_3x


def fill_macro_pixel_3x(
    maze: ProblemDataType,
    maze_3x: ProblemDataType,
    pipe_to_pattern_mapping: dict[str, np.ndarray],
    i: int,
    j: int,
):
    maze_3x[3 * i : 3 * i + 3, 3 * j : 3 * j + 3] = pipe_to_pattern_mapping[maze[i, j]]


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


def render_2d_array_to_text(data: ProblemDataType) -> str:
    if data.dtype == np.bool_:
        data = np.int8(data)
        result = "\n".join("".join(str(c) for c in line) for line in data)
        result = result.replace("0", "░").replace("1", "▓")
    else:
        result = "\n".join("".join(str(c) for c in line) for line in data)
    return result


def save_img(array: np.ndarray, filename: str, *, output_subdir: str = ""):
    year, day = get_year_and_day_from_filename(__file__)
    output_dir_central = f"generated/advent_of_code/year_{year}/day_{day:02d}"
    output_dir = Path(output_dir_central) / output_subdir
    output_dir.mkdir(exist_ok=True, parents=True)
    output_file_path = output_dir / filename
    im = Image.fromarray(array)
    im.save(output_file_path)
    print(f"Saved image to {output_file_path}")


def adapt_recursion_limit():
    print("Current recursion limit:")
    print(sys.getrecursionlimit())
    sys.setrecursionlimit(15_000)
    print("New recursion limit:")
    print(sys.getrecursionlimit())


def get_allowed_pipes_for_direction():
    return {
        "top": {"│", "┐", "┌"},
        "bottom": {"│", "┘", "└"},
        "left": {"─", "└", "┌"},
        "right": {"─", "┐", "┘"},
    }


def get_simple_pipes_mapping():
    return {
        "|": "│",
        "-": "─",
        "L": "└",
        "J": "┘",
        "7": "┐",
        "F": "┌",
        ".": "░",
        "S": "S",
    }


def get_double_pipes_mapping():
    return {
        "|": "║",
        "-": "═",
        "L": "╚",
        "J": "╝",
        "7": "╗",
        "F": "╔",
        ".": "░",
        "S": "S",
    }


def get_pipe_to_pattern_mapping() -> dict[str, np.ndarray]:
    return {
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
    }


if __name__ == "__main__":
    main()
