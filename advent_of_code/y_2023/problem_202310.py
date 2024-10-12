from dataclasses import dataclass
from typing import Any

import numpy as np
import numpy.typing as npt
import xarray as xr
from skimage.morphology import flood_fill  # pyright: ignore[reportUnknownVariableType]

from advent_of_code.common.common import (
    adapt_recursion_limit,
    parse_2d_string_array_to_u1,
    save_txt,
)
from advent_of_code.common.common_img import (
    save_img,  # pyright: ignore[reportUnknownVariableType]
)
from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = npt.NDArray[Any]


@dataclass(kw_only=True)
class AdventOfCodeProblem202310(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 10

    config_verbose: bool = False
    config_save_img: bool = False
    config_save_txt: bool = False
    config_save_img_for_video: bool = False
    config_accumulate_outputs: bool = False

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input(text)

    def solve_part_1(self, puzzle_input: PuzzleInput):
        maze = puzzle_input
        if self.config_verbose:
            print(render_2d_array_to_text(maze))
        if self.config_save_txt:
            save_txt(
                render_2d_array_to_text(maze),
                "part_1_input.txt",
                __file__,
                output_subdir="text",
            )

        minimum_distances = self.compute_minimum_distances(maze)
        farthest_point = np.max(minimum_distances)
        return int(farthest_point)

    def solve_part_2(self, puzzle_input: PuzzleInput):
        maze = puzzle_input
        if self.config_verbose:
            print(render_2d_array_to_text(maze))
        if self.config_save_txt:
            save_txt(
                render_2d_array_to_text(maze),
                "part_2_input.txt",
                __file__,
                output_subdir="text",
            )

        minimum_distances = self.compute_minimum_distances(maze)
        result, _ = self.compute_tiles_enclosed_by_loop_part_2(maze, minimum_distances)
        return result

    def compute_minimum_distances(self, maze: PuzzleInput) -> npt.NDArray[np.int32]:
        adapt_recursion_limit()

        i, j = locate_starting_index(maze)
        neighbour_dict = get_neighbour_indices_dict(i, j)
        allowed_pipes = get_allowed_pipes_for_direction()

        values_dict: dict[tuple[int, int], npt.NDArray[np.int32]] = {}
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

        if self.config_verbose:
            print(render_2d_array_to_text((minimum_distances != 0)))
        if self.config_save_txt:
            save_txt(
                render_2d_array_to_text((minimum_distances != 0)),
                "part_1_farthest_point.txt",
                __file__,
                output_subdir="text",
            )

        return minimum_distances

    def compute_tiles_enclosed_by_loop_part_2(
        self, maze: PuzzleInput, minimum_distances: npt.NDArray[np.int32]
    ):
        outputs_accumulator = {}

        if self.config_accumulate_outputs:
            outputs_accumulator["maze"] = maze
            outputs_accumulator["minimum_distances"] = minimum_distances

        # Keep only the main loop, remove everything else
        main_loop = np.where(minimum_distances != 0, maze, "░")

        # Replace starting S by the correct pipe
        put_good_pipe_in_place_of_starting_point(main_loop)

        if self.config_verbose:
            print(render_2d_array_to_text(main_loop))
        if self.config_save_txt:
            save_txt(
                render_2d_array_to_text(main_loop),
                "part_2_main_loop.txt",
                __file__,
                output_subdir="text",
            )
        if self.config_accumulate_outputs:
            outputs_accumulator["main_loop"] = main_loop

        # Prepare the upscale of the main_loop
        raster_3x = self.rasterize_main_loop(main_loop)

        image = raster_3x.astype(np.uint8) * np.uint8(255)
        if self.config_verbose:
            print(render_2d_array_to_text(image))
        if self.config_save_img:
            save_img(raster_3x, "arr_3x_1.png", __file__)
        if self.config_accumulate_outputs:
            outputs_accumulator["raster_3x"] = raster_3x

        # Use the Flood Fill algorithm to fill the loop from the exterior.
        # Start from a corner (here upper-left), as the array was padded,
        # guaranteeing free space on its boundaries.

        # Typing is a mess here.
        filled: npt.NDArray[np.uint8] = flood_fill(image, (0, 0), 128, tolerance=1)
        if self.config_save_img:
            save_img(filled, "arr_3x_2.png", __file__)
        if self.config_accumulate_outputs:
            outputs_accumulator["filled"] = filled

        # Coarsen to keep any filled macro-cell, then negate to get hole count.
        coarsened_xda: npt.NDArray[np.uint8] = ~(
            xr.DataArray(filled, dims=("i", "j")).coarsen(i=3, j=3).any()  # pyright: ignore[reportAttributeAccessIssue]
        )
        # Note: coarsen seems not to be typed very well yet

        if self.config_save_img:
            coarsened_img = (coarsened_xda).astype(np.uint8) * np.uint8(255)
            save_img(coarsened_img, "arr_1x_result_3.png", __file__)
        if self.config_accumulate_outputs:
            coarsened_img = (coarsened_xda).astype(np.uint8) * np.uint8(255)
            outputs_accumulator["coarsened_img"] = coarsened_img

        result = np.sum(coarsened_xda).item()
        return result, outputs_accumulator

    def rasterize_main_loop(self, main_loop: npt.NDArray[Any]):
        raster_3x = np.zeros(3 * np.array(main_loop.shape), dtype=np.bool_)
        pipe_to_pattern_mapping = get_pipe_to_pattern_mapping()

        # Rasterize the pipes. Each symbol maps to a 3x3 unique pattern.
        # Note: padded contour of empty cells is ignored.
        for i in range(1, main_loop.shape[0] - 1):
            for j in range(1, main_loop.shape[1] - 1):
                fill_macro_pixel_3x(main_loop, raster_3x, pipe_to_pattern_mapping, i, j)

                if self.config_save_img_for_video:
                    save_img(
                        raster_3x,
                        f"arr_i{i:05d}_j{j:05d}.png",
                        __file__,
                        output_subdir="mazegen",
                    )

        return raster_3x


def parse_text_input(text: str) -> PuzzleInput:
    mapping = get_simple_pipes_mapping()
    for source, target in mapping.items():
        text = text.replace(source, target)

    input_array = parse_2d_string_array_to_u1(text)

    # Add a border of dots will ease later checks,
    # not having to care about data outside the borders
    padded_array = np.pad(input_array, pad_width=1, constant_values=mapping["."])

    return padded_array


def locate_starting_index(maze: PuzzleInput) -> tuple[int, int]:
    i, j = np.nonzero(maze == "S")
    assert i.size == 1
    assert j.size == 1
    return i[0], j[0]


def get_neighbour_indices_dict(i: int, j: int):
    return dict(zip(("top", "bottom", "left", "right"), get_neighbour_indices(i, j)))


def get_neighbour_indices(i: int, j: int) -> tuple[tuple[int, int], ...]:
    return ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1))


def explore_maze(maze: PuzzleInput, values: PuzzleInput, distance: int, i: int, j: int):
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


def put_good_pipe_in_place_of_starting_point(main_loop: npt.NDArray[Any]):
    i, j = locate_starting_index(main_loop)
    neighbour_dict = get_neighbour_indices_dict(i, j)
    allowed_pipes = get_allowed_pipes_for_direction()
    directions = [
        direction
        for direction, neighbour in neighbour_dict.items()
        if main_loop[neighbour] in allowed_pipes[direction]
    ]
    good_pipe = get_good_pipe(directions)

    main_loop[i, j] = good_pipe


def fill_macro_pixel_3x(
    maze: PuzzleInput,
    maze_3x: PuzzleInput,
    pipe_to_pattern_mapping: dict[str, np.bool_],
    i: int,
    j: int,
):
    maze_3x[3 * i : 3 * i + 3, 3 * j : 3 * j + 3] = pipe_to_pattern_mapping[maze[i, j]]


def get_good_pipe(directions: list[str]):
    if set(directions) == {"bottom", "top"}:
        return "│"
    elif set(directions) == {"left", "right"}:
        return "─"
    elif set(directions) == {"bottom", "right"}:
        return "┌"
    elif set(directions) == {"bottom", "left"}:
        return "┐"
    elif set(directions) == {"right", "top"}:
        return "└"
    elif set(directions) == {"left", "top"}:
        return "┘"


def render_2d_array_to_text(data: PuzzleInput) -> str:
    if data.dtype == np.bool_:
        data = data.astype(np.int8)
        result = "\n".join("".join(str(c) for c in line) for line in data)
        result = result.replace("0", "░").replace("1", "▓")
    else:
        result = "\n".join("".join(str(c) for c in line) for line in data)
    return result


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


def get_pipe_to_pattern_mapping() -> dict[str, np.bool_]:
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
    print(AdventOfCodeProblem202310().solve())
