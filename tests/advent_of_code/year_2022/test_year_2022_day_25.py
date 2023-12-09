import numpy as np

from advent_of_code.year_2022.year_2022_day_25 import (
    convert_decimal_to_snafu,
    convert_snafu_to_decimal,
    parse_text_input,
)

EXAMPLE_INPUT = """

1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122

"""

EXAMPLE_DECIMAL_TO_SNAFU = {
    1: "1",
    2: "2",
    3: "1=",
    4: "1-",
    5: "10",
    6: "11",
    7: "12",
    8: "2=",
    9: "2-",
    10: "20",
    15: "1=0",
    20: "1-0",
    2022: "1=11-2",
    12345: "1-0---0",
    314159265: "1121-1110-1=0",
}

EXPECTED_SNAFU_TO_DECIMAL = {
    "1=-0-2": 1747,
    "12111": 906,
    "2=0=": 198,
    "21": 11,
    "2=01": 201,
    "111": 31,
    "20012": 1257,
    "112": 32,
    "1=-1=": 353,
    "1-12": 107,
    "12": 7,
    "1=": 3,
    "122": 37,
}


def test_year_2022_day_25_part_1():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    assert parsed_input == list(EXPECTED_SNAFU_TO_DECIMAL.keys())

    example_snafu = "2=-01"
    expected_decimal = 976
    actual_decimal = convert_snafu_to_decimal(example_snafu)
    assert actual_decimal == expected_decimal

    assert all(
        convert_snafu_to_decimal(snafu) == decimal
        for snafu, decimal in EXPECTED_SNAFU_TO_DECIMAL.items()
    )

    expected_decimal_sum = sum(
        convert_snafu_to_decimal(snafu) for snafu in EXPECTED_SNAFU_TO_DECIMAL.keys()
    )
    assert expected_decimal_sum == 4890
    assert all(
        convert_snafu_to_decimal(snafu) == decimal
        for decimal, snafu in EXAMPLE_DECIMAL_TO_SNAFU.items()
    )
    assert convert_snafu_to_decimal("2=-1=0") == expected_decimal_sum
    assert convert_snafu_to_decimal("1-111=") == 1747 + 906
    assert convert_snafu_to_decimal("2--1-") == 906 + 198
    assert convert_snafu_to_decimal("10=-") == 107 + 7
    convert_snafu_to_decimal("022222") == (5**5) // 2
    convert_snafu_to_decimal("1=====") == (5**5) // 2 + 1

    assert 4890 not in range(
        convert_snafu_to_decimal("1====="), convert_snafu_to_decimal("122222")
    )
    assert 4890 in range(
        convert_snafu_to_decimal("2====="), convert_snafu_to_decimal("222222")
    )
    assert 4890 in range(
        convert_snafu_to_decimal("2====="), convert_snafu_to_decimal("200000")
    )
    assert 4890 in range(
        convert_snafu_to_decimal("2====="), convert_snafu_to_decimal("2-----")
    )
    assert 4890 in range(
        convert_snafu_to_decimal("2====="), convert_snafu_to_decimal("2=0000")
    )

    assert (
        np.dot(
            np.array([5**k for k in reversed(range(6))]),
            np.array([2, -2, -1, 1, -2, 0]),
        )
        == expected_decimal_sum
    )

    assert convert_decimal_to_snafu(3) == "1="
    assert convert_decimal_to_snafu(198) == "2=0="
    assert convert_decimal_to_snafu(11) == "21"
    assert convert_decimal_to_snafu(expected_decimal_sum) == "2=-1=0"
    assert convert_decimal_to_snafu(906) == "12111"

    # Decimal to SNAFU
    assert all(
        convert_decimal_to_snafu(decimal) == snafu
        for snafu, decimal in EXPECTED_SNAFU_TO_DECIMAL.items()
    )
    assert all(
        convert_decimal_to_snafu(decimal) == snafu
        for decimal, snafu in EXAMPLE_DECIMAL_TO_SNAFU.items()
    )
    ...
