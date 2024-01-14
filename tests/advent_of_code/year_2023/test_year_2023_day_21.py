from advent_of_code.year_2023.year_2023_day_21 import (
    count_reached_garden_plots,
    get_starting_position,
    parse_text_input,
    run_steps,
    run_steps_old,
)

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


def test_year_2023_day_21_part_1_naive():
    test_input = EXAMPLE_INPUT
    garden = parse_text_input(test_input)

    initial_pos = get_starting_position(garden)

    max_iter = 6

    history = run_steps_old(garden, initial_pos, max_iter)

    assert count_reached_garden_plots(max_iter, history) == 16
    for index_plus_one, array_string in EXPECTED_PART_1_HISTORY.items():
        assert history[index_plus_one - 1] == array_string


def test_year_2023_day_21_part_1():
    test_input = EXAMPLE_INPUT
    garden = parse_text_input(test_input)

    initial_pos = get_starting_position(garden)

    max_iter = 6

    _, reached = run_steps(garden, initial_pos, max_iter)

    assert len(reached) == 16


def test_year_2023_day_21_part_2():
    # The solution has only be tested on the actual input data.
    # It is not guaranteed to work on the test input data
    # Note: not testing the test input data should ideally remain exceptional.
    pass
