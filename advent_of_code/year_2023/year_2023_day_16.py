import queue
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import numpy.typing as npt

from advent_of_code.common import (
    adapt_recursion_limit,
    create_output_file_path,
    load_input_text_file_from_filename,
    parse_2d_string_array_to_uint8,
)
from advent_of_code.constants import MOVE_EAST, MOVE_NORTH, MOVE_SOUTH, MOVE_WEST
from advent_of_code.protocols import AdventOfCodeProblem

type PuzzleInput = npt.NDArray[np.uint8]


CELL_EMPTY_SPACE = ord(b".")
CELL_MIRROR_SLASH = ord(b"/")
CELL_MIRROR_BACKSLASH = ord(b"\\")
CELL_SPLITTER_V = ord(b"|")
CELL_SPLITTER_H = ord(b"-")
CELL_WALL = ord(b"O")
CELL_ENERGY = ord(b"#")

CELL_DIRECTIONS: dict[tuple[int, ...], int] = {
    tuple(MOVE_SOUTH): ord(b"v"),
    tuple(MOVE_EAST): ord(b">"),
    tuple(MOVE_NORTH): ord(b"^"),
    tuple(MOVE_WEST): ord(b"<"),
}

EXPLORED_IDX: dict[tuple[int, ...], int] = {
    tuple(MOVE_SOUTH): 0,
    tuple(MOVE_EAST): 1,
    tuple(MOVE_NORTH): 2,
    tuple(MOVE_WEST): 3,
}

# [visu] would look real good in a 2D engine, maybe pygame, or panda3d (with z=0 empty space, z=1 mirror)
# this can also be visualized in terminal directly.
# this is literally ray tracing?


@dataclass(kw_only=True)
class AdventOfCodeProblem202316(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 16

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return parse_text_input(text)

    def solve_part_1(self, puzzle_input: PuzzleInput):
        adapt_recursion_limit(5000)

        board = puzzle_input
        initial_beam = Beam(np.array((1, 0)), MOVE_EAST)
        result_one_less_iter = do_part_1(
            board, initial_beam=initial_beam, max_depth=2499
        )
        result = do_part_1(board, initial_beam=initial_beam, max_depth=2500)
        result_one_more_iter = do_part_1(
            board, initial_beam=initial_beam, max_depth=2501
        )
        assert result_one_less_iter < result
        assert result == result_one_more_iter
        return result

    def solve_part_2(self, puzzle_input: PuzzleInput):
        adapt_recursion_limit(5000)

        board = puzzle_input
        result_1 = do_part_2(board, max_depth=2500)
        assert result_1 == 7505
        result_2 = do_part_2(board, max_depth=2700)
        assert result_2 == 7521
        result_22 = do_part_2(board, max_depth=3000)
        assert result_22 == 7521
        result = result_22
        return result

    def write_visualizations_instructions_for_part_1(self):
        # This code generate the breadth-first sequence of events for the rays (10k lines)
        # It can now be consumed in a simulation rendered via pygame.
        self.log_part_1(self.parse_input_text_file(), max_depth=2501)

    def log_part_1(self, puzzle_input: PuzzleInput, max_depth: int):
        adapt_recursion_limit(5000)

        board = puzzle_input
        initial_beam = Beam(np.array((1, 0)), MOVE_EAST)
        _ = do_part_1(board, initial_beam=initial_beam, max_depth=max_depth)

        # Explore the initial Beam
        history = explore_beam_breadth_first(initial_beam, max_depth=max_depth)
        output_file_path = self.get_visualizations_instructions_for_part_1_file_path()
        import json

        text = ",\n".join([json.dumps((line)) for line in history])
        output_file_path.write_text(f"[\n{text}\n]")
        print(f"Saved text to {output_file_path}")

    def get_visualizations_instructions_for_part_1_file_path(self) -> Path:
        return create_output_file_path("history.json", "", self.year, self.day)


@dataclass(frozen=True)
class Beam:  # poignée
    position: npt.NDArray[np.int32]
    speed: npt.NDArray[np.int32]

    # can be zero, one, or two
    children: list["Beam"] = field(default_factory=list)


@dataclass(order=True)
class PrioritizedBeam:
    priority: int
    item: Beam = field(compare=False)


def explore_beam_breadth_first(
    root_beam: Beam, max_depth: int = 2501
) -> list[tuple[int, list[int], list[int]]]:
    history = []
    q: queue.PriorityQueue[PrioritizedBeam] = queue.PriorityQueue()
    depth = 0
    q.put(PrioritizedBeam(depth, root_beam))
    while not q.empty() and depth < max_depth:
        pr_beam = q.get()
        depth = pr_beam.priority
        beam = pr_beam.item
        # [visu] this log can be used to control
        print(f"{" " * (depth//50)} | {depth=}, {beam.position=}, {beam.speed=}")
        history.append(
            (
                depth,
                beam.position.tolist(),
                beam.speed.tolist(),
                # (beam.position[0], beam.position[1]),
                # (beam.speed[0], beam.speed[1]),
            )
        )
        for child_beam in beam.children:
            q.put(PrioritizedBeam(depth + 1, child_beam))

    return history


def do_part_1(board: PuzzleInput, initial_beam: Beam, max_depth: int = 100) -> int:
    explored: PuzzleInput = np.zeros((4, *board.shape), dtype=np.uint8)
    update_simulation(board, initial_beam, 0, max_depth, explored)
    energized_count = np.sum(np.logical_or.reduce(explored[:, 1:-1, 1:-1]))
    return energized_count


def do_part_2(board: PuzzleInput, max_depth: int = 100) -> int:
    energized_counts = []
    row_count = board.shape[0]
    col_count = board.shape[1]
    for row in range(1, row_count):
        initial_beam = Beam(np.array((row, 0)), MOVE_EAST)
        energized_count = do_part_1(board, initial_beam, max_depth=max_depth)
        print("E", initial_beam.position)
        energized_counts.append(energized_count)
        initial_beam = Beam(np.array((row, col_count - 1)), MOVE_WEST)
        energized_count = do_part_1(board, initial_beam, max_depth=max_depth)
        print("W", initial_beam.position)
        energized_counts.append(energized_count)
    for col in range(1, col_count):
        initial_beam = Beam(np.array((0, col)), MOVE_SOUTH)
        energized_count = do_part_1(board, initial_beam, max_depth=max_depth)
        print("S", initial_beam.position)
        energized_counts.append(energized_count)
        initial_beam = Beam(np.array((row_count - 1, col)), MOVE_NORTH)
        energized_count = do_part_1(board, initial_beam, max_depth=max_depth)
        print("N", initial_beam.position)
        energized_counts.append(energized_count)
    maximum = max(energized_counts)
    return maximum


def update_simulation(
    board: PuzzleInput, beam: Beam, depth: int, max_depth: int, explored: PuzzleInput
) -> None:
    if depth > max_depth:
        return
    next_position = beam.position + beam.speed
    coords = next_position[0], next_position[1]
    index = tuple((EXPLORED_IDX[tuple(beam.speed)], *coords))
    if explored[index] == 1:
        return
    explored[index] = 1

    cell = board[coords].item()
    append_children_to_beam(beam, next_position, cell)

    # [visu] can be reused to save_txt
    # energy_board = np.copy(board)
    # draw_energized(energy_board, beam, CELL_DIRECTIONS[tuple(beam.speed)])
    # print(render_parsed_input(energy_board))

    # print(beam.position, beam.speed)  # Use this to draw [visu] the beams

    for beam in beam.children:
        update_simulation(board, beam, depth + 1, max_depth, explored)


def append_children_to_beam(
    beam: Beam, next_position: npt.NDArray[np.int32], cell: int
):
    if cell == CELL_EMPTY_SPACE:
        beam.children.append(Beam(next_position, beam.speed))
    elif cell == CELL_MIRROR_SLASH:
        speed = -beam.speed[::-1]
        beam.children.append(Beam(next_position, speed))
    elif cell == CELL_MIRROR_BACKSLASH:
        speed = beam.speed[::-1]
        beam.children.append(Beam(next_position, speed))
    elif cell == CELL_SPLITTER_V:
        if beam.speed[1] == 0:
            beam.children.append(Beam(next_position, beam.speed))
        else:
            beam.children.append(Beam(next_position, MOVE_SOUTH))
            beam.children.append(Beam(next_position, MOVE_NORTH))
    elif cell == CELL_SPLITTER_H:
        if beam.speed[0] == 0:
            beam.children.append(Beam(next_position, beam.speed))
        else:
            beam.children.append(Beam(next_position, MOVE_EAST))
            beam.children.append(Beam(next_position, MOVE_WEST))


def draw_energized(board: PuzzleInput, beam: Beam, fill_value: bytes):
    board[tuple(beam.position)] = fill_value
    for beam in beam.children:
        draw_energized(board, beam, fill_value)


def render_parsed_input(parsed_input: PuzzleInput) -> str:
    return "\n".join(line.tostring().decode() for line in parsed_input)


def parse_input_text_file() -> PuzzleInput:
    text = load_input_text_file_from_filename(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> PuzzleInput:
    input_array = parse_2d_string_array_to_uint8(text)
    padded = np.pad(input_array, pad_width=1, constant_values=CELL_WALL)
    return padded


if __name__ == "__main__":
    print(AdventOfCodeProblem202316().solve())
