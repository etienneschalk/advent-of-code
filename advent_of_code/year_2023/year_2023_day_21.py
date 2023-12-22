import numpy as np
import xarray as xr

from advent_of_code.common import load_input_text_file, render_2d_data_array
from advent_of_code.constants import (
    NEIGHBOUR_MOVES,
    Position,
    is_opposite_direction,
    is_out_of_bounds,
)

ProblemDataType = xr.DataArray


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    garden = parse_input_text_file()
    initial_pos = get_starting_position(garden)
    max_iter = 64
    history = run_steps(garden, initial_pos, max_iter)
    result = count_reached_garden_plots(max_iter, history)
    # 6886 too high
    return result


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
    q.extend((i, pos) for i in range(4))
    history = []
    explored = [
        garden.copy(data=np.zeros_like(garden.data, dtype=np.bool_)) for i in range(4)
    ]
    even_explored = set()
    odd_explored = set()

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
            if explored[from_direction][pos]:
                continue

            explored[from_direction][pos] = True

            for direction, move in NEIGHBOUR_MOVES.items():
                next_pos = move + pos
                next_pos = tuple(next_pos)
                if is_out_of_bounds(direction, pos, garden.shape):
                    continue
                # if is_opposite_direction(direction, from_direction):
                #     continue
                # if garden[next_pos] == b".":
                if garden[next_pos] == b"." or garden[next_pos] == b"S":
                    garden[next_pos] = b"O"
                    q.append((direction, next_pos))
                    if iter_count % 2 == 0:
                        even_explored.add(next_pos)
                    else:
                        odd_explored.add(next_pos)
        to_explore.clear()
        history.append(render_2d_data_array(garden))
        print(history[-1])
    explored_once = xr.concat(explored, dim="z").any(dim="z")
    stacked = explored_once.stack(u=("row", "col"))
    explored_once[::2, 1::2].sum() + explored_once[1::2, ::2].sum()
    explored_once[1::2, 1::2].sum() + explored_once[::2, ::2].sum()

    # This metric is to be used to count
    assert len(even_explored) == 16
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
