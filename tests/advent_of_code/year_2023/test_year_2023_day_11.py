from advent_of_code.year_2023.year_2023_day_11 import (
    compute_adjacency_matrix,
    compute_sum_of_shortest_paths_between_pairs,
    expand_space,
    parse_text_input,
)

EXAMPLE_INPUT = """

...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....

"""

EXAMPLE_EXPECTED_EXPANSION = """

....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......


"""


def test_year_2023_day_11_part_1():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)

    test_expected_expanded = EXAMPLE_EXPECTED_EXPANSION
    expected_expanded = parse_text_input(test_expected_expanded)

    expanded_space = expand_space(parsed_input)
    assert (expanded_space == expected_expanded).all()

    adjacency_matrix = compute_adjacency_matrix(expanded_space)
    assert adjacency_matrix[5 - 1][9 - 1] == adjacency_matrix[9 - 1][5 - 1] == 9
    assert adjacency_matrix[1 - 1][7 - 1] == adjacency_matrix[7 - 1][1 - 1] == 15
    assert adjacency_matrix[3 - 1][6 - 1] == adjacency_matrix[6 - 1][3 - 1] == 17
    assert adjacency_matrix[8 - 1][9 - 1] == adjacency_matrix[9 - 1][8 - 1] == 5

    actual_result = compute_sum_of_shortest_paths_between_pairs(adjacency_matrix)
    assert actual_result == 374


def test_year_2023_day_11_part_2():
    # test_input = EXAMPLE_INPUT
    # parsed_input = parse_text_input(test_input)
    ...
