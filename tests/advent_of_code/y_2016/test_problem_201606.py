from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2016.problem_201606 import AdventOfCodeProblem201606


def test_problem_201606_part_1(example_inputs_2016: ExampleInputsStore):
    test_input = example_inputs_2016.retrieve(__file__)
    aoc = AdventOfCodeProblem201606()
    assert aoc.solve_part_1(aoc.parse_text_input(test_input)) == "easter"


def test_problem_201606_part_2(example_inputs_2016: ExampleInputsStore):
    test_input = example_inputs_2016.retrieve(__file__)
    aoc = AdventOfCodeProblem201606()
    assert aoc.solve_part_2(aoc.parse_text_input(test_input)) == "advent"
