from dataclasses import dataclass, field

import numpy as np

from advent_of_code.common import adapt_recursion_limit, load_input_text_file

ProblemDataType = np.ndarray


MOVE_NULL = np.array((0, 0))
MOVE_SOUTH = np.array((1, 0))
MOVE_EAST = np.array((0, 1))
MOVE_NORTH = np.array((-1, 0))
MOVE_WEST = np.array((0, -1))

CELL_EMPTY_SPACE = b"."
CELL_MIRROR_FSLASH = b"/"
CELL_MIRROR_BSLASH = b"\\"
CELL_SPLITTER_V = b"|"
CELL_SPLITTER_H = b"-"
CELL_WALL = b"O"
CELL_ENERGY = b"#"

CELL_DIRECTIONS = {
    tuple(MOVE_SOUTH): b"v",
    tuple(MOVE_EAST): b">",
    tuple(MOVE_NORTH): b"^",
    tuple(MOVE_WEST): b"<",
}

EXPLORED_IDX = {
    tuple(MOVE_SOUTH): 0,
    tuple(MOVE_EAST): 1,
    tuple(MOVE_NORTH): 2,
    tuple(MOVE_WEST): 3,
}


@dataclass(frozen=True)
class Beam:  # poignée
    # position: tuple[int, int]
    # speed: tuple[int, int]
    position: np.ndarray
    speed: np.ndarray
    # can be zero, one, or two
    children: list["Beam"] = field(default_factory=list)


def main():
    adapt_recursion_limit(10000)
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    board = parse_input_text_file()
    initial_beam = Beam(np.array((1, 0)), MOVE_EAST)
    result_one_less_iter = do_part_1(board, initial_beam=initial_beam, max_depth=2499)
    result = do_part_1(board, initial_beam=initial_beam, max_depth=2500)
    result_one_more_iter = do_part_1(board, initial_beam=initial_beam, max_depth=2501)
    assert result_one_less_iter < result
    assert result == result_one_more_iter
    return result


def do_part_1(board: ProblemDataType, initial_beam: Beam, max_depth: int = 100) -> int:
    explored = np.zeros((4, *board.shape), dtype=np.uint8)
    update_simulation(board, initial_beam, 0, max_depth, explored)

    # energy_board = np.full_like(board, CELL_EMPTY_SPACE)
    # draw_energized(energy_board, initial_beam, CELL_ENERGY)
    # # Remove walls, they contain the initial out of bound beam.
    # energy_board = energy_board[1:-1, 1:-1]
    # print(render_parsed_input(energy_board))
    # energized_count = np.sum(energy_board == CELL_ENERGY)

    energized_count = np.sum(np.logical_or.reduce(explored[:, 1:-1, 1:-1]))
    return energized_count


def do_part_2(board: ProblemDataType, max_depth: int = 100) -> int:
    energized_counts = []
    row_count = board.shape[0]
    col_count = board.shape[1]
    for row in range(1, row_count):
        initial_beam = Beam(np.array((row, 0)), MOVE_EAST)
        energized_count = do_part_1(board, initial_beam, max_depth=max_depth)
        print(initial_beam.position)
        energized_counts.append(energized_count)
        initial_beam = Beam(np.array((row, col_count - 1)), MOVE_WEST)
        energized_count = do_part_1(board, initial_beam, max_depth=max_depth)
        print(initial_beam.position)
        energized_counts.append(energized_count)
    for col in range(1, col_count):
        initial_beam = Beam(np.array((0, col)), MOVE_SOUTH)
        energized_count = do_part_1(board, initial_beam, max_depth=max_depth)
        print(initial_beam.position)
        energized_counts.append(energized_count)
        initial_beam = Beam(np.array((row_count - 1, col)), MOVE_NORTH)
        energized_count = do_part_1(board, initial_beam, max_depth=max_depth)
        print(initial_beam.position)
        energized_counts.append(energized_count)
    maximum = max(energized_counts)
    return maximum


# def do_part_2(board: ProblemDataType, max_depth: int = 100) -> int:
#     energized_counts = []
#     for row in range(1, board.shape[0] - 1):
#         initial_beam = Beam(np.array((row, 1)), MOVE_RIGHT)
#         energized_count = do_part_1(board, initial_beam, max_depth=max_depth)
#         energized_counts.append(energized_count)
#         initial_beam = Beam(np.array((row, board.shape[1] - 1)), MOVE_LEFT)
#         energized_count = do_part_1(board, initial_beam, max_depth=max_depth)
#         energized_counts.append(energized_count)
#     for col in range(1, board.shape[1] - 1):
#         initial_beam = Beam(np.array((1, col)), MOVE_DOWN)
#         energized_count = do_part_1(board, initial_beam, max_depth=max_depth)
#         energized_counts.append(energized_count)
#         initial_beam = Beam(np.array((board.shape[0] - 1, col)), MOVE_UP)
#         energized_count = do_part_1(board, initial_beam, max_depth=max_depth)
#         energized_counts.append(energized_count)
#     maximum = max(energized_counts)
#     return maximum


def update_simulation(
    board: ProblemDataType, beam: Beam, depth: int, max_depth: int, explored: np.ndarray
) -> None:
    if depth > max_depth:
        return
    next_position = beam.position + beam.speed
    coords = tuple(next_position)
    if explored[tuple((EXPLORED_IDX[tuple(beam.speed)], *coords))] == 1:
        return
    explored[tuple((EXPLORED_IDX[tuple(beam.speed)], *coords))] = 1

    cell = board[coords]

    if cell == CELL_EMPTY_SPACE:
        beam.children.append(Beam(next_position, beam.speed))
    elif cell == CELL_MIRROR_FSLASH:
        speed = -beam.speed[::-1]
        beam.children.append(Beam(next_position, speed))
    elif cell == CELL_MIRROR_BSLASH:
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
    elif cell == CELL_WALL:
        # finito for the beam
        ...

    # energy_board = np.copy(board)
    # draw_energized(energy_board, beam, CELL_DIRECTIONS[tuple(beam.speed)])
    # print(render_parsed_input(energy_board))

    for beam in beam.children:
        update_simulation(board, beam, depth + 1, max_depth, explored)
    ...


def draw_energized(
    board: ProblemDataType, beam: Beam, fill_value: bytes
) -> ProblemDataType:
    board[tuple(beam.position)] = fill_value
    for beam in beam.children:
        draw_energized(board, beam, fill_value)


def compute_part_2():
    board = parse_input_text_file()
    result_1 = do_part_2(board, max_depth=2500)
    assert result_1 == 7505
    result_2 = do_part_2(board, max_depth=2700)
    assert result_2 == 7521
    result_22 = do_part_2(board, max_depth=3000)
    assert result_22 == 7521
    result = result_22
    return result


def render_parsed_input(parsed_input: ProblemDataType) -> str:
    return "\n".join(line.tostring().decode() for line in parsed_input)


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    lines = text.strip().split("\n")
    input_array = np.array([np.fromstring(line, dtype="<S1") for line in lines])
    padded = np.pad(input_array, pad_width=1, constant_values=CELL_WALL)
    return padded


if __name__ == "__main__":
    main()
