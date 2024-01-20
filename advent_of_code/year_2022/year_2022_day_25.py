import numpy as np
import numpy.typing as npt

from advent_of_code.common import load_input_text_file_from_filename

type ProblemDataType = list[str]


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()

    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    snafus = parse_input_text_file()
    expected_decimal_sum = sum(convert_snafu_to_decimal(snafu) for snafu in snafus)
    snafu_sum = convert_decimal_to_snafu(expected_decimal_sum)
    return snafu_sum


def compute_part_2():
    return None


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
    coefficients = convert_decimal_to_snafu_ndarray(decimal)
    mapping = {-2: "=", -1: "-", 0: "0", 1: "1", 2: "2"}
    return "".join(mapping[coef] for coef in reversed(coefficients)).lstrip("0")


def convert_decimal_to_snafu_ndarray(decimal: int) -> npt.NDArray[np.int8]:
    i = 0

    while decimal % (5**i) != decimal:
        i += 1

    coefficients = np.zeros(i + 1, dtype=np.int8)

    remainder = decimal

    while i > 0:
        power = 5**i
        quotient = remainder // power
        remainder = remainder % power

        if remainder > power // 2:
            quotient += 1
            remainder -= power

        if quotient == -3:
            coefficients[i + 1] -= 1
            quotient = 2
        if quotient == 3:
            coefficients[i + 1] += 1
            quotient = -2
        if quotient == 4:
            coefficients[i + 1] += 1
            quotient = -1
        coefficients[i] = quotient
        i -= 1

    coefficients[0] = remainder
    return coefficients


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file_from_filename(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    lines = text.strip().split("\n")
    ...
    return lines


if __name__ == "__main__":
    main()
