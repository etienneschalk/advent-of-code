from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from advent_of_code.common import load_input_text_file
from advent_of_code.constants import (
    DOWN,
    LEFT,
    NEIGHBOUR_MOVES,
    RIGHT,
    UP,
    WELL_KNOW_DIRECTION_MAPPING,
    Direction,
)


@dataclass(frozen=True, kw_only=True)
class DigInstruction:
    direction: Direction
    meters: int
    color: str

    @classmethod
    def from_string(cls, string: str) -> "DigInstruction":
        split = string.split(" ")
        direction = WELL_KNOW_DIRECTION_MAPPING[split[0]]
        meters = int(split[1])
        color = split[2][1:-1]
        return cls(direction=direction, meters=meters, color=color)

    @classmethod
    def from_hexadecimal_string(cls, string: str) -> "DigInstruction":
        mapping = {
            0: RIGHT,
            1: DOWN,
            2: LEFT,
            3: UP,
        }
        color = string.split(" ")[2][2:-1]
        meters = int(color[:5], base=16)
        direction = mapping[int(color[-1])]
        return cls(direction=direction, meters=meters, color=color)


ProblemDataType = list[DigInstruction]


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    dig_plan = parse_input_text_file()
    pick_area_including_exterior = compute_area(dig_plan)
    return pick_area_including_exterior


def compute_part_2():
    text = load_input_text_file(__file__)
    dig_plan = parse_text_input_part_2(text)
    pick_area_including_exterior = compute_area(dig_plan)
    return pick_area_including_exterior


def compute_area(dig_plan: list[DigInstruction]) -> int:
    pick_area_including_exterior = compute_pick_polygon_area_formula(
        compute_shoelace_formula(compute_polygon_coords(dig_plan)),
        compute_internal_perimeter(dig_plan) + 4,
    )
    return pick_area_including_exterior


def compute_pick_polygon_area_formula(
    interior_points_count: int, boundary_points_count: int
):
    i = interior_points_count
    b = boundary_points_count
    return i + b // 2 - 1


def compute_shoelace_formula(coords: npt.NDArray[np.int32]):
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


def compute_internal_perimeter(dig_plan):
    return sum(instr.meters for instr in dig_plan)


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    lines = text.strip().split("\n")
    dig_plan = [DigInstruction.from_string(line) for line in lines]
    return dig_plan


def parse_text_input_part_2(text: str) -> ProblemDataType:
    lines = text.strip().split("\n")
    dig_plan = [DigInstruction.from_hexadecimal_string(line) for line in lines]
    return dig_plan


if __name__ == "__main__":
    main()
