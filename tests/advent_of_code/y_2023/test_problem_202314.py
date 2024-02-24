import numpy as np

from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2023.problem_202314 import (
    AdventOfCodeProblem202314,
    attain_wanted_state,
    compute_total_load_for_north,
    compute_total_load_from_state_lines,
    compute_total_load_part_1,
    detect_cycle,
    get_list_of_str,
    update_state_for_one_full_rotation,
)


def test_problem_202314_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = AdventOfCodeProblem202314.parse_text_input(test_input)
    list_of_str = get_list_of_str(parsed_input, 3)
    total_load = compute_total_load_part_1(list_of_str)
    assert total_load == 136


def test_problem_202314_part_1_refactored(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = AdventOfCodeProblem202314.parse_text_input(test_input)
    total_load = compute_total_load_for_north(parsed_input)
    assert total_load == 136


def test_problem_202314_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = AdventOfCodeProblem202314.parse_text_input(test_input)

    expected_1 = (
        example_inputs.retrieve(__file__, "EXPECTED_PART_2_1_CYCLE").strip().split("\n")
    )
    expected_2 = (
        example_inputs.retrieve(__file__, "EXPECTED_PART_2_2_CYCLE").strip().split("\n")
    )
    expected_3 = (
        example_inputs.retrieve(__file__, "EXPECTED_PART_2_3_CYCLE").strip().split("\n")
    )
    init_rot = 4

    after_one_cycle = update_state_for_one_full_rotation(parsed_input, init_rot)
    assert get_list_of_str(after_one_cycle, 0) == expected_1
    after_two_cycles = update_state_for_one_full_rotation(after_one_cycle, init_rot)
    assert get_list_of_str(after_two_cycles, 0) == expected_2
    after_three_cycles = update_state_for_one_full_rotation(after_two_cycles, init_rot)
    assert get_list_of_str(after_three_cycles, 0) == expected_3


def test_problem_202314_part_2_more_iter(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = AdventOfCodeProblem202314.parse_text_input(test_input)

    init_rot = 4

    max_iter = 32
    state = parsed_input
    state_history = [state]
    for i in range(max_iter):
        state = update_state_for_one_full_rotation(state, init_rot)
        state_history.append(state.flatten().tostring())

    # Period of T=7 does appear at some point
    empirical_period = 7  # by reading the state_history
    assert state_history[8] != state_history[8 - empirical_period]
    assert state_history[9] != state_history[9 - empirical_period]
    assert state_history[10] == state_history[10 - empirical_period]
    for k in range(10, 32):
        assert state_history[k] == state_history[k - empirical_period]
    ...


def test_problem_202314_part_2_validate_problem_description(
    example_inputs: ExampleInputsStore,
):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = AdventOfCodeProblem202314.parse_text_input(test_input)

    init_rot = 4
    max_iter = 32
    state = parsed_input

    search_result = detect_cycle(init_rot, max_iter, state)
    start, period, state_history = search_result

    assert start == 3
    assert period == 7

    state_wanted = attain_wanted_state(1000000000, start, period, state_history)

    # It is not by chance...
    assert np.all(state_wanted == state_history[3])

    state_lines = get_list_of_str(state_wanted, 0)
    total_load = compute_total_load_from_state_lines(state_lines)

    assert total_load == 64
    ...
