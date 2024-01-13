import numpy as np
import xarray as xr

from advent_of_code.common import load_input_text_file_from_filename

ProblemDataType = xr.DataArray


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    space_xda = parse_input_text_file()
    expanded_space = expand_space(space_xda)
    adjacency_matrix = compute_adjacency_matrix(expanded_space)
    result = compute_sum_of_shortest_paths_between_pairs(adjacency_matrix)
    # idempotence part 1 part 2
    assert compute_sum_of_shortest_paths_part_2(space_xda, 1) == result
    return result


def compute_part_2():
    space_xda = parse_input_text_file()

    # Do not expand space manually

    result = compute_sum_of_shortest_paths_part_2(space_xda, 1000000 - 1)

    return result


def compute_sum_of_shortest_paths_part_2(
    space_xda: xr.DataArray, expansion_coef: int
) -> int:
    coord_array = create_coord_array(space_xda)
    chunk_coord_array = create_chunk_coord_array(space_xda, coord_array)

    adjacency_matrix = compute_adjacency_matrix(space_xda.compute())
    adjacency_matrix_chunks = compute_adjacency_matrix_from_coord_array(
        chunk_coord_array.compute()
    )

    total_adjacency = adjacency_matrix + expansion_coef * adjacency_matrix_chunks
    result = compute_sum_of_shortest_paths_between_pairs(total_adjacency)
    return result


def compute_sum_of_shortest_paths_between_pairs(adjacency_matrix: np.ndarray) -> int:
    return np.triu(adjacency_matrix).sum()


def create_chunk_coord_array(
    space_xda: xr.DataArray, coord_array: xr.DataArray
) -> xr.DataArray:
    row_chunks = get_compartiments(space_xda, "row", "col")
    col_chunks = get_compartiments(space_xda, "col", "row")

    chunk_coords = []
    for z in coord_array.z:
        row, col = coord_array.isel(z=z)
        chunk_row = find_compartiment_id(row, row_chunks)
        chunk_col = find_compartiment_id(col, col_chunks)
        chunk_coords.append([chunk_row, chunk_col])
    chunk_coord_array = coord_array.copy(data=chunk_coords)
    return chunk_coord_array


def compute_adjacency_matrix(space_xda: xr.DataArray) -> np.ndarray:
    coord_array = create_coord_array(space_xda)
    adjacency_matrix = compute_adjacency_matrix_from_coord_array(coord_array)

    return adjacency_matrix


def compute_adjacency_matrix_from_coord_array(coord_array: xr.DataArray) -> np.ndarray:
    adjacency_matrix = xr.concat(
        [
            np.abs(coord_array.isel(z=i) - coord_array).sum(dim="idx")
            for i in coord_array.z
        ],
        dim="z2",
    )

    return adjacency_matrix


def create_coord_array(space_xda: xr.DataArray) -> xr.DataArray:
    stacked = (space_xda == b"#").stack(z=("row", "col"), create_index=False)
    indices = stacked[stacked]
    coord_array = xr.DataArray(
        np.array([indices.row, indices.col]),
        dims=("idx", "z"),
        coords={"idx": ["row", "col"]},
    ).T

    return coord_array


def expand_space(parsed_input: xr.DataArray) -> xr.DataArray:
    xda = parsed_input
    xda = pad_xda(xda, "col", "row")
    xda = pad_xda(xda, "row", "col")
    return xda


def get_compartiments(xda, chunks_dim: str, dim_reduce: str):
    offset = (xda == b".").all(dim=dim_reduce)
    cs = offset[offset][chunks_dim] + 1
    boundaries = np.pad(cs, (1, 1), constant_values=(0, len(offset)))
    ranges = [
        range(boundaries[i], boundaries[i + 1]) for i in range(len(boundaries) - 1)
    ]
    compartiments = {idx: v for idx, v in enumerate(ranges)}
    return compartiments


def find_compartiment_id(value: int, compartiments: dict[int, range]) -> int:
    return [k for k, v in compartiments.items() if value in v][0]


def get_chunks_tuple(xda, chunks_dim: str, dim_reduce: str):
    offset = (xda == b".").all(dim=dim_reduce)
    cs = offset[offset][chunks_dim] + 1
    c0 = np.roll(np.pad(cs, (0, 1), constant_values=0), 1)
    c1 = np.pad(cs, (0, 1), constant_values=len(offset))
    chunks = c1 - c0
    return tuple(chunks)


def pad_xda(xda: xr.DataArray, dim_reduce: str, dim_concat: str):
    i = 0
    to_concat = []
    to_insert = (xda == b".").all(dim=dim_reduce)
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
    text = load_input_text_file_from_filename(__file__)
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
