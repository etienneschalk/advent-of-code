from typing import Literal

import numpy as np

Position = tuple[int, int]

EastType = Literal[0]
NorthType = Literal[1]
WestType = Literal[2]
SouthType = Literal[3]

Direction = Literal[EastType, NorthType, WestType, SouthType]

EAST: EastType = 0
NORTH: NorthType = 1
WEST: WestType = 2
SOUTH: SouthType = 3

RIGHT = EAST
UP = NORTH
LEFT = WEST
DOWN = SOUTH


MOVE_NULL = np.array((0, 0))
MOVE_EAST = MOVE_RIGHT = np.array((0, 1))
MOVE_NORTH = MOVE_NORTH = np.array((-1, 0))
MOVE_WEST = MOVE_WEST = np.array((0, -1))
MOVE_SOUTH = MOVE_SOUTH = np.array((1, 0))

NEIGHBOUR_MOVES: dict[Direction, np.ndarray] = {
    EAST: MOVE_EAST,
    NORTH: MOVE_NORTH,
    WEST: MOVE_WEST,
    SOUTH: MOVE_SOUTH,
}

WELL_KNOW_DIRECTION_MAPPING: dict[str, Direction] = {
    **{"R": RIGHT, "U": UP, "L": LEFT, "D": DOWN},
    **{"E": RIGHT, "N": UP, "W": LEFT, "S": DOWN},
}


def is_out_of_bounds(
    direction: Direction, position: Position, shape: tuple[int, int]
) -> bool:
    return (
        (direction == SOUTH and position[0] == shape[0] - 1)
        or (direction == EAST and position[1] == shape[1] - 1)
        or (direction == NORTH and position[0] == 0)
        or (direction == WEST and position[1] == 0)
    )


def is_opposite_direction(a: Direction, b: Direction) -> bool:
    # 2 90deg turns, 4 turns = full rotation
    return a == (b + 2) % 4
