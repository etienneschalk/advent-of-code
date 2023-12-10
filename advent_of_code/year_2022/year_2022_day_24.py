from collections import defaultdict

import numpy as np
import xarray as xr

from advent_of_code.common import load_input_text_file

ProblemDataType = np.ndarray
MOVE_NULL = np.array([0, 0])
MOVE_DOWN = np.array([1, 0])
MOVE_UP = -MOVE_DOWN
MOVE_RIGHT = np.array([0, 1])
MOVE_LEFT = -MOVE_RIGHT

ROLL_DOWN = 1
ROLL_UP = -ROLL_DOWN
ROLL_RIGHT = ROLL_DOWN
ROLL_LEFT = -ROLL_RIGHT

ROW_AXIS = 0
COL_AXIS = 1

MAX_ITER = 20

MOVE_STRATEGY_DOWN = [MOVE_DOWN, MOVE_RIGHT, MOVE_NULL, MOVE_LEFT, MOVE_UP]
MOVE_STRATEGY_RIGHT = [MOVE_RIGHT, MOVE_DOWN, MOVE_NULL, MOVE_UP, MOVE_LEFT]


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    data = parse_input_text_file()
    result = build_graph_part_1(data)
    return None


def compute_part_2():
    data = parse_input_text_file()
    ...
    return None


def logic_part_1_first_try(simulation_map: ProblemDataType) -> int:
    blizzard = initialize_blizzard(simulation_map)

    # E is not parsed currently
    initial_pos = np.array([-1, 0])
    # Note : slight preference for moving right (< strict)
    minutes = 0

    pos = initial_pos

    history_pos = []
    history_moves = []

    while True and minutes <= MAX_ITER:
        if pos[0] == blizzard.row.size - 1 and pos[1] == blizzard.col.size - 1:
            print(f"Finishing in {minutes=}")
            break
        minutes += 1

        # Run Blizzard Simulation
        advance_blizzard(blizzard)
        sum_of_blizz = sum(blizzard.values())

        moves = (
            MOVE_STRATEGY_DOWN
            if initial_pos[0] < initial_pos[1]
            else MOVE_STRATEGY_RIGHT
        )
        # It is likely that a recursion will be needed
        for move in moves:
            candidate_pos = pos + move
            free_space = (
                sum_of_blizz.isel(row=candidate_pos[0], col=candidate_pos[1]).item()
                == 0
            )
            if (
                free_space
                and np.all(candidate_pos >= 0)
                and candidate_pos[0] < blizzard.row.size
                and candidate_pos[1] < blizzard.col.size
            ):
                pos = candidate_pos
                history_moves.append(move)
                history_pos.append(pos)
                human_history_moves = render_history_moves(history_moves)
                print(human_history_moves)
                break
        ...
    return minutes


import xarray as xr


# Then this graph must be bfs
def build_graph_part_1(simulation_map: ProblemDataType) -> list[tuple]:
    blizzard_cube = compute_simulation_for_cross_period(simulation_map)
    obstacle_cube = sum(v for v in blizzard_cube.values()).astype(np.bool_)
    free_cube = ~obstacle_cube

    # E is not parsed currently
    initial_pos = np.array([-1, 0])

    graph = defaultdict(list)
    # Start at 1 to avoid entry issue
    build_graph_recursive_part_1(graph, free_cube, 0, initial_pos)
    ...
    # for time in free_cube.time:
    #     build_graph_iterative_part_1[graph, free_cube, time, initial_pos]


def build_graph_recursive_part_1(
    graph: dict[tuple[int, int, int], list[tuple[int, int, int]]],
    free_cube: xr.DataArray,
    time: int,
    initial_pos: np.ndarray,
):
    if time >= free_cube.time.size:
        return
    free_cube_moment = free_cube.isel(time=time)
    children = build_graph_iterative_part_1(free_cube_moment, initial_pos)
    initial_pos_tuple = (time - 1, initial_pos[0], initial_pos[1])
    for child in children:
        child_tuple = (time, child[0], child[1])
        if child_tuple in graph[initial_pos_tuple]:
            continue
        graph[initial_pos_tuple].append(child_tuple)
        build_graph_recursive_part_1(graph, free_cube, time + 1, child)


def build_graph_iterative_part_1(
    free_cube_moment: xr.DataArray,
    initial_pos: np.ndarray,
):
    children_positions = []
    for move in [MOVE_DOWN, MOVE_RIGHT, MOVE_NULL, MOVE_LEFT, MOVE_UP]:
        candidate_pos = initial_pos + move
        if (
            candidate_pos[0] >= 0
            and candidate_pos[1] >= 0
            and candidate_pos[0] < free_cube_moment.row.size
            and candidate_pos[1] < free_cube_moment.col.size
        ):
            free_space = free_cube_moment.isel(
                row=candidate_pos[0], col=candidate_pos[1]
            ).item()
            if free_space:
                children_positions.append(candidate_pos)
    if not children_positions:
        children_positions.append(
            initial_pos
        )  # starting point, there cannot be no move possible except here.
    return children_positions


def compute_simulation_for_cross_period(parsed_input, *, limit: int | None = None):
    blizzard = initialize_blizzard(parsed_input)
    blizzard_list = []
    print(f"{blizzard.row.size=}")
    print(f"{blizzard.col.size=}")
    limit = blizzard.row.size * blizzard.col.size if limit is None else limit
    for i in range(limit):
        blizzard_list.append(blizzard.copy(deep=True))
        advance_blizzard(blizzard)
    if limit == blizzard.row.size * blizzard.col.size:
        assert np.all(sum(blizzard_list[0].values()) == sum(blizzard.values()))
        assert all(v for v in np.all(blizzard_list[0] == blizzard).values())
    blizzard_cube = xr.concat(blizzard_list, dim="time")
    return blizzard_cube


def advance_blizzard(blizzard):
    blizzard["right"] = blizzard.right.roll(col=1)
    blizzard["left"] = blizzard.left.roll(col=-1)
    blizzard["up"] = blizzard.up.roll(row=-1)
    blizzard["down"] = blizzard.down.roll(row=1)


def initialize_blizzard(simulation_map: np.ndarray):
    # Remove walls, they perturbate rolling
    no_walls = simulation_map[1:-1, 1:-1]

    blizzard = xr.Dataset(
        dict(
            right=xr.DataArray(no_walls == b">", dims=["row", "col"]),
            left=xr.DataArray(no_walls == b"<", dims=["row", "col"]),
            down=xr.DataArray(no_walls == b"v", dims=["row", "col"]),
            up=xr.DataArray(no_walls == b"^", dims=["row", "col"]),
        )
    )

    return blizzard


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    lines = text.strip().split("\n")
    input_array = np.array([np.fromstring(line, dtype="<S1") for line in lines])
    return input_array


def render_history_moves(history_moves: list[np.ndarray]) -> list[str]:
    strings = []
    for move in history_moves:
        if np.all(move == MOVE_DOWN):
            string = "move down"
        if np.all(move == MOVE_UP):
            string = "move up"
        if np.all(move == MOVE_RIGHT):
            string = "move right"
        if np.all(move == MOVE_LEFT):
            string = "move left"
        if np.all(move == MOVE_NULL):
            string = "wait"
        strings.append(string)
    return strings


if __name__ == "__main__":
    main()