from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2019.problem_201907 import AdventOfCodeProblem201907


def test_problem_201907_part_1(example_inputs_2019: ExampleInputsStore):
    problem = AdventOfCodeProblem201907()

    text_input = example_inputs_2019.retrieve(__file__, "example_input_part_1_1")
    expected_output = example_inputs_2019.retrieve(__file__, "expected_answer_part_1_1")
    assert problem.solve_part_1(problem.parse_text_input(text_input)) == int(
        expected_output
    )

    text_input = example_inputs_2019.retrieve(__file__, "example_input_part_1_2")
    expected_output = example_inputs_2019.retrieve(__file__, "expected_answer_part_1_2")
    assert problem.solve_part_1(problem.parse_text_input(text_input)) == int(
        expected_output
    )

    text_input = example_inputs_2019.retrieve(__file__, "example_input_part_1_3")
    expected_output = example_inputs_2019.retrieve(__file__, "expected_answer_part_1_3")
    assert problem.solve_part_1(problem.parse_text_input(text_input)) == int(
        expected_output
    )


def test_problem_201907_part_2(example_inputs_2019: ExampleInputsStore):
    problem = AdventOfCodeProblem201907()

    text_input = example_inputs_2019.retrieve(__file__, "example_input_part_2_1")
    expected_output = example_inputs_2019.retrieve(__file__, "expected_answer_part_2_1")
    assert problem.solve_part_2(problem.parse_text_input(text_input)) == int(
        expected_output
    )

    text_input = example_inputs_2019.retrieve(__file__, "example_input_part_2_2")
    expected_output = example_inputs_2019.retrieve(__file__, "expected_answer_part_2_2")
    assert problem.solve_part_2(problem.parse_text_input(text_input)) == int(
        expected_output
    )
