from dataclasses import dataclass, field

import numpy as np

from advent_of_code.common import adapt_recursion_limit, load_input_text_file

ProblemDataType = np.ndarray

ROW_AXIS = 0
COL_AXIS = 1


MOVE_NULL = np.array((0, 0))
MOVE_DOWN = np.array((1, 0))
MOVE_RIGHT = np.array((0, 1))
MOVE_UP = np.array((-1, 0))
MOVE_LEFT = np.array((0, -1))

CELL_EMPTY_SPACE = b"."
CELL_MIRROR_FSLASH = b"/"
CELL_MIRROR_BSLASH = b"\\"
CELL_SPLITTER_V = b"|"
CELL_SPLITTER_H = b"-"
CELL_WALL = b"O"
CELL_ENERGY = b"#"

CELL_DIRECTIONS = {
    tuple(MOVE_DOWN): b"v",
    tuple(MOVE_RIGHT): b">",
    tuple(MOVE_UP): b"^",
    tuple(MOVE_LEFT): b"<",
}

EXPLORED_IDX = {
    tuple(MOVE_DOWN): 0,
    tuple(MOVE_RIGHT): 1,
    tuple(MOVE_UP): 2,
    tuple(MOVE_LEFT): 3,
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
    result_one_less_iter = do_part_1(board, max_depth=2499)
    result = do_part_1(board, max_depth=2500)
    result_one_more_iter = do_part_1(board, max_depth=2501)
    assert result_one_less_iter < result
    assert result == result_one_more_iter
    return result


def do_part_1(board: ProblemDataType, max_depth: int = 100) -> int:
    initial_beam = Beam(np.array((1, 0)), MOVE_RIGHT)
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
            beam.children.append(Beam(next_position, MOVE_DOWN))
            beam.children.append(Beam(next_position, MOVE_UP))
    elif cell == CELL_SPLITTER_H:
        if beam.speed[0] == 0:
            beam.children.append(Beam(next_position, beam.speed))
        else:
            beam.children.append(Beam(next_position, MOVE_RIGHT))
            beam.children.append(Beam(next_position, MOVE_LEFT))
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
    data = parse_input_text_file()
    ...
    return None


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
