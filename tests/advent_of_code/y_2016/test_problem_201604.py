import pytest

from advent_of_code.common.store import ExampleInputsStore, ExpectedAnswersStore
from advent_of_code.y_2016.problem_201604 import AdventOfCodeProblem201604


@pytest.mark.integration
def test_integration_201604(expected_answers_2016: ExpectedAnswersStore):
    problem = AdventOfCodeProblem201604()
    assert problem.solve() == expected_answers_2016.retrieve(problem)


def test_problem_202204_part_1(example_inputs_2016: ExampleInputsStore):
    example_input = example_inputs_2016.retrieve(__file__, "example_input")
    parsed = AdventOfCodeProblem201604.parse_text_input(example_input)
    result = AdventOfCodeProblem201604().solve_part_1(parsed)
    assert result == 1514


def test_problem_202204_part_2():
    example_input = "qzmt-zixmtkozy-ivhz-343[tutu]"
    parsed = AdventOfCodeProblem201604.parse_text_input(example_input)
    room_id = int(parsed[0][1])
    string = parsed[0][0]
    string = "".join(
        (" " if c == "-" else chr((((ord(c) - ord("a")) + room_id) % 26) + ord("a")))
        for c in string
    )
    assert string == "very encrypted name"
