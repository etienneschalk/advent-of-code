import numpy as np

from advent_of_code.common.constants import Position
from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2023.problem_202323 import (
    AdventOfCodeProblem202323,
    bruteforce_paths_in_exploration_tree,
    compute_all_path_lengths,
    compute_exploration_tree,
    solve_part_2,
)


def test_problem_202323_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
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


def test_problem_202323_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    hiking_trail = AdventOfCodeProblem202323.parse_text_input(test_input)

    hk = hiking_trail
    target = (5, (22, 20))
    result = solve_part_2(hk, target)
    assert result == 154
