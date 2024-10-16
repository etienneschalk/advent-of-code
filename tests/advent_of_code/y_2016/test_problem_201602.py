from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2016.problem_201602 import AdventOfCodeProblem201602


def test_problem_202201_part_1(example_inputs_2016: ExampleInputsStore):
    example_input = example_inputs_2016.retrieve(__file__, "example_input")
    # 1 2 3
    # 4 5 6
    # 7 8 9
    result = AdventOfCodeProblem201602().solve_part_1(example_input)
    assert result == "1985"


def test_problem_202201_part_2(example_inputs_2016: ExampleInputsStore):
    example_input = example_inputs_2016.retrieve(__file__, "example_input")
    #     1
    #   2 3 4
    # 5 6 7 8 9
    #   A B C
    #     D
    result = AdventOfCodeProblem201602().solve_part_2(example_input)
    assert result == "5DB3"
