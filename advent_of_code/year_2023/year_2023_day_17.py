import queue
from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt

from advent_of_code.common import parse_2d_string_array_to_uint8
from advent_of_code.constants import (
    NEIGHBOUR_MOVES,
    Direction,
    Position,
    is_opposite_direction,
    is_out_of_bounds,
)
from advent_of_code.protocols import AdventOfCodeProblem

# Literally copied from
# https://github.com/tbeu/AdventOfCode/blob/master/2023/day17/day17.cpp
# I had no idea how to implement this one without spending too much time.
# I figured out I would use my retro-engineering skills here...
# Other source: https://fr.wikipedia.org/wiki/Algorithme_de_Dijkstra

type HeatMap = npt.NDArray[np.uint8]
type PuzzleInput = HeatMap


@dataclass(kw_only=True)
class AdventOfCodeProblem202317(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 17

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_2d_string_array_to_uint8(text) - np.uint8(ord("0"))

    def solve_part_1(self, puzzle_input: PuzzleInput):
        return self.solve_part(puzzle_input, 1, 3, 250_000)

    def solve_part_2(self, puzzle_input: PuzzleInput):
        return self.solve_part(puzzle_input, 4, 10, 800_000)

    def solve_part(
        self,
        puzzle_input: PuzzleInput,
        min_step: int,
        max_step: int,
        max_iter: int,
    ):
        start = (0, 0)
        end = tuple((puzzle_input.shape[0] - 1, puzzle_input.shape[1] - 1))
        end = (end[0], end[1])  # make type system happy
        least_heat_loss = dijkstra(
            puzzle_input, start, end, min_step, max_step, max_iter=max_iter
        )
        return least_heat_loss


# The State is more complex than the usual dijkstra of explored nodes
# State is not only the node and its cost, but also
# the amount of steps in a given direction
@dataclass(frozen=True, order=True)
class State:
    # Heat is considered for comparison, but not for identity (priority queue)
    heat: int = field(hash=False, compare=True)
    # Position, Direction and Step are considered for identity,
    # but not for comparison (hash set)
    position: Position = field(hash=True, compare=False)
    direction: Direction = field(hash=True, compare=False)
    step: int = field(hash=True, compare=False)


# # See https://docs.python.org/3/library/queue.html#queue.PriorityQueue
# @dataclass(order=True)
# class PrioritizedState:
#     priority: int
#     item: Any = field(compare=False)


def dijkstra(
    heatmap: HeatMap,
    start: Position,
    end: Position,
    min_step: int = 1,
    max_step: int = 3,
    *,
    max_iter: int = 2000,
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
    q: queue.PriorityQueue[State] = queue.PriorityQueue()

    for next_direction in NEIGHBOUR_MOVES.keys():
        q.put(State((0), start, next_direction, (1)))

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
            if is_out_of_bounds(next_direction, state.position, heatmap.shape):  # type: ignore
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
            next_state = State(next_heat, next_position, next_direction, next_step)  # type: ignore

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


# def parse_text_input(text: str) -> HeatMap:
#     lines = text.strip().split("\n")
#     input_array = np.array([[int(c) for c in line] for line in lines])
#     return input_array


if __name__ == "__main__":
    print(AdventOfCodeProblem202317().solve_all())
