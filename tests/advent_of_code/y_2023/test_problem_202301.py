from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2023.problem_202301 import (
    build_part_2_mappings,
    correct_input_for_part_2,
    parse_text_input,
    recover_calibration_value,
    replace_first_last_spelled_digits,
)


def test_problem_20231_part_1(example_inputs_2023: ExampleInputsStore):
    test_input = example_inputs_2023.retrieve(__file__, "TEST_INPUT_1")

    words = parse_text_input(test_input)

    assert len(words) == 4
    assert recover_calibration_value(words[0]) == 12
    assert recover_calibration_value(words[1]) == 38
    assert recover_calibration_value(words[2]) == 15
    assert recover_calibration_value(words[3]) == 77


def test_problem_20231_part_2(example_inputs_2023: ExampleInputsStore):
    test_input = example_inputs_2023.retrieve(__file__, "TEST_INPUT_2")

    words = parse_text_input(test_input)

    assert len(words) == 7

    corrected = correct_input_for_part_2(words)

    assert len(corrected) == 7
    assert recover_calibration_value(corrected[0]) == 29
    assert recover_calibration_value(corrected[1]) == 83
    assert recover_calibration_value(corrected[2]) == 13
    assert recover_calibration_value(corrected[3]) == 24
    assert recover_calibration_value(corrected[4]) == 42
    assert recover_calibration_value(corrected[5]) == 14
    assert recover_calibration_value(corrected[6]) == 76


def test_do_not_substitute_too_much():
    mappings = build_part_2_mappings()

    word = "4ssskfrfqhz9eightfour37oneightjm"
    substituted = replace_first_last_spelled_digits(word, mappings)
    assert substituted == "4ssskfrfqhz9eightfour37on8jm"

    word = "onetwonine4noneightvk"
    substituted = replace_first_last_spelled_digits(word, mappings)

    # Passing this test is the key
    # oneight
    assert substituted == "1twonine4non8vk"
