from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2023.problem_202321 import (
    count_reached_garden_plots,
    get_starting_position,
    parse_text_input,
    run_steps,
    run_steps_old,
)


def test_problem_202321_part_1_naive(example_inputs_2023: ExampleInputsStore):
    test_input = example_inputs_2023.retrieve(__file__)
    garden = parse_text_input(test_input)

    initial_pos = get_starting_position(garden)

    max_iter = 6

    history = run_steps_old(garden, initial_pos, max_iter)

    assert count_reached_garden_plots(max_iter, history) == 16
    EXPECTED_PART_1_HISTORY = {
        i: example_inputs_2023.retrieve(
            __file__, f"EXPECTED_PART_1_HISTORY_{i}"
        ).strip()
        for i in (1, 2, 3, 6)
    }
    for index_plus_one, array_string in EXPECTED_PART_1_HISTORY.items():
        assert history[index_plus_one - 1] == array_string


def test_problem_202321_part_1(example_inputs_2023: ExampleInputsStore):
    test_input = example_inputs_2023.retrieve(__file__)
    garden = parse_text_input(test_input)

    initial_pos = get_starting_position(garden)

    max_iter = 6

    _, reached = run_steps(garden, initial_pos, max_iter)

    assert len(reached) == 16


def test_problem_202321_part_2():
    # The solution has only be tested on the actual input data.
    # It is not guaranteed to work on the test input data
    # Note: not testing the test input data should ideally remain exceptional.
    pass
