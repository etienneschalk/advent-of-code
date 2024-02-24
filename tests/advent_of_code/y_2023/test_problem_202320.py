from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2023.problem_202320 import (
    compute_result_for_part_1,
    compute_simulation_history,
    compute_successive_histories_until_circle_back,
    parse_text_to_module_dict,
)


def test_problem_202320_part_1_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__, "EXAMPLE_INPUT_1")
    expected_output = example_inputs.retrieve(__file__, "EXPECTED_OUTPUT_1")

    start_module_dict = parse_text_to_module_dict(test_input)
    module_dict = parse_text_to_module_dict(test_input)

    history_1 = compute_simulation_history(module_dict)
    assert [repr(h) for h in history_1] == expected_output.strip().split("\n")
    assert module_dict == start_module_dict

    # Circle-back is complete after 1 cycle.

    histories = [history_1]
    result_1 = compute_result_for_part_1(histories, 1000)
    assert result_1 == 32000000


def test_problem_202320_part_1_1bis(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__, "EXAMPLE_INPUT_1")
    start_module_dict = parse_text_to_module_dict(test_input)
    module_dict = parse_text_to_module_dict(test_input)
    histories = compute_successive_histories_until_circle_back(
        start_module_dict, module_dict
    )
    result = compute_result_for_part_1(histories, 1000)
    assert result == 32000000


def test_problem_202320_part_1_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__, "EXAMPLE_INPUT_2")
    expected_output_2_1 = example_inputs.retrieve(__file__, "EXPECTED_OUTPUT_2_1")
    expected_output_2_2 = example_inputs.retrieve(__file__, "EXPECTED_OUTPUT_2_2")
    expected_output_2_3 = example_inputs.retrieve(__file__, "EXPECTED_OUTPUT_2_3")
    expected_output_2_4 = example_inputs.retrieve(__file__, "EXPECTED_OUTPUT_2_4")

    start_module_dict = parse_text_to_module_dict(test_input)
    module_dict = parse_text_to_module_dict(test_input)

    history_1 = compute_simulation_history(module_dict)
    assert [repr(h) for h in history_1] == expected_output_2_1.strip().split("\n")
    assert module_dict != start_module_dict

    history_2 = compute_simulation_history(module_dict)
    assert [repr(h) for h in history_2] == expected_output_2_2.strip().split("\n")
    assert module_dict != start_module_dict

    history_3 = compute_simulation_history(module_dict)
    assert [repr(h) for h in history_3] == expected_output_2_3.strip().split("\n")
    assert module_dict != start_module_dict

    history_4 = compute_simulation_history(module_dict)
    assert [repr(h) for h in history_4] == expected_output_2_4.strip().split("\n")
    assert module_dict == start_module_dict

    # Circle-back is complete after 4 cycles.

    histories = [history_1, history_2, history_3, history_4]
    result = compute_result_for_part_1(histories, 1000)
    assert result == 11687500


def test_problem_202320_part_1_2bis(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__, "EXAMPLE_INPUT_2")
    start_module_dict = parse_text_to_module_dict(test_input)
    module_dict = parse_text_to_module_dict(test_input)
    histories = compute_successive_histories_until_circle_back(
        start_module_dict, module_dict
    )
    result = compute_result_for_part_1(histories, 1000)
    assert result == 11687500
