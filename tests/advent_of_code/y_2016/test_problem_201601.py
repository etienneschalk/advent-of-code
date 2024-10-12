from ast import literal_eval

from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2016.problem_201601 import AdventOfCodeProblem201601


def test_problem_202201_part_1(example_inputs_2016: ExampleInputsStore):
    test_inputs = example_inputs_2016.retrieve(__file__, "example_inputs_part_1")
    test_inputs = literal_eval(test_inputs)
    problem = AdventOfCodeProblem201601()
    for test_input, expected_result in test_inputs.items():
        parsed_input = problem.parse_text_input(test_input)
        assert problem.solve_part_1(parsed_input) == expected_result
