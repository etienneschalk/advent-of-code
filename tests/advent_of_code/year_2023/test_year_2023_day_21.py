from advent_of_code.common import render_2d_data_array
from advent_of_code.constants import NEIGHBOUR_MOVES, is_out_of_bounds
from advent_of_code.year_2023.year_2023_day_21 import parse_text_input

EXAMPLE_INPUT = """

...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........

"""

EXPECTED_PART_1_HISTORY = {
    1: """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#O#....
.##.OS####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
    """.strip(),
    2: """
...........
.....###.#.
.###.##..#.
..#.#O..#..
....#.#....
.##O.O####.
.##.O#...#.
.......##..
.##.#.####.
.##..##.##.
...........
    """.strip(),
    3: """
...........
.....###.#.
.###.##..#.
..#.#.O.#..
...O#O#....
.##.OS####.
.##O.#...#.
....O..##..
.##.#.####.
.##..##.##.
...........
    """.strip(),
    6: """
...........
.....###.#.
.###.##.O#.
.O#O#O.O#..
O.O.#.#.O..
.##O.O####.
.##.O#O..#.
.O.O.O.##..
.##.#.####.
.##O.##.##.
...........
    """.strip(),
}


def test_year_2023_day_21_part_1():
    test_input = EXAMPLE_INPUT
    garden = parse_text_input(test_input)
    stacked = garden.stack(z=("row", "col"))
    start_xda = stacked[stacked == b"S"]
    row_idx = start_xda.row.item()
    col_idx = start_xda.col.item()
    initial_pos = (row_idx, col_idx)
    garden[initial_pos] = b"."

    iter_count = 0
    pos = initial_pos
    q = []
    to_explore = []
    q.append(pos)
    max_iter = 6
    history = []
    while iter_count < max_iter:
        iter_count += 1
        to_explore.extend(q)
        q.clear()
        for pos in to_explore:
            garden[pos] = b"." if pos != initial_pos else b"S"
            for direction, move in NEIGHBOUR_MOVES.items():
                next_pos = move + pos
                next_pos = tuple(next_pos)
                if is_out_of_bounds(direction, pos, garden.shape):
                    continue
                if garden[next_pos] == b"." or garden[next_pos] == b"S":
                    garden[next_pos] = b"O"
                    q.append(next_pos)
        to_explore.clear()
        history.append(render_2d_data_array(garden))
        print(history[-1])

    for index_plus_one, array_string in EXPECTED_PART_1_HISTORY.items():
        assert history[index_plus_one - 1] == array_string

    assert history[max_iter - 1].count("O") == 16

    ...


def test_year_2023_day_21_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    ...
