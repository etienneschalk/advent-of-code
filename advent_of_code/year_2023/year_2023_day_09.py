import numpy as np

from advent_of_code.common import load_input_text_file

ProblemDataType = ...


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    parsed_input = parse_input_text_file()
    predictions = [predict_next_value_forward(arr) for arr in parsed_input]
    return sum(predictions)


def compute_part_2():
    parsed_input = parse_input_text_file()
    predictions = [predict_next_value_backward(arr) for arr in parsed_input]
    return sum(predictions)


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    lines = text.strip().split("\n")
    arrays = (np.fromstring(line, dtype=int, sep=" ") for line in lines)
    stacked = np.stack(list(arrays))
    return stacked


def predict_next_value_forward(arr: np.ndarray) -> int:
    if np.all(arr == 0):
        return 0

    diff = compute_finite_difference_forward(arr)
    next_value = predict_next_value_forward(diff)
    result = arr[-1] + next_value
    return result


def predict_next_value_backward(arr: np.ndarray) -> int:
    if np.all(arr == 0):
        return 0

    diff = compute_finite_difference_forward(arr)
    next_value = predict_next_value_backward(diff)
    result = arr[0] - next_value
    return result


def compute_finite_difference_forward(arr: np.ndarray) -> np.ndarray:
    return (np.roll(arr, -1) - arr)[:-1]


if __name__ == "__main__":
    main()
