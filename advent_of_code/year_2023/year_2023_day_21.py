import numpy as np
import xarray as xr

from advent_of_code.common import load_input_text_file, render_2d_data_array
from advent_of_code.constants import NEIGHBOUR_MOVES, Position, is_out_of_bounds

ProblemDataType = xr.DataArray


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    garden = parse_input_text_file()
    initial_pos = get_starting_position(garden)
    max_iter = 64
    history, reached = run_steps(garden, initial_pos, max_iter)
    result = len(reached)
    return result
    # result = count_reached_garden_plots(max_iter, history)
    # 6886 too high
    # return result


def compute_part_2():
    data = parse_input_text_file()

    return None


def count_reached_garden_plots(max_iter: int, history: list[str]):
    return history[max_iter - 1].count("O")


def run_steps(garden: xr.DataArray, initial_pos: Position, max_iter: int):
    iter_count = 0
    pos = initial_pos
    q = []
    to_explore = []
    q.extend([pos])
    history = []
    # Aggressive anti-backtracking
    explored = garden.copy(data=np.zeros_like(garden.data, dtype=np.bool_))
    reached_even = set()
    reached_odd = set()

    while iter_count < max_iter:
        iter_count += 1
        print(iter_count)
        to_explore.extend(q)
        q.clear()
        for pos in to_explore:
            if pos == initial_pos:
                garden[pos] = b"S"
            else:
                garden[pos] = b"."
            if explored[pos]:
                continue

            explored[pos] = True

            for direction, move in NEIGHBOUR_MOVES.items():
                next_pos = move + pos
                next_pos = tuple(next_pos)
                if is_out_of_bounds(direction, pos, garden.shape):
                    continue
                if garden[next_pos] == b"." or garden[next_pos] == b"S":
                    garden[next_pos] = b"O"
                    q.append(next_pos)
                    if iter_count % 2 == 0:
                        reached_even.add(next_pos)
                    else:
                        reached_odd.add(next_pos)
        to_explore.clear()
        history.append(render_2d_data_array(garden))
        print(history[-1])

    # This metric is to be used to count

    if max_iter % 2 == 0:
        return history, reached_even
    else:
        return history, reached_odd


def run_steps_old(garden: xr.DataArray, initial_pos: Position, max_iter: int):
    iter_count = 0
    pos = initial_pos
    q = []
    to_explore = []
    q.extend((i, pos) for i in range(4))
    history = []

    while iter_count < max_iter:
        iter_count += 1
        print(iter_count)
        to_explore.extend(q)
        q.clear()
        for from_direction, pos in to_explore:
            if pos == initial_pos:
                garden[pos] = b"S"
            else:
                garden[pos] = b"."

            for direction, move in NEIGHBOUR_MOVES.items():
                next_pos = move + pos
                next_pos = tuple(next_pos)
                if is_out_of_bounds(direction, pos, garden.shape):
                    continue
                if garden[next_pos] == b"." or garden[next_pos] == b"S":
                    garden[next_pos] = b"O"
                    q.append((direction, next_pos))
        to_explore.clear()
        history.append(render_2d_data_array(garden))
        print(history[-1])

    return history


def get_starting_position(garden):
    stacked = garden.stack(z=("row", "col"))
    start_xda = stacked[stacked == b"S"]
    row_idx = start_xda.row.item()
    col_idx = start_xda.col.item()
    initial_pos = (row_idx, col_idx)
    return initial_pos


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    lines = text.strip().split("\n")
    input_array = np.array([np.fromstring(line, dtype="<S1") for line in lines])
    return xr.DataArray(
        input_array,
        coords={
            "row": list(range(input_array.shape[0])),
            "col": list(range(input_array.shape[1])),
        },
    )


if __name__ == "__main__":
    main()
