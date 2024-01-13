from advent_of_code.year_2023.year_2023_day_20 import (
    compute_result_for_part_1,
    compute_simulation_history,
    compute_successive_histories_until_circle_back,
    parse_text_input,
)

EXAMPLE_INPUT_1 = """

broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a

"""

EXPECTED_OUTPUT_1 = """

button -low-> broadcaster
broadcaster -low-> a
broadcaster -low-> b
broadcaster -low-> c
a -high-> b
b -high-> c
c -high-> inv
inv -low-> a
a -low-> b
b -low-> c
c -low-> inv
inv -high-> a

""".strip().split("\n")

EXAMPLE_INPUT_2 = """

broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output

"""

EXPECTED_OUTPUT_2_1 = """

button -low-> broadcaster
broadcaster -low-> a
a -high-> inv
a -high-> con
inv -low-> b
con -high-> output
b -high-> con
con -low-> output

""".strip().split("\n")

EXPECTED_OUTPUT_2_2 = """

button -low-> broadcaster
broadcaster -low-> a
a -low-> inv
a -low-> con
inv -high-> b
con -high-> output

""".strip().split("\n")

EXPECTED_OUTPUT_2_3 = """

button -low-> broadcaster
broadcaster -low-> a
a -high-> inv
a -high-> con
inv -low-> b
con -low-> output
b -low-> con
con -high-> output

""".strip().split("\n")

EXPECTED_OUTPUT_2_4 = """

button -low-> broadcaster
broadcaster -low-> a
a -low-> inv
a -low-> con
inv -high-> b
con -high-> output


""".strip().split("\n")


def test_year_2023_day_20_part_1_1():
    test_input = EXAMPLE_INPUT_1
    start_module_dict = parse_text_input(test_input)
    module_dict = parse_text_input(test_input)

    history_1 = compute_simulation_history(module_dict)
    assert [repr(h) for h in history_1] == EXPECTED_OUTPUT_1
    assert module_dict == start_module_dict

    # Circle-back is complete after 1 cycle.

    histories = [history_1]
    result_1 = compute_result_for_part_1(histories, 1000)
    assert result_1 == 32000000


def test_year_2023_day_20_part_1_1bis():
    test_input = EXAMPLE_INPUT_1
    start_module_dict = parse_text_input(test_input)
    module_dict = parse_text_input(test_input)
    histories = compute_successive_histories_until_circle_back(
        start_module_dict, module_dict
    )
    result = compute_result_for_part_1(histories, 1000)
    assert result == 32000000


def test_year_2023_day_20_part_1_2():
    test_input = EXAMPLE_INPUT_2
    start_module_dict = parse_text_input(test_input)
    module_dict = parse_text_input(test_input)

    history_1 = compute_simulation_history(module_dict)
    assert [repr(h) for h in history_1] == EXPECTED_OUTPUT_2_1
    assert module_dict != start_module_dict

    history_2 = compute_simulation_history(module_dict)
    assert [repr(h) for h in history_2] == EXPECTED_OUTPUT_2_2
    assert module_dict != start_module_dict

    history_3 = compute_simulation_history(module_dict)
    assert [repr(h) for h in history_3] == EXPECTED_OUTPUT_2_3
    assert module_dict != start_module_dict

    history_4 = compute_simulation_history(module_dict)
    assert [repr(h) for h in history_4] == EXPECTED_OUTPUT_2_4
    assert module_dict == start_module_dict

    # Circle-back is complete after 4 cycles.

    histories = [history_1, history_2, history_3, history_4]
    result = compute_result_for_part_1(histories, 1000)
    assert result == 11687500


def test_year_2023_day_20_part_1_2bis():
    test_input = EXAMPLE_INPUT_2
    start_module_dict = parse_text_input(test_input)
    module_dict = parse_text_input(test_input)
    histories = compute_successive_histories_until_circle_back(
        start_module_dict, module_dict
    )
    result = compute_result_for_part_1(histories, 1000)
    assert result == 11687500
