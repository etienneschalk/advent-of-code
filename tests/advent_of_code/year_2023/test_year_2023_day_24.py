from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.year_2023.year_2023_day_24 import parse_text_input, solve_part_1


def test_year_2023_day_24_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
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
    expected = example_inputs.retrieve(__file__, "EXPECTED_LOG_PART_1")
    assert actual_log == expected.strip()
    assert len(qualified) == 2


def test_year_2023_day_24_part_2():
    ...
