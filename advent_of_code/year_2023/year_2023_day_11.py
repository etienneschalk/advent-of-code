import numpy as np
import xarray as xr

from advent_of_code.common import load_input_text_file

ProblemDataType = xr.DataArray


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    data = parse_input_text_file()
    expanded_space = expand_space(data)
    adjacency_matrix = compute_adjacency_matrix(expanded_space)
    result = compute_sum_of_shortest_paths_between_pairs(adjacency_matrix)
    return result


def compute_part_2():
    # data = parse_input_text_file()
    ...
    return None


def compute_sum_of_shortest_paths_between_pairs(adjacency_matrix: np.ndarray) -> int:
    return np.triu(adjacency_matrix).sum()


def compute_adjacency_matrix(expanded_space: xr.DataArray) -> np.ndarray:
    stacked = (expanded_space == b"#").stack(z=("row", "col"), create_index=False)
    indices = stacked[stacked]
    coord_array = xr.DataArray(
        np.array([indices.row, indices.col]),
        dims=("idx", "z"),
        coords={"idx": ["row", "col"]},
    ).T
    c = coord_array
    adjacency_matrix = xr.concat(
        ([np.abs(c.isel(z=i) - c).sum(dim="idx") for i in c.z]), dim="z2"
    )

    return adjacency_matrix


def expand_space(parsed_input: xr.DataArray) -> xr.DataArray:
    xda = parsed_input
    xda = pad_xda(xda, "col", "row")
    xda = pad_xda(xda, "row", "col")
    return xda


def pad_xda(xda: xr.DataArray, dim_reduce: str, dim_concat: str):
    i = 0
    to_concat = []
    to_insert = (xda == b".").all(dim=dim_reduce)
    print(f"{to_insert.sum().item()=}")
    for index in to_insert[to_insert][dim_concat].values:
        to_concat.append(xda.sel(**{dim_concat: slice(i, index)}))
        to_concat.append(xda.sel(**{dim_concat: index}))
        i = index + 1
    to_concat.append(xda.sel(**{dim_concat: slice(i, None)}))
    concatenated = xr.concat(to_concat, dim=dim_concat)
    return concatenated.assign_coords(
        **{dim_concat: list(range(len(concatenated[dim_concat])))}
    )


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    lines = text.strip().split("\n")
    input_array = np.array([np.fromstring(line, dtype="<S1") for line in lines])
    return xr.DataArray(
        input_array,
        coords={
            "row": list(range(input_array.shape[0])),
            "col": list(range(input_array.shape[1])),
        },
    )


if __name__ == "__main__":
    main()
