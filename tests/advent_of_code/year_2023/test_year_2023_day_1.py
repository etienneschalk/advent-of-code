from advent_of_code.year_2023.year_2023_day_1 import (
    build_part_2_mappings,
    correct_input_for_part_2,
    parse_text_input,
    recover_calibration_value,
    replace_first_last_spelled_digits,
)


def test_year_2023_day_1_part_1():
    test_input = """

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

"""
    words = parse_text_input(test_input)

    assert len(words) == 4
    assert recover_calibration_value(words[0]) == 12
    assert recover_calibration_value(words[1]) == 38
    assert recover_calibration_value(words[2]) == 15
    assert recover_calibration_value(words[3]) == 77


def test_year_2023_day_1_part_2():
    test_input = """

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

"""
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
