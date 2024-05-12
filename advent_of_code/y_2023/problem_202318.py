from dataclasses import dataclass
from typing import Self

import numpy as np
import numpy.typing as npt

from advent_of_code.common.constants import (
    DOWN,
    LEFT,
    NEIGHBOUR_MOVES,
    RIGHT,
    UP,
    WELL_KNOW_DIRECTION_MAPPING,
    Direction,
)
from advent_of_code.common.protocols import AdventOfCodeProblem

type PuzzleInput = str


@dataclass(kw_only=True)
class AdventOfCodeProblem202318(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 18

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return text

    def solve_part_1(self, puzzle_input: PuzzleInput):
        dig_plan = parse_text_input_part_1(puzzle_input)
        pick_area_including_exterior = compute_area(dig_plan)
        return pick_area_including_exterior

    def solve_part_2(self, puzzle_input: PuzzleInput):
        dig_plan = parse_text_input_part_2(puzzle_input)
        pick_area_including_exterior = compute_area(dig_plan)
        return pick_area_including_exterior


@dataclass(frozen=True, kw_only=True)
class DigInstruction:
    direction: Direction
    meters: int
    color: str

    @classmethod
    def from_string(cls, string: str) -> Self:
        split = string.split(" ")
        direction = WELL_KNOW_DIRECTION_MAPPING[split[0]]
        meters = int(split[1])
        color = split[2][1:-1]
        return cls(direction=direction, meters=meters, color=color)

    @classmethod
    def from_hexadecimal_string(cls, string: str) -> Self:
        mapping: dict[int, Direction] = {
            0: RIGHT,
            1: DOWN,
            2: LEFT,
            3: UP,
        }
        color = string.split(" ")[2][2:-1]
        meters = int(color[:5], base=16)
        direction = mapping[int(color[-1])]
        return cls(direction=direction, meters=meters, color=color)


def compute_area(dig_plan: list[DigInstruction]) -> int:
    interior_points_count = compute_shoelace_formula(compute_polygon_coords(dig_plan))
    boundary_points_count = compute_internal_perimeter(dig_plan) + 4

    pick_area_including_exterior = compute_pick_polygon_area_formula(
        interior_points_count, boundary_points_count
    )
    return pick_area_including_exterior


def compute_pick_polygon_area_formula(
    interior_points_count: int, boundary_points_count: int
):
    """Compute the area of a polygon using the Pick's formula

    .. math::

        A = i + \frac{b}{2} - 1

    See `Pick's theorem <https://en.wikipedia.org/wiki/Pick%27s_theorem>`_ on Wikipedia

    Parameters
    ----------
    interior_points_count
        the number of integer points interior to the polygon
    boundary_points_count
        the number of integer points on its boundary

    Returns
    -------
        The area of the polygon
    """
    i = interior_points_count
    b = boundary_points_count
    return i + b // 2 - 1


def compute_shoelace_formula(coords: npt.NDArray[np.int32]):
    r"""Compute the area of a polygon using the shoelace formula

    Note
    ----
    The trapezoid formula variant is used.

    .. math::

        A = \frac 1 2 \sum_{i=1}^n (y_i + y_{i+1})(x_i - x_{i+1})

    See `Shoelace formula <https://en.wikipedia.org/wiki/Shoelace_formula>`_ on Wikipedia

    Parameters
    ----------
    coords
        Numpy array of shape (N, 2) containing the (x, y) couples of coordinates for the N points
        defining the polygon.

    Returns
    -------
        The area of the polygon defined by ``coords``
    """
    xcoords = coords[0]
    ycoords = coords[1]
    return np.abs(
        np.sum((ycoords + np.roll(ycoords, -1)) * (xcoords - np.roll(xcoords, -1))) // 2
    )


def compute_polygon_coords(dig_plan: list[DigInstruction]) -> npt.NDArray[np.int32]:
    points = [np.array((0, 0))]
    for instr in dig_plan:
        next_point = points[-1] + NEIGHBOUR_MOVES[instr.direction] * instr.meters
        points.append(next_point)
    coords = np.array(points).T
    return coords


def compute_internal_perimeter(dig_plan: list[DigInstruction]):
    return sum(instr.meters for instr in dig_plan)


def parse_text_input_part_1(text: str) -> list[DigInstruction]:
    lines = text.strip().split("\n")
    dig_plan = [DigInstruction.from_string(line) for line in lines]
    return dig_plan


def parse_text_input_part_2(text: str) -> list[DigInstruction]:
    lines = text.strip().split("\n")
    dig_plan = [DigInstruction.from_hexadecimal_string(line) for line in lines]
    return dig_plan


if __name__ == "__main__":
    print(AdventOfCodeProblem202318().solve())
