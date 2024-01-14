import numpy as np

from advent_of_code.constants import Position
from advent_of_code.year_2023.year_2023_day_23 import (
    AdventOfCodeProblem202323,
    bruteforce_paths_in_exploration_tree,
    compute_all_path_lengths,
    compute_exploration_tree,
    solve_part_2,
)

EXAMPLE_INPUT = """

#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#

"""
EXPECTED_RESULT = """

#S#####################
#OOOOOOO#########...###
#######O#########.#.###
###OOOOO#OOO>.###.#.###
###O#####O#O#.###.#.###
###OOOOO#O#O#.....#...#
###v###O#O#O#########.#
###...#O#O#OOOOOOO#...#
#####.#O#O#######O#.###
#.....#O#O#OOOOOOO#...#
#.#####O#O#O#########v#
#.#...#OOO#OOO###OOOOO#
#.#.#v#######O###O###O#
#...#.>.#...>OOO#O###O#
#####v#.#.###v#O#O###O#
#.....#...#...#O#O#OOO#
#.#########.###O#O#O###
#...###...#...#OOO#O###
###.###.#.###v#####O###
#...#...#.#.>.>.#.>O###
#.###.###.#.###.#.#O###
#.....###...###...#OOO#
#####################O#

"""


def test_year_2023_day_23_part_1():
    test_input = EXAMPLE_INPUT
    hiking_trail = AdventOfCodeProblem202323.parse_text_input(test_input)
    hk = hiking_trail
    starting_position: Position = (1, 2)

    tree = compute_exploration_tree(hk, starting_position)
    bf = bruteforce_paths_in_exploration_tree(tree, 0)

    # It works ^^
    actual_result = compute_all_path_lengths(bf)
    assert actual_result[0] == 94
    assert all(actual_result == np.array([94, 90, 86, 82, 82, 74]))
    ...


def test_year_2023_day_23_part_2():
    test_input = EXAMPLE_INPUT
    hiking_trail = AdventOfCodeProblem202323.parse_text_input(test_input)

    hk = hiking_trail
    target = (5, (22, 20))
    result = solve_part_2(hk, target)
    assert result == 154
