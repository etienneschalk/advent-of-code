import numpy as np
import xarray as xr

from advent_of_code.common import load_input_text_file_from_filename

ProblemDataType = tuple[xr.DataArray]


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    patterns = parse_input_text_file()
    result = summarize_pattern_notes(patterns)
    return result


def compute_part_2():
    patterns = parse_input_text_file()
    result = summarize_pattern_notes(patterns, smudge_mode=True)
    return result


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file_from_filename(__file__)
    parsed = parse_text_input(text)

    # too low 32359
    # next try: 32967 too low
    # next try try: 33054
    # Lesson learned: don't spend 2 hours over-thinking
    # Take a break
    # Think
    # And change one single line of code to solve the problem
    return parsed


def summarize_pattern_notes(
    patterns: ProblemDataType, *, smudge_mode: bool = False
) -> int:
    columns, rows = compute_symmetry_amounts(patterns, smudge_mode=smudge_mode)

    number_of_columns = sum(columns)
    number_of_rows = sum(rows)

    np.array(rows) + np.array(columns)

    summary = number_of_columns + 100 * number_of_rows
    return summary


def compute_symmetry_amounts(
    patterns: ProblemDataType, *, smudge_mode: bool = False
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    columns = tuple(
        find_number_of_cols_above_symmetry_axis(xda, smudge_mode=smudge_mode)
        for xda in patterns
    )
    rows = tuple(
        find_number_of_rows_above_symmetry_axis(xda, smudge_mode=smudge_mode)
        for xda in patterns
    )

    return columns, rows


def find_number_of_cols_above_symmetry_axis(
    xda: xr.DataArray, *, smudge_mode: bool = False
) -> int:
    if not smudge_mode:
        return find_number_of_rows_above_symmetry_axis_part_1(xda.T, "col", "row")
    else:
        return find_number_of_rows_above_symmetry_axis_part_2(xda.T, "col", "row")


def find_number_of_rows_above_symmetry_axis(
    xda: xr.DataArray, *, smudge_mode: bool = False
) -> int:
    if not smudge_mode:
        return find_number_of_rows_above_symmetry_axis_part_1(xda)
    else:
        return find_number_of_rows_above_symmetry_axis_part_2(xda)


def find_number_of_rows_above_symmetry_axis_part_1(
    xda: xr.DataArray, row: str = "row", col: str = "col"
) -> int:
    return find_number_of_rows_above_symmetry_axis_both_parts(xda, 0, row, col)


def find_number_of_rows_above_symmetry_axis_part_2(
    xda: xr.DataArray, row: str = "row", col: str = "col"
) -> int:
    return find_number_of_rows_above_symmetry_axis_both_parts(xda, 1, row, col)


def find_number_of_rows_above_symmetry_axis_both_parts(
    xda: xr.DataArray,
    target_sum: int,
    row: str = "row",
    col: str = "col",
) -> int:
    size = xda[row].size
    for idx in range(1, size):
        reflect_length = min(idx, size - idx)
        spread = reflect_length
        left = xda[:idx][-spread:].stack(z=(row, col), create_index=False)
        right = xda[idx:][:spread][::-1].stack(z=(row, col), create_index=False)
        identical_reflect = (left != right).sum() == target_sum

        if identical_reflect:
            return idx
    return 0


def numpy_to_xarray(numpy_array: np.ndarray) -> xr.DataArray:
    return xr.DataArray(
        numpy_array,
        coords={
            "row": list(range(numpy_array.shape[0])),
            "col": list(range(numpy_array.shape[1])),
        },
    )


def parse_text_input(text: str) -> ProblemDataType:
    lines = text.strip().split("\n\n")
    input_arrays = (
        np.array(
            [np.frombuffer(line.encode(), dtype="u1") for line in block.split("\n")]
        )
        for block in lines
    )
    data_arrays = tuple(numpy_to_xarray(arr) for arr in input_arrays)
    return data_arrays


if __name__ == "__main__":
    main()
