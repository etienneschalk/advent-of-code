import numpy as np

from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.year_2022.year_2022_day_25 import (
    convert_decimal_to_snafu,
    convert_snafu_to_decimal,
    parse_text_input,
)


def test_year_2022_day_25_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)

    example_snafu_to_decimal = example_inputs.retrieve(
        __file__, "EXPECTED_SNAFU_TO_DECIMAL"
    )
    example_decimal_to_snafu = example_inputs.retrieve(
        __file__, "EXAMPLE_DECIMAL_TO_SNAFU"
    )

    example_snafu_to_decimal = dict(
        ((kv[:6].strip()), int(kv[6:].strip()))
        for kv in example_snafu_to_decimal.strip().split("\n")[1:]
    )
    example_decimal_to_snafu = dict(
        (int(kv[:10].strip()), kv[10:].strip())
        for kv in example_decimal_to_snafu.strip().split("\n")[1:]
    )

    parsed_input = parse_text_input(test_input)
    assert parsed_input == list(example_snafu_to_decimal.keys())

    example_snafu = "2=-01"
    expected_decimal = 976
    actual_decimal = convert_snafu_to_decimal(example_snafu)
    assert actual_decimal == expected_decimal

    assert all(
        convert_snafu_to_decimal(snafu) == decimal
        for snafu, decimal in example_snafu_to_decimal.items()
    )

    expected_decimal_sum = sum(
        convert_snafu_to_decimal(snafu) for snafu in example_snafu_to_decimal.keys()
    )
    assert expected_decimal_sum == 4890
    assert all(
        convert_snafu_to_decimal(snafu) == decimal
        for decimal, snafu in example_decimal_to_snafu.items()
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
        for snafu, decimal in example_snafu_to_decimal.items()
    )
    assert all(
        convert_decimal_to_snafu(decimal) == snafu
        for decimal, snafu in example_decimal_to_snafu.items()
    )
    ...
