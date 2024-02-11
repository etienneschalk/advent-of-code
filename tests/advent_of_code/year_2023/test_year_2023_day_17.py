from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.year_2023.year_2023_day_17 import (
    AdventOfCodeProblem202317,
    State,
    dijkstra,
)


def test_year_2023_day_17_misc():
    # Heat excluded from hash, but included in comparison
    assert hash(State(10, (0, 0), 0, 0)) == hash(State(99999, (0, 0), 0, 0))
    assert (State(10, (0, 0), 0, 0)) < (State(99999, (0, 0), 0, 0))
    assert (State(10, (0, 0), 0, 0)) in {(State(10, (0, 0), 0, 0))}
    # Unexpected behaviour: the heat should be ignored from hash... it seems not
    assert (State(10, (0, 0), 0, 0)) not in {(State(99999, (0, 0), 0, 0))}
    # Expected
    assert (State(10, (0, 0), 0, 0)) not in {(State(10, (1, 2), 3, 4))}

    # Workaround: dict of hash
    initial_state = State(10, (0, 0), 0, 0)
    dict_hashmap = {hash(initial_state): initial_state}
    different_heat_state = State(99999, (0, 0), 0, 0)
    assert hash(different_heat_state) == hash(initial_state)
    assert hash(different_heat_state) in dict_hashmap
    assert dict_hashmap[hash(different_heat_state)] == initial_state
    dict_hashmap[hash(different_heat_state)] = different_heat_state
    assert dict_hashmap[hash(different_heat_state)] == different_heat_state


def test_year_2023_day_17_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = AdventOfCodeProblem202317.parse_text_input(test_input)

    start = (0, 0)
    end = tuple((parsed_input.shape[0] - 1, parsed_input.shape[1] - 1))
    end = (end[0], end[1])
    least_heat_loss = dijkstra(parsed_input, start, end, 1, 3)
    assert least_heat_loss == 102


def test_year_2023_day_17_part_2_a(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = AdventOfCodeProblem202317.parse_text_input(test_input)

    start = (0, 0)
    end = tuple((parsed_input.shape[0] - 1, parsed_input.shape[1] - 1))
    end = (end[0], end[1])
    least_heat_loss = dijkstra(parsed_input, start, end, 4, 10)
    assert least_heat_loss == 94


def test_year_2023_day_17_part_2_b(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__, "EXAMPLE_INPUT_PART_2")
    parsed_input = AdventOfCodeProblem202317.parse_text_input(test_input)

    start = (0, 0)
    end = tuple((parsed_input.shape[0] - 1, parsed_input.shape[1] - 1))
    end = (end[0], end[1])
    least_heat_loss = dijkstra(parsed_input, start, end, 4, 10)
    assert least_heat_loss == 71
