from advent_of_code.year_2023.year_2023_day_1 import (
    build_part_2_mapping,
    correct_input_year_2023_day_1,
    parse_input_year_2023_day_1,
    recover_calibration_value,
    substitute_spelled_calibration_digits,
)


def test_year_2023_day_1_part_1():
    test_input = """
    
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

"""
    words = parse_input_year_2023_day_1(test_input)

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
    words = parse_input_year_2023_day_1(test_input)

    assert len(words) == 7

    corrected = correct_input_year_2023_day_1(words)

    assert len(corrected) == 7
    assert recover_calibration_value(corrected[0]) == 29
    assert recover_calibration_value(corrected[1]) == 83
    assert recover_calibration_value(corrected[2]) == 13
    assert recover_calibration_value(corrected[3]) == 24
    assert recover_calibration_value(corrected[4]) == 42
    assert recover_calibration_value(corrected[5]) == 14
    assert recover_calibration_value(corrected[6]) == 76

    assert correct_input_year_2023_day_1(
        [
            "fourtrkdhszg4pjh2goneone",
            "fclsdrjrthreebvjspsoneonefivenpfszjfqcd1",
            # "zheightwotwo5threeqrgbr"
            # "7fjkhndseventwotwonine8four"
            # "qtwone4dffhkjhjrqtwotwo"
            # "298xqtwotwo4fourhhhcblpg"
        ]
    ) == [
        # "4trkdhszg4pjh2gone1",
        "4trkdhszg4pjh2g11",
        "fclsdrjr3bvjspsoneonefivenpfszjfqcd1",
    ]
    # assert recover_calibration_value("fourtrkdhszg4pjh2goneone") == 41
    # assert recover_calibration_value("fclsdrjrthreebvjspsoneonefivenpfszjfqcd1") == 31
    # assert recover_calibration_value("zheightwotwo5threeqrgbr") == 0
    # assert recover_calibration_value("7fjkhndseventwotwonine8four") == 0
    # assert recover_calibration_value("qtwone4dffhkjhjrqtwotwo") == 0
    # assert recover_calibration_value("298xqtwotwo4fourhhhcblpg") == 0


def test_wrong_logic():
    mapping = build_part_2_mapping()

    oneight_list = [
        "soneightninetwo161vhmf",
        "voneightcqkcdvhxh4eight",
        "9qzbqxmqonefiveknrnzpxoneightrq",
        "4btqghfcqx25fivetwo95oneightxf",
        "bgoneightkhgvqbfivefour1seven",
        "tvoneight3xtbvffvthreezcbrgk85eightsixbdgqspftkr",
        "15qhpvsevensixoneightt",
        "7fiveeightoneightvs",
        "fivesevenfour9jslninesevenjtttt7oneightssr",
        "koneightkk7dbtkdmmbf",
        "4ssskfrfqhz9eightfour37oneightjm",
        "25sixjrjqgl5fivekhtxstwovgxzfpvzfmoneightb",
        "onetwonine4noneightvk",
        "honeight5one",
        "mzoneight9995five2bdg",
    ]
    word = oneight_list[0]
    word = "4ssskfrfqhz9eightfour37oneightjm"
    substituted = substitute_spelled_calibration_digits(word, mapping)
    # assert substituted != "4ssskfrfqhz98four37on8jm"
    # assert substituted == "4ssskfrfqhz9eightfour37on8jm"
    assert substituted == "4ssskfrfqhz98four37on8jm"

    word = "onetwonine4noneightvk"
    substituted = substitute_spelled_calibration_digits(word, mapping)
    # assert substituted != "1twonine4n1ightvk"

    # Passing this test is the key
    assert substituted == "1twonine4non8vk"
