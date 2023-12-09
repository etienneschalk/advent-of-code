from functools import reduce
import operator
from advent_of_code.year_2023.year_2023_day_08 import (
    compute_steps_for_part_2,
    count_required_steps,
    count_required_steps_simultaneously_bruteforce,
    detect_loop,
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

EXAMPLE_INPUT_PART_2 = """

LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)

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


def test_year_2023_day_08_part_2_bruteforce():
    test_input = EXAMPLE_INPUT_PART_2
    network_1 = parse_text_input(test_input)
    starts = ("11A", "22A")
    ends = ("11Z", "22Z")

    steps_1 = count_required_steps_simultaneously_bruteforce(network_1, starts, ends)
    assert steps_1 == 6


def test_year_2023_day_08_part_2():
    test_input = EXAMPLE_INPUT_PART_2
    network = parse_text_input(test_input)

    sources = tuple(sorted(key for key in network.nodes.keys() if key.endswith("A")))
    targets = tuple(sorted(key for key in network.nodes.keys() if key.endswith("Z")))

    assert sources == ("11A", "22A")
    assert targets == ("11Z", "22Z")

    steps = compute_steps_for_part_2(network, sources, "Z")

    assert steps == 2 * 3
