import numpy as np

from advent_of_code.year_2022.year_2022_day_25 import parse_text_input

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


def convert_snafu_to_decimal(snafu: str) -> int:
    base = 5
    components = []
    for index, value in enumerate(reversed(snafu)):
        if value == "-":
            value = -1
        elif value == "=":
            value = -2
        else:
            value = int(value)
        components.append(value * base**index)
    return sum(components)


def convert_decimal_to_snafu(decimal: int) -> str:
    coefs = convert_decimal_to_snafu_ndarray(decimal)
    mapping = {-2: "=", -1: "-", 0: "0", 1: "1", 2: "2"}
    return "".join(mapping[coef] for coef in reversed(coefs)).lstrip("0")


def convert_decimal_to_snafu_ndarray(decimal: int) -> str:
    base = 5
    i = 0
    while decimal % (5**i) != decimal:
        i += 1
    coefs = np.zeros(i + 1, dtype=np.int8)

    remainder = decimal
    orig_remainder = remainder
    while i > 0:
        power = 5**i
        half_power = power // 2
        quotient = remainder // power
        remainder = remainder % power

        if remainder > half_power:
            quotient += 1
            remainder -= power

        if quotient == -3:
            coefs[i + 1] -= 1
            quotient = 2
        if quotient == 3:
            coefs[i + 1] += 1
            quotient = -2
        if quotient == 4:
            coefs[i + 1] += 1
            quotient = -1
        coefs[i] = quotient
        i -= 1

    coefs[0] = remainder
    return coefs


# def convert_decimal_to_snafu(decimal: int) -> str:
#     base = 5
#     i = 0
#     while decimal % (5**i) != decimal:
#         i += 1
#     coefs = np.zeros(i, dtype=np.int8)

#     remainder = decimal
#     orig_remainder = remainder
#     while i != 1:
#         i -= 1
#         power = 5**i
#         quotient = remainder // power
#         remainder = remainder % power
#         half_power = power // 2
#         coefs[i] = quotient
#         if remainder > half_power:
#             quotient += 1
#             remainder -= half_power
#             assert power + half_power + remainder == orig_remainder
#         orig_remainder = remainder

#     ...


def test_year_2022_day_25_part_1():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)

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

    assert not 4890 in range(
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


def test_year_2022_day_25_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
