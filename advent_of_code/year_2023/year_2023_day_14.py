from dataclasses import dataclass
from pathlib import Path

import numpy as np
import numpy.typing as npt
import xarray as xr

from advent_of_code.common import (
    create_output_file_path,
    lines_to_2d_uint8_array,
    parse_2d_string_array_to_uint8,
)
from advent_of_code.protocols import AdventOfCodeProblem

# NORTH = 0
# WEST = 1
# SOUTH = 2
# EAST = 3

# [visu] would look real good in a 2D engine, maybe pygame, or panda3d (with z=0 floor, z=1 rocks)
# [visu] isometric 2.5d with rotation
# [visu] best would be to simulate the board in Blender and script it using Python

# tag: simulation
type PuzzleInput = npt.NDArray[np.uint8]


@dataclass(kw_only=True)
class AdventOfCodeProblem202314(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 14

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_2d_string_array_to_uint8(text)

    def solve_part_1(self, puzzle_input: PuzzleInput):
        return compute_total_load_for_north(puzzle_input)

    def solve_part_2(self, puzzle_input: PuzzleInput):
        # Kind of related to advent_of_code/year_2023/year_2023_day_08.py (detect a cycle)

        init_rot = 4
        max_iter = 1200
        state = puzzle_input
        search_result = detect_cycle(init_rot, max_iter, state)
        assert search_result is not None
        start, period, state_history = search_result
        print(start, period, state_history)

        state_wanted = attain_wanted_state(1000000000, start, period, state_history)
        state_lines = get_list_of_str(state_wanted, 0)
        total_load = compute_total_load_from_state_lines(state_lines)
        return total_load

    def write_visualizations_instructions_for_part_2(self):
        self.log_part_2(self.parse_input_text_file(), max_full_rotations_count=150)

    def log_part_2(self, puzzle_input: PuzzleInput, max_full_rotations_count: int):
        init_rot = 4
        next_board = puzzle_input
        next_board_xda = xr.DataArray(data=next_board, dims=["row", "col"])
        board_history = [next_board_xda]
        for full_rotation_count in range(max_full_rotations_count):
            print(full_rotation_count)
            for d in range(1, 5):
                k = init_rot - d
                next_board = np.rot90(
                    update_state(get_list_of_str(next_board, k)), 4 - k
                )
                next_board_xda = xr.DataArray(data=next_board, dims=["row", "col"])
                board_history.append(next_board_xda)

        output_file_path = self.get_visualizations_instructions_for_part_2_file_path()
        chunks = (
            len(board_history),
            next_board_xda.shape[0],
            next_board_xda.shape[1],
        )
        data_cube = xr.Dataset({"board_history": xr.concat(board_history, dim="time")})
        data_cube.to_zarr(
            store=output_file_path,
            mode="w",
            encoding=dict(board_history=dict(chunks=chunks)),
        )
        print(f"Saved zarr to {output_file_path}")

    def get_visualizations_instructions_for_part_2_file_path(self) -> Path:
        return create_output_file_path("history.zarr", "", self.year, self.day)


def compute_total_load_for_north(data: PuzzleInput) -> int:
    # North (k=3) (initial rotation of 270 degrees)
    return compute_total_load_part_1(get_list_of_str(data, 3))


def compute_total_load_part_1(parsed_input: list[str]):
    minimal_repr = get_minimal_representation(parsed_input)
    sum_of_loads = sum(sum(sum_rock_values(*y) for y in x) for x in minimal_repr)
    return sum_of_loads


def sum_rock_values(goal: int, length: int) -> int:
    go = goal
    le = length
    return ((go * (go + 1)) - ((go - le) * (go - le + 1))) // 2


# [visu] The visualization only needs to be ran on one cycle!
def detect_cycle(
    init_rot: int, max_iter: int, state: PuzzleInput
) -> tuple[int, int, list[PuzzleInput]] | None:
    state_history: list[PuzzleInput] = [state]
    for i in range(max_iter):
        print(i)
        state = update_state_for_one_full_rotation(state, init_rot)
        state_history.append(state)
        if sum(int(np.all(state_history[i] == h)) for h in state_history) > 1:
            indices = tuple(
                t[0]
                for t in (
                    (k, np.all(state_history[i] == h))
                    for k, h in enumerate(state_history)
                )
                if t[1]
            )
            print(f"{i=} found duplicates for {indices=}")
            if len(indices) == 2:
                period = indices[1] - indices[0]
                print(f"{i=} found duplicates for {indices=} and {period=}")
                # The problem should be nice so we can return immediately the
                # loop index start + period
                start = indices[0]
                return start, period, state_history[start : start + period]

                # i=141 found some repeat for indices=(107, 141)
                # i=141 found some repeat for indices=(107, 141) and delta=34
                # 142
                # i=142 found some repeat for indices=(108, 142)
                # i=142 found some repeat for indices=(108, 142) and delta=34


def attain_wanted_state(
    wanted_cycles: int, start: int, period: int, state_history: list[PuzzleInput]
):
    # Note: only works for wanted_cycles greater than the initial one marking the
    # entering in periodic regime
    state_wanted = state_history[(wanted_cycles - start) % period]
    return state_wanted


def update_state_for_one_full_rotation(
    parsed_input: PuzzleInput, rot: int
) -> PuzzleInput:
    next_board = parsed_input

    # North (k=3), West (k=2), South (k=1), East (k=0)
    for d in range(1, 5):
        k = rot - d
        next_board = np.rot90(update_state(get_list_of_str(next_board, k)), 4 - k)

    return next_board


def update_state(parsed_input: list[str]) -> PuzzleInput:
    minimal_repr = get_minimal_representation(parsed_input)
    rendered_lines = minimal_to_list_of_str(minimal_repr)
    return lines_to_2d_uint8_array(rendered_lines)


def get_minimal_representation(
    parsed_input: list[str],
) -> list[list[tuple[int, int]]]:
    split = [line.split("#") for line in parsed_input]
    cube_rock_indices = tuple(
        tuple((*(idx for idx, c in enumerate(li) if c == "#"), len(li)))
        for li in parsed_input
    )
    round_rock_counts = tuple(
        tuple(sum(el == "O" for el in li) for li in line) for line in split
    )
    minimal_repr = [
        list((goal, length) for goal, length in zip(idx, rock_count))
        for idx, rock_count in zip(cube_rock_indices, round_rock_counts)
    ]

    return minimal_repr


def minimal_to_list_of_str(minimal_repr: list[list[tuple[int, int]]]) -> list[str]:
    rendered_lines = []
    for line in minimal_repr:
        parts = []
        pgoal, plength = line[0]
        parts.append("." * (pgoal - plength) + "O" * plength)
        for i in range(1, len(line)):
            cgoal, clength = line[i]
            total_length = cgoal - pgoal - 1
            parts.append("." * (total_length - clength) + "O" * clength)
            pgoal, plength = cgoal, clength
        rendered_line = "#".join(parts)
        rendered_lines.append(rendered_line)
    return rendered_lines


def compute_total_load_from_state_lines(state_lines: list[str]):
    total_load = 0
    for index, line in enumerate((reversed(state_lines)), 1):
        total_load += sum(1 for c in line if c == "O") * index
    return total_load


def get_list_of_str(input_array: PuzzleInput, k: int) -> list[str]:
    arr = np.rot90(input_array, k)
    tolist = arr.tolist()
    data = ["".join(chr(i) for i in li) for li in tolist]
    return data


if __name__ == "__main__":
    # print(AdventOfCodeProblem202314().solve())
    AdventOfCodeProblem202314().write_visualizations_instructions_for_part_2()
