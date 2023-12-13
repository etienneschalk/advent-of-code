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
    patterns = parse_input_text_file()
    result = summarize_pattern_notes(patterns, smudge_mode=True)
    return result


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)

    # too low 32359
    # next try: 32967 too low
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


def find_number_of_rows_above_symmetry_axis_part_2(
    xda: xr.DataArray, row: str = "row", col: str = "col"
) -> int:
    # Impact of smudge:
    # Start from the candidate symmetry line,
    # and spread 1, then 2, etc. until a line is found (n)
    # at n+1, there is PROBABLY a smudge.
    # fixed smudge should have priority over non-smudge result
    size = xda[row].size
    candidates = [0]
    for idx in range(1, size):
        reflect_length = min(idx, size - idx)
        for spread in range(1, reflect_length + 1):
            left_lim = xda[idx - spread : idx]
            right_lim = xda[idx : idx + spread][::-1]
            upper_line = left_lim[0]
            lower_line = right_lim[0]
            if (upper_line != lower_line).sum() == 1:
                if len(left_lim) == 1 or len(right_lim) == 1:
                    candidates.append(idx)  # can already return
                else:
                    try_subarray = find_number_of_rows_above_symmetry_axis_part_1(
                        xda.drop_sel({row: [idx - spread, idx + spread - 1]}),
                        row,
                        col,
                    )
                    if try_subarray == idx - 1:
                        # This check ensure the correct reflection line is found
                        candidates.append(idx)
                    else:
                        print(
                            f"Warning: danger zone (other possible reflection) {idx=}"
                        )

    return max(candidates)


def find_number_of_rows_above_symmetry_axis_part_1(
    xda: xr.DataArray, row: str = "row", col: str = "col"
) -> int:
    # Impact of smudge:
    # Start from the candidate symmetry line,
    # and spread 1, then 2, etc. until a line is found (n)
    # at n+1, there is PROBABLY a smudge.
    # fixed smudge should have priority over non-smudge result
    size = xda[row].size
    for idx in range(1, size):
        reflect_length = min(idx, size - idx)
        spread = reflect_length
        left = xda[:idx][-spread:].stack(z=(row, col), create_index=False)
        right = xda[idx:][:spread][::-1].stack(z=(row, col), create_index=False)
        identical_reflect = (left == right).all().item()

        if identical_reflect:
            return idx
    return 0


# def find_number_of_rows_above_symmetry_axis(
#     xda: xr.DataArray, row: str = "row", col: str = "col", *, smudge_mode: bool = False
# ) -> int:
#     # Impact of smudge:
#     # Start from the candidate symmetry line,
#     # and spread 1, then 2, etc. until a line is found (n)
#     # at n+1, there is PROBABLY a smudge.
#     # fixed smudge should have priority over non-smudge result
#     size = xda[row].size
#     for idx in range(1, size):
#         reflect_length = min(idx, size - idx)
#         repaired = False
#         current_xda = xda
#         for spread in (
#             range(1, reflect_length + 1) if smudge_mode else (reflect_length,)
#         ):
#             # left_lim = xda[:idx][-spread:]
#             # right_lim = xda[idx:][:spread][::-1]
#             left_lim = current_xda[idx - spread : idx]
#             right_lim = current_xda[idx : idx + spread][::-1]
#             if smudge_mode:
#                 upper_line = left_lim[0]
#                 lower_line = right_lim[0]
#                 if not repaired and (upper_line != lower_line).sum() == 1:
#                     repaired = True
#                     current_xda = current_xda.drop_sel(
#                         {row: [idx - spread, idx + spread]}
#                     )
#                     if left_lim.size == 1 or right_lim.size == 1:
#                         return idx  # can already return
#             if repaired:
#                 left_idx = idx - 1
#                 right_idx = idx - 2
#             else:
#                 left_idx = right_idx = idx

#             left_lim = current_xda[left_idx - spread : left_idx]
#             right_lim = current_xda[right_idx : right_idx + spread][::-1]

#             left = left_lim.stack(z=(row, col), create_index=False)
#             right = right_lim.stack(z=(row, col), create_index=False)
#             identical_reflect = (left == right).all()

#             if identical_reflect and not (smudge_mode and not repaired):
#                 return idx
#         if repaired:
#             idx += 2
#     return 0


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
