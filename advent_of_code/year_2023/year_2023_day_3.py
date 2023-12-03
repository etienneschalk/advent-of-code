from pathlib import Path

import numpy as np
import numpy.typing as npt

DataType = npt.NDArray[np.dtype("|S1")]


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    array = load_input_text_file()
    flattened = compute_adjacent_numbers(array)
    print(flattened)
    answer = sum(flattened)
    return answer


def compute_part_2():
    # games = load_input_text_file()

    answer = None
    return answer


def load_input_text_file() -> DataType:
    input_path = "resources/advent_of_code/year_2023/input_year_2023_day_3.txt"
    input_path = Path(input_path)
    assert input_path.is_file()
    text = input_path.read_text()
    games = parse_text_input(text)
    assert len(games) == 140 + 2
    return games


def parse_text_input(text: str) -> DataType:
    lines = text.strip().split("\n")
    input_array = np.array([np.fromstring(line, dtype="<S1") for line in lines])
    # Add a border of dots will ease later checks,
    # not having to care about data outside the borders
    padded_array = np.pad(input_array, pad_width=1, constant_values=b".")
    return padded_array


def compute_adjacent_numbers(array: DataType) -> list[int]:
    adjacent_numbers_for_row = [
        detect_adjacent_numbers_in_line(array, row_index)
        for row_index in range(array.shape[0])
    ]
    flattened = [j for i in adjacent_numbers_for_row for j in i]
    return flattened


def detect_adjacent_numbers_in_line(array: np.ndarray, row_index: int):
    line = array[row_index]
    digit_was_detected = False
    adjacent_numbers = []
    stack_values = []
    for i in range(line.shape[0]):
        digit_is_detected = line[i].isdigit()
        if digit_is_detected:
            if not digit_was_detected:
                digit_was_detected = True
                col_start = i
            stack_values.append(line[i])
        else:
            if digit_was_detected:
                digit_was_detected = False
                # only the first stack_indices is useful actually
                if not is_solitary_number(array, row_index, col_start, i):
                    number = int("".join(i.decode() for i in stack_values))
                    adjacent_numbers.append(number)
                stack_values.clear()
    return adjacent_numbers


def is_solitary_number(
    array: np.ndarray, row_index: int, col_start_inclusive: int, col_end_exclusive: int
) -> bool:
    # Note: are touching numbers considered as symbols?
    # The current assumption is no.
    if array[row_index, col_start_inclusive - 1] != b".":
        return False
    if array[row_index, col_end_exclusive] != b".":
        return False

    for col in range(col_start_inclusive - 1, col_end_exclusive + 1):
        if array[row_index - 1, col] != b".":
            return False
        if array[row_index + 1, col] != b".":
            return False

    return True


if __name__ == "__main__":
    main()
