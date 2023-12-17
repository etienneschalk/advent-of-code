import queue
from dataclasses import dataclass, field
from typing import Literal

import numpy as np
import numpy.typing as npt

from advent_of_code.common import load_input_text_file

# Literally copied from
# https://github.com/tbeu/AdventOfCode/blob/master/2023/day17/day17.cpp
# I had no idea how to implement this one without spending too much time.
# I figured out I would use my retro-engineering skills here...
# Other source: https://fr.wikipedia.org/wiki/Algorithme_de_Dijkstra

HeatMap = npt.NDArray[np.uint8]
Position = tuple[int, int]
Step = np.uint8

# In trigonometrical order: E, N, W, S

EastType = Literal[0]
NorthType = Literal[1]
WestType = Literal[2]
SouthType = Literal[3]

EAST: EastType = 0
NORTH: NorthType = 1
WEST: WestType = 2
SOUTH: SouthType = 3

Direction = Literal[EastType, NorthType, WestType, SouthType]

MOVE_NULL = np.array((0, 0))
MOVE_EAST = np.array((0, 1))
MOVE_NORTH = np.array((-1, 0))
MOVE_WEST = np.array((0, -1))
MOVE_SOUTH = np.array((1, 0))

NEIGHBOUR_MOVES = {
    EAST: MOVE_EAST,
    NORTH: MOVE_NORTH,
    WEST: MOVE_WEST,
    SOUTH: MOVE_SOUTH,
}


# The State is more complex than the usual dijkstra of explored nodes
# State is not only the node and its cost, but also
# the amount of steps in a given direction
@dataclass(frozen=True, order=True)
class State:
    # Heat is considered for comparison, but not for identity (priority queue)
    heat: np.uint8 = field(hash=False, compare=True)
    # Position, Direction and Step are considered for identity,
    # but not for comparison (hash set)
    position: Position = field(hash=True, compare=False)
    direction: Direction = field(hash=True, compare=False)
    step: Step = field(hash=True, compare=False)


# # See https://docs.python.org/3/library/queue.html#queue.PriorityQueue
# @dataclass(order=True)
# class PrioritizedState:
#     priority: int
#     item: Any = field(compare=False)


def dijkstra(
    heatmap: HeatMap,
    start: Position,
    end: Position,
    min_step: Direction = 1,
    max_step: Direction = 3,
    *,
    max_iter=2000,
) -> int:
    """Compute the shortest path from start to end in given heatmap,
    using min and max steps.

    Parameters
    ----------
    heatmap
        Numpy 2-D array containing heat (weight), positive integers.
    start
        Initial given position in the heatmap
    end
        Final wanted position in the heatmap
    min_step, optional
        Permitted minimal amount of consecutive steps in the
        same direction, inclusive, by default 1
    max_step, optional
        Permitted maximal amount of consecutive steps in the
        same direction, inclusive, by default 3
    max_iter, optional
        Guard not to be stuck if an infinite loop
    Returns
    -------
        The path with the least heat loss from start to end in the heatmap.
    """
    # Visited states is a set backed by a dict of manually hashed state keys
    visited_states: dict[int, State] = {}

    # Queue of State (note: least heat = most priority)
    q = queue.PriorityQueue()

    for next_direction in NEIGHBOUR_MOVES.keys():
        q.put(State(0, start, next_direction, 1))

    iter_count = 0
    while not q.empty() and iter_count < max_iter:
        iter_count += 1
        state: State = q.get()

        # Destination is reached with permitted amount of steps
        if state.position == end and state.step >= min_step:
            return state.heat

        for next_direction, move in NEIGHBOUR_MOVES.items():
            # An immediate U-turn is illegal
            if is_opposite_direction(next_direction, state.direction):
                continue
            if is_out_of_bounds(next_direction, state.position, heatmap.shape):
                continue

            is_a_turn = next_direction != state.direction
            if is_a_turn:
                if state.step < min_step:
                    continue
                next_step = 1
            else:
                if state.step >= max_step:
                    continue
                next_step = state.step + 1

            next_position = tuple(state.position + move)
            next_heat = state.heat + heatmap[next_position]
            next_state = State(next_heat, next_position, next_direction, next_step)

            next_state_hash = hash(next_state)
            if next_state_hash in visited_states:
                # I cannot rely on the hash for set usage,
                # so I use directly manually my own hash in a dict.
                # The idea is that the heat does not participate in the hash.
                current_stored_state = visited_states[next_state_hash]
                if next_state.heat < current_stored_state.heat:
                    # just to update the heat... dataclass is frozen
                    visited_states[next_state_hash] = next_state
                    q.put(next_state)
            else:
                visited_states[next_state_hash] = next_state
                q.put(next_state)

    return -1


def is_opposite_direction(a: Direction, b: Direction) -> bool:
    # 2 90deg turns, 4 turns = full rotation
    return a == (b + 2) % 4


def is_out_of_bounds(
    direction: Direction, position: Position, shape: tuple[int, int]
) -> bool:
    return (
        (direction == SOUTH and position[0] == shape[0] - 1)
        or (direction == EAST and position[1] == shape[1] - 1)
        or (direction == NORTH and position[0] == 0)
        or (direction == WEST and position[1] == 0)
    )


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    parsed_input = parse_input_text_file()
    start = (0, 0)
    end = tuple((parsed_input.shape[0] - 1, parsed_input.shape[1] - 1))
    least_heat_loss = dijkstra(parsed_input, start, end, 1, 3, max_iter=250_000)
    return least_heat_loss


def compute_part_2():
    parsed_input = parse_input_text_file()
    start = (0, 0)
    end = tuple((parsed_input.shape[0] - 1, parsed_input.shape[1] - 1))
    least_heat_loss = dijkstra(parsed_input, start, end, 4, 10, max_iter=800_000)
    return least_heat_loss


def parse_input_text_file() -> HeatMap:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> HeatMap:
    lines = text.strip().split("\n")
    input_array = np.array([[int(c) for c in line] for line in lines])
    return input_array


if __name__ == "__main__":
    main()
