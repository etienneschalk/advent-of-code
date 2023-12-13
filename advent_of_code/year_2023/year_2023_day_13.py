import numpy as np
import xarray as xr

from advent_of_code.common import load_input_text_file

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
    data = parse_input_text_file()
    ...
    return None


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def summarize_pattern_notes(patterns: ProblemDataType) -> int:
    columns = tuple(find_number_of_cols_above_symmetry_axis(xda) for xda in patterns)
    rows = tuple(find_number_of_rows_above_symmetry_axis(xda) for xda in patterns)

    number_of_columns = sum(columns)
    number_of_rows = sum(rows)

    np.array(rows) + np.array(columns)

    summary = number_of_columns + 100 * number_of_rows
    return summary


def find_number_of_cols_above_symmetry_axis(xda: xr.DataArray) -> int:
    return find_number_of_rows_above_symmetry_axis(xda.T, "col", "row")


def find_number_of_rows_above_symmetry_axis(
    xda: xr.DataArray, row: str = "row", col: str = "col"
) -> int:
    size = xda[row].size
    for idx in range(1, size):
        reflect_length = min(idx, size - idx)
        left = xda[:idx][-reflect_length:].stack(z=(row, col), create_index=False)
        right = xda[idx:][:reflect_length][::-1].stack(z=(row, col), create_index=False)
        identical_reflect = (left == right).all().item()

        if identical_reflect:
            return idx
    return 0


# 24164 too low


def render_2d_data_array(xda: xr.DataArray) -> str:
    return render_2d_numpy_array(xda.data)


def render_2d_numpy_array(data: ProblemDataType) -> str:
    return "\n".join(line.tobytes().decode("utf-8") for line in data)


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
