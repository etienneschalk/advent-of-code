from dataclasses import asdict
from advent_of_code.common import save_txt
from advent_of_code.constants import Position
from advent_of_code.year_2023.year_2023_day_23 import (
    compute_exploration_tree,
    parse_text_input,
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
    hiking_trail = parse_text_input(test_input)
    hk = hiking_trail
    starting_position: Position = (1, 2)

    tree = compute_exploration_tree(hk, starting_position)
    dico = asdict(tree)

    import json

    txt = json.dumps(dico, indent=4, default=str)

    save_txt(
        txt,
        f"part1.json",
        __file__,
        output_subdir="text",
    )
    ...


def test_year_2023_day_23_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    ...
