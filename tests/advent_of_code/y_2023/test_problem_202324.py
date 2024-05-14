from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2023.problem_202324 import parse_text_input, solve_part_1


def test_problem_202324_part_1(example_inputs_2023: ExampleInputsStore):
    test_input = example_inputs_2023.retrieve(__file__)
    hailstones = parse_text_input(test_input)
    assert [str(h) for h in hailstones] == test_input.strip().replace("  ", " ").split(
        "\n"
    )

    xmin = ymin = 7
    xmax = ymax = 27

    logs = []
    qualified = []

    solve_part_1(hailstones, qualified, xmin, ymin, xmax, ymax, logs=logs)

    actual_log = "\n".join(logs[:-1])
    expected = example_inputs_2023.retrieve(__file__, "EXPECTED_LOG_PART_1")
    assert actual_log == expected.strip()
    assert len(qualified) == 2


def test_problem_202324_part_2(): ...
