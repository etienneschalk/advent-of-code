from dataclasses import dataclass

import numpy as np
import xarray as xr

from advent_of_code.common import (
    load_input_text_file_from_filename,
    parse_2d_string_array_to_uint8_xarray,
    render_2d_data_array,
)
from advent_of_code.constants import NEIGHBOUR_MOVES, Position, is_out_of_bounds
from advent_of_code.protocols import AdventOfCodeProblem

type PuzzleInput = xr.DataArray


@dataclass(kw_only=True)
class AdventOfCodeProblem202321(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 21

    def solve_part_1(self, puzzle_input: PuzzleInput):
        garden = puzzle_input
        initial_pos = get_starting_position(garden)
        max_iter = 64
        _, reached = run_steps(garden, initial_pos, max_iter)
        result = len(reached)
        return result

    def solve_part_2(self, puzzle_input: PuzzleInput):
        garden = puzzle_input

        initial_pos = get_starting_position(garden)
        max_iter = 65 * 2

        _, _, reached_even_xda, reached_odd_xda = run_steps_details(
            garden, initial_pos, max_iter
        )
        odd = reached_odd_xda
        eve = reached_even_xda

        # 1x1
        concat_1 = odd
        diamond_1x1 = create_diamond_mask_array(concat_1)

        # 3x3
        new_coords3 = list(range(3 * odd.row.size))
        concat_3 = xr.concat(
            [
                xr.concat([eve, odd, eve], dim="col"),
                xr.concat([odd, eve, odd], dim="col"),
                xr.concat([eve, odd, eve], dim="col"),
            ],
            dim="row",
        ).assign_coords(dict(row=new_coords3, col=new_coords3))
        diamond_3x3 = create_diamond_mask_array(concat_3)

        # 5x5
        new_coords5 = list(range(5 * odd.row.size))
        concat_5 = xr.concat(
            [
                xr.concat([odd, eve, odd, eve, odd], dim="col"),
                xr.concat([eve, odd, eve, odd, eve], dim="col"),
                xr.concat([odd, eve, odd, eve, odd], dim="col"),
                xr.concat([eve, odd, eve, odd, eve], dim="col"),
                xr.concat([odd, eve, odd, eve, odd], dim="col"),
            ],
            dim="row",
        ).assign_coords(dict(row=new_coords5, col=new_coords5))
        diamond_5x5 = create_diamond_mask_array(concat_5)

        # Interpolation
        x, y = compute_points_for_interpolation(
            concat_1, diamond_1x1, concat_3, diamond_3x3, concat_5, diamond_5x5
        )

        garden_side = garden.shape[0]  # 131
        target_step_count = 26501365
        period = target_step_count // garden_side
        result = evaluate_quadratic_equation(x, y, period)

        return result

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input(text)


def count_reached_garden_plots(max_iter: int, history: list[str]):
    return history[max_iter - 1].count("O")


def run_steps(garden: xr.DataArray, initial_pos: Position, max_iter: int):
    a, b, _, _ = run_steps_details(garden, initial_pos, max_iter)
    return a, b


def run_steps_details(
    garden: xr.DataArray, initial_pos: Position, max_iter: int, *, silent: bool = True
) -> tuple[list[str], set[Position], xr.DataArray, xr.DataArray]:
    iter_count = 0
    pos = initial_pos
    q = set()
    to_explore = []
    q.add(pos)
    history: list[str] = []
    # Aggressive anti-backtracking
    explored = garden.copy(data=np.zeros_like(garden.data, dtype=np.bool_))
    reached_even: set[Position] = set()
    reached_odd: set[Position] = set()
    reached_even_xda = garden.copy(data=np.zeros_like(garden.data, dtype=np.bool_))
    reached_odd_xda = garden.copy(data=np.zeros_like(garden.data, dtype=np.bool_))

    while iter_count < max_iter:
        iter_count += 1
        if not silent:
            print(iter_count)
        to_explore.extend(q)
        q.clear()
        for pos in to_explore:
            if pos == initial_pos:
                garden[pos] = ord(b"S")
            else:
                garden[pos] = ord(b".")
            if explored[pos]:
                continue

            explored[pos] = True

            for direction, move in NEIGHBOUR_MOVES.items():
                next_pos_array = pos + move
                next_pos: Position = next_pos_array[0], next_pos_array[1]
                if is_out_of_bounds(direction, pos, (garden.shape[0], garden.shape[1])):
                    continue
                if garden[next_pos] == ord(b".") or garden[next_pos] == ord(b"S"):
                    garden[next_pos] = ord(b"O")
                    q.add(next_pos)
                    if iter_count % 2 == 0:
                        reached_even.add(next_pos)
                        reached_even_xda[next_pos] = True
                    else:
                        reached_odd.add(next_pos)
                        reached_odd_xda[next_pos] = True

        to_explore.clear()
        history.append(render_2d_data_array(garden))
        if not silent:
            print(history[-1])

    # This metric is to be used to count

    if max_iter % 2 == 0:
        return history, reached_even, reached_even_xda, reached_odd_xda
    else:
        return history, reached_odd, reached_even_xda, reached_odd_xda


def run_steps_old(
    garden: xr.DataArray, initial_pos: Position, max_iter: int, *, silent: bool = True
) -> list[str]:
    iter_count = 0
    pos = initial_pos
    q = []
    to_explore = []
    q.extend((i, pos) for i in range(4))
    history = []

    while iter_count < max_iter:
        iter_count += 1
        if not silent:
            print(iter_count)
        to_explore.extend(q)
        q.clear()
        for _, pos in to_explore:
            if pos == initial_pos:
                garden[pos] = ord(b"S")
            else:
                garden[pos] = ord(b".")

            for direction, move in NEIGHBOUR_MOVES.items():
                next_pos = move + pos
                next_pos = tuple(next_pos)
                if is_out_of_bounds(direction, pos, (garden.shape[0], garden.shape[1])):
                    continue
                if garden[next_pos] == ord(b".") or garden[next_pos] == ord(b"S"):
                    garden[next_pos] = ord(b"O")
                    q.append((direction, next_pos))
        to_explore.clear()
        history.append(render_2d_data_array(garden))
        if not silent:
            print(history[-1])

    return history


def get_free_cells_xda(garden: PuzzleInput):
    return (garden == ord(b".")) | (garden == ord(b"S"))


def get_starting_position(garden: PuzzleInput) -> Position:
    stacked = garden.stack(z=("row", "col"))
    start_xda = stacked[stacked == ord(b"S")]
    row_idx = start_xda.row.item()
    col_idx = start_xda.col.item()
    initial_pos = (row_idx, col_idx)
    return initial_pos


def create_diamond_mask_array(input_xda: xr.DataArray) -> xr.DataArray:
    xda = create_diamond_int_array(input_xda)
    assert xda.sel(row=xda.row.size // 2, col=xda.row.size // 2) == 0
    return (xda.where(np.abs(xda) <= xda.row.size // 2, -1) >= 0).astype(np.uint8)


def create_diamond_int_array(xda: xr.DataArray) -> xr.DataArray:
    diamond_arr = np.abs((xda.row.values[:, None] - (xda.row.size // 2))) + (
        np.abs(xda.col.values - (xda.row.size // 2))
    )
    return xda.copy(data=diamond_arr)


def parse_input_text_file() -> PuzzleInput:
    text = load_input_text_file_from_filename(__file__)
    parsed = parse_text_input(text)
    return parsed


def evaluate_quadratic_equation(
    x: tuple[int, int, int], y: tuple[int, int, int], target: int
) -> int:
    """Evaluate Quadratic Equation with Numpy

    Thanks https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/kebm6ak/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    Alternatively, Lagrange polynomials could have been reimplemented.
    See https://en.wikipedia.org/wiki/Lagrange_polynomial

    The area growing is x**2, so 3 points are required to interpolate, hence the previous computing
    of 1x1, 3x3 and 5x5 grids

    Parameters
    ----------
    x
        Control Points' abscissa
    y
        Control Points' ordinates
    target
        Value to feed to the interpolated polynomial

    Returns
    -------
        Rounded evaluation of the polynomial for given target
    """
    # Fit a quadratic polynomial (degree=2) through the points
    coefficients = np.polyfit(x, y, 2)

    # Evaluate the quadratic equation at the given target value
    result = np.polyval(coefficients, target)

    return round(result)  # pyright: ignore[reportGeneralTypeIssues]


def parse_text_input(text: str) -> PuzzleInput:
    return parse_2d_string_array_to_uint8_xarray(text)


def compute_points_for_interpolation(
    concat_1: xr.DataArray,
    diamond_1x1: xr.DataArray,
    concat_3: xr.DataArray,
    diamond_3x3: xr.DataArray,
    concat_5: xr.DataArray,
    diamond_5x5: xr.DataArray,
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    x = (0, 1, 2)
    y = (
        concat_1.where(diamond_1x1, 0).sum().item(),
        concat_3.where(diamond_3x3, 0).sum().item(),
        concat_5.where(diamond_5x5, 0).sum().item(),
    )
    return x, y


if __name__ == "__main__":
    print(AdventOfCodeProblem202321().solve_all())
