from advent_of_code.year_2023.year_2023_day_08 import (
    count_required_steps,
    parse_text_input,
)

EXAMPLE_INPUT_1 = """

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)


"""


EXAMPLE_INPUT_2 = """

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)

"""


def test_year_2023_day_08_part_1():
    test_input_1 = EXAMPLE_INPUT_1
    network_1 = parse_text_input(test_input_1)
    steps_1 = count_required_steps(network_1)
    assert steps_1 == 2

    test_input_2 = EXAMPLE_INPUT_2
    network_2 = parse_text_input(test_input_2)
    steps_2 = count_required_steps(network_2)
    assert steps_2 == 6


def test_year_2023_day_08_part_2():
    test_input = EXAMPLE_INPUT_1
    parsed_input = parse_text_input(test_input)
