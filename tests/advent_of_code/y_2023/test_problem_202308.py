from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2023.problem_202308 import (
    compute_steps_for_part_2,
    count_required_steps,
    count_required_steps_simultaneously_bruteforce,
    parse_text_input,
)


def test_problem_202308_part_1_1(example_inputs: ExampleInputsStore):
    test_input_1 = example_inputs.retrieve(__file__, "EXAMPLE_INPUT_1")
    network_1 = parse_text_input(test_input_1)
    steps_1 = count_required_steps(network_1)
    assert steps_1 == 2


def test_problem_202308_part_1_2(example_inputs: ExampleInputsStore):
    test_input_2 = example_inputs.retrieve(__file__, "EXAMPLE_INPUT_2")
    network_2 = parse_text_input(test_input_2)
    steps_2 = count_required_steps(network_2)
    assert steps_2 == 6


def test_problem_202308_part_2_bruteforce(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__, "EXAMPLE_INPUT_PART_2")
    network_1 = parse_text_input(test_input)
    starts = ("11A", "22A")
    ends = ("11Z", "22Z")

    steps_1 = count_required_steps_simultaneously_bruteforce(network_1, starts, ends)
    assert steps_1 == 6


def test_problem_202308_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__, "EXAMPLE_INPUT_PART_2")
    network = parse_text_input(test_input)

    sources = tuple(sorted(key for key in network.nodes.keys() if key.endswith("A")))
    targets = tuple(sorted(key for key in network.nodes.keys() if key.endswith("Z")))

    assert sources == ("11A", "22A")
    assert targets == ("11Z", "22Z")

    steps = compute_steps_for_part_2(network, sources, "Z")

    assert steps == 2 * 3
